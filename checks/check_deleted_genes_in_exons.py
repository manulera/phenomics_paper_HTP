import pandas

data_list = list()
for i in range(1,4):
    this_data = pandas.read_csv(f'../data/chromosome{i}.exon.coords', sep='\t', na_filter=False, names=['systematic_id', 'start', 'end', 'strand'])
    this_data['chromosome'] = i
    data_list.append(this_data)

exon_coordinates = pandas.concat(data_list)

gene_ids_data = pandas.read_csv('../data/gene_IDs_names.tsv',sep='\t',na_filter=False, names=['systematic_id', 'primary_name', 'synonyms'])

data_from_missing_ids = exon_coordinates[~exon_coordinates.systematic_id.isin(set(gene_ids_data.systematic_id))]

for i in data_from_missing_ids.systematic_id.values:
    print(i)