import pandas
import json

with open('data/fypo-edit-chebi-dict.json') as ins:
    fypo2chebi = json.load(ins)

settings = [
    ('knock-out_condition_metadata', 'Condition_name_long'),
    ('OE_condition_metadata', 'Condition Name')
    ]

all_data = list()

for sheet_name, column_name in settings:
    phenotype_mappings = pandas.read_csv(f'results/mapping_phenotypes_{sheet_name}.tsv', sep='\t', na_filter=False)
    condition_mappings = pandas.read_csv(f'results/mapping_conditions_{sheet_name}.tsv', sep='\t', na_filter=False)
    manual_chebi_mappings = pandas.read_csv(f'mappings/manual_chebi_mappings_{sheet_name}.tsv', sep='\t', na_filter=False)
    spreadsheet_data: pandas.DataFrame = pandas.read_excel('mappings/vals_spreadsheet.xlsx', sheet_name=sheet_name, na_filter=False)
    if sheet_name == 'knock-out_condition_metadata':
        dose_table = spreadsheet_data.loc[:,[ column_name, 'Dose', 'Unit']]
        dose_table['Dose'] = dose_table['Dose'].astype('str')
        dose_table['condition_dose'] = dose_table.apply(lambda x: x['Dose'] + x['Unit'], axis=1)
        dose_table.drop(columns=['Dose', 'Unit'], inplace=True)
    else:
        dose_table = spreadsheet_data.loc[:,[ column_name, 'Dose']]
        dose_table.rename(columns={'Dose': 'condition_dose'}, inplace=True)


    merged_data = phenotype_mappings.merge(condition_mappings, on=column_name)
    merged_data['original_index'] = merged_data.index

    manually_mapped = merged_data.merge(manual_chebi_mappings, on=column_name)
    manually_mapped_logi = merged_data[column_name].isin(set(manually_mapped[column_name]))
    auto_mapped = merged_data.loc[~manually_mapped_logi, :].copy()

    auto_mapped['chemicals_chebi'] = auto_mapped['resistance'].apply(lambda x: fypo2chebi[x] if x in fypo2chebi else '')
    auto_mapped = auto_mapped.merge(dose_table, on=column_name, how='left')

    # Merge again
    merged_data = pandas.concat([auto_mapped, manually_mapped]).sort_values(by='original_index').drop(columns=['original_index'])

    # Default temperature
    merged_data.fillna('',inplace=True)
    merged_data.loc[merged_data['temperature'] == '', 'temperature'] = 32

    # Remove the "dose" and "temperature" placeholders

    merged_data['fyeco_terms'] = merged_data['fyeco_terms'].apply(lambda x : ','.join(i for i in x.split(',') if i not in ['temperature', 'dose']))

    if column_name == 'Condition_name_long':
        merged_data.drop(columns='Condition_name_long', inplace=True)
        merged_data.rename(columns={'Condition_short': 'condition'}, inplace=True)
        merged_data['expression'] = 'null'
    else:
        merged_data.rename(columns={column_name: 'condition'}, inplace=True)
        merged_data['expression'] = 'overexpression'

    all_data.append(merged_data)

pandas.concat(all_data).to_csv(f'results/full_mappings.tsv', sep='\t', index=False)