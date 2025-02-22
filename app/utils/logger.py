import logging
from logging.handlers import RotatingFileHandler
from flask import Flask

def configure_logging(app: Flask):
    # 基础配置
    log_level = logging.DEBUG if app.debug else logging.INFO
    app.logger.setLevel(log_level)

    # 文件日志（生产环境）
    if not app.debug:
        file_handler = RotatingFileHandler(
            '/var/log/3d-platform/backend.log',
            maxBytes=1024 * 1024 * 100,  # 100MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        app.logger.addHandler(file_handler)

    # 控制台日志（开发环境）
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter(
        '%(levelname)s: %(message)s'
    ))
    app.logger.addHandler(console_handler)
