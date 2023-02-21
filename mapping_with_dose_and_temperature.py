import pandas
import json

with open('data/fypo-edit-chebi-dict.json') as ins:
    fypo2chebi = json.load(ins)

settings = [
    ('knock-out_condition_metadata', 'Condition_name_long'),
    ('OE_condition_metadata', 'Condition Name')
    ]



for sheet_name, column_name in settings:
    phenotype_mappings = pandas.read_csv(f'results/mapping_phenotypes_{sheet_name}.tsv', sep='\t', na_filter=False)
    condition_mappings = pandas.read_csv(f'results/mapping_conditions_{sheet_name}.tsv', sep='\t', na_filter=False)

    merged_data = phenotype_mappings.merge(condition_mappings, on=column_name)
    merged_data['chebi_chemicals'] = merged_data['sensitive'].apply(lambda x: fypo2chebi[x] if x in fypo2chebi else '')
    merged_data.to_csv(f'a_{sheet_name}.tsv', sep='\t', index=False)