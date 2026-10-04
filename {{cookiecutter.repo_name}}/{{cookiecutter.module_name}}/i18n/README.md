# Translations

Extract strings and compile translations (Qt Linguist tools required):

```bash
pylupdate5 plugin.py provider.py algorithms/example_algorithm.py -ts i18n/{{ cookiecutter.module_name }}_sv.ts
lrelease i18n/{{ cookiecutter.module_name }}_sv.ts
```

`plugin.py` loads `i18n/{{ cookiecutter.module_name }}_<locale>.qm` automatically.
Source strings stay in English.
