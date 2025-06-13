import logging
import threading
import multiprocessing
import time
from django.shortcuts import HttpResponse


logger = logging.getLogger(__name__)


def blocking(request):
    logger.info("starting sync")
    time.sleep(2)
    logger.info(
        f"resuming sync - Running in thread: {threading.current_thread().native_id}"
    )
    return HttpResponse("sync response")


""" Running ASGI
$ loadtest -n 10 -k  http://127.0.0.1:8000/sync/blocking/

Target URL:          http://127.0.0.1:8000/sync/blocking/
Max requests:        10
Concurrent clients:  80
Running on cores:    8
Agent:               keepalive

Completed requests:  10
Total errors:        0
Total time:          2.058 s
Mean latency:        2045 ms
Effective rps:       5

Percentage of requests served within a certain time
  50%      2045 ms
  90%      2053 ms
  95%      2053 ms
  99%      2053 ms
 100%      2053 ms (longest request)
 
$ python -m gunicorn django_adjango.asgi:application -k uvicorn.workers.UvicornWorker  --access-logfile '-' --error-logfile '-'
...
starting sync
starting sync
starting sync
starting sync
resuming sync - Running in thread: 29298
resuming sync - Running in thread: 29294
resuming sync - Running in thread: 29296
resuming sync - Running in thread: 29299
resuming sync - Running in thread: 29300
...

"""


def computation(request, **kwargs):
    logger.info("starting sync")
    n = kwargs.get("times", 10)
    while n > 0:
        n -= 1
    logger.info(f"resuming sync")
    thread = threading.current_thread().native_id
    process = multiprocessing.current_process().ident
    logger.info(f"Running in thread: {thread} - Process: {process}")
    return HttpResponse("sync response")
