#coding=utf-8

import codecs
import os
import xlrd
from Config import globalparam
import csv

data_path = globalparam.data_path
def get_xls_to_dict(xlsname, sheetname):
    """
    读取excel表结果为dict
    第一行为字典的key，下面的为值
    return [{'title':'1','user':'root'},{'title':'2','user':'xiaoshitou'}]
    """
    datapath = os.path.join(data_path,xlsname)
    xls1 = xlrd.open_workbook(datapath)
    table = xls1.sheet_by_name(sheetname)
    dataresult = [table.row_values(i) for i in range(0, table.nrows)]
    #将list转化成dict
    result = [ dict(zip(dataresult[0], dataresult[i])) for i in range(1, len(dataresult))]
    return result

def get_url_data(title):
    """
    读取txt文件，转化成dict;读取url和导航栏的对应关系
    将txt转化成一个字典:下单=>/admin/order/index
    {'title1':'url1','下单':'/admin/order/index'}
    """
    name = 'urlsource.txt'
    txtpath = os.path.join(data_path,name)
    with codecs.open(txtpath,'r',encoding='utf-8') as f:
        txtcontent = f.readlines()
    txtdict = dict([txt.strip().replace('\ufeff','').split('=>') for txt in txtcontent])
    return txtdict[title]

def get_xls_to_list(excelname, sheetname):
    """
    读取excel表，返回一个list,只是返回第一列的值
    return [1,2,3,4,5]
    """
    datapath = os.path.join(data_path, excelname)
    excel = xlrd.open_workbook(datapath)
    table = excel.sheet_by_name(sheetname)
    result = [table.row_values(i)[0].strip() for i in range(1,table.nrows)]
    return result

def get_csv_to_dict(csv_path):
    #读取csv文件内容，并通过字典返回数据
    if os.path.exists(csv_path) == True:
        with open(csv_path,'r',encoding='utf-8-sig') as CS:
            csvdata = csv.reader(CS)
            keyname = next(csvdata)
            csv_reader = csv.DictReader(CS,fieldnames=keyname)
            csvlist = []
            for row in csv_reader:
                csvdict = {}
                for k,v in row.items():
                    csvdict[k] = v
                csvlist.append(csvdict)
            return csvlist
    else:
        raise NameError("指定的CSV文件不存在，请检查文件路径是否正确！")



if __name__=='__main__':
    res = get_xls_to_list('addressParse.xlsx','Sheet1')



