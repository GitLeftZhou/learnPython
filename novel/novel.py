# coding:utf-8
import os
import re

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

            # response = requests.get(req_url)
            response = session.get(req_url, headers=headers)
            # 解析网页中的字符集定义
            tmpHtml = bs4.BeautifulSoup(str(response.text), "html5lib")
            # print(tmpHtml)
            meta_charsets = tmpHtml.find_all(NovelSpider.__has_charset)
            # 默认GBK，大多数小说网站都是用的GBK
            html_charset = "gbk"
            if meta_charsets is None or len(meta_charsets) == 0:
                meta_charsets = tmpHtml.find_all("meta", content=re.compile("charset"))
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

    def __parse_menu_html(self):
        """
        解析首页，拿到小说名字，第一章节链接
        :return:
        """
        try:
            res = self.request_url(self.menu_url)
            menuHtml = bs4.BeautifulSoup(str(res), "html.parser")
            # body > div.jieshao > div.rt
            title = menuHtml.select("div.rt h1")
            novel_name = str(title[0].text)
            print("novel_name :    " + novel_name)
            li_lists = menuHtml.select("div.mulu ul li")
            for li_tag in li_lists:
                a_tag = li_tag.find("a")
                # print("a_tag is ", end=" ")
                # print(type(a_tag))
                if a_tag is not None:
                    name = a_tag.text
                    # if "不可控的未来" in name:
                    #     print(len(self.url_names))
                    self.url_names.append(name)
                    url = a_tag["href"]
                    # self.urls.append(tag.children.get("href")) # 方法1
                    self.urls.append(url)  # 方法2
                    # print("-------------------")
                    # print(name+":  "+url)
        except Exception as ex:
            print("解析首页时异常", ex)
        return novel_name

    def __parse_content_html(self, cur_url, *cnts):
        content = ""
        if cnts is not None and len(cnts) > 0:
            cnt = cnts[0]
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

    def __write_txt(self, text1, path, *name):
        """
        写入TXT文档
        :param text1:
        :param path:
        :param name:
        :return:
        """
        file_name = ""
        if name is None or len(name) == 0:
            file_name = "novel.txt"
        else:
            file_name = name[0]
        with open(path + file_name, 'a', encoding='utf-8') as f:
            f.write(str(file_name) + '\n')  # 写入名字并换行
            f.write(text1)  # 追加内容
            f.write('\n\n')  # 换两行

    def spider(self, *idx):
        try:
            novel_name = self.__parse_menu_html()
            filename = novel_name + ".txt"
            path = "files/"
            if not os.path.isdir(path):
                os.mkdir(path)
            if idx is None or len(idx)==0:
                bgn_idx = 0
            else:
                bgn_idx = int(idx[0])
            with open(path + filename, 'w', encoding='utf-8') as f:
                f.write(str(novel_name) + self.menu_url + '\n')  # 写入名字并换行
                for i in range(bgn_idx, len(self.urls)):
                    next_url = self.urls[i]
                    print("抓取 " + self.url_names[i], end=" ")
                    content = self.__parse_content_html(str(self.menu_url + "" + next_url))
                    if "第" not in str(self.url_names[i]):
                        f.write("第"+str(i)+"章")
                    f.write(str(self.url_names[i]) + "\r\n")  # 写入章节名字
                    f.write(content + '\r\n')  # 追加内容 换行
                    print(" 完成")
        except Exception as ex:
            print("保存小说时发生异常", ex)
            return False
        return True


# 运行入口
if __name__ == "__main__":

    # url = "https://www.88dush.com/xiaoshuo/103/103884/"
    url = input("输入目录页的网址:\r\n") + "\r\n"
    if url is not None and len(url) > 10:
        a = NovelSpider(url.strip())
        idx = input("输入起始章节序号:\r\n")
        a.spider(idx)
        print("================小说下载完了==================")
        # print(a.menu_url)
    else:
        print("网址输入错误")
