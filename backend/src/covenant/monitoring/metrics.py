"""Prometheus metrics"""
from time import perf_counter

from fastapi import Request
from prometheus_client import Counter, Histogram, Gauge

# Define metrics
evaluation_counter = Counter(
    'covenant_evaluations_total',
    'Total number of evaluations',
    ['result']
)

evaluation_duration = Histogram(
    'covenant_evaluation_duration_seconds',
    'Evaluation duration in seconds'
)

violation_counter = Counter(
    'covenant_violations_total',
    'Total violations',
    ['severity', 'type']
)

active_sessions = Gauge(
    'covenant_active_sessions',
    'Number of active sessions'
)

http_requests_total = Counter(
    'covenant_http_requests_total',
    'Total HTTP requests',
    ['method', 'path', 'status'],
)

http_request_duration_seconds = Histogram(
    'covenant_http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'path'],
)

http_in_flight_requests = Gauge(
    'covenant_http_in_flight_requests',
    'Number of in-flight HTTP requests',
)


def setup_metrics(app):
    """Setup lightweight HTTP metrics middleware."""

    @app.middleware("http")
    async def metrics_middleware(request: Request, call_next):
        start = perf_counter()
        path = request.url.path
        method = request.method
        http_in_flight_requests.inc()
        try:
            response = await call_next(request)
        except Exception:
            duration = perf_counter() - start
            http_request_duration_seconds.labels(method=method, path=path).observe(duration)
            http_requests_total.labels(method=method, path=path, status="500").inc()
            raise
        finally:
            http_in_flight_requests.dec()

        duration = perf_counter() - start
        http_request_duration_seconds.labels(method=method, path=path).observe(duration)
        http_requests_total.labels(method=method, path=path, status=str(response.status_code)).inc()
        return response