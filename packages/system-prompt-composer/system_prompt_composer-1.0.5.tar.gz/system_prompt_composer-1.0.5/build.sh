#!/bin/bash

# Build script for prompt-composer

set -e

echo "Building prompt-composer..."

# Check if we're in the right directory
if [ ! -f "Cargo.toml" ]; then
    echo "Error: Must run from prompt-composer directory"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install maturin if not present
if ! command -v maturin &> /dev/null; then
    echo "Installing maturin..."
    pip install maturin
fi

# Build Rust library
echo "Building Rust library..."
cargo build --release

# Build Python extension
echo "Building Python extension..."
maturin develop --features python

# Run tests
echo "Running tests..."
cargo test

# Test Python integration
echo "Testing Python integration..."
python test_prompt_composer.py

echo "✅ Build completed successfully!"
echo ""
echo "To use in development:"
echo "  source venv/bin/activate"
echo "  python -c 'import system_prompt_composer; print(\"Ready!\")'"
echo ""
echo "To use in Python:"
echo "  import system_prompt_composer"
echo "  response = system_prompt_composer.compose_system_prompt(json_request)"
