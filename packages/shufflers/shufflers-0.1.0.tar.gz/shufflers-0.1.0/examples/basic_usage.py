"""
Basic usage example for ShuffleLM.

This script demonstrates how to use ShuffleLM for text generation
with the shuffle mechanism.
"""

import torch
from shufflers import FasterDecodeMixer, ShuffleConfig, ShuffleTokenizer


def main():
    """Run basic ShuffleLM example."""
    print("🎯 ShuffleLM Basic Usage Example")
    print("=" * 40)
    
    # 1. Create model configuration
    print("1. Creating model configuration...")
    config = ShuffleConfig(
        vocab_size=50257,
        hidden_size=512,  # Smaller for demo
        num_layers=6,
        num_heads=8,
        max_parallel_tokens=20,
        rotary_dim=32
    )
    print(f"   ✓ Config created: {config.num_layers} layers, {config.hidden_size} hidden size")
    
    # 2. Initialize model
    print("\n2. Initializing FasterDecodeMixer model...")
    model = FasterDecodeMixer(config)
    model.eval()  # Set to evaluation mode
    print("   ✓ Model initialized successfully")
    
    # 3. Create tokenizer
    print("\n3. Setting up ShuffleTokenizer...")
    tokenizer = ShuffleTokenizer("gpt2", add_shuffle_tokens=True)
    print("   ✓ Tokenizer ready with shuffle-specific tokens")
    
    # 4. Generate text examples
    prompts = [
        "The future of artificial intelligence is",
        "Once upon a time in a distant galaxy",
        "Scientists have recently discovered",
        "In the year 2050, technology will"
    ]
    
    print("\n4. Generating text with shuffle mechanism...")
    print("-" * 40)
    
    for i, prompt in enumerate(prompts, 1):
        print(f"\nExample {i}: '{prompt}'")
        
        # Tokenize input
        inputs = tokenizer(prompt, return_tensors="pt")
        
        # Generate with shuffle
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_parallel_tokens=config.max_parallel_tokens,
                shuffle_strategy="rotary",
                temperature=0.8,
                do_sample=True,
                top_p=0.9
            )
        
        # Decode result
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        print(f"Generated: {generated_text}")
        print(f"Length: {len(generated_text.split())} words")
    
    print("\n" + "=" * 40)
    print("✓ Basic usage example completed!")
    
    # 5. Show model statistics
    print("\n5. Model Statistics:")
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    
    print(f"   Total parameters: {total_params:,}")
    print(f"   Trainable parameters: {trainable_params:,}")
    print(f"   Model size: ~{total_params * 4 / 1024 / 1024:.1f} MB")


def demo_shuffle_visualization():
    """Demonstrate shuffle visualization."""
    print("\n" + "=" * 40)
    print("🎨 Shuffle Visualization Demo")
    print("=" * 40)
    
    try:
        from shufflers.utils import visualize_shuffle
        
        # Create small model for visualization
        config = ShuffleConfig(
            hidden_size=256,
            num_layers=4,
            max_parallel_tokens=15,
            rotary_dim=16
        )
        
        model = FasterDecodeMixer(config)
        tokenizer = ShuffleTokenizer("gpt2")
        
        prompt = "Hello world, this is a test"
        
        print(f"Visualizing generation for: '{prompt}'")
        
        # Create visualization
        viz = visualize_shuffle(
            model=model,
            tokenizer=tokenizer,
            prompt=prompt,
            max_parallel_tokens=15
        )
        
        # Print text-based visualization
        viz.print_steps()
        
        # Show statistics
        stats = viz.get_statistics()
        print("\nVisualization Statistics:")
        for step_type, step_stats in stats.items():
            print(f"  {step_type}: {step_stats}")
        
    except ImportError as e:
        print(f"Visualization requires additional dependencies: {e}")
    except Exception as e:
        print(f"Visualization error: {e}")


def compare_with_standard_generation():
    """Compare shuffle generation with standard autoregressive generation."""
    print("\n" + "=" * 40)
    print("📊 Comparison: Shuffle vs Standard Generation")
    print("=" * 40)
    
    config = ShuffleConfig(hidden_size=256, num_layers=4, max_parallel_tokens=10)
    model = FasterDecodeMixer(config)
    tokenizer = ShuffleTokenizer("gpt2")
    
    prompt = "The weather today is"
    inputs = tokenizer(prompt, return_tensors="pt")
    
    print(f"Prompt: '{prompt}'")
    print()
    
    # Shuffle generation
    print("🎯 Shuffle Generation:")
    with torch.no_grad():
        shuffle_outputs = model.generate(
            **inputs,
            max_parallel_tokens=10,
            shuffle_strategy="rotary",
            temperature=0.7
        )
    
    shuffle_text = tokenizer.decode(shuffle_outputs[0], skip_special_tokens=True)
    print(f"  Result: {shuffle_text}")
    print(f"  Tokens: {shuffle_outputs.shape[1]} total")
    
    # Standard generation (simulated)
    print("\n🔄 Standard Generation (simulated):")
    with torch.no_grad():
        standard_outputs = model.generate(
            **inputs,
            max_parallel_tokens=10,
            shuffle_strategy="fixed",  # No shuffling
            temperature=0.7
        )
    
    standard_text = tokenizer.decode(standard_outputs[0], skip_special_tokens=True)
    print(f"  Result: {standard_text}")
    print(f"  Tokens: {standard_outputs.shape[1]} total")
    
    print("\nNote: This is a simplified comparison. In practice, shuffle generation")
    print("offers benefits in parallel processing and dynamic length determination.")


if __name__ == "__main__":
    # Run basic example
    main()
    
    # Run visualization demo
    demo_shuffle_visualization()
    
    # Run comparison
    compare_with_standard_generation()
