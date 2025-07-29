"""
Triksha - Advanced LLM Security Testing System

A comprehensive framework for testing and evaluating Large Language Model security,
including red teaming, guardrail testing, and vulnerability assessment.
"""

__version__ = "0.1.3"
__author__ = "Triksha Team"
__email__ = "info@triksha.ai"

# Core imports
try:
    from .cli.core import TrikshaCLI
    from .utils.db_handler import DravikDB
except ImportError:
    # Fallback for development/testing
    TrikshaCLI = None
    DravikDB = None

def main():
    """Main entry point for the Triksha CLI."""
    import sys
    import os
    
    # Add the package directory to the Python path
    package_dir = os.path.dirname(os.path.abspath(__file__))
    if package_dir not in sys.path:
        sys.path.insert(0, package_dir)
    
    try:
        # Load environment variables
        try:
            from .utils.env_loader import load_environment
            load_environment()
        except ImportError:
            try:
                from dotenv import load_dotenv
                load_dotenv()
            except ImportError:
                pass
        
        # Import and run the CLI
        from .main import main as cli_main
        cli_main()
        
    except ImportError as e:
        print(f"Error importing Triksha modules: {e}")
        print("Please ensure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error running Triksha: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 