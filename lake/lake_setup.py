# -*- coding: utf-8 -*-
"""
@Time ： 2023年11月13日 13点41分
@Auth ： zhoup
@File ：lake_setup.py
"""
import json
import yaml
import os

from lake.lake_handle import MyParser, MyContext
from lake.failure_result_parser import parse_failure_result

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
downloadImage = True
root_path = ""


# from lxml import etree
def load_meta_json(meta_json):
    """
    解析meta.json中标注的文件关系
    :return:
    """
    full_path = "/".join([meta_json, "$meta.json"])
    fp = open(full_path, 'r+', encoding='utf-8')
    json_obj = json.load(fp)
    meta = json_obj['meta']
    # print(meta)
    meta_obj = json.loads(meta)
    book_Yml = meta_obj['book']['tocYml']
    # print(book_Yml)
    # with open('meta_book_yml.yaml', 'w+', encoding='utf-8') as yaml_fp:
    #     yaml_fp.write(book_Yml)
    #     yaml_fp.flush()
    books = yaml.load(book_Yml, yaml.Loader)
    for book in books:
        if book.get('uuid'):
            id_and_book[book['uuid']] = book
        if book['type'] == 'META':
            continue
        if book['parent_uuid'] == '':
            root_books.append(book)
            continue
        parent_uuid = book['parent_uuid']
        if parent_id_and_child.get(parent_uuid):
            parent_id_and_child[parent_uuid].append(book)
        else:
            parent_id_and_child[parent_uuid] = []
            parent_id_and_child[parent_uuid].append(book)
    # print(books)
    global file_total
    global total
    file_total = len(id_and_book)
    total = len(id_and_book)


def create_tree_dir(parent_path, book):
    """
    根据解析出的关系创建文档的目录树
    :param parent_path: 输出目录的根路径
    :param book: 当前book对象
    :return:
    """
    if book is None:
        return
    uuid = book['uuid']
    name = book['title']
    file_url = book['url']
    if not os.path.exists(parent_path):
        os.makedirs(parent_path)
    book_children = parent_id_and_child.get(uuid)
    global file_count
    global all_file_count
    global failure_image_download_list
    all_file_count += 1
    if file_url != '':
        ltm = LakeToMd("{}/{}.json".format(root_path, file_url), target="/".join([parent_path, name]))
        ltm.to_md()
        failure_image_download_list += ltm.image_download_failure
        file_count += 1
        # print("\r", end="")
        # i = (file_count // file_total) * 100
        print("\rprocess progress: {}/{}/{}: ".format(file_count, all_file_count, file_total), end="")
        # sys.stdout.flush()
        # time.sleep(0.05)
    if not book_children:
        return
    for child in book_children:
        seg = [x for x in parent_path.split("/")]
        seg.append(child['title'])
        create_tree_dir("/".join(seg), child)


class LakeToMd:
    body_html = None
    image_download_failure = []

    def __init__(self, filename, target):
        self.filename = filename
        self.target = target
        self.__body_html()

    def __body_html(self):
        fp = open(file=self.filename, mode='r+', encoding='utf-8')
        fileJson = json.load(fp)
        body_html = fileJson["doc"]['body_draft_asl']
        fp.close()
        self.body_html = body_html

    def to_md(self):
        mp = MyParser(self.body_html)
        name = self.target.split("/")[-1]
        lastIndex = self.target.rindex("/")
        shortTarget = self.target[:lastIndex]
        context = MyContext(filename=name, imageTarget=shortTarget, downloadImage=downloadImage)
        res = mp.handle_descent(mp.soup, context)
        self.image_download_failure += context.failure_images
        with open(self.target + ".md", 'w', encoding='utf-8') as fp:
            fp.writelines(res)
            fp.flush()


def convert_to_md(file_path):
    output_path = file_path
    for root_book in root_books:
        title = root_book['title']
        create_tree_dir("/".join([output_path, title]), root_book)
    print("转换完成")
    os.system("explorer " + output_path)


def start_convert(meta, output, downloadImageOfIn):
    global root_path
    root_path = meta
    load_meta_json(meta)
    global downloadImage
    downloadImage = downloadImageOfIn
    abspath = os.path.abspath(output)
    convert_to_md(abspath)
    print("共导出%s个文件" % file_count)

    print("图片下载错误列表:")
    print(failure_image_download_list)
    parse_failure_result(failure_image_download_list)

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
