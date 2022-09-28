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
with open('mapping_conditions.tsv') as ins:
    # Skip header
    ins.readline()
    for line in ins:
        parts = line.strip().split('\t')
        # There might be two or three columsn in each line
        mapping_bits_dict[parts[0]] = parts[1:]

# %% Do the mappings
data = pandas.read_excel('data/elife-76000-supp1-v2.xlsx', sheet_name='knock-out_condition_metadata')

mapping_condition_dict = dict()
for condition in data['Condition_name_long']:
    terms2include = list()
    terms2remove = list()
    for c in condition.split('_'):
        # Empty
        if not c:
            continue
        mapping_list = mapping_bits_dict[c]
        # Comma separated FYECO terms
        terms2include += mapping_list[0].split(',')
        # If some term has to be removed
        if len(mapping_list)==2:
            terms2remove.append(mapping_list[1])

    mapping_condition_dict[condition] =  [term for term in terms2include if term not in terms2remove]

# %% Double check that mappings are correct by printing markdown file

ontology = Ontology('data/fyeco.obo')

with open('mapping_conditions_check.md','w') as out:
    for condition in data['Condition_name_long']:
        fyeco_terms = mapping_condition_dict[condition]
        out.write(f'* {condition}\n')
        for term_id in fyeco_terms:
            if term_id == 'missing':
                out.write('  * some mapping missing\n')
            if term_id == 'dose':
                out.write('  * dose\n')
            if not term_id.startswith('FYECO'):
                continue
            term = ontology[term_id]
            out.write(f'  * id: {term.id}\n')
            out.write(f'    * name: {term.name}\n')
            out.write(f'    * def: {term.definition.lstrip()}\n')

