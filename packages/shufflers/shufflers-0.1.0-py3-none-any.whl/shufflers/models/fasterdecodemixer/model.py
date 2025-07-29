"""
FasterDecodeMixer: Main model implementation combining Transformer + MLP-Mixer + Rotary Regression.
"""

from typing import Optional, Tuple, Union
import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers.modeling_outputs import CausalLMOutputWithPast

from ..shufflelm import ShuffleLM, ShuffleConfig
from .mixer import MLPMixer
from .rotary import RotaryRegression


class TransformerBlock(nn.Module):
    """Standard transformer decoder block."""
    
    def __init__(self, config: ShuffleConfig):
        super().__init__()
        self.ln_1 = nn.LayerNorm(config.hidden_size, eps=config.layer_norm_eps)
        self.attn = nn.MultiheadAttention(
            config.hidden_size,
            config.num_heads,
            dropout=config.attention_dropout,
            batch_first=True
        )
        self.ln_2 = nn.LayerNorm(config.hidden_size, eps=config.layer_norm_eps)
        self.mlp = nn.Sequential(
            nn.Linear(config.hidden_size, config.intermediate_size),
            nn.GELU(),
            nn.Linear(config.intermediate_size, config.hidden_size),
            nn.Dropout(config.dropout)
        )
        
    def forward(self, x, attention_mask=None):
        # Self-attention with residual connection
        residual = x
        x = self.ln_1(x)
        
        # Apply causal mask for autoregressive generation
        seq_len = x.size(1)
        causal_mask = torch.triu(torch.ones(seq_len, seq_len), diagonal=1).bool()
        causal_mask = causal_mask.to(x.device)
        
        attn_output, _ = self.attn(x, x, x, attn_mask=causal_mask)
        x = residual + attn_output
        
        # Feed-forward with residual connection
        residual = x
        x = self.ln_2(x)
        x = residual + self.mlp(x)
        
        return x


class FasterDecodeMixer(ShuffleLM):
    """
    FasterDecodeMixer: Enhanced Transformer with MLP-Mixer and Rotary Regression.
    
    This model replaces the final linear layer of a standard transformer decoder
    with an MLP-Mixer that outputs (embedding_size + 1) dimensions, where the
    extra dimension is used for Rotary Regression to determine token validity
    and sequence termination.
    """
    
    def __init__(self, config: ShuffleConfig):
        super().__init__(config)
        
        # MLP-Mixer replacing the final linear layer
        self.mixer = MLPMixer(
            hidden_size=config.hidden_size,
            num_layers=2,  # Small mixer for efficiency
            max_seq_len=config.max_parallel_tokens,
            output_size=config.hidden_size + 1  # +1 for rotary regression
        )
        
        # Rotary regression for position analysis
        self.rotary_regression = RotaryRegression(
            dim=config.rotary_dim,
            max_seq_len=config.max_parallel_tokens
        )
        
        # Output projection to vocabulary
        self.lm_head = nn.Linear(config.hidden_size, config.vocab_size, bias=False)
        
        # Initialize weights
        self.post_init()
    
    def _create_layer(self) -> nn.Module:
        """Create a transformer block."""
        return TransformerBlock(self.config)
    
    def forward(
        self,
        input_ids: Optional[torch.LongTensor] = None,
        attention_mask: Optional[torch.FloatTensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        labels: Optional[torch.LongTensor] = None,
        return_dict: Optional[bool] = None,
        **kwargs
    ):
        """Forward pass of FasterDecodeMixer."""
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict
        
        batch_size, seq_len = input_ids.shape
        device = input_ids.device
        
        # Token embeddings
        token_embeds = self.token_embedding(input_ids)
        
        # Position embeddings
        if position_ids is None:
            position_ids = torch.arange(seq_len, device=device).unsqueeze(0)
        pos_embeds = self.position_embedding(position_ids)
        
        # Combine embeddings
        hidden_states = token_embeds + pos_embeds
        hidden_states = self.dropout(hidden_states)
        
        # Pass through transformer layers
        for layer in self.layers:
            hidden_states = layer(hidden_states, attention_mask)
        
        # Final layer norm
        hidden_states = self.ln_f(hidden_states)
        
        # MLP-Mixer transformation (embedding_size + 1)
        mixer_output = self.mixer(hidden_states)
        
        # Split into token representation and rotary component
        token_repr = mixer_output[..., :-1]  # First embedding_size dimensions
        rotary_component = mixer_output[..., -1:]  # Last dimension
        
        # Apply rotary regression for position analysis
        position_scores = self.rotary_regression(rotary_component, position_ids)
        
        # Get logits for vocabulary
        logits = self.lm_head(token_repr)
        
        loss = None
        if labels is not None:
            # Calculate loss for both token prediction and position scoring
            shift_logits = logits[..., :-1, :].contiguous()
            shift_labels = labels[..., 1:].contiguous()
            
            # Token prediction loss
            token_loss = F.cross_entropy(
                shift_logits.view(-1, shift_logits.size(-1)),
                shift_labels.view(-1),
                ignore_index=-100
            )
            
            # Position scoring loss (optional, for training the termination signal)
            # This could be trained to predict sentence boundaries
            position_loss = 0  # Placeholder for position-based loss
            
            loss = token_loss + 0.1 * position_loss  # Weighted combination
        
        if not return_dict:
            output = (logits, position_scores)
            return ((loss,) + output) if loss is not None else output
        
        return CausalLMOutputWithPast(
            loss=loss,
            logits=logits,
            past_key_values=None,  # Not implemented for simplicity
            hidden_states=hidden_states,
            attentions=None,
        )
    
    def generate(
        self,
        input_ids: torch.LongTensor,
        max_parallel_tokens: Optional[int] = None,
        shuffle_strategy: str = "rotary",
        temperature: float = 1.0,
        do_sample: bool = True,
        top_p: float = 0.9,
        **kwargs
    ) -> torch.LongTensor:
        """
        Generate tokens using parallel generation and shuffling.
        
        Args:
            input_ids: Input token IDs [batch_size, seq_len]
            max_parallel_tokens: Maximum tokens to generate in parallel
            shuffle_strategy: How to determine sequence length ('rotary', 'fixed')
            temperature: Sampling temperature
            do_sample: Whether to use sampling
            top_p: Top-p (nucleus) sampling parameter
            
        Returns:
            Generated token IDs [batch_size, new_seq_len]
        """
        if max_parallel_tokens is None:
            max_parallel_tokens = self.config.max_parallel_tokens
        
        batch_size, input_len = input_ids.shape
        device = input_ids.device
        
        # Extend input to maximum generation length
        extended_ids = torch.cat([
            input_ids,
            torch.zeros(batch_size, max_parallel_tokens, dtype=torch.long, device=device)
        ], dim=1)
        
        # Generate for the extended sequence
        with torch.no_grad():
            outputs = self.forward(extended_ids)
            logits = outputs.logits
            
            # Get logits only for the new tokens
            new_logits = logits[:, input_len:input_len + max_parallel_tokens, :]
            
            # Sample tokens
            if do_sample:
                # Apply temperature
                new_logits = new_logits / temperature
                
                # Top-p sampling
                if top_p < 1.0:
                    sorted_logits, sorted_indices = torch.sort(new_logits, descending=True)
                    cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)
                    
                    # Remove tokens with cumulative probability above the threshold
                    sorted_logits_to_remove = cumulative_probs > top_p
                    sorted_logits_to_remove[..., 1:] = sorted_logits_to_remove[..., :-1].clone()
                    sorted_logits_to_remove[..., 0] = 0
                    
                    # Set logits to -inf for tokens to remove
                    sorted_logits[sorted_logits_to_remove] = float('-inf')
                    new_logits = torch.gather(sorted_logits, -1, sorted_indices.argsort(-1))
                
                # Sample from the distribution
                probs = F.softmax(new_logits, dim=-1)
                new_tokens = torch.multinomial(probs.view(-1, probs.size(-1)), 1)
                new_tokens = new_tokens.view(batch_size, max_parallel_tokens)
            else:
                # Greedy sampling
                new_tokens = torch.argmax(new_logits, dim=-1)
            
            # Determine actual sequence length using rotary regression
            if shuffle_strategy == "rotary":
                # Get rotary component for the new tokens
                mixer_output = self.mixer(self.ln_f(self.layers[-1](
                    self.token_embedding(extended_ids) + 
                    self.position_embedding(torch.arange(extended_ids.size(1), device=device))
                )))
                rotary_component = mixer_output[:, input_len:input_len + max_parallel_tokens, -1:]
                position_ids = torch.arange(max_parallel_tokens, device=device).unsqueeze(0)
                position_scores = self.rotary_regression(rotary_component, position_ids)
                
                # Find termination points (where position score exceeds threshold)
                termination_threshold = 0.5  # This could be learned
                termination_mask = position_scores.squeeze(-1) > termination_threshold
                
                # Find first termination point for each batch
                actual_lengths = []
                for i in range(batch_size):
                    termination_positions = torch.where(termination_mask[i])[0]
                    if len(termination_positions) > 0:
                        actual_length = min(termination_positions[0].item() + 1, max_parallel_tokens)
                    else:
                        actual_length = max_parallel_tokens
                    actual_lengths.append(actual_length)
                
                # Truncate generated tokens based on determined lengths
                result_tokens = []
                for i, length in enumerate(actual_lengths):
                    result_tokens.append(torch.cat([
                        input_ids[i],
                        new_tokens[i, :length]
                    ]))
                
                # Pad to same length for batching
                max_result_len = max(len(tokens) for tokens in result_tokens)
                result = torch.zeros(batch_size, max_result_len, dtype=torch.long, device=device)
                for i, tokens in enumerate(result_tokens):
                    result[i, :len(tokens)] = tokens
                
                return result
            else:
                # Fixed length generation
                return torch.cat([input_ids, new_tokens], dim=1)
    
    def shuffle_and_filter(
        self,
        tokens: torch.LongTensor,
        position_scores: torch.FloatTensor,
        shuffle_strategy: str = "rotary"
    ) -> torch.LongTensor:
        """
        Shuffle and filter tokens based on position scores.
        
        This method implements the core "shuffling" logic that reorders tokens
        and removes those deemed unnecessary by the position analysis.
        """
        batch_size, seq_len = tokens.shape
        
        if shuffle_strategy == "rotary":
            # Use position scores to determine token importance
            importance_scores = torch.sigmoid(position_scores.squeeze(-1))
            
            # Sort tokens by importance (descending)
            sorted_indices = torch.argsort(importance_scores, dim=-1, descending=True)
            
            # Reorder tokens
            shuffled_tokens = torch.gather(tokens, 1, sorted_indices)
            shuffled_scores = torch.gather(importance_scores, 1, sorted_indices)
            
            # Filter out tokens below threshold
            threshold = 0.3  # This could be configurable
            keep_mask = shuffled_scores > threshold
            
            # Apply filtering
            filtered_tokens = []
            for i in range(batch_size):
                kept_tokens = shuffled_tokens[i][keep_mask[i]]
                filtered_tokens.append(kept_tokens)
            
            return filtered_tokens
        
        return tokens
