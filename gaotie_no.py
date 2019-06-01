# coding: utf-8
import requests
import json
#需要参数：列车号，始发站、终点站的编码，日期

def getCityNumber(train_no, fs_telecode, ts_telecode,date):
    headers = {
        'Host': 'kyfw.12306.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        'Cookie': 'JSESSIONID=6F9DB6833F249AEE649F26CB192E7587; _jc_save_wfdc_flag=dc; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; BIGipServerotn=569377290.64545.0000; RAIL_EXPIRATION=1558733197798; RAIL_DEVICEID=MahLDnelNi0Ih-R8lMT3ZVY0GNAPyLFKIh6QT05ReMC-4A97Bnby6fAp-aEGz2M6es2q_a82HpSXMC2T1sCMFsf-qR0BKnDnBnyJ_E3yWCSREAt9A9_YTJJynA7SR-6Evm9KeYX50YQgeHbSuiH1oDZDS6vu5gOM; route=c5c62a339e7744272a54643b3be5bf64; _jc_save_toDate=2019-05-21; ten_key=xdd5naei5t2rzDlFyBqrh2yyFIiBCnDa; ten_js_key=xdd5naei5t2rzDlFyBqrh2yyFIiBCnDa; BIGipServerpool_passport=334299658.50215.0000; _jc_save_fromDate=2019-05-',
    }
    url = "https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no={train_no}&from_station_telecode={fs_telecode}&to_station_telecode={ts_telecode}&depart_date={date}"

    html = requests.get(url.format(train_no = train_no,fs_telecode = fs_telecode,ts_telecode = ts_telecode,date = date),
                        headers = headers)
    html.encoding = 'utf-8'
    text = html.text
    text = json.loads(text)
    lists = text.get("data").get("data")
    info = {}
    for list in lists:
        city = list.get("station_name")
        no = list.get("station_no")
        info[city] = no
    print("number函数测试")
    print(info)
    return info
if __name__ == "__main__":
    getCityNumber()