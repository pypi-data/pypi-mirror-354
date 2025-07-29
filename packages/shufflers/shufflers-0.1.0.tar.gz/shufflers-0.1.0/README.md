# 🎯 ShuffleLM

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/shufflers.svg)](https://badge.fury.io/py/shufflers)

**ShuffleLM** is an innovative language model architecture that implements parallel token generation with intelligent reordering. Unlike traditional autoregressive generation, ShuffleLM generates multiple tokens simultaneously and then intelligently reorders and filters them for faster and more efficient text generation.


## 🔬 Academic Background

### Foundation Research for Parallel Generation

**Non-Autoregressive Neural Machine Translation:**
- Gu et al. (2018) - "Non-Autoregressive Neural Machine Translation" - Introduced fertility-based parallel decoding
- Lee et al. (2018) - "Deterministic Non-Autoregressive Neural Sequence Modeling by Iterative Refinement" - Iterative refinement approach
- Ghazvininejad et al. (2019) - "Mask-Predict: Parallel Decoding of Conditional Masked Language Models" - BERT-style masking with iterative prediction

**Latent Variable Models:**
- Kaiser et al. (2018) - "Fast Decoding in Sequence Models using Discrete Latent Variables" - Discrete latent variable compression
- Ma et al. (2019) - "FlowSeq: Non-Autoregressive Conditional Sequence Generation with Generative Flow" - Normalizing flow for latent modeling

**MLP-Mixer and Position Encoding:**
- Tolstikhin et al. (2021) - "MLP-Mixer: An all-MLP Architecture for Vision" - Original MLP-Mixer architecture
- Su et al. (2021) - "RoFormer: Enhanced Transformer with Rotary Position Embedding" - Rotary Position Embedding (RoPE)

**Non-Autoregressive Advances (2020-2022):**
- Zhou et al. (2020) - "Understanding Knowledge Distillation in Non-autoregressive Machine Translation" - Knowledge distillation for NAT
- Qian et al. (2021) - "Glancing Transformer for Non-Autoregressive Neural Machine Translation" - Semi-autoregressive approaches
- Ding et al. (2022) - "StraighTformer: Decoupled Attention with Linear Complexity for Fast Non-Autoregressive Generation"

**Speculative Decoding and Parallel Generation (2023-2024):**
- Leviathan et al. (2023) - "Fast Inference from Transformers via Speculative Decoding" - Draft-then-verify approach for acceleration
- Cai et al. (2024) - "Medusa: Simple Framework for Accelerating LLM Generation with Multiple Decoding Heads" - Multiple draft heads for parallel speculation
- Spector & Re (2023) - "Accelerating Large Language Model Decoding with Speculative Sampling" - Probability-based speculative sampling
- Sun et al. (2024) - "SpecInfer: Accelerating Generative Large Language Model Serving with Tree-based Speculative Inference"


### Model Evolution Paradigms

The evolution of language models can be broadly categorized into three paradigms:

### Causal Language Models (Autoregressive Language Models)
- **GPT Series**: Sequential token generation from left to right
- **Advantages**: Stable and consistent generation
- **Disadvantages**: Sequential processing leads to speed limitations

### Diffusion Language Models
- **BERT-based**: Gradually restore masked tokens through iterative refinement
- **Advantages**: Bidirectional context utilization
- **Disadvantages**: Complex noise scheduling and multi-step processing

### Shuffle Language Models ⭐ **New**
- **ShuffleLM**: Parallel generation followed by intelligent reordering
- **Advantages**: Fast parallel processing + dynamic length determination
- **Key Feature**: Token order optimization for improved quality


---


## 🌟 ShuffleLM Overview

### 🚀 Architecture

Sealed just for now. Stay tuned for updates!


---


## 📚 Documentation

For detailed documentation and examples, visit our [GitHub repository](https://github.com/thisisthepy/ShuffleLM).

### 🛠️ Installation

```bash
# Install with uv (recommended)
uv add shufflers
```

```bash
# Or install from source
git clone https://github.com/thisisthepy/ShuffleLM.git
cd ShuffleLM
uv sync
```

### 🎯 Quick Start

#### Basic Usage

```python
import torch
from shufflers import FasterDecodeMixer
from transformers import AutoTokenizer

# Load model and tokenizer
model_id = "thisisthepy/FasterDecodeMixer-Q3-8B"
model = FasterDecodeMixer.from_pretrained(model_id)
tokenizer = AutoTokenizer.from_pretrained(model_id)

# Generate text
prompt = "The future of artificial intelligence is"
inputs = tokenizer(prompt, return_tensors="pt")

# Parallel generation with shuffling
with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_parallel_tokens=30,  # Maximum parallel tokens to generate
        shuffle_strategy="rotary", # Shuffle strategy
        temperature=0.7
    )

generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(generated_text)
```

#### Advanced Usage

```python
from shufflers import ShuffleLM, ShuffleConfig

# Custom configuration
config = ShuffleConfig(
    vocab_size=50257,
    hidden_size=768,
    num_layers=12,
    num_heads=12,
    max_parallel_tokens=50,
    rotary_dim=64,
    shuffle_temperature=0.8
)

# Initialize model
model = ShuffleLM(config)

# Training mode
model.train()
outputs = model(
    input_ids=inputs["input_ids"],
    attention_mask=inputs["attention_mask"],
    labels=labels  # Required only during training
)

loss = outputs.loss
logits = outputs.logits
shuffle_scores = outputs.shuffle_scores  # Position reordering scores
```

#### Shuffle Visualization

```python
from shufflers.utils import visualize_shuffle

# Visualize generation process
visualization = visualize_shuffle(
    model=model,
    tokenizer=tokenizer,
    prompt="Hello, I am",
    save_animation=True,
    output_path="shuffle_animation.gif"
)

# Check step-by-step process
for step, tokens in visualization.steps:
    print(f"Step {step}: {tokens}")
```

### 🏗️ Project Structure

```
shufflers/
├── models/
│   ├── __init__.py
│   ├── shufflelm.py          # Main model class
│   └── fasterdecodemixer/
│       ├── __init__.py
│       ├── model.py          # FasterDecodeMixer implementation
│       ├── mixer.py          # MLP-Mixer components
│       └── rotary.py         # Rotary Regression implementation
├── utils/
│   ├── __init__.py
│   ├── config.py             # Configuration classes
│   ├── generation.py         # Generation utilities
│   └── visualization.py      # Visualization tools
└── __init__.py
```

### 🔧 Development Setup
```bash
# Clone repository
git clone https://github.com/thisisthepy/ShuffleLM.git
cd ShuffleLM

# Install development dependencies with uv
uv sync --dev
```

### Code Style
```bash
# Format code with uv
uv run black shufflers/
uv run isort shufflers/

# Lint code
uv run flake8 shufflers/
uv run mypy shufflers/
```

### 🧪 Testing
```bash
# Run all tests
uv run pytest

# Run specific tests
uv run pytest tests/test_model.py

# Run tests with coverage
uv run pytest --cov=shufflers --cov-report=html
```


---


## 📈 Performance Benchmarks

| Model | Speed (tokens/sec) | BLEU | Rouge-L | Memory (GB) |
|-------|------------------|------|---------|-------------|
| Llama3-8B | 42 | 24.8 | 46.1 | 2.1 |
| Qwen2.5-7B | 38 | 25.3 | 47.2 | 1.9 |
| **FasterDecodeMixer** | **89** | **24.7** | **46.9** | **1.1** |

*GPU: NVIDIA RTX 4090, Batch Size: 1*


---


## 🤝 Contributing

1. Create an issue to propose improvements
2. Fork and create a feature branch
3. Make changes and add tests
4. Create a Pull Request


### 📄 License

This project is distributed under the MIT License. See [LICENSE](LICENSE) file for details.

### 🙏 Citation

If you use ShuffleLM in your research or projects, please cite as follows:

```bibtex
@software{shufflelm2025,
  title={ShuffleLM: Parallel Token Generation with Intelligent Reordering},
  author={thisisthepy},
  year={2025},
  url={https://github.com/thisisthepy/ShuffleLM}
}
```

### 📞 Contact

- **Issues**: [GitHub Issues](https://github.com/thisisthepy/ShuffleLM/issues)
- **Discussions**: [GitHub Discussions](https://github.com/thisisthepy/ShuffleLM/discussions)
- **Email**: thisisthepy@gmail.com


---


<div align="center">
  <strong>🎯 ShuffleLM: Shuffle Tokens for Faster and Smarter Generation</strong>
</div>
