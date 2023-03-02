import pandas
from pronto import Ontology
import re

fyeco_ontology = Ontology('data/fyeco.obo')
# chebi_ontology = Ontology('data/chebi_import.owl')
chebi_dict = dict()
with open('data/chebi_import.owl', 'r') as ins:
    for line in ins:
        line = line.strip()
        re_match = re.match(r'# Class: <http://purl.obolibrary.org/obo/CHEBI_(\d+)> \((.+?)\)', line)
        if re_match:
            g = re_match.groups()
            chebi_dict['CHEBI:' + g[0]] = g[1]

remove_fyeco_terms = ['FYECO:0000137', 'FYECO:0000334', 'FYECO:0000126']

mappings = pandas.read_csv('results/full_mappings_old.tsv', sep='\t', na_filter=False)

mappings['fyeco_terms'] = mappings.fyeco_terms.apply(lambda x: ','.join(i for i in x.split(',') if i not in remove_fyeco_terms))

mappings = mappings.loc[(mappings.fyeco_terms != '') & ~mappings.fyeco_terms.str.contains(',') & ~mappings.chemical_or_agent.str.contains('|',regex=False) & mappings.chemical_or_agent.str.contains('CHEBI'),['fyeco_terms', 'chemical_or_agent']].copy()

manual_mappings = pandas.DataFrame([
    ['FYECO:0000334', 'CHEBI:87192'],
    ['FYECO:0000181', 'CHEBI:17234'],
    ['FYECO:0000081', 'CHEBI:17234']
], columns=['fyeco_terms', 'chemical_or_agent'])
mappings = pandas.concat([mappings, manual_mappings])

# Delete link between stationary phase and glucose
mappings = mappings[mappings.fyeco_terms!='FYECO:0000123'].copy()

mappings['fyeco_label'] = mappings.fyeco_terms.apply(lambda x: fyeco_ontology[x].name)
mappings['chebi_label'] = mappings.chemical_or_agent.apply(lambda x: chebi_dict[x])
mappings.rename(columns={'chemical_or_agent': 'chebi_term', 'fyeco_terms': 'fyeco_term'}, inplace=True)
mappings.drop_duplicates(inplace=True)
mappings.to_csv('results/fyeco2chebi_mappings.tsv', sep='\t', index=False)

