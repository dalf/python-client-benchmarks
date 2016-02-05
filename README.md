# python-client-benchmarks
Micro-benchmarking of two python HTTP client tools : requests and pycurl.

## How to setup :
* create (or not) a virtual environement : ```virutalenv ve; . ./ve/bin/activate```
* ```pip install -r requirements.txt```

## How to run a test server

Two choices : nginx inside a docker image or a flask server.

Warning : the flask server is much slower than the nginx instance, and doesn't allow to test HTTPS connections.

### How to run the nginx docker image
First time :
* ```sudo server/docker-nginx/build.sh``` to use the nginx docker image as an server

Run the server :
* ```sudo server/docker-nginx/run.sh```

The server listens on 8000 (HTTP) and 4443 (HTTPS).

### How to run the flask server
* ```./server/flask/server.py```

The server listens on 8000 (HTTP)

## How to run the benchmark
* ```./benchmark.py``` on another terminal
* ```./benchmark.py --help``` to see some options or edit the file directly
