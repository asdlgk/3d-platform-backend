from flask import Blueprint, request, jsonify
from app.services import autodl, storage
from app.models.task import Task

task_bp = Blueprint('task', __name__)

@task_bp.route('', methods=['POST'])
def create_task():
    """创建建模任务"""
    if 'file' not in request.files:
        return jsonify({"error": "未上传文件"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "空文件名"}), 400

    try:
        # 1. 保存上传文件
        save_path = storage.save_upload(file)
        
        # 2. 创建任务记录
        task = Task.create(file.filename)
        
        # 3. 调用AutoDL服务
        result = autodl.process(
            algorithm=request.form.get('algorithm', 'dust3d'),
            input_path=save_path,
            task_id=task.id
        )
        
        # 4. 更新任务状态
        task.update(
            status='processing',
            model_url=storage.upload_result(result['output_path'])
        )
        
        return jsonify(task.to_dict()), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
