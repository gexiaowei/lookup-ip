#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create time @ 2016-03-27 15:03:56

import sys
import socket
from workflow import Workflow, ICON_WEB, web

API = "http://ip-api.com/json"


def main(wf):
    www_ip = get_www_ip()
    wf.add_item(
        title=www_ip['ip'],
        subtitle=www_ip['timezone'],
        arg=www_ip['ip'],
        valid=True,
        icon=ICON_WEB)

    lan_ip = get_lan_ip()
    wf.add_item(
        title=lan_ip,
        subtitle=lan_ip,
        arg=lan_ip,
        valid=True,
        icon=ICON_WEB)

    wf.send_feedback()


def get_www_ip():
    data = web.get(API).json()
    if data['status'] == 'success':
        return {
            "ip": data['query'],
            "timezone": data['timezone']
        }
    else:
        return {
            "ip": "unknown address",
        }


def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "unknown address"
    finally:
        s.close()
    return ip


if __name__ == '__main__':
    # Create a global `Workflow` object
    wf = Workflow()
    # Call your entry function via `Workflow.run()` to enable its helper
    # functions, like exception catching, ARGV normalization, magic
    # arguments etc.
    sys.exit(wf.run(main))
