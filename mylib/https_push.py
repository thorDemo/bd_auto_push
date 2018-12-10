import requests
from tools.push_tools import PushTool
from urllib import parse
import time
from random import randint
from datetime import datetime
import sys

success_num = 0
failure_num = 0
start_time = datetime.now()
server = PushTool.https_target()
cookie = PushTool.get_cookies()


def https_push(domain):
    global success_num
    global failure_num
    global start_time
    url = ''
    while True:
        code = 233
        r = PushTool.rand_all(domain)
        i = PushTool.rand_all(domain)
        try:
            headers = {
                'User-Agent': PushTool.user_agent(),
                'Referer': r,
                'Accept': '*/*',
                'Connection': 'keep-alive',
                'Host': 'sp0.baidu.com',
            }
            conn = requests.Session()
            conn.headers = headers
            # print(headers)
            # 将cookiesJar赋值给会话
            cookiesJar = requests.utils.cookiejar_from_dict(cookie, cookiejar=None, overwrite=True)
            conn.cookies = cookiesJar
            target = '%s?r=%s&l=%s' % (server, r, i)
            http = conn.get(target)
            code = http.status_code
            if http.content == b'' and http.status_code == 200:
                success_num += 1
            else:
                failure_num += 1
        except:
            failure_num += 1
        this_time = datetime.now()
        spend = this_time - start_time
        if int(spend.seconds) == 0:
            speed_sec = success_num / 1
        else:
            speed_sec = success_num / int(spend.seconds)
        speed_day = float('%.2f' % ((speed_sec * 60 * 60 * 24) / 10000))
        percent = success_num / (failure_num + success_num) * 100
        sys.stdout.write(' ' * 100 + '\r')
        sys.stdout.flush()
        print(r, code)
        sys.stdout.write(
            '%s 成功%s 预计(day/万):%s 万 成功率:%.2f%% 状态码:%s\r' % (datetime.now(), success_num, speed_day, percent, code))
        sys.stdout.flush()
