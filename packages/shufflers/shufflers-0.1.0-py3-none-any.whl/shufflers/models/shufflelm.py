"""
Base ShuffleLM implementation with transformers-compatible configuration.
"""

from typing import Optional, Tuple, Union
import torch
import torch.nn as nn
from transformers import PretrainedConfig, PreTrainedModel


class ShuffleConfig(PretrainedConfig):
    """
    Configuration class for ShuffleLM models, compatible with transformers library.
    
    This class inherits from PretrainedConfig to ensure full compatibility with
    transformers ecosystem including model saving/loading, hub integration, etc.
    """
    
    model_type = "shufflelm"
    
    def __init__(
        self,
        vocab_size: int = 50257,
        hidden_size: int = 768,
        num_layers: int = 12,
        num_heads: int = 12,
        intermediate_size: int = 3072,
        max_position_embeddings: int = 1024,
        # Shuffle-specific parameters
        max_parallel_tokens: int = 30,
        rotary_dim: int = 64,
        shuffle_temperature: float = 1.0,
        mixer_layers: int = 2,
        mixer_expansion_factor: int = 4,
        # Training parameters
        layer_norm_eps: float = 1e-5,
        dropout: float = 0.1,
        attention_dropout: float = 0.1,
        use_cache: bool = True,
        # Rotary regression parameters
        rotary_base: float = 10000.0,
        position_threshold: float = 0.5,
        termination_sensitivity: float = 1.0,
        # Token IDs
        pad_token_id: int = 50256,
        bos_token_id: int = 50256,
        eos_token_id: int = 50256,
        **kwargs
    ):
        super().__init__(
            pad_token_id=pad_token_id,
            bos_token_id=bos_token_id,
            eos_token_id=eos_token_id,
            **kwargs
        )
        
        # Model architecture
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.num_heads = num_heads
        self.intermediate_size = intermediate_size
        self.max_position_embeddings = max_position_embeddings
        
        # Shuffle-specific parameters
        self.max_parallel_tokens = max_parallel_tokens
        self.rotary_dim = rotary_dim
        self.shuffle_temperature = shuffle_temperature
        self.mixer_layers = mixer_layers
        self.mixer_expansion_factor = mixer_expansion_factor
        
        # Training parameters
        self.layer_norm_eps = layer_norm_eps
        self.dropout = dropout
        self.attention_dropout = attention_dropout
        self.use_cache = use_cache
        
        # Rotary regression parameters
        self.rotary_base = rotary_base
        self.position_threshold = position_threshold
        self.termination_sensitivity = termination_sensitivity


class ShuffleLM(PreTrainedModel):
    """
    Base ShuffleLM model implementing parallel token generation with intelligent reordering.
    
    This model serves as the foundation for more specific implementations like FasterDecodeMixer.
    It inherits from PreTrainedModel to ensure full transformers compatibility.
    """
    
    config_class = ShuffleConfig
    base_model_prefix = "shufflelm"
    supports_gradient_checkpointing = True
    _no_split_modules = ["TransformerBlock"]
    
    def __init__(self, config: ShuffleConfig):
        super().__init__(config)
        self.config = config
        
        # Token embeddings
        self.token_embedding = nn.Embedding(config.vocab_size, config.hidden_size)
        self.position_embedding = nn.Embedding(
            config.max_position_embeddings, config.hidden_size
        )
        
        # Transformer layers (to be implemented by subclasses)
        self.layers = nn.ModuleList([
            self._create_layer() for _ in range(config.num_layers)
        ])
        
        # Layer normalization
        self.ln_f = nn.LayerNorm(config.hidden_size, eps=config.layer_norm_eps)
        
        # Dropout
        self.dropout = nn.Dropout(config.dropout)
        
        # Initialize weights
        self.post_init()
    
    def _create_layer(self) -> nn.Module:
        """Create a single transformer layer. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement _create_layer")
    
    def forward(
        self,
        input_ids: Optional[torch.LongTensor] = None,
        attention_mask: Optional[torch.FloatTensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        labels: Optional[torch.LongTensor] = None,
        use_cache: Optional[bool] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
        **kwargs
    ):
        """Forward pass of the model."""
        raise NotImplementedError("Subclasses must implement forward")
    
    def generate(
        self,
        input_ids: torch.LongTensor,
        max_parallel_tokens: Optional[int] = None,
        shuffle_strategy: str = "rotary",
        temperature: float = 1.0,
        **kwargs
    ) -> torch.LongTensor:
        """
        Generate tokens using the shuffle strategy.
        
        Args:
            input_ids: Input token IDs
            max_parallel_tokens: Maximum number of tokens to generate in parallel
            shuffle_strategy: Strategy for token reordering ('rotary', 'learned')
            temperature: Sampling temperature
            
        Returns:
            Generated token IDs
        """
        if max_parallel_tokens is None:
            max_parallel_tokens = self.config.max_parallel_tokens
            
        # Implementation placeholder
        batch_size, seq_len = input_ids.shape
        
        # For now, return a simple extension (to be properly implemented)
        return input_ids
    
    def get_input_embeddings(self) -> nn.Module:
        """Get input embeddings layer."""
        return self.token_embedding
    
    def set_input_embeddings(self, new_embeddings: nn.Module) -> None:
        """Set input embeddings layer."""
        self.token_embedding = new_embeddings
    
    def resize_token_embeddings(self, new_num_tokens: int) -> nn.Embedding:
        """Resize token embeddings."""
        old_embeddings = self.get_input_embeddings()
        new_embeddings = self._get_resized_embeddings(old_embeddings, new_num_tokens)
        self.set_input_embeddings(new_embeddings)
        
        # Update config
        self.config.vocab_size = new_num_tokens
        
        return self.get_input_embeddings()
    
    def _init_weights(self, module: nn.Module) -> None:
        """Initialize model weights."""
        if isinstance(module, nn.Linear):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.padding_idx is not None:
                module.weight.data[module.padding_idx].zero_()
        elif isinstance(module, nn.LayerNorm):
            torch.nn.init.zeros_(module.bias)
            torch.nn.init.ones_(module.weight)
    
    def prepare_inputs_for_generation(
        self, 
        input_ids: torch.LongTensor, 
        past_key_values=None, 
        attention_mask=None, 
        **kwargs
    ):
        """Prepare inputs for generation."""
        # This method is called by the generate() method from transformers
        model_inputs = {"input_ids": input_ids}
        
        if attention_mask is not None:
            model_inputs["attention_mask"] = attention_mask
            
        return model_inputs
    
    @classmethod
    def from_pretrained(cls, pretrained_model_name_or_path, *args, **kwargs):
        """Load a pretrained model."""
        # This ensures compatibility with transformers hub
        return super().from_pretrained(pretrained_model_name_or_path, *args, **kwargs)
    
    def save_pretrained(self, save_directory, **kwargs):
        """Save the model."""
        # This ensures compatibility with transformers hub
        return super().save_pretrained(save_directory, **kwargs)
