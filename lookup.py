#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create time @ 2016-03-27 15:03:56

import sys
import json
import socket
from workflow import Workflow, ICON_WEB, web

API = "http://ip-api.com/json"
TAOBAO_IP_API = 'http://ip.taobao.com/service/getIpInfo2.php'


def main(wf):
    args = wf.args
    if not args[0]:
        add_www_ip(wf)
        add_lan_ip(wf)
    else:
        add_www_ip(wf, ip=args[0])
    wf.send_feedback()


def add_www_ip(wf, ip='myip'):
    response = web.post(TAOBAO_IP_API, params={'ip': ip}).json()
    data = response['data']
    if response['code'] == 0:
        wf.add_item(
            title=data['ip'],
            subtitle=u'{} {} {}'.format(data['country'], data['city'],
                                        data['isp']),
            arg=data['ip'],
            valid=True,
            icon=ICON_WEB)
    else:
        wf.add_item(
            title='unknown address', subtitle='WWW IP Address', icon=ICON_WEB)


def add_lan_ip(wf):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        wf.add_item(
            title=ip,
            subtitle="Lan IP Address",
            arg=ip,
            valid=True,
            icon=ICON_WEB)
    except:
        wf.add_item(
            title='unknown address', subtitle='Lan IP Address', icon=ICON_WEB)
    finally:
        s.close()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
    # get_www_ip()
