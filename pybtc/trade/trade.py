# coding=utf-8


import time
import httplib
import urllib2
import __main__
from pybtc.api import api as api


def get_last_price(coin):
    while True:
        try:
            ticker_info = api.ticker(coin)
            last_price = ticker_info['last']
            if last_price is not None:
                break
        except (IOError, httplib.HTTPException, urllib2.HTTPError,
                urllib2.URLError):
            print('get_last_price error...')
    return last_price


def test_order_closed(id, seconds):
    while True:
        try:
            result = api.fetch_order(id)
            order_status = result['status']
        except (IOError, httplib.HTTPException, urllib2.HTTPError,
                urllib2.URLError, KeyError):
            order_status = 'wait...'
        time.sleep(seconds)
        if order_status == 'closed':
            break
    return True


def trusted_fetch_order(id):
    try:
        result = api.fetch_order(id)
        order_status = result['status']
    except (IOError, httplib.HTTPException, urllib2.HTTPError,
            urllib2.URLError, KeyError):
        order_status = 'wait'
    return order_status


def trusted_cancel_order(id):
    while True:
        try:
            result = api.cancel_order(id)
            order_result = result['result']
        except (IOError, httplib.HTTPException, urllib2.HTTPError,
                urllib2.URLError, KeyError):
            print('Network Err...')
        if order_result is True:
            break
        elif order_result is False:
            print(result['message'])
    return True


def trusted_sell_or_buy(method, coin, amount, price):
    while True:
        status = False
        try:
            result = api.sell_or_buy(method, coin, amount, price)
            id = result['id']
            status = result['result']
        except (IOError, httplib.HTTPException, urllib2.HTTPError,
                urllib2.URLError):
            print('Network Err...')
        except (KeyError):
            print('Failed, {}'.format(result['message']))
        if status is True:
            break
    return id


def trusted_sell(coin, amount, price):
    return trusted_sell_or_buy('sell', coin, amount, price)


def trusted_buy(coin, amount, price):
    return trusted_sell_or_buy('buy', coin, amount, price)


def main():
    print('just use this~')


if __name__ == '__main__':
    main()
