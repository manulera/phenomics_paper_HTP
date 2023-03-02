import pandas

mappings = pandas.read_csv('results/full_mappings_old.tsv', sep='\t', na_filter=False)
fyeco2chebi_mappings = pandas.read_csv('results/fyeco2chebi_mappings.tsv', sep='\t', na_filter=False)
chebi2fyeco_dict = dict()

for i, row in fyeco2chebi_mappings.iterrows():
    chebi2fyeco_dict[row['chebi_term']] = row['fyeco_term']



def formatting_function(row):
    fyeco_terms = row['fyeco_terms']
    for chebi, dose in  zip(row['chemical_or_agent'].split('|'), row['condition_dose'].split('|')):
        if ('CHEBI' in chebi):
            if chebi == 'CHEBI:17234':
                glucose_terms = ['FYECO:0000181', 'FYECO:0000081']
                if not any(t in fyeco_terms for t in glucose_terms):
                    fyeco_terms = fyeco_terms + (f',FYECO:0000081({dose})' if ('0.1' in dose) else f',FYECO:0000181({dose})')
                    continue
                for fyeco_term2replace in glucose_terms:
                    fyeco_terms = fyeco_terms.replace(fyeco_term2replace, f'{fyeco_term2replace}({dose})')
            else:
                fyeco_term2replace = chebi2fyeco_dict[chebi]
                fyeco_terms = fyeco_terms.replace(fyeco_term2replace, f'{fyeco_term2replace}({dose})')

    if 'FYECO:0000004' in fyeco_terms:
        fyeco_terms = fyeco_terms.replace('FYECO:0000004', f'FYECO:0000004({row["temperature"]})')
    else:
        fyeco_terms = fyeco_terms + f',FYECO:0000005({row["temperature"]})'

    if 'FYECO:0000315' in fyeco_terms:
        fyeco_terms = fyeco_terms.replace('FYECO:0000315', f'FYECO:0000315({row["condition_dose"]})')
    return fyeco_terms

mappings['fyeco_terms'] = mappings.apply(formatting_function, axis=1)
mappings.drop(columns=['chemical_or_agent', 'condition_dose', 'temperature'], inplace=True)
mappings.to_csv('results/full_mappings.tsv', sep='\t', index=False)

