#!/usr/bin/env python3
"""
Setup script for Playwright Test Framework
One-click setup for the entire framework
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description=""):
    """Run a command and handle errors"""
    if description:
        print(f"\n{description}")

    print(f"Running: {' '.join(command)}")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False


def create_directories():
    """Create necessary directories"""
    directories = [
        'pages',
        'tests',
        'test-results',
        'screenshots',
        'test-results/videos'
    ]

    print("\nCreating directories...")
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"Created: {directory}")


def main():
    print("🚀 Setting up Playwright Test Framework")
    print("=" * 50)

    # Create directories
    create_directories()

    # Install Python dependencies
    if not run_command(
            [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
            "📦 Installing Python dependencies..."
    ):
        print("❌ Failed to install Python dependencies")
        sys.exit(1)

    # Install Playwright browsers
    if not run_command(
            [sys.executable, '-m', 'playwright', 'install'],
            "🌐 Installing Playwright browsers..."
    ):
        print("❌ Failed to install Playwright browsers")
        sys.exit(1)

    # Install Playwright system dependencies (for Linux)
    if os.name == 'posix':  # Linux/macOS
        run_command(
            [sys.executable, '-m', 'playwright', 'install-deps'],
            "🔧 Installing system dependencies..."
        )

    print("\n✅ Setup completed successfully!")
    print("\n🎯 Quick start commands:")
    print("   python test_runner.py                    # Run all tests")
    print("   python test_runner.py --parallel         # Run tests in parallel")
    print("   python test_runner.py --markers smoke    # Run smoke tests")
    print("   python test_runner.py --browser firefox  # Run with Firefox")
    print("\n📊 View reports at: test-results/report.html")
    print("📸 Screenshots saved to: screenshots/")


if __name__ == '__main__':
    main()