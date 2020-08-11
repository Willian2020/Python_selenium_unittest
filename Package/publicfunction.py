#coding=utf-8

from Config import globalparam
from Package import datainfo
import unittest
from Package.log import Log
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
import pykeyboard
import os
success = "SUCCESS   "
fail = "FAIL   "

# 截图放到report下的img目录下
def get_img(dr, filename):
    path = globalparam.img_path + '\\' + filename
    dr.take_screenshot(path)

class Mytest(unittest.TestCase):

    def setUp(self):
        self.logger = Log()
        self.logger.info('############################### START ###############################')
        if globalparam.browserType == 'Chrome' or globalparam.browserType == 'chrome':
            options = webdriver.ChromeOptions()
            options.add_argument('--user-data-dir=C:/Users/Administrator/User Data')
            self.driver = webdriver.Chrome(chrome_options=options)
            self.driver.maximize_window()
            time.sleep(3)
        elif globalparam.browserType == 'IE' or globalparam.browserType == 'ie':
            self.driver = webdriver.Ie()
            self.driver.maximize_window()
            time.sleep(3)
        else:
            raise NameError('浏览器类型配置错误！')

    def tearDown(self):
        self.driver.quit()
        self.logger.info('###############################  End  ###############################')
        time.sleep(1)


class ObjOperate(object):

    def __init__(self,selenium_driver,parent=None):
        self.driver = selenium_driver
        self.parent = parent

    def element_wait(self, css, secs=20):
        """
        Waiting for an element to display.
        Usage:
        self.driver.element_wait("id->kw",10)
        """
        if "->" not in css:
            raise NameError("Positioning syntax errors, lack of '->'.")

        by = css.split("->")[0].strip()
        value = css.split("->")[1].strip()
        messages = 'Element: {0} not found in {1} seconds.'.format(css, secs)

        if by == "id":
            WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.ID, value)), messages)
        elif by == "name":
            WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.NAME, value)), messages)
        elif by == "class":
            WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.CLASS_NAME, value)), messages)
        elif by == "link_text":
            WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.LINK_TEXT, value)), messages)
        elif by == "xpath":
            WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.XPATH, value)), messages)
        elif by == "css":
            WebDriverWait(self.driver, secs, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, value)),messages)
        else:
            raise NameError("Please enter the correct targeting elements,'id','name','class','link_text','xpaht','css'.")

    def get_element(self, css):
        """
        Judge element positioning way, and returns the element.

        Usage:
        self.driver.get_element('id->kw')
        """
        if "->" not in css:
            raise NameError("Positioning syntax errors, lack of '->'.")

        by = css.split("->")[0]
        value = css.split("->")[1]

        if by == "id":
            element = self.driver.find_element_by_id(value)
        elif by == "name":
            element = self.driver.find_element_by_name(value)
        elif by == "class":
            element = self.driver.find_element_by_class_name(value)
        elif by == "link_text":
            element = self.driver.find_element_by_link_text(value)
        elif by == "xpath":
            element = self.driver.find_element_by_xpath(value)
        elif by == "css":
            element = self.driver.find_element_by_css_selector(value)
        else:
            raise NameError("Please enter the correct targeting elements,'id','name','class','link_text','xpaht','css'.")
        return element

    def open(self, url):
        """
        open url.

        Usage:
        self.driver.open("https://www.baidu.com")
        """
        t1 = time.time()
        try:
            self.driver.get(url)
            Log().info("{0} Navigated to {1}, Spend {2} seconds".format(success,url,time.time()-t1))
        except Exception:
            Log().info("{0} Unable to load {1}, Spend {2} seconds".format(fail, url, time.time() - t1))
            raise

    def max_window(self):
        """
        Set browser window maximized.

        Usage:
        self.driver.max_window()
        """
        t1 = time.time()
        self.driver.maximize_window()
        Log().info("{0} Set browser window maximized, Spend {1} seconds".format(success, time.time() - t1))

    def set_window(self, wide, high):
        """
        Set browser window wide and high.

        Usage:
        self.driver.set_window(wide,high)
        """
        t1 = time.time()
        self.driver.set_window_size(wide, high)
        Log().info("{0} Set browser window wide: {1},high: {2}, Spend {3} seconds".format(success,
            wide,high,time.time() - t1))

    def type(self, css, text):
        """
        Operation input box.

        Usage:
        self.driver.type("id->kw","selenium")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            el.send_keys(text)
            Log().info("{0} Typed element: <{1}> content: {2}, Spend {3} seconds".format(success,
                css,text,time.time() - t1))
        except Exception:
            Log().info("{0} Unable to type element: <{1}> content: {2}, Spend {3} seconds".format(fail,
                css, text, time.time() - t1))
            raise

    def clear_type(self, css, text):
        """
        Clear and input element.

        Usage:
        self.driver.clear_type("id->kw","selenium")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            el.clear()
            el.send_keys(text)
            Log().info("{0} Clear and type element: <{1}> content: {2}, Spend {3} seconds".format(success,
                css, text,time.time() - t1))
        except Exception:
            Log().info("{0} Unable to clear and type element: <{1}> content: {2}, Spend {3} seconds".format(fail,
                css, text,time.time() - t1))
            raise

    def click(self, css):
        """
        It can click any text / image can be clicked
        Connection, check box, radio buttons, and even drop-down box etc..

        Usage:
        self.driver.click("id->kw")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            el.click()
            Log().info("{0} Clicked element: <{1}>, Spend {2} seconds".format(success,css,time.time() - t1))
        except Exception:
            Log().info("{0} Unable to click element: <{1}>, Spend {2} seconds".format(fail, css, time.time() - t1))
            raise

    def right_click(self, css):
        """
        Right click element.

        Usage:
        self.driver.right_click("id->kw")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            ActionChains(self.driver).context_click(el).perform()
            Log().info("{0} Right click element: <{1}>, Spend {2} seconds".format(success, css, time.time() - t1))
        except Exception:
            Log().info("{0} Unable to right click element: <{1}>, Spend {2} seconds".format(fail, css, time.time() - t1))
            raise

    def move_to_element(self, css):
        """
        Mouse over the element.

        Usage:
        self.driver.move_to_element("id->kw")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            ActionChains(self.driver).move_to_element(el).perform()
            Log().info("{0} Move to element: <{1}>, Spend {2} seconds".format(success, css, time.time() - t1))
        except Exception:
            Log().info("{0} unable move to element: <{1}>, Spend {2} seconds".format(fail, css, time.time() - t1))
            raise

    def double_click(self, css):
        """
        Double click element.

        Usage:
        self.driver.double_click("id->kw")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            ActionChains(self.driver).double_click(el).perform()
            Log().info("{0} Double click element: <{1}>, Spend {2} seconds".format(success, css, time.time() - t1))
        except Exception:
            Log().info("{0} Unable to double click element: <{1}>, Spend {2} seconds".format(fail, css, time.time() - t1))
            raise

    def drag_and_drop(self, el_css, ta_css):
        """
        Drags an element a certain distance and then drops it.

        Usage:
        self.driver.drag_and_drop("id->kw","id->su")
        """
        t1 = time.time()
        try:
            self.element_wait(el_css)
            element = self.get_element(el_css)
            self.element_wait(ta_css)
            target = self.get_element(ta_css)
            ActionChains(self.driver).drag_and_drop(element, target).perform()
            Log().info("{0} Drag and drop element: <{1}> to element: <{2}>, Spend {3} seconds".format(success,
                el_css,ta_css, time.time() - t1))
        except Exception:
            Log().info("{0} Unable to drag and drop element: <{1}> to element: <{2}>, Spend {3} seconds".format(fail,
                el_css, ta_css, time.time() - t1))
            raise

    def click_text(self, text):
        """
        Click the element by the link text

        Usage:
        self.driver.click_text("新闻")
        """
        t1 = time.time()
        try:
            self.driver.find_element_by_partial_link_text(text).click()
            Log().info("{0} Click by text content: {1}, Spend {2} seconds".format(success, text,time.time() - t1))
        except Exception:
            Log().info("{0} Unable to Click by text content: {1}, Spend {2} seconds".format(fail, text, time.time() - t1))
            raise

    def close(self):
        """
        Simulates the user clicking the "close" button in the titlebar of a popup
        window or tab.

        Usage:
        self.driver.close()
        """
        t1 = time.time()
        self.driver.close()
        Log().info("{0} Closed current window, Spend {1} seconds".format(success, time.time() - t1))

    def quit(self):
        """
        Quit the self.driver and close all the windows.

        Usage:
        self.driver.quit()
        """
        t1 = time.time()
        self.driver.quit()
        Log().info("{0} Closed all window and quit the driver, Spend {1} seconds".format(success, time.time() - t1))

    def submit(self, css):
        """
        Submit the specified form.

        Usage:
        self.driver.submit("id->kw")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            el = self.get_element(css)
            el.submit()
            Log().info("{0} Submit form args element: <{1}>, Spend {2} seconds".format(success,css, time.time() - t1))
        except Exception:
            Log().info("{0} Unable to submit form args element: <{1}>, Spend {2} seconds".format(fail, css, time.time() - t1))
            raise

    def F5(self):
        """
        Refresh the current page.

        Usage:
        self.driver.F5()
        """
        t1 = time.time()
        self.driver.refresh()
        Log().info("{0} Refresh the current page, Spend {1} seconds".format(success, time.time() - t1))

    def js(self, script):
        """
        Execute JavaScript scripts.

        Usage:
        self.driver.js("window.scrollTo(200,1000);")
        """
        t1 = time.time()
        try:
            self.driver.execute_script(script)
            Log().info("{0} Execute javascript scripts: {1}, Spend {2} seconds".format(success,script, time.time() - t1))
        except Exception:
            Log().info("{0} Unable to execute javascript scripts: {1}, Spend {2} seconds".format(fail,
                script, time.time() - t1))
            raise

    def get_attribute(self, css, attribute):
        """
        Gets the value of an element attribute.

        Usage:
        self.driver.get_attribute("id->su","href")
        """
        t1 = time.time()
        try:
            el = self.get_element(css)
            attr = el.get_attribute(attribute)
            Log().info("{0} Get attribute element: <{1}>,attribute: {2}, Spend {3} seconds".format(success,
                css,attribute,time.time()-t1))
            return attr
        except Exception:
            Log().info("{0} Unable to get attribute element: <{1}>,attribute: {2}, Spend {3} seconds".format(fail,
                css, attribute,time.time() - t1))
            raise

    def get_text(self, css):
        """
        Get element text information.

        Usage:
        self.driver.get_text("id->kw")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            text = self.get_element(css).text
            Log().info("{0} Get element text element: <{1}>, Spend {2} seconds".format(success,css,time.time()-t1))
            return text
        except Exception:
            Log().info("{0} Unable to get element text element: <{1}>, Spend {2} seconds".format(fail, css, time.time() - t1))
            raise

    def get_title(self) -> object:
        """
        Get window title.

        Usage:
        self.driver.get_title()
        """

        t1 = time.time()
        title = self.driver.title
        Log().info("{0} Get current window title, Spend {1} seconds".format(success, time.time() - t1))
        return title

    def get_url(self):
        """
        Get the URL address of the current page.

        Usage:
        self.driver.get_url()
        """
        t1 = time.time()
        url = self.driver.current_url
        Log().info("{0} Get current window url, Spend {1} seconds".format(success, time.time() - t1))
        return url

    def wait(self, secs):
        """
        Implicitly wait.All elements on the page.

        Usage:
        self.driver.wait(10)
        """
        t1 = time.time()
        self.driver.implicitly_wait(secs)
        Log().info("{0} Set wait all element display in {1} seconds, Spend {2} seconds".format(success,
            secs,time.time() - t1))

    def accept_alert(self):
        """
        Accept warning box.

        Usage:
        self.driver.accept_alert()
        """
        t1 = time.time()
        self.driver.switch_to.alert.accept()
        Log().info("{0} Accept warning box, Spend {1} seconds".format(success, time.time() - t1))

    def dismiss_alert(self):
        """
        Dismisses the alert available.

        Usage:
        self.driver.dismiss_alert()
        """
        t1 = time.time()
        self.driver.switch_to.alert.dismiss()
        Log().info("{0} Dismisses the alert available, Spend {1} seconds".format(success, time.time() - t1))

    def switch_to_frame(self, css):
        """
        Switch to the specified frame.

        Usage:
        self.driver.switch_to_frame("id->kw")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            iframe_el = self.get_element(css)
            self.driver.switch_to.frame(iframe_el)
            Log().info("{0} Switch to frame element: <{1}>, Spend {2} seconds".format(success,css, time.time() - t1))
        except Exception:
            Log().info("{0} Unable switch to frame element: <{1}>, Spend {2} seconds".format(fail, css, time.time() - t1))
            raise

    def switch_to_frame_out(self):
        """
        Returns the current form machine form at the next higher level.
        Corresponding relationship with switch_to_frame () method.

        Usage:
        self.driver.switch_to_frame_out()
        """
        t1 = time.time()
        self.driver.switch_to.default_content()
        Log().info("{0} Switch to frame out, Spend {1} seconds".format(success, time.time() - t1))

    def open_new_window(self, css):
        """
        Open the new window and switch the handle to the newly opened window.

        Usage:
        self.driver.open_new_window("id->kw")
        """
        t1 = time.time()
        try:
            original_windows = self.driver.current_window_handle
            el = self.get_element(css)
            el.click()
            all_handles = self.driver.window_handles
            for handle in all_handles:
                if handle != original_windows:
                    self.driver.switch_to.window(handle)
            Log().info("{0} Click element: <{1}> open a new window and swich into, Spend {2} seconds".format(success,
                css,time.time() - t1))
        except Exception:
            Log().info("{0} Click element: <{1}> open a new window and swich into, Spend {2} seconds".format(fail,
                css,time.time() - t1))
            raise

    def element_exist(self, css):
        """
        judge element is exist,The return result is true or false.

        Usage:
        self.driver.element_exist("id->kw")
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            Log().info("{0} Element: <{1}> is exist, Spend {2} seconds".format(success,css, time.time() - t1))
            return True
        except TimeoutException:
            Log().info("{0} Element: <{1}> is not exist, Spend {2} seconds".format(fail, css, time.time() - t1))
            return False

    def take_screenshot(self, file_path):
        """
        Get the current window screenshot.

        Usage:
        self.driver.take_screenshot('c:/test.png')
        """
        t1 = time.time()
        try:
            self.driver.get_screenshot_as_file(file_path)
            Log().info("{0} Get the current window screenshot,path: {1}, Spend {2} seconds".format(success,
                file_path, time.time() - t1))
        except Exception:
            Log().info("{0} Unable to get the current window screenshot,path: {1}, Spend {2} seconds".format(fail,
                file_path,time.time() - t1))
            raise

    def into_new_window(self):
        """
        Into the new window.

        Usage:
        dirver.into_new_window()
        """
        t1 = time.time()
        try:
            all_handle = self.driver.window_handles
            flag = 0
            while len(all_handle) < 2:
                time.sleep(1)
                all_handle = self.driver.window_handles
                flag += 1
                if flag == 5:
                    break
            self.driver.switch_to.window(all_handle[-1])
            Log().info("{0} Switch to the new window,new window's url: {1}, Spend {2} seconds".format(success,
                self.driver.current_url,time.time() - t1))
        except Exception:
            Log().info("{0} Unable switch to the new window, Spend {1} seconds".format(fail, time.time() - t1))
            raise

    def type_and_enter(self, css, text, secs=0.5):
        """
        Operation input box. 1、input message,sleep 0.5s;2、input ENTER.

        Usage:
        self.driver.type_css_keys('id->kw','beck')
        """
        t1 = time.time()
        try:
            self.element_wait(css)
            ele = self.get_element(css)
            ele.send_keys(text)
            time.sleep(secs)
            ele.send_keys(Keys.ENTER)
            Log().info("{0} Element <{1}> type content: {2},and sleep {3} seconds,input ENTER key, Spend {4} seconds".format(
                success,css,text,secs,time.time() - t1))
        except Exception:
            Log().info("{0} Unable element <{1}> type content: {2},and sleep {3} seconds,input ENTER key, Spend {4} seconds".
                format(fail, css, text, secs, time.time() - t1))
            raise

    def js_click(self, css):
        """
        Input a css selecter,use javascript click element.

        Usage:
        self.driver.js_click('#buttonid')
        """
        t1 = time.time()
        js_str = "$('{0}').click()".format(css)
        try:
            self.driver.execute_script(js_str)
            Log().info("{0} Use javascript click element: {1}, Spend {2} seconds".format(success,js_str,time.time()-t1))
        except Exception:
            Log().info("{0} Unable to use javascript click element: {1}, Spend {2} seconds".format(fail,
                js_str, time.time() - t1))
            raise

    def chrome_download(self,filePath):
        #检查文件是否存在，存在则删除
        if os.path.exists(filePath):
            os.remove(filePath)
        #输入文件保存路径并回车保存
        Keyboards = pykeyboard.PyKeyboard()
        t1 = time.time()
        try:
            Keyboards.type_string(filePath)
            time.sleep(1)
            Keyboards.tap_key(Keyboards.enter_key)
            time.sleep(5)
            Log().info("{0} Chrome DownLoad File,path: {1}, Spend {2} seconds".format(success,filePath, time.time() - t1))
        except Exception:
            Log().info("{0} Chrome DownLoad File,path: {1}, Spend {2} seconds".format(fail,filePath,time.time() - t1))
            raise


