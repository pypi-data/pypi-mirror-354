import sys

def main():
    """Main entry point for the DedupeFlow application."""
    if len(sys.argv) < 2:
        print("Usage: python -m dedupeflow <data_file>")
        sys.exit(1)

    data_file = sys.argv[1]
    print(f"Running DedupeFlow on {data_file}")
