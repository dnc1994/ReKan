# -*- encoding:utf-8 -*-
import sys
from gen_couplets import gen_couplet


def api_wrap():
    # todo: encoding
    first_half = sys.argv[1]
    results = gen_couplet(first_half)
    for result in results:
        print result


if __name__ == '__main__':
    api_wrap()
