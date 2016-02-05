#!/bin/bash
cd "$(dirname "$0")"
docker build -t nginx-ssl-test .
