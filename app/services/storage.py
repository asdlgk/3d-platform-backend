import oss2
from flask import current_app

class StorageManager:
    """存储服务管理类"""
    def __init__(self):
        self.auth = None
        self.bucket = None

    def init_app(self, app):
        """初始化OSS连接"""
        self.auth = oss2.Auth(
            app.config['OSS_ACCESS_KEY_ID'],
            app.config['OSS_ACCESS_KEY_SECRET']
        )
        self.bucket = oss2.Bucket(
            self.auth,
            app.config['OSS_ENDPOINT'],
            app.config['OSS_BUCKET_NAME']
        )

    def upload_to_oss(self, local_path, object_name):
        """上传文件到OSS"""
        try:
            self.bucket.put_object_from_file(object_name, local_path)
            return f"oss://{self.bucket.bucket_name}/{object_name}"
        except oss2.exceptions.OssError as e:
            current_app.logger.error(f"OSS Upload failed: {e}")
            raise

    def download_from_nas(self, remote_path, local_path):
        """从NAS下载文件（已挂载到本地）"""
        import shutil
        try:
            shutil.copy(f"{current_app.config['NAS_MOUNT_POINT']}/{remote_path}", local_path)
            return local_path
        except IOError as e:
            current_app.logger.error(f"NAS Download failed: {e}")
            raise
