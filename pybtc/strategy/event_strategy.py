#!/usr/bin/env python
#coding=utf-8

import time
import pika


status = 'close_long'


def get_user_pass():
    with open('rabbitmq.pem', 'r') as f:
        rabbit_user = eval(f.read())
    return rabbit_user


def send_event(event_dict):
    '''send event to trade execution module
    '''
    rabbit_user = get_user_pass()
    user_name = rabbit_user['username']
    pwd = rabbit_user['passwd']
    credentials = pika.PlainCredentials(user_name, pwd)
    connection = pika.BlockingConnection(
                     pika.ConnectionParameters('127.0.0.1', 5672,
                     '/', credentials))
    channel = connection.channel()
    channel.queue_declare(queue='trade')
    channel.basic_publish(exchange='',
                          routing_key='trade',
                          body=str(event_dict))
    connection.close()


def listen_event():
    rabbit_user = get_user_pass()
    user_name = rabbit_user['username']
    pwd = rabbit_user['passwd']
    credentials = pika.PlainCredentials(user_name, pwd)
    connection = pika.BlockingConnection(
                     pika.ConnectionParameters('127.0.0.1', 5672,
                     '/', credentials))

    channel = connection.channel()
    channel.queue_declare(queue='quote')

    channel.basic_consume(callback,
                          queue='quote',
                          no_ack=True)

    print(' [*] waiting for events. to exit press CTRL+C')
    channel.start_consuming()


def callback(ch, method, properties, body):
    print('*'*20)
    event_dict = eval(body)
    strategy(event_dict)


def strategy(event_dict):
    # call strategys
    event_type = event_dict['event_type']
    exchange = event_dict['exchange']
    instrument_id = event_dict['instrument_id']
    bar_type = event_dict['bar_type']
    if ((event_type == 'event_bar') and
        (exchange == 'okex_futures') and
        (instrument_id == 'EOS-USD-181228') and
        (bar_type == '3min')):
        future_p_eos(event_dict)
    else:
        pass


def future_p_eos(event_dict):
    global status
    instrument_id = event_dict['instrument_id']
    candles_bar = event_dict['data']
    print(candles_bar[-2])
    if (status == 'close_long'):
        print('ooooooo')
        price = str(float(candles_bar[-2][4])-1.5)
        amount = '1'
        order_type = 'going_long'
        match_price = '0'
        leverage = '10'
        order_dict = {
            'instrument_id': instrument_id,
            'timestamp': time.time(),
            'price': price,
            'amount': amount,
            'order_type': order_type,
            'match_price': match_price,
            'leverage': leverage,
        }
        event_dict = {
            'event_type': 'event_send_order',
            'exchange': 'okex_futures',
            'instrument_id': instrument_id,
            'data': order_dict
        }
        send_event(event_dict)
        status = 'going_long'
    elif (status == 'going_long'):
        status = 'close_long'
        print('xxxxxxx')


def main():
    listen_event()


if __name__ == '__main__':
    main()
