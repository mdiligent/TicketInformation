import json
import time
import random
import re
import pymysql
import requests
from cityAir3code import *
from prettytable import PrettyTable

def getOneWay(decity,arcity,date):
    headers = { "Host": "flights.ctrip.com",
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
               'Referer': 'https://flights.ctrip.com/itinerary/oneway/%s-%s?date=%s' %(city.get(decity).lower(), city.get(arcity).lower(), date),
               'Cookie': '_abtest_userid=d315690a-21ae-4b0b-ab99-e4e07202c9f2; _RSG=rcK.PPiny40nIJ4462DxW9; _RDG=286e7c7313ad3c23900847d4969df6fa96; _RGUID=013cc6c6-59f9-49b5-983b-3421841134b1; _ga=GA1.2.1955894738.1556982612; MKT_Pagesource=PC; gad_city=7ef2d299a82b620d706fcdc362cadd35; _gid=GA1.2.476719946.1558015237; _gac_UA-3748357-1=1.1558015237.CjwKCAjwlPTmBRBoEiwAHqpvhWiCFqoo1BodCN_wdUhJ6VTmMogGS38haLh1amrIUKtkXgdAOdT7oBoCNF4QAvD_BwE; MKT_OrderClick=ASID=4899155989&CT=1558015237369&CURL=https%3A%2F%2Fwww.ctrip.com%2F%3Fsid%3D155989%26allianceid%3D4899%26gclid%3DCjwKCAjwlPTmBRBoEiwAHqpvhWiCFqoo1BodCN_wdUhJ6VTmMogGS38haLh1amrIUKtkXgdAOdT7oBoCNF4QAvD_BwE%26gclsrc%3Daw.ds&VAL={"pc_vid":"1556982608216.ycos5"}; DomesticUserHostCity=TAO|%c7%e0%b5%ba; _gcl_aw=GCL.1558015238.~CjwKCAjwlPTmBRBoEiwAHqpvhWiCFqoo1BodCN_wdUhJ6VTmMogGS38haLh1amrIUKtkXgdAOdT7oBoCNF4QAvD_BwE; _gcl_dc=GCL.1558015238.CjwKCAjwlPTmBRBoEiwAHqpvhWiCFqoo1BodCN_wdUhJ6VTmMogGS38haLh1amrIUKtkXgdAOdT7oBoCNF4QAvD_BwE; appFloatCnt=5; FD_SearchHistorty={"type":"S","data":"S%24%u4E0A%u6D77%28SHA%29%24SHA%242019-05-18%24%u5E7F%u5DDE%28CAN%29%24CAN"}; Session=smartlinkcode=U439101&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; Union=AllianceID=1119&SID=439101&OUID=&Expires=1558658137260; _RF1=117.136.92.102; _bfa=1.1556982608216.ycos5.1.1558053326209.1558055811268.7.33; _bfs=1.4; _jzqco=%7C%7C%7C%7C1558015241839%7C1.104616703.1556982611895.1558055836147.1558055876903.1558055836147.1558055876903.undefined.0.0.31.31; __zpspc=9.7.1558055813.1558055876.4%233%7Cwww.2345.com%7C%7C%7C%7C%23; _bfi=p1%3D10320673302%26p2%3D10320673302%26v1%3D33%26v2%3D32',
               'Origin': 'https://flights.ctrip.com',
               'Connection': 'keep-alive',
                'Content-Type': 'application/json', }
    ParmDict = {"dcity":" ","acity":" ","dcityname":" ","acityname":" ","date":" "}
    ParmDict["dcity"] = city.get(decity)
    ParmDict["acity"] = city.get(arcity)
    ParmDict["dcityname"] = decity
    ParmDict["acityname"] = arcity
    ParmDict["date"] = date
    payload = {"flightWay":"Oneway",
                "classType":"ALL",
                "hasChild":'false',
                "hasBaby":'false',
                "searchIndex":1,
                "portingToken":"3fec6a5a249a44faba1f245e61e2af88",
                "airportParams":[ParmDict]
               }
    request_url = 'https://flights.ctrip.com/itinerary/api/12808/products'
    db = connectOnly()
    Table_Name = ParmDict["dcity"].lower()+"_"+ParmDict["acity"].lower()

    if (isNull(db, Table_Name) == 1):
        second = random.randint(15, 25)#不要请求的太频繁，防止被封
        time.sleep(second)
        #post方法要请求一个json格式的表单
        response = requests.post(request_url,data = json.dumps(payload),headers= headers).text
        routeList = json.loads(response).get('data').get('routeList')
        parseRoute(decity,arcity,routeList)

def parseRoute(decity,arcity,routeList):
    #主要函数，获取航班具体数据
    table = PrettyTable(["Airline", "FlightNumber",'CraftTypeName', 'DepartureCity',"DepartureAirport", "DepartureDate",'ArrivalCity',"ArriveAirport",'ArrivalDate', 'PunctualityRate', 'LowestPrice'])
    num = 0
    if (routeList == None):#防止没有查询到航班数据时出错
        return
    db = CreateTable(decity, arcity)
    for route in routeList:
        if len(route.get('legs')) == 1:
            num += 1
            info = {}
            legs = route.get('legs')[0]
            flight = legs.get('flight')
            if(flight == None):
                continue
            info['Airline'] = flight.get('airlineName')
            info['FlightNumber'] = flight.get('flightNumber')
            info['CraftTypeName'] = flight.get('craftTypeName')
            info['DepartureCity'] = decity
            info['DepartureAirport'] = flight.get('departureAirportInfo').get('airportName')
            info['DepartureDate'] = flight.get('departureDate')#[-8:-3]
            info['ArrivalCity'] = arcity
            info['ArrivalAirport'] = flight.get('arrivalAirportInfo').get('airportName')
            info['ArrivalDate'] = flight.get('arrivalDate')#[-8:-3]
            info['PunctualityRate'] = flight.get('punctualityRate')
            info['LowestPrice'] = legs.get('characteristic').get('lowestPrice')
            saveData(db,info)


            table.add_row(info.values())
    show(table,num)
    db.close()
def connectOnly():
    #只连接到数据库，不做其余操作
    db = pymysql.connect(host="localhost",
                         user="root",
                         port=3306,  # 端口号要为数字而非字符串
                         password="sql666",
                         db="airplane")
    return db

def CreateTable(decity,arcity):
    #创建表
    db = connectOnly()
    Table_Name = city.get(decity)+"_"+city.get(arcity)
    sq1_create_table = """create table if not exists `{table_name}`(
       DepartureCity varchar(50),
       ArrivalCity varchar(50),
       Airline varchar(30),
       FlightNumber varchar(20),
       CraftTypeName varchar(20),
       DepartureAirport varchar(50),
       DepartureDate   varchar(20),
       ArrivalAirport varchar(50),
       ArrivalDate   varchar(20),
       PunctualityRate varchar(10),
       LowestPrice int  )
       """
    cursor = db.cursor()
    cursor.execute(sq1_create_table.format(table_name = Table_Name))
    return db

def saveData(db, info):
    cursor = db.cursor()
    Table_Name = city.get(info['DepartureCity']) + "_" + city.get(info['ArrivalCity'])
    sql_insert_data = "insert into `{table_name}` values ('{a1}', '{a2}', '{a3}', '{a4}', '{a5}', '{a6}', '{a7}', '{a8}', '{a9}', '{a10}', '{a11}')"
    cursor.execute(sql_insert_data.format(table_name = Table_Name, a1 = info['DepartureCity'],
                a2 = info['ArrivalCity'], a3 = info['Airline'], a4 = info['FlightNumber'],
                a5 = info['CraftTypeName'], a6 = info['DepartureAirport'], a7 = info['DepartureDate'],
                a8 = info['ArrivalAirport'], a9 = info['ArrivalDate'], a10 = info['PunctualityRate'],
                a11 = info['LowestPrice'] ))
    db.commit()
def isNull(db,table_name):
    # 判断数据表是否存在
    cursor = db.cursor()
    sql = "show tables;"
    cursor.execute(sql)
    tables = [cursor.fetchall()]
    table_list = re.findall('(\'.*?\')',str(tables))
    table_list = [re.sub("'",'',each) for each in table_list]
    if table_name in table_list:
        return 0
    else:
        return 1


def show(table,num):
    print(table)
    print(num)
def main():
    date = '2019-05-23'
    for decity in city.keys():
        for arcity in city.keys():
            if(decity != arcity):
                getOneWay(decity, arcity, date)

if __name__ == "__main__":
    main()
