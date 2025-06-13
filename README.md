# Test project

The goal of the project is to compare the performance running django with WSGI vs django ASGI

I use gunicorn to start both servers, with uvicorn worker to target ASGI interface.

# Run the sample

## How to run Django

```bash
gunicorn django_adjango.wsgi --access-logfile '-' --error-logfile '-'
```

## How to run Async Django

```bash
python -m gunicorn django_adjango.asgi:application -k uvicorn.workers.UvicornWorker  --access-logfile '-' --error-logfile '-'
```

## Run the load test

```bash
loadtest -n 10 -k  http://127.0.0.1:8000/sync/blocking/
loadtest -n 10 -k  http://127.0.0.1:8000/async/blocking/
loadtest -n 10 -k  http://127.0.0.1:8000/async/non-blocking/
loadtest -n 10 -k  http://127.0.0.1:8000/async/comp/10/
loadtest -n 10 -k  http://127.0.0.1:8000/sync/comp/10/
```
