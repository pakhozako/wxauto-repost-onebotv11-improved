"""日志模块测试"""

import pytest
from pathlib import Path

# 添加src目录到路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from logger import get_logger


class TestLogger:
    """日志模块测试类"""
    
    def test_get_logger_default(self):
        """测试获取默认logger"""
        logger = get_logger()
        assert logger is not None
        assert hasattr(logger, 'info')
        assert hasattr(logger, 'error')
        assert hasattr(logger, 'warning')
        assert hasattr(logger, 'debug')
    
    def test_get_logger_custom_name(self):
        """测试获取自定义名称logger"""
        logger = get_logger('test_logger')
        assert logger is not None
    
    def test_logger_singleton(self):
        """测试logger单例模式"""
        logger1 = get_logger('same_name')
        logger2 = get_logger('same_name')
        assert logger1 is logger2
