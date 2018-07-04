#coding=utf-8

import trade_ut as trade
import sys
import time

def left_side_method(inst_id, amount, buy_price, sell_price):
    buy_id = trade.trusted_buy(inst_id, amount, buy_price)
    print "buying~, id = "+buy_id
    if trade.test_order_closed(buy_id,0.1):
        print "bought~"
        sell_id = trade.trusted_sell(inst_id, amount, sell_price)
        print "selling~, id = "+sell_id
        if trade.test_order_closed(sell_id,3):
            return 'A great deal!'

def right_side_method(inst_id, amount, buy_price, sell_price):
    sell_id = trade.trusted_sell(inst_id, amount, sell_price)
    print "selling~, id = "+sell_id
    if trade.test_order_closed(sell_id,0.1):
        print "selled~"
        buy_id = trade.trusted_buy(inst_id, amount, buy_price)
        print "buying~, id = "+buy_id
        if trade.test_order_closed(buy_id,3):
            return 'A great deal!'

def simple_side():
    print "~~Usage:"
    print "~~$python strategy.py"
    print "~~or $python strategy.py left btc 1 8600 8700"
    print "~~Ctrl+C to quit!"
    try:
        side, pair, amount, buy_price, sell_price = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    except IndexError:
        print "{left, right} {BTCUSDT, ETHUSDT, LTCUSDT} {amount} {price} {price}"
        order = raw_input("side pair amount buy_price sell_price:")
        side, pair, amount, buy_price, sell_price = order.split(" ")[0], order.split(" ")[1], order.split(" ")[2], order.split(" ")[3], order.split(" ")[4]

    inst_id = trade.trusted_get_inst(pair)
    while True:
        print "wait~"
        if side == 'left':
            print left_side_method(inst_id, amount, buy_price, sell_price)
        elif side == 'right':
            print right_side_method(inst_id, amount, buy_price, sell_price)
        else:
            print "error, running again~"

def stop_loss():
	pass

def auto_left_side(pair, amount_ratio, avg_price, earn_ratio, loss_ratio):
	pass

def get_average(list):
	sum = 0
	for item in list:
		sum += item
	return sum/len(list)

def get_ma(inst_id, k_line_time):
    lines = trade.get_candle_ticks(inst_id, 60, k_line_time)['tick']
    timestamp = lines[-1][-1]
    print timestamp
    pr = []
    for i in lines:
        pr.append(i[3])
    i = -1
    for p in pr:
        i += 1
        if p == 0 and i <= 10:
            continue
        elif p == 0:
            pr[i] = pr[i-1]
    ref_ma7 = get_average(pr[54:])
    ref_ma30 = get_average(pr[31:])
    return ref_ma7, ref_ma30, timestamp

def auto_right_side(pair, amount_ratio, avg_price, earn_ratio, loss_ratio):
    inst_id = trade.trusted_get_inst(pair)
    sell_price = str(float(avg_price) * (1 + float(earn_ratio)))
    buy_price = str(float(avg_price) * (1 - float(earn_ratio)))

    sell_loss_price = str(float(avg_price) * (1 - float(loss_ratio)))
    buy_loss_price = str(float(avg_price) * (1 + float(loss_ratio)))

    amount = str(float(trade.trusted_get_account_balance()[pair.split('USDT')[0]]) * float(amount_ratio))
    sell_id = trade.trusted_sell(inst_id, amount, sell_price)
    sell_time = time.time() + 3600
    print "selling~, id = "+str(sell_id)
    while True:
        last_price = float(trade.get_last_price(pair.split('USDT')[0]))
    	if ((last_price) < float(sell_loss_price)) or time.time() > sell_time:
            if trade.trusted_cancel_order(inst_id, sell_id):
                return "sell, stop loss or timeout"
    	elif trade.trusted_get_open_orders(inst_id, sell_id) == 'closed':
    		print "selled~"
    		break

    amount = str(float(trade.trusted_get_account_balance()['USDT']) * float(amount_ratio) / float(buy_price))
    buy_id = trade.trusted_buy(inst_id, amount, buy_price)
    buy_time = time.time() + 3600
    print "buying~, id = "+str(buy_id)
    while True:
        last_price = float(trade.get_last_price(pair.split('USDT')[0]))
        if ((last_price) > float(buy_loss_price)) or time.time() > buy_time:
            if trade.trusted_cancel_order(inst_id, buy_id):
                buy_price = str(float(last_price) * (1 - float(earn_ratio)))
                amount = (float(trade.trusted_get_account_balance()['USDT']) * float(amount_ratio) / float(buy_price))
                buy_id = trade.trusted_buy(inst_id, amount, buy_price)
                buy_time = time.time() + 3600
                print "buying~, id = "+str(buy_id)
                print "buy, stop loss or timeout"
    	elif trade.trusted_get_open_orders(inst_id, buy_id) == 'closed':
    		print "bought"
    		break
    return 'A great deal!'

def auto_side():
    print "~~Usage:"
    print "~~$python strategy.py"
    print "~~or:"
    print "~~$python strategy.py right LTCUSDT 0.0001 0.001 0.05"
    print "~~Ctrl+C to quit!"
    try:
        side, pair, amount_ratio, earn_ratio, loss_ratio = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    except IndexError:
        print "{left, right} {BTCUSDT, LTCUSDT} {amount_ratio} {earn_ratio} {loss_ratio}"
        order = raw_input("side pair amount earn_ratio loss_ratio:")
        side, pair, amount_ratio, earn_ratio, loss_ratio = order.split(" ")[0], order.split(" ")[1], order.split(" ")[2], order.split(" ")[3], order.split(" ")[4]

    while True:
        print "wait~"
        # avg_price = trade.get_last_price(pair.split('USDT')[0])
        pair = 'LTCUSDT'
        inst_id = trade.trusted_get_inst(pair)
        k_line_time = 3600
        ref_ma7, ref_ma30, timestamp = get_ma(inst_id, k_line_time)
        avg_price = ref_ma7
        # use neural network to predict the avg_price
        if side == 'left':
            print auto_left_side(pair, amount_ratio, avg_price, earn_ratio, loss_ratio)
        elif side == 'right':
            print auto_right_side(pair, amount_ratio, avg_price, earn_ratio, loss_ratio)
        else:
            print "error, running again~"

def test_api():
    pair = 'LTCUSD'
    inst_id = trade.trusted_get_inst(pair)
    k_line_time = 3600
    lines = trade.get_candle_ticks(inst_id, 60, k_line_time)['tick']
    print lines

def main():
    # simple_side()
    # auto_side()
    test_api()

if __name__ == '__main__':
    main()
