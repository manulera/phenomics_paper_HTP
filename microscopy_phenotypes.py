import pandas

data = pandas.read_excel('data/elife-76000-supp2-v2.xlsx', sheet_name='microscopy', skiprows=4)
data = data.loc[data['sample_type.x'] == 'ncRNA',:].copy()
data['allele_type'] = 'deletion'
data['expression'] = 'null'
data['evidence'] = 'ECO:0001098'
data.rename(columns={
    'strain': 'systematic_id',
}, inplace=True)


binuc_logi_index = ~data['significance_score_percentage_bi-nucleated'].str.startswith('no')
cell_length_index = ~data['significance_score_bi-nucleated'].str.startswith('no')

binuc_data = data.loc[binuc_logi_index, :].copy()
lenght_data = data.loc[cell_length_index, :].copy()

binuc_data['condition'] = 'microscopy_binucleate'
lenght_data['condition'] = 'microscopy_length'

binuc_data.rename(columns={
    'FC_dif_%_percentage_bi-nucleated': 'score',
}, inplace=True)
binuc_data['better_than_wild_type'] = binuc_data['score'] > 0

lenght_data.rename(columns={
    'FC_dif_%_bi-nucleated': 'score',
}, inplace=True)
lenght_data['better_than_wild_type'] = lenght_data['score'] > 0

columns = ['condition', 'systematic_id', 'better_than_wild_type', 'score', 'allele_type', 'expression', 'evidence']

output_data = pandas.concat(f[columns] for f in [lenght_data, binuc_data])
output_data['score'] = output_data['score']/100.
output_data['score_units'] = 'fold_change'
output_data.to_csv('results/microscopy_intermediate_dataset.tsv', sep='\t', index=False)
