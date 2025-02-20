import paramiko
import sshtunnel
from flask import current_app

class AutoDLClient:
    """AutoDL服务调用客户端"""
    def __init__(self, app=None):
        self.tunnels = {}
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """初始化SSH隧道连接"""
        self.config = app.config.get('AUTODL_CONFIG')
        self._connect_tunnels()

    def _connect_tunnels(self):
        """建立所有算法服务的SSH隧道"""
        for algo, cfg in self.config.items():
            tunnel = sshtunnel.SSHTunnelForwarder(
                (cfg['host'], cfg['ssh_port']),
                ssh_username="root",
                ssh_pkey=paramiko.RSAKey.from_private_key_file(cfg['ssh_key']),
                remote_bind_address=('127.0.0.1', cfg['service_port']),
                local_bind_address=('127.0.0.1', cfg['local_port'])
            )
            tunnel.start()
            self.tunnels[algo] = tunnel

    def call_algorithm(self, algo_name, input_data):
        """调用指定算法服务"""
        if algo_name not in self.tunnels:
            raise ValueError(f"Unsupported algorithm: {algo_name}")
        
        import requests
        local_port = self.config[algo_name]['local_port']
        try:
            resp = requests.post(
                f'http://127.0.0.1:{local_port}/process',
                json=input_data,
                timeout=current_app.config['REQUEST_TIMEOUT']
            )
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Algorithm call failed: {str(e)}")
            raise
