"""
MLP-Mixer implementation for token and channel mixing.
"""

from typing import Optional
import torch
import torch.nn as nn


class MLPMixerLayer(nn.Module):
    """Single MLP-Mixer layer with token-mixing and channel-mixing MLPs."""
    
    def __init__(self, hidden_size: int, max_seq_len: int, expansion_factor: int = 4):
        super().__init__()
        self.hidden_size = hidden_size
        self.max_seq_len = max_seq_len
        
        # Layer normalization
        self.norm1 = nn.LayerNorm(hidden_size)
        self.norm2 = nn.LayerNorm(hidden_size)
        
        # Token-mixing MLP (operates along sequence dimension)
        self.token_mixing = nn.Sequential(
            nn.Linear(max_seq_len, max_seq_len * expansion_factor),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(max_seq_len * expansion_factor, max_seq_len),
            nn.Dropout(0.1)
        )
        
        # Channel-mixing MLP (operates along feature dimension)
        self.channel_mixing = nn.Sequential(
            nn.Linear(hidden_size, hidden_size * expansion_factor),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_size * expansion_factor, hidden_size),
            nn.Dropout(0.1)
        )
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass of MLP-Mixer layer.
        
        Args:
            x: Input tensor of shape [batch_size, seq_len, hidden_size]
            
        Returns:
            Output tensor of same shape
        """
        batch_size, seq_len, hidden_size = x.shape
        
        # Pad sequence to max_seq_len if needed
        if seq_len < self.max_seq_len:
            padding = torch.zeros(batch_size, self.max_seq_len - seq_len, hidden_size, 
                                device=x.device, dtype=x.dtype)
            x_padded = torch.cat([x, padding], dim=1)
        else:
            x_padded = x[:, :self.max_seq_len, :]
        
        # Token-mixing: Apply MLP along sequence dimension
        residual = x_padded
        x_norm = self.norm1(x_padded)
        
        # Transpose to [batch_size, hidden_size, seq_len] for token mixing
        x_transposed = x_norm.transpose(1, 2)
        token_mixed = self.token_mixing(x_transposed)
        token_mixed = token_mixed.transpose(1, 2)  # Back to [batch_size, seq_len, hidden_size]
        
        x_padded = residual + token_mixed
        
        # Channel-mixing: Apply MLP along feature dimension
        residual = x_padded
        x_norm = self.norm2(x_padded)
        channel_mixed = self.channel_mixing(x_norm)
        x_padded = residual + channel_mixed
        
        # Remove padding if it was added
        if seq_len < self.max_seq_len:
            return x_padded[:, :seq_len, :]
        else:
            return x_padded


class MLPMixer(nn.Module):
    """
    MLP-Mixer architecture for replacing the final linear layer in transformers.
    
    This module applies alternating token-mixing and channel-mixing operations
    to process the hidden states and output embeddings with an additional
    dimension for rotary regression.
    """
    
    def __init__(
        self, 
        hidden_size: int, 
        num_layers: int = 2, 
        max_seq_len: int = 30,
        output_size: Optional[int] = None,
        expansion_factor: int = 4
    ):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.max_seq_len = max_seq_len
        self.output_size = output_size or hidden_size
        
        # Stack of MLP-Mixer layers
        self.layers = nn.ModuleList([
            MLPMixerLayer(hidden_size, max_seq_len, expansion_factor)
            for _ in range(num_layers)
        ])
        
        # Final output projection to desired size (embedding_size + 1)
        self.output_projection = nn.Linear(hidden_size, self.output_size)
        
        # Layer normalization before output
        self.final_norm = nn.LayerNorm(hidden_size)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through MLP-Mixer.
        
        Args:
            x: Input tensor [batch_size, seq_len, hidden_size]
            
        Returns:
            Output tensor [batch_size, seq_len, output_size]
        """
        # Pass through mixer layers
        for layer in self.layers:
            x = layer(x)
        
        # Final normalization and projection
        x = self.final_norm(x)
        x = self.output_projection(x)
        
        return x
    
    def get_mixer_stats(self, x: torch.Tensor) -> dict:
        """
        Get statistics about the mixing process for debugging/analysis.
        
        Args:
            x: Input tensor
            
        Returns:
            Dictionary with mixing statistics
        """
        stats = {}
        
        # Initial statistics
        stats['input_mean'] = x.mean().item()
        stats['input_std'] = x.std().item()
        
        # Pass through layers and collect stats
        for i, layer in enumerate(self.layers):
            x = layer(x)
            stats[f'layer_{i}_mean'] = x.mean().item()
            stats[f'layer_{i}_std'] = x.std().item()
        
        # Final output stats
        x = self.final_norm(x)
        x = self.output_projection(x)
        stats['output_mean'] = x.mean().item()
        stats['output_std'] = x.std().item()
        
        return stats


class AdaptiveMixer(nn.Module):
    """
    Adaptive MLP-Mixer that can handle variable sequence lengths more efficiently.
    
    This variant uses adaptive token mixing that doesn't require fixed max_seq_len.
    """
    
    def __init__(
        self,
        hidden_size: int,
        num_layers: int = 2,
        output_size: Optional[int] = None,
        expansion_factor: int = 4
    ):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.output_size = output_size or hidden_size
        
        # Adaptive mixer layers
        self.layers = nn.ModuleList([
            AdaptiveMixerLayer(hidden_size, expansion_factor)
            for _ in range(num_layers)
        ])
        
        # Output projection
        self.output_projection = nn.Linear(hidden_size, self.output_size)
        self.final_norm = nn.LayerNorm(hidden_size)
    
    def forward(self, x: torch.Tensor, attention_mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        Forward pass with optional attention mask for variable lengths.
        
        Args:
            x: Input tensor [batch_size, seq_len, hidden_size]
            attention_mask: Optional mask [batch_size, seq_len]
            
        Returns:
            Output tensor [batch_size, seq_len, output_size]
        """
        for layer in self.layers:
            x = layer(x, attention_mask)
        
        x = self.final_norm(x)
        x = self.output_projection(x)
        
        return x


class AdaptiveMixerLayer(nn.Module):
    """Adaptive mixer layer that handles variable sequence lengths."""
    
    def __init__(self, hidden_size: int, expansion_factor: int = 4):
        super().__init__()
        self.hidden_size = hidden_size
        
        # Layer normalization
        self.norm1 = nn.LayerNorm(hidden_size)
        self.norm2 = nn.LayerNorm(hidden_size)
        
        # Token mixing using 1D convolution (more flexible than fixed linear layer)
        self.token_mixing = nn.Sequential(
            nn.Conv1d(hidden_size, hidden_size * expansion_factor, kernel_size=1),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Conv1d(hidden_size * expansion_factor, hidden_size, kernel_size=1),
            nn.Dropout(0.1)
        )
        
        # Channel mixing MLP
        self.channel_mixing = nn.Sequential(
            nn.Linear(hidden_size, hidden_size * expansion_factor),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_size * expansion_factor, hidden_size),
            nn.Dropout(0.1)
        )
    
    def forward(self, x: torch.Tensor, attention_mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        Forward pass of adaptive mixer layer.
        
        Args:
            x: Input tensor [batch_size, seq_len, hidden_size]
            attention_mask: Optional mask [batch_size, seq_len]
            
        Returns:
            Output tensor [batch_size, seq_len, hidden_size]
        """
        # Token mixing
        residual = x
        x_norm = self.norm1(x)
        
        # Apply convolution along sequence dimension
        # Transpose to [batch_size, hidden_size, seq_len] for conv1d
        x_conv = x_norm.transpose(1, 2)
        token_mixed = self.token_mixing(x_conv)
        token_mixed = token_mixed.transpose(1, 2)  # Back to [batch_size, seq_len, hidden_size]
        
        # Apply attention mask if provided
        if attention_mask is not None:
            token_mixed = token_mixed * attention_mask.unsqueeze(-1)
        
        x = residual + token_mixed
        
        # Channel mixing
        residual = x
        x_norm = self.norm2(x)
        channel_mixed = self.channel_mixing(x_norm)
        
        if attention_mask is not None:
            channel_mixed = channel_mixed * attention_mask.unsqueeze(-1)
        
        x = residual + channel_mixed
        
        return x
