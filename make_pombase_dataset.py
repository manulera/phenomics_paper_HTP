import pandas

data = pandas.read_csv('results/pombase_intermediate_dataset.tsv',delimiter='\t', na_filter=False)

mappings = pandas.read_csv('results/full_mappings.tsv',delimiter='\t', na_filter=False)

# Fix errors in mappings
{'YESphlox-Gluc0.5starionary7': 'YESphlox-Gluc0.5stationary7'}


mappings.drop(columns=['sensitive_label', 'resistance_label'], inplace=True)

merged_data = data.merge(mappings, on=['condition', 'expression'], how='left')

print(pandas.unique(merged_data.loc[pandas.isna(merged_data['temperature']),'condition']))
exit()
merged_data['temperature'] = merged_data['temperature'].astype(int)

merged_data.to_csv('results/pombase_dataset.tsv', sep='\t', index=False, float_format='%.3f')
