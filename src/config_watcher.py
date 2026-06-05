"""
配置文件监视器
监听配置文件变化，实现热更新
"""

import time
import threading
from pathlib import Path
from typing import Callable, Optional
from logger import logger


class ConfigWatcher:
    """配置文件监视器"""
    
    def __init__(self, config_path: Path, on_change: Callable[[], None]) -> None:
        """初始化配置监视器
        
        Args:
            config_path: 配置文件路径
            on_change: 配置变化时的回调函数
        """
        self.config_path = config_path
        self.on_change = on_change
        self.running = False
        self.watch_thread: Optional[threading.Thread] = None
        self.last_modified: float = 0
        self.check_interval: float = 2.0  # 检查间隔（秒）
        
    def start(self) -> None:
        """启动监视"""
        if self.running:
            return
            
        self.running = True
        self.last_modified = self._get_modified_time()
        
        self.watch_thread = threading.Thread(target=self._watch_loop, daemon=True)
        self.watch_thread.start()
        logger.info(f"配置文件监视已启动: {self.config_path}")
        
    def stop(self) -> None:
        """停止监视"""
        self.running = False
        if self.watch_thread and self.watch_thread.is_alive():
            self.watch_thread.join(timeout=3)
        logger.info("配置文件监视已停止")
        
    def _get_modified_time(self) -> float:
        """获取文件修改时间"""
        try:
            return self.config_path.stat().st_mtime
        except FileNotFoundError:
            return 0
            
    def _watch_loop(self) -> None:
        """监视循环"""
        while self.running:
            try:
                current_modified = self._get_modified_time()
                
                if current_modified > self.last_modified:
                    logger.info("检测到配置文件变化，重新加载...")
                    self.last_modified = current_modified
                    
                    try:
                        self.on_change()
                        logger.info("配置热更新成功")
                    except Exception as e:
                        logger.error(f"配置热更新失败: {e}")
                        
                time.sleep(self.check_interval)
                
            except Exception as e:
                logger.error(f"配置监视异常: {e}")
                time.sleep(5)
