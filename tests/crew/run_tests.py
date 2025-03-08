#!/usr/bin/env python3
"""Test runner for the crew-local project."""

import os
import sys
import unittest
import argparse
from pathlib import Path


def discover_and_run_tests(test_path=None, pattern=None, verbosity=2):
    """Discover and run tests from the specified path."""
    # Set default test path if not provided
    if test_path is None:
        test_path = os.path.dirname(os.path.abspath(__file__))
    
    # Set default pattern if not provided
    if pattern is None:
        pattern = 'test_*.py'
    
    # Discover tests
    loader = unittest.TestLoader()
    test_suite = loader.discover(test_path, pattern=pattern)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(test_suite)
    
    # Return exit code based on test results
    return 0 if result.wasSuccessful() else 1


def run_specific_test(test_path, verbosity=2):
    """Run a specific test file."""
    # Check if the file exists
    if not os.path.exists(test_path):
        print(f"Error: Test file '{test_path}' not found.")
        return 1
    
    # Get the directory and filename
    directory = os.path.dirname(test_path) or '.'
    filename = os.path.basename(test_path)
    
    # Run the specific test
    return discover_and_run_tests(directory, filename, verbosity)


def main():
    """Main entry point for the test runner."""
    parser = argparse.ArgumentParser(description='Run tests for crew-local project')
    parser.add_argument(
        'test_path', 
        nargs='?', 
        help='Path to a specific test file or directory to run tests from'
    )
    parser.add_argument(
        '--pattern', '-p',
        default='test_*.py',
        help='Pattern to match test files (default: test_*.py)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='count',
        default=1,
        help='Increase verbosity (can be used multiple times)'
    )
    
    args = parser.parse_args()
    
    # Add the project root to the Python path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    # Determine if running a specific test file or discovering tests
    if args.test_path and os.path.isfile(args.test_path):
        return run_specific_test(args.test_path, args.verbose + 1)
    else:
        return discover_and_run_tests(args.test_path, args.pattern, args.verbose + 1)


if __name__ == "__main__":
    sys.exit(main())