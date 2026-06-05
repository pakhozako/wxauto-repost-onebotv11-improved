"""OneBot转换器测试"""

import pytest
from pathlib import Path

# 添加src目录到路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from onebot_converter import OneBotV11Converter


@pytest.fixture
def converter():
    """创建转换器实例"""
    class MockConfigManager:
        def get(self, key, default=None):
            if key == 'onebot.self_id':
                return 'test_bot'
            return default
    
    return OneBotV11Converter(MockConfigManager())


class TestOneBotConverter:
    """OneBot转换器测试类"""
    
    def test_init(self, converter):
        """测试初始化"""
        assert converter.self_id == 'test_bot'
    
    def test_generate_message_id(self, converter):
        """测试生成消息ID"""
        wechat_msg = {
            'user_name': 'test_user',
            'content': 'hello',
            'timestamp': 1234567890
        }
        msg_id = converter._generate_message_id(wechat_msg)
        assert isinstance(msg_id, int)
        assert msg_id > 0
    
    def test_wechat_to_onebot_text(self, converter):
        """测试文本消息转换"""
        wechat_msg = {
            'user_name': 'test_user',
            'user_id': '12345',
            'content': 'hello world',
            'message_type': 'text',
            'timestamp': 1234567890
        }
        onebot_msg = converter.wechat_to_onebot(wechat_msg)
        
        assert onebot_msg['post_type'] == 'message'
        assert onebot_msg['message_type'] == 'private'
        assert onebot_msg['user_id'] == '12345'
        assert onebot_msg['self_id'] == 'test_bot'
    
    def test_create_lifecycle_event(self, converter):
        """测试生命周期事件"""
        event = converter.create_lifecycle_event('connect')
        
        assert event['post_type'] == 'meta_event'
        assert event['meta_event_type'] == 'lifecycle'
        assert event['sub_type'] == 'connect'
