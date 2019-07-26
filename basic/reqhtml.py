# -*- coding:utf-8 -*-
import logging, requests
import sys
import os
import urllib


def report(count, blockSize, totalSize):
    percent = int(count * blockSize * 100 / totalSize)
    sys.stdout.write("\r%d%% complete" % percent )
    sys.stdout.flush()

logging.basicConfig(filename='log.log', level=logging.DEBUG, format=" %(asctime)s - %(levelname)s %(message)s")
# reg = r" href='(http.*\.mp4)' "
# serchword = "python"
url = "http://sxtvideomp4.bj.bcebos.com/%E6%89%80%E6%9C%89%E8%A7%86%E9%A2%91Mp4%E6%A0%BC%E5%BC%8F%2FJAVA300%E9%9B%862018%E7%89%88%2F02_%E9%9D%A2%E5%90%91%E5%AF%B9%E8%B1%A1%E5%9F%BA%E7%A1%80%2F070_%E9%9D%99%E6%80%81%E5%88%9D%E5%A7%8B%E5%8C%96%E5%9D%97_%E7%BB%A7%E6%89%BF%E6%A0%91%E7%9A%84%E8%BF%BD%E6%BA%AF.mp4"
full_name = urllib.parse.unquote(url.split(r".com/")[1])
f_paths = full_name.split(r"/")
name = f_paths[-1]
print(name)
paths = f_paths[0: len(f_paths)-1]
for path in paths:
    print(os.getcwd())
    if os.path.exists(path):
        os.chdir(path)
    else:
        os.mkdir(path)
        os.chdir(path)
print('\rFetching %s...\n' %name)
urllib.request.urlretrieve(url, name, reporthook=report)
print("\rDownload complete, saved as %s \n\n" %name)
os.chdir(sys.path[0])
print(os.getcwd())
# res = requests.get(url, headers= {'Connection': 'close'})
# print("get url response")
# print("download complete")
# res.raise_for_status()
# playFile = open("70.mp4", 'wb')
# for chunk in res.iter_content(100000):
#     playFile.write(chunk)
# playFile.close()
# bsojb = bs4.BeautifulSoup(res.text)
