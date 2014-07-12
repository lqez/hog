import eventlet
eventlet.monkey_patch()

import argparse
import re
import requests
import sys
import time
from collections import defaultdict


class Hog(object):
    def __init__(self, callback=None):
        self.callback = callback

    def fetch(self):
        elapsed = 0

        try:
            if self.method == 'GET':
                r = requests.get(
                    self.url, params=self.params, timeout=self.timeout
                )
            else:
                r = requests.post(
                    self.url, data=self.params, timeout=self.timeout
                )

            status = r.status_code
            elapsed = r.elapsed.total_seconds()
        except requests.exceptions.ConnectionError:
            status = -2
        except requests.exceptions.Timeout:
            status = -1

        self.status_count[status] += 1
        self.status_elapsed[status].append(elapsed)

        if self.callback:
            self.callback(self.status_count, self.requests)

    def run(self, url, params=None, method='GET',
            timeout=5, concurrency=10, requests=100, limit=0):
        self.url = url
        self.params = params
        self.method = method
        self.timeout = timeout
        self.requests = requests
        self.status_count = defaultdict(int)
        self.status_elapsed = defaultdict(list)

        pool = eventlet.GreenPool(int(concurrency))

        if limit == 0:
            for _ in pool.imap(lambda x: self.fetch(),
                               xrange(int(requests))):
                pass
        else:
            interval = 1.0 / limit
            for i in xrange(int(requests)):
                pool.spawn_n(self.fetch)
                time.sleep(interval)

        pool.waitall()

        return (self.status_count, self.status_elapsed)


def run(url, params=None, method='GET',
        timeout=5, concurrency=10, requests=100, limit=0, callback=None):
    return Hog(callback) \
        .run(url, params, method, timeout, concurrency, requests, limit)


def parse_parameters(args):
    params = {}

    if args.paramfile:
        with open(args.paramfile, 'r') as fh:
            args.params += [_.rstrip('\r\n') for _ in fh.readlines()]

    if args.params:
        for param in args.params:
            m = re.match(r'(?P<key>[^=]+)=(?P<value>.+)', param)
            if m:
                params[m.group('key')] = m.group('value')

    return params


def get_parser():
    parser = argparse.ArgumentParser(
        description='Sending multiple `HTTP` requests `ON` `GREEN` thread'
    )

    parser.add_argument(dest='url',
                        help='URL to be tested')
    parser.add_argument('-c', dest='concurrency', default=10,
                        help='Number of threads')
    parser.add_argument('-n', dest='requests', default=100,
                        help='Number of requests')
    parser.add_argument('-l', dest='limit', type=float, default=0,
                        help='Limit requests per second (0=unlimited)')
    parser.add_argument('-t', dest='timeout', type=float, default=5,
                        help='Timeout limit in seconds')
    parser.add_argument('-p', dest='params', nargs='*',
                        help='Parameters (in key=value format)')
    parser.add_argument('-f', dest='paramfile',
                        help='File contains parameters (multiple key=value)')
    parser.add_argument('-m', dest='method', default='GET',
                        choices=['GET', 'POST'],
                        help='Which method to be used (GET,POST)')
    return parser


def callback(status_count, requests):
    percent = sum(status_count.itervalues()) * 100 / requests
    sys.stdout.write("  [{:<70}] {:>3}%\r".format(
        '=' * int(0.7 * percent),
        percent
    ))
    sys.stdout.flush()


def main():
    HR = '-' * 79
    PERCENTAGE = [50, 66, 75, 80, 90, 95, 98, 99, 100, ]

    args = get_parser().parse_args()
    params = parse_parameters(args)

    # Running information
    print(HR)
    print("Hog is running with {} threads, ".format(args.concurrency) +
          "{} requests ".format(args.requests) +
          "and timeout in {} second(s).".format(args.timeout))
    if args.limit != 0:
        print(">>> Limit: {} request(s) per second.".format(args.limit))
    print(HR)

    # Let's begin!
    start = time.time()
    hog = Hog(callback)
    hog.run(args.url, params, args.method,
            int(args.timeout), int(args.concurrency),
            int(args.requests), int(args.limit))
    sys.stdout.write("\n")

    # Print out results
    print(HR)
    print("STATUS\tCOUNT\tAVERAGE")
    print(HR)

    for status, count in hog.status_count.iteritems():
        if status <= 0:
            continue

        print("{:>6}{:>7}{:>10.2f}ms".format(
            status, count, sum(hog.status_elapsed[status]) * 1000 / count
        ))

    # Print distribution
    if hog.status_count.get(200):
        print(HR)
        print("Response time distribution of succeed requests")

        elapsed_sorted = sorted(hog.status_elapsed[200])
        for p in PERCENTAGE:
            c = (len(hog.status_elapsed[200]) * p / 100) - 1
            print("{:>12}%{:>10.2f}ms".format(p, elapsed_sorted[c] * 1000))

    # Print errors and summary
    print(HR)
    elapsed = time.time() - start

    if hog.status_count.get(-1):
        print(">>> {} request(s) timed out".format(hog.status_count.get(-1)))

    if hog.status_count.get(-2):
        print(">>> {} request(s) just failed".format(hog.status_count.get(-2)))

    print("total time elapsed {:.4f}s".format(elapsed))


if __name__ == '__main__':
    main()
