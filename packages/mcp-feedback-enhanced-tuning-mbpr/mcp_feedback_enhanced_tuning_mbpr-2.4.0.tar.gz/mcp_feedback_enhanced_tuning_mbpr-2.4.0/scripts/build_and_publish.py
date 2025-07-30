#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build and Publish Script for MCP Feedback Enhanced Tuning MBPR
===============================================================

Script untuk build dan publish package ke PyPI dengan nama baru.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run command and return result"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(f"Output: {result.stdout}")
    return True

def clean_build():
    """Clean build directories"""
    print("🧹 Cleaning build directories...")
    
    build_dirs = ['build', 'dist', '*.egg-info']
    for pattern in build_dirs:
        for path in Path('.').glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"Removed directory: {path}")
            elif path.is_file():
                path.unlink()
                print(f"Removed file: {path}")

def build_package():
    """Build the package"""
    print("📦 Building package...")
    
    if not run_command("python -m build"):
        print("❌ Build failed!")
        return False
    
    print("✅ Package built successfully!")
    return True

def check_package():
    """Check package with twine"""
    print("🔍 Checking package...")
    
    if not run_command("python -m twine check dist/*"):
        print("❌ Package check failed!")
        return False
    
    print("✅ Package check passed!")
    return True

def publish_to_testpypi():
    """Publish to TestPyPI first"""
    print("🚀 Publishing to TestPyPI...")
    
    if not run_command("python -m twine upload --repository testpypi dist/*"):
        print("❌ TestPyPI upload failed!")
        return False
    
    print("✅ Published to TestPyPI successfully!")
    return True

def publish_to_pypi():
    """Publish to PyPI"""
    print("🚀 Publishing to PyPI...")
    
    if not run_command("python -m twine upload dist/*"):
        print("❌ PyPI upload failed!")
        return False
    
    print("✅ Published to PyPI successfully!")
    return True

def test_installation():
    """Test installation from PyPI"""
    print("🧪 Testing installation...")
    
    # Test with uvx
    if not run_command("uvx mcp-feedback-enhanced-tuning-mbpr@latest version"):
        print("❌ Installation test failed!")
        return False
    
    print("✅ Installation test passed!")
    return True

def main():
    """Main function"""
    print("🎯 MCP Feedback Enhanced Tuning MBPR - Build & Publish")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ pyproject.toml not found! Please run from project root.")
        sys.exit(1)
    
    # Check if required tools are installed
    required_tools = ["build", "twine"]
    for tool in required_tools:
        if not run_command(f"python -m {tool} --version"):
            print(f"❌ {tool} not installed! Please install with: pip install {tool}")
            sys.exit(1)
    
    # Ask user what to do
    print("\nWhat would you like to do?")
    print("1. Clean + Build + Check")
    print("2. Publish to TestPyPI")
    print("3. Publish to PyPI")
    print("4. Full workflow (Clean + Build + Check + TestPyPI + PyPI)")
    print("5. Test installation")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        clean_build()
        if build_package():
            check_package()
    
    elif choice == "2":
        if not Path("dist").exists():
            print("❌ No dist directory found! Please build first.")
            sys.exit(1)
        publish_to_testpypi()
    
    elif choice == "3":
        if not Path("dist").exists():
            print("❌ No dist directory found! Please build first.")
            sys.exit(1)
        
        confirm = input("⚠️  Are you sure you want to publish to PyPI? (yes/no): ").strip().lower()
        if confirm == "yes":
            publish_to_pypi()
        else:
            print("❌ Cancelled.")
    
    elif choice == "4":
        clean_build()
        if build_package() and check_package():
            if publish_to_testpypi():
                confirm = input("✅ TestPyPI upload successful! Proceed to PyPI? (yes/no): ").strip().lower()
                if confirm == "yes":
                    publish_to_pypi()
                    print("\n🎉 Full workflow completed successfully!")
                else:
                    print("❌ PyPI upload cancelled.")
    
    elif choice == "5":
        test_installation()
    
    else:
        print("❌ Invalid choice!")
        sys.exit(1)

if __name__ == "__main__":
    main()
