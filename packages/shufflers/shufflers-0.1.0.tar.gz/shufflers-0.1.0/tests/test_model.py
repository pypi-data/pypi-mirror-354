"""
Test cases for ShuffleLM models.
"""

import pytest
import torch

from shufflers.models import FasterDecodeMixer, ShuffleConfig
from shufflers.utils import ShuffleTokenizer


class TestShuffleConfig:
    """Test ShuffleConfig functionality."""
    
    def test_default_config(self):
        """Test default configuration creation."""
        config = ShuffleConfig()
        assert config.vocab_size == 50257
        assert config.hidden_size == 768
        assert config.num_layers == 12
        assert config.max_parallel_tokens == 30
    
    def test_config_serialization(self):
        """Test config serialization to/from dict."""
        config = ShuffleConfig(hidden_size=512, num_layers=6)
        config_dict = config.to_dict()
        
        assert config_dict["hidden_size"] == 512
        assert config_dict["num_layers"] == 6
        
        # Test round-trip
        restored_config = ShuffleConfig.from_dict(config_dict)
        assert restored_config.hidden_size == 512
        assert restored_config.num_layers == 6


class TestFasterDecodeMixer:
    """Test FasterDecodeMixer model."""
    
    @pytest.fixture
    def small_config(self):
        """Create small config for testing."""
        return ShuffleConfig(
            vocab_size=1000,
            hidden_size=128,
            num_layers=2,
            num_heads=4,
            intermediate_size=256,
            max_parallel_tokens=10,
            rotary_dim=16
        )
    
    @pytest.fixture
    def model(self, small_config):
        """Create model for testing."""
        return FasterDecodeMixer(small_config)
    
    def test_model_creation(self, model, small_config):
        """Test model can be created with config."""
        assert model.config.vocab_size == 1000
        assert model.config.hidden_size == 128
        assert hasattr(model, 'mixer')
        assert hasattr(model, 'rotary_regression')
    
    def test_forward_pass(self, model):
        """Test forward pass works."""
        batch_size, seq_len = 2, 8
        input_ids = torch.randint(0, 1000, (batch_size, seq_len))
        
        outputs = model.forward(input_ids)
        
        assert hasattr(outputs, 'logits')
        assert outputs.logits.shape == (batch_size, seq_len, 1000)
    
    def test_generation(self, model):
        """Test generation method."""
        input_ids = torch.randint(0, 1000, (1, 5))
        
        with torch.no_grad():
            outputs = model.generate(
                input_ids=input_ids,
                max_parallel_tokens=5,
                do_sample=False  # Use greedy for deterministic testing
            )
        
        assert outputs.shape[0] == 1  # Batch dimension
        assert outputs.shape[1] >= input_ids.shape[1]  # At least input length


class TestShuffleTokenizer:
    """Test ShuffleTokenizer functionality."""
    
    @pytest.fixture
    def tokenizer(self):
        """Create tokenizer for testing."""
        return ShuffleTokenizer("gpt2", add_shuffle_tokens=True)
    
    def test_tokenizer_creation(self, tokenizer):
        """Test tokenizer can be created."""
        assert hasattr(tokenizer, 'tokenizer')
        assert hasattr(tokenizer, 'shuffle_tokens')
    
    def test_shuffle_tokenization(self, tokenizer):
        """Test shuffle-specific tokenization."""
        text = "Hello world"
        encoding = tokenizer.tokenize_for_shuffle(text)
        
        assert 'input_ids' in encoding
        assert 'attention_mask' in encoding
        assert 'position_ids' in encoding
        assert 'shuffle_mask' in encoding
    
    def test_special_tokens(self, tokenizer):
        """Test shuffle special tokens."""
        special_ids = tokenizer.get_special_token_ids()
        assert isinstance(special_ids, dict)


class TestIntegration:
    """Integration tests."""
    
    def test_end_to_end_generation(self):
        """Test complete generation pipeline."""
        # Create small model for fast testing
        config = ShuffleConfig(
            vocab_size=50257,  # Use full vocab for real tokenizer
            hidden_size=64,
            num_layers=1,
            num_heads=4,
            max_parallel_tokens=5,
            rotary_dim=8
        )
        
        model = FasterDecodeMixer(config)
        tokenizer = ShuffleTokenizer("gpt2")
        
        # Test generation
        prompt = "Hello"
        inputs = tokenizer(prompt, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_parallel_tokens=5,
                do_sample=False
            )
        
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        assert isinstance(generated_text, str)
        assert len(generated_text) >= len(prompt)


if __name__ == "__main__":
    pytest.main([__file__])
