#!/usr/bin/env python3
"""
Main entry point for EOMS package.

This module allows running EOMS using:
    python -m eoms --version
    python -m eoms --help
"""

import argparse
import sys

from eoms import __version__


def main():
    """Main entry point for EOMS package."""
    parser = argparse.ArgumentParser(
        description="EOMS - Execution & Order Management System",
        prog="python -m eoms"
    )
    
    parser.add_argument(
        "--version", 
        action="version", 
        version=f"EOMS {__version__}"
    )
    
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch the GUI application (same as: python -m eoms.gui)"
    )
    
    args = parser.parse_args()
    
    if args.gui:
        # Import and launch GUI
        try:
            from eoms.gui.__main__ import main as gui_main
            return gui_main()
        except ImportError as e:
            print(f"Error: GUI dependencies not available: {e}")
            print("Install with: pip install -e '.[gui]'")
            return 1
    else:
        # Default behavior - show help if no specific action
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())