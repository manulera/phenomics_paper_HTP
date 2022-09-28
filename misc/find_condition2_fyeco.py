"""
Find the words in condition_bits in fyeco.obo
"""

import os

with open('condition2.txt') as ins:
    for line in ins:
        cond = line.strip()
        if cond[0].isnumeric():
            continue
        print(f'## {cond}')
        print('```')
        print(os.popen(f'grep -i -B 8 -A 4 "{cond}" ../data/fyeco.obo').read())
        print('```')
        print()
        print()
