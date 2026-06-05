"""
自定义异常模块
定义项目专用的异常类
"""


class WxAutoError(Exception):
    """WxAuto基础异常"""
    pass


class ConfigError(WxAutoError):
    """配置相关异常"""
    pass


class ConfigLoadError(ConfigError):
    """配置加载异常"""
    pass


class ConfigSaveError(ConfigError):
    """配置保存异常"""
    pass


class ConfigValidationError(ConfigError):
    """配置验证异常"""
    pass


class WeChatError(WxAutoError):
    """微信相关异常"""
    pass


class WeChatNotRunningError(WeChatError):
    """微信未运行异常"""
    pass


class WeChatSendError(WeChatError):
    """微信发送消息异常"""
    pass


class WebSocketError(WxAutoError):
    """WebSocket相关异常"""
    pass


class WebSocketConnectionError(WebSocketError):
    """WebSocket连接异常"""
    pass


class WebSocketTimeoutError(WebSocketError):
    """WebSocket超时异常"""
    pass


class MessageError(WxAutoError):
    """消息处理异常"""
    pass


class MessageParseError(MessageError):
    """消息解析异常"""
    pass


class MessageFilterError(MessageError):
    """消息过滤异常"""
    pass


class FileError(WxAutoError):
    """文件处理异常"""
    pass


class FileDownloadError(FileError):
    """文件下载异常"""
    pass


class FileSaveError(FileError):
    """文件保存异常"""
    pass
