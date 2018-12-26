# coding=utf-8

import sys
sys.path.append('..')


from pybtc.trade import trade_executor


def test_trade_executor():
    trade_executor.main()


def main():
    test_trade_executor()


if __name__ == '__main__':
    main()
