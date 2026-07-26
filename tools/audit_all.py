"""Daily audit entry point. Initial baseline parity is intentionally not checked here."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name('audit_worktree.py')), run_name='__main__')
