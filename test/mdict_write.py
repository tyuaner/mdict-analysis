# -*- coding: utf-8 -*-

from readmdict import MDX, MDD
from mdict_converter import write_indexed_data

mdx = MDX('/Users/tyuaner/Local/mdict/LDOCE5++ V 2-15.mdx')
items = mdx.items()
write_indexed_data(items, '/Users/tyuaner/Local/mdict/test/LDOCE5')
