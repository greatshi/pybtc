# coding=utf-8

import sys
sys.path.append('..')

from pybtc.quote import gen_quote


def test_gen_quote():
    gen_quote.main()


def main():
    test_gen_quote()


if __name__ == '__main__':
    main()
