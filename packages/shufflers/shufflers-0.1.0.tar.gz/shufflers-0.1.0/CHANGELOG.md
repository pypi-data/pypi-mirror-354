# Changelog

All notable changes to ShuffleLM will be documented in this file.

## [0.1.0] - 2025-06-10

### Added
- Initial implementation of ShuffleLM architecture
- FasterDecodeMixer model with MLP-Mixer and Rotary Regression
- Parallel token generation with intelligent reordering
- Dynamic sequence length determination
- ShuffleTokenizer with shuffle-specific token support
- Visualization utilities for generation process
- Command-line interface for text generation and demos
- Comprehensive test suite
- Documentation and examples

### Features
- **Parallel Generation**: Generate multiple tokens simultaneously
- **Intelligent Shuffling**: Reorder tokens based on position analysis
- **Dynamic Length**: Automatically determine optimal sequence length
- **Rotary Regression**: Novel position analysis technique
- **MLP-Mixer Integration**: Replace final linear layer with mixer architecture
- **Visualization**: Animated visualization of shuffle process
- **CLI Tools**: Easy-to-use command line interface

### Architecture Components
- `FasterDecodeMixer`: Main model class
- `MLPMixer`: Token and channel mixing layers
- `RotaryRegression`: Position analysis and termination detection
- `ShuffleTokenizer`: Enhanced tokenizer with shuffle support
- `ShuffleVisualization`: Generation process visualization
