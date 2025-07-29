"""
Custom tokenizer utilities for ShuffleLM.
"""

from typing import Optional, List, Dict, Any, Union
import torch
from transformers import AutoTokenizer, PreTrainedTokenizer


class ShuffleTokenizer:
    """Wrapper around standard tokenizers with shuffle-specific functionality."""
    
    def __init__(self, tokenizer: Union[str, PreTrainedTokenizer], add_shuffle_tokens: bool = True):
        if isinstance(tokenizer, str):
            self.tokenizer = AutoTokenizer.from_pretrained(tokenizer)
        else:
            self.tokenizer = tokenizer
            
        self.shuffle_tokens = {}
        
        if add_shuffle_tokens:
            self._add_shuffle_special_tokens()
    
    def _add_shuffle_special_tokens(self) -> None:
        """Add shuffle-specific special tokens."""
        special_tokens = {
            "shuffle_start": "<|shuffle_start|>",
            "shuffle_end": "<|shuffle_end|>", 
            "position_marker": "<|pos|>",
            "termination_signal": "<|term|>",
        }
        
        new_tokens = []
        for token_name, token_str in special_tokens.items():
            if token_str not in self.tokenizer.get_vocab():
                new_tokens.append(token_str)
                self.shuffle_tokens[token_name] = token_str
        
        if new_tokens:
            self.tokenizer.add_tokens(new_tokens)
    
    def tokenize_for_shuffle(self, text: str, max_length: Optional[int] = None) -> Dict[str, torch.Tensor]:
        """Tokenize text optimized for shuffle generation."""
        encoding = self.tokenizer(text, max_length=max_length, padding=True, truncation=True, return_tensors="pt")
        
        seq_len = encoding["input_ids"].size(1)
        batch_size = encoding["input_ids"].size(0)
        
        encoding["position_ids"] = torch.arange(seq_len).unsqueeze(0).repeat(batch_size, 1)
        encoding["shuffle_mask"] = torch.ones(batch_size, seq_len, dtype=torch.bool)
        
        return encoding
    
    def __getattr__(self, name):
        """Delegate unknown attributes to the underlying tokenizer."""
        return getattr(self.tokenizer, name)
    
    def __call__(self, *args, **kwargs):
        """Make the class callable like the underlying tokenizer."""
        return self.tokenizer(*args, **kwargs)
