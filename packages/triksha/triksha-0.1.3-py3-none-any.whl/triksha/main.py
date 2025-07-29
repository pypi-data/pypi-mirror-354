#!/usr/bin/env python3
"""
Triksha CLI - Command Line Interface for Advanced LLM Security Testing

This is the main entry point for the Triksha command-line interface.
"""

import os
import sys

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

from .cli.core import TrikshaCLI

def main():
    """Main entry point for the CLI."""
    try:
        cli = TrikshaCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()