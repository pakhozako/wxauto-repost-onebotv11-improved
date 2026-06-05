"""CQ码解析测试"""

import pytest
from pathlib import Path

# 添加src目录到路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from message_handler import MessageHandler


@pytest.fixture
def handler():
    """创建消息处理器实例"""
    class MockConfigManager:
        def get(self, key, default=None):
            return default
        def get_monitor_users(self):
            return []
    
    class MockWeChatMonitor:
        def send_message(self, user, content):
            return True
    
    class MockOneBotConverter:
        self_id = 'test_bot'
    
    class MockWebSocketClient:
        is_connected = True
        def set_callbacks(self, **kwargs):
            pass
    
    return MessageHandler(
        MockConfigManager(),
        MockWeChatMonitor(),
        MockOneBotConverter(),
        MockWebSocketClient()
    )


class TestCQCodeParser:
    """CQ码解析测试类"""
    
    def test_parse_plain_text(self, handler):
        """测试解析纯文本"""
        result = handler._parse_cq_code("hello world")
        assert len(result) == 1
        assert result[0]['type'] == 'text'
        assert result[0]['data']['text'] == 'hello world'
    
    def test_parse_single_cq_code(self, handler):
        """测试解析单个CQ码"""
        result = handler._parse_cq_code("[CQ:image,file=test.jpg]")
        assert len(result) == 1
        assert result[0]['type'] == 'image'
        assert result[0]['data']['file'] == 'test.jpg'
    
    def test_parse_mixed_content(self, handler):
        """测试解析混合内容"""
        result = handler._parse_cq_code("看这张图[CQ:image,file=test.jpg]漂亮吗")
        assert len(result) == 3
        assert result[0]['type'] == 'text'
        assert result[0]['data']['text'] == '看这张图'
        assert result[1]['type'] == 'image'
        assert result[2]['type'] == 'text'
        assert result[2]['data']['text'] == '漂亮吗'
    
    def test_parse_cq_code_with_special_chars(self, handler):
        """测试解析包含特殊字符的CQ码"""
        result = handler._parse_cq_code("[CQ:text,text=hello&#91;world&#93;]")
        assert len(result) == 1
        assert result[0]['type'] == 'text'
        assert result[0]['data']['text'] == 'hello[world]'
    
    def test_parse_at_message(self, handler):
        """测试解析@消息"""
        result = handler._parse_cq_code("[CQ:at,qq=12345] 你好")
        assert len(result) == 2
        assert result[0]['type'] == 'at'
        assert result[0]['data']['qq'] == '12345'
        assert result[1]['type'] == 'text'
        assert result[1]['data']['text'] == ' 你好'
