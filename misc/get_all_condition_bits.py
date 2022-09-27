"""
Get all the condition names from supp1 file.
Some are composed of several conditions, hence the splitting with _
"""

# %%

import pandas

data = pandas.read_excel('../data/elife-76000-supp1-v2.xlsx', sheet_name='knock-out_condition_metadata')

condition_bits = set()

for condition in data['Condition_name_long']:
    for c in condition.split('_'):
        condition_bits.add(c)

condition_bits = sorted(list(condition_bits))

for cb in condition_bits:
    print(cb)