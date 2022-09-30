#%%
import pandas
from pronto import Ontology

fypo = Ontology('data/fypo-base.obo')
#%%
import re

data = pandas.read_excel('data/vals_spreadsheet.xlsx', sheet_name='OE_condition_metadata', na_filter=False)
resistance_terms = list()
sensitive_terms = list()
for condition, fypo_terms_string in zip(data['Condition Name'], data['phenotype']):
    fypo_terms = re.findall('FYPO:\d+',fypo_terms_string)
    sensitive_term = None
    resistance_term = None
    for term_id in fypo_terms:
        term = fypo[term_id]

        # Checks
        if not ('sensitive' in term.name or 'resistance' in term.name):
            print(term.name)

        # Assign term to resistant or sensitive
        if 'sensitive' in term.name:
            sensitive_term = term.id
        if 'resistance' in term.name:
            resistance_term = term.id

    sensitive_terms.append(sensitive_term)
    resistance_terms.append(resistance_term)

data['sensitive'] = sensitive_terms
data['resistance'] = resistance_terms


data[['Condition Name','sensitive', 'resistance']].to_csv('mapping_phenotypes2.tsv',sep='\t',index=False)
