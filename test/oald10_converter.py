# -*- coding: utf-8 -*-
import csv
import os
import zlib

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
