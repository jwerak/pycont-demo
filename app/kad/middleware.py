from flask import request
from prometheus_client import Counter
from prometheus_client import Histogram
from random import randint

import time
import os

# Prometheus metrics
REQUEST_LATENCY = Histogram(
    'request_latency',
    'HTTP Request latency',
    ['method', 'endpoint']
)


def start_timer():
    request.start_time = time.time()


def record_request_data(response):
    resp_time = time.time() - request.start_time

    REQUEST_LATENCY.labels(request.method, request.path).observe(resp_time)

    return response


# 10% change to die
def die(response):
    if randint(0, 100) > 90:
        os._exit(1)

    return response


def setup_metrics(app):
    app.before_request(start_timer)
    app.after_request(record_request_data)
    app.after_request(die)
