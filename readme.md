# PMID:34984977

default temp is 32 °C

```bash
poetry install
poetry shell
```

```bash
bash get_data.sh
python ontology_to_term_dict.py data/fypo-edit.owl data/fypo-edit-dict.json data/fypo-edit-chebi-dict.json
python mapping_conditions.py
python mapping_phenotypes.py
python mapping_with_dose_and_temperature.py
```