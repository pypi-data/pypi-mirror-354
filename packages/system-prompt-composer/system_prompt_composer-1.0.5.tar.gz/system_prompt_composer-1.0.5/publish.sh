#!/bin/bash

# PyPI Publishing Script for prompt-composer
# This script will upload the built wheel to TestPyPI first, then PyPI

set -e

echo "🚀 Publishing prompt-composer to PyPI"
echo "======================================="

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Must run from prompt-composer directory"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Add cargo to PATH
export PATH="$HOME/.cargo/bin:$PATH"

# Build the package
echo "📦 Building package..."
maturin build --release --features python

# Check the wheel exists
WHEEL_FILE="target/wheels/prompt_composer-0.1.0-cp312-cp312-manylinux_2_34_x86_64.whl"
if [ ! -f "$WHEEL_FILE" ]; then
    echo "❌ Error: Wheel file not found: $WHEEL_FILE"
    exit 1
fi

echo "✅ Package built successfully!"
echo "   Wheel: $WHEEL_FILE"
echo ""

# Show what we're about to upload
echo "📋 Package details:"
echo "   Name: prompt-composer"
echo "   Version: 0.1.0"
echo "   Author: POSITRONIC AI LLC"
echo "   Repository: https://github.com/xcud/prompt-composer"
echo ""

# First, upload to TestPyPI
echo "🧪 Step 1: Uploading to TestPyPI..."
echo "   You'll need your TestPyPI API token"
echo "   Create one at: https://test.pypi.org/manage/account/token/"
echo ""

read -p "Do you want to upload to TestPyPI? (y/N): " upload_test
if [[ $upload_test =~ ^[Yy]$ ]]; then
    echo "Uploading to TestPyPI..."
    twine upload --repository testpypi "$WHEEL_FILE"
    
    echo ""
    echo "✅ Upload to TestPyPI complete!"
    echo "   Test with: pip install --index-url https://test.pypi.org/simple/ prompt-composer"
    echo ""
    
    read -p "Did the TestPyPI installation work? Upload to production PyPI? (y/N): " upload_prod
    if [[ $upload_prod =~ ^[Yy]$ ]]; then
        echo "🚀 Step 2: Uploading to production PyPI..."
        echo "   You'll need your PyPI API token"
        echo "   Create one at: https://pypi.org/manage/account/token/"
        echo ""
        
        twine upload "$WHEEL_FILE"
        
        echo ""
        echo "🎉 SUCCESS! Package published to PyPI!"
        echo "   Install with: pip install prompt-composer"
        echo "   View at: https://pypi.org/project/prompt-composer/"
    else
        echo "❌ Skipping production upload"
    fi
else
    echo "❌ Skipping TestPyPI upload"
fi

echo ""
echo "🏁 Publishing script complete!"
