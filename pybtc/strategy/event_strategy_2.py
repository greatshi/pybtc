#!/usr/bin/env python
#coding=utf-8

import time
import pika


def set_user_pass():
    global rabbit_user
    with open('rabbitmq.pem', 'r') as f:
        rabbit_user = eval(f.read())


def send_event(event_dict):
    '''send event to trade execution module
    '''
    global rabbit_user
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
    global rabbit_user
    user_name = rabbit_user['username']
    pwd = rabbit_user['passwd']
    credentials = pika.PlainCredentials(user_name, pwd)
    connection = pika.BlockingConnection(
                     pika.ConnectionParameters('127.0.0.1', 5672,
                     '/', credentials))

    channel = connection.channel()
    # channel.queue_declare(queue='quote')
    channel.exchange_declare(exchange='quote', exchange_type='fanout')
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='quote',queue=queue_name)

    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)

    print(' [*] waiting for quote events...')
    channel.start_consuming()


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
        if (bar_type == '3min'):
            future_p_eos(event_dict)
    elif ((event_type == 'event_tick') and
        (exchange == 'okex_futures') and
        (instrument_id == 'EOS-USD-190329')):
        now = time.time()
        data = eval(event_dict['data'])
        print('2: {}, offset: {}'.format(data, now - data['time']))
        # on_tick()
        pass

status = 'close_long'


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


def shift_time(timestamp):
    tz = time.timezone
    if tz/3600 == 5:
        timestamp = timestamp + tz + 28800 - 3600
    format = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(timestamp)
    return time.strftime(format, value)

def send_order(instrument_id, price, amount, order_type, match_price):
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


def future_p_eos(event_dict):
    global status
    instrument_id = event_dict['instrument_id']
    candles_bar = event_dict['data']
    ms_s = compute_ma(candles_bar, 7)
    ms_l = compute_ma(candles_bar, 30)
    time_now = shift_time(ms_s[-2][0]/1000)
    print('2: time: {}, ma_s: {}, ma_l: {}'.format(
          time_now, ms_s[-2][1], ms_l[-2][1]))
    if ((status == 'close_long') and
        (ms_s[-2][1] < ms_l[-2][1]) and
        (ms_s[-3][1] > ms_l[-3][1])):
    # if (status == 'close_long'):
        price = str(float(candles_bar[-2][4]))
        amount = '1'
        order_type = 'going_long'
        match_price = '0'
        send_order(instrument_id, price, amount, order_type, match_price)
        status = 'going_long'
        print('time: {}, status: {}'.format(time_now, status))
    elif ((status == 'going_long') and
        (ms_s[-2][1] > ms_l[-2][1]) and
        (ms_s[-3][1] < ms_l[-3][1])):
    # elif (status == 'going_long'):
        price = str(float(candles_bar[-2][4]))
        amount = '1'
        order_type = 'close_long'
        match_price = '0'
        send_order(instrument_id, price, amount, order_type, match_price)
        status = 'close_long'
        print('time: {}, status: {}'.format(time_now, status))


def main():
    set_user_pass()
    listen_event()


if __name__ == '__main__':
    main()
