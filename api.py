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

def signature(wait_sign_string):
	return hmac.new(hashlib.md5(manege_keys(1)).hexdigest(), wait_sign_string, hashlib.sha256).hexdigest()

def do_post(type, data):
	url = "http://api.btctrade.com/api/" + type + "/"
	data = urllib.urlencode(data)
	response = urllib2.urlopen(url, data)
	true = True
	false = False
	return eval(response.read())	

def balance():	
	nonce = gen_nonce()
	wait_sign_string = 'key='+manege_keys(0)+'&nonce='+nonce+'&version=2'
	data = OrderedDict([('key', manege_keys(0)), ('nonce', nonce), ('version', '2'), ('signature', signature(wait_sign_string))])
	return do_post('balance', data)

def orders(coin, type):
	#coin = 'btc','eth','ltc','doge','ybc'; type = open, closed, cancelled
	nonce = gen_nonce()
	wait_sign_string = 'coin='+coin+'&type='+type+'&since=1493695903.525188&ob=ASC&key='+manege_keys(0)+'&nonce='+nonce+'&version=2'
	data = OrderedDict([('coin', coin), ('type', type), ('since', '1493695903.525188'), ('ob', 'ASC'), ('key', manege_keys(0)), ('nonce', nonce), ('version', '2'), ('signature', signature(wait_sign_string))])
	return do_post('orders', data)

def fetch_order(id):
	nonce = gen_nonce()
	wait_sign_string = 'id='+id+'&key='+manege_keys(0)+'&nonce='+nonce+'&version=2'
	data = OrderedDict([('id', id), ('key', manege_keys(0)), ('nonce', nonce), ('version', '2'), ('signature', signature(wait_sign_string))])
	return do_post('fetch_order', data)

def cancel_order(id):
	nonce = gen_nonce()
	wait_sign_string = 'id='+id+'&key='+manege_keys(0)+'&nonce='+nonce+'&version=2'
	data = OrderedDict([('id', id), ('key', manege_keys(0)), ('nonce', nonce), ('version', '2'), ('signature', signature(wait_sign_string))])
	return do_post('cancel_order', data)

def sell_or_buy(method, coin, amount, price):
	#method = 'sell','buy'; coin = 'btc','eth','ltc','doge','ybc'; amount = '666'; price = '100000' 
	nonce = gen_nonce()
	wait_sign_string = 'coin='+coin+'&amount='+amount+'&price='+price+'&key='+manege_keys(0)+'&nonce='+nonce+'&version=2'
	data = OrderedDict([('coin', coin), ('amount', amount), ('price', price), ('key', manege_keys(0)), ('nonce', nonce), ('version', '2'), ('signature', signature(wait_sign_string))])
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
