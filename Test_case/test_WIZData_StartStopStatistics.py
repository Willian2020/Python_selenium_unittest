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

class StartStopStatistics(Mytest):

    mydata = datainfo.get_xls_to_dict('WIZData.xlsx', 'DataConfig')
    #启停统计-设备目录列表搜索测试
    @unittest.skipIf(mydata[5]['是否执行'] == 'no', '不执行此用例')
    def test_EquipmentTreeSearch(self):
        eqtName = self.mydata[5]['设备名称']
        #登入大数据产品化系统
        LogIn(self.driver).LoginWIZData(self.mydata[5]['登入用户名'])
        # 进入启停统计页面
        ObjOperate(self.driver).click('class->nav-icon-deviceManage')#点击设备管理主菜单
        time.sleep(2)
        ObjOperate(self.driver).click('xpath->//h4[text()="启停统计"]')#点击启停统计图标
        time.sleep(3)
        #输入设备名称关键字回车，检查列表是否按搜索的设备名称自动选中对应的设备列表名称
        ObjOperate(self.driver).type_and_enter('xpath->//input[@placeholder="输入关键字"]',eqtName)
        time.sleep(2)
        checkPoint = ObjOperate(self.driver).element_exist('xpath->//div[@class="el-tree-node is-current is-focusable"]//span[text()="%s"]' % eqtName)
        self.assertTrue(checkPoint,msg='启停统计页面按关键字搜索设备目录列表失败！')

    # 启停统计-额定运行时间新增、设置、导出历史维护记录测试
    @unittest.skipIf(mydata[6]['是否执行'] == 'no', '不执行此用例')
    def test_RatedRuntime(self):
        eqtName = self.mydata[6]['设备名称']
        downPath = os.path.join(globalparam.data_path,self.mydata[6]['文件名称路径'])
        datalist = self.mydata[6]['数字'].split(';')
        Ldata = int(datalist[0]) + 1

        # 登入大数据产品化系统
        LogIn(self.driver).LoginWIZData(self.mydata[6]['登入用户名'])
        # 进入启停统计页面
        ObjOperate(self.driver).click('class->nav-icon-deviceManage')  # 点击设备管理主菜单
        time.sleep(2)
        ObjOperate(self.driver).click('xpath->//h4[text()="启停统计"]')  # 点击启停统计图标
        time.sleep(3)
        # 输入设备名称关键字回车
        ObjOperate(self.driver).type_and_enter('xpath->//input[@placeholder="输入关键字"]', eqtName)
        time.sleep(2)
        #新增额定运行时间设置
        ObjOperate(self.driver).click('xpath->//div[contains(text(),"额定运行时间")]//span[text()="+"]')
        ObjOperate(self.driver).clear_type('xpath->//div[contains(text(),"额定运行时间")]//span[text()="+"]/following::input[1]',datalist[0])
        #输入额定运行时间后点击设置按钮，设置报警时间与描述等信息
        ObjOperate(self.driver).click('xpath->//div[contains(text(),"额定运行时间")]//span[text()="+"]/following::i[@class="icon-setting"]')
        time.sleep(2)
        #选择上次维护时间为当前时间
        ObjOperate(self.driver).click('xpath->//span[text()="上次维护时间："]/following::input[@placeholder="选择日期时间"]')
        time.sleep(1)
        ObjOperate(self.driver).click('xpath->//div[@class="el-picker-panel__footer"]//span[contains(text(),"此刻")]')
        nowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        time.sleep(1)
        #输入报警值大于额定值
        ObjOperate(self.driver).type('xpath->//input[@placeholder="请输入报警值"]',Ldata)
        #输入报警描述信息
        ObjOperate(self.driver).type('xpath->//span[text()="报警描述："]/following::textarea[@placeholder="请输入内容"]','自动化测试：报警描述')
        #点击保存按钮，检查是否弹出报警值不能大于额定输入值错误提示信息
        ObjOperate(self.driver).click('xpath->//span[text()="保存"]')
        time.sleep(2)
        checkwarning = ObjOperate(self.driver).element_exist('xpath->//div[@class="el-message el-message--warning"]/p[text()="报警值不能大于额定输入值"]')
        self.assertTrue(checkwarning,msg='输入报警值大于额定值保存后系统未弹出警告提示信息！')
        #重新输入小于额定值得报警值，点击保存，检查是否保存成功
        if checkwarning ==  True:
            ObjOperate(self.driver).clear_type('xpath->//input[@placeholder="请输入报警值"]',datalist[1])
            ObjOperate(self.driver).click('xpath->//span[text()="保存"]')
            time.sleep(1)
            checksuccess = ObjOperate(self.driver).element_exist('xpath->//div[@class="el-message el-message--success"]/p[text()="修改成功"]')
            self.assertTrue(checksuccess, msg='输入报警值小于额定值保存后未弹出修改成功提示信息！')

            #导出历史维护记录
            if checksuccess == True:
                #点击设置按钮
                ObjOperate(self.driver).click('xpath->//div[contains(text(),"额定运行时间")]//span[text()="+"]/following::i[@class="icon-setting"]')
                #点击历史维护记录按钮
                ObjOperate(self.driver).click('xpath->//div[@class="content"]//i[@class="history-record"]')
                time.sleep(2)
                #点击导出按钮，下载维护记录数据至本地
                ObjOperate(self.driver).click('xpath->//header[text()="历史维护记录"]/following::span[text()="导出"]')
                time.sleep(2)
                ObjOperate(self.driver).chrome_download(downPath)
                time.sleep(2)
                try:
                    #检查文件是否下载成功
                    self.assertTrue(os.path.exists(downPath),msg='额定运行时间历史维护记录导出失败！')
                    #若文件下载成功，则检查文件字段信息是否与页面修改的内容一致
                    if os.path.exists(downPath) == True:
                        csvData = datainfo.get_csv_to_dict(downPath)
                        #检查文件维护时间是否正确
                        timeList = []
                        for i in range(0,len(csvData)):
                            csvTime = csvData[i]['维护时间']
                            timeList.append(csvTime.split('.')[0])
                        self.assertIn(nowTime,timeList,msg='额定运行时间历史维护记录导出文件中维护时间字段值错误！')
                        #若维护时间在CSV中存在，则检查对应的维护内容信息是否正确
                        if nowTime in timeList:
                            myindex = timeList.index(nowTime)
                            csvText = csvData[myindex]['维护内容']
                            self.assertEqual('自动化测试：报警描述', csvText, msg='额定运行时间历史维护记录导出文件中维护内容字段值错误！')
                finally:
                    #删除历史维护记录
                    ObjOperate(self.driver).click('xpath->//div[@class="el-table__body-wrapper is-scrolling-none"]//span[text()="删除"][1]')
                    time.sleep(1)
                    #检查是否弹出删除成功提示信息
                    checkDel = ObjOperate(self.driver).element_exist('xpath->//div[@class="el-message el-message--success"]/p[text()="删除成功"]')
                    self.assertTrue(checkDel,msg='删除额定运行时间历史维护记录后系统未弹出删除成功提示信息，删除失败！')

    # 启停统计-删除额定运行时间测试
    @unittest.skipIf(mydata[7]['是否执行'] == 'no', '不执行此用例')
    def test_DeleteRatedRuntime(self):
        eqtName = self.mydata[7]['设备名称']
        datalist = self.mydata[7]['数字'].split(';')

        # 登入大数据产品化系统
        LogIn(self.driver).LoginWIZData(self.mydata[7]['登入用户名'])
        # 进入启停统计页面
        ObjOperate(self.driver).click('class->nav-icon-deviceManage')  # 点击设备管理主菜单
        time.sleep(2)
        ObjOperate(self.driver).click('xpath->//h4[text()="启停统计"]')  # 点击启停统计图标
        time.sleep(3)
        # 输入设备名称关键字回车
        ObjOperate(self.driver).type_and_enter('xpath->//input[@placeholder="输入关键字"]', eqtName)
        time.sleep(2)
        # 新增额定运行时间设置
        ObjOperate(self.driver).click('xpath->//div[contains(text(),"额定运行时间")]//span[text()="+"]')
        ObjOperate(self.driver).clear_type(
            'xpath->//div[contains(text(),"额定运行时间")]//span[text()="+"]/following::input[1]', datalist[0])
        # 输入额定运行时间后点击设置按钮，设置报警时间与描述等信息
        ObjOperate(self.driver).click(
            'xpath->//div[contains(text(),"额定运行时间")]//span[text()="+"]/following::i[@class="icon-setting"]')
        time.sleep(2)
        # 选择上次维护时间为当前时间
        ObjOperate(self.driver).click('xpath->//span[text()="上次维护时间："]/following::input[@placeholder="选择日期时间"]')
        time.sleep(1)
        ObjOperate(self.driver).click('xpath->//div[@class="el-picker-panel__footer"]//span[contains(text(),"此刻")]')
        time.sleep(1)
        # 输入报警值
        ObjOperate(self.driver).type('xpath->//input[@placeholder="请输入报警值"]', datalist[1])
        # 输入报警描述信息
        ObjOperate(self.driver).type('xpath->//span[text()="报警描述："]/following::textarea[@placeholder="请输入内容"]',
                                     '自动化测试：报警描述')
        # 点击保存按钮
        ObjOperate(self.driver).click('xpath->//span[text()="保存"]')
        time.sleep(2)
        #检查是否新增设置成功，若成功则进行删除功能验证
        checksuccess = ObjOperate(self.driver).element_exist(
            'xpath->//div[@class="el-message el-message--success"]/p[text()="修改成功"]')
        if checksuccess == True:
            ObjOperate(self.driver).click(
                'xpath->//div[contains(text(),"额定运行时间")]//span[text()="+"]/following::i[@class="icon-del"]')
            time.sleep(1)
            #检查是否删除成功
            checkDelete = ObjOperate(self.driver).element_exist('xpath->//div[@class="el-message el-message--success"]/p[text()="删除成功"]')
            self.assertTrue(checkDelete,msg='删除额定运行时间设置后，系统未弹出删除成功提示信息，删除失败！')
        else:
            raise NameError('新增额定运行时间设置失败，无法进行删除验证！')



    # 启停统计-额定启动次数新增、设置、导出与删除测试
    @unittest.skipIf(mydata[8]['是否执行'] == 'no', '不执行此用例')
    def test_RatedStartCount(self):
        eqtName = self.mydata[8]['设备名称']
        downPath = os.path.join(globalparam.data_path, self.mydata[8]['文件名称路径'])
        datalist = self.mydata[8]['数字'].split(';')
        Ldata = int(datalist[0]) + 1

        # 登入大数据产品化系统
        LogIn(self.driver).LoginWIZData(self.mydata[8]['登入用户名'])
        # 进入启停统计页面
        ObjOperate(self.driver).click('class->nav-icon-deviceManage')  # 点击设备管理主菜单
        time.sleep(2)
        ObjOperate(self.driver).click('xpath->//h4[text()="启停统计"]')  # 点击启停统计图标
        time.sleep(3)
        # 输入设备名称关键字回车
        ObjOperate(self.driver).type_and_enter('xpath->//input[@placeholder="输入关键字"]', eqtName)
        time.sleep(2)
        # 新增额定启动次数设置
        ObjOperate(self.driver).click('xpath->//div[contains(text(),"额定启动次数")]//span[text()="+"]')
        ObjOperate(self.driver).clear_type(
            'xpath->//div[contains(text(),"额定启动次数")]//span[text()="+"]/following::input[1]', datalist[0])
        # 输入额定运行时间后点击设置按钮，设置报警时间与描述等信息
        ObjOperate(self.driver).click(
            'xpath->//div[contains(text(),"额定启动次数")]//span[text()="+"]/following::i[@class="icon-setting"]')
        time.sleep(2)
        # 选择上次维护时间为当前时间
        ObjOperate(self.driver).click('xpath->//span[text()="上次维护时间："]/following::input[@placeholder="选择日期时间"]')
        time.sleep(1)
        ObjOperate(self.driver).click('xpath->//div[@class="el-picker-panel__footer"]//span[contains(text(),"此刻")]')
        nowTime = time.strftime('%Y-%m-%d %H:%M:%S')
        time.sleep(1)
        # 输入报警值大于额定值
        ObjOperate(self.driver).type('xpath->//input[@placeholder="请输入报警值"]', Ldata)
        # 输入报警描述信息
        ObjOperate(self.driver).type('xpath->//span[text()="报警描述："]/following::textarea[@placeholder="请输入内容"]',
                                     '自动化测试：报警描述')
        # 点击保存按钮，检查是否弹出报警值不能大于额定输入值错误提示信息
        ObjOperate(self.driver).click('xpath->//span[text()="保存"]')
        time.sleep(2)
        checkwarning = ObjOperate(self.driver).element_exist(
            'xpath->//div[@class="el-message el-message--warning"]/p[text()="报警值不能大于额定输入值"]')
        self.assertTrue(checkwarning, msg='输入报警值大于额定值保存后系统未弹出警告提示信息！')
        # 重新输入小于额定值得报警值，点击保存，检查是否保存成功
        if checkwarning == True:
            ObjOperate(self.driver).clear_type('xpath->//input[@placeholder="请输入报警值"]', datalist[1])
            ObjOperate(self.driver).click('xpath->//span[text()="保存"]')
            time.sleep(1)
            checksuccess = ObjOperate(self.driver).element_exist(
                'xpath->//div[@class="el-message el-message--success"]/p[text()="修改成功"]')
            self.assertTrue(checksuccess, msg='输入报警值小于额定值保存后未弹出修改成功提示信息！')

            # 导出历史维护记录
            if checksuccess == True:
                # 点击设置按钮
                ObjOperate(self.driver).click(
                    'xpath->//div[contains(text(),"额定启动次数")]//span[text()="+"]/following::i[@class="icon-setting"]')
                # 点击历史维护记录按钮
                ObjOperate(self.driver).click('xpath->//div[@class="content"]//i[@class="history-record"]')
                time.sleep(2)
                # 点击导出按钮，下载维护记录数据至本地
                ObjOperate(self.driver).click('xpath->//header[text()="历史维护记录"]/following::span[text()="导出"]')
                time.sleep(2)
                ObjOperate(self.driver).chrome_download(downPath)
                time.sleep(2)
                # 检查文件是否下载成功
                try:
                    self.assertTrue(os.path.exists(downPath), msg='额定运行时间历史维护记录导出失败！')
                    # 若文件下载成功，则检查文件字段信息是否与页面修改的内容一致
                    if os.path.exists(downPath) == True:
                        csvData = datainfo.get_csv_to_dict(downPath)
                        # 检查文件维护时间是否正确
                        timeList = []
                        for i in range(0, len(csvData)):
                            csvTime = csvData[i]['维护时间']
                            timeList.append(csvTime.split('.')[0])
                        self.assertIn(nowTime, timeList, msg='额定运行时间历史维护记录导出文件中维护时间字段值错误！')
                        # 若维护时间在CSV中存在，则检查对应的维护内容信息是否正确
                        if nowTime in timeList:
                            myindex = timeList.index(nowTime)
                            csvText = csvData[myindex]['维护内容']
                            self.assertEqual('自动化测试：报警描述', csvText, msg='额定运行时间历史维护记录导出文件中维护内容字段值错误！')
                finally:
                    # 删除历史维护记录
                    ObjOperate(self.driver).click(
                        'xpath->//div[@class="el-table__body-wrapper is-scrolling-none"]//span[text()="删除"][1]')
                    time.sleep(1)
                    # 检查是否弹出删除成功提示信息
                    checkDel = ObjOperate(self.driver).element_exist(
                        'xpath->//div[@class="el-message el-message--success"]/p[text()="删除成功"]')
                    self.assertTrue(checkDel, msg='删除额定运行时间后系统未弹出删除成功提示信息，删除失败！')


    # 启停统计-删除额定启动次数测试
    @unittest.skipIf(mydata[9]['是否执行'] == 'no', '不执行此用例')
    def test_DeleteRatedStartCount(self):
        eqtName = self.mydata[9]['设备名称']
        datalist = self.mydata[9]['数字'].split(';')

        # 登入大数据产品化系统
        LogIn(self.driver).LoginWIZData(self.mydata[9]['登入用户名'])
        # 进入启停统计页面
        ObjOperate(self.driver).click('class->nav-icon-deviceManage')  # 点击设备管理主菜单
        time.sleep(2)
        ObjOperate(self.driver).click('xpath->//h4[text()="启停统计"]')  # 点击启停统计图标
        time.sleep(3)
        # 输入设备名称关键字回车
        ObjOperate(self.driver).type_and_enter('xpath->//input[@placeholder="输入关键字"]', eqtName)
        time.sleep(2)
        # 新增额定启动次数设置
        ObjOperate(self.driver).click('xpath->//div[contains(text(),"额定启动次数")]//span[text()="+"]')
        ObjOperate(self.driver).clear_type(
            'xpath->//div[contains(text(),"额定启动次数")]//span[text()="+"]/following::input[1]', datalist[0])
        # 输入额定运行时间后点击设置按钮，设置报警时间与描述等信息
        ObjOperate(self.driver).click(
            'xpath->//div[contains(text(),"额定启动次数")]//span[text()="+"]/following::i[@class="icon-setting"]')
        time.sleep(2)
        # 选择上次维护时间为当前时间
        ObjOperate(self.driver).click('xpath->//span[text()="上次维护时间："]/following::input[@placeholder="选择日期时间"]')
        time.sleep(1)
        ObjOperate(self.driver).click('xpath->//div[@class="el-picker-panel__footer"]//span[contains(text(),"此刻")]')
        time.sleep(1)
        # 输入报警值
        ObjOperate(self.driver).type('xpath->//input[@placeholder="请输入报警值"]', datalist[1])
        # 输入报警描述信息
        ObjOperate(self.driver).type('xpath->//span[text()="报警描述："]/following::textarea[@placeholder="请输入内容"]',
                                     '自动化测试：报警描述')
        # 点击保存按钮
        ObjOperate(self.driver).click('xpath->//span[text()="保存"]')
        time.sleep(2)
        # 检查是否新增设置成功，若成功则进行删除功能验证
        checksuccess = ObjOperate(self.driver).element_exist(
            'xpath->//div[@class="el-message el-message--success"]/p[text()="修改成功"]')
        if checksuccess == True:
            ObjOperate(self.driver).click(
                'xpath->//div[contains(text(),"额定启动次数")]//span[text()="+"]/following::i[@class="icon-del"]')
            time.sleep(1)
            # 检查是否删除成功
            checkDelete = ObjOperate(self.driver).element_exist(
                'xpath->//div[@class="el-message el-message--success"]/p[text()="删除成功"]')
            self.assertTrue(checkDelete, msg='删除额定启动次数设置后，系统未弹出删除成功提示信息，删除失败！')
        else:
            raise NameError('新增额定启动次数设置失败，无法进行删除验证！')

    # 启停统计-设备总运行时间、总停运时间统计功能测试
    @unittest.skipIf(mydata[10]['是否执行'] == 'no', '不执行此用例')
    def test_EquipSumStatistics(self):
        eqtName = self.mydata[10]['设备名称']

        # 登入大数据产品化系统
        LogIn(self.driver).LoginWIZData(self.mydata[10]['登入用户名'])
        # 进入启停统计页面
        ObjOperate(self.driver).click('class->nav-icon-deviceManage')  # 点击设备管理主菜单
        time.sleep(2)
        ObjOperate(self.driver).click('xpath->//h4[text()="启停统计"]')  # 点击启停统计图标
        time.sleep(3)
        # 输入设备名称关键字回车
        ObjOperate(self.driver).type_and_enter('xpath->//input[@placeholder="输入关键字"]', eqtName)
        time.sleep(2)
        #获取设备当前运行状态
        runstatus = ObjOperate(self.driver).get_text('xpath->//div[text()="设备当前状态"]/following::div[@class="equip-content"][1]')
        #获取导航设备总运行时间、总停运时间值
        Fsumstart = ObjOperate(self.driver).get_text('xpath->//div[text()="总运行时间"]/following::div[1]')
        Fsumstop = ObjOperate(self.driver).get_text('xpath->//div[text()="总停运时间"]/following::div[1]')
        #等待一分钟后刷新页面，再次获取导航设备总运行时间、总停运时间值
        time.sleep(60)
        ObjOperate(self.driver).F5()
        time.sleep(3)
        Ssumstart = ObjOperate(self.driver).get_text('xpath->//div[text()="总运行时间"]/following::div[1]')
        Ssumstop = ObjOperate(self.driver).get_text('xpath->//div[text()="总停运时间"]/following::div[1]')
        #检查统计数据是否根据设备运行状态正确变化
        try:
            if runstatus == "停止":
                try:
                    self.assertEqual(Fsumstart,Ssumstart,msg='设备停止状态，总运行时间会变化，不符合实际需求！')
                finally:
                    self.assertNotEqual(Fsumstop,Ssumstop,msg='设备停止状态，总停运时间没有随着时间累加！')
            elif runstatus == "启动":
                try:
                    self.assertEqual(Fsumstop,Ssumstop, msg='设备启动状态，总停运时间会变化，不符合实际需求！')
                finally:
                    self.assertNotEqual(Fsumstart,Ssumstart, msg='设备启动状态，总运行时间没有随着时间累加！')
            else:
                raise NameError('页面显示设备运行状态不为启动或停止，状态显示错误！')
        finally:
            # 将鼠标移动至设备总运行时间统计饼状图上
            ObjOperate(self.driver).move_to_element('xpath->//div[text()="设备总运行时间"]/following::div[@class="pieCharts"]')
            time.sleep(1)
            # 检查是否悬浮展示设备总运行时间、总停运时间
            checkPoint = ObjOperate(self.driver).element_exist(
                'xpath->//div[text()="设备总运行时间"]/following::div[@class="pieCharts"]//div[contains(text(),"小时")]')
            self.assertTrue(checkPoint, msg='鼠标悬浮至设备总运行时间饼状图上，未悬浮显示设备总运行统计时间！')
            #若显示悬浮信息，则获取时间值
            if checkPoint == True:
                tableValue = ObjOperate(self.driver).get_text('xpath->//div[text()="设备总运行时间"]/following::div[@class="pieCharts"]//div[contains(text(),"小时")]')
                #检查值是否与导航设备总运行时间一致
                self.assertTrue(Ssumstart in tableValue or Ssumstop in tableValue,msg='设备总运行时间饼状图数据与导航总运行时间统计数据不一致！')

    # 启停统计-设备启停统计数据查询与图表展示功能测试
    @unittest.skipIf(mydata[11]['是否执行'] == 'no', '不执行此用例')
    def test_StartStopStatisticsSearch(self):
        eqtName = self.mydata[11]['设备名称']
        dataList = self.mydata[11]['日期'].split(';')
        # 登入大数据产品化系统
        LogIn(self.driver).LoginWIZData(self.mydata[11]['登入用户名'])
        # 进入启停统计页面
        ObjOperate(self.driver).click('class->nav-icon-deviceManage')  # 点击设备管理主菜单
        time.sleep(2)
        ObjOperate(self.driver).click('xpath->//h4[text()="启停统计"]')  # 点击启停统计图标
        time.sleep(3)
        # 输入设备名称关键字回车
        ObjOperate(self.driver).type_and_enter('xpath->//input[@placeholder="输入关键字"]', eqtName)
        time.sleep(2)
        #选择搜索开始日期与结束日期
        ObjOperate(self.driver).click('xpath->//i[@class="el-input__icon el-range__icon el-icon-time"]')
        time.sleep(2)
        ObjOperate(self.driver).clear_type(
            'xpath->//div[@class="el-date-range-picker__time-header"]//input[@placeholder="开始日期"]',dataList[0])
        time.sleep(1)
        self.driver.find_element_by_xpath('//div[@class="el-date-range-picker__time-header"]//input[@placeholder="结束日期"]').clear()
        time.sleep(1)
        ObjOperate(self.driver).clear_type(
            'xpath->//div[@class="el-date-range-picker__time-header"]//input[@placeholder="结束日期"]', dataList[1])
        time.sleep(1)
        ObjOperate(self.driver).click('xpath->//div[@class="el-picker-panel__footer"]//span[contains(text(),"确定")]')
        time.sleep(1)
        #点击搜索按钮
        ObjOperate(self.driver).click('xpath->//i[@class="el-icon-search"]/following::span[text()="搜索"]')
        time.sleep(3)
        #检查是否查询出指定时间段的启停统计数据
        searchResult = ObjOperate(self.driver).element_exist('xpath->//span[@class="el-table__empty-text" and text()="暂无数据"]')
        if searchResult == False:
            #若成功查询出数据，则获取列表数据的开始日期
            TableValue = ObjOperate(self.driver).get_text('xpath->//tr[@class="el-table__row"][1]/td[@class="el-table_1_column_3  "]/div[1]')
            #将值转换为日期，并与预期的日期进行比较
            try:
                actureDate = datetime.datetime.strptime(TableValue.split(' ')[0],'%Y-%m-%d')
                startDate = datetime.datetime.strptime(dataList[0],'%Y-%m-%d')
                endDate = datetime.datetime.strptime(dataList[1], '%Y-%m-%d')
                self.assertTrue(actureDate>=startDate and actureDate<=endDate,msg='设备启停统计数据按时间段查询失败，结果开始日期不在指定日期范围内！')
            finally:
                #检查是否按搜索结果显示统计柱状图
                ObjOperate(self.driver).move_to_element('xpath->//div[text()="启停次数"]/following::div[@class="ve-histogram"]//canvas[1]')
                time.sleep(1)
                #检查是否悬浮显示统计信息
                self.assertTrue(ObjOperate(self.driver).element_exist(
                    'xpath->//div[@class="ve-histogram"]//div[text()="次数"]'),msg='鼠标停放至启停统计柱状图上未悬浮显示启停统计信息')
        else:
            raise NameError('未查询出设备：%s在时间段：%s至%s的启停统计数据！' %(eqtName,dataList[0],dataList[1]))

    # 启停统计-设备启停统计数据导出功能测试
    @unittest.skipIf(mydata[12]['是否执行'] == 'no', '不执行此用例')
    def test_StartStopStatisticsExport(self):
        eqtName = self.mydata[12]['设备名称']
        dataList = self.mydata[12]['日期'].split(';')
        downPath = os.path.join(globalparam.data_path,self.mydata[12]['文件名称路径'])
        # 登入大数据产品化系统
        LogIn(self.driver).LoginWIZData(self.mydata[12]['登入用户名'])
        # 进入启停统计页面
        ObjOperate(self.driver).click('class->nav-icon-deviceManage')  # 点击设备管理主菜单
        time.sleep(2)
        ObjOperate(self.driver).click('xpath->//h4[text()="启停统计"]')  # 点击启停统计图标
        time.sleep(3)
        # 输入设备名称关键字回车
        ObjOperate(self.driver).type_and_enter('xpath->//input[@placeholder="输入关键字"]', eqtName)
        time.sleep(2)
        # 选择搜索开始日期与结束日期
        ObjOperate(self.driver).click('xpath->//i[@class="el-input__icon el-range__icon el-icon-time"]')
        time.sleep(2)
        ObjOperate(self.driver).clear_type(
            'xpath->//div[@class="el-date-range-picker__time-header"]//input[@placeholder="开始日期"]', dataList[0])
        time.sleep(1)
        self.driver.find_element_by_xpath(
            '//div[@class="el-date-range-picker__time-header"]//input[@placeholder="结束日期"]').clear()
        time.sleep(1)
        ObjOperate(self.driver).clear_type(
            'xpath->//div[@class="el-date-range-picker__time-header"]//input[@placeholder="结束日期"]', dataList[1])
        time.sleep(1)
        ObjOperate(self.driver).click('xpath->//div[@class="el-picker-panel__footer"]//span[contains(text(),"确定")]')
        time.sleep(1)
        # 点击搜索按钮
        ObjOperate(self.driver).click('xpath->//i[@class="el-icon-search"]/following::span[text()="搜索"]')
        time.sleep(3)
        #检查是否搜索出数据
        searchResult = ObjOperate(self.driver).element_exist(
            'xpath->//span[@class="el-table__empty-text" and text()="暂无数据"]')
        if searchResult == False:
            #获取列表数据中的状态、开始日期、结束日期与时长值
            status = ObjOperate(self.driver).get_text('xpath->//tr[@class="el-table__row"][1]/td[@class="el-table_1_column_2  "]/div[1]')
            startDate = ObjOperate(self.driver).get_text('xpath->//tr[@class="el-table__row"][1]/td[@class="el-table_1_column_3  "]/div[1]')
            endDate = ObjOperate(self.driver).get_text('xpath->//tr[@class="el-table__row"][1]/td[@class="el-table_1_column_4  "]/div[1]')
            searchList = ['1',status,startDate,endDate]
            #点击导出按钮，下载数据至本地
            ObjOperate(self.driver).click('xpath->//button[@class="el-button el-button--primary"]/span[text()="导出"]')
            time.sleep(2)
            ObjOperate(self.driver).chrome_download(downPath)
            time.sleep(3)
            #检查文件下载是否成功以及文件信息的准确性
            self.assertTrue(os.path.exists(downPath),msg='启停统计数据导出失败！')
            csvValue = datainfo.get_csv_to_dict(downPath)
            csvList = [csvValue[0]['序号'],csvValue[0]['运行状态'],csvValue[0]['开始时间'],csvValue[0]['结束时间']]
            self.assertEqual(csvList,searchList,msg='启停统计导出文件数据与页面搜索结果信息不一致！')
        else:
            raise NameError('未查询出设备：%s在时间段：%s至%s的启停统计数据,无法进行导出数据验证！' % (eqtName, dataList[0], dataList[1]))




if __name__ == '__main__':
    unittest.main()