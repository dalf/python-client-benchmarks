#!/usr/bin/env python
import time
from flask import Flask
app = Flask(__name__)

response = "0123456789" * 1024 * 2

@app.route("/ping")
def hello():
    # time.sleep(0.01)
    return response

if __name__ == "__main__":
    app.run()
