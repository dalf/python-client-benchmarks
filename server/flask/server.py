#!/usr/bin/env python
import time
from flask import Flask
app = Flask(__name__)

response20480 = "0123456789" * 1024 * 2
response40960 = "0123456789" * 1024 * 4
response81920 = "0123456789" * 1024 * 8

@app.route("/20480")
def return20480():
    return response20480

@app.route("/40960")
def return40960():
    return response40960

@app.route("/81920")
def return81920():
    return response81920

if __name__ == "__main__":
    app.run(port=8000)
