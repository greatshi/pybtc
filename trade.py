import api
import time
import httplib
import urllib2
import __main__

import sys

def get_last_price(coin):
    while True:
        try:
            ticker_info = api.ticker(coin)
            last_price = ticker_info['last']
            if last_price != None:
                break
        except (IOError, httplib.HTTPException, urllib2.HTTPError, urllib2.URLError):
            print "error info"
            pass
    return last_price

def test_order_closed(id, seconds):
    while True:
        try:
            fetch_order_result = api.fetch_order(id)
            order_status = fetch_order_result['status']
        except (IOError, httplib.HTTPException, urllib2.HTTPError, urllib2.URLError):
            order_status = 'wait...'
        time.sleep(seconds)
        if order_status == 'closed':
            break
    return True
 
def trusted_sell_or_buy(method, coin, amount, price):
    while True:
        try:
            result = api.sell_or_buy(method, coin, amount, price)
            id = result['id']
            status = result['result']
        except (IOError, httplib.HTTPException, urllib2.HTTPError, urllib2.URLError, KeyError):
            status = False
        if status == True:
            break
    return id

def trusted_sell(coin, amount, price):
    return trusted_sell_or_buy('sell', coin, amount, price)

def trusted_buy(coin, amount, price):
    return trusted_sell_or_buy('buy', coin, amount, price)

def main():
    print "just use this~"


if __name__ == '__main__':
    main()
    