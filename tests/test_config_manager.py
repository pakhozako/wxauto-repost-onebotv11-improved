"""配置管理器测试"""

import json
import pytest
from pathlib import Path
from unittest.mock import MagicMock

# 添加src目录到路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from config_manager import ConfigManager


@pytest.fixture
def config_manager(tmp_path):
    """创建临时配置管理器实例"""
    config_file = tmp_path / "config.json"
    return ConfigManager(str(config_file))


class TestConfigManager:
    """配置管理器测试类"""
    
    def test_init_default_config(self, config_manager):
        """测试默认配置初始化"""
        assert config_manager.get('webui.port') == 10001
        assert config_manager.get('wechat.enabled') == False
        assert config_manager.get('onebot.enabled') == False
    
    def test_get_nested_key(self, config_manager):
        """测试获取嵌套配置"""
        assert config_manager.get('wechat.window_minimize.enabled') == False
        assert config_manager.get('wechat.window_minimize.interval') == 3600
    
    def test_get_with_default(self, config_manager):
        """测试获取配置带默认值"""
        assert config_manager.get('nonexistent.key', 'default') == 'default'
    
    def test_set_config(self, config_manager):
        """测试设置配置"""
        assert config_manager.set('webui.port', 8080) == True
        assert config_manager.get('webui.port') == 8080
    
    def test_set_nested_config(self, config_manager):
        """测试设置嵌套配置"""
        assert config_manager.set('wechat.enabled', True) == True
        assert config_manager.get('wechat.enabled') == True
    
    def test_save_and_load(self, config_manager):
        """测试保存和加载配置"""
        config_manager.set('webui.port', 9999)
        assert config_manager.save_config() == True
        
        # 重新加载
        new_manager = ConfigManager(str(config_manager.config_file))
        assert new_manager.get('webui.port') == 9999
    
    def test_validate_config(self, config_manager):
        """测试配置验证"""
        errors = config_manager.validate_config()
        assert isinstance(errors, list)
    
    def test_add_monitor_user_string(self, config_manager):
        """测试添加监听用户（字符串格式）"""
        assert config_manager.add_monitor_user('test_user') == True
        users = config_manager.get('wechat.monitor_users')
        assert 'test_user' in users
    
    def test_add_monitor_user_dict(self, config_manager):
        """测试添加监听用户（字典格式）"""
        user_data = {'nickname': 'test', 'user_id': '12345'}
        assert config_manager.add_monitor_user(user_data) == True
        users = config_manager.get('wechat.monitor_users')
        assert user_data in users
    
    def test_remove_monitor_user(self, config_manager):
        """测试移除监听用户"""
        config_manager.add_monitor_user('test_user')
        assert config_manager.remove_monitor_user('test_user') == True
        users = config_manager.get('wechat.monitor_users')
        assert 'test_user' not in users
    
    def test_update_config(self, config_manager):
        """测试批量更新配置"""
        updates = {
            'webui': {'port': 8888},
            'wechat': {'enabled': True}
        }
        assert config_manager.update(updates) == True
        assert config_manager.get('webui.port') == 8888
        assert config_manager.get('wechat.enabled') == True
    
    def test_get_all(self, config_manager):
        """测试获取所有配置"""
        config = config_manager.get_all()
        assert isinstance(config, dict)
        assert 'webui' in config
        assert 'wechat' in config
        assert 'onebot' in config
