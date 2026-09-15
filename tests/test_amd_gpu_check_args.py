import shutil
import subprocess
from pathlib import Path

from core.platform_compat import find_bash


SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check-docker-amd-gpu.sh"

# Resolve bash explicitly rather than letting CreateProcess pick it. On Windows,
# C:\Windows\System32\bash.exe (the WSL launcher) is found before anything on
# PATH, and a default Git install does not put Git Bash on PATH at all, so
# shutil.which() also returns WSL. find_bash() rejects the WSL stub and falls
# back to the known Git Bash locations. On POSIX it resolves to the same
# /usr/bin/bash the bare name would have found.
BASH = find_bash() or "bash"

def test_amd_gpu_check_rejects_unknown_extra_arg_before_diagnostics():
    proc = subprocess.run(
        [BASH, str(SCRIPT), "--bad-option"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert proc.returncode == 1
    assert "Unknown option: --bad-option" in proc.stderr


def test_amd_gpu_check_shell_syntax():
    subprocess.run([BASH, "-n", str(SCRIPT)], check=True)
