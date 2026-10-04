"""Validate the answers before anything is generated."""
import re
import sys

module_name = "{{ cookiecutter.module_name }}"
class_name = "{{ cookiecutter.class_name }}"
min_version = "{{ cookiecutter.qgis_min_version }}"
max_version = "{{ cookiecutter.qgis_max_version }}"
version = "{{ cookiecutter.version }}"

errors = []

if not re.fullmatch(r"[a-z][a-z0-9_]*", module_name):
    errors.append(
        f"module_name '{module_name}' must be lowercase ASCII (a-z, 0-9, _) and start "
        "with a letter, because it becomes the Python package name."
    )
if not class_name.isidentifier() or not class_name.isascii():
    errors.append(f"class_name '{class_name}' is not a valid ASCII Python identifier.")
for label, value in (("qgis_min_version", min_version), ("qgis_max_version", max_version)):
    if not re.fullmatch(r"\d+\.\d+(\.\d+)?", value):
        errors.append(f"{label} '{value}' must look like 3.34 or 4.99.")
if not re.fullmatch(r"\d+\.\d+\.\d+", version):
    errors.append(f"version '{version}' must look like 0.1.0.")

if errors:
    print("ERROR: " + "\n       ".join(errors), file=sys.stderr)
    sys.exit(1)
