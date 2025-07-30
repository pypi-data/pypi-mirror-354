# Push Tool - 企业消息推送工具

一个通过企业微信机器人和电子邮件发送消息的实用工具库。

## 功能特性

### 企业微信机器人
- **文本消息**
  - 支持@提及特定用户
  - 支持@提及所有人
  - 支持消息链接
  
- **图片消息**
  - 支持本地图片文件
  - 自动验证图片格式和大小
  - 支持JPEG/PNG格式
  
- **文件消息**
  - 支持多种文件类型
  - 自动检查文件大小限制(20MB)
  
- **Markdown消息**
  - 支持标准Markdown语法
  - 支持标题、列表、代码块等格式
  - 自动处理特殊字符转义

### 电子邮件发送
- **基础功能**
  - 纯文本邮件
  - HTML格式邮件
  - 支持抄送(CC)和密送(BCC)
  
- **附件支持**
  - 多附件支持
  - 自动检测MIME类型
  - 支持常见文档格式
  
- **安全连接**
  - TLS加密支持
  - SMTP认证
  - 连接超时处理

## 安装指南

### 通过PyPI安装

```bash
pip install PushInfo
```

### 从源码安装

1. 克隆仓库：
```bash
 ngit clone https://github.com/yourusername/push_info.git
cd push_info
```

2. 安装依赖：
```bash
pip install .
```

### 开发模式安装

```bash
pip install -e .[dev]
```

### 依赖要求

- Python 3.7+
- 核心依赖：
  - `requests` >= 2.25.1
  - `python-dotenv` >= 0.19.0 (用于环境变量配置)
  
开发依赖：
  - `pytest` >= 6.2.5
  - `pytest-cov` >= 2.12.1
  - `mypy` >= 0.910
  - `flake8` >= 3.9.2

### 配置要求

#### 企业微信机器人
1. 在企业微信中创建群聊机器人
2. 获取Webhook URL
3. (可选)设置IP白名单

#### 邮件服务器
1. SMTP服务器地址和端口
2. 认证用户名和密码
3. (可选)配置TLS/SSL设置

## 详细使用指南

### 企业微信机器人高级用法

#### 环境变量配置
建议将敏感信息存储在环境变量中：

```python
import os
from push_tools import WeChatBot

# 从环境变量读取webhook_url
webhook_url = os.getenv("WECHAT_WEBHOOK_URL")
bot = WeChatBot(webhook_url)
```

#### 消息发送重试机制

```python
from push_tools import WeChatBot
from requests.exceptions import RequestException

bot = WeChatBot("your_webhook_url")


def send_with_retry(message, max_retries=3):
    for attempt in range(max_retries):
        try:
            return bot.send_text(message)
        except RequestException as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # 指数退避


send_with_retry("重要通知")
```

#### 批量发送消息
```python
messages = ["通知1", "通知2", "通知3"]
for msg in messages:
    try:
        bot.send_text(msg)
    except Exception as e:
        print(f"Failed to send message: {msg}. Error: {str(e)}")
```

### 邮件发送高级功能

#### 使用环境变量配置

```python
from push_tools import EmailSender
import os

sender = EmailSender(
    smtp_server=os.getenv("SMTP_SERVER"),
    smtp_port=int(os.getenv("SMTP_PORT", "587")),
    username=os.getenv("SMTP_USERNAME"),
    password=os.getenv("SMTP_PASSWORD")
)
```

#### 发送带多个收件人和附件的邮件
```python
sender.send_email(
    subject="项目报告",
    content="请查收项目报告",
    to_addrs=["user1@example.com", "user2@example.com"],
    cc_addrs=["manager@example.com"],
    attachments=["report.pdf", "data.xlsx"]
)
```

#### 邮件模板
```python
def send_welcome_email(user_email, user_name):
    content = f"""
    <h1>欢迎{user_name}加入我们！</h1>
    <p>您的账号已成功创建。</p>
    """
    sender.send_email(
        subject="欢迎邮件",
        content=content,
        to_addrs=user_email,
        html=True
    )
```

## 错误处理与调试

### 常见错误及解决方案

#### 企业微信机器人错误
1. **Webhook URL无效**
   - 检查URL是否正确
   - 确认机器人是否已启用

2. **消息发送失败**
   - 检查网络连接
   - 验证消息内容是否符合规范
   - 检查IP白名单设置

#### 邮件发送错误
1. **SMTP认证失败**
   - 检查用户名和密码
   - 确认服务器是否需要TLS/SSL

2. **附件发送失败**
   - 检查文件路径是否正确
   - 验证文件大小是否超过限制

### 日志记录
建议配置日志记录以帮助调试：
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("push_tools")

try:
    bot.send_text("测试消息")
except Exception as e:
    logger.error(f"消息发送失败: {str(e)}")
```

## 测试指南

### 运行测试套件
```bash
pytest tests/ --cov=push_tools --cov-report=html
```

### 测试覆盖率报告
测试完成后，可以在`htmlcov`目录中查看详细的覆盖率报告：
```bash
open htmlcov/index.html
```

### 静态类型检查
```bash
mypy push_tools/
```

### 代码风格检查
```bash
flake8 push_tools/
```

## 贡献指南

我们欢迎各种形式的贡献，包括但不限于：

1. **报告问题**
   - 在GitHub Issues中描述遇到的问题
   - 提供重现步骤和环境信息

2. **功能请求**
   - 详细描述需求场景
   - 说明预期的行为

3. **代码贡献**
   - Fork仓库并创建特性分支
   - 提交清晰的提交信息
   - 确保测试覆盖率不降低
   - 更新相关文档

4. **文档改进**
   - 修正拼写错误
   - 添加使用示例
   - 完善API文档

## 项目状态

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()
[![Build Status](https://img.shields.io/github/actions/workflow/status/yourusername/push-tool/python-package.yml)]()
[![Coverage](https://img.shields.io/codecov/c/github/yourusername/push-tool)]()
[![PyPI Version](https://img.shields.io/pypi/v/push-tool)]()

## 许可证

本项目采用 [MIT 许可证](https://choosealicense.com/licenses/mit/)。
