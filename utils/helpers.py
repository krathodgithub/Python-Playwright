"""
Utility helper functions for the testing framework
"""

import os
import json
import csv
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import random
import string


class TestDataHelper:
    """Helper class for managing test data"""

    @staticmethod
    def load_json_data(file_path: str) -> Dict[str, Any]:
        """Load test data from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Warning: Test data file {file_path} not found")
            return {}

    @staticmethod
    def load_csv_data(file_path: str) -> List[Dict[str, Any]]:
        """Load test data from CSV file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return list(csv.DictReader(file))
        except FileNotFoundError:
            print(f"Warning: Test data file {file_path} not found")
            return []

    @staticmethod
    def generate_random_string(length: int = 10) -> str:
        """Generate random string"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def generate_random_email() -> str:
        """Generate random email address"""
        username = TestDataHelper.generate_random_string(8)
        domain = random.choice(['example.com', 'test.org', 'demo.net'])
        return f"{username}@{domain}"

    @staticmethod
    def generate_test_user() -> Dict[str, str]:
        """Generate test user data"""
        return {
            'username': f"user_{TestDataHelper.generate_random_string(6)}",
            'email': TestDataHelper.generate_random_email(),
            'password': f"Pass{TestDataHelper.generate_random_string(6)}!",
            'first_name': random.choice(['John', 'Jane', 'Alice', 'Bob', 'Carol']),
            'last_name': random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones'])
        }


class FileHelper:
    """Helper class for file operations"""

    @staticmethod
    def create_directory(path: str) -> None:
        """Create directory if it doesn't exist"""
        Path(path).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def delete_file(file_path: str) -> bool:
        """Delete file if it exists"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")
            return False

    @staticmethod
    def clean_directory(directory: str, older_than_days: int = 7) -> None:
        """Clean files older than specified days"""
        try:
            current_time = time.time()
            cutoff_time = current_time - (older_than_days * 24 * 60 * 60)

            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.getmtime(file_path) < cutoff_time:
                        FileHelper.delete_file(file_path)
        except Exception as e:
            print(f"Error cleaning directory {directory}: {e}")


class WaitHelper:
    """Helper class for wait utilities"""

    @staticmethod
    def wait_for_condition(condition_func, timeout: int = 30, interval: float = 0.5) -> bool:
        """Wait for a condition to be true"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                if condition_func():
                    return True
            except:
                pass
            time.sleep(interval)
        return False

    @staticmethod
    def retry_action(action_func, max_attempts: int = 3, delay: float = 1.0):
        """Retry an action with exponential backoff"""
        for attempt in range(max_attempts):
            try:
                return action_func()
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise e
                time.sleep(delay * (2 ** attempt))


class EnvironmentHelper:
    """Helper class for environment management"""

    @staticmethod
    def get_env_var(key: str, default: str = None) -> str:
        """Get environment variable with default"""
        return os.getenv(key, default)

    @staticmethod
    def is_ci_environment() -> bool:
        """Check if running in CI environment"""
        ci_indicators = ['CI', 'CONTINUOUS_INTEGRATION', 'GITHUB_ACTIONS', 'JENKINS_URL', 'TRAVIS']
        return any(os.getenv(indicator) for indicator in ci_indicators)

    @staticmethod
    def get_browser_from_env() -> str:
        """Get browser from environment with fallback"""
        return EnvironmentHelper.get_env_var('DEFAULT_BROWSER', 'chromium')

    @staticmethod
    def should_run_headless() -> bool:
        """Determine if tests should run headless"""
        return (EnvironmentHelper.get_env_var('HEADLESS', 'false').lower() == 'true' or
                EnvironmentHelper.is_ci_environment())


class ScreenshotHelper:
    """Helper class for screenshot management"""

    @staticmethod
    def generate_screenshot_name(test_name: str, timestamp: bool = True) -> str:
        """Generate screenshot filename"""
        clean_name = "".join(c for c in test_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        clean_name = clean_name.replace(' ', '_')

        if timestamp:
            timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            return f"{clean_name}_{timestamp_str}.png"
        return f"{clean_name}.png"

    @staticmethod
    def save_screenshot_metadata(screenshot_path: str, test_info: Dict[str, Any]) -> None:
        """Save screenshot metadata"""
        metadata_path = screenshot_path.replace('.png', '_metadata.json')
        try:
            with open(metadata_path, 'w', encoding='utf-8') as file:
                json.dump(test_info, file, indent=2, default=str)
        except Exception as e:
            print(f"Warning: Could not save screenshot metadata: {e}")


class ReportHelper:
    """Helper class for report generation"""

    @staticmethod
    def generate_test_summary(results_dir: str) -> Dict[str, Any]:
        """Generate test execution summary"""
        summary = {
            'timestamp': datetime.now().isoformat(),
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'duration': 0,
            'environment': {
                'python_version': os.sys.version,
                'platform': os.name,
                'ci_environment': EnvironmentHelper.is_ci_environment()
            }
        }

        # This would be enhanced to parse actual test results
        return summary

    @staticmethod
    def create_html_report(summary: Dict[str, Any], output_path: str) -> None:
        """Create a simple HTML report"""
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Execution Summary</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .summary {{ background: #f5f5f5; padding: 20px; border-radius: 5px; }}
                .passed {{ color: green; }}
                .failed {{ color: red; }}
                .skipped {{ color: orange; }}
            </style>
        </head>
        <body>
            <h1>Test Execution Summary</h1>
            <div class="summary">
                <p><strong>Timestamp:</strong> {timestamp}</p>
                <p><strong>Total Tests:</strong> {total_tests}</p>
                <p class="passed"><strong>Passed:</strong> {passed}</p>
                <p class="failed"><strong>Failed:</strong> {failed}</p>
                <p class="skipped"><strong>Skipped:</strong> {skipped}</p>
                <p><strong>Duration:</strong> {duration}s</p>
                <p><strong>Environment:</strong> {environment}</p>
            </div>
        </body>
        </html>
        """

        try:
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(html_template.format(**summary))
        except Exception as e:
            print(f"Error creating HTML report: {e}")


class BrowserHelper:
    """Helper class for browser-specific utilities"""

    @staticmethod
    def get_browser_args(browser_name: str, headless: bool = False) -> List[str]:
        """Get browser-specific arguments"""
        args = []

        if browser_name.lower() == 'chromium':
            args.extend([
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--disable-web-security',
                '--allow-running-insecure-content'
            ])
            if headless:
                args.append('--headless')

        elif browser_name.lower() == 'firefox':
            if headless:
                args.append('--headless')

        elif browser_name.lower() == 'webkit':
            # WebKit specific args if needed
            pass

        return args

    @staticmethod
    def get_mobile_devices() -> Dict[str, Dict[str, Any]]:
        """Get mobile device configurations"""
        return {
            'iPhone 12': {
                'viewport': {'width': 390, 'height': 844},
                'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X)'
            },
            'iPad': {
                'viewport': {'width': 820, 'height': 1180},
                'user_agent': 'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X)'
            },
            'Samsung Galaxy S21': {
                'viewport': {'width': 384, 'height': 854},
                'user_agent': 'Mozilla/5.0 (Linux; Android 11; SM-G991B)'
            }
        }


class ValidationHelper:
    """Helper class for common validations"""

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Validate URL format"""
        import re
        pattern = r'^https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?$'
        return re.match(pattern, url) is not None

    @staticmethod
    def is_strong_password(password: str) -> bool:
        """Validate password strength"""
        import re
        # At least 8 characters, one uppercase, one lowercase, one digit, one special char
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        return re.match(pattern, password) is not None


class DatabaseHelper:
    """Helper class for database operations (if needed)"""

    @staticmethod
    def cleanup_test_data(connection_string: str, test_user_prefix: str = 'test_') -> None:
        """Clean up test data from database"""
        # Implementation would depend on specific database
        # This is a placeholder for database cleanup operations
        pass

    @staticmethod
    def create_test_data(connection_string: str, data: Dict[str, Any]) -> None:
        """Create test data in database"""
        # Implementation would depend on specific database
        # This is a placeholder for test data creation
        pass


class APIHelper:
    """Helper class for API operations"""

    @staticmethod
    def build_api_url(base_url: str, endpoint: str, params: Dict[str, Any] = None) -> str:
        """Build API URL with parameters"""
        import urllib.parse

        url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        if params:
            query_string = urllib.parse.urlencode(params)
            url = f"{url}?{query_string}"

        return url

    @staticmethod
    def create_auth_headers(token: str, token_type: str = 'Bearer') -> Dict[str, str]:
        """Create authorization headers"""
        return {
            'Authorization': f"{token_type} {token}",
            'Content-Type': 'application/json'
        }