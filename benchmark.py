#!/usr/bin/env python
from __future__ import print_function

import timeit
import time
import sys
import argparse

# Import clients, so script fails fast if not available
try:
    from cStringIO import StringIO
except:
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO

CYCLES = 10000
URL='https://localhost:4443/20480'
# URL='http://localhost:8000/20480'
TIMER = timeit.default_timer
# CPU time (only on Linux, not Windows)
# TIMER = time.clock


# parsing command line
parser = argparse.ArgumentParser(description='Run requests and pycurl benchmark.')
parser.add_argument('-n', type=int, default=CYCLES, help='Number of requests to perform')
parser.add_argument('-u', default=URL, help='The URL where to send the requests')
parser.add_argument('-m', default='total', choices=['cpu','total'], help='Wether to measure CPU time or total time')
args = parser.parse_args()

CYCLES = args.n

if 'url' in args:
    URL = args.url

if args.m=='total':
    TIMER = timeit.default_timer
else:
    TIMER = time.clock

print('URL: {0}'.format(URL))

# run the tests
def run_test(title, cycles, timer, setup, stmt):
    print("{0:<60}: {1} cycles".format(title, cycles), end='')
    sys.stdout.flush()
    t = timeit.Timer(stmt=stmt, setup=setup, timer=timer)
    try:
        total_time = t.timeit(cycles)
        print(' ran in {2} seconds'.format(title, cycles, total_time))
    except:
        print(' ... exception')
        t.print_exc()
    
# pycurl, saving in a new buffer, connection reuse
run_test("pycurl, saving in a new buffer, connection reuse", CYCLES, TIMER,

         "from pycurl import Curl; \
         from cStringIO import StringIO; \
         mycurl=Curl();",

         "body = StringIO();\
         mycurl.setopt(mycurl.URL, '{0}'); \
         mycurl.setopt(mycurl.SSL_VERIFYPEER, 0); \
         mycurl.setopt(mycurl.WRITEDATA, body); \
         mycurl.perform(); \
         output = body.getvalue(); \
         body.close()".format(URL))

# requests connection reuse
run_test("requests, connection reuse", CYCLES, TIMER,

         'import requests; \
         requests.packages.urllib3.disable_warnings(); \
         session = requests.Session()',

         "r = session.get('{0}', verify=False)".format(URL));

# requests, no connection reuse
run_test("requests, no connection reuse", CYCLES, TIMER,

         'import requests; \
         requests.packages.urllib3.disable_warnings();',
         
         "r = requests.get('{0}', verify=False)".format(URL));

# pycurl, saving in a new buffer, no connection reuse
run_test("pycurl, saving in a new buffer, no connection reuse", CYCLES, TIMER,

         "from pycurl import Curl; \
         from cStringIO import StringIO;",

         "mycurl=Curl();\
         body = StringIO();\
         mycurl.setopt(mycurl.URL, '{0}'); \
         mycurl.setopt(mycurl.SSL_VERIFYPEER, 0); \
         mycurl.setopt(mycurl.WRITEDATA, body); \
         mycurl.perform(); \
         output = body.getvalue(); \
         body.close()".format(URL));

# pycurl, saving in the same buffer, connection reuse
run_test("pycurl, saving in the same buffer, connection reuse", CYCLES, TIMER,

         "from pycurl import Curl; \
         from cStringIO import StringIO; \
         mycurl=Curl(); \
         mycurl.setopt(mycurl.URL, '{0}'); \
         mycurl.setopt(mycurl.SSL_VERIFYPEER, 0); \
         body = StringIO(); \
         mycurl.setopt(mycurl.WRITEDATA, body);".format(URL),

         "mycurl.perform();"
         );

# pycurl, no saving, connection reuse
run_test("pycurl, no saving, connection reuse", CYCLES, TIMER,

         "from pycurl import Curl; \
         mycurl=Curl(); \
         mycurl.setopt(mycurl.URL, '{0}'); \
         mycurl.setopt(mycurl.SSL_VERIFYPEER, 0); \
         mycurl.setopt(mycurl.WRITEFUNCTION, lambda x: None);".format(URL),
         "mycurl.perform()");


