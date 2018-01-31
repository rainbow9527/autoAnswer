#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    #Author: smilesmith
    #Date: 2018-01-29
    #Desc: 公共方法
"""
import time
from colorama import Fore

def date_time_string():
    """Return the current time formatted """
    now = time.time()
    year, month, day, hh, mm, ss, x, y, z = time.localtime(now)
    s = "%04d%02d%02d" % (year, month, day)
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
