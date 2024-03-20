import os
import re


def remove_invalid_characters(filename):
    # 定义要移除的字符列表
    invalid_chars = r'[<>:"/\\|?*]'
    # 使用正则表达式替换不支持的字符为空字符串
    cleaned_filename = re.sub(invalid_chars, "", filename)
    return cleaned_filename


filename = "【读薄 CSAPP】壹 数据表示 | 小土刀 2.0"
filename = remove_invalid_characters(filename)
os.makedirs("F:\\tmp\\xxx\\最近计划\\深度理解计算机系统\\" + filename, exist_ok=True)
