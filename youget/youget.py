import os


class YouGetDownloader:
    """
    包装了一下you-get工具，现有的you-get工具使用-l 参数下载容易出错
    重新下载会从第一个文件开始
    本类实现了自定义从第几个文件开始下载
    """

    def __init__(self, p_dir: str, d_url: str, *args_range: int):
        """
        构造函数
        :param p_dir: 下载目录
        :param d_url: 下载链接
        :param args_range: 两个int参数  begin index , end index
        """
        self.dl_url = "you-get -o " + p_dir + " " + d_url
        self.bgn = None
        self.end = None
        if args_range is not None:
            self.bgn = args_range[0]
            self.end = args_range[1] + 1
        # print(self.dl_url)
        # print(self.bgn)
        # print(self.end)

    def down(self):
        command = ""
        if self.bgn is not None and self.end is not None:
            if self.dl_url.find("?p="):
                command = self.dl_url.split("?p=")[0] + "?p="
            else:
                if self.dl_url.endswith("/"):
                    command + "?p="
                else:
                    command + "/?p="
            for idx in range(self.bgn, self.end):
                c_command = command + str(idx)
                print(c_command)
                r_v = os.system(c_command)
                print(r_v)
        else:
            command = self.dl_url
            print(command)
            r_v = os.system(command)
            print(r_v)
        print("=" * 20 + "complete" + ("=" * 20))


if __name__ == "__main__":
    CRLF = "\r\n"
    # c_url = r"c:\download\java\SpringCloud https://www.bilibili.com/video/av22613028/?p=5"
    defaultValue = {"dir": "E:/myfile/bilibili"}
    thisValue = {"dir": r"E:/myfile/bilibili/flink", "url": "https://www.bilibili.com/video/av50540281"}

    # 加这个 CRLF 控制符很有必要，在输入时，解决直接粘贴的问题
    p_dir = input("input the store directory:\r\n") + CRLF
    if p_dir is None or len(p_dir.strip()) == 0:
        p_dir = thisValue.get("dir")  # 使用get(key)
    p_url = input("input the url:\r\n") + CRLF
    if p_url is None or len(p_url.strip()) == 0:
        p_url = thisValue["url"]  # 使用[key]
    p_bgn = input("input the range index of beginning:\r\n") + CRLF
    p_end = input("input the range index of ending:\r\n") + CRLF

    downloader = YouGetDownloader(p_dir.rstrip(), p_url.strip(), int(p_bgn.strip()), int(p_end.strip()))
    downloader.down()
