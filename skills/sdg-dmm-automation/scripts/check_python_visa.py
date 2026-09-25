"""Read-only check of Python, PyVISA, and the VISA backend."""
import importlib
import platform
import sys


def main():
    print("python:", sys.version.split()[0])
    print("executable:", sys.executable)
    print("platform:", platform.platform())
    try:
        visa = importlib.import_module("pyvisa")
    except ImportError as exc:
        print("pyvisa: MISSING (%s)" % exc)
        return 2
    print("pyvisa:", getattr(visa, "__version__", "unknown"))
    try:
        manager = visa.ResourceManager()
        print("visa_backend:", getattr(manager, "visalib", None))
        print("resources:", list(manager.list_resources()))
        manager.close()
    except Exception as exc:
        print("visa_backend: ERROR (%s)" % exc)
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
