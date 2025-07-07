# Makefile
.PHONY: help setup test test-parallel test-smoke test-regression clean install

# Default target
help:
	@echo "Playwright Test Framework Commands:"
	@echo "=================================="
	@echo "make setup          - Install dependencies and setup framework"
	@echo "make test           - Run all tests"
	@echo "make test-parallel  - Run tests in parallel"
	@echo "make test-smoke     - Run smoke tests only"
	@echo "make test-regression - Run regression tests only"
	@echo "make test-firefox   - Run tests in Firefox"
	@echo "make test-webkit    - Run tests in WebKit"
	@echo "make test-mobile    - Run tests with mobile emulation"
	@echo "make test-debug     - Run tests with debug logging and visible browser"
	@echo "make test-logs      - Run tests with detailed console logging"
	@echo "make clean          - Clean test results and screenshots"
	@echo "make install        - Install Python dependencies only"
	@echo "make check-args     - Test argument parsing"

# Setup the entire framework
setup:
	@echo "Setting up Playwright Test Framework..."
	python setup.py

# Install dependencies only
install:
	@echo "Installing dependencies..."
	python test_runner.py --install

# Test argument parsing
check-args:
	@echo "Testing argument parsing..."
	python test_args.py --show-logs --log-level DEBUG --device "iPhone 12"

# Run all tests
test:
	@echo "Running all tests..."
	python test_runner.py

# Run tests in parallel
test-parallel:
	@echo "Running tests in parallel..."
	python test_runner.py --parallel

# Run smoke tests
test-smoke:
	@echo "Running smoke tests..."
	python test_runner.py --markers smoke

# Run regression tests
test-regression:
	@echo "Running regression tests..."
	python test_runner.py --markers regression

# Run tests in Firefox
test-firefox:
	@echo "Running tests in Firefox..."
	python test_runner.py --browser firefox

# Run tests in WebKit
test-webkit:
	@echo "Running tests in WebKit..."
	python test_runner.py --browser webkit

# Run tests with mobile emulation
test-mobile:
	@echo "Running tests with iPhone 12 emulation..."
	python test_runner.py --device "iPhone 12"

# Run tests with different devices
test-iphone:
	@echo "Running tests with iPhone 12..."
	python test_runner.py --device "iPhone 12"

test-ipad:
	@echo "Running tests with iPad..."
	python test_runner.py --device "iPad"

test-pixel:
	@echo "Running tests with Pixel 5..."
	python test_runner.py --device "Pixel 5"

test-desktop:
	@echo "Running tests with Desktop Chrome..."
	python test_runner.py --device "Desktop Chrome"

# Run tests with visual debugging
test-debug:
	@echo "Running tests in debug mode..."
	python test_runner.py --headless false --log-level DEBUG --show-logs

# Run tests with detailed logging
test-logs:
	@echo "Running tests with detailed console logging..."
	python test_runner.py --show-logs --log-level INFO

# Clean test results
clean:
	@echo "Cleaning test results..."
	rm -rf test-results/
	rm -rf screenshots/
	rm -rf allure-results/
	rm -rf allure-report/
	rm -rf logs/
	mkdir -p test-results screenshots allure-results logs

# Quick development workflow
dev: clean test-smoke
	@echo "Development test run completed!"

# CI/CD workflow
ci: test-parallel
	@echo "CI test run completed!"