"""Dock widget for {{ cookiecutter.plugin_name }}."""
from qgis.PyQt.QtWidgets import QDockWidget, QLabel, QVBoxLayout, QWidget


class {{ cookiecutter.class_name }}DockWidget(QDockWidget):
    """Minimal code-only dock widget (no .ui file, so no uic differences Qt5/Qt6)."""

    def __init__(self, parent=None):
        super().__init__("{{ cookiecutter.plugin_name }}", parent)
        self.setObjectName("{{ cookiecutter.class_name }}DockWidget")

        content = QWidget(self)
        layout = QVBoxLayout(content)
        layout.addWidget(QLabel("Hello from {{ cookiecutter.plugin_name }}!"))
        layout.addStretch()
        self.setWidget(content)
