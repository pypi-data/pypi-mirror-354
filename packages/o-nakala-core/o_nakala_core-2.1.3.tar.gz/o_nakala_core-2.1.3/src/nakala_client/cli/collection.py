#!/usr/bin/env python3
"""
CLI interface for NAKALA collection functionality.
This module provides the command-line interface for the collection functionality.
"""


def main():
    """Main entry point for nakala-collection CLI command."""
    # Import and execute the collection module main function
    from nakala_client.collection import main as collection_main

    collection_main()


if __name__ == "__main__":
    main()
