"""
微信消息监听模块
使用wxauto库监听微信消息
"""

import time
import threading
from typing import List, Dict, Any, Optional, Callable

from logger import logger
from message_parser import MessageParser
from message_filter import MessageFilter

try:
    import pythoncom
    from wxauto import WeChat
except ImportError:
    logger.warning("wxauto库未安装，请运行 pip install wxauto")
    WeChat = None
    pythoncom = None


class WeChatMonitor:
    """微信消息监听器"""
    
    def __init__(self, config_manager: Any) -> None:
        """初始化微信监听器
        
        Args:
            config_manager: 配置管理器
        """
        self.config_manager = config_manager
        self.wechat: Optional[WeChat] = None
        self.running: bool = False
        self.monitor_thread: Optional[threading.Thread] = None
        
        # 消息回调函数
        self.message_callback: Optional[Callable[[Dict[str, Any]], None]] = None
        
        # 消息解析器
        self.parser = MessageParser(config_manager)
        
        # 消息去重缓存
        self.sent_message_cache: Dict[str, float] = {}
        self.cache_expire_time: int = 30  # 秒
        
    def set_message_callback(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """设置消息回调函数
        
        Args:
            callback: 消息回调函数
        """
        self.message_callback = callback
        
    def start(self) -> bool:
        """启动微信监听
        
        Returns:
            是否启动成功
        """
        if self.running:
            logger.info("微信监听器已在运行中")
            return True
            
        if WeChat is None:
            logger.error("wxauto库未安装，无法启动微信监听")
            return False
            
        try:
            # 初始化COM组件
            if pythoncom:
                pythoncom.CoInitialize()
            
            # 初始化微信客户端
            self.wechat = WeChat()
            
            # 检查微信是否已登录
            if not self._check_wechat_login():
                logger.error("微信未登录或无法连接")
                self.running = False
                return False
                
            self.running = True
            
            # 启动监听线程
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            
            logger.info("微信监听器启动成功")
            return True
            
        except Exception as e:
            logger.error(f"启动微信监听器失败: {e}")
            self.running = False
            return False
            
    def stop(self) -> bool:
        """停止微信监听
        
        Returns:
            是否停止成功
        """
        if not self.running:
            logger.info("微信监听器未在运行")
            return True
            
        self.running = False
        
        # 等待监听线程结束
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5)
            
        # 清理COM组件
        if pythoncom:
            try:
                pythoncom.CoUninitialize()
            except Exception:
                pass
            
        self.wechat = None
        logger.info("微信监听器已停止")
        return True
        
    def is_running(self) -> bool:
        """检查是否正在运行
        
        Returns:
            是否正在运行
        """
        return self.running
        
    def _check_wechat_login(self) -> bool:
        """检查微信是否已登录
        
        Returns:
            是否已登录
        """
        try:
            if self.wechat is not None:
                logger.info("微信客户端连接成功")
                return True
            return False
        except Exception as e:
            logger.error(f"检查微信登录状态失败: {e}")
            return False
            
    def _on_message_callback(self, msg: Any, chat: Any) -> None:
        """消息回调函数
        
        Args:
            msg: 消息对象
            chat: 聊天对象
        """
        try:
            # 获取用户名
            username = self.parser.get_chat_username(chat)
            
            # 跳过系统消息类型
            if hasattr(msg, 'type') and msg.type == 'sys':
                return
            
            # 获取消息内容
            content = msg.content if hasattr(msg, 'content') else str(msg)
            
            # 过滤wxauto调试消息
            if MessageFilter.is_wxauto_debug_message(content):
                logger.debug(f"过滤wxauto调试消息: {content[:30]}...")
                return
                
            logger.info(f"收到来自 {username} 的消息: {content[:50]}...")
            
            # 处理消息
            self._process_message(username, msg)
            
        except Exception as e:
            logger.error(f"处理回调消息时出错: {e}")
    
    def _monitor_loop(self) -> None:
        """监听循环"""
        try:
            # 在监听线程中初始化COM组件
            if pythoncom:
                pythoncom.CoInitialize()
                
            logger.info("开始监听微信消息...")
            
            # 添加监听用户
            self._setup_listeners()
            
            # 保持程序运行
            while self.running:
                time.sleep(1)
                    
        except Exception as e:
            logger.error(f"监听循环异常退出: {e}")
        finally:
            # 清理COM组件
            if pythoncom:
                try:
                    pythoncom.CoUninitialize()
                except Exception:
                    pass
                
    def _setup_listeners(self) -> None:
        """设置监听用户"""
        try:
            monitor_users = self.config_manager.get('wechat.monitor_users', [])
            
            if not monitor_users:
                logger.warning("未配置监听用户")
                return
                
            for user in monitor_users:
                try:
                    # 支持两种格式
                    if isinstance(user, str):
                        nickname = user
                    elif isinstance(user, dict):
                        nickname = user.get('nickname', '')
                    else:
                        continue
                        
                    if nickname:
                        self.wechat.AddListenChat(nickname=nickname, callback=self._on_message_callback)
                        logger.info(f"已添加监听用户: {nickname}")
                except Exception as e:
                    logger.error(f"添加监听用户失败: {e}")
                    
        except Exception as e:
            logger.error(f"设置监听用户失败: {e}")
            
    def _get_user_id_by_nickname(self, nickname: str) -> str:
        """根据昵称获取用户ID
        
        Args:
            nickname: 用户昵称
            
        Returns:
            用户ID
        """
        monitor_users = self.config_manager.get('wechat.monitor_users', [])
        
        for user in monitor_users:
            if isinstance(user, dict) and user.get('nickname') == nickname:
                return user.get('user_id', '')
                
        return ''
            
    def _process_message(self, username: str, message: Any) -> None:
        """处理消息
        
        Args:
            username: 用户名
            message: 消息对象
        """
        try:
            # 检查是否是监听的用户
            monitored_users = self.config_manager.get('wechat.monitor_users', [])
            
            is_monitored = False
            for user in monitored_users:
                if isinstance(user, str) and user == username:
                    is_monitored = True
                    break
                elif isinstance(user, dict) and user.get('nickname') == username:
                    is_monitored = True
                    break
            
            if not is_monitored:
                return
                
            # 获取用户ID
            user_id = self._get_user_id_by_nickname(username)
            
            # 解析消息
            parsed_msg = self.parser.parse_message(message, username, user_id)
            
            if parsed_msg and self.message_callback:
                self.message_callback(parsed_msg)
                
        except Exception as e:
            logger.error(f"处理消息失败: {e}")
            
    def _is_recently_sent_message(self, content: str) -> bool:
        """检查是否是最近发送的消息（防止回显）
        
        Args:
            content: 消息内容
            
        Returns:
            是否是最近发送的消息
        """
        current_time = time.time()
        
        # 清理过期缓存
        expired_keys = [k for k, v in self.sent_message_cache.items() 
                       if current_time - v > self.cache_expire_time]
        for key in expired_keys:
            del self.sent_message_cache[key]
        
        return content in self.sent_message_cache
        
    def _record_sent_message(self, content: str) -> None:
        """记录已发送的消息
        
        Args:
            content: 消息内容
        """
        self.sent_message_cache[content] = time.time()
        
    def send_message(self, username: str, content: str, msg_type: str = 'text') -> bool:
        """发送消息给指定用户
        
        Args:
            username: 用户昵称
            content: 消息内容
            msg_type: 消息类型
            
        Returns:
            是否发送成功
        """
        try:
            if not self.wechat or not self.running:
                logger.warning("微信监听器未运行")
                return False
                
            # 记录发送的消息
            if msg_type == 'text':
                self._record_sent_message(content)
                self.wechat.SendMsg(content, who=username)
            elif msg_type == 'image':
                self._record_sent_message('[图片]')
                self.wechat.SendFiles(content, who=username)
            elif msg_type == 'file':
                self._record_sent_message('[文件]')
                self.wechat.SendFiles(content, who=username)
            elif msg_type == 'voice':
                self._record_sent_message('[语音]')
                self.wechat.SendFiles(content, who=username)
            else:
                self._record_sent_message(content)
                self.wechat.SendMsg(content, who=username)
                
            logger.info(f"发送至 {username}: {content[:30]}...")
            return True
            
        except Exception as e:
            logger.error(f"发送消息失败: {e}")
            return False
            
    def send_image(self, username: str, image_path: str) -> bool:
        """发送图片
        
        Args:
            username: 用户昵称
            image_path: 图片路径
            
        Returns:
            是否发送成功
        """
        return self.send_message(username, image_path, 'image')
        
    def send_file(self, username: str, file_path: str) -> bool:
        """发送文件
        
        Args:
            username: 用户昵称
            file_path: 文件路径
            
        Returns:
            是否发送成功
        """
        return self.send_message(username, file_path, 'file')
        
    def get_user_list(self) -> List[str]:
        """获取用户列表
        
        Returns:
            用户列表
        """
        try:
            if not self.wechat:
                return []
            return self.wechat.GetAllMessage()
        except Exception as e:
            logger.error(f"获取用户列表失败: {e}")
            return []
