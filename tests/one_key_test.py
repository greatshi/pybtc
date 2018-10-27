#!/usr/bin/env python
#coding=utf-8


import time
import sys
sys.path.append('..')

from multiprocessing import Process

from pybtc.quote import gen_quote
from pybtc.strategy import event_strategy
from pybtc.trade import trade_executor


def test_gen_quote():
    gen_quote.okex_futures_quote()


def test_event_strategy():
    event_strategy.listen_event()


def test_trade_executor():
    trade_executor.listen_event()


def process_monitor(process_dict_list):
    while True:
        print('monitor running')
        for process_dict in process_dict_list:
            process = process_dict['process']
            if (process.is_alive() is False):
                name = process_dict['name']
                if (name == 'test_gen_quote'):
                    p1 = Process(target=test_gen_quote, args=())
                    p1.start()
                    process_dict['process'] = p1
                    print('name: {}, new_pid: {}'.format(
                          name, p1.pid))
                elif (name == 'test_event_strategy'):
                    p2 = Process(target=test_event_strategy, args=())
                    p2.start()
                    process_dict['process'] = p2
                    print('name: {}, new_pid: {}'.format(
                          name, p2.pid))
                elif (name == 'test_trade_executor'):
                    p3 = Process(target=test_trade_executor, args=())
                    p3.start()
                    process_dict['process'] = p3
                    print('name: {}, new_pid: {}'.format(
                          name, p3.pid))
            else:
                pass
        time.sleep(10)


def main():
    p1 = Process(target=test_gen_quote, args=())
    p2 = Process(target=test_event_strategy, args=())
    p3 = Process(target=test_trade_executor, args=())
    p1.start()
    p2.start()
    p3.start()
    process_dict_list = [{'name': 'test_gen_quote', 'process': p1},
                         {'name': 'test_event_strategy', 'process': p2},
                         {'name': 'test_trade_executor', 'process': p3}]
    print('p1: {}, p2: {}, p3: {}'.format(p1.pid, p2.pid, p3.pid))

    process_monitor(process_dict_list)


if __name__ == '__main__':
    main()
