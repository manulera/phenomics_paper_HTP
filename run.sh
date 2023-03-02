set -e
# Download data of valid ids from PomBase and exon coordinates
# bash get_data.sh
python make_fyeco2chebi_mappings.py
# Make dictionaries that map FYPO terms to their labels or the CHEBI terms used in them
python ontology_to_term_dict.py data/fypo-edit.owl data/fypo-edit-dict.json data/fypo-edit-chebi-dict.json
# Make mapping between the condition substrings to FYECO terms, see 'results/mapping_conditions_*.tsv'
python mapping_conditions.py
# Make mapping between the phenotypes and FYPO terms, see mapping_phenotypes_*.tsv
python mapping_phenotypes.py
# Combine both mappings and add chebi terms and doses, see full_mappings.tsv
python full_mappings_to_new_mappings.py
python mapping_with_dose_and_temperature.py
# Create an intermediate format prior to formatting for pombase (keep only rows with phenotypes, only relevant columns)
python make_intermediate_dataset.py
# Create an intermediate format prior to formatting for pombase (keep only rows with phenotypes, only relevant columns) for microscopy data
python microscopy_phenotypes.py
# Create the file that can be submitted to PomBase
python make_pombase_dataset.py