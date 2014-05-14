import eventlet
eventlet.monkey_patch()

import argparse
import time
import re
import requests
from collections import defaultdict


HR = '-' * 79
PARAM_PATTERN = r'(?P<key>[^=]+)=(?P<value>.+)'


def fetch(request_id, args, params):
    try:
        if args.method == 'GET':
            r = requests.get(args.url, params=params, timeout=args.timeout)
        else:
            r = requests.post(args.url, data=params, timeout=args.timeout)
    except requests.exceptions.ConnectionError:
        return (-2, 0)
    except requests.exceptions.Timeout:
        return (-1, 0)

    return (r.status_code, r.elapsed.total_seconds())


def parse_parameters(args):
    params = {}

    if args.paramfile:
        with open(args.paramfile, 'r') as fh:
            args.params += [_.rstrip('\r\n') for _ in fh.readlines()]

    if args.params:
        for param in args.params:
            m = re.match(PARAM_PATTERN, param)
            if m:
                params[m.group('key')] = m.group('value')

    return params


def main():
    parser = argparse.ArgumentParser(
        description='Testing multiple HTTP request on green thread'
    )

    parser.add_argument('-u', dest='url', required=True,
                        help='URL to be tested')
    parser.add_argument('-c', dest='concurrency', default=10,
                        help='Number of threads')
    parser.add_argument('-n', dest='requests', default=100,
                        help='Number of requests')
    parser.add_argument('-t', dest='timeout', default=5,
                        help='Timeout limit in seconds')
    parser.add_argument('-p', dest='params', nargs='*',
                        help='Parameters on POST request(in key=value format)')
    parser.add_argument('-f', dest='paramfile',
                        help='File contains parameters(multiple key=value)')
    parser.add_argument('-m', dest='method', default='GET',
                        choices=['GET', 'POST'],
                        help='Which method to be used (GET,POST)')

    args = parser.parse_args()
    params = parse_parameters(args)

    # Running information
    print(HR)
    print('Run with {} threads, {} requests, timeout in {} second(s).'.format(
        args.concurrency, args.requests, args.timeout))
    print(HR)

    # Let's begin!
    pool = eventlet.GreenPool(int(args.concurrency))
    status_count = defaultdict(int)
    status_elapsed = defaultdict(int)

    start = time.time()

    for status, elapsed in pool.imap(lambda x: fetch(x, args, params),
                                     xrange(int(args.requests))):
        status_count[status] += 1
        status_elapsed[status] += elapsed

    elapsed = time.time() - start

    # Print out results
    print("STATUS\tCOUNT\tAVERAGE")
    print(HR)
    for status, count in status_count.iteritems():
        if status > 0:
            print("{}\t{}\t{:.2f}ms".format(
                status, count, status_elapsed[status] * 1000 / count
            ))

    # Print errors and summary
    print(HR)

    if status_count.get(-1):
        print('>>> {} request(s) timed out'.format(status_count.get(-1)))

    if status_count.get(-2):
        print('>>> {} request(s) just failed'.format(status_count.get(-2)))

    print('total time elapsed {:.4f}s'.format(elapsed))


if __name__ == '__main__':
    main()
