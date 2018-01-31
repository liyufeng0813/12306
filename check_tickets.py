import requests
import re


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Referer': 'https://kyfw.12306.cn/otn/login/init'
}


def station():
    url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9044"
    r = requests.get(url, headers=headers)
    station = re.findall("'(.*)'", r.text)[0]
    station_list = station.split('@')[1:]
    station_dict = {}
    for i in station_list:
        temp_list = i.split('|')
        station_dict[temp_list[1]] = temp_list[2]
    return station_dict


def tickets():
    station_dict = station()
    DATE = '2018-02-18'
    FROM_STATION = 'CSQ'
    TO_STATION = 'CDW'
    # DATE = input('输入如下格式的日期2018-01-20：')
    # from_station = input("输入出发地车站：")
    from_station = '长沙'
    to_station = '成都'
    # to_station = input("输入目的地车站：")
    # FROM_STATION = station_dict[from_station]
    # TO_STATION = station_dict[to_station]
    url = "https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT".format(DATE, FROM_STATION, TO_STATION)
    r = requests.get(url, headers=headers)
    tickets_info = r.json()['data']['result']
    for i in tickets_info:
        temp_list = i.split('|')
        print(
        """
            {}车次
            出发站：{}
            到达站：{}
            出发时间：{}
            到达时间：{}
            历时：{}
            商务座，特等座：{}
            一等座：{}
            二等座：{}
            高级软卧：{}
            软卧：{}
            硬卧：{}
            硬座：{}
            无座：{}
        """.format(temp_list[3], temp_list[6], temp_list[7], temp_list[8], temp_list[9], temp_list[10], temp_list[32],
                   temp_list[31], temp_list[30], temp_list[21], temp_list[23], temp_list[28], temp_list[29], temp_list[26]))
    return tickets_info, DATE, from_station, to_station


if __name__ == "__main__":
    tickets()
