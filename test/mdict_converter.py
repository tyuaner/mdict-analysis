# -*- coding: utf-8 -*-
import zlib
import csv
import os
import re
from readmdict import MDX, MDD


def generate_indexed_data(mdict_path):
    """
     将词典文件转换为索引文件和数据文件。索引文件使用 CSV 格式，数据文件使用二进制格式。
     索引文件包含词典中的每个键的元数据，包括键、偏移量和长度。数据文件包含词典中的每个词条内容。
     词条文本使用zlib压缩，音频数据不压缩。
    :param mdict_path: mdx或者mdd词典文件路径
    :return: None
    """
    base_name, extension = os.path.splitext(mdict_path)
    if extension.lower() not in ('.mdx', '.mdd'):
        raise ValueError('Invalid file extension: %s' % extension)
    mdict = MDX(mdict_path) if extension.lower() == '.mdx' else MDD(mdict_path)
    items = mdict.items()
    data_path = '{}_{}_data.bin'.format(base_name, extension.lstrip('.'))
    index_path = '{}_{}_index.csv'.format(base_name, extension.lstrip('.'))

    # 使用 'wb' 模式打开文件以确保兼容 Python 2.7 和 3.x
    with open(data_path, 'wb') as data_file, open(index_path, 'w') as index_file:
        # 创建 CSV 写入器，仅在需要时引用字段
        csv_writer = csv.writer(index_file, quoting=csv.QUOTE_MINIMAL)

        offset = 0  # 初始化偏移量
        for key, value in items:
            # 压缩值
            mdict_value = zlib.compress(value) if extension.lower() == '.mdx' else value
            data_file.write(mdict_value)
            length = len(mdict_value)

            # 写入索引文件：key, 偏移量, 长度
            csv_writer.writerow([key, offset, length])

            # 更新偏移量
            offset += length


def retrieve_data_by_keys(keys, index_path):
    """
    根据提供的键列表从索引文件和数据文件中检索对应的数据，并处理重复键。
    :param keys: 需要检索的键列表。
    :param index_path: 索引文件的路径。
    :return: 字典，键为索引中的键，值为一个列表，包含所有对应的值。
    """
    # 确定数据文件的路径
    data_path = index_path.replace("_index.csv", "_data.bin")

    # 读取索引文件
    index_data = []
    with open(index_path, 'r') as idx_file:
        csv_reader = csv.reader(idx_file)
        for row in csv_reader:
            if row[0] in keys:
                index_data.append((row[0], int(row[1]), int(row[2])))  # (key, offset, length)

    # 按照索引中的 offset 进行排序
    index_data.sort(key=lambda x: x[1])

    # 读取数据文件并提取值
    results = {}
    with open(data_path, 'rb') as data_file:
        for item in index_data:
            key, offset, length = item
            data_file.seek(offset)
            mdict_value = data_file.read(length)
            value = zlib.decompress(mdict_value).decode('utf-8') if re.search(r'_mdx_', data_path) else mdict_value

            if key not in results:
                results[key] = [value]
            else:
                results[key].append(value)

    return results
