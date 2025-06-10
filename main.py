import sys
from pipeline.cli import main

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("An error occurred: %s", e)
        sys.exit(1)