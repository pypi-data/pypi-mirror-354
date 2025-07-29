#!/usr/bin/env python3
"""
Installation verification script for ShuffleLM.

This script checks if all components are properly installed and working.
"""

import sys
import importlib
import traceback


def check_import(module_name, component_name=None):
    """Check if a module/component can be imported."""
    try:
        if component_name:
            module = importlib.import_module(module_name)
            getattr(module, component_name)
            print(f"✓ {module_name}.{component_name}")
        else:
            importlib.import_module(module_name)
            print(f"✓ {module_name}")
        return True
    except ImportError as e:
        print(f"✗ {module_name}{f'.{component_name}' if component_name else ''}: {e}")
        return False
    except AttributeError as e:
        print(f"✗ {module_name}.{component_name}: {e}")
        return False


def check_basic_functionality():
    """Check basic ShuffleLM functionality."""
    print("\n📋 Checking Basic Functionality")
    print("-" * 40)
    
    try:
        from shufflers import FasterDecodeMixer, ShuffleConfig, ShuffleTokenizer
        
        # Test configuration
        config = ShuffleConfig(
            hidden_size=128,
            num_layers=2,
            max_parallel_tokens=5
        )
        print("✓ Configuration creation")
        
        # Test model creation
        model = FasterDecodeMixer(config)
        print("✓ Model initialization")
        
        # Test tokenizer
        tokenizer = ShuffleTokenizer("gpt2")
        print("✓ Tokenizer initialization")
        
        # Test basic forward pass
        import torch
        input_ids = torch.randint(0, 1000, (1, 3))
        
        with torch.no_grad():
            outputs = model.forward(input_ids)
        
        print("✓ Model forward pass")
        
        # Test generation
        with torch.no_grad():
            generated = model.generate(
                input_ids=input_ids,
                max_parallel_tokens=3,
                do_sample=False
            )
        
        print("✓ Text generation")
        
        return True
        
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        traceback.print_exc()
        return False


def check_dependencies():
    """Check required dependencies."""
    print("\n📦 Checking Dependencies")
    print("-" * 40)
    
    dependencies = [
        "torch",
        "transformers", 
        "numpy",
        "einops",
        "tqdm",
        "safetensors",
        "tokenizers",
        "huggingface_hub",
        "packaging"
    ]
    
    all_good = True
    for module, component in components:
        if not check_import(module, component):
            all_good = False
    
    return all_good


def check_optional_features():
    """Check optional features."""
    print("\n🎨 Checking Optional Features")
    print("-" * 40)
    
    optional_deps = [
        ("matplotlib", "For visualization"),
        ("seaborn", "For enhanced plots"),
        ("plotly", "For interactive plots"),
        ("pillow", "For image processing"),
        ("imageio", "For GIF creation")
    ]
    
    for dep, description in optional_deps:
        try:
            importlib.import_module(dep)
            print(f"✓ {dep} - {description}")
        except ImportError:
            print(f"○ {dep} - {description} (optional, not installed)")


def run_verification():
    """Run complete verification."""
    print("🔍 ShuffleLM Installation Verification")
    print("=" * 40)
    
    all_checks = []
    
    # Check dependencies
    all_checks.append(check_dependencies())
    
    # Check ShuffleLM components
    all_checks.append(check_shufflers_components())
    
    # Check basic functionality
    all_checks.append(check_basic_functionality())
    
    # Check optional features
    check_optional_features()
    
    # Summary
    print("\n📊 Verification Summary")
    print("-" * 40)
    
    if all(all_checks):
        print("✅ All core components are working correctly!")
        print("🎉 ShuffleLM is ready to use!")
        
        print("\n🚀 Next Steps:")
        print("1. Try the basic example: python examples/basic_usage.py")
        print("2. Run the CLI demo: python -m shufflers.cli demo")
        print("3. Read the documentation in README.md")
        
        return 0
    else:
        print("❌ Some components are not working properly.")
        print("🔧 Please check the installation and dependencies.")
        
        print("\n🛠️ Troubleshooting:")
        print("1. Ensure you have Python 3.9+")
        print("2. Install with: uv add shufflers")
        print("3. Check for dependency conflicts")
        print("4. Try reinstalling in a clean environment")
        
        return 1


def main():
    """Main verification function."""
    try:
        return run_verification()
    except KeyboardInterrupt:
        print("\n\n⏹️ Verification interrupted by user.")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error during verification: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
    for dep in dependencies:
        if not check_import(dep):
            all_good = False
    
    return all_good


def check_shufflers_components():
    """Check all ShuffleLM components."""
    print("\n🎯 Checking ShuffleLM Components")
    print("-" * 40)
    
    components = [
        ("shufflers", None),
        ("shufflers.models", None),
        ("shufflers.models", "FasterDecodeMixer"),
        ("shufflers.models", "ShuffleConfig"),
        ("shufflers.utils", None),
        ("shufflers.utils", "ShuffleTokenizer"),
        ("shufflers.utils", "visualize_shuffle"),
    ]
    
    all_good = True
    for module, component in components:
        if not check_import(module, component):
            all_good = False
    
    return all_good


def check_optional_features():
    """Check optional features."""
    print("\n🎨 Checking Optional Features")
    print("-" * 40)
    
    optional_deps = [
        ("matplotlib", "For visualization"),
        ("seaborn", "For enhanced plots"),
        ("plotly", "For interactive plots"),
        ("pillow", "For image processing"),
        ("imageio", "For GIF creation")
    ]
    
    for dep, description in optional_deps:
        try:
            importlib.import_module(dep)
            print(f"✓ {dep} - {description}")
        except ImportError:
            print(f"○ {dep} - {description} (optional, not installed)")


def run_verification():
    """Run complete verification."""
    print("🔍 ShuffleLM Installation Verification")
    print("=" * 40)
    
    all_checks = []
    
    # Check dependencies
    all_checks.append(check_dependencies())
    
    # Check ShuffleLM components
    all_checks.append(check_shufflers_components())
    
    # Check basic functionality
    all_checks.append(check_basic_functionality())
    
    # Check optional features
    check_optional_features()
    
    # Summary
    print("\n📊 Verification Summary")
    print("-" * 40)
    
    if all(all_checks):
        print("✅ All core components are working correctly!")
        print("🎉 ShuffleLM is ready to use!")
        
        print("\n🚀 Next Steps:")
        print("1. Try the basic example: python examples/basic_usage.py")
        print("2. Run the CLI demo: python -m shufflers.cli demo")
        print("3. Read the documentation in README.md")
        
        return 0
    else:
        print("❌ Some components are not working properly.")
        print("🔧 Please check the installation and dependencies.")
        
        print("\n🛠️ Troubleshooting:")
        print("1. Ensure you have Python 3.9+")
        print("2. Install with: uv add shufflers")
        print("3. Check for dependency conflicts")
        print("4. Try reinstalling in a clean environment")
        
        return 1


def main():
    """Main verification function."""
    try:
        return run_verification()
    except KeyboardInterrupt:
        print("\n\n⏹️ Verification interrupted by user.")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error during verification: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
    for module, component in components:
        if not check_import(module, component):
            all_good = False
    
    return all_good


def check_optional_features():
    """Check optional features."""
    print("\n🎨 Checking Optional Features")
    print("-" * 40)
    
    optional_deps = [
        ("matplotlib", "For visualization"),
        ("seaborn", "For enhanced plots"),
        ("plotly", "For interactive plots"),
        ("pillow", "For image processing"),
        ("imageio", "For GIF creation")
    ]
    
    for dep, description in optional_deps:
        try:
            importlib.import_module(dep)
            print(f"✓ {dep} - {description}")
        except ImportError:
            print(f"○ {dep} - {description} (optional, not installed)")


def run_verification():
    """Run complete verification."""
    print("🔍 ShuffleLM Installation Verification")
    print("=" * 40)
    
    all_checks = []
    
    # Check dependencies
    all_checks.append(check_dependencies())
    
    # Check ShuffleLM components
    all_checks.append(check_shufflers_components())
    
    # Check basic functionality
    all_checks.append(check_basic_functionality())
    
    # Check optional features
    check_optional_features()
    
    # Summary
    print("\n📊 Verification Summary")
    print("-" * 40)
    
    if all(all_checks):
        print("✅ All core components are working correctly!")
        print("🎉 ShuffleLM is ready to use!")
        
        print("\n🚀 Next Steps:")
        print("1. Try the basic example: python examples/basic_usage.py")
        print("2. Run the CLI demo: python -m shufflers.cli demo")
        print("3. Read the documentation in README.md")
        
        return 0
    else:
        print("❌ Some components are not working properly.")
        print("🔧 Please check the installation and dependencies.")
        
        print("\n🛠️ Troubleshooting:")
        print("1. Ensure you have Python 3.9+")
        print("2. Install with: uv add shufflers")
        print("3. Check for dependency conflicts")
        print("4. Try reinstalling in a clean environment")
        
        return 1


def main():
    """Main verification function."""
    try:
        return run_verification()
    except KeyboardInterrupt:
        print("\n\n⏹️ Verification interrupted by user.")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error during verification: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
