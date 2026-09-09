import os
import pytest

from tests.helpers.cli_loader import load_script


@pytest.mark.skipif(
    os.name == "nt",
    reason="asserts the POSIX execute bit; Windows has no X_OK to clear, "
           "so chmod(0o644) leaves os.access(path, os.X_OK) True",
)
def test_is_runnable_subcommand_requires_executable_file(tmp_path):
    cli = load_script("odysseus")
    sub = tmp_path / "odysseus-demo"
    sub.write_text("#!/bin/sh\n")
    sub.chmod(0o644)

    assert cli._is_runnable_subcommand(sub) is False

    sub.chmod(0o755)
    assert cli._is_runnable_subcommand(sub) is True
