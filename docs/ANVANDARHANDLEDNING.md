# Användarhandledning: QGIS-pluginmallen

Den här mallen skapar ett nytt QGIS-plugin som är kompatibelt med både QGIS 3 (Qt5) och QGIS 4 (Qt6). Du svarar på några frågor och får en färdig mapp med rätt filer, tester, CI och byggskript.

## 1. Förutsättningar

- Python 3.9 eller senare (på Windows fungerar startkommandot `py`)
- Git
- Cookiecutter: `py -m pip install --user cookiecutter`
- QGIS 3 och/eller 4 för att prova pluginet
- Valfritt: `ruff` och `pytest` (`py -m pip install --user ruff pytest`)

Windows hittar ofta inte `cookiecutter` direkt i PATH. Kör därför `py -m cookiecutter` i stället för bara `cookiecutter`.

## 2. Skapa ett nytt plugin

Interaktivt:

```bash
py -m cookiecutter C:\GITHUB\QGIS_plugin_stub -o C:\GITHUB
```

`-o` anger i vilken mapp det nya projektet skapas. Utan flaggan skapas det i den mapp du står i.

Utan frågor (värden du inte anger får standardvärdet):

```bash
py -m cookiecutter C:\GITHUB\QGIS_plugin_stub --no-input -o C:\GITHUB plugin_name="Min Karttjanst"
```

### Frågorna

| Fråga | Betydelse |
| --- | --- |
| `plugin_name` | Namnet som visas i QGIS. Från det räknas övriga namn ut. |
| `module_name` | Pythonpaketets namn, till exempel `min_karttjanst`. Endast a–z, 0–9 och `_`. Svenska tecken (å, ä, ö) godkänns inte. |
| `repo_name` | Namn på repomappen, till exempel `min-karttjanst`. |
| `class_name` | Namn på pluginklassen, till exempel `MinKarttjanst`. |
| `short_description` | En mening på engelska. |
| `version` | Startversion, till exempel `0.1.0`. |
| `author`, `email` | Visas i QGIS och på plugins.qgis.org. |
| `github_user` | Används för länkarna i `metadata.txt`. Standardvärdet är `matself`. |
| `qgis_min_version` | Lägsta QGIS-version. Standard 3.34. |
| `qgis_max_version` | Högsta QGIS-version. Standard 4.99, vilket gör pluginet tillgängligt för QGIS 4. |
| `category` | Kategori i pluginhanteraren. |
| `license` | GPL-2.0-or-later eller GPL-3.0-or-later. QGIS-plugin ska ha GPL-kompatibel licens. |
| `include_dockwidget` | `yes`: knappen i verktygsfältet visar/döljer en dockpanel. `no`: knappen visar ett meddelande. |
| `include_processing_provider` | `yes`: lägger till en Processing-provider med en exempelalgoritm. |
| `include_i18n` | `yes`: lägger till översättningsstöd och mappen `i18n/`. |
| `include_tests` | `yes`: lägger till pytest-tester. |
| `include_github_actions` | `yes`: lägger till CI-workflow. |
| `init_git` | `yes`: kör `git init` och gör första commit. |

Om du anger ett ogiltigt värde (till exempel ett modulnamn med å) avbryts genereringen med ett felmeddelande innan något skapas.

### Standardvärden

Du kan ändra standardvärdena i [cookiecutter.json](../cookiecutter.json), till exempel `author`, `email` och `github_user`, så slipper du fylla i dem varje gång.

## 3. Vad du får

Exempel för `plugin_name="Min Karttjanst"` med alla tillval:

```
min-karttjanst/
├── min_karttjanst/            ← själva pluginet (det här laddas in i QGIS)
│   ├── __init__.py            ← classFactory som QGIS anropar
│   ├── plugin.py              ← pluginklassen: initGui, unload, run
│   ├── compat.py              ← QGIS 3/4-anpassningar på ett ställe
│   ├── dockwidget.py          ← (om valt) dockpanelen
│   ├── provider.py            ← (om valt) Processing-provider
│   ├── algorithms/
│   │   └── example_algorithm.py   ← (om valt) exempelalgoritm
│   ├── i18n/                  ← (om valt) översättningar
│   ├── icon.svg
│   └── metadata.txt           ← pluginets metadata
├── tests/                     ← (om valt)
├── scripts/build_zip.py       ← bygger installationsbar zip-fil
├── .github/workflows/ci.yml   ← (om valt)
├── pyproject.toml             ← inställningar för ruff och pytest
├── README.md
├── LICENSE
└── .gitignore
```

Valda delar som du inte kryssat för tas bort automatiskt efter genereringen.

## 4. Prova pluginet i QGIS

QGIS läser plugin från din profilmapp. Det smidigaste under utveckling är att länka din källkodsmapp dit, så att ändringar syns direkt utan kopiering.

Kör i PowerShell, från det nya repots rotkatalog:

```powershell
New-Item -ItemType Junction `
  -Path "$env:APPDATA\QGIS\QGIS3\profiles\default\python\plugins\min_karttjanst" `
  -Target "$PWD\min_karttjanst"
```

Byt `min_karttjanst` mot ditt modulnamn. För QGIS 4 heter profilmappen sannolikt `QGIS4` i stället för `QGIS3`. Verifiera det på din dator, till exempel via *Inställningar → Användarprofiler → Öppna aktiv profilmapp* i QGIS.

Sedan:

1. Starta QGIS.
2. Öppna *Tillägg → Hantera och installera tillägg → Installerade*.
3. Bocka i ditt plugin. Syns det inte, bocka i *Visa experimentella*, eftersom mallen sätter `experimental=True`.
4. Klicka på knappen i verktygsfältet.

Installera gärna tillägget **Plugin Reloader** så kan du ladda om pluginet efter kodändringar utan att starta om QGIS.

Alternativ utan länk: bygg en zip (avsnitt 6) och använd *Installera från ZIP*.

## 5. Utveckla vidare

### Regler för QGIS 3 och 4

Följ dessa regler så fungerar samma kod i båda versionerna:

- Importera Qt bara via `qgis.PyQt` (aldrig `PyQt5` eller `PyQt6`).
- Använd fullt kvalificerade enum-värden: `Qt.DockWidgetArea.RightDockWidgetArea`, `Qgis.MessageLevel.Info`.
- Använd `exec()`, inte `exec_()`.
- Skriv `from qgis.PyQt import sip`, inte bara `import sip`.
- Allt som inte går att skriva så att det fungerar i båda versionerna läggs i `compat.py`. Se hur `QAction` och `FAST_INSERT` löses där.

Om du sänker `qgis_min_version` under 3.34 kan fler delar behöva anpassas (till exempel scopade enum-värden som infördes i olika 3.x-versioner).

### Lägga till en Processing-algoritm

Kopiera `algorithms/example_algorithm.py`, ändra klassnamn, `name()`, parametrar och `processAlgorithm`, och registrera den i `provider.py` i `loadAlgorithms()`:

```python
self.addAlgorithm(MinNyaAlgoritm())
```

### Översättningar

Källtexter ska vara på engelska. Se `i18n/README.md` i det genererade pluginet för hur du extraherar och kompilerar översättningar. Verktygsnamnet kan skilja mellan Qt5 och Qt6 (`pylupdate5` / `pylupdate6`), så kontrollera vad som finns installerat.

## 6. Tester, kontroll och bygge

Kör från det genererade repots rotkatalog:

```bash
py -m pytest              # metadatatester; QGIS-testet hoppas över utanför QGIS
py -m ruff check .        # stilkontroll
py scripts/build_zip.py   # skapar dist/<modul>-<version>.zip
```

Testet `test_plugin_load.py` laddar pluginet i en riktig QGIS. Det körs bara om `qgis` kan importeras, till exempel i CI-containern eller med QGIS egna Python.

### CI på GitHub

Workflowen kör ruff, tester mot QGIS-containrarna `qgis/qgis:ltr` och `qgis/qgis:latest`, och bygger zip-filen som artefakt. Kontrollera på Docker Hub att taggarna finns och att `latest` ger den QGIS-version du vill testa. Byt vid behov till en fast tagg.

### Skapa repot på GitHub

Mallen skapar bara ett lokalt repo. Vill du publicera det:

```bash
gh repo create min-karttjanst --private --source . --push
```

## 7. Publicera på plugins.qgis.org

1. Kontrollera att `LICENSE` innehåller den fullständiga GPL-texten. Post-hooken försöker hämta den från gnu.org, men om du var offline får du bara en kort notis och ett meddelande om det.
2. Fyll i `about`, `tags`, `changelog` och `experimental` i `metadata.txt`. Texterna ska vara på engelska.
3. Bygg zip-filen med `scripts/build_zip.py`.
4. Ladda upp på <https://plugins.qgis.org>. Vid uppladdning körs en automatisk Qt6-kontroll, och resultatet visas på fliken *Qt6 Check*.
5. Pluginet kan granskas innan uppladdning med skillen `qgis-plugin-review`.

## 8. Ändra mallen

Mallen ligger i `C:\GITHUB\QGIS_plugin_stub`:

| Du vill ändra | Fil |
| --- | --- |
| Frågor och standardvärden | `cookiecutter.json` |
| Kontroller före generering | `hooks/pre_gen_project.py` |
| Borttagning av valda delar, licenshämtning, git | `hooks/post_gen_project.py` |
| Innehållet i det genererade pluginet | `{{cookiecutter.repo_name}}/` |

Filerna i mallen innehåller Jinja-uttryck som `{{ cookiecutter.plugin_name }}` och är därför inte körbara som de är. Efter ändringar, kör mallens tester:

```bash
cd C:\GITHUB\QGIS_plugin_stub
py -m pytest
```

Testet genererar plugin med alla kombinationer av dockwidget och provider, kompilerar koden, kör ruff och metadatatesterna. Det tar cirka en minut.

Om du lägger till GitHub Actions-uttryck av typen `${{ ... }}` i mallfiler måste de omslutas med `{% raw %}` ... `{% endraw %}`, annars tolkar Cookiecutter dem som sina egna.

## 9. Felsökning

| Problem | Orsak och lösning |
| --- | --- |
| `cookiecutter` hittas inte | Använd `py -m cookiecutter`. |
| `Python was not found` | Använd `py` i stället för `python`, eller stäng av Microsoft Store-genvägen under *Inställningar → Appar → Appkörningsalias*. |
| Genereringen avbryts med "module_name ... must be lowercase ASCII" | Pluginnamnet gav ett ogiltigt modulnamn. Ange `module_name` själv, till exempel `module_name=min_karttjanst`. |
| Pluginet syns inte i QGIS | Kontrollera att junction-länken pekar på mappen som innehåller `metadata.txt`, och bocka i *Visa experimentella*. |
| Meddelande om att pluginet inte stöder din QGIS-version | Kontrollera `qgisMinimumVersion` och `qgisMaximumVersion` i `metadata.txt`. |
| LICENSE saknar full text | Hämta texten från gnu.org och klistra in den. |
| Fel i QGIS 4 som inte finns i QGIS 3 | Qt6 är striktare. Kontrollera Qt6-fliken på plugins.qgis.org och reglerna i avsnitt 5. |

## Källor

- QGIS migreringsguide för plugin: <https://plugins.qgis.org/docs/migrate-qgis4>
- Cookiecutter: <https://cookiecutter.readthedocs.io>
