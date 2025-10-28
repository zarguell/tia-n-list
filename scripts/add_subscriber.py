#!/usr/bin/env python3
"""
Subscriber management script for Tia N. List project.

This script provides a command-line interface for adding subscribers
to the Beehiiv newsletter via the API.
"""

import sys
import argparse
from src import distribution


def main():
    """Main function for subscriber management."""
    parser = argparse.ArgumentParser(description='Add subscriber to Tia N. List newsletter')
    parser.add_argument('email', help='Email address to add', required=True)
    parser.add_argument('--api-key', help='Beehiiv API key (optional, uses env var if not provided)')

    args = parser.parse_args()

    # Set API key if provided
    if args.api_key:
        import os
        os.environ['BEEHIIV_API_KEY'] = args.api_key

    try:
        success = distribution.add_subscriber(args.email)
        if success:
            print(f"✅ Successfully added subscriber: {args.email}")
            sys.exit(0)
        else:
            print(f"✗ Failed to add subscriber: {args.email}")
            sys.exit(1)

    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()