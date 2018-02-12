#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""程序主进程"""

from multiprocessing import Process
import webbrowser
from servers.web_server import run_server
from servers.sogou_proxy import run_sogou_proxy
from servers.baidu_websocket import websocket_server
from src.units import adb, sqlite
from src.units.method import check_hosts

PORT = 8080
PROXY_PORT = 8888

HOST = 'dev.secr.baidu.com'


def run():
    """主函数"""
    if check_hosts(HOST):
        adb.init()
        sqlite.init_table()
        # baidu_process = Process(target=websocket_server)
        # baidu_process.start()
        sub_process = Process(target=run_sogou_proxy)
        sub_process.start()
        webbrowser.open("http://%s:%s/index.html" % (HOST, PORT))
        run_server(port=PORT)


if __name__ == '__main__':
    run()
