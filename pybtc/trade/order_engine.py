#!/usr/bin/env python
#coding=utf-8


import time
import pika
import pymongo
from threading import Thread

from pybtc.strategy import trade_util_me as trade_util
from pybtc.trade import trade_ok_futures_v3 as trade


def on_tick(tick):
    global tick_counter
    global open_price
    global close_price
    global quantity

    if len(str(int(tick['time']))) == 13:
        time_now = trade_util.shift_time(tick['time']/1000)
    else:
        time_now = trade_util.shift_time(tick['time'])

    last_price = float(tick['price'])
    # print(last_price, time_now)
    try:
        with open('order_dict_list.txt', 'r') as f:
            order_dict_list = eval(f.read())
    except Exception as e:
        order_dict_list = []

    if (len(order_dict_list) > 0):
        timestamp = int(time.time())
        for order_dict in order_dict_list:
            status = order_dict['status']
            direct = order_dict['direct']
            coin = order_dict['instrument_id']
            if ((status == 'new')):
                print(status, order_dict)
                open_price = order_dict['price']
                quantity = order_dict['amount']
                if (direct == 'long'):
                    open_order_id = going_long(coin)
                elif (direct == 'short'):
                    open_order_id = going_short(coin)
                order_dict['open_order_id'] = open_order_id
                order_dict['status'] = 'wait'
            elif (status == 'wait'):
                print(status, order_dict)
                open_order_id = order_dict['open_order_id']
                status_order = order_status(coin, open_order_id)
                if (status_order == 2):
                    close_price = order_dict['profit_target']
                    quantity = order_dict['amount']
                    if (direct == 'long'):
                        close_order_id = close_long(coin)
                    elif (direct == 'short'):
                        close_order_id = close_short(coin)
                    order_dict['close_order_id'] = close_order_id
                    order_dict['status'] = 'open'
                elif (status_order == 0):
                    time_valid = order_dict['time_valid'] + order_dict['timestamp']
                    # print(timestamp, time_valid)
                    if (timestamp > time_valid):
                        open_order_id = order_dict['open_order_id']
                        rst = trade.cancel_order(coin, open_order_id)
                    else:
                        pass
                elif (status_order == -1):
                    order_dict['status'] = 'drop'
            elif (status == 'open'):
                print(status, order_dict)
                close_order_id = order_dict['close_order_id']
                status_order = order_status(coin, close_order_id)
                if (status_order == 2):
                    order_dict['status'] = 'close'
                elif (status_order == 0):
                    stop_loss_price = order_dict['stop_loss']
                    if (direct == 'long'):
                        if (last_price < stop_loss_price):
                            close_order_id = order_dict['close_order_id']
                            quantity = order_dict['amount']
                            rst = trade.cancel_order(coin, close_order_id)
                            if (rst == True):
                                stop_loss_order_id = market_close_long(coin)
                                order_dict['stop_loss_order_id'] = stop_loss_order_id
                            else:
                                pass
                        else:
                            pass
                    elif (direct == 'short'):
                        if (last_price > stop_loss_price):
                            close_order_id = order_dict['close_order_id']
                            quantity = order_dict['amount']
                            rst = trade.cancel_order(coin, close_order_id)
                            if (rst == True):
                                stop_loss_order_id = market_close_short(coin)
                                order_dict['stop_loss_order_id'] = stop_loss_order_id
                            else:
                                pass
                        else:
                            pass
    else:
        pass
    with open('order_dict_list.txt', 'w') as f:
        f.write(str(order_dict_list))


def order_status(coin, order_id):
    order_dict = trade.orders(coin, order_id)
    if ('order_id' not in order_dict):
        order_dict['status'] = 0
    else:
        pass
    return int(order_dict['status'])


def going_long(coin):
    global open_price
    global quantity
    order_dict = {
        'instrument_id': coin,
        'timestamp': time.time(),
        'price': open_price,
        'amount': quantity,
        'order_type': 'going_long',
        'match_price': '0',
        'leverage': '10',
    }
    return send_order(order_dict)


def close_long(coin):
    global close_price
    global quantity
    order_dict = {
        'instrument_id': coin,
        'timestamp': time.time(),
        'price': close_price,
        'amount': quantity,
        'order_type': 'close_long',
        'match_price': '0',
        'leverage': '10',
    }
    return send_order(order_dict)


def market_close_long(coin):
    global close_price
    global quantity
    order_dict = {
        'instrument_id': coin,
        'timestamp': time.time(),
        'price': close_price,
        'amount': quantity,
        'order_type': 'close_long',
        'match_price': '1',
        'leverage': '10',
    }
    return send_order(order_dict)


def going_short(coin):
    global open_price
    global quantity
    order_dict = {
        'instrument_id': coin,
        'timestamp': time.time(),
        'price': open_price,
        'amount': quantity,
        'order_type': 'going_short',
        'match_price': '0',
        'leverage': '10',
    }
    return send_order(order_dict)


def close_short(coin):
    global close_price
    global quantity
    order_dict = {
        'instrument_id': coin,
        'timestamp': time.time(),
        'price': close_price,
        'amount': quantity,
        'order_type': 'close_short',
        'match_price': '0',
        'leverage': '10',
    }
    return send_order(order_dict)


def market_close_short(coin):
    global close_price
    global quantity
    order_dict = {
        'instrument_id': coin,
        'timestamp': time.time(),
        'price': close_price,
        'amount': quantity,
        'order_type': 'close_short',
        'match_price': '1',
        'leverage': '10',
    }
    return send_order(order_dict)


def set_user_pass():
    global rabbit_user
    with open('rabbitmq.pem', 'r') as f:
        rabbit_user = eval(f.read())


# def send_event(event_dict):
#     '''send event to trade execution module
#     '''
#     global rabbit_user
#
#     user_name = rabbit_user['username']
#     pwd = rabbit_user['passwd']
#     credentials = pika.PlainCredentials(user_name, pwd)
#     connection = pika.BlockingConnection(
#                      pika.ConnectionParameters('127.0.0.1', 5672,
#                      '/', credentials))
#     channel = connection.channel()
#     channel.queue_declare(queue='trade')
#     channel.basic_publish(exchange='',
#                           routing_key='trade',
#                           body=str(event_dict))
#     connection.close()


def get_connection():
    global rabbit_user
    global connection
    global connection_setup
    user_name = rabbit_user['username']
    pwd = rabbit_user['passwd']
    credentials = pika.PlainCredentials(user_name, pwd)
    connection = pika.BlockingConnection(
                     pika.ConnectionParameters('127.0.0.1', 5672,
                     '/', credentials))


def listen_event():
    global connection
    channel = connection.channel()
    channel.exchange_declare(exchange='quote', exchange_type='fanout')
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='quote', queue=queue_name)

    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)

    print(' [*] waiting for quote events...')
    connection_setup = 1
    channel.start_consuming()


def keep_connection_alive():
    global connection
    while True:
        try:
            connection.process_data_events()
        except Exception as e:
            get_connection()
            print('reconnect...')
        time.sleep(60)


def callback(ch, method, properties, body):
    event_dict = eval(body)
    strategy(event_dict)


def strategy(event_dict):
    # call strategys
    event_type = event_dict['event_type']
    exchange = event_dict['exchange']
    instrument_id = event_dict['instrument_id']
    if ((event_type == 'event_bar') and
        (exchange == 'okex_futures') and
        (instrument_id == 'EOS-USD-190329')):
        bar_type = event_dict['bar_type']
        if (bar_type == '1hour'):
            # bars = event_dict['data']
            # on_bar(bars)
            pass
    elif ((event_type == 'event_tick') and
        (exchange == 'okex_futures') and
        (instrument_id == 'EOS-USD-190329')):
        tick = eval(event_dict['data'])
        on_tick(tick)
        pass


def send_order(order_dict):
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
    print('execute trade, type: {}, price: {}, size: {}'.format(
          type, price, size))

    order_id = trade.order(instrument_id, type, price, size,
                           match_price, leverage)
    return order_id


# def send_order(order_dict):
#     event_dict = {
#         'event_type': 'event_send_order',
#         'exchange': 'okex_futures',
#         'instrument_id': order_dict['instrument_id'],
#         'data': order_dict
#     }
#     send_event(event_dict)


def main():
    global coin
    global quantit
    global tick_counter
    global connection_setup

    connection_setup = 0

    coin = 'EOS-USD-190329'
    quantity = 1
    tick_counter = 0

    set_user_pass()
    get_connection()

    # listen_event()

    t_1 = Thread(target=listen_event, args=())
    t_2 = Thread(target=keep_connection_alive, args=())
    t_1.start()
    t_2.start()


if __name__ == '__main__':
    main()
