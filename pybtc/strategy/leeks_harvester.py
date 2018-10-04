# coding=utf-8


import sys
import time
import datetime
from pybtc.trade import trade_ut as trade
# import pandas as pd


# def get_ma_baks(inst_id):
#     df = pd.DataFrame(trade.get_candle_ticks(inst_id, 7, 60)['tick'], columns=['zero', 'one', 'two', 'three', 'four','five'])
#     ref_ma7 = df[df.one > 0].ix[::,3].mean()
#     df = pd.DataFrame(trade.get_candle_ticks(inst_id, 30, 60)['tick'], columns=['zero', 'one', 'two', 'three', 'four','five'])
#     ref_ma30 = df[df.one > 0].ix[::,3].mean()
#     return ref_ma7, ref_ma30


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


def ma_strategy(pair, k_line_time, amount_ratio='0.97', earn_ratio='0.0001'):
    inst_id = trade.trusted_get_inst(pair)
    ref_ma7, ref_ma30, timestamp = get_ma(inst_id, k_line_time)
    print 'ma7: ' + str(ref_ma7) + 'ma30: ' + str(ref_ma30)

    while True:
        while True:
            new_ts = trade.get_candle_ticks(inst_id, 2, k_line_time)['tick'][-1][-1]
            if new_ts != timestamp:
                print new_ts
                break
            else:
                time.sleep(3)

        ma7, ma30, timestamp = get_ma(inst_id, k_line_time)
        print 'ma7: ' + str(ma7) + 'ma30: ' + str(ma30)

        if ma7 > ma30 and ref_ma7 <= ref_ma30:
            last_price = float(trade.get_last_price(pair.split('USDT')[0]))
            buy_price = str(float(last_price) * (1 - float(earn_ratio)))
            amount = str(float(trade.trusted_get_account_balance()['USDT']) * float(amount_ratio) / float(buy_price))
            buy_id = trade.trusted_buy(inst_id, amount, buy_price)
            print "buying~, id = "+str(buy_id)
            buy_time = time.time() + 5
            while True:
                if time.time() > buy_time:
                    if trade.trusted_cancel_order(inst_id, buy_id):
                        last_price = float(trade.get_last_price(pair.split('USDT')[0]))
                        buy_price = str(float(last_price) * (1 - float(earn_ratio)))
                        amount = (float(trade.trusted_get_account_balance()['USDT']) * float(amount_ratio) / float(buy_price))
                        buy_id = trade.trusted_buy(inst_id, amount, buy_price)
                        buy_time = time.time() + 5
                        print "buying~, id = "+str(buy_id)
                elif trade.trusted_get_open_orders(inst_id, buy_id) == 'closed':
                    print "bought"
                    break
        if ma7 < ma30 and ref_ma7 >= ref_ma30:
            last_price = float(trade.get_last_price(pair.split('USDT')[0]))
            sell_price = str(float(last_price) * (1 + float(earn_ratio)))
            amount = str(float(trade.trusted_get_account_balance()[pair.split('USDT')[0]]) * float(amount_ratio))
            sell_id = trade.trusted_sell(inst_id, amount, sell_price)
            sell_time = time.time() + 5
            print "selling~, id = "+str(sell_id)
            while True:
                if time.time() > sell_time:
                    if trade.trusted_cancel_order(inst_id, sell_id):
                        last_price = float(trade.get_last_price(pair.split('USDT')[0]))
                        sell_price = str(float(last_price) * (1 + float(earn_ratio)))
                        amount = str(float(trade.trusted_get_account_balance()[pair.split('USDT')[0]]) * float(amount_ratio))
                        sell_id = trade.trusted_sell(inst_id, amount, sell_price)
                        sell_time = time.time() + 5
                        print "selling~, id = "+str(sell_id)
                elif trade.trusted_get_open_orders(inst_id, sell_id) == 'closed':
                    print "selled~"
                    break

        ref_ma7, ref_ma30 = ma7, ma30


def main():
    pair = 'LTCUSDT'
    k_line_time = 300
    ma_strategy(pair, k_line_time)
    # while True:
    #     print get_ma('LTCUSDT', 300)
    #     time.sleep(1)


if __name__ == '__main__':
    main()
