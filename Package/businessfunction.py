from Package import datainfo
from Package.publicfunction import ObjOperate
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

class LogIn():
    def __init__(self,seleniumdriver):
        self.driver = seleniumdriver

    def LoginWIZData(self, usrname):
        logindata = datainfo.get_xls_to_dict('WIZData.xlsx', 'LogInfo')
        for i in range(0, len(logindata)):
            if logindata[i]['用户名'] == usrname:
                password = logindata[i]['密码']
                siteadress = logindata[i]['URL']
                self.driver.get(siteadress)
                time.sleep(3)
             #   ObjOperate(self.driver).clear_type('id->username',usrname)
             #   ObjOperate(self.driver).clear_type('id->password',password)
             #   ObjOperate(self.driver).click('id->submit')
             #   time.sleep(3)
                break
            else:
                raise NameError('未匹配到指定的用户名，请检查数据配置文件！')




