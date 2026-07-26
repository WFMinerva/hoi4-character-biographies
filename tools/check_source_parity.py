"""Deprecated compatibility wrapper. Use verify_initial_baseline.py only for migration checks."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name('verify_initial_baseline.py')), run_name='__main__')
