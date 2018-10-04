# coding=utf-8

import urllib
import urllib2
import hmac
import hashlib
import json
import random
import requests
import os
import socket
import socks

# from collections import OrderedDict
import httplib
import time


def manege_keys(i):
    # i = 0, i = 1
    if not os.path.exists("ut_api_key.pem"):
        keys = raw_input("paste keys like this:user api_key")
        with open('ut_api_key.pem', 'w') as f:
            f.write(keys)
    with open('ut_api_key.pem', 'r') as f:
        keys = f.read()
        key = keys.split(" ")[i]
    return key


def do_get(sec_type, coin):
    proxies = {
        'http': 'socks5://user:pass@127.0.0.1:1080',
        'https': 'socks5://user:pass@127.0.0.1:1080'
    }
    url = "https://api-na.coinut.com/"+sec_type+"/" + coin + "usd"
    # response = requests.get(url, proxies=proxies, timeout=5)
    response = requests.get(url, proxies=proxies)
    return eval(response.content)


def ticker(coin):
    return do_get('spot', coin)


def request(api, content={}):
    url = 'https://api-na.coinut.com'
    headers = {}
    content["request"] = api
    content["nonce"] = random.randint(1, 1000000000)
    content = json.dumps(content)

    sig = hmac.new(manege_keys(1), msg=content,
                   digestmod=hashlib.sha256).hexdigest()
    headers = {'X-USER': manege_keys(0), "X-SIGNATURE": sig}

    response = requests.post(url, headers=headers, data=content)
    return eval(response.content)


def get_spot_trading_instruments(inst_id=None):
    result = request("inst_list", {'sec_type': 'SPOT'})
    if inst_id is not None:
        return result['SPOT'][inst_id][0]
    else:
        return result['SPOT']


def get_inst(pair):
    return get_spot_trading_instruments(pair)['inst_id']


def inst_tick(inst_id):
    return request("inst_tick", {"inst_id": inst_id})


def candle_ticks(inst_id, start_time, end_time, interval):
    return request("candle_ticks", {"inst_id": inst_id,
                   "start_time": start_time, "end_time": end_time,
                                             "interval": interval})


def inst_order_book(inst_id):
    return request("inst_order_book", {"inst_id": inst_id, "top_n": 10})


def get_market_trades(inst_id):
    return request("inst_trade", {"inst_id": inst_id})


def get_account_balance():
    return request("user_balance")


def submit_an_order(inst_id, side, qty, price=None):
    return request("new_order", new_order(inst_id, side, qty, price))


def new_order(inst_id, side, qty, price=None):
    order = {
        'inst_id': inst_id,
        'side': side,
        'qty': "%.8f" % float(qty),
        'client_ord_id': random.randint(1, 4294967290)
    }
    if price is not None:
        order['price'] = "%.8f" % float(price)
    return order


def submit_orders(ords):
    return request("new_orders", {"orders": ords})


def get_open_orders(inst_id):
    return request("user_open_orders", {"inst_id": inst_id})['orders']


def cancel_an_order(inst_id, order_id):
    return request("cancel_order", {"inst_id": inst_id, "order_id": order_id})


def cancel_orders(inst_id, ids):
    ords = [{'inst_id': inst_id, 'order_id': x} for x in ids]
    return request("cancel_orders", {'entries': ords})


def cancel_all_orders(inst_id):
    ords = get_existing_orders(inst_id)
    cancel_orders(inst_id, [x['order_id'] for x in ords])


def balance():
    return request("user_balance")


def main():
    print(ticker('btc'))
    # print balance()
    # print get_spot_trading_instruments()
    # print get_inst('BTCUSDT')
    # print inst_order_book('LTCUSDT')
    print('test ok! ')


if __name__ == '__main__':
    main()
