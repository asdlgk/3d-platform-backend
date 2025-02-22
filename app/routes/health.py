from flask import Blueprint, jsonify
from flask_redis import FlaskRedis

health_bp = Blueprint('health', __name__)
redis = FlaskRedis()

@health_bp.route('', methods=['GET'])
def health_check():
    try:
        # 检查Redis连接
        redis.ping()
        return jsonify({
            "status": "healthy",
            "redis": "connected",
            "version": "1.0.0"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500
