mkdir -p data

# Paper data
curl -k https://cdn.elifesciences.org/articles/76000/elife-76000-supp1-v2.xlsx --output  data/elife-76000-supp1-v2.xlsx
curl -k https://cdn.elifesciences.org/articles/76000/elife-76000-supp2-v2.xlsx --output  data/elife-76000-supp2-v2.xlsx
curl -k https://cdn.elifesciences.org/articles/76000/elife-76000-supp3-v2.xlsx --output  data/elife-76000-supp3-v2.xlsx
curl -k https://cdn.elifesciences.org/articles/76000/elife-76000-supp4-v2.xlsx --output  data/elife-76000-supp4-v2.xlsx
curl -k https://cdn.elifesciences.org/articles/76000/elife-76000-supp5-v2.xlsx --output  data/elife-76000-supp5-v2.xlsx
curl -k https://cdn.elifesciences.org/articles/76000/elife-76000-supp6-v2.xlsx --output  data/elife-76000-supp6-v2.xlsx

# Other
curl -k https://raw.githubusercontent.com/pombase/fypo/master/fyeco.obo --output data/fyeco.obo
curl -L https://raw.githubusercontent.com/pombase/fypo/master/src/ontology/fypo-edit.owl --output data/fypo-edit.owl