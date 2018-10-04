# coding=utf-8

import urllib.request
import urllib.parse
import urllib.error
# import urllib.request, urllib.error, urllib.parse
import hmac
import hashlib
import json
import random
import requests
import os
import socket

import http.client
import time


def manege_keys(i):
    # i = 0, i = 1
    if not os.path.exists("ok_api_key.pem"):
        keys = eval(input("paste keys like this:apiKey secretKey"))
        with open('ok_api_key.pem', 'w') as f:
            f.write(keys)
    with open('ok_api_key.pem', 'r') as f:
        keys = f.read()
        key = keys.split(" ")[i]
    return key


def do_get(sec_type, coin, other=''):
    url = "https://www.okex.com/api/v1/{}?symbol={}_usdt{}".format(
          sec_type, coin, other)
    headers = {'contentType': 'application/x-www-form-urlencoded'}
    response = requests.get(url, headers=headers, timeout=5)
    return eval(response.content)


def ticker(coin):
    return do_get('ticker.do', coin)


def kline(coin, type, size, since):
    other = '&type='+type+'&size='+size+'&since='+since
    return do_get('kline.do', coin, other)


def request(api, params):
    url = "https://www.okex.com/api/v1/" + api
    headers = {'contentType': 'application/x-www-form-urlencoded'}
    sign = ''
    for key in sorted(params.keys()):
        sign += key + '=' + str(params[key]) + '&'
    data = sign+'secret_key='+manege_keys(1)
    sign = hashlib.md5(data.encode("utf8")).hexdigest().upper()
    params['sign'] = sign

    response = requests.post(url, headers=headers, data=params)

    true = True
    false = False
    return eval(response.content)


def userinfo():
    api = "userinfo.do"
    params = {'api_key': manege_keys(0)}
    return request(api, params)


def trade(coin, tradetype, price='', amount=''):
    api = "trade.do"
    params = {
        'api_key': manege_keys(0),
        'symbol': coin+'_usdt',
        'type': tradetype
    }
    if price:
        params['price'] = price
    if amount:
        params['amount'] = amount
    return request(api, params)


def fetch_or_cancel_order(api, coin, id):
    params = {
        'api_key': manege_keys(0),
        'symbol': coin+'_usdt',
        'order_id': id
    }
    return request(api, params)


def fetch_order(coin, id):
    api = "order_info.do"
    return fetch_or_cancel_order(api, coin, id)


def cancel_order(coin, id):
    api = "cancel_order.do"
    return fetch_or_cancel_order(api, coin, id)


def main():
    print(ticker('btc')['ticker']['last'])
    print(userinfo())
    # print(get_spot_trading_instruments())
    # print(get_inst('BTCUSDT'))
    # print(inst_order_book('LTCUSDT'))
    print('test ok! ')


if __name__ == '__main__':
    main()
