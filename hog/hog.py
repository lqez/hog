# -*- coding: utf-8 -*-
"""
hog
~~~

Sending multiple HTTP requests ON GREEN thread.

:copyright: (c) 2014-2016 by Park Hyunwoo.
:license: MIT, see LICENSE for more details.

"""

from __future__ import print_function
from six import itervalues, iteritems
from six.moves import xrange

import eventlet
eventlet.monkey_patch()

import argparse
import re
import requests
import sys
import time
from collections import defaultdict


HR = '-' * 79
PERCENTAGE = [50, 66, 75, 80, 90, 95, 98, 99, 100, ]


class HogResult(object):
    def __init__(self):
        super(HogResult, self).__init__()
        self.elapsed = 0
        self.requests = 0
        self.responses = defaultdict(list)
        self.succeed_responses = []

    @property
    def ok(self):
        return len(self.succeed_responses) == self.requests


class Hog(object):
    STATUS_TIMEOUT = -1
    STATUS_FAILED = -2

    def __init__(self, callback=None):
        super(Hog, self).__init__()
        self.callback = callback

    def fetch(self):
        elapsed = 0

        try:
            if self.method == 'GET':
                r = requests.get(
                    self.url,
                    params=self.params,
                    headers=self.headers,
                    timeout=self.timeout
                )
            else:
                r = requests.post(
                    self.url,
                    data=self.params,
                    headers=self.headers,
                    timeout=self.timeout
                )

            status = r.status_code
            elapsed = r.elapsed.total_seconds()

            if 200 <= status < 400:
                self.result.succeed_responses.append(elapsed)
        except requests.exceptions.ConnectionError:
            status = self.STATUS_FAILED
        except requests.exceptions.Timeout:
            status = self.STATUS_TIMEOUT

        self.result.responses[status].append(elapsed)

        if self.callback:
            self.callback(self.result)

    def run(self, url, params=None, headers=None, method='GET',
            timeout=5, concurrency=10, requests=100, limit=0):
        self.url = url
        self.params = params
        self.headers = headers
        self.method = method
        self.timeout = timeout

        self.result = HogResult()
        self.result.requests = requests

        if self.callback:
            self.callback(self.result)

        pool = eventlet.GreenPool(int(concurrency))
        start = time.time()

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
        self.result.elapsed = time.time() - start

        return self.result


def run(url, params=None, headers=None, method='GET',
        timeout=5, concurrency=10, requests=100, limit=0, callback=None):
    return Hog(callback) \
        .run(url, params, headers, method, timeout, concurrency, requests, limit)


def parse_from_list_and_file(lst, filename):
    res = {}

    if filename:
        with open(filename, 'r') as fh:
            lst += [_.rstrip('\r\n') for _ in fh.readlines()]

    if lst:
        for param in lst:
            m = re.match(r'(?P<key>[^=]+)=(?P<value>.+)', param)
            if m:
                res[m.group('key')] = m.group('value')

    return res


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
    parser.add_argument('-H', dest='headers', nargs='*',
                        help='Custom headers (in key=value format)')
    parser.add_argument('-F', dest='headerfile',
                        help='File contains custom headers (multiple key=value)')
    parser.add_argument('-m', dest='method', default='GET',
                        choices=['GET', 'POST'],
                        help='Which method to be used (GET,POST)')
    return parser


def callback(result):
    percent = sum([len(_) for _
                   in itervalues(result.responses)]) * 100 / result.requests
    sys.stdout.write("  [{:<70}] {:>3}%\r".format(
        '=' * int(0.7 * percent),
        percent
    ))
    sys.stdout.flush()


def print_result(result):
    # Print out results
    print(HR)
    print("STATUS\tCOUNT\tAVERAGE")
    print(HR)

    for status, elapsed_times in iteritems(result.responses):
        if status <= 0:
            continue

        count = len(elapsed_times)
        print("{:>6}{:>7}{:>10.2f}ms".format(
            status, count, sum(elapsed_times) * 1000 / count
        ))

    # Print distribution
    if result.succeed_responses:
        print(HR)
        print("Response time distribution of succeed requests")

        elapsed_sorted = sorted(result.succeed_responses)
        for p in PERCENTAGE:
            c = (len(elapsed_sorted) * p / 100) - 1
            print("{:>12}%{:>10.2f}ms".format(p, elapsed_sorted[int(c)] * 1000))

    # Print errors and summary
    print(HR)

    if result.responses.get(-1):
        print(">>> {} request(s) timed out".format(len(result.responses[-1])))

    if result.responses.get(-2):
        print(">>> {} request(s) failed".format(len(result.responses[-2])))

    print("total time elapsed {:.4f}s".format(result.elapsed))


def main():
    args = get_parser().parse_args()
    params = parse_from_list_and_file(args.params, args.paramfile)
    headers = parse_from_list_and_file(args.headers, args.headerfile)

    # Running information
    print(HR)
    print("Hog is running with {} threads, ".format(args.concurrency) +
          "{} requests ".format(args.requests) +
          "and timeout in {} second(s).".format(args.timeout))
    if args.limit != 0:
        print(">>> Limit: {} request(s) per second.".format(args.limit))
    print(HR)

    # Let's begin!
    result = Hog(callback).run(args.url, params, headers, args.method,
                               int(args.timeout), int(args.concurrency),
                               int(args.requests), int(args.limit))

    sys.stdout.write("\n")
    print_result(result)


if __name__ == '__main__':
    main()
