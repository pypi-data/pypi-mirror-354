"""Push Tools - A utility for sending messages via WeChat Work bot and email.

Features:
- WeChat Work Bot:
  * Send text messages
  * Send images
  * Send files
  * Send markdown messages
  
- Email:
  * Send plain text emails
  * Send HTML emails
  * Send emails with attachments
  * Support CC/BCC
"""

__version__ = "0.1.0"

from .wechat import WeChatBot
from .email import EmailSender
from .utils import load_config, setup_logging, validate_file_path

__all__ = [
    'WeChatBot', 
    'EmailSender',
    'load_config',
    'setup_logging',
    'validate_file_path'
]
