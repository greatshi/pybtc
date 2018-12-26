# coding=utf-8

import os
import sys
sys.path.append('..')


from pybtc.trade import order_engine


def test_order_engine():
    try:
        order_engine.main()
    except (KeyboardInterrupt):
        filename = os.path.basename(__file__)
        print(' Stop {} !'.format(filename))


def main():
    test_order_engine()


if __name__ == '__main__':
    main()
