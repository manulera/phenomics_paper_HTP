"""
Map the conditions from the condition column to FYECO terms
"""

from pronto import Ontology
import pandas

settings = [
    ('knock-out_condition_metadata', 'Condition_name_long'),
    ('OE_condition_metadata', 'Condition Name')
    ]

fyeco_ontology = Ontology('data/fyeco.obo')

for sheet_name, column_name in settings:
    
    # output / input file names depending on the sheet
    mappings_file = f'mappings/mapping_conditions_{sheet_name}.tsv'
    check_tsv = f'checks/mapping_conditions_{sheet_name}_long.tsv'
    check_md = f'checks/mapping_conditions_{sheet_name}_check.md'
    results_file = f'results/mapping_conditions_{sheet_name}.tsv'

    # create mapping_bits_dict: A dictionary to map the string bits flanked by underscores _  in Condition_name_long to
    # FYECO terms.
    # It is generated from the mappings files, that look like this:
    # Xylose2Gluc0.1	FYECO:0000414,FYECO:0000081	FYECO:0000137
    #
    # Xylose2Gluc0.1: name of the substring flanked by underscores
    # FYECO:0000414,FYECO:0000081: terms that the substring maps to, comma-separated
    # FYECO:0000137: terms to be excluded from the mapping. E.g. in this case exclude YES because of Xylose being the carbon source.
    #
    # The resulting dictionary looks like this {'Xylose2Gluc0.1': ['FYECO:0000414,FYECO:0000081', 'FYECO:0000137']}
    # the list may have length 1 or 2 depending on whether there are.

    mapping_bits_dict = dict()
    with open(mappings_file) as ins:
        # Skip header
        ins.readline()
        for line in ins:
            parts = line.strip().split('\t')
            # There might be two or three columsn in each line
            mapping_bits_dict[parts[0]] = parts[1:]

    # Use the dictionary to map the conditions to FYECO terms
    data = pandas.read_excel('data/elife-76000-supp1-v2.xlsx', sheet_name=sheet_name)
    mapping_condition_dict = dict()
    for condition in data[column_name]:
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

        mapping_condition_dict[condition] =  sorted(list(set(term for term in terms2include if term not in terms2remove)))

    with open(results_file,'w') as out:
        out.write(f'{column_name}\tfyeco_terms\n')
        for condition in data[column_name]:
            out.write(f'{condition}\t{",".join(mapping_condition_dict[condition])}\n')

    ## Print some extra checks
    # Double check that mappings are correct by printing markdown file

    with open(check_md,'w') as out:
        for condition in data[column_name]:
            fyeco_terms = mapping_condition_dict[condition]
            out.write(f'* {condition}\n')
            for term_id in fyeco_terms:
                if term_id == 'missing':
                    out.write('  * some mapping missing\n')
                if term_id == 'dose':
                    out.write('  * dose\n')
                if not term_id.startswith('FYECO'):
                    continue
                term = fyeco_ontology[term_id]
                out.write(f'  * id: {term.id}\n')
                out.write(f'    * name: {term.name}\n')
                out.write(f'    * def: {term.definition.lstrip()}\n')

    #  Print additional tsv file to verify right FYECO terms

    mappings = pandas.read_csv(mappings_file,delimiter='\t', na_filter=False)

    term_names = list()
    for term_ids in mappings['terms']:
        term_names.append('|'.join([fyeco_ontology[term_id].name for term_id in term_ids.split(',') if term_id not in ['skip', 'dose', 'temperature']]))

    exclude_names = list()
    for exclude_id in mappings['exclude_term']:
        exclude_names.append(fyeco_ontology[exclude_id].name if exclude_id else None)

    mappings['term_names'] = term_names
    mappings['exclude_term_name'] = exclude_names

    mappings.to_csv(check_tsv, sep='\t', index=False)