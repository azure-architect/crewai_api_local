# tests/crew/run_tests.py
import os
import sys
import unittest
from pathlib import Path

def setup_paths():
    """Setup correct Python paths for importing modules."""
    # Get the project root directory (two levels up from this script)
    script_dir = Path(__file__).parent.absolute()
    project_root = script_dir.parent.parent.absolute()
    
    # Remove any duplicate paths
    if str(project_root) in sys.path:
        sys.path.remove(str(project_root))
    
    # Add project root to sys.path FIRST to ensure it's found before any other paths
    sys.path.insert(0, str(project_root))
    
    print(f"Project root added to Python path: {project_root}")
    
    # Verify imports work
    try:
        import crew
        print("✓ Successfully imported crew package")
        
        import crew.interfaces
        print("✓ Successfully imported crew.clients package")
        
        from crew.interfaces import prompt_loader
        print("✓ Successfully imported prompt_loader module")
        
        print("All required modules imported successfully!")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        
        # Display directory structure for debugging
        print("\nCrew package structure:")
        crew_dir = project_root / "crew"
        for root, dirs, files in os.walk(crew_dir):
            level = root.replace(str(project_root), '').count(os.sep)
            indent = ' ' * 4 * level
            print(f"{indent}{os.path.basename(root)}/")
            sub_indent = ' ' * 4 * (level + 1)
            for file in files:
                print(f"{sub_indent}{file}")

def run_tests():
    """Run all test modules in the current directory."""
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern="test_*.py")
    
    # Run the tests
    runner = unittest.TextTestRunner()
    return runner.run(suite)

if __name__ == "__main__":
    print("Starting test runner...")
    
    # Setup import paths before running tests
    setup_paths()
    
    # Run tests
    result = run_tests()
    
    # Exit with appropriate code
    sys.exit(not result.wasSuccessful())