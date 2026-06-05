"""消息过滤器测试"""

import pytest
from pathlib import Path

# 添加src目录到路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from message_filter import MessageFilter


class TestMessageFilter:
    """消息过滤器测试类"""
    
    def test_empty_content(self):
        """测试空内容"""
        assert MessageFilter.is_system_message("") == True
        assert MessageFilter.is_system_message(None) == True
        assert MessageFilter.is_system_message("   ") == True
    
    def test_normal_message(self):
        """测试普通消息"""
        assert MessageFilter.is_system_message("你好") == False
        assert MessageFilter.is_system_message("今天天气怎么样？") == False
        assert MessageFilter.is_system_message("Hello World") == False
    
    def test_system_keywords(self):
        """测试系统消息关键词"""
        assert MessageFilter.is_system_message("--- 以上为历史消息 ---") == True
        assert MessageFilter.is_system_message("--- 以下为新消息 ---") == True
        assert MessageFilter.is_system_message("撤回了一条消息") == True
        assert MessageFilter.is_system_message("系统消息") == True
        assert MessageFilter.is_system_message("系统提示") == True
    
    def test_system_patterns(self):
        """测试系统消息模式"""
        assert MessageFilter.is_system_message("[系统消息]") == True
        assert MessageFilter.is_system_message("[提示]") == True
        assert MessageFilter.is_system_message("[通知]") == True
        assert MessageFilter.is_system_message("...") == True
        assert MessageFilter.is_system_message("…") == True
        assert MessageFilter.is_system_message("---") == True
    
    def test_wxauto_debug_message(self):
        """测试wxauto调试消息"""
        assert MessageFilter.is_wxauto_debug_message("[wxauto] 开始监听") == True
        assert MessageFilter.is_wxauto_debug_message("wxauto listening") == True
        assert MessageFilter.is_wxauto_debug_message("正常消息") == False


class TestMessageParser:
    """消息解析器测试类"""
    
    def test_get_chat_username_nickname(self):
        """测试获取用户名（有nickname属性）"""
        from message_parser import MessageParser
        
        class MockConfig:
            def get(self, key, default=None):
                return default
        
        parser = MessageParser(MockConfig())
        
        class MockChat:
            nickname = "测试用户"
        
        assert parser.get_chat_username(MockChat()) == "测试用户"
    
    def test_get_chat_username_name(self):
        """测试获取用户名（有name属性）"""
        from message_parser import MessageParser
        
        class MockConfig:
            def get(self, key, default=None):
                return default
        
        parser = MessageParser(MockConfig())
        
        class MockChat:
            name = "测试用户"
        
        assert parser.get_chat_username(MockChat()) == "测试用户"
    
    def test_get_chat_username_string(self):
        """测试获取用户名（从字符串提取）"""
        from message_parser import MessageParser
        
        class MockConfig:
            def get(self, key, default=None):
                return default
        
        parser = MessageParser(MockConfig())
        
        class MockChat:
            def __str__(self):
                return 'Chat("测试用户")'
        
        assert parser.get_chat_username(MockChat()) == "测试用户"


class TestFileHandler:
    """文件处理器测试类"""
    
    def test_init_dirs(self, tmp_path):
        """测试初始化目录"""
        from file_handler import FileHandler
        
        class MockConfig:
            def get(self, key, default=None):
                if key == 'message.image_save_dir':
                    return str(tmp_path / 'images')
                elif key == 'message.file_save_dir':
                    return str(tmp_path / 'files')
                elif key == 'message.voice_save_dir':
                    return str(tmp_path / 'voices')
                return default
        
        handler = FileHandler(MockConfig())
        assert handler.image_dir.exists()
        assert handler.file_dir.exists()
        assert handler.voice_dir.exists()
