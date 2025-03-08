#!/usr/bin/env python3
# tests/crew/test_llm_tools.py

import sys
import os
import unittest
from unittest.mock import MagicMock, patch
import json
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the necessary modules
try:
    from crew.interfaces.prompt_loader import list_tool_types, get_prompt
    from crew.tools.base_tool import BaseTool
    # Import tool factory functions
    from crew.tools.LLM_keyword_extractor_tool import create_keyword_extraction_tool
    from crew.tools.LLM_primary_theme_extractor_tool import create_theme_extraction_tool
    from crew.tools.LLM_process_extractor_tool import create_process_extraction_tool
    from crew.tools.LLM_code_analysis_tool import create_code_analysis_tool
    from crew.tools.LLM_content_repurposing_tool import create_content_repurposing_tool
    from crew.tools.LLM_entity_extraction_tool import create_entity_extraction_tool
    from crew.tools.LLM_section_analyzer_tool import create_section_analyzer_tool
    from crew.tools.LLM_summary_generation_tool import create_summary_generation_tool
    
    print("Successfully imported LLM tool modules")
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure all tool files are in the correct location.")
    sys.exit(1)

class MockLLMClient:
    """Mock LLM client for testing tools."""
    
    def __init__(self, response_map=None):
        """
        Initialize mock client with predefined responses.
        
        Args:
            response_map: Dictionary mapping prompt prefixes to responses
        """
        self.response_map = response_map or {}
        self.calls = []
    
    def generate(self, prompt, model=None, options=None):
        """
        Mock generate method that returns predefined responses.
        
        Args:
            prompt: The prompt to generate from
            model: The model to use
            options: Generation options
            
        Returns:
            str: A predefined response or a default JSON string
        """
        self.calls.append({
            'prompt': prompt,
            'model': model,
            'options': options
        })
        
        # Check if we have a predefined response for this prompt
        for prefix, response in self.response_map.items():
            if prompt.startswith(prefix):
                return response
        
        # Default response: a valid JSON object with a "mock" key
        tool_type = "unknown"
        for type_name in list_tool_types():
            if type_name in prompt:
                tool_type = type_name
                break
        
        return f'{{"mock": true, "tool_type": "{tool_type}", "message": "This is a mock response"}}'

class TestLLMTools(unittest.TestCase):
    """Test cases for all LLM tools."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures that are reused across all tests."""
        cls.mock_client = MockLLMClient()
        
        # Create all tools with the mock client
        cls.tools = {
            'keyword_extraction': create_keyword_extraction_tool(cls.mock_client),
            'theme_extraction': create_theme_extraction_tool(cls.mock_client),
            'process_extraction': create_process_extraction_tool(cls.mock_client),
            'code_analysis': create_code_analysis_tool(cls.mock_client),
            'content_repurposing': create_content_repurposing_tool(cls.mock_client),
            'entity_extraction': create_entity_extraction_tool(cls.mock_client),
            'section_analyzer': create_section_analyzer_tool(cls.mock_client),
            'summary_generation': create_summary_generation_tool(cls.mock_client)
        }
    
    def test_tool_creation(self):
        """Test that all tools can be created successfully."""
        for tool_name, tool in self.tools.items():
            self.assertIsNotNone(tool, f"Failed to create {tool_name} tool")
            self.assertTrue(hasattr(tool, "name"), f"{tool_name} tool missing 'name' attribute")
            self.assertTrue(hasattr(tool, "description"), f"{tool_name} tool missing 'description' attribute")
    
    def test_prompt_loading(self):
        """Test that all tools can load their prompts correctly."""
        tool_types = list_tool_types()
        
        for tool_type in tool_types:
            prompt = get_prompt(tool_type, "standard") if tool_type != "summary_generation" else get_prompt(tool_type, "executive")
            self.assertIsNotNone(prompt, f"Failed to load prompt for {tool_type}")
            self.assertIsInstance(prompt, str, f"Prompt for {tool_type} is not a string")
            self.assertGreater(len(prompt), 0, f"Prompt for {tool_type} is empty")
    
    def test_tool_execution(self):
        """Test that all tools can execute with mock client."""
        test_content = "This is test content for tool execution."
        
        for tool_name, tool in self.tools.items():
            print(f"\nTesting execution of {tool_name} tool...")
            try:
                # Clear previous calls
                self.mock_client.calls = []
                
                # Execute the tool function with test content
                result = tool.func(test_content)
                
                # Verify the tool called the LLM client
                self.assertEqual(len(self.mock_client.calls), 1, f"{tool_name} tool didn't call LLM client exactly once")
                
                # Verify the result is not an error
                self.assertNotIn("error", result, f"{tool_name} tool returned an error: {result.get('error', '')}")
                
                # Verify the result has the expected content
                self.assertIn("mock", result, f"{tool_name} tool result missing expected content")
                self.assertTrue(result["mock"], f"{tool_name} tool result has incorrect value")
                self.assertEqual(result["tool_type"], tool_name if tool_name != "theme_extraction" else "unknown", 
                                f"{tool_name} tool result has incorrect tool_type")
                
                print(f"✓ {tool_name} tool execution successful")
            except Exception as e:
                print(f"✗ {tool_name} tool execution failed: {e}")
                raise
    
    def test_error_handling(self):
        """Test that all tools handle errors correctly."""
        # Create a client that returns invalid JSON
        bad_client = MockLLMClient({"Analyze": "This is not valid JSON"})
        
        for tool_name, tool_factory in {
            'keyword_extraction': create_keyword_extraction_tool,
            'code_analysis': create_code_analysis_tool,
            'summary_generation': create_summary_generation_tool
        }.items():
            # Create a tool with the bad client
            tool = tool_factory(bad_client)
            
            # Execute the tool and verify it handles the error
            result = tool.func("Test content")
            
            # Verify error is included in the result
            self.assertIn("error", result, f"{tool_name} tool didn't include error key in result")
            print(f"✓ {tool_name} tool correctly handled invalid JSON")

def run_tests():
    """Run all tests."""
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

if __name__ == "__main__":
    print("Testing LLM tools...")
    run_tests()
    print("All tests completed.")