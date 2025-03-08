#!/usr/bin/env python3
"""Test script for the extraction tools using prompt templates."""

import sys
import os
import unittest
import json
from unittest.mock import MagicMock, patch
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the necessary modules
try:
    from crew.clients.prompt_loader import get_prompt
    print("Successfully imported prompt_loader module")
except ImportError as e:
    print(f"Error: Could not import prompt_loader module. Details: {e}")
    sys.exit(1)


# Create a mock extraction tool creator
def create_mock_extraction_tool(tool_type):
    """
    Create a mock extraction tool for testing.
    
    Args:
        tool_type: Type of extraction tool (keyword_extraction, theme_extraction, etc.)
        
    Returns:
        function: A mock extraction function
    """
    def extract_data(content, variant="standard"):
        """
        Mock extraction function.
        
        Args:
            content: The content to analyze
            variant: The prompt variant to use
            
        Returns:
            dict: Mock extraction results
        """
        # Get the actual prompt template to verify it exists and is properly formatted
        prompt_template = get_prompt(tool_type, variant)
        
        if not prompt_template:
            return {"error": f"Prompt template not found for {tool_type}/{variant}"}
        
        # Return mock results based on tool type
        mock_results = {
            "keyword_extraction": {
                "primary_keywords": ["test", "keywords", "extraction"],
                "secondary_keywords": ["more", "test", "keywords"],
                "technical_terms": ["term1", "term2"]
            },
            "theme_extraction": {
                "primary_theme": "Testing theme extraction",
                "secondary_themes": ["unit testing", "mocking"],
                "business_domains": ["software development"]
            },
            "process_extraction": {
                "has_processes": True,
                "processes": [
                    {
                        "process_name": "Test Process",
                        "steps_count": 3,
                        "is_complete": True,
                        "complexity": "Low",
                        "description": "A process for testing"
                    }
                ]
            },
            "entity_extraction": {
                "people": ["Test Person"],
                "organizations": ["Test Org"],
                "locations": ["Test Location"]
            }
        }
        
        # Return mock results for the tool type or a generic response
        return mock_results.get(tool_type, {"result": f"Mock data for {tool_type}"})
    
    return extract_data


class TestExtractionTools(unittest.TestCase):
    """Test cases for the extraction tools."""

    def test_keyword_extraction(self):
        """Test the keyword extraction tool with different variants."""
        tool_type = "keyword_extraction"
        extract_keywords = create_mock_extraction_tool(tool_type)
        
        variants = ["standard", "technical", "marketing", "domain"]
        test_content = "This is test content for keyword extraction."
        
        for variant in variants:
            print(f"\nTesting {tool_type} with {variant} variant...")
            result = extract_keywords(test_content, variant)
            
            # Verify result is not an error
            self.assertNotIn("error", result, f"Error in {tool_type} with {variant} variant")
            print(f"Result: {json.dumps(result, indent=2)}")
    
    def test_theme_extraction(self):
        """Test the theme extraction tool with different variants."""
        tool_type = "theme_extraction"
        extract_themes = create_mock_extraction_tool(tool_type)
        
        variants = ["standard", "technical", "marketing", "business"]
        test_content = "This is test content for theme extraction."
        
        for variant in variants:
            print(f"\nTesting {tool_type} with {variant} variant...")
            result = extract_themes(test_content, variant)
            
            # Verify result is not an error
            self.assertNotIn("error", result, f"Error in {tool_type} with {variant} variant")
            print(f"Result: {json.dumps(result, indent=2)}")
    
    def test_process_extraction(self):
        """Test the process extraction tool."""
        tool_type = "process_extraction"
        extract_processes = create_mock_extraction_tool(tool_type)
        
        test_content = """
        Process test:
        1. Step one
        2. Step two
        3. Step three
        """
        
        print(f"\nTesting {tool_type}...")
        result = extract_processes(test_content)
        
        # Verify result is not an error
        self.assertNotIn("error", result, f"Error in {tool_type}")
        print(f"Result: {json.dumps(result, indent=2)}")
    
    def test_entity_extraction(self):
        """Test the entity extraction tool."""
        tool_type = "entity_extraction"
        extract_entities = create_mock_extraction_tool(tool_type)
        
        test_content = """
        John Doe from Acme Corp visited New York last week.
        """
        
        print(f"\nTesting {tool_type}...")
        result = extract_entities(test_content)
        
        # Verify result is not an error
        self.assertNotIn("error", result, f"Error in {tool_type}")
        print(f"Result: {json.dumps(result, indent=2)}")
    
    def test_nonexistent_variant(self):
        """Test behavior with nonexistent variants."""
        tool_type = "keyword_extraction"
        extract_keywords = create_mock_extraction_tool(tool_type)
        
        result = extract_keywords("Test content", "nonexistent_variant")
        
        # Should return an error for nonexistent variant
        self.assertIn("error", result, "Should return error for nonexistent variant")


def run_tests():
    """Run the test suite."""
    unittest.main(argv=['first-arg-is-ignored'], exit=False)


if __name__ == "__main__":
    print("Testing extraction tools...")
    run_tests()
    print("All tests completed.")