import asyncio
import logging
import multiprocessing
import threading
import time
from django.shortcuts import HttpResponse

logger = logging.getLogger(__name__)


async def non_blocking(request):
    logger.info("starting async")
    await asyncio.sleep(2)
    logger.info(f"resuming async - Running in thread: {threading.current_thread().native_id}")
    return HttpResponse("async response")





""" Running ASGI
$ loadtest -n 10 -k  http://127.0.0.1:8000/async/non-blocking/

Target URL:          http://127.0.0.1:8000/async/non-blocking/
Max requests:        10
Concurrent clients:  80
Running on cores:    8
Agent:               keepalive

Completed requests:  10
Total errors:        0
Total time:          2.037 s
Mean latency:        2024.5 ms
Effective rps:       5

Percentage of requests served within a certain time
  50%      2026 ms
  90%      2028 ms
  95%      2028 ms
  99%      2028 ms
 100%      2028 ms (longest request)

===================
starting async
starting async
starting async
starting async
starting async
resuming async - Running in thread: 29135
resuming async - Running in thread: 29135
resuming async - Running in thread: 29135
resuming async - Running in thread: 29135
resuming async - Running in thread: 29135
resuming async - Running in thread: 29135
....

"""

async def blocking(request):
    logger.info("starting async")
    time.sleep(2)
    logger.info(f"resuming async - Running in thread: {threading.current_thread().native_id}")
    return HttpResponse("async response")

""" Running ASGI
$ loadtest -n 10 -k  http://127.0.0.1:8000/async/blocking/

Target URL:          http://127.0.0.1:8000/async/blocking/
Max requests:        10
Concurrent clients:  80
Running on cores:    8
Agent:               keepalive

Completed requests:  10
Total errors:        0
Total time:          20.065 s
Mean latency:        18244.9 ms
Effective rps:       0

Percentage of requests served within a certain time
  50%      20045 ms
  90%      20054 ms
  95%      20054 ms
  99%      20054 ms
 100%      20054 ms (longest request)

===================
starting async
resuming async - Running in thread: 29135
starting async
resuming async - Running in thread: 29135
starting async
resuming async - Running in thread: 29135
"""



async def computation(request, **kwargs):
    logger.info("starting async")
    n = kwargs.get("times", 10)
    while n > 0:
        n -= 1
    logger.info(f"resuming async")
    thread = threading.current_thread().native_id
    process = multiprocessing.current_process().ident
    logger.info(f"Running in thread: {thread} - Process: {process}")
    return HttpResponse("async response")