#coding=utf-8

import trade_ut as trade
import sys

def left_side_method(pair, amount, buy_price, sell_price):
    buy_id = trade.trusted_buy(pair, amount, buy_price)
    print "buying~, id = "+buy_id
    if trade.test_order_closed(buy_id,0.1):
        print "bought~"
        sell_id = trade.trusted_sell(pair, amount, sell_price)
        print "selling~, id = "+sell_id
        if trade.test_order_closed(sell_id,3):
            return 'A great deal!'

def right_side_method(pair, amount, buy_price, sell_price):
    sell_id = trade.trusted_sell(pair, amount, sell_price)
    print "selling~, id = "+sell_id
    if trade.test_order_closed(sell_id,0.1):
        print "selled~"
        buy_id = trade.trusted_buy(pair, amount, buy_price)
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
    while True:
        print "wait~"
        if side == 'left':
            print left_side_method(pair, amount, buy_price, sell_price)
        elif side == 'right':
            print right_side_method(pair, amount, buy_price, sell_price)
        else:
            print "error, running again~"
def main():
    simple_side()

if __name__ == '__main__':
    main()
