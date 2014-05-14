hog
===

Sending multiple HTTP requests ON GREEN thread. 


USAGE
-----

    usage: hog.py [-h] -u URL [-c CONCURRENCY] [-n REQUESTS] [-t TIMEOUT]
                  [-p [PARAMS [PARAMS ...]]] [-f PARAMFILE] [-m {GET,POST}]

    Sending multiple `HTTP` requests `ON` `GREEN` thread

    optional arguments:
      -h, --help            show this help message and exit
      -u URL                URL to be tested
      -c CONCURRENCY        Number of threads
      -n REQUESTS           Number of requests
      -t TIMEOUT            Timeout limit in seconds
      -p [PARAMS [PARAMS ...]]
                            Parameters on POST request(in key=value format)
      -f PARAMFILE          File contains parameters(multiple key=value)
      -m {GET,POST}         Which method to be used (GET,POST)


SAMPLE RESULT
-------------

    $ hog -c 1000 -n 10000 -m POST -t 1 -p foo=bar http://somewhere.in.universe/
    -------------------------------------------------------------------------------
    Run with 1000 threads, 10000 requests, timeout in 1.0 second(s).
    -------------------------------------------------------------------------------
    STATUS	COUNT	AVERAGE
    -------------------------------------------------------------------------------
    200	    2035	2171.37ms
    502	    1636	1597.74ms
    -------------------------------------------------------------------------------
    >>> 6233 request(s) timed out
    >>> 96 request(s) just failed
    total time elapsed 28.5283s


INSTALL
-------

    pip install hog


Author
------

Park Hyunwoo([@lqez](https://twitter.com/lqez))


License
-------

`hog` is distributed under MIT license.
