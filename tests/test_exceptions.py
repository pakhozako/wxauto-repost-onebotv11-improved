"""异常类测试"""

import pytest
from pathlib import Path

# 添加src目录到路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from exceptions import (
    WxAutoError, ConfigError, ConfigLoadError, ConfigSaveError, ConfigValidationError,
    WeChatError, WeChatNotRunningError, WeChatSendError,
    WebSocketError, WebSocketConnectionError, WebSocketTimeoutError,
    MessageError, MessageParseError, MessageFilterError,
    FileError, FileDownloadError, FileSaveError
)


class TestExceptions:
    """异常类测试"""
    
    def test_wxauto_error(self):
        """测试基础异常"""
        with pytest.raises(WxAutoError):
            raise WxAutoError("test error")
    
    def test_config_error_hierarchy(self):
        """测试配置异常继承关系"""
        assert issubclass(ConfigError, WxAutoError)
        assert issubclass(ConfigLoadError, ConfigError)
        assert issubclass(ConfigSaveError, ConfigError)
        assert issubclass(ConfigValidationError, ConfigError)
    
    def test_wechat_error_hierarchy(self):
        """测试微信异常继承关系"""
        assert issubclass(WeChatError, WxAutoError)
        assert issubclass(WeChatNotRunningError, WeChatError)
        assert issubclass(WeChatSendError, WeChatError)
    
    def test_websocket_error_hierarchy(self):
        """测试WebSocket异常继承关系"""
        assert issubclass(WebSocketError, WxAutoError)
        assert issubclass(WebSocketConnectionError, WebSocketError)
        assert issubclass(WebSocketTimeoutError, WebSocketError)
    
    def test_message_error_hierarchy(self):
        """测试消息异常继承关系"""
        assert issubclass(MessageError, WxAutoError)
        assert issubclass(MessageParseError, MessageError)
        assert issubclass(MessageFilterError, MessageError)
    
    def test_file_error_hierarchy(self):
        """测试文件异常继承关系"""
        assert issubclass(FileError, WxAutoError)
        assert issubclass(FileDownloadError, FileError)
        assert issubclass(FileSaveError, FileError)
    
    def test_exception_message(self):
        """测试异常消息"""
        error = ConfigLoadError("配置加载失败: file not found")
        assert "配置加载失败" in str(error)
        assert "file not found" in str(error)
    
    def test_exception_catch_hierarchy(self):
        """测试异常捕获层级"""
        # ConfigLoadError 应该能被 ConfigError 和 WxAutoError 捕获
        try:
            raise ConfigLoadError("test")
        except ConfigError:
            pass  # 应该被捕获
        
        try:
            raise ConfigLoadError("test")
        except WxAutoError:
            pass  # 应该被捕获
