Hog
===

Sending multiple HTTP requests ON GREEN thread like an [hog](http://en.wikipedia.org/wiki/Giant_forest_hog).
Runs on Python 2 / 3.


Using Hog as console script
---------------------------
```shell
Usage: hog [OPTIONS] URL

  Sending multiple `HTTP` requests `ON` `GREEN` thread

Options:
  -c, --concurrency INTEGER  Number of threads
  -n, --requests INTEGER     Number of requests
  -l, --limit INTEGER        Limit requests per second (0=unlimited)
  -t, --timeout INTEGER      Timeout limit in seconds
  -p, --params TEXT          Parameters (in key=value format)
  -f, --paramfile TEXT       File contains parameters (multiple key=value)
  -H, --headers TEXT         Custom headers (in key=value format)
  -F, --headerfile TEXT      File contains custom headers (multiple key=value)
  -m, --method [GET|POST]    Method to be used (GET,POST)
  --help                     Show this message and exit.
```


Using Hog via module
--------------------

    import hog

    r = hog.run("http://somewhere.in.universe/")

    if r.ok:
        print("Looking good.")



Sample result
-------------

    $ hog -c 250 -n 1000 -t 5 http://somewhere.in.universe/
    -------------------------------------------------------------------------------
    Hog is running with 250 threads, 1000 requests and timeout in 5 second(s).
    -------------------------------------------------------------------------------
      [======================================================================] 100%
    -------------------------------------------------------------------------------
    STATUS  COUNT   AVERAGE
    -------------------------------------------------------------------------------
       200    360   2161.32ms
       502    427    450.02ms
       503    113    632.74ms
    -------------------------------------------------------------------------------
    Response time distribution of succeed requests
              50%   2214.45ms
              66%   2337.06ms
              75%   2420.22ms
              80%   2489.50ms
              90%   2635.47ms
              95%   2709.51ms
              98%   2753.71ms
              99%   2785.34ms
             100%   2839.30ms
    -------------------------------------------------------------------------------
    >>> 100 request(s) just failed
    total time elapsed 9.9918s


Install
-------

    pip install hog


Author
------

Park Hyunwoo([@lqez](https://twitter.com/lqez))


License
-------

`hog` is distributed under MIT license.
