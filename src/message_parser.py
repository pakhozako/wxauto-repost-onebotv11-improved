"""
消息解析模块
负责将wxauto消息对象解析为标准格式
"""

import time
from typing import Dict, Any, Optional
from logger import logger
from message_filter import MessageFilter
from file_handler import FileHandler


class MessageParser:
    """消息解析器"""
    
    def __init__(self, config_manager: Any) -> None:
        """初始化消息解析器
        
        Args:
            config_manager: 配置管理器
        """
        self.config_manager = config_manager
        self.file_handler = FileHandler(config_manager)
    
    def parse_message(self, message: Any, username: str, user_id: str) -> Optional[Dict[str, Any]]:
        """解析消息对象
        
        Args:
            message: wxauto消息对象
            username: 用户昵称
            user_id: 用户ID
            
        Returns:
            解析后的消息字典，如果消息应被过滤则返回None
        """
        try:
            # 获取消息类型
            msg_type = getattr(message, 'type', 'text')
            
            # 获取消息内容
            content = message.content if hasattr(message, 'content') else str(message)
            
            # 过滤系统消息
            if msg_type == 'text' or not hasattr(message, 'type'):
                if MessageFilter.is_system_message(content):
                    logger.debug(f"过滤系统消息: {content[:30]}...")
                    return None
            
            # 构造基础消息结构
            parsed = {
                'user_name': username,
                'user_id': user_id,
                'timestamp': int(time.time()),
                'raw_message': str(message)
            }
            
            # 根据消息类型解析
            if msg_type == 'text' or not hasattr(message, 'type'):
                parsed.update({
                    'message_type': 'text',
                    'content': content
                })
                
            elif msg_type == 'image':
                image_path = self.file_handler.save_image(message)
                parsed.update({
                    'message_type': 'image',
                    'content': '[图片]',
                    'image_path': image_path,
                    'image_url': f'file://{image_path}' if image_path else None
                })
                
            elif msg_type == 'file':
                file_path = self.file_handler.save_file(message)
                parsed.update({
                    'message_type': 'file',
                    'content': '[文件]',
                    'file_path': file_path,
                    'file_name': getattr(message, 'filename', 'unknown_file')
                })
                
            elif msg_type == 'voice':
                if self.config_manager.get('message.enable_voice', False):
                    voice_path = self.file_handler.save_voice(message)
                    parsed.update({
                        'message_type': 'voice',
                        'content': '[语音]',
                        'voice_path': voice_path
                    })
                else:
                    parsed.update({
                        'message_type': 'text',
                        'content': '[语音消息]'
                    })
                    
            else:
                parsed.update({
                    'message_type': 'text',
                    'content': f'[{msg_type}消息]'
                })
                
            return parsed
            
        except Exception as e:
            logger.error(f"解析消息失败: {e}")
            return None
    
    def get_chat_username(self, chat: Any) -> str:
        """获取聊天对象的用户名
        
        Args:
            chat: 聊天对象
            
        Returns:
            用户名
        """
        if hasattr(chat, 'nickname'):
            return chat.nickname
        elif hasattr(chat, 'name'):
            return chat.name
        else:
            # 从字符串表示中提取
            chat_str = str(chat)
            if '("' in chat_str and '")' in chat_str:
                return chat_str.split('("')[1].split('")')[0]
            return chat_str
