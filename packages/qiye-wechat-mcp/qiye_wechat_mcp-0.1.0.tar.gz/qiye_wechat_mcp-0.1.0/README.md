# 企业微信消息 MCP 服务器

超简单的企业微信群机器人 MCP 服务器，让 AI 助手能发送消息到企业微信群。

## 安装

### 方式一：pip安装（推荐）
```bash
pip install qiye-wechat-mcp
```

### 方式二：从源码安装
```bash
git clone https://github.com/example/qiye-wechat-mcp.git
cd qiye-wechat-mcp
pip install -e .
```

## 快速开始

### 1. 配置企业微信群机器人
1. 在企业微信群中添加群机器人
2. 复制机器人的 Webhook URL

### 2. 设置环境变量
```bash
# 设置环境变量
export WECHAT_WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-webhook-key"

# 或者创建 .env 文件
echo "WECHAT_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-webhook-key" > .env
```

### 3. 运行服务器

#### 使用命令行工具
```bash
qiye-wechat-mcp
```

#### 或使用Python模块
```bash
python -m qiye_wechat_mcp
```

### 4. 配置 Claude Desktop
在 Claude Desktop 配置文件中添加：

```json
{
  "mcpServers": {
    "企业微信": {
      "command": "qiye-wechat-mcp",
      "env": {
        "WECHAT_WEBHOOK_URL": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-webhook-key"
      }
    }
  }
}
```

或者使用Python模块方式：
```json
{
  "mcpServers": {
    "企业微信": {
      "command": "python",
      "args": ["-m", "qiye_wechat_mcp"],
      "env": {
        "WECHAT_WEBHOOK_URL": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=your-webhook-key"
      }
    }
  }
}
```

## 功能
- `send_text_message(content)` - 发送文本消息
- `send_markdown_message(content)` - 发送Markdown消息

## 发布到PyPI

### 构建包
```bash
python setup.py sdist bdist_wheel
```

### 上传到PyPI
```bash
pip install twine
twine upload dist/*
```

就这么简单！
