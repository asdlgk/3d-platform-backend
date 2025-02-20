# File: app/models/task.py
from datetime import datetime
import uuid
from ..extensions import redis_client

class Task:
    """任务数据模型"""
    
    @classmethod
    def create(cls, **kwargs):
        """创建新任务"""
        task_id = str(uuid.uuid4())
        task_data = {
            'id': task_id,
            'created_at': datetime.utcnow().isoformat(),
            'status': 'pending',
            **kwargs
        }
        redis_client.hset(f'tasks:{task_id}', mapping=task_data)
        redis_client.rpush('task_queue', task_id)
        return cls(task_data)

    @classmethod
    def get(cls, task_id):
        """获取任务详情"""
        data = redis_client.hgetall(f'tasks:{task_id}')
        if not data:
            return None
        return cls(data)

    def __init__(self, data):
        self.data = data

    def to_dict(self):
        return self.data

    @staticmethod
    def generate_id():
        return str(uuid.uuid4())
