### !!! see [svanoort/python-client-benchmarks](https://github.com/svanoort/python-client-benchmarks) for up to date results
* the changes in this forked have been merged into / rewrote in the svanoort version.
* the results here may have an issue related to [this bug](https://bugzilla.redhat.com/show_bug.cgi?id=1130239) as svanoort as noticed https://github.com/pycurl/pycurl/issues/309 

# python-client-benchmarks
Micro-benchmarking of two python HTTP client tools : requests and pycurl.

## How to setup :
* create (or not) a virtual environement : ```mkdir ve; virtualenv ve; . ./ve/bin/activate```
* ```pip install -r requirements.txt```

## How to run a test server

Two choices : nginx inside a docker image or a flask server.

Warning : the flask server is much slower than the nginx instance, and doesn't allow to test HTTPS connections.

### How to run the nginx docker image
First time :
* ```sudo server/docker-nginx/build.sh```

Run the server (the logs will be shown on the terminal) :
* ```sudo server/docker-nginx/run.sh```

The server listens on 8000 (HTTP) and 4443 (HTTPS).

### How to run the flask server
* ```./server/flask/server.py```

The server listens on 8000 (HTTP)

## How to run the benchmark
* ```./benchmark.py``` on another terminal

to see some options :
* ```./benchmark.py --help```  

or edit the file directly

## Results on my laptop

So to sum up for 10000 requests (time express in second) and response of 20480 bytes : 

|                                                     | HTTP (Flask), total time | HTTP (NGINX), total time | HTTPS (NGINX), total time | HTTPS (NGINX), cpu time |
|-----------------------------------------------------|--------------|--------------|---------------|-------------------------|
| pycurl, saving in a new buffer, connection reuse    |     15.7     |      4.1     |      12.8     |           4.9           |
| requests, connection reuse                          |     38.2     |     23.18    |      30.3     |           27.0          |
| requests, no connection reuse                       |     44.3     |     39.7     |     122.8     |           63.4          |
| pycurl, saving in a new buffer, no connection reuse |     66.7     |     56.4     |     130.8     |           32.3          |
| pycurl, saving in the same buffer, connection reuse |     21.9     |      4.5     |      13.7     |           4.8           |
| pycurl, no saving, connection reuse                 |     18.0     |      4.0     |      13.0     |           4.5           |

Note : The "no connection reuse" speed are limited by my laptop CPU (i3-2367M, 1.4Ghz)
