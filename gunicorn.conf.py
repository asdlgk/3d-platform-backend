import multiprocessing

bind = "127.0.0.1:5000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
timeout = 300
keepalive = 65
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
capture_output = True
log_level = "info"
preload_app = True

# SSL配置（如需）
# keyfile = "/path/to/privkey.pem"
# certfile = "/path/to/cert.pem"
