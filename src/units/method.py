#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    #Author: smilesmith
    #Date: 2018-01-29
    #Desc: 公共方法
"""
import time
from urllib.request import Request, urlopen
from colorama import Fore


def date_time_string():
    """Return the current time formatted """
    now = time.time()
    year, month, day, hh, mm, ss, x, y, z = time.localtime(now)
    s = "%04d%02d%02d-%02d" % (year, month, day, hh)
    return s


def __log_date_time_string():
    """Return the current time formatted for logging."""
    monthname = [None,
                 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    now = time.time()
    year, month, day, hh, mm, ss, x, y, z = time.localtime(now)
    s = "%02d/%3s/%04d %02d:%02d:%02d" % (
        day, monthname[month], year, hh, mm, ss)
    return s


def log_info(log_format, *args):
    """自定义日志"""
    print("[%s] %s" %
          (__log_date_time_string(), log_format % args))


def log_error(log_format, *args):
    """错误日志"""
    print(Fore.LIGHTRED_EX + ("[%s] %s" %
                              (__log_date_time_string(), log_format % args)) + Fore.RESET)


def log_warn(log_format, *args):
    """警告日志"""
    print(Fore.YELLOW + ("[%s] %s" %
                         (__log_date_time_string(), log_format % args)) + Fore.RESET)


def get_prefer_result(results, options):
    """返回优选答案"""
    pri_obj = {}
    for result in results:
        if result.text not in pri_obj:
            pri_obj[result.text] = result.prop
        else:
            pri_obj[result.text] += result.prop

    prefer_option = ''

    prefer_pri = 0

    for option, prop in pri_obj.items():
        if prefer_pri < prop:
            prefer_option = option
            prefer_pri = prop

    for index, option in enumerate(options):
        if prefer_option == option:
            return index

    return None


ANDROID_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.1.1; Google Pixel - \
7.1.0 - API 25 - 1080x1920 Build/NMF26Q; wv) AppleWebKit/537.36 (KHTML, like Gecko) \
Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 SogouSearch Android1.0 version3.0 AppVersion/5802"

HEADERS = {
    'Host': 'answer.sm.cn',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Accept': 'text/html, */*; q=0.01',
    'User-Agent': ANDROID_USER_AGENT,
    'Referer': 'http://answer.sm.cn/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}


def mock_request(path, **my_headers):
    """伪装请求"""
    headers = HEADERS.copy()
    for key in my_headers:
        headers[key] = my_headers[key]

    req = Request(path, headers=headers)
    res = urlopen(req)
    res_str = str(res.read(), 'UTF-8')
    return res_str
