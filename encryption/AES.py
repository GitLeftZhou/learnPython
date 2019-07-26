import base64
import json
import os
import random
import sys
import time

from Crypto.Cipher import AES
import hashlib


class AESEncrypt:
    """
    AES 加解密工具类
    """

    # 进度条
    @staticmethod
    def report(count, current, job):
        percent = int(current * 100 / count)
        sys.stdout.write("\r%s %d%%" % (job, percent))
        sys.stdout.flush()

    def __init__(self, u_key):
        """
        将文件解密，转换成字典放到内存中
        """
        self.key = u_key
        file_string = AESEncrypt.__cache_file()
        self.file_dic: dict = None
        if file_string is None or len(file_string) == 0:
            self.file_dic = {}
        else:
            try:
                delay = random.randint(5, 12)
                for i in range(delay):
                    time.sleep(1)
                    AESEncrypt.report(delay, i, "Verifying The Password ")
                print("\r\n")
                file_string = AESEncrypt.decrypt(self.key, file_string)
                # print(file_string)
                self.file_dic: dict = json.loads(file_string)
            except Exception as ex:
                print("Bad Password")
                sys.exit(1)

    @staticmethod
    def __cache_file():
        base_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
        if os.path.exists(base_dir + "/hehehehe"):
            with open(base_dir + "/hehehehe", "r") as f:
                file_text = f.read()
                return file_text
        else:
            return None

    @staticmethod
    def __rewrite_file(file_text):
        base_dir = os.path.dirname(os.path.realpath(sys.argv[0]))

        with open(base_dir + "/hehehehe", "w") as f:
            f.write(file_text)

    @staticmethod
    def __key_md5_16(key):
        """
        将key包装成16位
        :param key:
        :return: 返回bytes
        """
        md5 = hashlib.md5(key.encode("utf-8")).hexdigest()
        if len(md5) > 16:
            md5 = md5[0:8] + md5[-8:]
        return str.encode(md5)  # 返回bytes

    @staticmethod
    def __add_to_16(text):
        """
        不是16的倍数那就补足为16的倍数
        :param text: 待加密字符串
        :return: bytes
        """
        while len(text) % 16 != 0:
            text += '\0'
        return str.encode(text)  # 返回bytes

    @classmethod
    def encrypt(cls, key, text):
        """
        加密
        :param key: 密码
        :param text: 明文
        :return:
        """
        aes = AES.new(cls.__key_md5_16(key), AES.MODE_ECB)  # 初始化加密器
        return str(base64.encodebytes(aes.encrypt(cls.__add_to_16(text))), encoding='utf8').replace('\n', '')

    @classmethod
    def decrypt(cls, key, encrypted_text):
        """
        解密
        :param key: 密码
        :param encrypted_text:密文
        :return:
        """
        aes = AES.new(cls.__key_md5_16(key), AES.MODE_ECB)  # 初始化加密器
        return str(aes.decrypt(base64.decodebytes(bytes(encrypted_text, encoding='utf8'))).rstrip(b'\0')
                   .decode("utf8"))

    def view_all(self):
        for temp_key in self.file_dic.keys():
            print(temp_key, end=" : [")
            print("|".join(self.file_dic[temp_key]), end="]\r\n")

    def edit(self):
        dic_key: str = input("Input The Key:" + CRLF)
        account: str = input("Input The Account:" + CRLF)
        password: str = input("Input The Password:" + CRLF)
        comment: str = input("Input The Comment:" + CRLF)
        input_values = [dic_key, account, password, comment]
        # 更新内存字典
        if dic_key in self.file_dic.keys():
            dic_value: tuple = self.file_dic[dic_key]
            for i in range(len(input_values)):
                if input_values[i] is None or len(input_values[i]) == 0:
                    input_values[i] = dic_value[i]
        self.file_dic[dic_key] = tuple(input_values)

        # 更新文件
        AESEncrypt.__rewrite_file(AESEncrypt.encrypt(self.key, json.dumps(self.file_dic)))

    def find(self, find_key):
        if find_key in self.file_dic.keys():
            print(find_key, end=" : [")
            print("|".join(self.file_dic[find_key]), end="]\r\n")
        else:
            for it in self.file_dic.keys():
                if find_key in self.file_dic[it]:
                    print(it, end=" : [")
                    print("|".join(self.file_dic[it]), end="]\r\n")


if __name__ == "__main__":
    # u_key: str =input(" input your password \r\n")
    # u_text: str = input(" input the text which you trying to encrypt \r\n")  # 待加密文本
    # u_encrypted_text = AESEncrypt.encrypt(u_key, u_text)
    # print('加密值：', u_encrypted_text)
    # text_decrypted = AESEncrypt.decrypt(u_key, u_encrypted_text)
    # print('解密值：', text_decrypted)
    print("*" * 50)
    isRunning = True
    CRLF = "\r\n"
    u_key = input("Input Your Password :" + CRLF)
    encryption = AESEncrypt(u_key)
    manu: tuple = ("1.View All", "2.Edit", "3.Find", "4.Exit")
    action_info = CRLF.join(manu)

    while isRunning:
        print(action_info)
        caseId: str = input("Choose The Action :" + CRLF)
        print("*" * 50)
        if caseId in ("1", "2", "3", "4"):
            if caseId == "1":
                encryption.view_all()
            elif caseId == "2":
                encryption.edit()
            elif caseId == "3":
                find_key: str = input("Input the Keyword :" + CRLF)
                encryption.find(find_key)
            elif caseId == "4":
                print("GoodBye...")
                isRunning = False
        else:
            print("Error Input")

    print("*" * 50)
