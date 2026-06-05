"""配置监视器测试"""

import pytest
import time
import tempfile
from pathlib import Path

# 添加src目录到路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from config_watcher import ConfigWatcher


class TestConfigWatcher:
    """配置监视器测试"""
    
    def test_init(self, tmp_path):
        """测试初始化"""
        config_file = tmp_path / "config.json"
        config_file.write_text("{}")
        
        callback_called = False
        def on_change():
            nonlocal callback_called
            callback_called = True
            
        watcher = ConfigWatcher(config_file, on_change)
        assert watcher.config_path == config_file
        assert watcher.running == False
    
    def test_start_stop(self, tmp_path):
        """测试启动和停止"""
        config_file = tmp_path / "config.json"
        config_file.write_text("{}")
        
        watcher = ConfigWatcher(config_file, lambda: None)
        
        watcher.start()
        assert watcher.running == True
        assert watcher.watch_thread is not None
        
        watcher.stop()
        assert watcher.running == False
    
    def test_detect_change(self, tmp_path):
        """测试检测文件变化"""
        config_file = tmp_path / "config.json"
        config_file.write_text("{}")
        
        change_detected = False
        def on_change():
            nonlocal change_detected
            change_detected = True
            
        watcher = ConfigWatcher(config_file, on_change)
        watcher.check_interval = 0.1  # 加快检查频率
        watcher.start()
        
        # 修改文件
        time.sleep(0.2)
        config_file.write_text('{"key": "value"}')
        
        # 等待检测
        time.sleep(0.3)
        
        watcher.stop()
        assert change_detected == True
