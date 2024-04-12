# -*- coding: utf-8 -*-
import codecs
from readmdict import MDX, MDD
from pathvalidate import sanitize_filename
import os
import time

# from bs4 import BeautifulSoup


mdx = MDX('/Users/tyuaner/Local/mdict/LDOCE5++ V 2-15.mdx')
items = mdx.items()
base_path = '/Users/tyuaner/Local/mdict/test/lpd3/'
start_time = time.time()
for key, value in items:
    pass
end_time = time.time()  # 获取结束时间
print("执行时间: {} 秒".format(end_time - start_time))
mdd = MDD('/Users/tyuaner/Local/mdict/LDOCE5++ V 2-15.mdd')
mdd_items = mdd.items()
start_time = time.time()
for key, value in mdd_items:
    pass
end_time = time.time()
print("执行时间: {} 秒".format(end_time - start_time))# 获取结束时间
# for key, value in items:
#     if 'red' == key.lower():
#         filename = sanitize_filename(key)
#         full_path = os.path.join(base_path, filename + '.html')
#
#         # 检查文件是否存在，如果存在则添加序号
#         counter = 1
#         while os.path.exists(full_path):
#             full_path = os.path.join(base_path, "{0}_{1}.html".format(filename, counter))
#             counter += 1
#
#         with codecs.open(full_path, 'w', 'utf-8') as f:
#             f.write(value.decode('utf-8'))

# mdd = MDD('/Users/tyuaner/Local/mdict/LDOCE5++ V 2-15.mdd')
# mdd_items = mdd.items()
# for i in range(20):
#     print next(mdd_items)
