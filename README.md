hog
===

Sending multiple HTTP requests ON GREEN thread. 


USAGE as script
---------------

    usage: hog.py [-h] -u URL [-c CONCURRENCY] [-n REQUESTS] [-t TIMEOUT]
                  [-p [PARAMS [PARAMS ...]]] [-f PARAMFILE] [-m {GET,POST}]

    Sending multiple `HTTP` requests `ON` `GREEN` thread

    positional arguments:
      url                   URL to be tested

    optional arguments:
      -h, --help            show this help message and exit
      -c CONCURRENCY        Number of threads
      -n REQUESTS           Number of requests
      -l LIMIT              Limit requests per second (0=unlimited)
      -t TIMEOUT            Timeout limit in seconds
      -p [PARAMS [PARAMS ...]]
                            Parameters (in key=value format)
      -f PARAMFILE          File contains parameters (multiple key=value)
      -m {GET,POST}         Which method to be used (GET,POST)


USAGE as module
---------------

    import hog

    hog.run('http://somewhere.in.universe/')


SAMPLE RESULT
-------------

    $ hog -c 250 -n 1000 -t 5 -p foo=bar http://somewhere.in.universe/
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


INSTALL
-------

    pip install hog


Author
------

Park Hyunwoo([@lqez](https://twitter.com/lqez))


License
-------

`hog` is distributed under MIT license.
