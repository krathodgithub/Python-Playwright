#!/usr/bin/env python3
"""
Quick script to test if arguments are being parsed correctly
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description='Test argument parsing')

    # Test the same arguments as test_runner.py
    parser.add_argument('--install', action='store_true', help='Install dependencies')
    parser.add_argument('--parallel', action='store_true', help='Run tests in parallel')
    parser.add_argument('--workers', type=int, help='Number of parallel workers')
    parser.add_argument('--markers', help='Run tests with specific markers')
    parser.add_argument('--test-file', help='Run specific test file')
    parser.add_argument('--browser', choices=['chromium', 'firefox', 'webkit'], help='Browser to use')
    parser.add_argument('--headless', type=bool, help='Run in headless mode')
    parser.add_argument('--device', help='Device to emulate')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], help='Set logging level')
    parser.add_argument('--show-logs', action='store_true', help='Show logs in console during test execution')

    try:
        args = parser.parse_args()
        print("✅ Arguments parsed successfully!")
        print(f"Arguments received: {vars(args)}")

        if args.show_logs:
            print("✅ --show-logs flag detected correctly!")

    except SystemExit as e:
        print(f"❌ Argument parsing failed with exit code: {e.code}")
        parser.print_help()
        sys.exit(e.code)


if __name__ == '__main__':
    main()