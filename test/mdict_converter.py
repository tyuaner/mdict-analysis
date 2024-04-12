# -*- coding: utf-8 -*-
import zlib
import csv
import os


def write_indexed_data(items, directory):
    """
    将键值对数据写入压缩文件和索引 CSV 文件。
    :param items: 包含 (key, value) 对的迭代器，value 应该是已编码的字符串。
    :param directory: 存储 index.csv 和 data.bin 文件的目录路径。
    """
    # 确保指定的目录存在，如果不存在，则创建它
    if not os.path.exists(directory):
        os.makedirs(directory)

    data_path = os.path.join(directory, 'data.bin')
    index_path = os.path.join(directory, 'index.csv')

    # 使用 'wb' 模式打开文件以确保兼容 Python 2.7 和 3.x
    with open(data_path, 'wb') as data_file, open(index_path, 'w') as index_file:
        # 创建 CSV 写入器，仅在需要时引用字段
        csv_writer = csv.writer(index_file, quoting=csv.QUOTE_MINIMAL)

        offset = 0  # 初始化偏移量
        for key, value in items:
            # 压缩值
            compressed_value = zlib.compress(value)
            data_file.write(compressed_value)
            length = len(compressed_value)

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
    directory = os.path.dirname(index_path)
    data_path = os.path.join(directory, 'data.bin')

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
            compressed_value = data_file.read(length)
            value = zlib.decompress(compressed_value).decode('utf-8')

            if key not in results:
                results[key] = [value]
            else:
                results[key].append(value)

    return results
