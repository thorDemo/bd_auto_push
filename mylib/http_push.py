from tools.push_tools import PushTool
import requests
import traceback
from urllib import parse
from datetime import datetime
import sys
import time
from random import randint

success_num = 0
failure_num = 0
cookie = PushTool.get_cookies()
start_time = datetime.now()


def http_push(domain):
    tool = PushTool()
    while True:
        global success_num
        global failure_num
        global start_time
        referer = tool.rand_all()
        r = tool.rand_all()
        headers = {
            'User-Agent': PushTool.user_agent(),
            'Referer': referer,
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'api.share.baidu.com',
        }
        conn = requests.Session()
        conn.headers = headers
        # print(headers)
        # 将cookiesJar赋值给会话
        cookies_jar = requests.utils.cookiejar_from_dict(cookie, cookiejar=None, overwrite=True)
        conn.cookies = cookies_jar
        payload = {'r': r}
        code = 404
        url = ''
        try:
            r = parse.quote_plus(r)
            url = 'http://api.share.baidu.com/s.gif?r=%s&l=%s' % (r, referer)
            res = conn.get(url, params=payload, timeout=10)
            code = res.status_code
            url = parse.unquote(res.url)
            if code == 200:
                if url == 'http://www.baidu.com/search/error.html':
                    failure_num += 1
                else:
                    success_num += 1
            else:
                failure_num += 1
        except:
            # traceback.print_exc()
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
        print(referer, code)
        sys.stdout.write(
            '%s 成功%s 预计(day/万):%s 万 成功率:%.2f%% 状态码:%s\r' % (datetime.now(), success_num, speed_day, percent, code))
        sys.stdout.flush()
