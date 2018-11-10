# !/usr/bin/env python
# coding=utf8


import time
import pika


def get_user_pass():
    with open('rabbitmq.pem', 'r') as f:
        rabbit_user = eval(f.read())
    return rabbit_user


def send_event(event_dict):
    rabbit_user = get_user_pass()
    user_name = rabbit_user['username']
    pwd = rabbit_user['passwd']
    credentials = pika.PlainCredentials(user_name, pwd)
    connection = pika.BlockingConnection(
                     pika.ConnectionParameters('127.0.0.1', 5672,
                     '/', credentials))

    channel = connection.channel()
    channel.exchange_declare(exchange='quote', exchange_type='fanout')

    # channel.queue_declare(queue='')
    channel.basic_publish(exchange='quote',
                          routing_key='',
                          body=str(event_dict))
    connection.close()


def okex_futures_quote():
    from pybtc.trade import trade_ok_futures_v3 as trade

    instrument_id = 'EOS-USD-181228'
    # granularity = 60
    granularity = 180
    start = time.time() - granularity*2000
    end = time.time()

    candles_bar = trade.candles(instrument_id, start, end, granularity)
    begin_timestamp = int(candles_bar[-1][0])

    while True:
        start = time.time() - granularity*2000
        end = time.time()
        candles_bar = trade.candles(instrument_id, start, end, granularity)
        new_timestamp = int(candles_bar[-1][0])
        if begin_timestamp < new_timestamp:
            begin_timestamp = new_timestamp
            event_dict = {
                'event_type': 'event_bar',
                'exchange': 'okex_futures',
                'instrument_id': instrument_id,
                'bar_type': '3min',
                'data': candles_bar
            }
            send_event(event_dict)
            # print('send event_bar')
        event_dict = {
            'event_type': 'event_tick',
            'exchange': 'okex_futures',
            'instrument_id': instrument_id,
            'tick_type': '',
            'data': str({'time': time.time(),
                         'price': candles_bar[-1][4]})
        }
        send_event(event_dict)
        # print('send event_tick')
        time.sleep(0.3)


def main():
    okex_futures_quote()


if __name__ == '__main__':
    main()
