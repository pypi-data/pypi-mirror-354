"""
Rotary Regression implementation for position analysis and sequence termination.
"""

import math
from typing import Optional, Tuple
import torch
import torch.nn as nn


def apply_rotary_pos_emb(x: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor) -> torch.Tensor:
    """
    Apply rotary position embedding to input tensor.
    
    Args:
        x: Input tensor [batch_size, seq_len, dim]
        cos: Cosine values [seq_len, dim//2]
        sin: Sine values [seq_len, dim//2]
        
    Returns:
        Tensor with rotary position encoding applied
    """
    # Split x into two halves
    x1, x2 = x.chunk(2, dim=-1)
    
    # Apply rotation
    rotated = torch.cat([
        x1 * cos - x2 * sin,
        x2 * cos + x1 * sin
    ], dim=-1)
    
    return rotated


class RotaryEmbedding(nn.Module):
    """Rotary position embedding layer."""
    
    def __init__(self, dim: int, max_seq_len: int = 2048, base: float = 10000.0):
        super().__init__()
        self.dim = dim
        self.max_seq_len = max_seq_len
        self.base = base
        
        # Precompute frequency values
        inv_freq = 1.0 / (base ** (torch.arange(0, dim, 2).float() / dim))
        self.register_buffer('inv_freq', inv_freq)
        
        # Precompute cos and sin values for efficiency
        self._precompute_freqs(max_seq_len)
    
    def _precompute_freqs(self, seq_len: int):
        """Precompute cosine and sine values for given sequence length."""
        t = torch.arange(seq_len).type_as(self.inv_freq)
        freqs = torch.outer(t, self.inv_freq)
        
        # Create cos and sin tables
        cos = torch.cos(freqs)
        sin = torch.sin(freqs)
        
        self.register_buffer('cos_cached', cos)
        self.register_buffer('sin_cached', sin)
    
    def forward(self, seq_len: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """Get cosine and sine values for the given sequence length."""
        if seq_len > self.max_seq_len:
            self._precompute_freqs(seq_len)
        
        return self.cos_cached[:seq_len], self.sin_cached[:seq_len]


class RotaryRegression(nn.Module):
    """
    Rotary Regression module for analyzing position information and determining
    sequence termination points.
    """
    
    def __init__(self, dim: int, max_seq_len: int = 2048, base: float = 10000.0):
        super().__init__()
        self.dim = dim
        self.max_seq_len = max_seq_len
        
        # Rotary embedding for analysis
        self.rotary_embed = RotaryEmbedding(dim, max_seq_len, base)
        
        # Position analysis network
        self.position_analyzer = nn.Sequential(
            nn.Linear(1, dim),
            nn.LayerNorm(dim),
            nn.GELU(),
            nn.Linear(dim, dim // 2),
            nn.GELU(),
            nn.Linear(dim // 2, 1),
            nn.Sigmoid()
        )
        
        # Learned termination patterns
        self.termination_classifier = nn.Sequential(
            nn.Linear(dim + 1, dim),
            nn.LayerNorm(dim),
            nn.GELU(),
            nn.Linear(dim, dim // 4),
            nn.GELU(),
            nn.Linear(dim // 4, 1),
            nn.Sigmoid()
        )
        
        # Learnable parameters
        self.position_threshold = nn.Parameter(torch.tensor(0.5))
        self.termination_sensitivity = nn.Parameter(torch.tensor(1.0))
    
    def forward(self, rotary_component: torch.Tensor, position_ids: torch.Tensor) -> torch.Tensor:
        """Main forward pass of rotary regression."""
        # Analyze position information
        position_scores = self.position_analyzer(rotary_component)
        
        # Get rotary features for termination analysis
        cos, sin = self.rotary_embed(rotary_component.size(1))
        
        if position_ids.dim() == 1:
            position_ids = position_ids.unsqueeze(0).expand(rotary_component.size(0), -1)
        
        pos_indices = position_ids.clamp(0, cos.size(0) - 1)
        cos_pos = cos[pos_indices]
        sin_pos = sin[pos_indices]
        rotary_features = torch.cat([cos_pos, sin_pos], dim=-1)
        
        # Combine features
        combined_features = torch.cat([rotary_features, rotary_component], dim=-1)
        termination_scores = self.termination_classifier(combined_features)
        
        # Combine position and termination analysis
        combined_scores = position_scores * (1 - termination_scores * self.termination_sensitivity)
        
        return combined_scores
