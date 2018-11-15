# coding=utf-8

import sys
import time
sys.path.append('..')

from pybtc.trade import trade_ok_futures_v3 as trade


def shift_time_v3(timestamp):
    format = '%Y-%m-%dT%H:%M:%SZ'
    value = time.localtime(timestamp)
    return time.strftime(format, value)


def test_candles():
    instrument_id = 'EOS-USD-181228'
    granularity = 180
    start = time.time()-granularity*2000
    end = time.time()
    candles = trade.candles(instrument_id, start, end, granularity)
    time_now = shift_time_v3(candles[-1][0]/1000)
    print(len(candles))
    print(time_now)
    print(candles[-10:])


def test_ticker():
    instrument_id = 'EOS-USD-181228'
    print(trade.ticker(instrument_id))


def test_book():
    instrument_id = 'EOS-USD-181228'
    size = 10
    print(trade.book(instrument_id, size))


def test_position():
    print(trade.position())


def test_get_leverage():
    instrument_id = 'BTC-USD-181228'
    rst = trade.get_leverage(instrument_id)
    print(rst)


def test_set_leverage():
    '''direction = 'long' '1'
    'short' '2'
    '''
    margin_mode = 'fixed'
    # margin_mode = 'crossed'
    currency = 'eos'
    instrument_id = 'EOS-USD-181228'
    direction = 'long'
    # direction = '1'
    leverage = '10'
    rst = trade.set_leverage(margin_mode, currency, instrument_id,
                           direction, leverage)
    print(rst)


def test_order():
    instrument_id = 'EOS-USD-181228'
    type = '1'
    price = '3.3'
    size = '1'
    margin_mode = 'fixed_mode'
    match_price = '0'
    leverage = '10'
    order_dict = trade.order(instrument_id, type, price, size,
                             match_price, leverage)
    print(order_dict)


def test_cancel_order():
    instrument_id = 'EOS-USD-181228'
    order_id = '1692899199260672'
    rst = trade.cancel_order(instrument_id, order_id)
    print(rst)


def test_orders():
    instrument_id = 'EOS-USD-181228'
    order_id = '1692899199260672'
    rst = trade.orders(instrument_id, order_id)
    print(rst)


def main():
    # test_candles()
    # test_ticker()
    # test_book()
    # test_position()
    # test_get_leverage()
    # test_set_leverage()
    test_order()
    # test_cancel_order()
    # test_orders()
    print('test pass')


if __name__ == '__main__':
    main()
