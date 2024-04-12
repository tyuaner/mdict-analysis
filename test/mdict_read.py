# -*- coding: utf-8 -*-

from mdict_converter import retrieve_data_by_keys

keys = ['\lpd006_a.png', '\lpd010_a.png']
index_path = '/Users/tyuaner/Local/mdict/LPD3byOeasy20130607_mdd_index.csv'  # 替换为你的索引文件路径
key_value_dict = retrieve_data_by_keys(keys, index_path)
for key, values in key_value_dict.items():
    for value in values:
        with open('/Users/tyuaner/Local/mdict/' + key, 'wb') as bin_file:
            bin_file.write(value)
