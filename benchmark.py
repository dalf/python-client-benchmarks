#/usr/bin/env/python
from __future__ import print_function

import timeit
import time
import sys

# Import clients, so script fails fast if not available
try:
    from cStringIO import StringIO
except:
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO

CYCLES = 10000
URL='http://localhost:5000/ping'
TIMER = timeit.default_timer
# CPU time (only on Linux, not Windows)
# TIMER = time.clock

def run_test(title, cycles, timer, setup, stmt):
    print("{0:<60}: {1} cycles".format(title, cycles), end='')
    sys.stdout.flush()
    t = timeit.Timer(stmt=stmt, setup=setup, timer=timer)
    try:
        total_time = t.timeit(cycles)
        print(' ran in {2} seconds'.format(title, cycles, total_time))
    except:
        print('')
        t.print_exc()
    
# pycurl, saving in a new buffer, connection reuse
run_test("pycurl, saving in a new buffer, connection reuse", CYCLES, TIMER,

         "from pycurl import Curl; \
         from cStringIO import StringIO; \
         mycurl=Curl();",

         "body = StringIO();\
         mycurl.setopt(mycurl.URL, '{0}'); \
         mycurl.setopt(mycurl.WRITEDATA, body); \
         mycurl.perform(); \
         output = body.getvalue(); \
         body.close()".format(URL))

# requests connection reuse
run_test("requests, connection reuse", CYCLES, TIMER,

         'import requests; \
         session = requests.Session()',

         "r = session.get('{0}')".format(URL));

# requests, no connection reuse
run_test("requests, no connection reuse", CYCLES, TIMER,

         'import requests',
         
         "r = requests.get('{0}')".format(URL));

# pycurl, saving in a new buffer, no connection reuse
run_test("pycurl, saving in a new buffer, no connection reuse", CYCLES, TIMER,

         "from pycurl import Curl; \
         from cStringIO import StringIO;",

         "mycurl=Curl();\
         body = StringIO();\
         mycurl.setopt(mycurl.URL, '{0}'); \
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
         body = StringIO(); \
         mycurl.setopt(mycurl.WRITEDATA, body);".format(URL),

         "mycurl.perform();"
         );

# pycurl, no saving, connection reuse
run_test("pycurl, no saving, connection reuse", CYCLES, TIMER,

         "from pycurl import Curl; \
         mycurl=Curl(); \
         mycurl.setopt(mycurl.URL, '{0}'); \
         mycurl.setopt(mycurl.WRITEFUNCTION, lambda x: None);".format(URL),

         "mycurl.perform()");


