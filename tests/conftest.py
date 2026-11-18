"""Shared helpers for the tool tests. Every fixture here is synthetic."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))


def run_tool(script, *args):
    """Run tools/<script> as the CI does and return the CompletedProcess."""
    return subprocess.run(
        [sys.executable, str(TOOLS / script), *map(str, args)],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
