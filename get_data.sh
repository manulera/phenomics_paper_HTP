curl -k https://www.pombase.org/data/names_and_identifiers/gene_IDs_names.tsv | tail -n+2 >> data/gene_IDs_names.tsv

curl -k https://www.pombase.org/data/genome_sequence_and_features/Exon_Coordinates/chromosome1.exon.coords --output data/chromosome1.exon.coords
curl -k https://www.pombase.org/data/genome_sequence_and_features/Exon_Coordinates/chromosome2.exon.coords --output data/chromosome2.exon.coords
curl -k https://www.pombase.org/data/genome_sequence_and_features/Exon_Coordinates/chromosome3.exon.coords --output data/chromosome3.exon.coords
