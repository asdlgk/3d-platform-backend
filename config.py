# File: config.py
import os

class Config:
    # 基础配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-123')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # 存储配置
    NAS_MOUNT_POINT = '/mnt/nas'
    OSS_ACCESS_KEY_ID = os.getenv('OSS_AK_ID')
    OSS_ACCESS_KEY_SECRET = os.getenv('OSS_AK_SECRET')
    OSS_ENDPOINT = 'oss-cn-hangzhou.aliyuncs.com'
    OSS_BUCKET_NAME = '3d-model-platform'
    
    # AutoDL配置
    AUTODL_CONFIG = {
        'dust3d': {
            'host': 'region-3.autodl.com',
            'ssh_port': 23746,
            'service_port': 5000,
            'local_port': 6000,
            'ssh_key': '/etc/secrets/autodl_key'
        },
        'wonder3d': {
            'host': 'region-3.autodl.com',
            'ssh_port': 23747,
            'service_port': 5001,
            'local_port': 6001,
            'ssh_key': '/etc/secrets/autodl_key'
        }
    }
    
    # 请求超时设置
    REQUEST_TIMEOUT = 30
