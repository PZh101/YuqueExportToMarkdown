import tarfile
import os


def untar_file(tar_file, extract_to):
    with tarfile.open(tar_file, 'r') as tar_ref:
        tar_ref.extractall(extract_to)


# 示例用法
tar_file = os.path.relpath('lakebook/学习笔记.lakebook', __file__)
extract_to = 'destination_folder'  # 要提取到的目录

# 确保提取目录存在
if not os.path.exists(extract_to):
    os.makedirs(extract_to)

# 解压文件
untar_file(tar_file, extract_to)
