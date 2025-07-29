#!/usr/bin/env python3
"""
CLI interface for NAKALA curator functionality.
This module provides the command-line interface for the curator functionality.
"""


def main():
    """Main entry point for nakala-curator CLI command."""
    # Import and execute the curator module main function
    from nakala_client.curator import main as curator_main

    curator_main()


if __name__ == "__main__":
    main()
