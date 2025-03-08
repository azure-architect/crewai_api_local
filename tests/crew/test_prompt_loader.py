#!/usr/bin/env python3
"""Test script for the prompt loader functionality."""

import sys
import os
import unittest
import json
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the module to test
try:
    from crew.clients.prompt_loader import get_prompt, get_prompt_metadata, get_available_prompt_variants, list_tool_types
    print("Successfully imported prompt_loader module")
except ImportError as e:
    print(f"Error: Could not import prompt_loader module. Details: {e}")
    sys.exit(1)


class TestPromptLoader(unittest.TestCase):
    """Test cases for the prompt loader functionality."""

    def test_list_tool_types(self):
        """Test listing all available tool types."""
        tool_types = list_tool_types()
        print(f"Available tool types: {tool_types}")
        
        # Check that expected tool types exist
        expected_types = [
            "keyword_extraction", 
            "theme_extraction", 
            "process_extraction",
            "entity_extraction",
            "section_analyzer",
            "content_repurposing",
            "summary_generation",
            "code_analysis"
        ]
        
        for tool_type in expected_types:
            self.assertIn(tool_type, tool_types, f"Tool type '{tool_type}' should be available")
    
    def test_get_available_prompt_variants(self):
        """Test getting available prompt variants for each tool type."""
        tool_types = list_tool_types()
        
        for tool_type in tool_types:
            variants = get_available_prompt_variants(tool_type)
            print(f"Variants for {tool_type}: {variants}")
            
            # Check that the standard variant exists for each tool type
            self.assertIn("standard", variants, f"Standard variant should exist for '{tool_type}'")
            
    def test_get_prompt(self):
        """Test getting prompt templates for different tool types and variants."""
        test_cases = [
            ("keyword_extraction", "standard"),
            ("keyword_extraction", "technical"),
            ("theme_extraction", "standard"),
            ("process_extraction", "standard")
        ]
        
        for tool_type, variant in test_cases:
            prompt = get_prompt(tool_type, variant)
            
            # Check that the prompt exists and contains expected placeholders
            self.assertIsNotNone(prompt, f"Should get prompt for {tool_type}/{variant}")
            self.assertIn("{content}", prompt, f"Prompt should contain content placeholder")
            print(f"Successfully loaded {tool_type}/{variant} prompt")
            
    def test_get_prompt_metadata(self):
        """Test getting prompt metadata for different tool types."""
        test_cases = [
            ("keyword_extraction", "standard"),
            ("theme_extraction", "standard"),
            ("process_extraction", "standard")
        ]
        
        for tool_type, variant in test_cases:
            metadata = get_prompt_metadata(tool_type, variant)
            
            # Check that metadata exists and contains expected fields
            self.assertIsNotNone(metadata, f"Should get metadata for {tool_type}/{variant}")
            self.assertIn("template_id", metadata, "Metadata should contain template_id")
            self.assertIn("description", metadata, "Metadata should contain description")
            self.assertIn("version", metadata, "Metadata should contain version")
            print(f"Successfully loaded metadata for {tool_type}/{variant}")
            
    def test_nonexistent_prompt(self):
        """Test behavior with nonexistent prompts."""
        # Nonexistent variant
        prompt = get_prompt("keyword_extraction", "nonexistent")
        self.assertIsNone(prompt, "Should return None for nonexistent variant")
        
        # Nonexistent tool type
        prompt = get_prompt("nonexistent_type", "standard")
        self.assertIsNone(prompt, "Should return None for nonexistent tool type")


def run_tests():
    """Run the test suite."""
    unittest.main(argv=['first-arg-is-ignored'], exit=False)


if __name__ == "__main__":
    print("Testing prompt loader functionality...")
    run_tests()
    print("All tests completed.")