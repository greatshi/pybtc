#coding=utf-8

import trade_ut as trade
# import api_ut as api
# import time
# import datetime
# import matplotlib.pyplot as plt
# import pandas as pd
# import logging

def test_sell(inst_id, qty, sell_price):
    sell_id = trade.trusted_sell(inst_id, qty, sell_price)
    return sell_id

def test_get_trade():
    price, qty, timestamp = trade.get_trades('LTCUSDT')
    print(len(price))
    plt.figure()
    plt.plot(timestamp, price)
    plt.show()

def test_account_balances():
    balance = trade.trusted_get_account_balance()
    print balance['USDT']
    print balance['LTC']

def test_log():
    logging.basicConfig(level=logging.WARNING,
                        filename='./log.txt',
                        filemode='w',
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    # use logging
    logging.info('this is a loggging info message')
    logging.debug('this is a loggging debug message')
    logging.warning('this is loggging a warning message')
    logging.error('this is an loggging error message')
    logging.critical('this is a loggging critical message')

def test_get_time():
    # pair = 'LTCUSDT' # 490590
    # inst_id = trade.trusted_get_inst(pair)
    inst_id = 490590
    # print inst_id
    print trade.get_realtime_ticks(inst_id)

def main():
    # BTCUSDT, ETHUSDT, LTCUSDT
    # test_log()
    i = 0
    while True:
        test_get_time()
        i += 1
        if i >10:
            break




if __name__ == '__main__':
    main()
