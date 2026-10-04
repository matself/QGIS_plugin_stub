# QGIS plugin template (QGIS 3 + QGIS 4)

Cookiecutter template that generates a new QGIS plugin repository compatible with both
QGIS 3 (Qt5) and QGIS 4 (Qt6).

## Use

```bash
pip install cookiecutter
cookiecutter C:\GITHUB\QGIS_plugin_stub                 # interactive
cookiecutter C:\GITHUB\QGIS_plugin_stub --no-input plugin_name="My Map Tool"
```

Answers are asked for in the terminal; press Enter for the default. Defaults live in
`cookiecutter.json` - edit it to set your own name, e-mail and GitHub user.

## Options

| Option | Effect |
| --- | --- |
| `plugin_name` | Display name; `module_name`, `repo_name`, `class_name` are derived from it |
| `qgis_min_version` / `qgis_max_version` | Written to `metadata.txt` (default 3.34 - 4.99) |
| `include_dockwidget` | Adds a code-only dock widget toggled from the toolbar button |
| `include_processing_provider` | Adds a Processing provider with an example algorithm |
| `include_i18n` | Adds translation loading and an `i18n/` folder |
| `include_tests` | Adds pytest tests (metadata + load inside QGIS) |
| `include_github_actions` | Adds CI: ruff, tests on QGIS ltr + latest Docker images, zip artifact |
| `init_git` | Runs `git init` and makes the first commit |

The post-generation hook downloads the full GPL text from gnu.org (falls back to a short
notice if offline).

## Test the template

```bash
pip install cookiecutter pytest
pytest
```

## QGIS 4 compatibility notes

- `supportsQt6` is no longer recognised by QGIS. Use `qgisMaximumVersion=4.99` instead.
- Generated code imports Qt via `qgis.PyQt`, uses scoped enums and `exec()`; version
  differences are isolated in the plugin's `compat.py`.
- plugins.qgis.org runs `pyqgis4-checker` on uploads and reports results in a *Qt6 Check* tab.
- Sources: <https://plugins.qgis.org/docs/migrate-qgis4>
