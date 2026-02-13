import logging
from datetime import datetime, timedelta

# Alert monitoring logic
def check_alerts(alerts):
    for alert in alerts:
        if alert.is_active():
            logging.info(f"Active alert: {alert.name}")
        else:
            logging.info(f"No active alerts for {alert.name}")
