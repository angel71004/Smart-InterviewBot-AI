"""
Setup script for AI Interview Question Generator
Run this script to install dependencies and download required models
"""

import subprocess
import sys
import os

def run_command(command):
    """Run a shell command and print output"""
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return False

def main():
    print("=" * 50)
    print("AI Interview Question Generator - Setup")
    print("=" * 50)
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Install requirements
    print("\n1. Installing Python packages...")
    if not run_command(f"{sys.executable} -m pip install --upgrade pip"):
        print("Failed to upgrade pip")
        sys.exit(1)
    
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt"):
        print("Failed to install requirements")
        sys.exit(1)
    
    # Download spaCy model
    print("\n2. Downloading spaCy language model...")
    if not run_command(f"{sys.executable} -m spacy download en_core_web_sm"):
        print("Failed to download spaCy model")
        print("You can manually run: python -m spacy download en_core_web_sm")
    
    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("=" * 50)
    print("\nTo run the application:")
    print("  streamlit run app.py")
    print("\nMake sure you're in the project directory:")

if __name__ == "__main__":
    main()

