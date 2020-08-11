#coding=utf-8
from Package import HTMLTestRunner
import os
import unittest
import time
#设置报告文件存放位置
report_path = os.path.dirname(os.path.abspath('.')) + '/Report/'
#获取当前系统时间
now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
#设置碰撞报告名称格式
HtmlFile = report_path + now + "HTMLtemplate.html"
fp = open(HtmlFile, "web")

suite = unittest.TestLoader().discover("Test_case")
if __name__ == '__main__':
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title="WizData项目测试报告",description="用例测试情况")
    runner.run(suite)

