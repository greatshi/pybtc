# coding=utf-8


import hmac
import json
import random
import urllib
import urllib2
import base64
import hashlib
import requests
import os
import socket

import httplib
import time


def manege_keys():
    # i = 0, i = 1
    if not os.path.exists("ok_futures_v3_api_key.pem"):
        keys = {'api_key': '', 'secret_key': '', 'passphrase': ''}
        with open('ok_futures_v3_api_key.pem', 'w') as f:
            f.write(str(keys))
    with open('ok_futures_v3_api_key.pem', 'r') as f:
        keys = eval(f.read())
        api_key = keys['api_key']
        secret_key = keys['secret_key']
        passphrase = keys['passphrase']
    return api_key, secret_key, passphrase


def shift_time_v3(timestamp):
    format = '%Y-%m-%dT%H:%M:%SZ'
    value = time.localtime(timestamp)
    return time.strftime(format, value)


def request(api, method, params):
    api_key, secret_key, passphrase = manege_keys()
    request_path = api
    url = "https://www.okex.com"
    timestamp = str(time.time())
    headers = {'Content-Type': 'application/json'}
    headers['OK-ACCESS-KEY'] = api_key
    headers['OK-ACCESS-TIMESTAMP'] = timestamp
    headers['OK-ACCESS-PASSPHRASE'] = passphrase

    if str(params) == '{}' or str(params) == 'None':
        params = ''
    if method == 'GET':
        params = ''
        url += request_path
    if method == 'POST':
        request_path += '?'
        for key, value in params.items():
            request_path = request_path + str(key) + '=' + str(value) + '&'
        request_path = request_path[0:-1]
        params = json.dumps(params)

    message = '{timestamp}{method}{request_path}{params}'.format(
               timestamp=timestamp, method=method,
               request_path=request_path, params=params)

    signature = hmac.new(bytes(secret_key.encode('utf-8')),
                         msg=bytes(message.encode('utf-8')),
                         digestmod=hashlib.sha256).digest()

    headers['OK-ACCESS-SIGN'] = base64.b64encode(signature)

    if method == 'GET':
        response = requests.get(url, headers=headers)
    if method == 'POST':
        url += request_path
        response = requests.post(url, headers=headers, data=params)

    true = True
    false = False
    return eval(response.content)


def do_get(sec_type, params):
    url = 'https://www.okex.com/api/futures/v3/instruments/{}{}'.format(
           sec_type, params)
    headers = {'contentType': 'application/x-www-form-urlencoded'}
    response = requests.get(url, headers=headers, timeout=5)
    true = True
    false = False
    return eval(response.content)


def ticker(instrument_id):
    params = '?instrument_id={instrument_id}'.format(
             instrument_id=instrument_id)
    return do_get('{}/ticker'.format(instrument_id), params)


def book(instrument_id, size):
    '''depth
    '''
    params = '?instrument_id={instrument_id}&size={size}'.format(
             instrument_id=instrument_id, size=size)
    return do_get('{}/book'.format(instrument_id), params)


def candles(instrument_id, start, end, granularity):
    start = urllib.quote(shift_time_v3(start))
    end = urllib.quote(shift_time_v3(end))
    params = '?instrument_id={instrument_id}start={start}&end={end}&granularity={granularity}'.format(
             instrument_id=instrument_id, start=start,
             end=end, granularity=granularity)
    return do_get('{}/candles'.format(instrument_id), params)


def position():
    api = "/api/futures/v3/position"
    method = 'GET'
    params = {}
    return request(api, method, params)


def get_leverage(instrument_id):
    api = '/api/futures/v3/accounts/{currency}/leverage'.format(
           currency=instrument_id.split('-')[0].lower())
    method = 'GET'
    params = {}
    return request(api, method, params)


def set_leverage(margin_mode, currency, instrument_id,
                 direction, leverage):
    '''direction long short
       leverage 10 20
    '''
    api = '/api/futures/v3/accounts/{currency}/leverage'.format(
           currency=instrument_id.split('-')[0].lower())
    method = 'POST'
    if margin_mode == 'crossed':
        params = {
            # 'instrument_id':instrument_id,
            # 'direction':direction,
            'leverage': leverage,
            'currency': currency
        }
    elif margin_mode == 'fixed':
        params = {
            'currency': currency,
            'instrument_id': instrument_id,
            'direction': direction,
            'leverage': leverage,
        }
    return request(api, method, params)


def order(instrument_id, type, price, size, match_price, leverage):
    '''margin_mode: 全仓crossed_mode 逐仓fixed_mode
    '''
    api = "/api/futures/v3/order"
    method = 'POST'
    params = {
        'instrument_id': instrument_id,
        'type': type,
        'price': price,
        'size': size,
        # 'margin_mode': margin_mode,
        'match_price': match_price,
        'leverage': leverage
    }
    return request(api, method, params)


def cancel_order(instrument_id, order_id):
    api = '/api/futures/v3/cancel_order/{instrument_id}/{order_id}'.format(
          instrument_id=instrument_id, order_id=order_id)
    method = 'POST'
    params = {
        'instrument_id': instrument_id,
        'order_id': order_id
    }
    return request(api, method, params)


def orders(instrument_id, order_id):
    api = '/api/futures/v3/orders/{instrument_id}/{order_id}'.format(
           instrument_id=instrument_id, order_id=order_id)
    method = 'GET'
    params = {
        'instrument_id': instrument_id,
        'order_id': order_id
    }
    return request(api, method, params)


def main():
    print('test ok! ')


if __name__ == '__main__':
    main()
