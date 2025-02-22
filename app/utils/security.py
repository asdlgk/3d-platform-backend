import os
import hmac
import hashlib
from datetime import datetime, timedelta

class SecurityUtils:
    @staticmethod
    def generate_secure_token(length=32):
        """生成加密安全令牌"""
        return hmac.new(
            os.urandom(32),
            datetime.utcnow().isoformat().encode(),
            hashlib.sha256
        ).hexdigest()[:length]

    @staticmethod
    def validate_request_signature(data, signature):
        """验证请求签名"""
        expected = hmac.new(
            os.environ.get('API_SECRET').encode(),
            str(data).encode(),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature)

    @classmethod
    def generate_presigned_url(cls, object_path, expiration=3600):
        """生成OSS预签名URL"""
        expire_time = int((datetime.utcnow() + timedelta(seconds=expiration)).timestamp())
        signature = cls._generate_oss_signature(object_path, expire_time)
        return f"https://{os.environ['OSS_BUCKET']}.{os.environ['OSS_ENDPOINT']}/{object_path}?OSSAccessKeyId={os.environ['OSS_ACCESS_KEY_ID']}&Expires={expire_time}&Signature={signature}"

    @staticmethod
    def _generate_oss_signature(object_path, expire_time):
        key = os.environ['OSS_ACCESS_KEY_SECRET']
        string_to_sign = f"GET\n\n\n{expire_time}\n/{os.environ['OSS_BUCKET']}/{object_path}"
        return hmac.new(key.encode(), string_to_sign.encode(), hashlib.sha1).digest().encode('base64').strip()
