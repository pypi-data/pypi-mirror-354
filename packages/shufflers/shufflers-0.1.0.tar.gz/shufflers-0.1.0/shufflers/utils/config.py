"""
Configuration utilities for ShuffleLM models.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
import json


@dataclass
class ShuffleGenerationConfig:
    """Configuration for generation with shuffling."""
    
    # Generation parameters
    max_parallel_tokens: Optional[int] = None
    temperature: float = 1.0
    top_p: float = 0.9
    top_k: Optional[int] = None
    do_sample: bool = True
    
    # Shuffle-specific parameters
    shuffle_strategy: str = "rotary"  # 'rotary', 'learned', 'fixed'
    termination_threshold: Optional[float] = None
    min_generation_length: int = 1
    max_generation_length: Optional[int] = None
    
    # Advanced parameters
    repetition_penalty: float = 1.0
    length_penalty: float = 1.0
    early_stopping: bool = False
    
    # Debugging
    return_shuffle_info: bool = False
    return_attention_weights: bool = False
    
    def validate(self) -> None:
        """Validate configuration parameters."""
        if self.temperature <= 0:
            raise ValueError("Temperature must be positive")
        
        if not 0 <= self.top_p <= 1:
            raise ValueError("top_p must be between 0 and 1")
        
        if self.top_k is not None and self.top_k <= 0:
            raise ValueError("top_k must be positive")
        
        if self.shuffle_strategy not in ["rotary", "learned", "fixed"]:
            raise ValueError(f"Unknown shuffle strategy: {self.shuffle_strategy}")


@dataclass
class ShuffleTrainingConfig:
    """Configuration for training ShuffleLM models."""
    
    # Basic training parameters
    learning_rate: float = 5e-5
    batch_size: int = 8
    gradient_accumulation_steps: int = 1
    num_train_epochs: int = 3
    max_steps: Optional[int] = None
    
    # Optimizer parameters
    optimizer: str = "adamw"
    weight_decay: float = 0.01
    adam_beta1: float = 0.9
    adam_beta2: float = 0.999
    adam_epsilon: float = 1e-8
    
    # Learning rate schedule
    lr_scheduler_type: str = "linear"
    warmup_steps: int = 0
    warmup_ratio: float = 0.0
    
    # Shuffle-specific training
    shuffle_loss_weight: float = 0.1
    position_loss_weight: float = 0.05
    termination_loss_weight: float = 0.1
    
    # Regularization
    dropout: float = 0.1
    label_smoothing: float = 0.0
    gradient_clipping: float = 1.0
    
    # Logging and saving
    logging_steps: int = 10
    save_steps: int = 500
    eval_steps: int = 500
    save_total_limit: int = 3
    
    # Hardware optimization
    fp16: bool = False
    bf16: bool = False
    dataloader_num_workers: int = 0
    
    def get_optimizer_params(self) -> Dict[str, Any]:
        """Get optimizer parameters."""
        return {
            "lr": self.learning_rate,
            "betas": (self.adam_beta1, self.adam_beta2),
            "eps": self.adam_epsilon,
            "weight_decay": self.weight_decay,
        }
