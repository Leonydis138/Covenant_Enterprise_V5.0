import time
import psutil

def collect_metrics():
    metrics = {
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent,
    }
    return metrics
