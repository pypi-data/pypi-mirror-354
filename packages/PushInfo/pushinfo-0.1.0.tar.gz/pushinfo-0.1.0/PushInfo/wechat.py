import requests

import mimetypes
from typing import Optional, Union, Dict, Any
from pathlib import Path

class WeChatBot:
    """企业微信机器人消息发送工具"""
    
    def __init__(self, webhook_url: str):
        """
        初始化企业微信机器人
        
        Args:
            webhook_url: 企业微信机器人的webhook地址
        """
        self.webhook_url = webhook_url
        self.session = requests.Session()
        
    def send_text(self, content: str, mentioned_list: Optional[list] = None) -> Dict[str, Any]:
        """
        发送文本消息
        
        Args:
            content: 消息内容
            mentioned_list: 要@的成员列表
            
        Returns:
            企业微信API的响应结果
        """
        payload = {
            "msgtype": "text",
            "text": {
                "content": content,
                "mentioned_list": mentioned_list or []
            }
        }
        return self._send_request(payload)
    
    def _send_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """发送请求到企业微信API"""
        try:
            response = self.session.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to send message: {str(e)}")
            
    def send_image(self, image_path: Union[str, Path]) -> Dict[str, Any]:
        """
        发送图片消息
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            企业微信API的响应结果
        """
        media_id = self._upload_media(image_path, "image")
        payload = {
            "msgtype": "image",
            "image": {
                "media_id": media_id
            }
        }
        return self._send_request(payload)
        
    def send_file(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        发送文件消息
        
        Args:
            file_path: 文件路径
            
        Returns:
            企业微信API的响应结果
        """
        media_id = self._upload_media(file_path, "file")
        payload = {
            "msgtype": "file",
            "file": {
                "media_id": media_id
            }
        }
        return self._send_request(payload)
        
    def send_markdown(self, content: str) -> Dict[str, Any]:
        """
        发送markdown格式消息
        
        Args:
            content: markdown格式内容
            
        Returns:
            企业微信API的响应结果
        """
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "content": content
            }
        }
        return self._send_request(payload)
        
    def _upload_media(self, file_path: Union[str, Path], media_type: str) -> str:
        """
        上传媒体文件到企业微信临时素材库
        
        Args:
            file_path: 文件路径
            media_type: 媒体类型(image/file)
            
        Returns:
            媒体文件的media_id
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        with open(path, "rb") as f:
            file_data = f.read()
            
        # 获取文件mime类型
        mime_type, _ = mimetypes.guess_type(path.name)
        mime_type = mime_type or "application/octet-stream"
        
        # 构造上传URL
        upload_url = self.webhook_url.replace(
            "send",
            "upload_media?type=" + media_type
        )
        
        # 构造multipart/form-data请求
        files = {
            "media": (path.name, file_data, mime_type)
        }
        
        try:
            response = self.session.post(
                upload_url,
                files=files,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return result["media_id"]
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to upload media: {str(e)}")
