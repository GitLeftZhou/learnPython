# -*- coding: utf-8 -*-
import shelve
import time
import re

from selenium.webdriver.chrome.webdriver import WebDriver


# from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys


class Okaction:
    """
    这个是网站内动作类

    """
    # sleep_sec_per: int = 1
    # sleep_times: int = 30
    # webbw: WebDriver = None

    def __init__(self, webbw: WebDriver):
        self.sleep_times: int = 30
        self.sleep_sec_per: int = 1
        self.webbw = webbw

    def login(self):

        """
        登录网站
        :return 无返回:
        """

        try:
            # 打开OKEX首页
            self.webbw.get('https://www.okb.com/')

            # 点击登录
            user_login = self.webbw.find_element_by_class_name('user-login')
            user_login.click()

            # 输入用户名密码
            username = self.webbw.find_element_by_name('username')
            password = self.webbw.find_element_by_name('password')
            input_username = None
            input_passwd = None
            try:
                mydata = shelve.open('mydata')

                if "ok_input_username" in mydata.keys() and "ok_input_passwd" in mydata.keys():
                    input_username = mydata['ok_input_username']
                    input_passwd = mydata['ok_input_passwd']
                else:
                    input_username = input('输入用户名\n')
                    input_passwd = input('输入密码\n')
                    mydata["ok_input_username"] = input_username
                    mydata["ok_input_passwd"] = input_passwd

                mydata.close()
            except IOError:
                print("从本地存储文件中获取用户密码失败")

            username.send_keys(input_username)
            password.send_keys(input_passwd)

            # 点击登录
            login_btn = self.webbw.find_element_by_class_name('login-btn ')
            login_btn.click()

            # 点击发送验证码
            cnt = 0
            while True:
                send_code = self.webbw.find_element_by_class_name('send-code-btn ')
                if send_code is not None and send_code.text == "发送验证码":
                    try:
                        send_code.click()
                        break
                    except:
                        print("click send-code-btn error retry again")
                        cnt += 1
                else:
                    cnt += 1
                if cnt >= self.sleep_times:
                    break

                time.sleep(self.sleep_sec_per)

            # 输入验证码
            input_code = input('输入验证码\n')
            code = self.webbw.find_element_by_class_name('send-code')
            code.send_keys(input_code)

            # 确认登录
            confirm_btn = self.webbw.find_element_by_class_name('confirm-btn')
            confirm_btn.click()
        except Exception as ex:
            print("login error")
            raise Exception("login error", ex)

    def view_trade(self):
        """
        查看币币交易
        :return:
        """
        cnt = 0
        while True:
            trade_url = self.webbw.find_element_by_css_selector("a[href *='/trade']")
            if trade_url is not None:
                if "active" not in trade_url.get_attribute("class"):
                    trade_url.click()
                break
            else:
                cnt += 1
            if cnt >= self.sleep_times:
                break
            time.sleep(self.sleep_sec_per)

    def view_balance(self):
        """
        查看账户
        :return:
        """
        cnt = 0
        while True:
            balance_url = self.webbw.find_element_by_css_selector("a[href *='/balance']")
            if balance_url is not None:
                if "active" not in balance_url.get_attribute("class"):
                    balance_url.click()
                break
            else:
                cnt += 1
            if cnt >= self.sleep_times:
                break
            time.sleep(self.sleep_sec_per)

    def shift_trade_view(self, base_currency: str, tgt_currency: str) -> object:
        """
        切换交易界面
        :param base_currency:
        :param tgt_currency:
        :return:
        """
        # 切换到交易本币窗口  使用xpath更方便获取
        try:
            # 基础交易货币类型字典
            base_cur_dict = ("USDT", "ETH", "BTC")
            if base_currency not in base_cur_dict:
                raise Exception("无效的基础交易货币")
            else:
                base_currency = base_currency.upper()

            letter = re.compile(r"^[a-zA-Z]+$")
            tgt_check = letter.match(tgt_currency)
            if tgt_check:
                tgt_currency = str(tgt_currency).upper()
            else:
                raise Exception("无效目标币种")

            cnt = 0
            while True:
                xpath_base_currency = "//ul[@class='spot-head-tab']/li[contains(text(),'" + base_currency + "')]"
                li_base_currency = self.webbw.find_element_by_xpath(xpath_base_currency)
                if li_base_currency is not None:
                    if "active" in li_base_currency.get_attribute("class"):
                        print("current spot-head-tab: " + base_currency + " is active.no need to click")
                    else:
                        li_base_currency.click()
                    break
                else:
                    cnt += 1
                if cnt >= self.sleep_times:
                    break
                time.sleep(self.sleep_sec_per)

            # 切换到目标币种页  使用xpath更方便获取
            # // label[contains(text(), "ETH/USDT")]
            cnt = 0
            while True:
                xpath_tgt_currency = "//label[contains(text(),'" + tgt_currency + "/" + base_currency + "')]"
                label_tgt_currency = self.webbw.find_element_by_xpath(xpath_tgt_currency)
                if label_tgt_currency is not None:
                    if "active" in label_tgt_currency.get_attribute("class"):
                        print("current label: " + tgt_currency + "/" + base_currency + " is active.no need to click")
                    else:
                        label_tgt_currency.click()
                    break
                else:
                    cnt += 1
                if cnt >= self.sleep_times:
                    break
                time.sleep(self.sleep_sec_per)
            return True
        except Exception as err:
            print("切换交易页面失败", err)
            return False

    def get_current_price(self, base_currency: str, tgt_currency: str):
        """
        获取当前交易价格
        :param base_currency: str 交易本币
        :param tgt_currency: str  目标交易币
        :return pirce_dict : dict {"sell_list":[{price:str,num:str}],"buy_list":[{price:str,num:str}],"up_ticker":str}
                            sell_list: 卖出价
                            buy_list:  买入价
                            up_ticker：当前价格
        """
        try:
            base_cur_dict = ("USDT", "ETH", "BTC")
            if base_currency not in base_cur_dict:
                raise Exception("无效的基础交易货币")

            shift_flag = self.shift_trade_view(base_currency, tgt_currency)
            if not shift_flag:
                raise Exception("切换交易页面失败")

            # 获取价格列表  使用css selector 更方便获取
            # div.scroll-box > ul.sell-list  ul.buy-list  ul.up ticker  ul.down ticker
            # pirce_dict = {}
            cnt = 0
            while True:
                dom_sell_list = self.webbw.find_elements_by_css_selector("ul.sell-list>li")
                dom_buy_list = self.webbw.find_elements_by_css_selector("ul.buy-list>li")
                if dom_sell_list and dom_buy_list:
                    #  卖方价格列表
                    sell_list = []
                    #  买方价格列表
                    buy_list = []
                    for dom_sell_item in dom_sell_list:
                        # 卖方价格字典
                        dom_price = dom_sell_item.find_element_by_css_selector("span:nth-child(1)")
                        dom_num = dom_sell_item.find_element_by_css_selector("span:nth-child(2)")
                        sell_item = {"price": str(dom_price.text), "num": str(dom_num.text)}
                        sell_list.append(sell_item)

                    for dom_buy_item in dom_buy_list:
                        # 买方价格字典
                        dom_price = dom_buy_item.find_element_by_css_selector("span:nth-child(1)")
                        dom_num = dom_buy_item.find_element_by_css_selector("span:nth-child(2)")
                        buy_item = {"price": str(dom_price.text), "num": str(dom_num.text)}
                        buy_list.append(buy_item)
                    # 返回价格列表
                    pirce_dict = {"sell_list": sell_list, "buy_list": buy_list}
                    return pirce_dict
                else:
                    cnt += 1
                if cnt >= self.sleep_times:
                    break
                time.sleep(self.sleep_sec_per)

        except Exception as ex:
            print("获取价格列表失败", ex)
            return None
        return None

    def buy(self, base_currency: str, tgt_currency: str, trade_mode: str, price: float, num: float, total: float):
        """
        购买动作
        :param base_currency: 交易基础币
        :param tgt_currency: 交易目标币
        :param trade_mode:交易类型(限价单，市价单)
        :param price: 交易价格
        :param num: 交易数量   defalt 0 参数为0时 忽略此参数
        :param total: 交易总额  defalt 0 参数为0时 忽略此参数
        :return:
        """
        try:
            if not price:
                price = 0
            if not num:
                num = 0
            if not total:
                total = 0

            return self.__trade__('sell', base_currency, tgt_currency, trade_mode, price, num, total)
        except Exception as ex:
            print("购买时发生异常", ex)
            return False

    def sell(self, base_currency: str, tgt_currency: str, trade_mode: str, price: float, num: float, total: float):
        """
        购买动作
        :param base_currency: 交易基础币
        :param tgt_currency: 交易目标币
        :param trade_mode:交易类型(限价，市场价)
        :param price: 交易价格
        :param num: 交易数量   defalt 0 参数为0时 忽略此参数
        :param total: 交易总额  defalt 0 参数为0时 忽略此参数
        :return:
        """
        try:
            if not price:
                price = 0
            if not num:
                num = 0
            if not total:
                total = 0
            return self.__trade__('sell', base_currency, tgt_currency, trade_mode, price, num, total)
        except Exception as ex:
            print("购买时发生异常", ex)
            return False

    def __trade__(self, trade_type: str, base_currency: str, tgt_currency: str, trade_mode: str,
                  price: float, num: float, total: float) -> object:
        """
        交易动作
        :param trade_type: 交易类型 'buy','sell'
        :param base_currency: 交易基础币
        :param tgt_currency: 交易目标币
        :param trade_mode:交易模式(限价单，市价单)  暂时不考虑市价单 默认限价单
        :param price: 交易价格 defalt 0 参数为0时 忽略此参数
        :param num: 交易数量   defalt 0 参数为0时 忽略此参数
        :param total: 交易总额  defalt 0 参数为0时 忽略此参数
        :return:
        """
        try:

            trade_type_tgt = trade_type + tgt_currency

            # 切换交易页面
            shift_flag = self.shift_trade_view(base_currency, tgt_currency)
            if not shift_flag:
                raise Exception("切换交易页面失败")

            # 切换买入卖出窗口
            shift_flag = self.__shift_trade_type__(trade_type, tgt_currency)
            if not shift_flag:
                raise Exception("切换买入卖出窗口失败")

            # 切换价格方案  限价交易，市场价交易
            shift_flag = self.__shift_trade_mode__(trade_mode)
            if not shift_flag:
                raise Exception("切换价格方案限价交易，市场价交易失败")

            # 将购买参数录入到交易区
            shift_flag = self.__input_trade_argument__(price, num, total)
            if not shift_flag:
                raise Exception("将购买参数录入到交易区失败")

            # 获取交易提交按钮并点击 eg:[买入ETH, 卖出ETH]  确认交易
            # $('.spot-submit>button')
            cnt = 0
            while True:
                spot_submit_button = self.webbw.find_element_by_css_selector(".spot-submit>button")
                if spot_submit_button:
                    # 确保页面按钮和交易参数是一致的，防止页面元素未切换就提交
                    if trade_type == "买入" and spot_submit_button.text == trade_type_tgt:
                        spot_submit_button.click()
                    elif trade_type == "卖出" and spot_submit_button.text == trade_type_tgt:
                        spot_submit_button.click()
                    break
                else:
                    cnt += 1
                if cnt >= self.sleep_times:
                    break
                time.sleep(self.sleep_sec_per)

            return True
        except Exception as ex:
            print("交易时发生异常", ex)
            return False

    def __shift_trade_type__(self, trade_type: str,tgt_currency: str) -> object:
        """
        切换交易类型 ： 买入，卖出
        :param trade_type: 交易类型 'buy','sell'
        :param tgt_currency: 交易目标币
        :return:
        """
        try:

            if trade_type not in ('buy', 'sell', 'BUY', 'SELL'):
                raise Exception("无效的交易类型")
            # 处理交易类型
            if trade_type in ('buy',  'BUY'):
                trade_type = "买入"
            elif trade_type in ('sell', 'SELL'):
                trade_type = "卖出"

            letter = re.compile(r"^[a-zA-Z]+$")
            tgt_check = letter.match(tgt_currency)
            if tgt_check:
                tgt_currency = str(tgt_currency).upper()
            else:
                raise Exception("无效目标币种")

            trade_type_tgt = trade_type + tgt_currency

            # 切换买入卖出窗口
            # $x('//ul[@class="spot-tab-heads"]/li[contains(text(),"买入ETH")]')
            cnt = 0
            while True:
                spot_tab_heads_active = self.webbw.\
                    find_element_by_css_selector("//ul[@class='spot-tab-heads']/li[contains(text(),'" + trade_type_tgt + "')]")
                if spot_tab_heads_active:
                    if "active" in spot_tab_heads_active.get_attribute("class"):
                        print("current label: " + trade_type_tgt + " is active. no need to click")
                    else:
                        spot_tab_heads_active.click()
                    break
                else:
                    cnt += 1
                if cnt >= self.sleep_times:
                    break
                time.sleep(self.sleep_sec_per)

            return True
        except Exception as ex:
            print("切换交易类型时发生异常", ex)
            return False

    def __shift_trade_mode__(self, trade_mode: str) -> object:
        """
        切换交易模式
        :param trade_mode:交易模式(限价单，市价单)  默认限价单
        :return:
        """
        try:
            if trade_mode:
                if trade_mode not in ('限价单', '市价单'):
                    raise Exception("无效的交易模式")
            else:
                trade_mode = "限价单"

            # 切换价格方案  限价交易，市场价交易
            # $('#react-select-6--value>div.Select-value') 外层对象，点击展示 下拉菜单 Select-arrow-zone
            # $('span#react-select-6--value-item') 内层对象，获取界面显示值
            # Select-menu-outer

            cnt = 0
            while True:
                select_value_label = self.webbw.find_element_by_css_selector("span#react-select-6--value-item")
                if select_value_label:
                    if select_value_label.text == trade_mode:
                        print("current label: " + trade_mode + " is active. no need to click")
                    else:
                        # 点击“委托类型”
                        cnt_1 = 0
                        while True:
                            react_select = self.webbw.find_element_by_css_selector("#react-select-6--value>div.Select-value")
                            if react_select:
                                react_select.click()
                                break
                            else:
                                cnt_1 += 1
                            if cnt_1 >= self.sleep_times:
                                break
                            time.sleep(self.sleep_sec_per)

                        # 获取下拉列表 并点击
                        cnt_1 = 0
                        while True:
                            select_menu_outer = self.webbw.find_elements_by_css_selector("div.Select-menu-outer>div")
                            if react_select:
                                for li_menu in select_menu_outer:
                                    if li_menu.text == trade_mode:
                                        li_menu.click()
                                break
                            else:
                                cnt_1 += 1
                            if cnt_1 >= self.sleep_times:
                                break
                            time.sleep(self.sleep_sec_per)
                    break
                else:
                    cnt += 1
                if cnt >= self.sleep_times:
                    break
                time.sleep(self.sleep_sec_per)

            return True
        except Exception as ex:
            print("切换交易模式时发生异常", ex)
            return False

    def __input_trade_argument__(self, price: float, num: float, total: float):
        """
        输入交易区参数
        :param price:
        :param num:
        :param total:
        :return:
        """
        try:
            # 获取到交易区元素  以交易基础币为单位
            # .spot-price input-container>span  text contains "价格"    .spot-price input-container>input
            # .spot-amout input-container>span  text contains "数量"    .spot-amout input-container>input
            # .spot-total input-container>span  text contains "总金额"  .spot-total input-container>input
            cnt = 0
            while True:
                spot_price_container = self.webbw.find_element_by_css_selector(".spot-price.input-container")
                spot_amout_container = self.webbw.find_element_by_css_selector(".spot-amout.input-container")
                spot_total_container = self.webbw.find_element_by_css_selector(".spot-total.input-container")
                if spot_price_container and price > 0:
                    _input_ = spot_price_container.find_element_by_css_selector("input")
                    # 调用_input_.clear() 清除后数据会重新出现，使用暴力清除，模拟键盘退格键删除
                    _input_value_ = _input_.get_attribute("value")
                    for i in range(len(_input_value_)):
                        _input_.send_keys(Keys.BACK_SPACE)
                    _input_.send_keys(str(price))
                elif spot_amout_container and num > 0:
                    _input_ = spot_amout_container.find_element_by_css_selector("input")
                    _input_value_ = _input_.get_attribute("value")
                    for i in range(len(_input_value_)):
                        _input_.send_keys(Keys.BACK_SPACE)
                    _input_.send_keys(str(num))
                elif spot_total_container and total > 0:
                    _input_ = spot_total_container.find_element_by_css_selector("input")
                    _input_value_ = _input_.get_attribute("value")
                    for i in range(len(_input_value_)):
                        _input_.send_keys(Keys.BACK_SPACE)
                    _input_.send_keys(str(total))
                else:
                    cnt += 1
                if cnt >= self.sleep_times:
                    break
                time.sleep(self.sleep_sec_per)

            return True
        except Exception as ex:
            print("输入交易区参数时发生异常", ex)
            return False

    def sort_trade(self, sort_list, is_asc):
        """
        排序
        :param sort_list:
        :param is_asc: True 升序排列  Flase 降序排列
        :return:
        """
        if is_asc:
            return sorted(sort_list, key=lambda price: float(price["price"]))
        else:
            return sorted(sort_list, key=lambda price: float(price["price"]), reverse=False)

    def get_min(self, sort_list, is_sorted):
        """
        获取最小交易
        :param sort_list:
        :param is_sorted: 是否升序排列  升序=True 降序=False 无序(不确定)=None
        :return:
        """
        list_size = len(sort_list)
        if is_sorted is None:
            new_list = sorted(sort_list, key=lambda price: float(price["price"]), reverse=True)
            return new_list[0]
        elif is_sorted:
            return sort_list[0]
        else:
            return sort_list[list_size]

    def get_max(self, sort_list, is_sorted):
        """
        获取最大交易
        :param sort_list:
        :param is_sorted: 是否升序排列  升序=True 降序=False 无序(不确定)=None
        :return:
        """
        list_size = len(sort_list)
        if is_sorted is None:
            new_list = sorted(sort_list, key=lambda price: float(price["price"]), reverse=False)
            return new_list[0]
        elif is_sorted:
            return sort_list[list_size]
        else:
            return sort_list[list_size]

    def get_unfinished_entrust(self):
        """
        获取未完成委托
        :return:
        """
        try:

            # 切换到未完成委托页
            # ul.tabs.clear-fix
                # li>span.text = "未成交委托"
                # li>span.text = "历史委托"
            cnt = 0
            while True:
                entrust_tab_unfinished = self.webbw.find_element_by_css_selector(
                    "//ul[@class='tabs clear-fix']/li/span[contains(text(),'未成交委托')]")
                if entrust_tab_unfinished:
                    if "active" in entrust_tab_unfinished.get_attribute("class"):
                        # 如果当前TAB页已经是[未成交委托] 切换一下TAB页，刷新一下数据
                        entrust_tab_history = self.webbw.find_element_by_css_selector(
                            "//ul[@class='tabs clear-fix']/li/span[contains(text(),'历史委托')]")
                        if entrust_tab_history:
                            entrust_tab_history.click()
                        entrust_tab_unfinished.click()
                    else:
                        entrust_tab_unfinished.click()
                    break
                else:
                    cnt += 1
                if cnt >= self.sleep_times:
                    break
                time.sleep(self.sleep_sec_per)

            # 获取未完成委托列表数据
            # table.ok-table>tbody>tr
                # td[0]>div>div>span[0] span[1]: 委托时间 td[1]>span: 币对(ETH/USDT)
                # td[2]>span: 类型(币币) td[3]>div>span: 方向(卖出)
                # td[4]>div: 委托总量|已完成(0.500000 ETH \r 0.000000 ETH)
                # td[5]>div: 委托价|成交均价(1,500.0000 USDT \r 0.0000 USDT)
                # td[6]: 委托金额(750.00 USDT) td[7]>span: 状态(未成交) td[8]>div>a: 操作(撤单)
            cnt = 0
            while True:
                unfinished_entrust_trs = self.webbw.find_elements_by_css_selector("table.ok-table>tbody>tr")
                if unfinished_entrust_trs:
                    for tr in unfinished_entrust_trs:
                        tds = tr.find_elements_by_css_selector("td")
                else:
                    cnt += 1
                if cnt >= self.sleep_times:
                    break
                time.sleep(self.sleep_sec_per)
            return True
        except Exception as ex:
            print("交易时发生异常", ex)
            return False