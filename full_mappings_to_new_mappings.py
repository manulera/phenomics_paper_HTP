import pandas

old_mappings = pandas.read_csv('results/full_mappings_old.tsv', sep='\t', na_filter=False)
fyeco2chebi_mappings = pandas.read_csv('results/fyeco2chebi_mappings.tsv', sep='\t', na_filter=False)
chebi2fyeco_dict = dict()

for i, row in fyeco2chebi_mappings.iterrows():
    chebi2fyeco_dict[row['chebi_term']] = row['fyeco_term']


# old_mappings['chemical_or_agent'] = old_mappings['chemical_or_agent'].apply(str.split,args=['|'])
# old_mappings['condition_dose'] = old_mappings['condition_dose'].apply(str.split,args=['|'])

# old_mappings = old_mappings.explode(column=['chemical_or_agent', 'condition_dose'])

def formatting_function(row):
    fyeco_terms = row['fyeco_terms']
    for chebi, dose in  zip(row['chemical_or_agent'].split('|'), row['condition_dose'].split('|')):
        if ('CHEBI' in chebi):
            fyeco_term2replace = chebi2fyeco_dict[chebi]
            if chebi in chebi2fyeco_dict:
                fyeco_terms = fyeco_terms.replace(fyeco_term2replace, f'{fyeco_term2replace}({dose})')
            else:
                fyeco_terms = fyeco_terms + f',{fyeco_term2replace}({dose})'

    if 'FYECO:0000004' in fyeco_terms:
        fyeco_terms = fyeco_terms.replace('FYECO:0000004', f'FYECO:0000004({row["temperature"]})')
    else:
        fyeco_terms = fyeco_terms + f',FYECO:0000005({row["temperature"]})'

    return fyeco_terms


old_mappings['fyeco_terms'] = old_mappings.apply(formatting_function, axis=1)
old_mappings.to_csv('a.tsv', sep='\t', index=False)

