Files to format data from PMID:34984977 for PomBase HTP data

## Mappings

All files are in the `mappings` directory:

* vals_spreadsheet: manual mappings between fypo terms and conditions
* self-explaining tsv files
* missing_conditions: conditions that are used in the data, but not listed in the metadata in supplementary data 1

## Run the mappings

Install dependencies

```bash
poetry install
poetry shell
```

Run this:

```bash
# Download necessary files from pombase and from elife
bash get_data.sh
# Dictionaries that map FYPO terms to their labels or to their 
python ontology_to_term_dict.py data/fypo-edit.owl data/fypo-edit-dict.json data/fypo-edit-chebi-dict.json
python mapping_conditions.py
python mapping_phenotypes.py
python mapping_with_dose_and_temperature.py
python make_intermediate_dataset.py
python microscopy_phenotypes.py
python make_pombase_dataset.py 
```