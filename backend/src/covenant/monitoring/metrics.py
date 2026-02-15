"""Prometheus metrics"""
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

def setup_metrics(app):
    """Setup metrics collection"""
    pass  # Middleware automatically collects