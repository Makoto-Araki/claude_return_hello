import subprocess
import sys
from pathlib import Path

HELLO_PATH = Path(__file__).resolve().parent.parent / "src" / "hello.py"


def test_hello_prints_hello_to_stdout():
    result = subprocess.run(
        [sys.executable, str(HELLO_PATH)],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout == "Hello\n"
    assert result.stderr == ""
    assert result.returncode == 0
