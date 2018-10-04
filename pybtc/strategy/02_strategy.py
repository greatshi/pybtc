# coding=utf-8


import sys
from pybtc.trade import trade as trade


def stop_loss():
    pass


def auto_right_side(coin, amount, avg_price, earn_ratio, loss_ratio):
    sell_price = str(float(avg_price) * (1 + float(earn_ratio)))
    buy_price = str(float(avg_price) * (1 - float(earn_ratio)))

    sell_loss_price = str(float(avg_price) * (1 - float(loss_ratio)))
    # buy_loss_price = str(float(buy_price) * (1 + float(loss_ratio)))

    sell_id = trade.trusted_sell(coin, amount, sell_price)
    print "selling~, id = "+sell_id
    while True:
        if float(trade.get_last_price(coin)) < float(sell_loss_price):
            if trade.trusted_cancel_order(sell_id):
                sell_id = trade.trusted_sell(coin, amount, sell_loss_price)
                print "stop loss, sell_id = "+sell_id
                return "stop loss"
        elif trade.trusted_fetch_order(sell_id) == 'closed':
            print "selled~"
            break
    buy_id = trade.trusted_buy(coin, amount, buy_price)
    print "buying~, id = "+buy_id
    while True:
        if trade.trusted_fetch_order(buy_id) == 'closed':
            print "bought"
            break
    return 'A great deal!'
        # elif float(trade.get_last_price(coin)) > float(buy_loss_price):
        #     if trade.trusted_cancel_order(buy_id):
        #         buy_id = trade.trusted_buy(coin, amount, buy_loss_price)
        #         print "stop loss, buy_id = "+buy_id
        #         return "stop loss"


def auto_left_side(coin, amount, avg_price, earn_ratio, loss_ratio):
    pass


def auto_side():
    print "~~Usage:"
    print "~~$python 02_strategy.py"
    print "~~or:"
    print "~~$python 02_strategy.py left btc 1 0.01 0.1"
    print "~~Ctrl+C to quit!"
    try:
        side, coin, amount, earn_ratio, loss_ratio = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    except IndexError:
        print "{left, right} {btc, eth, ltc, doge, ybc} {amount} {earn_ratio} {loss_ratio}"
        order = raw_input("side coin amount earn_ratio loss_ratio:")
        side, coin, amount, earn_ratio, loss_ratio = order.split(" ")[0], order.split(" ")[1], order.split(" ")[2], order.split(" ")[3], order.split(" ")[4]

    avg_price = trade.get_last_price(coin)

    while True:
        print "wait~"
        if side == 'left':
            print auto_left_side(coin, amount, avg_price, earn_ratio, loss_ratio)
        elif side == 'right':
            print auto_right_side(coin, amount, avg_price, earn_ratio, loss_ratio)
        else:
            print "error, running again~"


def main():
    auto_side()


if __name__ == '__main__':
    main()
