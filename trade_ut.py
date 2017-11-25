#coding=utf-8

import api_ut as api
import time
import httplib
import urllib2
import __main__

def get_last_price(coin):
    while True:
        try:
            ticker_info = api.ticker(coin)
            last_price = ticker_info['last']
            if last_price != None:
                break
        except (IOError, httplib.HTTPException, urllib2.HTTPError, urllib2.URLError):
            print "error..."
    return last_price

def trusted_get_open_orders(pair, order_id):
    try:
        result = api.get_open_orders(pair)
        order_ids = []
        for res in result['orders']:
            order_ids.append(res['order_id'])
        if order_id in order_ids:
            order_status = 'wait'
        elif order_id not in order_ids:
            order_status = 'closed'
    except (IOError, httplib.HTTPException, urllib2.HTTPError, urllib2.URLError, KeyError):
        order_status = 'wait'
    return order_status

def test_order_closed(pair, order_id, seconds):
    while True:
        try:
            result = api.get_open_orders(pair)
            order_ids = []
            for res in result['orders']:
                order_ids.append(res['order_id'])
            if order_id in order_ids:
                order_status = 'wait'
            elif order_id not in order_ids:
                order_status = 'closed'
        except (IOError, httplib.HTTPException, urllib2.HTTPError, urllib2.URLError, KeyError):
            order_status = 'wait...'
        time.sleep(seconds)
        if order_status == 'closed':
            break
    return True

def trusted_cancel_order(pair, order_id):
    while True:
        try:
            result = api.cancel_an_order(pair, order_id)
            order_result = result['reply']
        except (IOError, httplib.HTTPException, urllib2.HTTPError, urllib2.URLError, KeyError):
            print 'Network Err...'
        if order_result == 'cancel_order':
            break
    return True

def trusted_submit_an_order(pair, side, qty, price):
    while True:
        status = False
        try:
            result = api.submit_an_order(pair, side, qty, price)
            order_id = result['order_id']
            status = result['reply']
        except (IOError, httplib.HTTPException, urllib2.HTTPError, urllib2.URLError):
            print 'Network Err...'
        except (KeyError):
            print 'Failed, ', result['reply']
        if status == 'order_accepted':
            break
    return order_id

def trusted_sell(pair, qty, ask):
    return trusted_submit_an_order('SELL', pair, amount, price)

def trusted_buy(pair, qty, bid):
    return trusted_submit_an_order('BUY', pair, amount, price)

def main():
    print "just use this~"
    # while True:
    #     print get_last_price('btc')
    #     print get_last_price('ltc')

if __name__ == '__main__':
    main()
