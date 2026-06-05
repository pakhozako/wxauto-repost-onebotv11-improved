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
├── main.py                 # 入口
├── requirements.txt        # 依赖
├── config/                 # 配置
├── src/                    # 源码
│   ├── config_manager.py   # 配置管理
│   ├── wechat_monitor.py   # 消息监听
│   ├── onebot_converter.py # 协议转换
│   ├── websocket_client.py # WS 客户端
│   ├── message_handler.py  # 消息处理
│   ├── window_controller.py# 窗口管理
│   ├── web_ui.py           # Web 界面
│   └── logger.py           # 日志模块
└── static/                 # 静态资源
```

## 许可证

MIT License
