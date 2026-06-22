# 🔄 WxAuto OneBot V11 Framework

> **Language:** [中文](./README.md) | [English](./README_EN.md)

> 🚀 **基于 wxauto + OneBot V11 协议的微信消息转发框架**，支持 WebUI 配置管理、反向 WebSocket 通信、多媒体消息处理与窗口定时管理。

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)

---

## ✨ 核心功能

| 🔧 功能 | 📝 说明 |
|---------|---------|
| 🖥️ **WebUI 配置界面** | 支持深色/浅色主题，所有配置通过网页管理 |
| 📡 **反向 WebSocket** | 与 OneBot V11 兼容端点双向通信 |
| 💬 **多媒体消息** | 支持文字、图片、文件、语音消息转发 |
| 🪟 **窗口定时管理** | 自动最小化/恢复微信窗口 |
| 🔐 **Token 认证** | API 访问令牌 + 请求限流保护 |
| 🔄 **配置热更新** | 修改配置无需重启，自动检测变更 |
| 📋 **Schema 校验** | 配置文件结构校验，防止错误配置 |
| 📊 **日志轮转** | 自动轮转日志文件，防止磁盘占满 |
| 🐳 **Docker 支持** | 提供 Dockerfile 和 docker-compose.yml |

---

## 🏗️ 项目结构

```
├── main.py                   # 入口
├── requirements.txt          # 依赖
├── pyproject.toml            # 项目配置（ruff/pytest）
├── Makefile                  # 命令快捷方式
├── Dockerfile                # Docker 镜像
├── docker-compose.yml        # 容器编排
├── config/                   # 配置目录
│   ├── config.json           # 主配置
│   └── backups/              # 配置备份
├── src/                      # 源码
│   ├── config_manager.py     # 配置管理
│   ├── config_watcher.py     # 配置热更新
│   ├── constants.py          # 常量定义
│   ├── exceptions.py         # 自定义异常
│   ├── file_handler.py       # 文件处理（图片/文件/语音）
│   ├── logger.py             # 日志（支持轮转）
│   ├── message_filter.py     # 消息过滤
│   ├── message_handler.py    # 消息处理
│   ├── message_parser.py     # 消息解析
│   ├── onebot_converter.py   # OneBot V11 协议转换
│   ├── web_ui.py             # Web 界面（Flask）
│   ├── websocket_client.py   # WebSocket 客户端
│   ├── wechat_monitor.py     # 微信消息监听
│   └── window_controller.py  # 窗口定时管理
├── static/                   # 静态资源
├── tests/                    # 单元测试
└── cache/                    # 缓存目录
    ├── images/
    ├── files/
    └── voices/
```

---

## 🚀 快速开始

### 独立运行

```bash
pip install -r requirements.txt
python main.py
```

启动后访问 `http://localhost:10001`，首次启动会在日志中显示访问令牌。

### AstrBot 插件模式

作为 AstrBot 插件集成使用，配置后自动启动。

### Docker 部署

```bash
docker-compose up -d
```

---

## ⚙️ 配置说明

通过 WebUI 界面进行配置，所有配置保存在 `config/config.json`。

| 🔑 配置项 | 📖 说明 |
|----------|---------|
| 监听用户 | 要监听的用户列表 |
| WebSocket 地址 | 反向 WS 连接地址 |
| 窗口管理 | 定时最小化/恢复 |

---

## 🛠️ 开发命令

| 📋 命令 | 📖 说明 |
|---------|---------|
| `make install` | 安装依赖 |
| `make dev` | 安装开发依赖 |
| `make test` | 运行测试 |
| `make lint` | 代码检查 |
| `make format` | 格式化代码 |
| `make run` | 运行程序 |

---

## 📄 许可证

[MIT](LICENSE)
