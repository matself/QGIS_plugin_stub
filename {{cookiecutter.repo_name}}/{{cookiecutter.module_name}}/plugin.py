"""Main plugin class for {{ cookiecutter.plugin_name }}."""
from pathlib import Path

{% if cookiecutter.include_dockwidget != "yes" and cookiecutter.include_processing_provider == "yes" -%}
from qgis.core import Qgis, QgsApplication
{% elif cookiecutter.include_dockwidget != "yes" -%}
from qgis.core import Qgis
{% elif cookiecutter.include_processing_provider == "yes" -%}
from qgis.core import QgsApplication
{% endif -%}
{% if cookiecutter.include_i18n == "yes" and cookiecutter.include_dockwidget == "yes" -%}
from qgis.PyQt.QtCore import QCoreApplication, QSettings, Qt, QTranslator
{% elif cookiecutter.include_i18n == "yes" -%}
from qgis.PyQt.QtCore import QCoreApplication, QSettings, QTranslator
{% elif cookiecutter.include_dockwidget == "yes" -%}
from qgis.PyQt.QtCore import Qt
{% endif -%}
from qgis.PyQt.QtGui import QIcon

from .compat import QAction
{% if cookiecutter.include_dockwidget == "yes" -%}
from .dockwidget import {{ cookiecutter.class_name }}DockWidget
{% endif -%}
{% if cookiecutter.include_processing_provider == "yes" -%}
from .provider import {{ cookiecutter.class_name }}Provider
{% endif %}
PLUGIN_NAME = "{{ cookiecutter.plugin_name }}"


class {{ cookiecutter.class_name }}Plugin:
    """QGIS plugin implementation."""

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = Path(__file__).parent
        self.action = None
{%- if cookiecutter.include_dockwidget == "yes" %}
        self.dock = None
{%- endif %}
{%- if cookiecutter.include_processing_provider == "yes" %}
        self.provider = None
{%- endif %}
{%- if cookiecutter.include_i18n == "yes" %}
        self.translator = None
        self._load_translation()

    def _load_translation(self):
        locale = QSettings().value("locale/userLocale", "en")[:2]
        path = self.plugin_dir / "i18n" / f"{{ cookiecutter.module_name }}_{locale}.qm"
        if path.exists():
            self.translator = QTranslator()
            self.translator.load(str(path))
            QCoreApplication.installTranslator(self.translator)
{%- endif %}

    @staticmethod
    def tr(message):
{%- if cookiecutter.include_i18n == "yes" %}
        return QCoreApplication.translate("{{ cookiecutter.class_name }}Plugin", message)
{%- else %}
        return message
{%- endif %}

    def initGui(self):  # noqa: N802 (name required by QGIS)
        icon = QIcon(str(self.plugin_dir / "icon.svg"))
        self.action = QAction(icon, self.tr(PLUGIN_NAME), self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&" + PLUGIN_NAME, self.action)
{%- if cookiecutter.include_processing_provider == "yes" %}

        self.provider = {{ cookiecutter.class_name }}Provider()
        QgsApplication.processingRegistry().addProvider(self.provider)
{%- endif %}

    def unload(self):
        self.iface.removePluginMenu("&" + PLUGIN_NAME, self.action)
        self.iface.removeToolBarIcon(self.action)
        self.action.deleteLater()
        self.action = None
{%- if cookiecutter.include_dockwidget == "yes" %}
        if self.dock is not None:
            self.iface.removeDockWidget(self.dock)
            self.dock.deleteLater()
            self.dock = None
{%- endif %}
{%- if cookiecutter.include_processing_provider == "yes" %}
        if self.provider is not None:
            QgsApplication.processingRegistry().removeProvider(self.provider)
            self.provider = None
{%- endif %}
{%- if cookiecutter.include_i18n == "yes" %}
        if self.translator is not None:
            QCoreApplication.removeTranslator(self.translator)
            self.translator = None
{%- endif %}

    def run(self):
{%- if cookiecutter.include_dockwidget == "yes" %}
        if self.dock is None:
            self.dock = {{ cookiecutter.class_name }}DockWidget(self.iface.mainWindow())
            self.iface.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)
        self.dock.setVisible(not self.dock.isVisible())
{%- else %}
        self.iface.messageBar().pushMessage(
            PLUGIN_NAME, self.tr("Hello from the plugin!"), level=Qgis.MessageLevel.Info
        )
{%- endif %}
