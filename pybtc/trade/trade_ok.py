# coding=utf-8


import time
import datetime
import http.client
import urllib.request
import urllib.error
import urllib.parse
import __main__
import OpenSSL
from pybtc.api import api_ok as api


def get_last_price(coin):
    while True:
        try:
            ticker_info = api.ticker(coin)
            last_price = ticker_info['ticker']['last']
            if last_price is not None:
                break
        except (IOError, http.client.HTTPException, urllib.error.HTTPError,
                urllib.error.URLError):
            print('get_last_price error...')
    return last_price


def get_kline(coin, type, size, since):
    while True:
        try:
            return api.kline(coin, type, size, since)
        except (IOError, http.client.HTTPException, urllib.error.HTTPError,
                urllib.error.URLError, KeyError, SyntaxError,
                OpenSSL.SSL.ZeroReturnError):
            print("get_kline error...")
        time.sleep(1)


def get_userinfo():
    while True:
        try:
            return api.userinfo()
        except (IOError, http.client.HTTPException, urllib.error.HTTPError,
                urllib.error.URLError, KeyError, SyntaxError,
                OpenSSL.SSL.ZeroReturnError):
            print("userinfo error...")


# pass
def test_order_closed(id, seconds):
    while True:
        try:
            result = api.fetch_order(id)
            order_status = result['status']
        except (IOError, http.client.HTTPException, urllib.error.HTTPError,
                urllib.error.URLError, KeyError):
            order_status = 'wait...'
        time.sleep(seconds)
        if order_status == 'closed':
            break
    return True


def trusted_fetch_order(coin, id):
    try:
        result = api.fetch_order(coin, id)
    except (IOError, http.client.HTTPException, urllib.error.HTTPError,
            urllib.error.URLError, KeyError):
        result = 'wait'
    return result


def trusted_cancel_order(coin, id):
    while True:
        order_result = False
        try:
            result = api.cancel_order(coin, id)
            order_result = result['result']
        except (IOError, http.client.HTTPException, urllib.error.HTTPError,
                urllib.error.URLError, KeyError):
            print('Network Err...')
        if order_result is True:
            break
        else:
            try:
                print(result['error_code'])
            except Exception as e:
                pass
    return True


def trusted_trade(coin, method, price, amount):
    # method = buy_market  sell_market
    while True:
        status = False
        try:
            result = api.trade(coin, method, price, amount)
            id = result['order_id']
            status = result['result']
        except (IOError, http.client.HTTPException, urllib.error.HTTPError,
                urllib.error.URLError):
            print('Network Err...')
        except (KeyError):
            print('Failed, {}'.format(result))
        if status is True:
            break
    return id


def trusted_sell(coin, price, amount):
    return trusted_trade(coin, 'sell', price, amount)


def trusted_buy(coin, price, amount):
    return trusted_trade(coin, 'buy', price, amount)


def main():
    coin = 'btc'
    # print get_last_price(coin)
    amount = 0.001
    price = 1000
    print(trusted_buy(coin, price, amount))

    print(trusted_fetch_order(coin, 945793949))
    # print trusted_cancel_order(coin, 794218443)

    # print get_kline(coin, '15min', '2000', '')
    userinfo = get_userinfo()
    print(userinfo['info']['funds']['free']['btc'])
    print(userinfo['info']['funds']['free']['usdt'])

    print('just use this~')


if __name__ == '__main__':
    main()
