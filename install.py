"""Explicit full user setup from a reviewed checkout/release; Python 3.12+."""
from pathlib import Path
import runpy

if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).resolve().parent /
                      "skills/intelligence-is-not-enough/scripts/install.py"), run_name="__main__")
