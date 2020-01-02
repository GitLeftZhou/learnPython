# coding:utf-8
import os
import re
import sys
import time
from concurrent.futures.thread import ThreadPoolExecutor

import bs4
import requests


class NovelSpider:

    def __init__(self, menu_url):
        self.menu_url = menu_url
        self.url_names = []
        self.urls = []

    @staticmethod
    def __has_charset(tag):
        return tag.has_attr('charset')

    def request_url(self, req_url):
        res = ""
        try:
            session = requests.session()
            headers = {"Accept": "text/html,application/xhtml+xml,application/xml;"
                                 "q=0.9,image/webp,image/apng,*/*;q=0.8",
                       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                                     "Chrome/66.0.3359.139 Safari/537.36"}

            response = session.get(req_url, headers=headers)
            # 解析网页中的字符集定义
            tmp_html = bs4.BeautifulSoup(str(response.text), "html5lib")
            # print(tmpHtml)
            meta_charsets = tmp_html.prettify().find_all(NovelSpider.__has_charset)
            # 默认GBK，大多数小说网站都是用的GBK
            html_charset = "gbk"
            if meta_charsets is None or len(meta_charsets) == 0:
                meta_charsets = tmp_html.find_all("meta", content=re.compile("charset"))
                meta_charset = meta_charsets[0]
                # print("meta_charset", end=" : ")
                # print(meta_charset)
                content_charset = str(meta_charset.get("content"))
                html_charset = content_charset.split("charset=")[-1]
                # print("==============" + content_charset)
                # print("==============" + html_charset)
            else:
                meta_charset = meta_charsets[0]
                # print("meta_charset", end=" : ")
                # print(meta_charset)
                html_charset = meta_charset.get("charset")
            # print("html_charset", end=" : ")
            # print(html_charset)
            res = response.content.decode(encoding=html_charset, errors='ignore')
            response.raise_for_status()
        except Exception as ex:
            print("获取网页文本", ex)
        return res

    def __parse_menu_html(self, title_name):
        """
        解析首页，拿到小说名字，第一章节链接
        :return:
        """
        novel_name = ""
        mark_index = 0
        try:
            res = self.request_url(self.menu_url)
            menu_html = bs4.BeautifulSoup(str(res), "html.parser")
            # body > div.jieshao > div.rt
            title = menu_html.select("div.rt h1")
            novel_name = str(title[0].text)
            print("novel_name :    " + novel_name)
            li_lists = menu_html.select("div.mulu ul li")
            for li_tag in li_lists:
                a_tag = li_tag.find("a")
                if a_tag is not None:
                    name = a_tag.text
                    if title_name is not None and title_name in name:
                        mark_index = len(self.url_names)
                    self.url_names.append(name)
                    # self.urls.append(tag.children.get("href")) # 方法1
                    url = a_tag["href"]
                    self.urls.append(url)  # 方法2

        except Exception as ex:
            print("解析首页时异常", ex)
        return novel_name, mark_index

    def __parse_content_html(self, cur_url, *counts):
        content = ""
        if counts is not None and len(counts) > 0:
            cnt = counts[0]
        else:
            cnt = 0
        try:
            res = self.request_url(cur_url)
            contentHtml = bs4.BeautifulSoup(str(res), "html.parser")
            content_obj: bs4.element.Tag = contentHtml.find("div", class_="yd_text2")
            # print("content_obj is ", end=" ")
            # print(type(content_obj))
            # print(content_obj)
            content = content_obj.text

        except Exception as ex:
            # 可能网络异常 重试5次
            if cnt < 5:
                cnt = cnt + 1
                self.__parse_content_html(cur_url, cnt)
            print("解析内容页时异常", ex)
        return content

    def __auto_next(self):
        """
        获取下一个链接地址  1  从返回网页里面获取下一页   2   从目录页直接获取
        采用目录页获取   使用方法1时  使用此方法
        :return:
        """
        return ""

    def __persistence(self, content):
        """
        例如抓数据存 nosql
        :param content:
        :return:
        """
        try:
            # 其他方式的持久化
            print("持久化")
        except Exception as ex:
            print("保存小说时发生异常", ex)
            return False
        return True

    def spider(self, novel_name, bgn_idx):
        """
        串行方式抓取
        :param novel_name:
        :param bgn_idx:
        :return:
        """
        try:
            filename = novel_name + ".txt"
            path = "files/"
            if not os.path.isdir(path):
                os.mkdir(path)
            with open(path + filename, 'w', encoding='utf-8') as f:
                f.write(str(novel_name) + self.menu_url + '\n')  # 写入名字并换行
                for i in range(bgn_idx, len(self.urls)):
                    next_url = self.urls[i]
                    print("抓取 " + self.url_names[i], end=" ")
                    content = self.__parse_content_html(str(self.menu_url + "" + next_url))
                    # if "第" not in str(self.url_names[i]):
                    f.write("第" + str(i) + "章 ")
                    f.write(str(self.url_names[i]).replace("第", "").replace("章", "") + "\r\n")  # 写入章节名字
                    f.write(content + '\r\n')  # 追加内容 换行
                    print(" 完成")
        except Exception as ex:
            print("保存小说时发生异常", ex)
            return False
        return True

    def concurrent_spider(self, novel_name, bgn_idx, max_workers):
        """
        并行方式获取
        :param novel_name: 文件名
        :param bgn_idx: 起始章节序号
        :param max_workers: 并行数
        :return:
        """
        try:
            filename = novel_name + ".txt"
            path = "files/"
            if not os.path.isdir(path):
                os.mkdir(path)
            # 初始化线程池
            executor = ThreadPoolExecutor(max_workers=max_workers)
            with open(path + filename, 'w', encoding='utf-8') as f:
                f.write(str(novel_name) + self.menu_url + '\n')  # 写入文件名并换行
                # 使用线程池map方式执行, 可以顺序的获取到结果
                for content in executor.map(self.__get_content, range(bgn_idx, len(self.urls)), self.urls[bgn_idx:]):
                    f.write(content + '\r\n')  # 追加内容 换行

        except Exception as ex:
            print("保存小说时发生异常", ex)
            return False
        return True

    def __get_content(self, url_index, target_url):
        """
        拼装每个章节的内容
        :param url_index: 章节序号
        :param target_url: 章节地址
        :return: 章节标题+章节内容
        """
        result_data = ""
        # 处理标题
        # if "第" not in str(self.url_names[url_index]):
        result_data = result_data + "第{}章 ".format(url_index)
        result_data = result_data + re.sub(r"第.*章", "", str(self.url_names[url_index])) + "\r\n"
        # 抓取内容并处理
        content = self.__parse_content_html(str(self.menu_url + "" + target_url))
        result_data = result_data + content.replace("\r", "").replace("\n", "").strip()
        # 返回内容
        print("抓取 [{}] 完成".format(self.url_names[url_index]))
        return result_data

    def get_bgn_idx(self, idx):
        """
        获取起始章节序号
        :param idx:
        :return:
        """
        bgn_idx = 0
        title_name = None
        if idx is not None:
            if idx.isdigit():
                bgn_idx = int(idx)
            else:
                title_name = idx
        (novel_name, mark_idx) = self.__parse_menu_html(title_name)
        if mark_idx is not None and mark_idx > 0:
            bgn_idx = mark_idx
        print((novel_name, bgn_idx))
        return novel_name, bgn_idx


# 运行入口
if __name__ == "__main__":
    begin_time = time.time()
    main_page = "https://www.88dush"
    url = input("输入目录页的网址:\r\n") + "\r\n"
    if url is not None and url.startswith(main_page):
        a = NovelSpider(url.strip())
        index = input("输入 [起始章节序号/起始章节名称]:\r\n")
        (file_name, begin_idx) = a.get_bgn_idx(index)
        workers = input("输入并行数(不能超过10个,默认10个):\r\n")
        if workers is not None and workers.isdigit():
            if int(workers) > 10:
                print("并发数不能超过10")
                sys.exit(0)
        elif workers is None or len(workers.strip()) == 0:
            workers = 10
        else:
            print("输入字符[{}]不合法,只能为10以下的整数".format(workers))
            sys.exit(0)
        if int(workers) < 2:
            a.spider(file_name, begin_idx)
        else:
            a.concurrent_spider(file_name, begin_idx, int(workers))
        end_time = time.time()
        print("=============[{}]下载完了,共耗时{}秒===============".format(file_name, format(end_time-begin_time, "0.2f")))
    else:
        print("错误的网址，目前只支持：" + main_page)
