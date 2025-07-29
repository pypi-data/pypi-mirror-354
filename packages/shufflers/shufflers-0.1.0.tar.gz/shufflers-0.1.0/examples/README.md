# ShuffleLM Examples

This directory contains various examples demonstrating how to use ShuffleLM.

## 📋 Example List

### 1. `basic_usage.py`
An example showing basic usage of ShuffleLM.

- Model configuration and initialization
- Basic text generation
- Shuffle mechanism demonstration
- Visualization demo
- Performance comparison

**How to run:**
```bash
cd examples
python basic_usage.py
```

## 🚀 Quick Start

### Basic Generation Example
```python
from shufflers import FasterDecodeMixer, ShuffleConfig, ShuffleTokenizer

# Model configuration
config = ShuffleConfig(max_parallel_tokens=20)
model = FasterDecodeMixer(config)
tokenizer = ShuffleTokenizer("gpt2")

# Text generation
prompt = "The future of AI is"
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_parallel_tokens=20)
result = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(result)
```

### Visualization Example
```python
from shufflers.utils import visualize_shuffle

# Visualize shuffle process
viz = visualize_shuffle(
    model=model,
    tokenizer=tokenizer,
    prompt="Hello world",
    save_animation=True,
    output_path="shuffle_demo.gif"
)

# Print step-by-step process
viz.print_steps()
```

## 🎯 Key Feature Demonstrations

### 1. Parallel Token Generation
ShuffleLM generates multiple tokens simultaneously:

```python
# Generate up to 30 tokens in parallel
outputs = model.generate(
    **inputs,
    max_parallel_tokens=30,
    shuffle_strategy="rotary"
)
```

### 2. Dynamic Length Determination
The model automatically determines appropriate length:

```python
# Dynamic length determination using Rotary Regression
outputs = model.generate(
    **inputs,
    shuffle_strategy="rotary",  # Position-based termination decision
    temperature=0.8
)
```

### 3. Various Shuffle Strategies
```python
# Fixed length generation
fixed_output = model.generate(**inputs, shuffle_strategy="fixed")

# Position-based shuffling
rotary_output = model.generate(**inputs, shuffle_strategy="rotary")
```

## 📊 Performance Comparison

Examples include performance comparisons such as:

- **Generation Speed**: Parallel generation vs sequential generation
- **Memory Usage**: Batch processing efficiency
- **Quality Evaluation**: Results comparison across different strategies

## 🔧 Configuration Examples

### Small Model (for quick testing)
```python
small_config = ShuffleConfig(
    hidden_size=256,
    num_layers=4,
    max_parallel_tokens=15,
    rotary_dim=16
)
```

### Large Model (for high-quality generation)
```python
large_config = ShuffleConfig(
    hidden_size=1024,
    num_layers=24,
    max_parallel_tokens=50,
    rotary_dim=128
)
```

## 🎨 Visualization Options

### Text-based Visualization
```python
viz.print_steps()  # Step-by-step output to console
```

### Animation Saving
```python
viz = visualize_shuffle(
    model, tokenizer, prompt,
    save_animation=True,
    output_path="generation_process.gif"
)
```

### Statistical Analysis
```python
stats = viz.get_statistics()
print(f"Generated tokens: {stats['generate']['token_count']}")
print(f"Tokens after filtering: {stats['filter']['token_count']}")
```

## 🚀 Next Steps

1. Run `basic_usage.py` to check basic functionality
2. Experiment with various prompts
3. Adjust configurations to optimize performance
4. Understand the shuffle process through visualization
5. Integrate into your actual projects

## 💡 Tips

- Start with short prompts and gradually increase complexity
- Adjust `max_parallel_tokens` value to find the right balance between speed and quality
- Control creativity with `temperature` values (0.1-2.0 range)
- Use visualization to understand how the model works
