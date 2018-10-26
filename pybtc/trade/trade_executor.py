#!/usr/bin/env python
#coding=utf-8


import time
import pika


def get_user_pass():
    with open('rabbitmq.pem', 'r') as f:
        rabbit_user = eval(f.read())
    return rabbit_user


def listen_event():
    rabbit_user = get_user_pass()
    user_name = rabbit_user['username']
    pwd = rabbit_user['passwd']
    credentials = pika.PlainCredentials(user_name, pwd)
    connection = pika.BlockingConnection(
                     pika.ConnectionParameters('127.0.0.1', 5672,
                     '/', credentials))

    channel = connection.channel()
    channel.queue_declare(queue='trade')

    channel.basic_consume(callback,
                          queue='trade',
                          no_ack=True)

    print(' [*] waiting for events. to exit press CTRL+C')
    channel.start_consuming()


def callback(ch, method, properties, body):
    print('*'*20)
    event_dict = eval(body)
    # print(event_dict)
    executor(event_dict)


def executor(event_dict):
    exchange = event_dict['exchange']
    if (exchange == 'okex_futures'):
        execute_okex_futures(event_dict)
    if (exchange == 'ut'):
        execute_ut(event_dict)


def execute_okex_futures(event_dict):
    from pybtc.trade import trade_ok_futures_v3 as trade
    event_type = event_dict['event_type']
    if (event_type == 'event_send_order'):
        order_dict = event_dict['data']
        timestamp = order_dict['timestamp']
        # print('time_diff: {}'.format(time.time() - timestamp))
        if (time.time() > timestamp+5):
            print('{}, order: {}'.format('order timeout', order_dict))
            return None
        instrument_id = order_dict['instrument_id']
        order_type = order_dict['order_type']
        if (order_type == 'going_long'):
            type = '1'
        elif (order_type == 'going_short'):
            type = '2'
        elif (order_type == 'close_long'):
            type = '3'
        elif (order_type == 'close_short'):
            type = '4'
        price = order_dict['price']
        size = order_dict['amount']
        match_price = order_dict['match_price']
        leverage = order_dict['leverage']
        order_id = trade.order(instrument_id, type, price, size,
                               match_price, leverage)
        print(order_id)
        time.sleep(3)
        rst = trade.cancel_order(instrument_id, order_id)
        print(rst)
        time.sleep(3)
        rst = trade.orders(instrument_id, order_id)
        print(rst)


def execute_ut(event_dict):
    pass


def main():
    print('test pass')


if __name__ == '__main__':
    main()
