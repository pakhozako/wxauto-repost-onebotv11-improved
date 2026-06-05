"""
统一日志模块
支持独立运行模式和AstrBot插件模式，支持日志轮转
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from constants import LOG_DIR, DEFAULT_LOG_MAX_SIZE, DEFAULT_LOG_BACKUP_COUNT


def get_logger(name: str = "wxauto") -> logging.Logger:
    """获取统一的日志记录器
    
    Args:
        name: 日志记录器名称
        
    Returns:
        日志记录器实例
    """
    try:
        # 尝试使用AstrBot的日志系统
        from astrbot.api import logger
        return logger
    except ImportError:
        pass
    
    # 独立运行模式：使用标准logging
    logger_instance = logging.getLogger(name)
    
    if not logger_instance.handlers:
        logger_instance.setLevel(logging.DEBUG)
        
        # 控制台输出
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        logger_instance.addHandler(console_handler)
        
        # 文件输出（带轮转）
        try:
            LOG_DIR.mkdir(parents=True, exist_ok=True)
            
            from datetime import datetime
            log_file = LOG_DIR / f"app_{datetime.now().strftime('%Y%m%d')}.log"
            
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=DEFAULT_LOG_MAX_SIZE,
                backupCount=DEFAULT_LOG_BACKUP_COUNT,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)
            file_format = logging.Formatter(
                '[%(asctime)s] [%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_format)
            logger_instance.addHandler(file_handler)
        except Exception:
            pass  # 文件日志失败不影响控制台输出
    
    return logger_instance


# 全局logger实例
logger = get_logger()
