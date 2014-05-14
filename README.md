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


INSTALL
-------

    pip install hog


Author
------

Park Hyunwoo([@lqez](https://twitter.com/lqez))


License
-------

`hog` is distributed under MIT license.
