# -*- coding: utf-8 -*-
"""
@Time ： 2023年11月13日 13点41分
@Auth ： zhoup
@File ：lake_handle.py
"""
from bs4 import BeautifulSoup, NavigableString, Tag
import json
from urllib import parse
import urllib
import queue
import os
import requests
import time
import re

html_text = """
<div>
    <h1>标题1</h1>
    <div>
        <h2>标题2</h2>
        <p>这是什么文档</p>
    </div>
</div>
"""


def remove_invalid_characters(filename):
    p = r"^[a-zA-Z]:"
    prefix = ""
    h = re.match(p, filename)
    if h:
        regs = h.regs
        prefix = filename[regs[0][0]:regs[0][1]]
        filename = filename.replace(prefix, "")
    # 定义要移除的字符列表
    invalid_chars = r'[<>:"|?*]'
    # 使用正则表达式替换不支持的字符为空字符串
    cleaned_filename = re.sub(invalid_chars, "", filename)
    return prefix + cleaned_filename


class MyContext:
    def __init__(self, filename="xxx", download_image=True, image_target="", skip_existing=False):
        self.template_queue = queue.Queue()
        self.result = ""
        # 存放图片的目录
        self.filename = filename + ".assert"
        self.image_target = image_target
        # 下载失败的图片
        self.failure_images = []
        # 下载图片
        self.download_image = download_image
        # 是否跳过本地已存在的图片文件
        self.skip_existing = skip_existing

    def append_failure(self, name, image_src):
        r = "[{}]{}".format(name, image_src)
        self.failure_images.append(r)

    def find_file_path(self, file_uid):
        return file_uid


def eventual_tag(tag: Tag) -> bool:
    return len(tag.contents) == 0 or (len(tag.contents) == 1 and isinstance(tag.contents[0], NavigableString))


class MyParser:
    def __init__(self, htmlText):
        self.soup = BeautifulSoup(htmlText, 'html.parser')
        self.tagQueue = queue.Queue()

    def traverse(self, tag: Tag, deep: int):
        if isinstance(tag, NavigableString):
            return
        self.handle_tag(tag, deep)
        for _tag in tag.contents:
            _tag: Tag = _tag
            if isinstance(_tag, NavigableString):
                # print(_tag)
                continue
            self.traverse(_tag, deep + 1)

    def handle_tag(self, tag1: Tag, deep: int):
        prefix = " " * deep
        print(prefix + tag1.name)
        self.tagQueue.put(tag1)

    def handle_descent(self, tag: Tag, context1: MyContext) -> str:
        tag_name = tag.name
        if tag_name == 'span':
            return self.handle_span(tag, context1)
        elif tag_name == 'p':
            return self.handle_p(tag, context1)
        elif tag_name == 'h1':
            return self.handle_title(tag, 1, context1)
        elif tag_name == 'h2':
            return self.handle_title(tag, 2, context1)
        elif tag_name == 'h3':
            return self.handle_title(tag, 3, context1)
        elif tag_name == 'h4':
            return self.handle_title(tag, 4, context1)
        elif tag_name == 'h5':
            return self.handle_title(tag, 5, context1)
        elif tag_name == 'h6':
            return self.handle_title(tag, 6, context1)
        elif tag_name == 'h7':
            return self.handle_title(tag, 7, context1)
        elif tag_name == 'blockquote':
            return self.handle_blockquote(tag, context1)
        elif tag_name == 'card':
            return self.handle_card(tag, context1)
        elif tag_name == 'strong':
            return self.handle_strong(tag, context1)
        elif tag_name == 'em':
            return self.handle_em(tag, context1)
        elif tag_name == 'del':
            return self.handle_del(tag, context1)
        elif tag_name == 'u':
            return self.handle_u(tag, context1)
        elif tag_name == 'sup':
            return self.handle_sup(tag, context1)
        elif tag_name == 'sub':
            return self.handle_sub(tag, context1)
        elif tag_name == 'code':
            return self.handle_code(tag, context1)
        elif tag_name == 'ul':
            return self.handle_ul(tag, context1)
        elif tag_name == 'ol':
            return self.handle_ol(tag, context1)
        elif tag_name == 'a':
            return self.handle_a(tag, context1)
        elif tag_name == 'table':
            return self.handle_table(tag, context1)
        else:
            # print("meet the tag name : " + tag_name)
            return self.handle_common(context1, tag)

    def handle_title(self, tag: Tag, level: int, context1: MyContext):
        prefix = "#" * level
        prefix = prefix + " {}\n"
        if eventual_tag(tag):
            if len(tag) == 0:
                return prefix.format("")
            return prefix.format(tag.text)
        else:
            r = self.handle_common(context1, tag)
            return prefix.format(r)

    def handle_blockquote(self, tag: Tag, context1: MyContext):
        template = "> {}\n"
        if eventual_tag(tag):
            if len(tag) == 0:
                return template.format("")
            return template.format(tag.text)
        else:
            r = self.handle_common(context1, tag)
            return template.format(r)

    def handle_card(self, tag: Tag, context1: MyContext):
        name = tag.attrs.get("name")
        value = tag.attrs.get("value")
        value = value[5:]
        data = urllib.parse.unquote(value, encoding='utf-8')
        data_json = json.loads(data)
        if name == 'codeblock':
            mode = data_json.get('mode')
            code = data_json.get('code')
            card_name = data_json.get('name')
            if not mode:
                mode = 'plain'
            if not card_name:
                card_name = ''
            f_res = "{0}\n```{1}\n{2}\n```\n".format(card_name, mode, code)
            return f_res
        elif name == 'image':
            card_name = data_json.get('name')
            card_name, relative_image_path = self.download_resource(context1, data_json, card_name)
            return "![{}]({})\n".format(card_name, "./" + relative_image_path)
        elif name == 'hr':
            return "\n---\n"
        elif name == 'label':
            return data_json['label']
        elif name == 'math':
            la_tex = data_json['code']
            card_name, relative_image_path = self.download_resource(context1, data_json, '数学公式')
            return la_tex + '\n' + "![{}]({})\n".format(card_name, "./" + relative_image_path)
        elif name == 'file':
            card_name = data_json.get('name')
            card_name, relative_image_path = self.download_resource(context1, data_json, card_name)
            return "![{}]({})\n".format(card_name, "./" + relative_image_path)
        elif name == 'yuque':
            src = data_json.get('src')
            file_uid = src.split("/")[-1]
            title = data_json.get("detail").get("title")
            path = context1.find_file_path(file_uid)
            return "[{}]({})".format(title, path)

        else:
            return "\n"

    def download_resource(self, context1, data_json, name):
        """
        下载图片
        :param context1:
        :param data_json:
        :param name:
        :return:
        """
        src = data_json['src']
        resource_name = src.split("/")[-1]
        full_image_name = "/".join([context1.image_target, context1.filename, resource_name])
        full_image_path = "/".join([context1.image_target, context1.filename])
        relative_image_path = "/".join([context1.filename, resource_name])
        if not name:
            name = full_image_name
        if context1.filename != '':
            if not os.path.exists(full_image_path):
                full_image_path = remove_invalid_characters(full_image_path)
                os.makedirs(full_image_path, exist_ok=True)
            try:
                if context1.download_image:
                    full_image_name = remove_invalid_characters(full_image_name)
                    # 检查文件是否已存在，如果存在且设置了跳过则跳过下载
                    if context1.skip_existing and os.path.exists(full_image_name):
                        print(f"图片已存在，跳过下载: {resource_name}")
                        return name, relative_image_path

                    time.sleep(0.5)
                    resp = requests.get(src)
                    if resp.status_code != 200:
                        raise Exception("失败链接：{},响应码:{}".format(src, resp.status_code))
                    with open(full_image_name, 'wb') as imageFp:
                        imageFp.write(resp.content)
                        imageFp.flush()
            except Exception as ex:
                # ex.with_traceback()
                context1.append_failure(name, src)
                print("附件 {0} 下载失败".format(src))
                name = "附件下载失败"
        return name, relative_image_path

    def handle_span(self, tag, context1: MyContext):
        if eventual_tag(tag):
            if len(tag) == 0:
                return ""
            return tag.text
        else:
            return self.handle_common(context1, tag)

    def handle_p(self, tag, context1: MyContext):
        if eventual_tag(tag):
            if len(tag) == 0:
                return "\n"
            return tag.text + "\n"
        else:
            return self.handle_common(context1, tag) + "\n"

    def handle_common(self, context1, tag):
        temp_str = ""
        for _tag in tag.contents:
            if isinstance(_tag, NavigableString):
                if tag.name == '[document]':
                    continue
                temp_str = temp_str + _tag
                continue
            temp_str += self.handle_descent(_tag, context1)
        return temp_str

    def handle_strong(self, tag, context1: MyContext):
        template = "**{}**"
        if eventual_tag(tag):
            if len(tag) == 0:
                return template.format("")
            return template.format(tag.text)
        else:
            r = self.handle_common(context1, tag)
            return template.format(r)

    def handle_em(self, tag, context1: MyContext):
        # 斜体字
        template = "*{}*"
        if eventual_tag(tag):
            if len(tag) == 0:
                return template.format("")
            return template.format(tag.text)
        else:
            r = self.handle_common(context1, tag)
            return template.format(r)

    def handle_del(self, tag, context1: MyContext):

        """
        删除字
        :param context1:
        :param tag:
        :return:
        """
        template = "~~{}~~"
        if eventual_tag(tag):
            if len(tag) == 0:
                return template.format("")
            return template.format(tag.text)
        else:
            r = self.handle_common(context1, tag)
            return template.format(r)

    def handle_u(self, tag, context1: MyContext):
        """
        下划线
        :param context1:
        :param tag:
        :return:
        """
        template = "<u>{}</u>"
        if eventual_tag(tag):
            if len(tag) == 0:
                return template.format("")
            return template.format(tag.text)
        else:
            r = self.handle_common(context1, tag)
            return template.format(r)

    def handle_sup(self, tag, context1: MyContext):
        """
        上标
        :param context1:
        :param tag:
        :return:
        """
        template = "^{}"
        if eventual_tag(tag):
            if len(tag) == 0:
                return template.format("")
            return template.format(tag.text)
        else:
            r = self.handle_common(context1, tag)
            return template.format(r)

    def handle_sub(self, tag, context1: MyContext):
        """
        下标
        :param context1:
        :param tag:
        :return:
        """
        template = "~{}"
        if eventual_tag(tag):
            if len(tag) == 0:
                return template.format("")
            return template.format(tag.text)
        else:
            r = self.handle_common(context1, tag)
            return template.format(r)

    def handle_code(self, tag, context1: MyContext):
        """
        将ne-code转换为markdown行内代码格式
        :param context1:
        :param tag:
        :return:
        """
        template = "`{}`"
        if eventual_tag(tag):
            if len(tag) == 0:
                return template.format("")
            return template.format(tag.text)
        else:
            r = self.handle_common(context1, tag)
            return template.format(r)

    def handle_ul(self, tag, context1: MyContext):
        """
        无序列表
        :param context1:
        :param tag:
        :return:
        """
        template = "- {}\n"
        if eventual_tag(tag):
            if len(tag) == 0:
                return template.format("")
            return template.format(tag.text)
        else:
            tempStr = ""
            for _tag in tag.contents:
                if isinstance(_tag, NavigableString):
                    tempStr += _tag
                    continue
                if _tag.name == 'li':
                    template1 = "- {}"
                    r = self.handle_common(context1, _tag)
                    tempStr += "\n" + template1.format(r)
                else:
                    r = self.handle_common(context1, _tag)
                    tempStr += r
            return tempStr

    def handle_ol(self, tag, context1: MyContext):
        """
        有序列表
        :param context1:
        :param tag:
        :return:
        """
        template = "1. {}"
        if eventual_tag(tag):
            if len(tag) == 0:
                return template.format("")
            return template.format(tag.text)
        else:
            tempStr = ""
            count = 1
            for _tag in tag.contents:
                if isinstance(_tag, NavigableString):
                    tempStr += _tag
                    continue
                if _tag.name == 'li':
                    template1 = "{}. {}"
                    r = self.handle_common(context1, _tag)
                    tempStr += "\n" + template1.format(count, r)
                    count += 1
                else:
                    r = self.handle_common(context1, _tag)
                    tempStr += r
            return tempStr

    def handle_a(self, tag, context1: MyContext):
        """
        链接
        :param context1:
        :param tag:
        :return:
        """
        template = "[{}]({})"
        if eventual_tag(tag):
            if len(tag) == 0:
                return template.format("temp", "temp")
            return template.format(tag.text, tag.attrs.get("href"))
        else:
            href = tag.attrs.get("href")
            r = self.handle_common(context1, tag)
            return template.format(r, href)

    def handle_table(self, tag, context1: MyContext):
        """
        表格
        :param context1:
        :param tag:
        :return:
        """
        tbody: Tag = tag.tbody
        # if not tbody:
        #     return self.handle_common(context1, tag)
        table_str = ""
        row_count = 0
        col_num = 0
        for _tr in tbody.contents:
            row = " | "
            for _td in _tr.contents:
                if row_count == 0:
                    col_num += 1
                r = self.handle_common(context1, _td)
                r = r.replace("\n", "")
                row += r + " | "
            row += "\n"
            table_str += row
            if row_count == 0:
                separate = "|" + "|".join(["---" for _ in range(0, col_num)]) + "|\n"
                table_str += separate
            row_count += 1
        return table_str

    #


if __name__ == '__main__':
    # fp = open('../html_test/lake_asl.html', mode='r', encoding='utf-8')
    # allText = fp.readlines()
    # fp.close()
    my = MyParser(html_text)
    # my = MyParser("".join(allText))
    # my.traverse(my.soup, 0)
    context = MyContext()
    res = my.handle_descent(my.soup, context)
    # content = "\n".join(context.result)
    print(res)
    f = open('../html_test/lake_data_t.md', 'w', encoding='utf-8')
    f.writelines(res)
    f.flush()
    f.close()
    # s = "{0},{0},{1}".format("nihao", "hello")
    # print(s)
