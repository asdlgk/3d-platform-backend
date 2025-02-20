redis_client = FlaskRedis()
autodl_client = AutoDLClient()

def create_app(config_class='config.Config'):
    """应用工厂函数"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化扩展
    redis_client.init_app(app)
    autodl_client.init_app(app)
    
    # 注册蓝图
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    
    return app
