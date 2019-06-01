# coding: utf-8
import urllib3
import requests
import pymysql
import json
import time
import random
import re
from gaotie_price import *
from gaotie_station import  *
from  gaotie_no import *
from save_highway_data import *
from gaotie_code import *
def getGaoTieLine(fs_code ,ts_code,date,stations,stationsReverse):
    #获取车次主要信息页的基本信息
    url = ('https://kyfw.12306.cn/otn/leftTicket/query?'
           'leftTicketDTO.train_date={}&'
           'leftTicketDTO.from_station={}&'
           'leftTicketDTO.to_station={}&'
           'purpose_codes=ADULT').format(date,fs_code, ts_code)
    db = connectOnly()
    table_name = fs_code.lower() + "_" + ts_code.lower()#表名是小写的，而url是大写的
    if isNull(db, table_name):
        CreateTable(fs_code.lower(), ts_code.lower())
        requests.packages.urllib3.disable_warnings()
        r = requests.get(url, verify=False)
        # print(r.json())
        # 　　requests得到的是一个json格式的对象，ｒ.json()转化成python字典格式数据来提取，所有的车次结果result
        r.encoding = 'utf-8'
        raw_trains = r.json()['data']['result']
        for raw_train in raw_trains:
            info = {}
            # split切割之后得到的是一个列表
            data_list = raw_train.split("|")
            train_code = data_list[2]
            info['train_no'] = data_list[3]
            initial = info['train_no'][0].lower()
            info['from_station_code'] = data_list[6]
            info['to_station_code'] = data_list[7]
            info['from_station_name'] = stationsReverse[info['from_station_code']]
            info['to_station_name'] = stationsReverse[info['to_station_code']]
            info['start_time'] = data_list[8]
            info['arrive_time'] = data_list[9]
            info['time_duration'] = data_list[10]
            first_class_seat = data_list[31] or "--"
            second_class_seat = data_list[30] or "--"
            soft_sleep = data_list[23] or "--"
            hard_sleep = data_list[28] or "--"
            hard_seat = data_list[29] or "--"
            no_seat = data_list[33] or "--"
            if(initial == 'g'):
                prices = computePrice(train_code,info['from_station_code'], info['to_station_code'],date,stations,stationsReverse)
                info['TeDengSeat'] = prices.get('A9','---')
                info['FirstSeat'] = prices.get('M','---')
                info['SecondSeat'] = prices.get('O','---')
                saveData(db, info, stationsReverse,fs_code,ts_code)

def computePrice(train_code, from_station_code, to_station_code,date,stations,stationsReverse):
    #通过列车号和经停站顺序计算价格
    fs_name = stationsReverse[from_station_code]
    ts_name = stationsReverse[to_station_code]
    se = random.randint(10,20)
    time.sleep(se)
    number = getCityNumber(train_code , from_station_code, to_station_code ,date)
    if(fs_name in number.keys()):
        print(number)
    else:
        return {'A9':'---','M':'---','O':'---'}
    fs_no = number[fs_name]#可能报keyerror的错
    ts_no = number[ts_name]
    second = random.randint(15,25)
    time.sleep(second)
    print(ts_name)
    prices = getThreePrice(train_code, fs_no, ts_no,date)
    return prices

def main():
    stations,stationsReverse = getTelecode()
    date = "2019-06-02"
    for fs_code in ['TJP', 'CCT', 'CDW', 'CSQ', 'FZS', 'GIW', 'GZQ', 'HBB', 'HFH' 'HZH',
                   'JNK',  'KMM']:
        for ts_code in spider_city_Reverse.keys():
            if(ts_code != fs_code):
                getGaoTieLine(fs_code, ts_code, date, stations,stationsReverse)

if __name__ == "__main__":
    main()