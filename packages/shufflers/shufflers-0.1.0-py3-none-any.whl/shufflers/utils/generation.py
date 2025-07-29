"""
Generation utilities for ShuffleLM models.
"""

from typing import Optional, Dict, Any, List, Tuple
import torch
import torch.nn.functional as F
from .config import ShuffleGenerationConfig


def generate_with_shuffle(
    model,
    tokenizer,
    prompt: str,
    config: Optional[ShuffleGenerationConfig] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Generate text using ShuffleLM with configurable shuffle strategies.
    
    Args:
        model: ShuffleLM model instance
        tokenizer: Tokenizer for encoding/decoding
        prompt: Input text prompt
        config: Generation configuration
        **kwargs: Additional generation parameters
        
    Returns:
        Dictionary containing generated text and optional debug info
    """
    if config is None:
        config = ShuffleGenerationConfig()
    
    # Override config with kwargs
    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)
    
    config.validate()
    
    # Encode prompt
    inputs = tokenizer(prompt, return_tensors="pt")
    input_ids = inputs["input_ids"]
    
    # Generate with shuffle
    with torch.no_grad():
        outputs = model.generate(
            input_ids=input_ids,
            max_parallel_tokens=config.max_parallel_tokens,
            shuffle_strategy=config.shuffle_strategy,
            temperature=config.temperature,
            do_sample=config.do_sample,
            top_p=config.top_p,
        )
    
    # Decode results
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    result = {
        "generated_text": generated_text,
        "prompt": prompt,
        "config": config,
    }
    
    if config.return_shuffle_info:
        # Add shuffle-specific information
        result["shuffle_info"] = _extract_shuffle_info(model, input_ids, outputs)
    
    return result


def _extract_shuffle_info(model, input_ids: torch.Tensor, outputs: torch.Tensor) -> Dict[str, Any]:
    """Extract shuffle-specific information from generation process."""
    # This would be called during generation to collect shuffle statistics
    return {
        "original_length": input_ids.size(1),
        "generated_length": outputs.size(1) - input_ids.size(1),
        "shuffle_strategy": "rotary",  # This would come from the actual generation
        "termination_points": [],  # Positions where generation was terminated
    }


def apply_top_k_top_p_filtering(
    logits: torch.Tensor,
    top_k: int = 0,
    top_p: float = 1.0,
    filter_value: float = float("-inf"),
    min_tokens_to_keep: int = 1,
) -> torch.Tensor:
    """
    Filter a distribution of logits using top-k and/or nucleus (top-p) filtering.
    
    Args:
        logits: logits distribution shape (batch size, vocabulary size)
        top_k: keep only top k tokens with highest probability (top-k filtering)
        top_p: keep the top tokens with cumulative probability >= top_p (nucleus filtering)
        filter_value: value to replace filtered logits with
        min_tokens_to_keep: minimum number of tokens to keep per batch
        
    Returns:
        Filtered logits
    """
    if top_k > 0:
        top_k = min(max(top_k, min_tokens_to_keep), logits.size(-1))
        # Remove all tokens with a probability less than the last token of the top-k
        indices_to_remove = logits < torch.topk(logits, top_k)[0][..., -1, None]
        logits[indices_to_remove] = filter_value

    if top_p < 1.0:
        sorted_logits, sorted_indices = torch.sort(logits, descending=True)
        cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

        # Remove tokens with cumulative probability above the threshold (token with 0 are kept)
        sorted_indices_to_remove = cumulative_probs > top_p
        if min_tokens_to_keep > 1:
            # Keep at least min_tokens_to_keep
            sorted_indices_to_remove[..., :min_tokens_to_keep] = 0
        # Shift the indices to the right to keep also the first token above the threshold
        sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
        sorted_indices_to_remove[..., 0] = 0

        # scatter sorted tensors to original indexing
        indices_to_remove = sorted_indices_to_remove.scatter(1, sorted_indices, sorted_indices_to_remove)
        logits[indices_to_remove] = filter_value

    return logits


def sample_tokens(
    logits: torch.Tensor,
    temperature: float = 1.0,
    top_k: int = 0,
    top_p: float = 1.0,
    do_sample: bool = True,
) -> torch.Tensor:
    """
    Sample tokens from logits with temperature, top-k, and top-p filtering.
    
    Args:
        logits: Logits tensor [batch_size, seq_len, vocab_size]
        temperature: Sampling temperature
        top_k: Top-k filtering parameter
        top_p: Top-p (nucleus) filtering parameter
        do_sample: Whether to sample or use greedy decoding
        
    Returns:
        Sampled token IDs [batch_size, seq_len]
    """
    if not do_sample:
        # Greedy decoding
        return torch.argmax(logits, dim=-1)
    
    # Apply temperature
    if temperature != 1.0:
        logits = logits / temperature
    
    # Apply top-k and top-p filtering
    batch_size, seq_len, vocab_size = logits.shape
    logits_flat = logits.view(-1, vocab_size)
    
    filtered_logits = apply_top_k_top_p_filtering(
        logits_flat, top_k=top_k, top_p=top_p
    )
    
    # Sample from the filtered distribution
    probs = F.softmax(filtered_logits, dim=-1)
    sampled_flat = torch.multinomial(probs, 1).squeeze(-1)
    
    # Reshape back to original dimensions
    sampled = sampled_flat.view(batch_size, seq_len)
    
    return sampled


class ShuffleGenerator:
    """
    Advanced generator class for ShuffleLM with support for various shuffle strategies.
    """
    
    def __init__(self, model, tokenizer, config: Optional[ShuffleGenerationConfig] = None):
        self.model = model
        self.tokenizer = tokenizer
        self.config = config or ShuffleGenerationConfig()
        
    def generate(
        self,
        prompt: str,
        config: Optional[ShuffleGenerationConfig] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate text with the configured shuffle strategy."""
        generation_config = config or self.config
        
        # Override with kwargs
        for key, value in kwargs.items():
            if hasattr(generation_config, key):
                setattr(generation_config, key, value)
        
        return generate_with_shuffle(
            self.model, self.tokenizer, prompt, generation_config
        )
    
    def batch_generate(
        self,
        prompts: List[str],
        config: Optional[ShuffleGenerationConfig] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Generate text for multiple prompts."""
        results = []
        for prompt in prompts:
            result = self.generate(prompt, config, **kwargs)
            results.append(result)
        return results
    
    def interactive_generate(self, max_turns: int = 10):
        """Interactive generation loop."""
        print("ShuffleLM Interactive Generation")
        print("Type 'quit' to exit, 'config' to show current configuration")
        print("-" * 50)
        
        for turn in range(max_turns):
            try:
                prompt = input(f"Turn {turn + 1}> ")
                
                if prompt.lower() == 'quit':
                    break
                elif prompt.lower() == 'config':
                    print(f"Current config: {self.config}")
                    continue
                
                result = self.generate(prompt)
                print(f"Generated: {result['generated_text']}")
                print("-" * 50)
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def benchmark_generation(
        self,
        prompts: List[str],
        num_runs: int = 5
    ) -> Dict[str, Any]:
        """Benchmark generation speed and quality."""
        import time
        
        times = []
        results = []
        
        for run in range(num_runs):
            start_time = time.time()
            
            batch_results = self.batch_generate(prompts)
            
            end_time = time.time()
            times.append(end_time - start_time)
            results.extend(batch_results)
        
        avg_time = sum(times) / len(times)
        tokens_per_second = sum(
            len(self.tokenizer.encode(r['generated_text'])) 
            for r in results
        ) / sum(times)
        
        return {
            "average_time": avg_time,
            "tokens_per_second": tokens_per_second,
            "total_runs": num_runs,
            "total_prompts": len(prompts) * num_runs,
            "results": results[:len(prompts)]  # Return results from first run
        }
