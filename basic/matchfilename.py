import os

exception = ("Windows", "license","htm", "xml", "txt", "关键字替换","Python", "Docker", "kubernetes","WinRAR", "充电-技术","培训资料")
with open(r"tmp.txt", 'w', encoding='utf-8') as fw:
    for line_str_all in open(r"src.txt", encoding="utf-8"):
        if "matches in " in line_str_all and "Windows" not in line_str_all:
            file_full_path = line_str_all.split("matches in ")[1].replace("\n", "")
            is_del = True
            for exc in exception:
                if exc in file_full_path:
                    is_del = False
            if is_del and os.path.exists(file_full_path):
                print(file_full_path)
                fw.writelines(file_full_path+"\n")
                # try:
                #     os.remove(file_full_path)
                #     print(file_full_path+"成功删除")
                # except BaseException as e:
                #     print(file_full_path + "删除错误"+ str(e))

print("执行完成")