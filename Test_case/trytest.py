import csv
from Package import datainfo

csvValue = datainfo.get_csv_to_dict('E:\AutoTest_WIZData\Data\csvtest.csv')
print(csvValue[0].keys())

