# coding=utf-8

import sys
import time
sys.path.append('..')

from pybtc.api import api_ok_futures_v3 as api


def test_candles():
    instrument_id = 'EOS-USD-181228'
    granularity = 60
    import urllib
    start = time.time()-granularity*2000
    end =  time.time()
    print(api.candles(instrument_id, start, end, granularity)[-10:])


def test_ticker():
    instrument_id = 'EOS-USD-181228'
    print(api.ticker(instrument_id))


def test_book():
    instrument_id = 'EOS-USD-181228'
    size = 10
    print(api.book(instrument_id, size))


def test_position():
    print(api.position())


def test_get_leverage():
    instrument_id = 'BTC-USD-181228'
    rst = api.get_leverage(instrument_id)
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
    direction = '1'
    leverage = '10'
    rst = api.set_leverage(margin_mode, currency, instrument_id,
                           direction, leverage)
    print(rst)


def test_order():
    instrument_id = 'EOS-USD-181228'
    type = '1'
    price = '4.1'
    size = '1'
    margin_mode = 'fixed_mode'
    match_price = '0'
    leverage = '10'
    order_dict = api.order(instrument_id, type, price, size, margin_mode,
                           match_price, leverage)
    print(order_dict)


def test_cancel_order():
    instrument_id = 'EOS-USD-181228'
    order_id = '1644900936662016'
    rst = api.cancel_order(instrument_id, order_id)
    print(rst)


def test_orders():
    instrument_id = 'EOS-USD-181228'
    order_id = '1644900936662016'
    rst = api.orders(instrument_id, order_id)
    print(rst)


def main():
    test_candles()
    # test_ticker()
    # test_book()
    # test_position()
    # test_get_leverage()
    # test_set_leverage()
    # test_order()
    # test_cancel_order()
    # test_orders()
    print('test pass')


if __name__ == '__main__':
    main()
