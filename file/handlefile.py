"""
@Author:qiang.zhou
@Time:
"""
import os
import shutil

path = "F:/VIDEOS/2019/1/"
for (parent, dirs, files) in os.walk(path):
    print(parent)
    for filename in files:
        file = parent+"/"+filename
        if os.path.isfile(file):
            print(file)
            shutil.move(file, "F:/VIDEOS/2019/"+filename)
    # for dirc in dirs:
    #     print(dirc)
    # shutil.move("old", "new")
