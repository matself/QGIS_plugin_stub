"""Remove files for options that were switched off, fetch the license, init git."""
import shutil
import subprocess
import urllib.request
from pathlib import Path

ROOT = Path.cwd()
PKG = ROOT / "{{ cookiecutter.module_name }}"

LICENSE_URLS = {
    "GPL-2.0-or-later": "https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt",
    "GPL-3.0-or-later": "https://www.gnu.org/licenses/gpl-3.0.txt",
}


def remove(path):
    path = Path(path)
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


if "{{ cookiecutter.include_dockwidget }}" != "yes":
    remove(PKG / "dockwidget.py")

if "{{ cookiecutter.include_processing_provider }}" != "yes":
    remove(PKG / "provider.py")
    remove(PKG / "algorithms")

if "{{ cookiecutter.include_i18n }}" != "yes":
    remove(PKG / "i18n")

if "{{ cookiecutter.include_tests }}" != "yes":
    remove(ROOT / "tests")

if "{{ cookiecutter.include_github_actions }}" != "yes":
    remove(ROOT / ".github")


def fetch_license():
    """Download the full license text; keep the short notice if offline."""
    url = LICENSE_URLS["{{ cookiecutter.license }}"]
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            text = response.read().decode("utf-8")
    except Exception as exc:  # offline, proxy, ... -> keep the notice
        print(f"NOTE: could not download the full license text ({exc}).")
        print(f"      Replace LICENSE with the full text from {url} before publishing.")
        return
    notice = (ROOT / "LICENSE").read_text(encoding="utf-8")
    (ROOT / "LICENSE").write_text(notice + "\n" + "-" * 72 + "\n\n" + text, encoding="utf-8")


fetch_license()


def git(*args):
    subprocess.run(["git", *args], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)


if "{{ cookiecutter.init_git }}" == "yes":
    try:
        git("init", "-b", "main")
        git("add", "-A")
        git("commit", "-m", "Initial commit from QGIS plugin template")
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"NOTE: git setup failed ({exc}); run 'git init' manually.")

print()
print("Created {{ cookiecutter.repo_name }}.")
print("Next: develop with a symlink/junction from your QGIS profile's plugins folder to")
print("      the '{{ cookiecutter.module_name }}' directory, or run scripts/build_zip.py.")
