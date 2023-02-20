import pandas
import json
import re

with open('data/fypo-edit-dict.json') as ins:
    fypo = json.load(ins)

def nb_different_words(str1, str2):
    print(str1, str2)
    # Split the strings into lists of words
    list1 = str1.split()
    list2 = str2.split()

    # Create sets of words
    set1 = set(list1)
    set2 = set(list2)

    # Find the words that differ between the sets
    return len(set1.symmetric_difference(set2))

for sheet_name, column_name in [('knock-out_condition_metadata', 'Condition_name_long'), ('OE_condition_metadata', 'Condition Name')]:

    data = pandas.read_excel('data/vals_spreadsheet.xlsx', sheet_name=sheet_name, na_filter=False)
    resistance_terms = list()
    sensitive_terms = list()
    resistance_term_names = list()
    sensitive_term_names = list()
    for condition, fypo_terms_string in zip(data[column_name], data['phenotype']):
        fypo_terms = re.findall('FYPO:\d+',fypo_terms_string)
        sensitive_term = None
        resistance_term = None
        sensitive_term_name = None
        resistance_term_name = None

        for term_id in fypo_terms:
            term_name = fypo[term_id]

            # Assign term to resistant or sensitive
            if 'sensitive' in term_name or 'decreased' in term_name or 'reduced' in term_name or 'loss' in term_name:
                sensitive_term = term_id
                sensitive_term_name = term_name
            if 'resistance' in term_name or 'increased' in term_name:
                resistance_term = term_id
                resistance_term_name = term_name
        if sensitive_term is None or resistance_term is None:
            print(fypo_terms)
            exit(0)
        sensitive_terms.append(sensitive_term)
        sensitive_term_names.append(sensitive_term_name)
        resistance_terms.append(resistance_term)
        resistance_term_names.append(resistance_term_name)


    data['sensitive'] = sensitive_terms
    data['resistance'] = resistance_terms

    data['sensitive_label'] = sensitive_term_names
    data['resistance_label'] = resistance_term_names

    data['difference'] = data.apply(lambda r: nb_different_words(r['sensitive_label'], r['resistance_label']),axis=1)

    data.loc[data['difference'] != 2,['sensitive_label', 'resistance_label']].to_csv(f'data/mapping_phenotypes_{sheet_name}_check.tsv', sep='\t', index=False)
    if 'Condition_name_long' in data:
        data[['Condition_name_long','Condition_short','sensitive', 'resistance', 'sensitive_label', 'resistance_label']].to_csv(f'mapping_phenotypes_{sheet_name}.tsv',sep='\t',index=False)
    else:
        data[['Condition Name','sensitive', 'resistance', 'sensitive_label', 'resistance_label']].to_csv(f'mapping_phenotypes_{sheet_name}.tsv',sep='\t',index=False)
