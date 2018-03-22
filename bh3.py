#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import requests


# 获取metadata列表
class Buyer:
    def __init__(self, bh_auth_key, bh_sign):
        self.bh_url = """https://event.bh3.com/bh3_2018spring_festival/trade.php?auth_key=%s&sign=%s&action=1&quantity=1""" % (
            bh_auth_key, bh_sign)

    def get_data(self):
        uri = self.bh_url
        r = requests.get(uri)
        if not r.ok:
            exit()
        return r.text

    def buy(self, type, price):
        uri = self.bh_url + ("&type=%s&price=%s") % (type, price)
        r = requests.post(uri)
        if not r.ok:
            exit()
        return r.text


def exchange(key, sign, which):
    url = 'https://event.bh3.com/bh3_2018spring_festival/exchange.php?auth_key=%s&sign=%s&redeem_id=%s' % (
        key.get(), sign.get(), which)
    a = requests.post(url)
    a


def start():
    global Buyer
    sign = '7e6db5a9426483eeba4f69cfbd3121966738d53e727491f89c6e04ec35966979'
    auth_key = """3XpVDZy0DM1ITN1ISNfZmbjl2ah5Wb9UWJ1UWJ4ITJ1kWJ3UWJ3ETJihWJ4UTJlhTJ5gWJyUTJwgWJyEWJ4UWJmFWJhJWJ4UTJ1kWJlJWJ1UWJ3EWJjFWJwUWJmJTJwklJs9XZlZDb20yMfZmdwl3XvBWa05TP4YDMwYlJl9mduVDdy0DM4E3cyBWan52XlZ3cpRmdsFlJ09Wal1TP1ETM1gjMycjM%3DM"""
    types = ['papercut', 'chipao']
    price_to_buy = ['0100']
    buyer = Buyer(auth_key, sign)

    n = 0
    while True:
        data = buyer.get_data()
        data = json.loads(data)
        if data['retcode'] == 0:
            data = data['data']
            for t in types:
                for p in price_to_buy:
                    n += 1
                    sys.stdout.write(str(n))
                    sys.stdout.flush()
                    if data[t][p] != '0':
                        res = buyer.buy(t, p)
                        res = json.loads(res)
                        if res['retcode'] == '0':
                            print('购买' + t + '   ' + p + '1个')
        else:
            continue


if __name__ == '__main__':
    start()
