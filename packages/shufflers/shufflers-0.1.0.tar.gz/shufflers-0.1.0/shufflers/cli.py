"""
Command line interface for ShuffleLM.
"""

import argparse
import sys
import torch

from .models import FasterDecodeMixer, ShuffleConfig
from .utils import ShuffleTokenizer, visualize_shuffle


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="ShuffleLM CLI")
    subparsers = parser.add_subparsers(dest="command")
    
    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate text using ShuffleLM")
    gen_parser.add_argument("prompt", type=str, help="Input prompt")
    gen_parser.add_argument("--model", default="shuffle-base", help="Model size or path")
    gen_parser.add_argument("--max-tokens", type=int, default=30, help="Maximum parallel tokens")
    
    # Demo command
    demo_parser = subparsers.add_parser("demo", help="Run interactive demo")
    demo_parser.add_argument("--model", default="shuffle-base", help="Model size or path")
    
    args = parser.parse_args()
    
    if args.command == "generate":
        run_generate(args)
    elif args.command == "demo":
        run_demo(args)
    else:
        parser.print_help()


def run_generate(args):
    """Run text generation."""
    config = ShuffleConfig()
    model = FasterDecodeMixer(config)
    tokenizer = ShuffleTokenizer("gpt2")
    
    inputs = tokenizer(args.prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_parallel_tokens=args.max_tokens)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    print(result)


def run_demo(args):
    """Run interactive demo."""
    print("ShuffleLM Demo - Type 'quit' to exit")
    
    config = ShuffleConfig()
    model = FasterDecodeMixer(config)
    tokenizer = ShuffleTokenizer("gpt2")
    
    while True:
        prompt = input("Prompt> ").strip()
        if prompt.lower() == 'quit':
            break
        
        try:
            inputs = tokenizer(prompt, return_tensors="pt")
            outputs = model.generate(**inputs, max_parallel_tokens=20)
            result = tokenizer.decode(outputs[0], skip_special_tokens=True)
            print(f"Generated: {result}\n")
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
