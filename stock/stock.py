# coding: utf-8

import tushare as ts
import os

# tushare获取股票代码表 stocks_list
stock_list = ts.get_today_all()
filename = "E:\myfile\stock\stock_list.csv"
if os.path.exists(filename):
    stock_list.to_csv(filename, mode='a', header=None)
else:
    stock_list.to_csv(filename)
# print(ts.get_realtime_quotes('sh'))
# data = ts.get_hist_data('600050', start="2018-9-30", end="2019-9-30")
