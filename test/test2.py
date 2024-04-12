# -*- coding: utf-8 -*-
import codecs
from readmdict import MDX, MDD
from pathvalidate import sanitize_filename
import os
import time

# from bs4 import BeautifulSoup


mdx = MDX('/Users/tyuaner/Local/mdict/LDOCE5++ V 2-15.mdx')
items = mdx.items()
base_path = '/Users/tyuaner/Local/mdict/test/LDOCE5/'
for key, value in items:
    if 'blue' == key.lower():
        filename = sanitize_filename(key)
        full_path = os.path.join(base_path, filename + '.html')

        # 检查文件是否存在，如果存在则添加序号
        counter = 1
        while os.path.exists(full_path):
            full_path = os.path.join(base_path, "{0}_{1}.html".format(filename, counter))
            counter += 1

        with codecs.open(full_path, 'w', 'utf-8') as f:
            f.write(value.decode('utf-8'))
