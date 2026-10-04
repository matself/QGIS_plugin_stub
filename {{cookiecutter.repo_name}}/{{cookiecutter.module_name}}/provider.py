"""Processing provider for {{ cookiecutter.plugin_name }}."""
from pathlib import Path

from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

from .algorithms.example_algorithm import ExampleAlgorithm


class {{ cookiecutter.class_name }}Provider(QgsProcessingProvider):
    def id(self):
        return "{{ cookiecutter.module_name }}"

    def name(self):
        return "{{ cookiecutter.plugin_name }}"

    def longName(self):  # noqa: N802
        return self.name()

    def icon(self):
        return QIcon(str(Path(__file__).parent / "icon.svg"))

    def loadAlgorithms(self):  # noqa: N802
        self.addAlgorithm(ExampleAlgorithm())
