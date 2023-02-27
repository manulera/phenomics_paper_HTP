import pandas

data = pandas.concat([
    pandas.read_csv('results/pombase_intermediate_dataset.tsv',delimiter='\t', na_filter=False),
    pandas.read_csv('results/microscopy_intermediate_dataset.tsv',delimiter='\t', na_filter=False),
])
data.drop(columns=['file', 'sheet_name'], inplace=True)
data = data[data.systematic_id != '972'].copy()


mappings = pandas.read_csv('results/full_mappings.tsv',delimiter='\t', na_filter=False)

# Add UV to the mappings
mappings.loc[mappings['condition'].str.contains('YES-UV'), 'chemical_or_agent'] = 'UV'


mappings.drop(columns=['sensitive_label', 'resistance_label'], inplace=True)

merged_data = data.merge(mappings, on=['condition', 'expression'], how='left')

merged_data['temperature'] = merged_data['temperature'].astype(int)

merged_data['fypo_id'] = ''
merged_data.loc[merged_data.better_than_wild_type, 'fypo_id'] = merged_data.loc[merged_data.better_than_wild_type, 'resistance']
merged_data.loc[~merged_data.better_than_wild_type, 'fypo_id'] = merged_data.loc[~merged_data.better_than_wild_type, 'sensitive']
merged_data.drop(columns=['sensitive','resistance',], inplace=True)

merged_data.to_csv('results/analysis_dataset.tsv', sep='\t', index=False, float_format='%.3f')

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
    'temperature': 'Temperature',
    'chemical_or_agent': 'Chemical or agent',
    'condition_dose': 'Chemical or agent dose',
    'score': 'Phenotype score',
    'score_units': 'Phenotype score units'
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
merged_data['Severity'] = ''
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
    'Temperature',
    'Chemical or agent',
    'Chemical or agent dose',
    'Phenotype score',
    'Phenotype score units'
]

merged_data = merged_data.loc[:,column_order]
merged_data.to_csv('results/pombase_dataset.tsv', sep='\t', index=False, float_format='%.3f')
