# -*- coding: utf-8 -*-
"""
hog
~~~

Sending multiple HTTP requests ON GREEN thread.

:copyright: (c) 2014-2019 by Park Hyunwoo.
:license: MIT, see LICENSE for more details.

"""

from six import itervalues, iteritems
from six.moves import xrange

import eventlet
eventlet.monkey_patch()

import click
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
    click.echo(HR)
    click.echo("STATUS\tCOUNT\tAVERAGE")
    click.echo(HR)

    for status, elapsed_times in iteritems(result.responses):
        if status <= 0:
            continue

        count = len(elapsed_times)
        click.echo("{:>6}{:>7}{:>10.2f}ms".format(
            status, count, sum(elapsed_times) * 1000 / count
        ))

    # Print distribution
    if result.succeed_responses:
        click.echo(HR)
        click.echo("Response time distribution of succeed requests")

        elapsed_sorted = sorted(result.succeed_responses)
        for p in PERCENTAGE:
            c = (len(elapsed_sorted) * p / 100) - 1
            click.echo("{:>12}%{:>10.2f}ms".format(p, elapsed_sorted[int(c)] * 1000))

    # Print errors and summary
    click.echo(HR)

    if result.responses.get(-1):
        click.echo(">>> {} request(s) timed out".format(len(result.responses[-1])))

    if result.responses.get(-2):
        click.echo(">>> {} request(s) failed".format(len(result.responses[-2])))

    click.echo("total time elapsed {:.4f}s".format(result.elapsed))



@click.command()
@click.option('-c', '--concurrency', type=int, default=10, help='Number of threads')
@click.option('-n', '--requests', type=int, default=100, help='Number of requests')
@click.option('-l', '--limit', type=int, default=0, help='Limit requests per second (0=unlimited)')
@click.option('-t', '--timeout', type=int, default=5, help='Timeout limit in seconds')
@click.option('-p', '--params', multiple=True, help='Parameters (in key=value format)')
@click.option('-f', '--paramfile', help='File contains parameters (multiple key=value)')
@click.option('-H', '--headers', multiple=True, help='Custom headers (in key=value format)')
@click.option('-F', '--headerfile', help='File contains custom headers (multiple key=value)')
@click.option('-m', '--method', type=click.Choice(['GET', 'POST']), default='GET', help='Method to be used (GET,POST)')
@click.argument('url')
def hog(concurrency, requests, limit, timeout,
        params, paramfile, headers, headerfile, method, url):
    '''Sending multiple `HTTP` requests `ON` `GREEN` thread'''

    params = parse_from_list_and_file(params, paramfile)
    headers = parse_from_list_and_file(headers, headerfile)

    # Running information
    click.echo(HR)
    click.echo("Hog is running with {} threads, ".format(concurrency) +
          "{} requests ".format(requests) +
          "and timeout in {} second(s).".format(timeout))
    if limit != 0:
        click.echo(">>> Limit: {} request(s) per second.".format(limit))
    click.echo(HR)

    # Let's begin!
    result = Hog(callback).run(url, params, headers, method, timeout, concurrency, requests, limit)

    sys.stdout.write("\n")
    print_result(result)


if __name__ == '__main__':
    hog()
