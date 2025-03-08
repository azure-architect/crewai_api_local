# tests/crew/test_prompt_loader.py
import os
import sys
import unittest
from pathlib import Path

# Add project root to Python path if needed
project_root = Path(__file__).parent.parent.parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

try:
    from crew.interfaces.prompt_loader import (
        get_prompt,
        get_prompt_metadata,
        get_available_prompt_variants,
        list_tool_types
    )
except ImportError as e:
    print(f"Error importing prompt_loader: {e}")
    print("Python path:")
    for p in sys.path:
        print(f"  {p}")
    sys.exit(1)

class TestPromptLoader(unittest.TestCase):
    def setUp(self):
        # Set up test data
        self.tool_type = "keyword_extraction"
        self.variant = "standard"
    
    def test_get_prompt(self):
        """Test getting a prompt template."""
        prompt = get_prompt(self.tool_type, self.variant)
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)
    
    def test_get_prompt_metadata(self):
        """Test getting prompt metadata."""
        metadata = get_prompt_metadata(self.tool_type, self.variant)
        self.assertIsInstance(metadata, dict)
    
    def test_get_available_prompt_variants(self):
        """Test getting available prompt variants."""
        variants = get_available_prompt_variants(self.tool_type)
        self.assertIsInstance(variants, list)
        self.assertIn(self.variant, variants)
    
    def test_list_tool_types(self):
        """Test listing available tool types."""
        tool_types = list_tool_types()
        self.assertIsInstance(tool_types, list)
        self.assertIn(self.tool_type, tool_types)

if __name__ == "__main__":
    unittest.main()