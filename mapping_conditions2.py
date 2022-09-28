"""
Map the conditions from the column Condition_name_long in supp1 to FYECO terms
"""
# %%
from pronto import Ontology
import pandas

# %% Build a dictionary with the mappings
#
# A dictionary to map the string bits flanked by underscores _  in Condition_name_long to
# FYECO terms

mapping_bits_dict = dict()
with open('mapping_conditions2.tsv') as ins:
    # Skip header
    ins.readline()
    for line in ins:
        parts = line.strip().split('\t')
        # There might be two or three columsn in each line
        mapping_bits_dict[parts[0]] = parts[1:]

# %% Do the mappings
data = pandas.read_excel('data/elife-76000-supp1-v2.xlsx', sheet_name='OE_condition_metadata')

mapping_condition_dict = dict()
for condition in data['Condition Name']:
    terms2include = list()
    terms2remove = list()
    mapping_list = mapping_bits_dict[condition]
    # Comma separated FYECO terms
    terms2include += mapping_list[0].split(',')
    # If some term has to be removed
    if len(mapping_list)==2:
        terms2remove.append(mapping_list[1])

    mapping_condition_dict[condition] =  [term for term in terms2include if term not in terms2remove]





# %% Print additional tsv file to verify right FYECO terms
ontology = Ontology('data/fyeco.obo')

mappings = pandas.read_csv('mapping_conditions2.tsv',delimiter='\t', na_filter=False)

term_names = list()
for term_ids in mappings['terms']:
    term_names.append('|'.join([ontology[term_id].name for term_id in term_ids.split(',') if term_id not in ['skip', 'dose', 'temperature']]))

exclude_names = list()
for exclude_id in mappings['exclude_term']:
    exclude_names.append(ontology[exclude_id].name if exclude_id else None)

mappings['term_names'] = term_names
mappings['exclude_term_name'] = exclude_names

mappings.to_csv('mapping_conditions2_long.tsv', sep='\t', index=False)