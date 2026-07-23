#!/bin/bash

# Navigate to project directory
cd "$(dirname "$0")/ecart"

# Step 1: Remove any existing venv if needed (optional)
if [ -d ".venv" ]; then
    echo "Removing existing .venv..."
    rm -rf .venv
fi

# Step 2: Create virtual environment
echo "Creating virtual environment..."
python -m venv .venv

# Step 3: Activate virtual environment (Git Bash-compatible)
echo "Activating virtual environment..."
source .venv/Scripts/activate

# Step 4: Install dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Setup complete."
else
    echo "⚠️ No requirements.txt found!"
fi
