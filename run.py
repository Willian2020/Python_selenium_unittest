# coding=utf-8

import unittest
from Package import HTMLTestRunner
import time
from Config import globalparam


def run():
    test_dir = './Test_case'
    suite = unittest.defaultTestLoader.discover(start_dir=test_dir, pattern='test*.py')
    now = time.strftime('%Y-%m-%d_%H_%M_%S')
    reportname = globalparam.report_path + '\\' + 'TestResult' + now + '.html'
    with open(reportname, 'wb') as f:
        runner = HTMLTestRunner.HTMLTestRunner(
            stream=f,
            title='WizData项目测试报告',
            description='Test the import testcase'
        )
        runner.run(suite)
    time.sleep(3)

if __name__ == '__main__':
    run()
