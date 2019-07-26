# -*- coding: utf-8 -*-
import re
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

sys.path.append(r"E:\PycharmProjects\learnPython")

from okex.okaction import Okaction

# 打开Chrome
webbw: WebDriver = webdriver.Chrome('e:\\myfile\\chromedriver.exe')
action = Okaction(webbw)
action.login()
sell_list = []
buy_list = []
while True:
    try:
        curl = input("1.切换到币币交易页面\n2.切换到资金管理页面\n3.获取交易价格\n4.切换交易页面\nq.退出程序")
        if str(curl) == '1':
            a = time.time()
            action.view_trade()
            b = time.time()
            print("执行耗时%d" % (a - b))
        elif str(curl) == '2':
            a = time.time()
            action.view_balance()
            b = time.time()
            print("执行耗时%d" % (a - b))
        elif str(curl) == '3':
            a = time.time()
            # 切换的币币交易主页
            action.view_trade()
            base_currency = input("交易基础币(USDT,ETH,BTC)")
            tgt_currency = input("交易目标币")
            letter = re.compile(r"^[a-zA-Z]+$")
            base_check = letter.match(base_currency)
            if base_check:
                base_currency = str(base_currency).upper()
            if base_currency not in ('USDT', 'ETH', 'BTC'):
                print("invalible input base_currency")
                base_currency = None
            tgt_check = letter.match(tgt_currency)
            if tgt_check:
                tgt_currency = str(tgt_currency).upper()
            else:
                print("invalible input tgt_currency")

            if base_currency and tgt_currency:
                trade_price_list = action.get_current_price(base_currency, tgt_currency)
                trade_list_keys = trade_price_list.keys()
                if trade_price_list and "sell_list" in trade_list_keys and "buy_list" in trade_list_keys:
                    sell_list = trade_price_list.get("sell_list")
                    buy_list = trade_price_list.get("buy_list")

                    sell_list = action.sort_trade(sell_list, True)
                    buy_list = action.sort_trade(buy_list, False)

                    print("sell_list : ", end='')
                    print(sell_list)

                    print("buy_list : ", end='')
                    print(buy_list)

                    print("the min of sell_list :", end='')
                    print(Okaction.get_min(sell_list, True))
                    print("the max of buy_list :", end='')
                    print(Okaction.get_max(buy_list, False))
            b = time.time()
            print("执行耗时%d" % (a - b))
        elif str(curl) == '4':
            a = time.time()
            # 切换的币币交易主页
            Okaction.view_trade()
            base_currency = input("交易基础币(USDT,ETH,BTC)")
            tgt_currency = input("交易目标币")
            letter = re.compile(r"^[a-zA-Z]+$")
            base_check = letter.match(base_currency)
            if base_check:
                base_currency = str(base_currency).upper()
            if base_currency not in ('USDT', 'ETH', 'BTC'):
                print("invalible input base_currency")
                base_currency = None
            tgt_check = letter.match(tgt_currency)
            if tgt_check:
                tgt_currency = str(tgt_currency).upper()
            else:
                print("invalible input tgt_currency")

            if base_currency and tgt_currency:
                shift_flag = action.shift_trade_view(base_currency, tgt_currency)
                if shift_flag:
                    print("切换成功")
                else:
                    print("切换失败")
            b = time.time()
            print("执行耗时%d" % (a - b))
        elif str(curl) == 'q':
            webbw.close()
            sys.exit("good bye")
        else:
            print("invalible input menu")
        time.sleep(5)
    except Exception as err:
        print("执行过程中发生异常啦", err)

