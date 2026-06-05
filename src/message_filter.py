"""
消息过滤模块
负责判断消息是否为系统消息或调试消息
"""

import re
from logger import logger
from constants import SYSTEM_MESSAGE_KEYWORDS, WXAUTO_DEBUG_KEYWORDS


class MessageFilter:
    """消息过滤器"""
    
    # 系统消息正则模式（精简版）
    SYSTEM_PATTERNS = [
        re.compile(r'^\s*\[.*(?:系统|提示|通知|记录|历史|消息).*\]\s*$', re.IGNORECASE),
        re.compile(r'^\s*\.{3,}\s*$'),  # 纯省略号
        re.compile(r'^\s*…+\s*$'),  # 纯中文省略号
        re.compile(r'^\s*[-=*_]{3,}\s*$'),  # 纯分隔符
    ]
    
    # 短消息系统模式
    SHORT_SYSTEM_PATTERNS = [
        re.compile(r'.*新消息.*', re.IGNORECASE),
        re.compile(r'.*历史.*消息.*', re.IGNORECASE),
        re.compile(r'.*以下.*消息.*', re.IGNORECASE),
        re.compile(r'.*以上.*消息.*', re.IGNORECASE),
    ]
    
    @classmethod
    def is_system_message(cls, content: str) -> bool:
        """判断是否为系统消息
        
        Args:
            content: 消息内容
            
        Returns:
            是否为系统消息
        """
        if not content or not content.strip():
            return True
            
        content_clean = content.strip()
        content_lower = content_clean.lower()
        
        # 检查关键词
        for keyword in SYSTEM_MESSAGE_KEYWORDS:
            if keyword.lower() in content_lower:
                logger.debug(f"匹配到系统消息关键词: '{keyword}'")
                return True
        
        # 检查正则模式
        for pattern in cls.SYSTEM_PATTERNS:
            if pattern.search(content_clean):
                logger.debug(f"匹配到系统消息模式: '{pattern.pattern}'")
                return True
        
        # 短消息（<20字符）额外检查
        if len(content_clean) < 20:
            for pattern in cls.SHORT_SYSTEM_PATTERNS:
                if pattern.search(content_lower):
                    logger.debug("匹配到短系统消息")
                    return True
        
        return False
    
    @classmethod
    def is_wxauto_debug_message(cls, content: str) -> bool:
        """判断是否为wxauto调试消息
        
        Args:
            content: 消息内容
            
        Returns:
            是否为wxauto调试消息
        """
        if not content:
            return False
            
        content_lower = content.lower()
        
        for keyword in WXAUTO_DEBUG_KEYWORDS:
            if keyword in content_lower:
                return True
                
        return False
