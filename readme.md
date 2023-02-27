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
# Download data of valid ids from PomBase
curl -k https://www.pombase.org/data/names_and_identifiers/gene_IDs_names.tsv | tail -n+2 >> valid_ids_data/gene_IDs_names.tsv
# Make dictionaries that map FYPO terms to their labels or the CHEBI terms used in them
python ontology_to_term_dict.py data/fypo-edit.owl data/fypo-edit-dict.json data/fypo-edit-chebi-dict.json
# Make mapping between the condition substrings to FYECO terms, see 'results/mapping_conditions_*.tsv'
python mapping_conditions.py
# Make mapping between the phenotypes and FYPO terms, see mapping_phenotypes_*.tsv
python mapping_phenotypes.py
# Combine both mappings and add chebi terms and doses, see full_mappings.tsv
python mapping_with_dose_and_temperature.py
# Create an intermediate format prior to formatting for pombase (keep only rows with phenotypes, only relevant columns)
python make_intermediate_dataset.py
# Create an intermediate format prior to formatting for pombase (keep only rows with phenotypes, only relevant columns) for microscopy data
python microscopy_phenotypes.py
# Create the file that can be submitted to PomBase
python make_pombase_dataset.py
```
