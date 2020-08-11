#coding=utf-8
from Package import datainfo
from Package.publicfunction import Mytest
from Package.publicfunction import ObjOperate
from Package.businessfunction import LogIn
import unittest
import time
import datetime
import os
from Config import globalparam

class AlarmScreen(Mytest):

    mydata = datainfo.get_xls_to_dict('WIZData.xlsx', 'DataConfig')
    #报警画面-报警实时占比鼠标悬浮数据展示测试
    @unittest.skipIf(mydata[0]['是否执行'] == 'no', '不执行此用例')
    def test_AlarmRealTimePercent(self):
        #登入大数据产品化系统
        LogIn(self.driver).LoginWIZData(self.mydata[0]['登入用户名'])
        # 进入报警画面页面
        ObjOperate(self.driver).click('class->nav-icon-realTimeWatch')
        time.sleep(1)
        ObjOperate(self.driver).click('xpath->//div[@class="tab"]//li[2]')
        time.sleep(3)
        #鼠标悬停至燃机系统报警实时占比指针上
        ObjOperate(self.driver).move_to_element('xpath->//div[text()="燃机系统"]/following::div[1]')
        time.sleep(1)
        #检查是否悬浮体现该指标占比数据
        checkPoint = ObjOperate(self.driver).element_exist('xpath->//div[@class="ve-gauge"][1]//div[contains(@style,"position: absolute")]')
        self.assertTrue(checkPoint,msg='鼠标悬浮至指针上未悬浮显示报警实时占比数据')



    #报警画面-报警分布数据查询与展示测试
    @unittest.skipIf(mydata[1]['是否执行'] == 'no', '不执行此用例')
    def test_AlarmDistributionSearch(self):
        searchType = self.mydata[1]['查询方式']
        searchTime = self.mydata[1]['日期']
        LogIn(self.driver).LoginWIZData(self.mydata[1]['登入用户名'])
        # 进入报警画面页面
        ObjOperate(self.driver).click('class->nav-icon-realTimeWatch')
        time.sleep(1)
        ObjOperate(self.driver).click('xpath->//div[@class="tab"]//li[2]')
        time.sleep(3)
        #选择查询方式：按天、按周、按月、按年分析
        ObjOperate(self.driver).click('class->el-select')
        time.sleep(1)
        ObjOperate(self.driver).click('xpath->//span[text()="%s"]' %searchType)
        #选择时间
        ObjOperate(self.driver).click('xpath->//i[@class="el-input__icon el-icon-date"]')
        time.sleep(1)
        searchDay = searchTime.split("-")
        if searchType.strip() == '按天分析'or searchType.strip() == '按周分析':
            #选择年、月、日
            ObjOperate(self.driver).click('xpath->//span[@class="el-date-picker__header-label" and contains(text(),"年")]')
            time.sleep(1)
            ObjOperate(self.driver).click('xpath->//table[@class="el-year-table"]//a[text()="%s"]' %searchDay[0])
            ObjOperate(self.driver).click('xpath->//table[@class="el-month-table"]//a[text()="%s"]' %searchDay[1])
            ObjOperate(self.driver).click('xpath->//table[@class="el-date-table"]//span[contains(text(),"%s")]' % searchDay[2])
            time.sleep(1)
        elif searchType.strip() == '按月分析':
            # 选择年、月
            ObjOperate(self.driver).click('xpath->//span[@class="el-date-picker__header-label" and contains(text(),"年")]')
            time.sleep(1)
            ObjOperate(self.driver).click('xpath->//table[@class="el-year-table"]//a[text()="%s"]' % searchDay[0])
            ObjOperate(self.driver).click('xpath->//table[@class="el-month-table"]//a[text()="%s"]' % searchDay[1])
        elif searchType.strip() == '按年分析':
            # 选择年份
            ObjOperate(self.driver).click('xpath->//span[@class="el-date-picker__header-label" and contains(text(),"年")]')
            time.sleep(1)
            ObjOperate(self.driver).click('xpath->//table[@class="el-year-table"]//a[text()="%s"]' % searchDay[0])
        else:
            raise NameError('指定的数据查询方式有误，请检查数据表相应数据是否正确！')
        #点击搜索按钮
        ObjOperate(self.driver).click('xpath->//span[text()="搜索"]')
        time.sleep(3)
        try:
            #检查是否正常展示相应的星状图表
            checkStarTable = ObjOperate(self.driver).element_exist('xpath->//div[@class="ve-radar"]//canvas[@data-zr-dom-id="zr_0"]')
            self.assertTrue(checkStarTable,msg='报警分布数据查询失败，未展示相应的星状数据图表')
        finally:
            #切换图标为柱状图
            ObjOperate(self.driver).click('xpath->//span[@class="icon icon-histogram active"]')
            time.sleep(3)
            #将鼠标移动至柱状图上
            ObjOperate(self.driver).move_to_element('class->ve-histogram')
            time.sleep(1)
            #检查是否悬浮展示数据信息
            checkHistogram = ObjOperate(self.driver).element_exist('xpath->//div[@class="ve-histogram"]//div[contains(@style,"position: absolute")]')
            self.assertTrue(checkHistogram,msg='报警分布数据查询使用柱状图显示，鼠标悬停至图标上未悬浮显示相应数据信息')



    #报警画面-实时定值报警数据查询测试
    @unittest.skipIf(mydata[2]['是否执行'] == 'no', '不执行此用例')
    def test_AlarmRealTimeDataSearch(self):
        searchName = self.mydata[2]['设备名称']
        searchDate = self.mydata[2]['日期'].split("-")
        searchKKS = self.mydata[2]['测点']
        alarmType = self.mydata[2]['报警类型']
        LogIn(self.driver).LoginWIZData(self.mydata[2]['登入用户名'])
        # 进入报警画面页面
        ObjOperate(self.driver).click('class->nav-icon-realTimeWatch')
        time.sleep(1)
        ObjOperate(self.driver).click('xpath->//div[@class="tab"]//li[2]')
        time.sleep(3)
        try:
            #选择实时定值报警列表中的报警时间并搜索，检查数据是否按时间筛选
            ObjOperate(self.driver).click('xpath->//span[@class="time-icon table-icon"]')
            ObjOperate(self.driver).click('xpath->//div[@class="alarm-dz"]//i[@class="el-input__icon el-icon-date"]')
            time.sleep(1)
            # 选择年、月、日
            ObjOperate(self.driver).click('xpath->//span[@class="el-date-picker__header-label" and contains(text(),"年")]')
            time.sleep(1)
            ObjOperate(self.driver).click('xpath->//table[@class="el-year-table"]//a[text()="%s"]' % searchDate[0])
            ObjOperate(self.driver).click('xpath->//table[@class="el-month-table"]//a[text()="%s"]' % searchDate[1])
            ObjOperate(self.driver).click('xpath->//table[@class="el-date-table"]//span[contains(text(),"%s")]' % searchDate[2])
            ObjOperate(self.driver).click('xpath->//button[@class="el-button el-button--primary"]/span[contains(text(),"确定")]')
            time.sleep(3)
            #获取第一行第一列的报警时间值,并转换为日期
            actureDate_cell=ObjOperate(self.driver).get_element('xpath->//tbody/tr[@class="el-table__row thirdAlarm"][1]/td[@class="el-table_1_column_1  "]/div[1]').text
            actureDate = datetime.datetime.strptime(actureDate_cell.split(" ")[0],'%Y-%m-%d')
            #将搜索输入的时间字符串转换为日期
            daydicts={'一月':'01','二月':'02','三月':'03','四月':'04','五月':'05','六月':'06','七月':'07','八月':'08','九月':'09','十月':'10','十一月':'11','十二月':'12'}
            mysearchDate = datetime.datetime.strptime(searchDate[0] + '-' + daydicts[searchDate[1]] + '-' + searchDate[2],'%Y-%m-%d')
            #检查查询出的数据日期是否大于等于输入的日期
            self.assertTrue(actureDate >= mysearchDate,msg='实时定值报警列表按时间筛选数据失败！')
        finally:
            try:
                #通过设备名称搜索数据
                #输入设备名称，点击确定按钮
                ObjOperate(self.driver).click('xpath->//span[@class="devicename-icon table-icon"]')
                ObjOperate(self.driver).type('xpath->//input[@placeholder="请输入设备名称"]',searchName)
                ObjOperate(self.driver).click('xpath->//button[@class="el-button el-button--primary"]/span[contains(text(),"确定")]')
                time.sleep(3)
                #获取第一行数据的设备名称值
                actureName = ObjOperate(self.driver).get_element('xpath->//tbody/tr[@class="el-table__row thirdAlarm"][1]/td[@class="el-table_1_column_2  "]/div[1]').text
                #检查实际的设备名称与搜索输入的设备名称是否一致
                self.assertTrue(searchName == actureName,msg='实时定值报警列表按设备名称筛选数据失败')
            finally:
                try:
                    #通过测点名称搜索数据
                    ObjOperate(self.driver).click('xpath->//span[@class="kkscode-icon table-icon"]')
                    ObjOperate(self.driver).type('xpath->//input[@placeholder="请输入测点"]', searchKKS)
                    ObjOperate(self.driver).click('xpath->//button[@class="el-button el-button--primary"]/span[contains(text(),"确定")]')
                    time.sleep(3)
                    #获取第一行数据的测点名称值
                    actureKKS = ObjOperate(self.driver).get_element('xpath->//tbody/tr[@class="el-table__row thirdAlarm"][1]/td[@class="el-table_1_column_3  "]/div[1]').text
                    #检查实际测点名称是否与搜索输入的值一致
                    self.assertIn(searchKKS,actureKKS,msg='实时定值报警列表按测点名称筛选数据失败')
                finally:
                    #通过报警类型搜索数据
                    ObjOperate(self.driver).click('xpath->//span[@class="alarmtype-icon table-icon"]')
                    ObjOperate(self.driver).click('xpath->//div[@class="item-content-select alarm-dz alarmType"]//span[@class="el-input__suffix-inner"]')
                    time.sleep(1)
                    ObjOperate(self.driver).click('xpath->//div[@class="el-scrollbar"]//span[text()="%s"]' % alarmType)
                    time.sleep(3)
                    #获取第一行数据的报警类型值
                    actureAlarmType = ObjOperate(self.driver).get_element(
                        'xpath->//tbody/tr[@class="el-table__row thirdAlarm"][1]/td[@class="el-table_1_column_7  "]/div[1]').text
                    #检查数据是否按报警类型搜索成功
                    self.assertEqual(alarmType,actureAlarmType,msg='实时定值报警列表按报警类型筛选数据失败')
                    self.ass



    #报警画面-测点报警信息查询展示与统计导出测试
    @unittest.skipIf(mydata[3]['是否执行'] == 'no', '不执行此用例')
    def test_AlarmRealTimeKKSViewAndExport(self):
        searchDate = self.mydata[3]['日期'].split("-")
        searchKKS = self.mydata[3]['测点']
        downPath = os.path.join(globalparam.data_path,self.mydata[3]['文件名称路径'])
        LogIn(self.driver).LoginWIZData(self.mydata[2]['登入用户名'])
        # 进入报警画面页面
        ObjOperate(self.driver).click('class->nav-icon-realTimeWatch')
        time.sleep(1)
        ObjOperate(self.driver).click('xpath->//div[@class="tab"]//li[2]')
        time.sleep(3)

        # 选择实时定值报警列表中的报警时间
        ObjOperate(self.driver).click('xpath->//span[@class="time-icon table-icon"]')
        ObjOperate(self.driver).click('xpath->//div[@class="alarm-dz"]//i[@class="el-input__icon el-icon-date"]')
        time.sleep(1)
        # 选择年、月、日
        ObjOperate(self.driver).click('xpath->//span[@class="el-date-picker__header-label" and contains(text(),"年")]')
        time.sleep(1)
        ObjOperate(self.driver).click('xpath->//table[@class="el-year-table"]//a[text()="%s"]' % searchDate[0])
        ObjOperate(self.driver).click('xpath->//table[@class="el-month-table"]//a[text()="%s"]' % searchDate[1])
        ObjOperate(self.driver).click('xpath->//table[@class="el-date-table"]//span[contains(text(),"%s")]' % searchDate[2])
        ObjOperate(self.driver).click('xpath->//button[@class="el-button el-button--primary"]/span[contains(text(),"确定")]')
        time.sleep(1)
        # 输入测点名称搜索数据
        ObjOperate(self.driver).click('xpath->//span[@class="kkscode-icon table-icon"]')
        ObjOperate(self.driver).type('xpath->//input[@placeholder="请输入测点"]', searchKKS)
        ObjOperate(self.driver).click('xpath->//button[@class="el-button el-button--primary"]/span[contains(text(),"确定")]')
        time.sleep(3)
        #单击报警列表中的数据
        ObjOperate(self.driver).click('xpath->//tbody/tr[@class="el-table__row thirdAlarm"][1]/td[@class="el-table_1_column_3  "]/div[1]')
        time.sleep(3)
        #检查是否弹出报警测点信息页签
        checkTab = ObjOperate(self.driver).element_exist('xpath->//header[text()="报警测点信息"]')
        self.assertTrue(checkTab,msg='点击报警列表数据，系统未弹出报警测点信息详情页面！')
        #若弹出测点详情页面，则继续检查相关信息是否正确
        if checkTab == True:
            try:
                #获取详情页面测点名称值，并检查是否与搜索的测点名称一致
                detailKKS = ObjOperate(self.driver).element_exist('xpath->//div[@class="tab-content"]//div[@class="cell" and contains(text(),"%s")]' % searchKKS)
                self.assertTrue(detailKKS,msg='报警测点信息页面测点名称值与实时定值列表中的测点名称不一致！')
            finally:
                try:
                    #测点报警按报警次数统计功能检查
                    ObjOperate(self.driver).click('xpath->//button[@class="el-button el-button--primary"]/span[text()="报警次数统计"]')
                    time.sleep(2)
                    checkAlarmCount = ObjOperate(self.driver).element_exist('xpath->//header[text()="报警次数统计"]')
                    self.assertTrue(checkAlarmCount,msg='测点报警信息按报警次数统计功能异常！')
                    #测点报警按报警时长统计功能检查
                    if checkAlarmCount==True:
                        ObjOperate(self.driver).click('xpath->//header[text()="报警次数统计"]/span[@class="dialog-close"]')#关闭按次数统计窗口
                        time.sleep(1)
                finally:
                    try:
                        #点击按时长统计按钮，检查功能是否正常
                        ObjOperate(self.driver).click('xpath->//button[@class="el-button el-button--primary"]/span[text()="累计报警时长统计"]')
                        time.sleep(3)
                        checkAlarmTime = ObjOperate(self.driver).element_exist('xpath->//header[text()="累计报警时长统计"]')
                        self.assertTrue(checkAlarmTime, msg='测点报警信息按报警时长统计功能异常！')
                        if checkAlarmTime==True:
                            ObjOperate(self.driver).click('xpath->//header[text()="累计报警时长统计"]/span[@class="dialog-close"]')
                            time.sleep(1)
                    finally:
                        #导出测点报警信息
                        ObjOperate(self.driver).click('xpath->//div[@class="tab-content"]//span[text()="导出"]')
                        time.sleep(3)
                        #输入文件保存路径后回车保存
                        ObjOperate(self.driver).chrome_download(downPath)
                        #检查文件是否成功下载至本地
                        self.assertTrue(os.path.exists(downPath),msg='测点报警信息导出后文件未成功下载至本地!')
                        #若下载成功，则检查文件字段信息是否正确
                        if os.path.exists(downPath) == True:
                            KKSFileValueList = datainfo.get_xls_to_dict(self.mydata[3]['文件名称路径'], 'Sheet1')
                            KKSName = KKSFileValueList[0]['测点kks']
                            self.assertIn(searchKKS,KKSName,msg='测点报警信息导出文件中的字段值错误！')



    #报警画面-实时定值报警列表数据导出测试
    @unittest.skipIf(mydata[4]['是否执行'] == 'no', '不执行此用例')
    def test_AlarmRealTimeDataExport(self):
        searchDate = self.mydata[4]['日期'].split("-")
        searchName = self.mydata[4]['设备名称']
        downPath = os.path.join(globalparam.data_path,self.mydata[4]['文件名称路径'])
        LogIn(self.driver).LoginWIZData(self.mydata[4]['登入用户名'])
        # 进入报警画面页面
        ObjOperate(self.driver).click('class->nav-icon-realTimeWatch')
        time.sleep(1)
        ObjOperate(self.driver).click('xpath->//div[@class="tab"]//li[2]')
        time.sleep(3)

        # 选择实时定值报警列表中的报警时间
        ObjOperate(self.driver).click('xpath->//span[@class="time-icon table-icon"]')
        ObjOperate(self.driver).click('xpath->//div[@class="alarm-dz"]//i[@class="el-input__icon el-icon-date"]')
        time.sleep(1)
        # 选择年、月、日
        ObjOperate(self.driver).click('xpath->//span[@class="el-date-picker__header-label" and contains(text(),"年")]')
        time.sleep(1)
        ObjOperate(self.driver).click('xpath->//table[@class="el-year-table"]//a[text()="%s"]' % searchDate[0])
        ObjOperate(self.driver).click('xpath->//table[@class="el-month-table"]//a[text()="%s"]' % searchDate[1])
        ObjOperate(self.driver).click('xpath->//table[@class="el-date-table"]//span[contains(text(),"%s")]' % searchDate[2])
        ObjOperate(self.driver).click('xpath->//button[@class="el-button el-button--primary"]/span[contains(text(),"确定")]')
        time.sleep(1)
        # 输入设备名称，点击确定按钮
        ObjOperate(self.driver).click('xpath->//span[@class="devicename-icon table-icon"]')
        ObjOperate(self.driver).type('xpath->//input[@placeholder="请输入设备名称"]', searchName)
        ObjOperate(self.driver).click('xpath->//button[@class="el-button el-button--primary"]/span[contains(text(),"确定")]')
        time.sleep(3)
        #点击导出按钮，导出报警列表数据至本地
        ObjOperate(self.driver).click('xpath->//span[@class="icon-export icon-small"]')
        time.sleep(1)
        ObjOperate(self.driver).chrome_download(downPath)
        # 检查文件是否成功下载至本地
        self.assertTrue(os.path.exists(downPath), msg='实时定值报警列表数据导出后文件未成功下载至本地!')
        # 若下载成功，则检查文件字段信息是否正确
        if os.path.exists(downPath) == True:
            FileValueList = datainfo.get_csv_to_dict(downPath)
            Devicename = FileValueList[0]['设备名称']
            self.assertEqual(Devicename,searchName,msg='实时定值报警列表数据导出文件信息错误！')



if __name__ == '__main__':
    unittest.main()