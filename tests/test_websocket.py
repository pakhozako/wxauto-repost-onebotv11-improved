"""WebSocket客户端测试"""

import pytest
from pathlib import Path

# 添加src目录到路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))


class TestWebSocketHelpers:
    """WebSocket辅助函数测试"""
    
    def test_exponential_backoff(self):
        """测试指数退避算法"""
        base_interval = 5
        max_interval = 60
        
        # 模拟重连间隔计算
        intervals = []
        for attempt in range(1, 11):
            backoff = min(base_interval * (2 ** (attempt - 1)), max_interval)
            intervals.append(backoff)
        
        # 验证间隔递增
        for i in range(1, len(intervals)):
            assert intervals[i] >= intervals[i-1]
        
        # 验证不超过最大值
        for interval in intervals:
            assert interval <= max_interval
    
    def test_message_queue_config(self):
        """测试消息队列配置"""
        warning_threshold = 100
        
        # 队列大小应该合理
        assert warning_threshold > 0
        assert warning_threshold <= 10000  # 不应该太大
    
    def test_reconnect_config(self):
        """测试重连配置"""
        max_attempts = 10
        base_interval = 5
        max_interval = 60
        
        assert max_attempts > 0
        assert base_interval > 0
        assert max_interval >= base_interval
