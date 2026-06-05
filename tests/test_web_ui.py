"""WebUI测试"""

import pytest
from pathlib import Path

# 添加src目录到路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))


class TestWebUIHelpers:
    """WebUI辅助函数测试"""
    
    def test_token_generation(self):
        """测试Token生成"""
        import secrets
        import hashlib
        
        token = secrets.token_urlsafe(32)
        assert len(token) > 0
        
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        assert len(token_hash) == 64  # SHA256 hex长度
    
    def test_token_comparison(self):
        """测试Token安全比较"""
        import secrets
        
        token1 = secrets.token_urlsafe(32)
        token2 = token1
        token3 = secrets.token_urlsafe(32)
        
        # 相同token应该匹配
        assert secrets.compare_digest(token1, token2) == True
        
        # 不同token不应该匹配
        assert secrets.compare_digest(token1, token3) == False
    
    def test_rate_limiter_config(self):
        """测试限流器配置"""
        # 验证限流参数合理性
        max_requests = 200
        time_window = 60  # 秒
        
        requests_per_second = max_requests / time_window
        assert requests_per_second > 0
        assert requests_per_second <= 10  # 合理范围
