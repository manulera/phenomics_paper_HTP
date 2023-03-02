import pandas
import re

def make_synonym_dict(data):
    synonyms = dict()
    for i,row in data.iterrows():
        for synonym in [row['primary_name']] + row['synonyms'].split(','):
            if len(synonym):
                if synonym in synonyms:
                    synonyms[synonym].append(row['systematic_id'])
                    # Ensure unique
                    synonyms[synonym] = list(set(synonyms[synonym]))
                else:
                    synonyms[synonym] = [row['systematic_id']]

    return synonyms

data = pandas.read_excel('data/elife-76000-supp1-v2.xlsx', sheet_name='lincRNA_metadata')
def formatting_function(r):
    start = r['start']
    end = r['end']
    strand = r['strand']
    if strand == '+' or strand == 1:
        return f'{start}..{end}'
    else:
        return f'complement({start}..{end})'

data['coordinates'] = data.apply(formatting_function, axis=1)

def format_deletion(r):
    start = r['start']
    end = r['end']
    chr = r['chr'] * 'I'
    return f'{chr}:g.{start}_{end}del'

data['allele_variant'] = data.apply(format_deletion, axis=1)

data.rename(inplace=True, columns={
    'chr': 'chromosome',
    'gene': 'systematic_id',

})

# Missing one
data.loc[data.index[-1], 'systematic_id'] = 'SPNCRNA.5041'
# Keep only relevant columns
data = data.loc[:, ['systematic_id', 'chromosome', 'coordinates', 'allele_variant', 'h90']].copy()
data['h90'] = data['h90'].astype(bool)
# Load synonym dict
gene_ids_data = pandas.read_csv('data/gene_IDs_names.tsv',sep='\t',na_filter=False, names=['systematic_id', 'primary_name', 'synonyms'])
synonym_dict = make_synonym_dict(gene_ids_data)

# Create column with current synonyms
data['systematic_id_missing'] = ~data.systematic_id.isin(gene_ids_data['systematic_id'])
data['current_synonym'] = ''
data.loc[data['systematic_id_missing'], 'current_synonym'] = data.loc[data['systematic_id_missing'], 'systematic_id'].apply(lambda x: synonym_dict[x][0] if x in synonym_dict else '')
data.loc[data['systematic_id_missing'], 'synonym_already_present'] = data.loc[data['systematic_id_missing'], 'current_synonym'].isin(set(data['systematic_id']))

# Load coordinates of current features
data_list = list()
for i in range(1,4):
    this_data = pandas.read_csv(f'data/chromosome{i}.exon.coords', sep='\t', na_filter=False, names=['systematic_id', 'start', 'end', 'strand'])
    this_data['chromosome'] = i
    data_list.append(this_data)
current_coordinates = pandas.concat(data_list)
# There are some with several exons, so keep only min and max values
current_coordinates = current_coordinates.groupby(['systematic_id', 'chromosome', 'strand'], as_index=False).agg({'start': lambda x: min(x.values), 'end': lambda x: max(x.values)})

current_coordinates = current_coordinates[current_coordinates.systematic_id.str.startswith('SPNCRNA')].copy()
current_coordinates['current_coordinates'] = current_coordinates.apply(formatting_function, axis=1)




data = data.merge(current_coordinates[['systematic_id', 'current_coordinates']], on='systematic_id', how='left')
# Merge the synonyms
current_coordinates.rename(columns={'current_coordinates': 'synonym_coordinates', 'systematic_id': 'current_synonym'}, inplace=True)
data = data.merge(current_coordinates[['current_synonym', 'synonym_coordinates']], on='current_synonym', how='left')

data.loc[data.current_coordinates==data.coordinates, 'current_coordinates'] = ''
data.loc[data.synonym_coordinates==data.coordinates, 'synonym_coordinates'] = ''

output_data = data[['systematic_id', 'systematic_id_missing', 'current_synonym', 'synonym_already_present', 'chromosome', 'coordinates', 'current_coordinates', 'synonym_coordinates', 'allele_variant', 'h90']]
output_data.fillna('', inplace=True)

missing_ids = output_data.systematic_id_missing == True
synonym_doesnt_match = missing_ids & (output_data.synonym_coordinates != '')
changed_coordinates = output_data.current_coordinates != ''

output_data[missing_ids].to_csv('results/ncRNA_table_missing.tsv', sep='\t', index=False)
output_data[changed_coordinates].to_csv('results/ncRNA_table_differing_coordinates.tsv', sep='\t', index=False)
output_data.to_csv('results/ncRNA_table.tsv', sep='\t', index=False)

fixed_synonyms = output_data[synonym_doesnt_match].copy()
fixed_coordinates = output_data[changed_coordinates].copy()
def get_coords(input_str):
    match = re.search(r'(\d+)\.\.(\d+)', input_str)
    start, end = match.groups()
    strand = -1 if 'complement' in input_str else 1
    return int(start), int(end), strand

def format_number(num):
    if int(num)>0:
        return str(num)
    else:
        return f'({num})'

def format_allele_description(r, current_column, study_column):
    start_current, end_current, strand_current = get_coords(r[current_column])
    start_study, end_study, strand_study = get_coords(r[study_column])
    if strand_study == 1:
        return format_number(start_study-start_current) + '-' + format_number(end_study-start_current)
    else:
        return format_number(end_current-end_study) + '-' + format_number(end_current-start_study)


fixed_synonyms['Allele description'] = fixed_synonyms.apply(format_allele_description, axis=1, args=['synonym_coordinates', 'coordinates'])
fixed_synonyms.rename(columns={'current_synonym': 'corresponding_systematic_id'}, inplace=True)
fixed_synonyms['Allele synonym'] = fixed_synonyms['systematic_id'].apply(lambda x : x + 'delta')

fixed_coordinates['Allele description'] = fixed_coordinates.apply(format_allele_description, axis=1, args=['current_coordinates', 'coordinates'])
fixed_coordinates['corresponding_systematic_id'] = fixed_coordinates['systematic_id']
fixed_coordinates['Allele synonym'] = ''

columns2keep = ['systematic_id', 'corresponding_systematic_id', 'Allele description', 'Allele synonym', 'Allele type']

fixed = pandas.concat([fixed_coordinates, fixed_synonyms])
fixed['Allele type'] = 'partial_nucleotide_deletion'
fixed[columns2keep].to_csv('results/fixes_alleles.tsv', sep='\t', index=False)
