#!/usr/bin/env python3
"""
DEPRECATED: This script has been replaced by a comprehensive Makefile.

Please use the following commands instead:
- `make dev-setup` instead of `python dev_setup.py`
- `make help` to see all available commands
- See MIGRATION.md for a complete migration guide

This file is kept for backward compatibility but will be removed in a future version.

Original development script to install and test the package locally using uv.
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {cmd}")
    print(f"{'='*50}")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print("STDOUT:")
        print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    
    if result.returncode != 0:
        print(f"❌ Command failed with return code {result.returncode}")
        return False
    else:
        print("✅ Command completed successfully")
        return True

def check_uv_installed():
    """Check if uv is installed."""
    result = subprocess.run("uv --version", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ uv is not installed. Please install it first:")
        print("   curl -LsSf https://astral.sh/uv/install.sh | sh")
        print("   or: brew install uv")
        sys.exit(1)
    else:
        print(f"✅ uv is installed: {result.stdout.strip()}")

def main():
    """Main development workflow using uv."""
    print("🚀 Cobli Logging Formatter - Development Setup (with uv)")
    
    # Check if uv is installed
    check_uv_installed()
    
    # Sync dependencies and create virtual environment
    if not run_command("uv sync --dev", "Syncing dependencies and creating virtual environment"):
        sys.exit(1)
    
    # Install package in development mode
    if not run_command("uv pip install -e .", "Installing package in development mode"):
        sys.exit(1)
    
    # Run tests using uv
    if not run_command("uv run python -m pytest tests/ -v", "Running tests"):
        print("⚠️  Tests failed, but continuing...")
    
    # Run code formatting
    if not run_command("uv run python -m black cobli_logging/ tests/ examples/", "Formatting code with black"):
        print("⚠️  Code formatting failed, but continuing...")
    
    # Run linting
    if not run_command("uv run python -m flake8 cobli_logging/ --max-line-length=88 --extend-ignore=E203,W503", "Running linting with flake8"):
        print("⚠️  Linting failed, but continuing...")
    
    # Run type checking
    if not run_command("uv run python -m mypy cobli_logging/", "Running type checking with mypy"):
        print("⚠️  Type checking failed, but continuing...")
    
    # Test basic import
    if not run_command("uv run python -c 'from cobli_logging import get_logger; print(\"✅ Import successful\")'", 
                      "Testing basic import"):
        print("⚠️  Import test failed!")
        sys.exit(1)
    
    # Run example (with mocked ddtrace)
    if not run_command("uv run python test_package.py", "Running package test"):
        print("⚠️  Package test failed, but continuing...")
    
    print("\n🎉 Development setup completed!")
    print("\nNext steps:")
    print("1. Run tests: uv run python -m pytest")
    print("2. Format code: uv run python -m black .")
    print("3. Run examples: uv run python test_package.py")
    print("4. Build package: uv build")
    print("5. Sync dependencies: uv sync")
    print("6. Type checking: uv run python -m mypy cobli_logging/")

if __name__ == "__main__":
    main()
