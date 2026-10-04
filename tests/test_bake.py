"""Generate the template with several option combinations and sanity-check the output."""
import compileall
import itertools
import subprocess
import sys
from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter

TEMPLATE = Path(__file__).resolve().parent.parent

COMBOS = list(itertools.product(["yes", "no"], repeat=2))  # dockwidget x processing


@pytest.mark.parametrize("dock,processing", COMBOS)
def test_bake(tmp_path, dock, processing):
    out = cookiecutter(
        str(TEMPLATE),
        no_input=True,
        output_dir=str(tmp_path),
        extra_context={
            "include_dockwidget": dock,
            "include_processing_provider": processing,
            "init_git": "no",
        },
    )
    repo = Path(out)
    pkg = repo / "my_qgis_plugin"

    assert (pkg / "metadata.txt").exists()
    assert (pkg / "dockwidget.py").exists() == (dock == "yes")
    assert (pkg / "provider.py").exists() == (processing == "yes")
    assert (pkg / "algorithms").exists() == (processing == "yes")

    # no unrendered Jinja left behind (the CI matrix expression is the one exception)
    for path in repo.rglob("*"):
        if path.is_file() and path.name != "ci.yml":
            assert "cookiecutter" not in path.read_text(encoding="utf-8", errors="ignore"), path

    assert compileall.compile_dir(str(repo), quiet=1, force=True)

    lint = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "."], cwd=repo, capture_output=True, text=True
    )
    if "No module named ruff" not in lint.stderr:
        assert lint.returncode == 0, lint.stdout

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "tests/test_metadata.py"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_invalid_module_name_is_rejected(tmp_path):
    with pytest.raises(Exception):
        cookiecutter(
            str(TEMPLATE),
            no_input=True,
            output_dir=str(tmp_path),
            extra_context={"plugin_name": "Åäö Plugin", "init_git": "no"},
        )
