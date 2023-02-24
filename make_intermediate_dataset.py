import pandas
import re
# We create a dictionary to map the integer in 'RNA_gene' column to the systematic id

lincRNA_metadata = pandas.read_excel('data/elife-76000-supp1-v2.xlsx', sheet_name='lincRNA_metadata')
ncRNA_dict = dict()
for gene in lincRNA_metadata.gene:
    if not pandas.isna(gene):
        nb = int(gene.split('.')[1])
        ncRNA_dict[nb] = gene

# missing mapping
ncRNA_dict[5041] = 'SPNCRNA.5041'

# Settings:
settings = [
    ('data/elife-76000-supp2-v2.xlsx','RNA_gene', 'condition_short', True, 'deletion', 'null'),
    ('data/elife-76000-supp4-v2.xlsx','strain_id', 'condition_short', False, 'deletion', 'null'),
    ('data/elife-76000-supp6-v2.xlsx','strain_id', 'condition_timepoint', True, 'wild type', 'overexpression')
]


sheet_names = ['growth_benign', 'viability_benign', 'growth_stresses', 'viability_stresses']

all_data = list()

for data_file, gene_column, condition_column, is_rna, allele_type, expression in settings:

    for sheet_name in sheet_names:
        try:
            data = pandas.read_excel(data_file, sheet_name=sheet_name)
        except ValueError:
            # Skip sheet names that don't exist
            continue

        data = data.loc[data['is_hit'], :].copy()
        # Rename inconsistent columns
        if 'RNA-gene' in data:
            data.rename(columns={'RNA-gene': 'RNA_gene'}, inplace=True)

        if condition_column == 'condition_timepoint':
            data = data.loc[~data[gene_column].str.contains('evc'),:].copy()
            data[condition_column] = data[condition_column].apply(lambda x: re.sub(r'-\d+h$','',x))
        if gene_column == 'RNA_gene':
            data[gene_column] = data[gene_column].astype(int)
            data['systematic_id'] = data[gene_column].apply(lambda x: ncRNA_dict[x])
        else:
            data['systematic_id'] = data[gene_column]

        data['better_than_wild_type'] = data['median_fitness_log2'] > 0
        data = data.loc[:,[condition_column, 'systematic_id', 'better_than_wild_type', 'median_fitness_log2']]
        data['allele_type'] = allele_type
        data['expression'] = expression
        data['evidence'] = 'ECO:0001563' if 'growth' in sheet_name else 'ECO:0005004'

        data.rename(columns={condition_column: 'condition', 'median_fitness_log2': 'score'}, inplace=True)
        all_data.append(data)
out_data = pandas.concat(all_data)
out_data['score_units'] = 'median_fitness_log2'
out_data.to_csv('results/pombase_intermediate_dataset.tsv', index=False, sep='\t')