"""List VISA resources without sending commands or changing instrument state."""
import argparse
import importlib


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", help="optional PyVISA backend/library path")
    args = parser.parse_args()
    visa = importlib.import_module("pyvisa")
    manager = visa.ResourceManager(args.backend) if args.backend else visa.ResourceManager()
    try:
        for resource in manager.list_resources():
            print(resource)
    finally:
        manager.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
