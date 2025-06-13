# Django with WSGI & ASGI

---

## Contents

1. Introduction
2. Load Testing with ASGI
3. Load Testing with WSGI
4. Bonus: Computation

---

## Introduction

### WSGI

* The Web Server Gateway Interface (PEP 3333)
* Standard interface between synchronous Python web servers and applications

### ASGI

* Asynchronous Server Gateway Interface
* Standard for both async and sync Python applications
* Backwards-compatible with WSGI; supported by multiple servers and frameworks

---

## Load Testing with ASGI

### Server Launch

```
# using Gunicorn + Uvicorn worker
python -m gunicorn django_adjango.asgi:application \
  -k uvicorn.workers.UvicornWorker \
  --access-logfile '-' \
  --error-logfile '-'
```

### Load Test: Async Endpoint

```
loadtest -n 10 -k http://127.0.0.1:8000/async/non-blocking/
```

* Completed requests: 10
* Total errors: 0
* Total time: 2.037 s
* Mean latency: 2024.5 ms
* Effective RPS: 5

#### Server Logs

```
$ python -m gunicorn django_adjango.asgi:application \
  -k uvicorn.workers.UvicornWorker \
  --access-logfile '-' --error-logfile '-'
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
```

### Load Test: Sync Endpoint

```
loadtest -n 10 -k http://127.0.0.1:8000/sync/blocking/
```

* Completed requests: 10
* Total errors: 0
* Total time: 2.058 s
* Mean latency: 2045 ms
* Effective RPS: 5

#### Server Logs

```
$ python -m gunicorn django_adjango.asgi:application \
  -k uvicorn.workers.UvicornWorker \
  --access-logfile '-' --error-logfile '-'
starting sync
starting sync
starting sync
starting sync
resuming sync - Running in thread: 29298
resuming sync - Running in thread: 29294
resuming sync - Running in thread: 29296
resuming sync - Running in thread: 29299
resuming sync - Running in thread: 29300
```

---

## Load Testing with WSGI

### Server Launch

```
gunicorn django_adjango.wsgi \
  --access-logfile '-' \
  --error-logfile '-'
```

### Load Test: Async Endpoint

```
loadtest -n 10 -k http://127.0.0.1:8000/async/non-blocking/
```

* Completed requests: 10
* Total errors: 0
* Total time: 20.076 s
* Mean latency: 11036.4 ms
* Effective RPS: 0

#### Server Logs

```
$ gunicorn django_adjango.wsgi \
  --access-logfile '-' \
  --error-logfile '-'
starting async
resuming async - Running in thread: 13146
starting async
resuming async - Running in thread: 13165
...
```

### Load Test: Sync Endpoint

```
loadtest -n 10 -k http://127.0.0.1:8000/sync/blocking/
```

* Completed requests: 10
* Total errors: 0
* Total time: 20.035 s
* Mean latency: 11018.5 ms
* Effective RPS: 0

#### Server Logs

```
$ gunicorn django_adjango.wsgi \
  --access-logfile '-' \
  --error-logfile '-'
starting sync
resuming sync - Running in thread: 11242
starting sync
resuming sync - Running in thread: 11242
...
```

---

## Bonus: Computation & Trade-offs

### Computation Endpoints

```
def computation(request, times=10):
    n = times
    while n > 0:
        n -= 1
    return HttpResponse("sync response")
```

* WSGI sync computation: RPS 323, Mean latency: 6.7 ms
* ASGI async computation: RPS 217, Mean latency: 27.3 ms

### CPU-bound Comparison

* WSGI blocking CPU-bound: single-threaded → better performance ?
* ASGI blocking CPU-bound: event-loop overhead → lower performance ?
