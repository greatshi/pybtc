#coding=utf-8

import trade_ok as trade
import time

def compute_ma(klines, bars):
    ma_lines = []
    for i in range(len(klines)-1, bars-1-1, -1):
        timestamp = klines[i][0]
        bars_line = klines[i-bars+1:i+1]
        sum = 0
        for j in bars_line:
            sum += j[4]
        ma_lines.append([timestamp, sum/float(bars)])
    ma_lines.reverse()
    return ma_lines

def ma_strategy(coin, type, size, since, ma_s, ma_l, earn_ratio, loss_ratio):
    status = 'selled'
    klines = trade.get_kline(coin, type, size, since)
    begin_timestamp = klines[-1][0]
    while True:
        klines = trade.get_kline(coin, type, size, since)
        if begin_timestamp < klines[-1][0]:
            begin_timestamp = klines[-1][0]
            ma_s_lines = compute_ma(klines, ma_s)
            ma_l_lines = compute_ma(klines, ma_l)
            last_price = klines[-2][4]
            print 'begin_timestamp'+ str(begin_timestamp)

            usdt = trade.get_userinfo()['info']['funds']['free']['usdt']

            if (ma_s_lines[-2][1] >= ma_l_lines[-2][1]) and (ma_s_lines[-3][1] < ma_l_lines[-3][1]) and status == 'selled':
                # buy
                buy_id = trade.trusted_trade(coin, 'buy_market', usdt, '')
                status = 'bought'
                b_num = trade.get_userinfo()['info']['funds']['free'][coin]
                buy_price = trade.trusted_fetch_order(coin, buy_id)['orders'][0]['price']
                sell_id_ins = trade.trusted_sell(coin, buy_price*(1+earn_ratio), b_num)
            elif status == 'bought':
                if (trade.trusted_fetch_order(coin, sell_id_ins)['orders'][0]['status'] == 2):
                    status = 'selled'
                elif(last_price < buy_price*(1-loss_ratio) and status == 'bought'):
                    # sell stop loss
                    trade.trusted_cancel_order(coin, sell_id_ins)
                    b_num = trade.get_userinfo()['info']['funds']['free'][coin]
                    sell_id = trade.trusted_trade(coin, 'sell_market', '', b_num)
                    status = 'selled'
        else:
            time.sleep(5)

def test_ma_strategy(coin, type, size, since, ma_s, ma_l, earn_ratio, loss_ratio):
    status = 'selled'
    klines = trade.get_kline(coin, type, size, since)
    begin_timestamp = klines[-1][0]
    while True:
        klines = trade.get_kline(coin, type, size, since)
        if klines[-1][0] > begin_timestamp:
            begin_timestamp = klines[-1][0]
            ma_s_lines = compute_ma(klines, ma_s)
            ma_l_lines = compute_ma(klines, ma_l)
            last_price = klines[-2][4]

            usdt = trade.get_userinfo()['info']['funds']['free']['usdt']
            print 'new timestamp: '+ str(begin_timestamp)
            print ma_s_lines[-2][0], ma_l_lines[-2][0]
            print ma_s_lines[-3][0], ma_l_lines[-3][0]
            print usdt

        else:
            time.sleep(5)

def main():
    coin = 'btc'
    type = '15min'
    size = '100'
    since = ''
    ma_s = 23
    ma_l = 68
    earn_ratio = 0.009
    loss_ratio = 0.009
    ma_strategy(coin, type, size, since, ma_s, ma_l, earn_ratio, loss_ratio)

    # type = '1min'
    # test_ma_strategy(coin, type, size, since, ma_s, ma_l, earn_ratio, loss_ratio)

if __name__ == '__main__':
    main()
