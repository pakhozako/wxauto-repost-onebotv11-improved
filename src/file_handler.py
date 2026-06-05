"""
文件处理模块
负责保存图片、文件、语音等多媒体消息
"""

import time
from pathlib import Path
from typing import Optional, Any

from logger import logger


class FileHandler:
    """文件处理器"""
    
    def __init__(self, config_manager: Any) -> None:
        """初始化文件处理器
        
        Args:
            config_manager: 配置管理器
        """
        self.config_manager = config_manager
        
        # 获取项目根目录
        self.project_root = Path(__file__).parent.parent
        
        # 文件保存目录
        self.image_dir = self.project_root / config_manager.get('message.image_save_dir', 'cache/images')
        self.file_dir = self.project_root / config_manager.get('message.file_save_dir', 'cache/files')
        self.voice_dir = self.project_root / config_manager.get('message.voice_save_dir', 'cache/voices')
        
        # 创建目录
        self._ensure_dirs()
    
    def _ensure_dirs(self) -> None:
        """确保所有缓存目录存在"""
        self.image_dir.mkdir(parents=True, exist_ok=True)
        self.file_dir.mkdir(parents=True, exist_ok=True)
        self.voice_dir.mkdir(parents=True, exist_ok=True)
    
    def save_image(self, message: Any) -> Optional[str]:
        """保存图片消息
        
        Args:
            message: 消息对象
            
        Returns:
            保存的图片路径，失败返回None
        """
        if not self.config_manager.get('message.enable_image', True):
            return None
            
        try:
            # 生成文件名
            timestamp = int(time.time())
            filename = f"image_{timestamp}.jpg"
            file_path = self.image_dir / filename
            
            # 保存图片
            if hasattr(message, 'save_image'):
                message.save_image(str(file_path))
                logger.info(f"图片已保存: {filename}")
                return str(file_path)
            elif hasattr(message, 'image_path'):
                return message.image_path
                
            return None
            
        except Exception as e:
            logger.error(f"保存图片失败: {e}")
            return None
    
    def save_file(self, message: Any) -> Optional[str]:
        """保存文件消息
        
        Args:
            message: 消息对象
            
        Returns:
            保存的文件路径，失败返回None
        """
        if not self.config_manager.get('message.enable_file', True):
            return None
            
        try:
            # 生成文件名
            timestamp = int(time.time())
            original_name = getattr(message, 'filename', f'file_{timestamp}')
            file_path = self.file_dir / f"{timestamp}_{original_name}"
            
            # 保存文件
            if hasattr(message, 'save_file'):
                message.save_file(str(file_path))
                logger.info(f"文件已保存: {original_name}")
                return str(file_path)
            elif hasattr(message, 'file_path'):
                return message.file_path
                
            return None
            
        except Exception as e:
            logger.error(f"保存文件失败: {e}")
            return None
    
    def save_voice(self, message: Any) -> Optional[str]:
        """保存语音消息
        
        Args:
            message: 消息对象
            
        Returns:
            保存的语音路径，失败返回None
        """
        try:
            # 生成文件名
            timestamp = int(time.time())
            filename = f"voice_{timestamp}.wav"
            file_path = self.voice_dir / filename
            
            # 保存语音
            if hasattr(message, 'save_voice'):
                message.save_voice(str(file_path))
                logger.info(f"语音已保存: {filename}")
                return str(file_path)
            elif hasattr(message, 'voice_path'):
                return message.voice_path
                
            return None
            
        except Exception as e:
            logger.error(f"保存语音失败: {e}")
            return None
