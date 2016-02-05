#!/bin/bash
docker run --rm -i -t -p 4443:443 -p 8000:80 nginx-ssl-test
