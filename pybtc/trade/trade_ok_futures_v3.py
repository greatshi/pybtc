# coding=utf-8


import time
import datetime
import httplib
import urllib
import urllib2
import urlparse
import OpenSSL


from pybtc.api import api_ok_futures_v3 as api


def ticker(instrument_id):
    while True:
        try:
            ticker_info = api.ticker(instrument_id)
            return ticker_info
        except (IOError, httplib.HTTPException, urllib2.HTTPError,
                urllib2.URLError):
            print u'ticker error...'
    time.sleep(1)


def book(instrument_id, size):
    while True:
        try:
            return api.book(instrument_id, size)
        except (IOError, httplib.HTTPException, urllib2.HTTPError,
                urllib2.URLError, KeyError, SyntaxError,
                OpenSSL.SSL.ZeroReturnError):
            print('book error...')
        time.sleep(1)


def candles(instrument_id, start, end, granularity):
    while True:
        try:
            return api.candles(instrument_id, start, end, granularity)
        except (IOError, httplib.HTTPException, urllib2.HTTPError,
                urllib2.URLError, KeyError, SyntaxError,
                OpenSSL.SSL.ZeroReturnError):
            print('candles error...')
        time.sleep(1)


def position():
    while True:
        try:
            return api.position()
        except (IOError, httplib.HTTPException, urllib2.HTTPError,
                urllib2.URLError, KeyError, SyntaxError,
                OpenSSL.SSL.ZeroReturnError):
            print('position error...')
        time.sleep(1)


def get_leverage(instrument_id):
    while True:
        try:
            return api.get_leverage(instrument_id)
        except (IOError, httplib.HTTPException, urllib2.HTTPError,
                urllib2.URLError, KeyError, SyntaxError,
                OpenSSL.SSL.ZeroReturnError):
            print('get_leverage error...')
        time.sleep(1)


def set_leverage(margin_mode, currency, instrument_id,
                 direction, leverage):
    while True:
        try:
            return api.set_leverage(margin_mode, currency,
                                    instrument_id,
                                    direction, leverage)
        except (IOError, httplib.HTTPException, urllib2.HTTPError,
                urllib2.URLError, KeyError, SyntaxError,
                OpenSSL.SSL.ZeroReturnError):
            print('set_leverage error...')
        time.sleep(1)


def order(instrument_id, type, price, size, match_price, leverage):
    while True:
        status = False
        try:
            result = api.order(instrument_id, type, price,
                               size, match_price, leverage)
            id = result['order_id']
            status = result['result']
            if (id == -1):
                print('Failed, {}'.format(result['error_messsage']))
                break
            if (result['error_code'] == 0):
                return id
        except (IOError, httplib.HTTPException, urllib2.HTTPError,
                urllib2.URLError, KeyError):
            print('order error...')
        if status is True:
            break
    return id


def cancel_order(instrument_id, order_id):
    while True:
        order_result = False
        try:
            result = api.cancel_order(instrument_id, order_id)
            order_result = result['result']
            if (int(result['order_id']) == int(order_id)):
                break
            else:
                print(result)
        except (IOError, httplib.HTTPException, urllib2.HTTPError,
                urllib2.URLError, KeyError):
            print('cancel_order error...')
    return True


def orders(instrument_id, order_id):
    while True:
        try:
            result = api.orders(instrument_id, order_id)
        except (IOError, httplib.HTTPException, urllib2.HTTPError,
                urllib2.URLError, KeyError):
            print('cancel_order error...')
        if (int(result['order_id']) == int(order_id)):
            break
    return result


def main():
    print('just use this~')


if __name__ == u'__main__':
    main()
