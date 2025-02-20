# File: app/routes/api.py
from flask import Blueprint, request, jsonify
from ..services import storage, autodl
from ..models.task import Task

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/tasks', methods=['POST'])
def submit_task():
    """提交三维建模任务"""
    data = request.json
    required_fields = ['algorithm', 'input_path']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        # 1. 从NAS下载输入数据
        local_file = storage.download_from_nas(data['input_path'], '/tmp/input')
        
        # 2. 调用算法服务
        result = autodl.call_algorithm(data['algorithm'], {
            'input_path': local_file,
            'resolution': data.get('resolution', 1024)
        })
        
        # 3. 上传结果到OSS
        oss_url = storage.upload_to_oss(result['output_path'], 
            f"results/{Task.generate_id()}.glb")
        
        # 4. 保存任务记录
        task = Task.create(
            algorithm=data['algorithm'],
            input_path=data['input_path'],
            output_url=oss_url,
            status='completed'
        )
        
        return jsonify(task.to_dict()), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_blueprint.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    """获取任务状态"""
    task = Task.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task.to_dict())
