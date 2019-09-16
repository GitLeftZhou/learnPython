import random
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED, as_completed
import time

"""
线程池的几种使用方式
"""


# 参数times用来模拟网络请求的时间
def get_html(num):
    sleep = 1  # random.randint(0, 5)
    time.sleep(sleep)
    print("get page {} finished".format(num))
    return num


executor = ThreadPoolExecutor(max_workers=3)
urls = [2, 3, 4, 5, 6, 7]  # 并不是真的url

# all_task = [executor.submit(get_html, (url)) for url in urls]

# 这个方式将所有的future保存,结果会根据urls顺序输出
# wait(all_task, return_when=ALL_COMPLETED)
# for task in all_task:
#     print("result page {} has been finished".format(task.result()))
# print("main completed")

# 这个方式没有排序
# for future in as_completed(all_task):
#     data = future.result()
#     print("in main: get page {} success".format(data))

for data in executor.map(get_html, urls[2:]):
    print("in main: get page {} success".format(data))
