from flask import Flask
from flask_redis import FlaskRedis
from .services.autodl import AutoDLClient
from .utils.logger import configure_logging

redis_client = FlaskRedis()
autodl_client = AutoDLClient()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化组件
    redis_client.init_app(app)
    autodl_client.init_app(app)
    configure_logging(app)
    
    # 注册蓝图
    from .routes.task import task_bp
    from .routes.health import health_bp
    app.register_blueprint(task_bp, url_prefix='/api/tasks')
    app.register_blueprint(health_bp, url_prefix='/api/health')
    
    return app
