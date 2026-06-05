"""日志模块测试（含轮转）"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# 添加src目录到路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))


class TestLogger:
    """日志模块测试"""
    
    def test_get_logger_default(self):
        """测试获取默认logger"""
        from logger import get_logger
        logger = get_logger()
        assert logger is not None
        assert hasattr(logger, 'info')
        assert hasattr(logger, 'error')
        assert hasattr(logger, 'warning')
        assert hasattr(logger, 'debug')
    
    def test_get_logger_custom_name(self):
        """测试获取自定义名称logger"""
        from logger import get_logger
        logger = get_logger('test_logger')
        assert logger is not None
    
    def test_logger_singleton(self):
        """测试logger单例模式"""
        from logger import get_logger
        logger1 = get_logger('same_name')
        logger2 = get_logger('same_name')
        assert logger1 is logger2
    
    def test_logger_handlers(self):
        """测试logger处理器"""
        from logger import get_logger
        logger = get_logger('test_handlers')
        # 应该有控制台和文件两个处理器
        assert len(logger.handlers) >= 1
    
    def test_logger_level(self):
        """测试logger级别"""
        from logger import get_logger
        logger = get_logger('test_level')
        # 默认应该是DEBUG级别（最低）
        assert logger.level <= 10  # DEBUG = 10
