"""
Main entry point for the mplfontutils package.

Run this module to test font compatibility with a sample text.
Usage: python -m mplfontutils [-o OUTPUT] [text]
"""

import argparse
import sys

from .core import find_available_fonts


def main():
    """Main function to test font compatibility."""
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Test font compatibility with sample text",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m mplfontutils
  python -m mplfontutils "Your custom text"
  python -m mplfontutils "🎨 Emoji test 🎭" -o test_output.png
  python -m mplfontutils --output fonts_test.png "中文测试"
        """,
    )

    parser.add_argument("text", nargs="*", default=["Hello", "中文测试"], help="Text to test font compatibility with (default: 'Hello 中文测试')")

    parser.add_argument("-o", "--output", type=str, default=None, help="Output path for font test visualization image (optional; e.g., 'output.png')")

    # Parse arguments
    args = parser.parse_args()

    # Join text arguments into a single string
    test_text = " ".join(args.text)

    print(f"Testing font compatibility for: '{test_text}'")
    if args.output:
        print(f"Will save visualization to: {args.output}")
    print("-" * 50)

    # Find available fonts
    try:
        available_fonts = find_available_fonts(test_text, args.output)
        if available_fonts:
            print(f"Found {len(available_fonts)} compatible fonts:")
            print()
            for font in sorted(available_fonts):
                print(f"  • {font}")
        else:
            print("No compatible fonts found for the provided text.")

    except Exception as e:
        print(f"Error testing fonts: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
