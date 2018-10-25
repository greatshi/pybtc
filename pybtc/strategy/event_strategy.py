#!/usr/bin/env python
#coding=utf-8

import pika


def send_event(event_dict):
    user_name = ''
    pwd = ''
    credentials = pika.PlainCredentials(user_name, pwd)
    connection = pika.BlockingConnection(
                     pika.ConnectionParameters('127.0.0.1', 5672,
                     '/', credentials))
    channel = connection.channel()
    channel.queue_declare(queue='quote')
    channel.basic_publish(exchange='',
                          routing_key='quote',
                          body=str(event_dict))
    connection.close()


def listen_event():
    user_name = ''
    pwd = ''
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
    instrument_id = event_dict['instrument_id']
    bar_type = event_dict['bar_type']
    if ((event_type == 'event_bar') and
        (instrument_id == 'EOS-USD-181228') and
        (bar_type == '3min')):
        future_p_macd(event_dict)
    else:
        pass


def future_p_macd(event_dict):
    candles_bar = event_dict['data']
    print(candles_bar[-2])
    if ('balabala...' == '...')
        order_dict = {}
        event_dict = {
            'event_type': 'event_order',
            'instrument_id': instrument_id,
            'data': order_dict
        }
        send_event(event_dict)


def main():
    listen_event()


if __name__ == '__main__':
    main()
