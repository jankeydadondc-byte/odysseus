import shutil
import subprocess
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check-docker-amd-gpu.sh"



# Resolve bash from PATH rather than letting CreateProcess pick it. On Windows,
# C:\Windows\System32\bash.exe (the WSL launcher) lives in the system directory,
# which CreateProcess searches before PATH, so a bare "bash" runs WSL. WSL cannot
# see the repo at its Windows path (exit 127, "No such file or directory") and its
# /usr/bin shadows anything injected into PATH. shutil.which() returns the
# PATH-resolved bash (Git Bash here), which handles both correctly. On POSIX this
# resolves to the same /usr/bin/bash the bare name would have found.
BASH = shutil.which("bash") or "bash"

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
