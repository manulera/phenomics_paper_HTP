# Re-make mappings in a useful format for other publications

import pandas
import re

data = pandas.read_csv('full_mappings.tsv', sep='\t')

data['combined_fypo'] = data['sensitive'] + ' ' +  data['resistance']

data = data[['condition', 'sensitive_label', 'combined_fypo', 'fyeco_terms']]

def formatting_fun(x):
    terms = x.split(',')
    exclude = ['FYECO:0000005', 'FYECO:0000137', 'FYECO:0000334', 'FYECO:0000004', 'FYECO:0000126']
    terms = [term for term in terms if not any(e in term for e in exclude)]
    return ','.join(terms)

data['fyeco_terms'] = data['fyeco_terms'].apply(formatting_fun)

data.to_csv('reformatted/useful_mappings.tsv', sep='\t', index=False)