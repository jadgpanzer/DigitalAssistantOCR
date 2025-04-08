import time
import requests
import socket
from urllib.parse import urlparse

class MessageSender:
    def __init__(self, endpoints):
        self.endpoints = endpoints

    def check_endpoint(self, url):
        """检查端点可达性"""
        try:
            parsed = urlparse(url)
            port = parsed.port or (80 if parsed.scheme == 'http' else 443)
            with socket.create_connection((parsed.hostname, port), timeout=5):
                return True
        except Exception:

            return False

    def send(self, message, use_gpt):
        """发送消息到对应端点"""
        # 根据是否使用GPT选择端点
        # 这里如果匹配的关键词在keywords.txt中没有找到，则使用默认的GPT端点，触发Fay调用GPT回复
    
        if not isinstance(use_gpt, bool):
            raise ValueError("use_gpt参数必须是布尔值")
        
        endpoint_type = 'gpt' if use_gpt else 'transparent'
        endpoint = self.endpoints.get(f"{endpoint_type}_endpoint")
        
        if not self.check_endpoint(endpoint):
            raise ConnectionError(f"端点不可达: {endpoint}")

        payload = self.build_payload(message, use_gpt)
        
        try:
            response = requests.post(
                endpoint,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API请求失败: {str(e)}")

    def build_payload(self, message, is_gpt):
        """构造请求负载"""
        if is_gpt:
            return {
            "model": "fay",
            "messages": [{
                "role": "User",
                "content": message
            }]
        }
        else:
            return {
                "user": "User",
                "audio": None,
                "text": message,
                "timestamp": int(time.time())
            }
        