# WxAuto OneBot V11 Framework

基于 wxauto 和 OneBot V11 协议的消息转发框架，支持 WebUI 配置管理。

## 运行模式

- **独立模式**：直接运行 `python main.py`
- **AstrBot 插件模式**：作为 AstrBot 插件集成使用

## 功能

- WebUI 配置界面（支持深色/浅色主题）
- 消息监听与协议转换
- 反向 WebSocket 通信
- 多媒体消息支持（文字、图片、文件）
- 窗口定时管理
- Token 认证与 API 限流
- 配置 Schema 校验
- 配置热更新
- 日志轮转

## 安装

```bash
pip install -r requirements.txt
```

## 使用

```bash
python main.py
```

启动后访问 `http://localhost:10001`，首次启动会在日志中显示访问令牌。

## 配置

通过 WebUI 界面进行配置，所有配置保存在 `config/config.json`。

### 主要配置项

| 配置 | 说明 |
|------|------|
| 监听用户 | 要监听的用户列表 |
| WebSocket 地址 | 反向 WS 连接地址 |
| 窗口管理 | 定时最小化/恢复 |

## 项目结构

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
│   ├── message_filter.py     # 消息过滤（系统消息/调试消息）
│   ├── message_handler.py    # 消息处理（API/回复）
│   ├── message_parser.py     # 消息解析
│   ├── onebot_converter.py   # OneBot V11 协议转换
│   ├── web_ui.py             # Web 界面（Flask）
│   ├── websocket_client.py   # WebSocket 客户端
│   ├── wechat_monitor.py     # 微信消息监听
│   └── window_controller.py  # 窗口定时管理
├── static/                   # 静态资源
│   └── css/
│       └── style.css
├── tests/                    # 单元测试
│   ├── test_config_manager.py
│   ├── test_config_watcher.py
│   ├── test_constants.py
│   ├── test_cq_parser.py
│   ├── test_exceptions.py
│   ├── test_logger.py
│   ├── test_logger_advanced.py
│   ├── test_message_modules.py
│   ├── test_onebot_converter.py
│   ├── test_web_ui.py
│   └── test_websocket.py
└── cache/                    # 缓存目录
    ├── images/
    ├── files/
    └── voices/
```

## 开发

```bash
make install     # 安装依赖
make dev         # 安装开发依赖
make test        # 运行测试
make lint        # 代码检查
make format      # 格式化代码
make run         # 运行程序
```

## 许可证

MIT License
