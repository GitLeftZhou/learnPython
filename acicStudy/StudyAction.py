# -*- coding: utf-8 -*-
import shelve
import sys
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver import ActionChains

from selenium.webdriver.chrome.webdriver import WebDriver


class StudyAction:

    def __init__(self, web_driver: WebDriver):
        self.sleep_times: int = 30
        self.sleep_sec_per: int = 1
        self.webbw = web_driver

    def login(self):

        """
        登录网站
        :return 无返回:
        """

        try:
            # 打开首页
            self.webbw.get('http://acic.21tb.com/')
            self.webbw.maximize_window()
            main_window = self.webbw.current_window_handle
            # 点击登录

            input_username = None
            input_passwd = None
            try:
                mydata = shelve.open('mydata')

                if "acic_input_username" in mydata.keys() and "acic_input_passwd" in mydata.keys():
                    input_username = mydata['acic_input_username']
                    input_passwd = mydata['acic_input_passwd']
                else:
                    input_username = input('输入用户名\n')
                    input_passwd = input('输入密码\n')
                    mydata["acic_input_username"] = input_username
                    mydata["acic_input_passwd"] = input_passwd

                mydata.close()
            except IOError:
                print("从本地存储文件中获取用户密码失败")

            username = self.webbw.find_element_by_id("loginName")
            password = self.webbw.find_element_by_id('swInput')
            username.send_keys(input_username)
            password.send_keys(input_passwd)
            # 点击登录
            login_btn = self.webbw.find_element_by_css_selector('div.denglu > input[type=submit]')
            login_btn.click()
            return main_window
        except Exception as ex:
            print("login error")
            raise Exception("login error", ex)

    def goto_course_page(self, main_handle):

        if self.webbw.current_window_handle != main_handle:
            self.webbw.switch_to.window(main_handle)

        tmp_cnt = 0
        while True:
            try:
                go_into_btn = self.webbw.find_element_by_class_name("goIntoBtn")
                if go_into_btn is not None and go_into_btn.text == "进入学习平台":
                    go_into_btn.click()
                    break
                else:
                    tmp_cnt += 1
            except NoSuchElementException as ex:
                print("click goIntoBtn error retry again")
                tmp_cnt += 1
            if tmp_cnt >= self.sleep_times:
                break
            time.sleep(self.sleep_sec_per)

        tmp_cnt = 0
        while True:
            try:
                # dr.find_element_by_xpath("//div[@class='codelist codelist-desktop cate3']
                #                                //h4[contains(text(),'Python3')]").click()
                # document.querySelector("div.tbc-desktop-slide.tbc-tabset > div > div:nth-child(2) > div > span")

                course_center = self.webbw.find_element_by_css_selector("div[_shortcutid='new_course_center']")
                if course_center is not None:
                    course_center.click()
                    break
                else:
                    tmp_cnt += 1
            except NoSuchElementException as ex:
                print("click course_center error retry again")
                tmp_cnt += 1
            if tmp_cnt >= self.sleep_times:
                break
            time.sleep(self.sleep_sec_per)

        # 获取当前所有开启窗口的句柄
        all_handles = self.webbw.window_handles
        for handle in all_handles:
            if handle != main_handle:  # 获取到与当前窗口不一样的窗口
                self.webbw.switch_to.window(handle)  # 切换
                time.sleep(2)

        return self.webbw.current_window_handle

    def switch_to_desktop(self, main_handle):
        if self.webbw.current_window_handle != main_handle:
            self.webbw.switch_to.window(main_handle)

    def get_all_course(self, limit_period, limit_course):
        tmp_cnt = 0
        while True:
            try:
                # ncMenuHead
                # self.webbw.find_element_by_css_selector("#ncMenuHead > a").click()
                course_center = self.webbw.find_element_by_css_selector("#ncMenuHead > a")
                if course_center is not None and course_center.text == "全部课程分类":
                    course_center.click()
                    time.sleep(5)
                    actions = ActionChains(self.webbw)
                    my_page_url = self.webbw.find_element_by_css_selector("#loadStudyTask")
                    actions.move_to_element(my_page_url)
                    # self.webbw.find_element_by_css_selector("dl:nth-child(1) > dd:nth-child(3)").click()
                    break
                else:
                    tmp_cnt += 1
            except NoSuchElementException as ex:
                print("click course_center error retry again")
                tmp_cnt += 1
            if tmp_cnt >= self.sleep_times:
                break
            time.sleep(self.sleep_sec_per)

        course_count = 0
        with open("new-course-ids", 'w', encoding='utf-8') as f:
            # a.laypage_next
            has_laypage_next = True
            while has_laypage_next and course_count < limit_course:
                course_cards = self.webbw.find_elements_by_css_selector("li.nc-course-card")
                # print("course_cards size = "+str(len(course_cards)))
                for course_card in course_cards:
                    data_id = course_card.find_element_by_tag_name("a")
                    data_id_value = data_id.get_attribute("data-id")
                    done_txt = course_card.find_element_by_css_selector("span > span").text
                    xue_shi = course_card.find_element_by_css_selector(".card-msg-period").text
                    xue_fen = course_card.find_element_by_css_selector(".card-msg-credit").text
                    record_value = data_id_value + "," + done_txt + "," + xue_shi + "," + xue_fen
                    if done_txt != "已选" and float(xue_shi) < limit_period:
                        print(record_value)
                        f.write(record_value + "\n")  # 追加内容 换行
                        course_count += 1
                try:
                    laypage_next = self.webbw.find_element_by_css_selector("a.laypage_next")
                    laypage_next.click()
                    time.sleep(10)
                except WebDriverException as ex:
                    has_laypage_next = False

    def __choose_course(self):
        tmp_cnt = 0
        while True:
            try:
                choose_course = self.webbw.find_element_by_css_selector("#chooseCourse")
                if choose_course is not None and choose_course.is_enabled():
                    choose_course.click()
                    print("chooseCourse clicked")
                    break
                else:
                    tmp_cnt += 1
            except NoSuchElementException as ex:
                print("click choose_course error retry again")
                tmp_cnt += 1
            if tmp_cnt >= self.sleep_times:
                break
            time.sleep(self.sleep_sec_per)

        tmp_cnt = 0
        while True:
            try:
                go_study = self.webbw.find_element_by_css_selector("#goStudy")
                if go_study is not None and go_study.is_enabled():
                    go_study.click()
                    print("goStudy clicked ")
                    break
                else:
                    tmp_cnt += 1
            except NoSuchElementException as ex:
                print("click choose_course error retry again")
                tmp_cnt += 1
            if tmp_cnt >= self.sleep_times:
                break
            time.sleep(self.sleep_sec_per)

    def study_new_course(self, desktop, course_window):

        with open("new-course-ids", 'r', encoding='utf-8') as f:
            for line in f.readlines():
                course_infos = line.split(",")
                course_id = course_infos[0]
                choose_course_url = "http://acic.21tb.com/els/html/course/course.courseInfo.do?courseId={}&courseType=NEW_COURSE_CENTER&p=".format(
                    course_id)
                js = "window.open('{}');".format(choose_course_url)
                self.webbw.execute_script(js)
                window_handles = self.webbw.window_handles
                choose_course_handle = None
                for handle in window_handles:
                    if handle != course_window_handle and handle != desktop_handle:
                        choose_course_handle = handle
                        break
                print("choose_course_handle = {}".format(choose_course_handle))

                if choose_course_handle is not None:
                    self.webbw.switch_to.window(choose_course_handle)
                else:
                    print("CAN NOT GET CHOOSE COURSE HANDLE ERROR")
                self.__choose_course()
                course_time = int(3600 * (float(course_infos[2])))
                print("studying the {}.....thread will sleep {}".format(course_id, course_time))
                if course_time > 900:
                    course_time = 900
                time.sleep(course_time)
                self.webbw.close()
                self.webbw.switch_to.window(desktop_handle)

    def __get_my_course(self, main_handle, course_handle):

        if course_handle != self.webbw.current_window_handle:
            self.webbw.switch_to.window(course_handle)
            self.goto_course_page(main_handle)

        tmp_cnt = 0
        while True:
            try:
                my_course_center = self.webbw.find_element_by_css_selector("#loadStudyTask")
                if my_course_center is not None and my_course_center.is_enabled():
                    my_course_center.click()
                    time.sleep(5)
                    break
                else:
                    tmp_cnt += 1
            except NoSuchElementException as ex:
                print("click my_course_center error retry again")
                tmp_cnt += 1
            if tmp_cnt >= self.sleep_times:
                break
            time.sleep(self.sleep_sec_per)

        # //label[data-type='NOT_STARTED']
        # data-type STUDY
        # tmp_cnt = 0
        # while True:
        #     try:
        #         not_started = self.webbw.find_element_by_css_selector("label[data-type='NOT_STARTED']")
        #         if not_started is not None and not_started.is_enabled():
        #             not_started.click()
        #             time.sleep(5)
        #             break
        #         else:
        #             tmp_cnt += 1
        #     except NoSuchElementException as ex:
        #         print("click not_started error retry again")
        #         tmp_cnt += 1
        #     if tmp_cnt >= self.sleep_times:
        #         break
        #     time.sleep(self.sleep_sec_per)

        tmp_cnt = 0
        while True:
            try:
                studying = self.webbw.find_element_by_css_selector("label[data-type='STUDY']")
                if studying is not None and studying.is_enabled():
                    studying.click()
                    time.sleep(5)
                    break
                else:
                    tmp_cnt += 1
            except NoSuchElementException as ex:
                print("click studying error retry again")
                tmp_cnt += 1
            if tmp_cnt >= self.sleep_times:
                break
            time.sleep(self.sleep_sec_per)

        with open("my-studying-course-ids", 'w', encoding='utf-8') as f:
            # a.laypage_next
            has_laypage_next = True
            while has_laypage_next:
                my_course_cards = self.webbw.find_elements_by_css_selector("li.nc-course-card")
                print("my_course_cards size = " + str(len(my_course_cards)))
                for my_course_card in my_course_cards:
                    data_id = my_course_card.find_element_by_tag_name("a")
                    data_id_value = data_id.get_attribute("data-id")
                    try:
                        progress_text = my_course_card.find_element_by_css_selector("span.nc-progress-text")
                        if progress_text is not None and progress_text.is_enabled() and "课程学习" in progress_text.text:
                            record_value = data_id_value + "," + progress_text.text
                            print(record_value)
                            f.write(record_value + "\n")  # 追加内容 换行
                            # progress_text = None
                    except NoSuchElementException as nee:
                        pass
                try:
                    laypage_next = self.webbw.find_element_by_css_selector("a.laypage_next")
                    laypage_next.click()
                    time.sleep(10)
                except WebDriverException as ex:
                    has_laypage_next = False

    def study_my_course(self, main_handle, course_handle):
        running_flag = True
        while running_flag:
            self.__get_my_course(main_handle, course_handle)
            with open("my-studying-course-ids", 'r', encoding='utf-8') as fx:
                id_lines = fx.readlines()
                if len(id_lines) > 0:
                    for line in id_lines:
                        course_infos = line.split(",")
                        course_id = course_infos[0]
                        choose_course_url = "http://acic.21tb.com/els/html/courseStudyItem/courseStudyItem.learn.do?courseId={}&courseType=NEW_COURSE_CENTER&vb_server=http%3A%2F%2F21tb-video.21tb.com".format(
                            course_id)
                        js = "window.open('{}','study');".format(choose_course_url)
                        self.webbw.execute_script(js)
                        # 获取当前所有开启窗口的句柄
                        all_handles = self.webbw.window_handles
                        for handle in all_handles:
                            if handle != main_handle and handle != course_handle:  # 获取到与当前窗口不一样的窗口
                                self.webbw.switch_to.window(handle)  # 切换
                                time.sleep(2)
                        course_time = 600
                        print("studying the {}.....thread will sleep {}".format(course_id, course_time))
                        time.sleep(course_time)
                        # self.webbw.close()
                        # time.sleep(10)
                        # self.webbw.switch_to.window(desktop_handle)
                else:
                    running_flag = False


if __name__ == "__main__":
    sys.path.append(r"E:\PycharmProjects\learnPython")
    web_browser: WebDriver = webdriver.Chrome('E:\\myfile\\webbrowerdriver\\chromedriver_win32\\79\\chromedriver.exe')
    action = StudyAction(web_browser)
    desktop_handle = action.login()
    print("desktop-handle = " + desktop_handle)
    course_window_handle = action.goto_course_page(desktop_handle)
    print("course_window_handle = " + course_window_handle)
    action.get_all_course(0.2, 10)
    action.study_new_course(desktop_handle, course_window_handle)
    # action.study_my_course(desktop_handle, course_window_handle)
