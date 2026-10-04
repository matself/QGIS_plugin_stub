# {{ cookiecutter.plugin_name }}

{{ cookiecutter.short_description }}

Compatible with QGIS {{ cookiecutter.qgis_min_version }} up to {{ cookiecutter.qgis_max_version }} (Qt5 and Qt6).

## Development

Link the plugin folder into your QGIS profile so changes are picked up (use the Plugin Reloader plugin):

```powershell
# Windows (run once, adjust profile name if needed)
New-Item -ItemType Junction `
  -Path "$env:APPDATA\QGIS\QGIS3\profiles\default\python\plugins\{{ cookiecutter.module_name }}" `
  -Target "$PWD\{{ cookiecutter.module_name }}"
```

Build an installable zip:

```bash
python scripts/build_zip.py   # -> dist/{{ cookiecutter.module_name }}-{{ cookiecutter.version }}.zip
```

## Qt5 / Qt6 compatibility rules

- Import Qt only via `qgis.PyQt`, never `PyQt5` / `PyQt6`.
- Use fully scoped enums (`Qt.DockWidgetArea.RightDockWidgetArea`).
- Use `exec()`, not `exec_()`.
- Put anything that differs between QGIS 3 and 4 in `{{ cookiecutter.module_name }}/compat.py`.
- plugins.qgis.org runs an automatic Qt6 check on upload (see the *Qt6 Check* tab).

## License

{{ cookiecutter.license }} - see [LICENSE](LICENSE).
