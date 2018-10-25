# coding=utf-8

import sys
sys.path.append('..')

from pybtc.strategy import event_strategy


def test_event_strategy():
    event_strategy.listen_event()


def main():
    test_event_strategy()


if __name__ == '__main__':
    main()
