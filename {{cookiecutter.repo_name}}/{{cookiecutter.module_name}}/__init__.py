"""{{ cookiecutter.plugin_name }} - QGIS plugin entry point."""


def classFactory(iface):  # noqa: N802 (name required by QGIS)
    """Load the plugin class. Called by QGIS."""
    from .plugin import {{ cookiecutter.class_name }}Plugin

    return {{ cookiecutter.class_name }}Plugin(iface)
