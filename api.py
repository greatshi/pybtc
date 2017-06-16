#coding=utf-8

import urllib 
import urllib2
import hmac
import hashlib
import random
import requests
import os

from collections import OrderedDict
import httplib
import time

def manege_keys(i):
	#i = 0, i = 1
	if not os.path.exists("keys.pem"):
		keys = raw_input("paste keys like this:{Public_Key Private_Key}")
		with open('keys.pem', 'w') as f:
			f.write(keys)
	with open('keys.pem', 'r') as f:
		keys = f.read()
		key = keys.split(" ")[i]
	return key

def do_get(type, coin):
	url = "http://api.btctrade.com/api/"+ type +"?coin="+coin
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	true = True
	false = False
	return eval(response.read())

def ticker(coin):
	return do_get('ticker', coin)

def depth(coin):
	return do_get('depth', coin)

def trades(coin):
	return do_get('trades', coin)

def gen_nonce():
	return str(int(round(time.time() * 1000)))

def do_post(type, data):
	url = "http://api.btctrade.com/api/" + type + "/"
	keys = []
	values = []
	for d in data.split('&'):
		keys.append(d.split('=')[0])
		values.append(d.split('=')[1])
	keys.append('signature')
	signature = hmac.new(hashlib.md5(manege_keys(1)).hexdigest(), data, hashlib.sha256).hexdigest()
	values.append(signature)
	data = OrderedDict(zip(keys,values))
	data = urllib.urlencode(data)
	response = urllib2.urlopen(url, data)
	true = True
	false = False
	return eval(response.read())

def balance():	
	data = 'key='+manege_keys(0)+'&nonce='+gen_nonce()+'&version=2'
	return do_post('balance', data)

def orders(coin, type):
	data = 'coin='+coin+'&type='+type+'&since=1493695903.525188&ob=ASC&key='+manege_keys(0)+'&nonce='+gen_nonce()+'&version=2'
	return do_post('orders', data)

def fetch_or_cancel_order(type, id):
	data = 'id='+id+'&key='+manege_keys(0)+'&nonce='+gen_nonce()+'&version=2'
	return do_post(type, data)

def fetch_order(id):
	return fetch_or_cancel_order('fetch_order', id)

def cancel_order(id):
	return fetch_or_cancel_order('cancel_order', id)

def sell_or_buy(method, coin, amount, price):
	data = 'coin='+coin+'&amount='+amount+'&price='+price+'&key='+manege_keys(0)+'&nonce='+gen_nonce()+'&version=2'
	return do_post(method, data)

def sell(coin, amount, price):
	return sell_or_buy('sell', coin, amount, price)

def buy(coin, amount, price):
	return sell_or_buy('buy', coin, amount, price)

def main():
	print "\033[5;32;47m%s\033[0m" %  balance()
	print ticker('btc')
	print orders('btc', 'all')
	print 'test ok! '

if __name__ == '__main__':
	main()