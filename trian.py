import requests, time, datetime, re
from urllib import parse
import information, check_tickets, codes, random


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Referer': 'https://kyfw.12306.cn/otn/login/init',
}
req = requests.Session()


def login():
    url = "https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.6896128496891729"
    image_code = req.get(url, headers=headers).content
    with open("image_code.png", "wb") as f:
        f.write(image_code)
    print('获取验证码...')

    url = "https://kyfw.12306.cn/passport/captcha/captcha-check"
    verification_code = input('code:')      #自己输入验证码
    # verification_code = codes.codes('image_code.png', 287)      #平台打码
    data = {
        'answer': verification_code,
        'login_site': 'E',
        'rand': 'sjrand'
    }
    r = req.post(url, data=data, headers=headers)
    result_code = r.json()['result_code']
    if result_code != '4':
        print('验证失败')
        login()
        return

    url = "https://kyfw.12306.cn/passport/web/login"
    data = {
        'username': information.USERNAME,
        'password': information.PASSWORD,
        'appid': 'otn'
    }
    r = req.post(url, data=data, headers=headers)
    result_code = r.json()['result_code']
    if result_code != 0:
        print('验证失败1')
        time.sleep(3)
        login()
        return

    url = "https://kyfw.12306.cn/passport/web/auth/uamtk"
    data = {
        'appid': 'otn'
    }
    r = req.post(url, data=data, headers=headers)
    result_code = r.json()['result_code']
    if result_code != 0:
        print('验证失败2')
        login()
        return

    TK = r.json()['newapptk']
    url = "https://kyfw.12306.cn/otn/uamauthclient"
    data = {
        'tk': TK
    }
    r = req.post(url, data=data, headers=headers)
    result_code = r.json()['result_code']
    if result_code != 0:
        print('验证失败3')
        login()
        return

    url = "https://kyfw.12306.cn/otn/login/checkUser"
    data = {
        '_json_att': ''
    }
    r = req.post(url, data=data, headers=headers)
    result_code = r.json()['status']
    if result_code is not True:
        print('验证失败4')
        login()
        return
    print('登陆成功')


def order(secret_str, DATE, from_station, to_station, left_ticket, train_no, station_train_code, train_date, seat_type, from_station_telecode, to_station_telecode, train_location):
    now = str(datetime.datetime.now())[:11]
    url = "https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest"
    data = {
        'secretStr': secret_str,
        'train_date': DATE,
        'back_train_date': now,
        'tour_flag': 'dc',
        'purpose_codes': 'ADULT',
        'query_from_station_name': from_station,
        'query_to_station_name': to_station,
        'undefined': ''
    }
    r = req.post(url=url, data=data, headers=headers)
    result_code = r.json()['status']
    if result_code is not True:
        print('下单失败1')

    url = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"
    data = {
        '_json_att': ''
    }
    r = req.post(url=url, data=data, headers=headers)
    REPEAT_SUBMIT_TOKEN = re.findall(r"globalRepeatSubmitToken = '(.*?)';", r.text)[0]
    key_check_isChange = re.findall(r"'key_check_isChange':'(.*?)',", r.text)[0]

    url = "https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs"
    data = {
        '_json_att': '',
        'REPEAT_SUBMIT_TOKEN': REPEAT_SUBMIT_TOKEN
    }
    r = req.post(url=url, data=data, headers=headers)
    result_code = r.json()['status']
    if result_code is not True:
        print('下单失败2')

    url = "https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo"
    data = {
        'cancel_flag': '2',
        'bed_level_order_num': '000000000000000000000000000000',
        'passengerTicketStr': seat_type + ',0,1,李宇峰,1,430281199508134676,18163910296,N',
        'oldPassengerStr': '李宇峰,1,430281199508134676,1_',
        'tour_flag': 'dc',
        'randCode': '',
        'whatsSelect': '1',
        '_json_att': '',
        'REPEAT_SUBMIT_TOKEN': REPEAT_SUBMIT_TOKEN
    }
    print(seat_type + ',0,1,李宇峰,1,430281199508134676,18163910296,N')
    r = req.post(url=url, data=data, headers=headers)
    result_code = r.json()['status']
    if result_code is not True:
        print('下单失败3')

    url = "https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount"
    data = {
        'train_date': train_date,
        'train_no': train_no,
        'stationTrainCode': station_train_code,
        'seatType': seat_type,
        'fromStationTelecode': from_station_telecode,
        'toStationTelecode': to_station_telecode,
        'leftTicket': left_ticket,
        'purpose_codes': '00',
        'train_location': train_location,
        '_json_att': '',
        'REPEAT_SUBMIT_TOKEN': REPEAT_SUBMIT_TOKEN
    }
    print('train_date:', train_date, '  train_no:', train_no, '  station_train_code:', station_train_code, '  seat_type:', seat_type, '  from_station_telecode:', from_station_telecode, '  to_station_telecode:', to_station_telecode, '  left_ticket:', left_ticket, '  train_location:', train_location, '  REPEAT_SUBMIT_TOKEN:', REPEAT_SUBMIT_TOKEN)
    r = req.post(url=url, data=data, headers=headers)
    result_code = r.json()['status']
    if result_code is not True:
        print('下单失败4')

    url = "https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue"
    data = {
        'passengerTicketStr': seat_type + ',0,1,李宇峰,1,' + information.identity_card + ',' + information.phone_number + ',N',
        'oldPassengerStr': '李宇峰,1,' + information.identity_card + ',1_',
        'randCode': '',
        'purpose_codes': '00',
        'key_check_isChange': key_check_isChange,
        'leftTicketStr': left_ticket,
        'train_location': train_location,
        'choose_seats': '',
        'seatDetailType': '000',
        'whatsSelect': '1',
        'roomType': '00',
        'dwAll': 'N',
        '_json_att': '',
        'REPEAT_SUBMIT_TOKEN': REPEAT_SUBMIT_TOKEN
    }
    r = req.post(url=url, data=data, headers=headers)
    result_code = r.json()['status']
    if result_code is not True:
        print('下单失败5')

    random_ = '151737731' + str(random.randint(1000, 9999))
    url = "https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?random={}&tourFlag=dc&_json_att=&REPEAT_SUBMIT_TOKEN={}".format(random_, REPEAT_SUBMIT_TOKEN)
    r = req.get(url)
    orderId = r.json()['data']['orderId']


    url = "https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue"
    data = {
        'orderSequence_no':	orderId,
        '_json_att': '',
        'REPEAT_SUBMIT_TOKEN': REPEAT_SUBMIT_TOKEN
    }
    r = req.post(url=url, data=data, headers=headers)
    result_code = r.json()['status']
    if result_code is not True:
        print('下单失败6')


def main():
    login()
    tickets_info, DATE, from_station, to_station = check_tickets.tickets()
    TICKET = input('要买哪种票(无座、硬座、硬卧、软卧、高级软卧、二等座、一等座、商务座)：')
    seat_type_dict = {'硬座': '1', '硬卧': '3', '软卧': '4', '二等座': 'O', '商务座': 'P'}
    seat_type = seat_type_dict[TICKET]
    ticket_dict = {'无座': 26, '硬座': 29, '硬卧': 28, '软卧': 23, '高级软卧': 21, '二等座': 30, '一等座': 31, '商务座': 32}
    TICKET_NUM = ticket_dict[TICKET]
    train_date = time.strftime('%a %b %d %Y %H:%M:%S', time.strptime(DATE, '%Y-%m-%d')) + ' GMT+0800 (中国标准时间)'
    for i in tickets_info:
        temp_list = i.split('|')
        print(temp_list[TICKET_NUM])
        from_station_telecode = temp_list[4]
        to_station_telecode = temp_list[5]
        train_location = temp_list[15]
        if temp_list[TICKET_NUM] == '' or temp_list[TICKET_NUM] == '无':
            continue
        else:
            secret_str = parse.unquote(temp_list[0])
            left_ticket = temp_list[12]
            train_no = temp_list[2]
            station_train_code = temp_list[3]
            order(secret_str, DATE, from_station, to_station, left_ticket, train_no, station_train_code, train_date, seat_type, from_station_telecode, to_station_telecode, train_location)
            break
    else:
        print('无票')


if __name__ == '__main__':
    main()