#!/usr/bin/env python
#coding=utf-8


import time
import pika
import pymongo


def set_user_pass():
    global rabbit_user
    with open('rabbitmq.pem', 'r') as f:
        rabbit_user = eval(f.read())
    return None


def listen_event():
    global rabbit_user
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

    print(' [*] waiting for trading events...')
    channel.start_consuming()


def callback(ch, method, properties, body):
    event_dict = eval(body)
    executor(event_dict)


def executor(event_dict):
    exchange = event_dict['exchange']
    if (exchange == 'okex_futures'):
        execute_okex_futures(event_dict)
    if (exchange == 'ut'):
        execute_ut(event_dict)


def execute_okex_futures(event_dict):
    global order_dict_list
    from pybtc.trade import trade_ok_futures_v3 as trade
    event_type = event_dict['event_type']
    if (event_type == 'event_send_order'):
        order_dict = event_dict['data']
        timestamp = order_dict['timestamp']
        # print('time_diff: {}'.format(time.time() - timestamp))
        if (time.time() > timestamp+5):
            print('{}, order: {}'.format('order 5s late', order_dict))
        if (time.time() > timestamp+15):
            print('{}, order: {}'.format('order timeout', order_dict))
            return None
        instrument_id = order_dict['instrument_id']
        order_type = order_dict['order_type']
        if (order_type == 'if_done_oco'):
            return execute_if_done_oco(order_dict)
        elif (order_type == 'going_long'):
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
        print('execute trade, type: {}, price: {}, size: {}'.format(
              type, price, size))

        order_id = trade.order(instrument_id, type, price, size,
                               match_price, leverage)
        print(order_id)


def execute_ut(event_dict):
    pass


def execute_if_done_oco(order_dict):
    try:
        with open('order_dict_list.txt', 'r') as f:
            order_dict_list = eval(f.read())
    except Exception as e:
        order_dict_list = []

    order_dict_list.append(order_dict)

    with open('order_dict_list.txt', 'w') as f:
        f.write(str(order_dict_list))

    return None


def main():
    set_user_pass()
    listen_event()
    print('test pass')


if __name__ == '__main__':
    main()
