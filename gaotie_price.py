# coding: utf-8
import chardet
import requests
import json
#需要参数始发终点站的号，列车号，和时间

def getThreePrice(train_code, fs_no, ts_no,date):
    headers = {
        'Accept': '* / *',
        'Accept - Encoding': 'gzip, deflate, br',
        'Cache - Control': 'no - cache',
        'Host': 'kyfw.12306.cn',
        'X - Requested - With': 'XMLHttpRequest',
        'If - Modified - Since': '0',
        'Accept - Language': 'zh - CN,zh;q=0.9,en;q = 0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        'Cookie': 'JSESSIONID=9A8AE26B5F871CD53305332B08474A70; ten_key=xdd5naei5t2rzDlFyBqrh2yyFIiBCnDa; ten_js_key=xdd5naei5t2rzDlFyBqrh2yyFIiBCnDa; _jc_save_wfdc_flag=dc; RAIL_EXPIRATION=1559381330258; RAIL_DEVICEID=BURyW-kgA7NOnzDwoV4rntfFji-zSqHl5cxrIf7-j3fe1nOSUkVAR162kn2SnXoVugZWxT7U8zHwsKuL9Lg-zSjKqXUX91ZKC5EmeMQv8nqdCyGKNXR4UoiyCl8TibgYacPlgKCsg9DaXOT47ZwRLM5AU5RJCvpf; BIGipServerpool_passport=216859146.50215.0000; route=c5c62a339e7744272a54643b3be5bf64; BIGipServerotn=183501322.50210.0000; _jc_save_fromStation=%u91CD%u5E86%2CCQW; _jc_save_toDate=2019-05-30; _jc_save_toStation=%u5357%u660C%2CNCG; _jc_save_fromDate=2019-05-30'
    }
    url = "https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no={}&from_station_no={}&to_station_no={}&seat_types=OM9&train_date=2019-06-02"
    html = requests.get(url.format(train_code, fs_no, ts_no))
    html.encoding = 'utf-8'  #防止乱码无法解析
    print(type(html.text))
    if(html.status_code == 200):
        text = html.text
    if(len(text) == 0):
        text = requests.get(url.format(train_code, fs_no, ts_no),headers=headers).text
    if text.startswith(u'\ufeff'):
        text = text.encode('utf8')[3:].decode('utf8')
    print(len(text))
    print(train_code)
    print(text)
    #text = json.loads(text)
    lists = html.json()["data"]
    price = {}
    price["A9"] = lists.get("A9","---")
    price["M"] = lists.get("M","---")
    price["O"] = lists.get("O","---")
    print("price函数测试")
    print(price)
    return price
if __name__ == "__main__":
    getThreePrice()