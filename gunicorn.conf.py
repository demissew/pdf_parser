# Gunicorn configuration file
# This file provides default settings that can be overridden via command-line args or environment variables

import multiprocessing
import os

# Server socket
bind = "0.0.0.0:8000"

# Worker processes
workers = int(os.getenv("PDF_PARSER_WORKERS", "2"))
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = int(os.getenv("PDF_PARSER_WORKER_TIMEOUT", "600"))
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = os.getenv("PDF_PARSER_LOG_LEVEL", "INFO").lower()

# Process naming
proc_name = "pdf_parser"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (disabled by default, configure if needed)
keyfile = None
certfile = None
