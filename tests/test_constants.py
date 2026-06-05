"""常量模块测试"""

import pytest
from pathlib import Path

# 添加src目录到路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from constants import (
    PROJECT_ROOT, CONFIG_DIR, CACHE_DIR, LOG_DIR,
    DEFAULT_WEBUI_PORT, DEFAULT_WECHAT_ENABLED,
    DEFAULT_ONEBOT_ENABLED, DEFAULT_ONEBOT_WS_URL,
    SYSTEM_MESSAGE_KEYWORDS, WXAUTO_DEBUG_KEYWORDS,
    WS_MAX_RECONNECT_ATTEMPTS, API_SUCCESS
)


class TestConstants:
    """常量模块测试"""
    
    def test_project_root_exists(self):
        """测试项目根目录"""
        assert PROJECT_ROOT.exists()
        assert PROJECT_ROOT.is_dir()
    
    def test_path_types(self):
        """测试路径类型"""
        assert isinstance(PROJECT_ROOT, Path)
        assert isinstance(CONFIG_DIR, Path)
        assert isinstance(CACHE_DIR, Path)
        assert isinstance(LOG_DIR, Path)
    
    def test_default_values(self):
        """测试默认值类型"""
        assert isinstance(DEFAULT_WEBUI_PORT, int)
        assert isinstance(DEFAULT_WECHAT_ENABLED, bool)
        assert isinstance(DEFAULT_ONEBOT_ENABLED, bool)
        assert isinstance(DEFAULT_ONEBOT_WS_URL, str)
    
    def test_default_port_range(self):
        """测试默认端口范围"""
        assert 1 <= DEFAULT_WEBUI_PORT <= 65535
    
    def test_keywords_is_list(self):
        """测试关键词列表类型"""
        assert isinstance(SYSTEM_MESSAGE_KEYWORDS, list)
        assert isinstance(WXAUTO_DEBUG_KEYWORDS, list)
    
    def test_keywords_not_empty(self):
        """测试关键词列表非空"""
        assert len(SYSTEM_MESSAGE_KEYWORDS) > 0
        assert len(WXAUTO_DEBUG_KEYWORDS) > 0
    
    def test_reconnect_constants(self):
        """测试重连常量"""
        assert WS_MAX_RECONNECT_ATTEMPTS > 0
        assert isinstance(WS_MAX_RECONNECT_ATTEMPTS, int)
    
    def test_api_constants(self):
        """测试API常量"""
        assert API_SUCCESS == 0
        assert isinstance(API_SUCCESS, int)
