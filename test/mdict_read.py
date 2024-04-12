# -*- coding: utf-8 -*-

from mdict_converter import retrieve_data_by_keys

keys = ['red', 'blue', 'blues', "what"]
index_path = '/Users/tyuaner/Local/mdict/test/LDOCE5/index.csv'  # 替换为你的索引文件路径
key_value_dict = retrieve_data_by_keys(keys, index_path)
for key, values in key_value_dict.items():
    for value in values:
        print(key + '  :  ' + value)
