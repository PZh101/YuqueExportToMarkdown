import os

from typing import List

__FILE_SPILT_ = 7573746172003030
__FILE_SEPARATOR_ = [0x75, 0x73, 0x74, 0x61, 0x72, 0x00, 0x30, 0x30]
__EMPTY_ = 0x00
__HEAD_LEN_ = 512


def to_hex(n):
    return hex(n)


def get_file_name(head_info_byte):
    file_name_part_byte = head_info_byte[:100]
    file_name_byte = []
    for b in file_name_part_byte:
        if b == __EMPTY_:
            break
        else:
            file_name_byte.append(b)
    return bytes(file_name_byte).decode("utf-8")


def read_lake_book(book_path):
    file_name_array = []
    with open(book_path, 'rb+') as f:
        while True:
            head_info_byte = f.read(512)
            temp_bytes = []
            # 1 is name, 2,is content
            file_name = get_file_name(head_info_byte)
            mode_end = 100 + 6
            file_mode = head_info_byte[100:mode_end]

            while file_bytes and len(file_bytes) == 1:
                if file_bytes[0] == __EMPTY_:
                    file_name_array.append(str(file_bytes))
                temp_bytes.append(file_bytes[0])
                file_bytes = f.read(1)


if __name__ == '__main__':
    lake_book_path = os.path.relpath('lakebook/学习笔记.lakebook', __file__)
    extract_to = 'extracted'  # 要提取到的目录
    read_lake_book(lake_book_path)
