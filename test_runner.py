#!/usr/bin/env python3
"""
Test Runner for Playwright Test Framework
Simple script to run tests with different configurations
"""

import subprocess
import sys
import os
import argparse
from pathlib import Path


class TestRunner:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.ensure_directories()

    def ensure_directories(self):
        """Create necessary directories"""
        directories = [
            'test-results',
            'screenshots',
            'test-results/videos',
            'allure-results',
            'allure-report',
            'logs'
        ]

        for directory in directories:
            Path(directory).mkdir(exist_ok=True)

    def run_command(self, command):
        """Run a command and return the result"""
        print(f"Running: {' '.join(command)}")
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
            return result.returncode == 0
        except Exception as e:
            print(f"Error running command: {e}")
            return False

    def install_dependencies(self):
        """Install required dependencies"""
        print("Installing dependencies...")

        # Install Python packages
        if not self.run_command([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt']):
            return False

        # Install Playwright browsers
        if not self.run_command([sys.executable, '-m', 'playwright', 'install']):
            return False

        print("Dependencies installed successfully!")
        return True

    def check_allure_cli(self):
        """Check if Allure CLI is installed"""
        try:
            result = subprocess.run(['allure', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Allure CLI found: {result.stdout.strip()}")
                return True
        except FileNotFoundError:
            pass

        print("⚠️ Allure CLI not found. Install with:")
        print("   npm install -g allure-commandline")
        print("   or: brew install allure")
        return False

    def run_tests(self, args):
        """Run tests with specified parameters"""
        command = [sys.executable, '-m', 'pytest']

        # Add basic options
        command.extend([
            '-v',
            '--tb=short',
            '--html=test-results/report.html',
            '--self-contained-html',
            '--junitxml=test-results/junit.xml'
        ])

        # Add Allure options if enabled
        if getattr(args, 'allure', False):
            # Check if Allure CLI is available
            if self.check_allure_cli():
                command.extend(['--alluredir=allure-results'])
                print("📊 Allure reporting enabled")
            else:
                print("⚠️ Allure CLI not found, using HTML reports only")

        # Add logging options
        if getattr(args, 'show_logs', False):
            command.extend(['--capture=no', '-s'])
            print("🔍 Console logging enabled")
        else:
            command.extend(['--capture=sys'])

        # Add parallel execution if specified
        if getattr(args, 'parallel', False):
            workers = getattr(args, 'workers', None)
            if workers:
                command.extend(['-n', str(workers)])
            else:
                command.extend(['-n', 'auto'])
            print(f"🚀 Parallel execution enabled")

        # Add markers if specified
        markers = getattr(args, 'markers', None)
        if markers:
            command.extend(['-m', markers])
            print(f"🏷️ Running tests with markers: {markers}")

        # Add specific test file if specified
        test_file = getattr(args, 'test_file', None)
        if test_file:
            command.append(test_file)
            print(f"📁 Running specific test file: {test_file}")
        else:
            command.append('tests/')

        # Set environment variables
        env = os.environ.copy()

        browser = getattr(args, 'browser', None)
        if browser:
            env['BROWSER'] = browser
            print(f"🌐 Browser: {browser}")

        headless = getattr(args, 'headless', None)
        if headless is not None:
            env['HEADLESS'] = str(headless).lower()
            print(f"👁️ Headless: {headless}")

        device = getattr(args, 'device', None)
        if device:
            env['DEVICE'] = device
            print(f"📱 Device: {device}")

        log_level = getattr(args, 'log_level', None)
        if log_level:
            env['LOG_LEVEL'] = log_level.upper()
            print(f"📋 Log level: {log_level}")

        # Run tests
        print("\n" + "=" * 60)
        print(f"🚀 Running command: {' '.join(command)}")
        print("=" * 60)

        try:
            result = subprocess.run(command, env=env)
            success = result.returncode == 0

            # Generate Allure report if requested and tests completed
            if getattr(args, 'allure', False) and self.check_allure_cli():
                print("\n📊 Generating Allure report...")
                if self.generate_allure_report():
                    print("🌐 Allure report available at: allure-report/index.html")
                    print("💡 Tip: Run 'allure open allure-report' to view in browser")

            # Always show HTML report location
            print(f"\n📋 HTML report available at: test-results/report.html")

            return success

        except Exception as e:
            print(f"❌ Error running tests: {e}")
            return False

    def generate_allure_report(self):
        """Generate Allure report if allure is installed"""
        try:
            # Check if we have results
            if not os.path.exists('allure-results') or not os.listdir('allure-results'):
                print("⚠️ No Allure results found")
                return False

            # Generate report
            cmd = ['allure', 'generate', 'allure-results', '-o', 'allure-report', '--clean']
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print("✅ Allure report generated successfully!")
                return True
            else:
                print(f"❌ Failed to generate Allure report: {result.stderr}")
                return False

        except Exception as e:
            print(f"❌ Error generating Allure report: {e}")
            return False

    def serve_allure_report(self, port=8080):
        """Serve Allure report on local server"""
        try:
            print(f"🌐 Starting Allure server on port {port}...")
            subprocess.run(['allure', 'serve', 'allure-results', '--port', str(port)])
        except Exception as e:
            print(f"❌ Could not start Allure server: {e}")


def main():
    print("🎯 Playwright Test Framework Runner")
    print("=" * 50)

    parser = argparse.ArgumentParser(
        description='Run Playwright tests with various options',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_runner.py                                    # Run all tests
  python test_runner.py --parallel                         # Run tests in parallel  
  python test_runner.py --show-logs                        # Show logs in console
  python test_runner.py --allure                           # Generate Allure report
  python test_runner.py --device "iPhone 12"               # Run with device emulation
  python test_runner.py --browser firefox --show-logs      # Run with Firefox and logs
  python test_runner.py --parallel --markers smoke --device "iPhone 12" --show-logs --allure
        """
    )

    # Test execution options
    parser.add_argument('--install', action='store_true',
                        help='Install dependencies and setup framework')
    parser.add_argument('--parallel', action='store_true',
                        help='Run tests in parallel using all CPU cores')
    parser.add_argument('--workers', type=int, metavar='N',
                        help='Number of parallel workers (default: auto-detect)')
    parser.add_argument('--markers', metavar='MARKER',
                        help='Run tests with specific markers (smoke, regression, etc.)')
    parser.add_argument('--test-file', metavar='FILE',
                        help='Run specific test file or directory')

    # Browser options
    parser.add_argument('--browser', choices=['chromium', 'firefox', 'webkit'],
                        help='Browser to use for testing')
    parser.add_argument('--headless', type=bool, metavar='BOOL',
                        help='Run in headless mode (true/false)')
    parser.add_argument('--device', metavar='DEVICE',
                        help='Device to emulate (iPhone 12, iPad, Pixel 5, etc.)')

    # Logging options
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                        help='Set logging level for detailed output')
    parser.add_argument('--show-logs', action='store_true',
                        help='Show detailed logs in console during test execution')

    # Report options
    parser.add_argument('--allure', action='store_true',
                        help='Generate Allure report after test execution')
    parser.add_argument('--serve-allure', type=int, metavar='PORT', nargs='?',
                        const=8080, help='Serve Allure report on specified port (default: 8080)')

    # Parse arguments and handle errors gracefully
    try:
        args = parser.parse_args()

        # Debug: Print parsed arguments
        print(f"📋 Parsed arguments: {vars(args)}")

    except SystemExit as e:
        if e.code != 0:
            print("\n❌ Argument parsing failed!")
            parser.print_help()
        sys.exit(e.code)

    runner = TestRunner()

    # Install dependencies if requested
    if args.install:
        print("📦 Installing dependencies...")
        if not runner.install_dependencies():
            print("❌ Failed to install dependencies")
            sys.exit(1)
        print("✅ Dependencies installed successfully")
        return

    # Serve Allure report if requested
    if args.serve_allure:
        print("🌐 Serving Allure report...")
        runner.serve_allure_report(args.serve_allure)
        return

    # Run tests
    print("🚀 Starting test execution...")
    success = runner.run_tests(args)

    # Print final result
    if success:
        print("\n✅ Tests completed successfully!")
        if getattr(args, 'allure', False):
            print("📊 Allure report: allure-report/index.html")
        print("📋 HTML report: test-results/report.html")
    else:
        print("\n❌ Tests failed or encountered errors!")

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()