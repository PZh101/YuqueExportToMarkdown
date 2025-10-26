# -*- coding: utf-8 -*-
"""
@Time ： 2023年11月13日 13点41分
@Auth ： zhoup
@File ：lake_setup.py
"""
import json

import yaml
import os
import shutil
from lake.lake_handle import MyParser, MyContext, remove_invalid_characters
from lake.lake_reader import unpack_lake_book_file
from lake.failure_result_parser import parse_failure_result


class GlobalContext:
    # parent_id和book
    parent_id_and_child: dict = {}
    # 将id和book映射起来
    id_and_book = {}
    # 存放根目录的book
    root_books = []
    file_count = 0
    all_file_count = 0
    failure_image_download_list = []
    file_total = 0
    total = 0
    download_image = True
    root_path = ""


# from lxml import etree
def load_meta_json(global_context: GlobalContext):
    """
    解析meta.json中标注的文件关系
    :return:
    """
    full_path = "/".join([global_context.root_path, "$meta.json"])
    fp = open(full_path, 'r+', encoding='utf-8')
    json_obj = json.load(fp)
    meta = json_obj['meta']
    # print(meta)
    meta_obj = json.loads(meta)
    book_yml = meta_obj['book']['tocYml']
    # print(book_yml)
    # with open('meta_book_yml.yaml', 'w+', encoding='utf-8') as yaml_fp:
    #     yaml_fp.write(book_yml)
    #     yaml_fp.flush()
    books = yaml.load(book_yml, yaml.Loader)
    for book in books:
        if book.get('uuid'):
            global_context.id_and_book[book['uuid']] = book
        if book['type'] == 'META':
            continue
        if book['parent_uuid'] == '':
            global_context.root_books.append(book)
            continue
        parent_uuid = book['parent_uuid']
        if global_context.parent_id_and_child.get(parent_uuid):
            global_context.parent_id_and_child[parent_uuid].append(book)
        else:
            global_context.parent_id_and_child[parent_uuid] = []
            global_context.parent_id_and_child[parent_uuid].append(book)
    # print(books)
    global_context.file_total = len(global_context.id_and_book)
    global_context.total = len(global_context.id_and_book)


def create_tree_dir(global_context, parent_path, book):
    """
    根据解析出的关系创建文档的目录树
    :param parent_path: 输出目录的根路径
    :param book: 当前book对象
    :param global_context 上下文
    :return:
    """
    if book is None:
        return
    uuid = book['uuid']
    name = book['title']
    file_url = book['url']
    if not os.path.exists(parent_path):
        parent_path = parent_path.replace("/", os.path.sep)
        parent_path = remove_invalid_characters(parent_path)
        os.makedirs(parent_path, exist_ok=True)
    book_children = global_context.parent_id_and_child.get(uuid)
    global_context.all_file_count += 1
    if file_url != '':
        ltm = LakeToMd("{}/{}.json".format(global_context.root_path, file_url), target="/".join([parent_path, name]))
        ltm.to_md(global_context)
        global_context.failure_image_download_list += ltm.image_download_failure
        global_context.file_count += 1
        # print("\r", end="")
        # i = (file_count // file_total) * 100
        print("\rprocess progress: {}/{}/{}. ".format(global_context.file_count, global_context.all_file_count,
                                                      global_context.file_total), end="")
        # sys.stdout.flush()
        # time.sleep(0.05)
    if not book_children:
        return
    for child in book_children:
        seg = [x for x in parent_path.split("/")]
        seg.append(child['title'])
        create_tree_dir(global_context, "/".join(seg), child)


class LakeToMd:
    body_html = None
    image_download_failure = []

    def __init__(self, filename, target):
        self.filename = filename
        self.target = target
        self.__body_html()

    def __body_html(self):
        fp = open(file=self.filename, mode='r+', encoding='utf-8')
        file_json = json.load(fp)
        body_html = file_json["doc"]['body_draft_asl']
        fp.close()
        self.body_html = body_html

    def to_md(self, global_context):
        mp = MyParser(self.body_html)
        name = self.target.split("/")[-1]
        last_index = self.target.rindex("/")
        short_target = self.target[:last_index]
        context = MyContext(filename=name, image_target=short_target, download_image=global_context.download_image)
        res = mp.handle_descent(mp.soup, context)
        self.image_download_failure += context.failure_images
        self.target = remove_invalid_characters(self.target)
        md_path = self.target.replace("/", os.path.sep)
        with open(md_path + ".md", 'w+', encoding='utf-8') as fp:
            fp.writelines(res)
            fp.flush()


def convert_to_md(global_context, file_path):
    output_path = file_path
    for root_book in global_context.root_books:
        title = root_book['title']
        create_tree_dir(global_context, "/".join([output_path, title]), root_book)
    print(">>> markdown 转换完成")
    # 根据操作系统选择合适的命令打开文件夹
    import platform
    system = platform.system()
    if system == 'Windows':
        os.system("explorer " + output_path)
    elif system == 'Darwin':  # macOS
        os.system("open " + output_path)
    elif system == 'Linux':
        os.system("xdg-open " + output_path)
    else:
        print("未识别的操作系统，无法自动打开输出文件夹")


def start_convert(meta, lake_book, output, download_image_of_in):
    global_context = GlobalContext()
    temp_dir = "temp"
    if lake_book:
        global_context.root_path = unpack_lake_book_file(lake_book, temp_dir)
        print(">>> lake文件抽取完成")
    else:
        global_context.root_path = meta
    if not global_context.root_path:
        print("参数校验失败！-i或者-l二者必须有一个")
        return
    try:
        load_meta_json(global_context)
        print(">>> meta json解析完成")
        global_context.download_image = download_image_of_in
        abspath = os.path.abspath(output)
        print(">>> 开始进行markdown转换")
        convert_to_md(global_context, abspath)
        print("共导出%s个文件" % global_context.file_count)

        print("图片下载错误列表:")
        print(' list: ',global_context.failure_image_download_list)
        parse_failure_result(global_context.failure_image_download_list)
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
    except Exception as e:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        print(e)
# """
# 已经完成到根据meta生成目录了
# """
# if __name__ == '__main__':
#     load_meta_json('data/$.meta.json')
#     file_total = len(id_and_book)
#     total = len(id_and_book)
#     abspath = os.path.abspath("test")
#     convert_to_md(abspath)
#     print("共导出%s个文件" % file_count)
#
#     print("图片下载错误列表:")
#     print(failure_image_download_list)
#     parse_failure_result(failure_image_download_list)
