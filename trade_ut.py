#coding=utf-8

import api_ut as api
import time
import datetime
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

def get_candle_ticks(pair, days, interval):
    end_time = int(time.time())
    date_array = datetime.datetime.utcfromtimestamp(end_time)
    n_day_ago = date_array - datetime.timedelta(days = days)
    start_time = int(time.mktime(n_day_ago.timetuple()))
    return api.candle_ticks(pair, start_time, end_time, interval)

def get_trades(pair):
    price = []
    qty = []
    timestamp = []

    trades = api.get_market_trades(pair)
    for trade in trades['trades']:
        price.append(float(trade['price']))
        qty.append(float(trade['qty']))
        timestamp.append(trade['timestamp'])
    return price, qty, timestamp

def trusted_get_account_balance():
    while True:
        try:
            balance = api.get_account_balance()
            break
        except (IOError, httplib.HTTPException, urllib2.HTTPError, urllib2.URLError, KeyError):
            pass
    return balance

def trusted_get_open_orders(pair, order_id):
    try:
        result = api.get_open_orders(pair)
        order_ids = []
        for res in result:
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
        order_status = trusted_get_open_orders(pair, order_id)
        time.sleep(seconds)
        if order_status == 'closed':
            break
    return True

def trusted_cancel_order(pair, order_id):
    while True:
        order_result = 'none'
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
            if type(result) == dict:
                order_id = result['order_id']
                status = result['reply']
            elif type(result) == list:
                order_id = result[0]['order']['order_id']
                status = result[0]['reply']
        except (IOError, httplib.HTTPException, urllib2.HTTPError, urllib2.URLError):
            print 'Network Err...'
        except (KeyError):
            print 'Failed, ', str(status)
        if status == 'order_accepted' or status == 'order_filled':
            break
    return order_id

def trusted_sell(pair, qty, ask):
    return trusted_submit_an_order(pair, 'SELL', qty, ask)

def trusted_buy(pair, qty, bid):
    return trusted_submit_an_order(pair, 'BUY', qty, bid)

def main():
    print "just use this~"
    # while True:
    #     print get_last_price('btc')
    #     print get_last_price('ltc')

if __name__ == '__main__':
    main()
