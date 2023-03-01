import pandas

data = pandas.concat([
    pandas.read_csv('results/pombase_intermediate_dataset.tsv',delimiter='\t', na_filter=False),
    pandas.read_csv('results/microscopy_intermediate_dataset.tsv',delimiter='\t', na_filter=False),
])
data.drop(columns=['file', 'sheet_name'], inplace=True)
data = data[data.systematic_id != '972'].copy()

mappings = pandas.read_csv('results/full_mappings.tsv',delimiter='\t', na_filter=False)
mappings.drop(columns=['sensitive_label', 'resistance_label'], inplace=True)

merged_data = data.merge(mappings, on=['condition', 'expression'], how='left')

merged_data['fypo_id'] = ''
merged_data.loc[merged_data.better_than_wild_type, 'fypo_id'] = merged_data.loc[merged_data.better_than_wild_type, 'resistance']
merged_data.loc[~merged_data.better_than_wild_type, 'fypo_id'] = merged_data.loc[~merged_data.better_than_wild_type, 'sensitive']
merged_data.drop(columns=['sensitive','resistance',], inplace=True)

merged_data.to_csv('results/analysis_dataset.tsv', sep='\t', index=False, float_format='%.3f')

ncRNA_table = pandas.read_csv('results/ncRNA_table.tsv',delimiter='\t', na_filter=False)
ncRNA_table['expression'] = 'null'
ncRNA_table2 = ncRNA_table.copy()
ncRNA_table2['expression'] = 'overexpression'
ncRNA_table2['allele_variant'] = ''
ncRNA_table = pandas.concat([ncRNA_table, ncRNA_table2])
print(ncRNA_table)
logi = ncRNA_table.expression == 'overexpression'

def format_overexpression(r):
    chr = r['chromosome'] * 'I'
    coord = r['coordinates']
    return f'{chr}:{coord}'

ncRNA_table.loc[logi, 'allele_variant'] = ncRNA_table.loc[logi, :].apply(format_overexpression, axis=1)
# Set value for deletion alleles
merged_data = merged_data.merge(ncRNA_table[['systematic_id', 'expression', 'allele_variant']], on=['systematic_id', 'expression'], how='left')
# Set value for overexpression alleles

merged_data.drop(inplace=True, columns=[
    'condition',
    'better_than_wild_type',
])

merged_data.rename(inplace=True, columns={
    'systematic_id': 'Gene systematic ID',
    'allele_type': 'Allele type',
    'expression': 'Expression',
    'evidence': 'Evidence',
    'fyeco_terms': 'Condition',
    'fypo_id': 'FYPO ID',
    'severity': 'Severity',
    'allele_variant': 'Allele Variant'
})
merged_data['Allele description'] = merged_data['Allele type']
merged_data['Parental strain'] = '972 h-'
merged_data.loc[merged_data['Gene systematic ID'].str.startswith('SPNCRNA'), 'Parental strain'] = '972 h- or 968 h90'
merged_data['Background strain name'] = ''
merged_data['Background genotype description'] = ''
merged_data['Gene name'] = ''
merged_data['Allele name'] = ''
merged_data['Allele synonym'] = ''
merged_data['Penetrance'] = ''

merged_data['Extension'] = ''
merged_data['Reference'] = 'PMID:34984977'
merged_data['taxon'] = '4896'
merged_data['Date'] = '2023-02-23'
merged_data['Ploidy'] = 'haploid'
column_order = [
    'Gene systematic ID',
    'FYPO ID',
    'Allele description',
    'Expression',
    'Parental strain',
    'Background strain name',
    'Background genotype description',
    'Gene name',
    'Allele name',
    'Allele synonym',
    'Allele type',
    'Evidence',
    'Condition',
    'Penetrance',
    'Severity',
    'Extension',
    'Reference',
    'taxon',
    'Date',
    'Ploidy',
    'Allele Variant'
]

# Fix rows of missing systematic ids
allele_fixes = pandas.concat([
    pandas.read_csv('results/fixes_alleles.tsv', delimiter='\t', na_filter=False),
    pandas.read_csv('data/manual_fixes_alleles.tsv', delimiter='\t', na_filter=False)])

allele_fixes.rename(columns= {'systematic_id': 'Gene systematic ID'}, inplace=True)
allele_fixes['Expression'] = 'null'

merged_data = merged_data.merge(allele_fixes, on=['Gene systematic ID', 'Expression'], how='left')
merged_data.fillna('', inplace=True)
replacing_cols = ['Allele description', 'Allele synonym', 'Allele type']
for col in replacing_cols:
    merged_data[col] = merged_data.apply(lambda r: r[col+'_y'] if r[col+'_y'] else r[col+'_x'], axis=1)

merged_data.loc[merged_data.corresponding_systematic_id != '', 'Gene systematic ID'] = merged_data.corresponding_systematic_id[merged_data.corresponding_systematic_id != '']
merged_data.drop(columns='corresponding_systematic_id', inplace=True)

overexpressed_fragments = (merged_data['Expression'] == 'overexpression') & merged_data['Gene systematic ID'].isin(set(allele_fixes['Gene systematic ID']))
merged_data.loc[overexpressed_fragments, 'Allele type'] = 'other'
merged_data.loc[overexpressed_fragments, 'Allele synonym'] = merged_data.loc[overexpressed_fragments, 'Gene systematic ID'].apply(lambda x: f'{x}OE')

# Finally replace systematic ids by synonyms
missing_rnas = pandas.read_csv('results/ncRNA_table_missing.tsv', delimiter='\t', na_filter=False),
synonym_dict = dict()
for i, row in missing_rnas.iterrows():
    if row['current_synonym'] != '':
        synonym_dict[row['systematic_id']] = row['current_synonym']
synonym_dict['SPNCRNA.01'] = 'SPAC31G5.10'

# merged_data['systematic_id'] = 

merged_data = merged_data.loc[:,column_order]
merged_data.to_csv('results/pombase_dataset.tsv', sep='\t', index=False, float_format='%.3f')
