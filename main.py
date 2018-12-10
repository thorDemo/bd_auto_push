from configparser import ConfigParser
from threadpool import ThreadPool, makeRequests


config = ConfigParser()
config.read('config.ini', 'utf-8')
https = int(config.get('bd_push', 'https'))
thread_num = 2
target = config.get('bd_push', 'target')
if https == 1:
    from mylib.https_push import https_push
    pool = ThreadPool(thread_num)
    arg = []
    for x in range(0, thread_num):
        arg.append(target)
    request = makeRequests(https_push, arg)
    [pool.putRequest(req) for req in request]
    pool.wait()
elif https == 0:
    from mylib.http_push import http_push
    pool = ThreadPool(thread_num)
    arg = []
    for x in range(0, thread_num):
        arg.append(target)
    request = makeRequests(http_push, arg)
    [pool.putRequest(req) for req in request]
    pool.wait()
