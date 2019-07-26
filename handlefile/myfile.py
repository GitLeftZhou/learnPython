# coding:utf-8

import os
import re


# for line_str in open(r"E:\myfile\pythonfile\re.txt", encoding="utf-8"):
#
#     if line_str.find("matches in") > -1:
#         str0 = line_str.split("matches in ")[1]
#         str1 = str0.split("::")[0]
#         if str1 is not None and len(str1) > 3:
#             if os.path.exists(str1):
#                 print(str1,end=" ")
#                 os.unlink(str1)
#                 print(" has been deleted")
# send2trash.send2trash(str1)


# with open("E:\\myfile\\pythonfile\\re.txt", encoding="utf-8") as f:
#
#     line = f.readline()
#     while line:
#         if line.find("matches in") > -1:
#             print(line)
#         line = f.readline()

def walkFolder(file):
    for root, dirs, files in os.walk(file):
        #  root 当前文件夹路径
        #  dirs 子目录list
        #  files 文件list

        # s = "尚硅谷_SpringCloud#9. 09.尚硅谷_SpringCloud_为什么选择SpringCloud作为微服务架构.flv"
        # t = re.compile(r'\. \d+\.').findall(s)
        # print(t)
        # 遍历
        for f in files:
            # new_name = f.replace("（全） ", "")
            new_name = re.sub(r'#\d+\. ', 'P', f, 1, flags=re.I)\
                .replace("Python教程_600集Python从入门到精通教程（懂中文就能学会）", "Python_教程")\
                # .replace("Java视频", "_").replace("视频教程", "")
            abs_old = os.path.join(root, f)
            abs_new = os.path.join(root, new_name)
            print(abs_new)
            os.rename(abs_old, abs_new)


def main():
    walkFolder("E:\\myfile\\bilibili\\python\\python黑马程序员版")


if __name__ == '__main__':
    main()
