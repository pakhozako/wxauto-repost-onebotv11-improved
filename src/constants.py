"""
常量定义模块
集中管理项目中的常量
"""

from pathlib import Path

# ==================== 路径常量 ====================
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
CACHE_DIR = PROJECT_ROOT / "cache"
LOG_DIR = PROJECT_ROOT / "wxauto_logs"

# 默认缓存子目录
DEFAULT_IMAGE_DIR = "cache/images"
DEFAULT_FILE_DIR = "cache/files"
DEFAULT_VOICE_DIR = "cache/voices"

# ==================== 配置常量 ====================
DEFAULT_CONFIG_FILE = "config.json"
BACKUP_DIR_NAME = "backups"
MAX_BACKUP_COUNT = 5

# ==================== 默认配置值 ====================
DEFAULT_WEBUI_HOST = "0.0.0.0"
DEFAULT_WEBUI_PORT = 10001
DEFAULT_WEBUI_DEBUG = False

DEFAULT_WECHAT_ENABLED = False
DEFAULT_CHECK_INTERVAL = 1.0
DEFAULT_AUTO_REPLY = False

DEFAULT_WINDOW_MINIMIZE_ENABLED = False
DEFAULT_WINDOW_MINIMIZE_INTERVAL = 3600
DEFAULT_WINDOW_RESTORE_DELAY = 1.0

DEFAULT_ONEBOT_ENABLED = False
DEFAULT_ONEBOT_WS_URL = "ws://localhost:10001/ws"
DEFAULT_ONEBOT_ACCESS_TOKEN = ""
DEFAULT_ONEBOT_RECONNECT_INTERVAL = 5
DEFAULT_ONEBOT_HEARTBEAT_INTERVAL = 30
DEFAULT_ONEBOT_SELF_ID = "wxauto_bot"

DEFAULT_MESSAGE_MAX_LENGTH = 4096
DEFAULT_ENABLE_IMAGE = True
DEFAULT_ENABLE_FILE = True
DEFAULT_ENABLE_VOICE = False

DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
DEFAULT_LOG_BACKUP_COUNT = 5

# ==================== WebSocket常量 ====================
WS_MAX_RECONNECT_ATTEMPTS = 10
WS_BASE_RECONNECT_INTERVAL = 5
WS_MAX_RECONNECT_INTERVAL = 60
WS_HEARTBEAT_INTERVAL = 30
WS_CONNECTION_TIMEOUT = 10

# ==================== 消息处理常量 ====================
MESSAGE_QUEUE_WARNING_THRESHOLD = 100
MESSAGE_CACHE_EXPIRE_TIME = 3600  # 1小时
SENT_MESSAGE_CACHE_EXPIRE_TIME = 30  # 30秒

# ==================== 系统消息关键词 ====================
SYSTEM_MESSAGE_KEYWORDS = [
    "以下为新消息",
    "以上为历史消息",
    "消息记录",
    "聊天记录",
    "历史消息",
    "系统消息",
    "新消息",
    "撤回了一条消息",
    "撤回了消息",
    "withdrew a message",
    "消息提醒",
    "系统提示",
    "消息通知"
]

# ==================== wxauto调试消息关键词 ====================
WXAUTO_DEBUG_KEYWORDS = [
    "[wxauto]",
    "[WXAuto]",
    "wxauto",
    "listening",
    "监听中",
    "开始监听"
]

# ==================== OneBotV11常量 ====================
ONEBOT_VERSION = "11"
ONEBOT_POST_TYPE_MESSAGE = "message"
ONEBOT_POST_TYPE_META_EVENT = "meta_event"
ONEBOT_POST_TYPE_REQUEST = "request"
ONEBOT_POST_TYPE_NOTICE = "notice"

ONEBOT_MESSAGE_TYPE_PRIVATE = "private"
ONEBOT_MESSAGE_TYPE_GROUP = "group"

ONEBOT_SUB_TYPE_FRIEND = "friend"
ONEBOT_SUB_TYPE_NORMAL = "normal"

# ==================== API响应码 ====================
API_SUCCESS = 0
API_ERROR_ASYNC = 1
API_ERROR_BAD_REQUEST = 100
API_ERROR_UNSUPPORTED_ACTION = 1404
API_ERROR_INTERNAL = 1500
