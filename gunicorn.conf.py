import signal
import logging

# Server configuration
bind = "0.0.0.0:5000"
workers = 1
worker_class = "sync"
keepalive = 2

# Logging configuration
loglevel = "warning"  # Reduce log noise
accesslog = "-"
errorlog = "-"

def on_starting(server):
    """Called just before the master process is initialized."""
    # Ignore SIGWINCH signal to prevent continuous handling in containerized environments
    signal.signal(signal.SIGWINCH, signal.SIG_IGN)
    logging.info("Gunicorn startup: SIGWINCH signal handling disabled")