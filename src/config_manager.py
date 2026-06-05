#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块
负责配置文件的读取、写入和管理
"""

import json
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional
import threading
from jsonschema import validate, ValidationError

from logger import logger
from exceptions import ConfigLoadError, ConfigSaveError
from constants import (
    DEFAULT_WEBUI_HOST, DEFAULT_WEBUI_PORT, DEFAULT_WEBUI_DEBUG,
    DEFAULT_WECHAT_ENABLED, DEFAULT_CHECK_INTERVAL, DEFAULT_AUTO_REPLY,
    DEFAULT_WINDOW_MINIMIZE_ENABLED, DEFAULT_WINDOW_MINIMIZE_INTERVAL, DEFAULT_WINDOW_RESTORE_DELAY,
    DEFAULT_ONEBOT_ENABLED, DEFAULT_ONEBOT_WS_URL, DEFAULT_ONEBOT_ACCESS_TOKEN,
    DEFAULT_ONEBOT_RECONNECT_INTERVAL, DEFAULT_ONEBOT_HEARTBEAT_INTERVAL, DEFAULT_ONEBOT_SELF_ID,
    DEFAULT_MESSAGE_MAX_LENGTH, DEFAULT_ENABLE_IMAGE, DEFAULT_ENABLE_FILE, DEFAULT_ENABLE_VOICE,
    MAX_BACKUP_COUNT
)

class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: str = None):
        """初始化配置管理器
        
        Args:
            config_file: 配置文件路径，默认为 config/config.json
        """
        if config_file is None:
            # 获取项目根目录
            project_root = Path(__file__).parent.parent
            config_dir = project_root / "config"
            config_dir.mkdir(exist_ok=True)
            config_file = config_dir / "config.json"
            
        self.config_file = Path(config_file)
        self.config_data = {}
        self._lock = threading.Lock()
        
        # 默认配置
        self.default_config = {
            "webui": {
                "host": DEFAULT_WEBUI_HOST,
                "port": DEFAULT_WEBUI_PORT,
                "debug": DEFAULT_WEBUI_DEBUG
            },
            "wechat": {
                "enabled": DEFAULT_WECHAT_ENABLED,
                "monitor_users": [],
                "check_interval": DEFAULT_CHECK_INTERVAL,
                "auto_reply": DEFAULT_AUTO_REPLY,
                "window_minimize": {
                    "enabled": DEFAULT_WINDOW_MINIMIZE_ENABLED,
                    "interval": DEFAULT_WINDOW_MINIMIZE_INTERVAL,
                    "restore_delay": DEFAULT_WINDOW_RESTORE_DELAY
                }
            },
            "onebot": {
                "enabled": DEFAULT_ONEBOT_ENABLED,
                "ws_url": DEFAULT_ONEBOT_WS_URL,
                "access_token": DEFAULT_ONEBOT_ACCESS_TOKEN,
                "reconnect_interval": DEFAULT_ONEBOT_RECONNECT_INTERVAL,
                "heartbeat_interval": DEFAULT_ONEBOT_HEARTBEAT_INTERVAL,
                "self_id": DEFAULT_ONEBOT_SELF_ID
            },
            "message": {
                "max_length": DEFAULT_MESSAGE_MAX_LENGTH,
                "enable_image": DEFAULT_ENABLE_IMAGE,
                "enable_file": DEFAULT_ENABLE_FILE,
                "enable_voice": DEFAULT_ENABLE_VOICE,
                "image_cache_dir": "cache/images",
                "file_cache_dir": "cache/files"
            },
            "logging": {
                "level": "INFO",
                "file": "logs/app.log",
                "max_size": "10MB",
                "backup_count": 5
            }
        }
        
        # 配置校验Schema
        self.config_schema = {
            "type": "object",
            "properties": {
                "webui": {
                    "type": "object",
                    "properties": {
                        "host": {"type": "string"},
                        "port": {"type": "integer", "minimum": 1, "maximum": 65535},
                        "debug": {"type": "boolean"}
                    },
                    "required": ["host", "port"]
                },
                "wechat": {
                    "type": "object",
                    "properties": {
                        "enabled": {"type": "boolean"},
                        "monitor_users": {"type": "array"},
                        "check_interval": {"type": "number", "minimum": 0.1},
                        "auto_reply": {"type": "boolean"}
                    },
                    "required": ["enabled"]
                },
                "onebot": {
                    "type": "object",
                    "properties": {
                        "enabled": {"type": "boolean"},
                        "ws_url": {"type": "string", "format": "uri"},
                        "access_token": {"type": "string"},
                        "reconnect_interval": {"type": "integer", "minimum": 1},
                        "heartbeat_interval": {"type": "integer", "minimum": 5},
                        "self_id": {"type": "string"}
                    },
                    "required": ["enabled", "ws_url"]
                },
                "message": {
                    "type": "object",
                    "properties": {
                        "max_length": {"type": "integer", "minimum": 1},
                        "enable_image": {"type": "boolean"},
                        "enable_file": {"type": "boolean"},
                        "enable_voice": {"type": "boolean"}
                    }
                }
            },
            "required": ["webui", "wechat", "onebot", "message"]
        }
        
        # 加载配置文件
        self.load_config()
        
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件
        
        Returns:
            配置字典
            
        Raises:
            ConfigLoadError: 加载失败时抛出
        """
        with self._lock:
            try:
                if self.config_file.exists():
                    with open(self.config_file, 'r', encoding='utf-8') as f:
                        loaded_config = json.load(f)
                    
                    # 合并默认配置和加载的配置
                    self.config_data = self._merge_config(self.default_config, loaded_config)
                else:
                    # 如果配置文件不存在，使用默认配置
                    self.config_data = self.default_config.copy()
                    self.save_config()
                    
                return self.config_data.copy()
                
            except json.JSONDecodeError as e:
                logger.error(f"配置文件JSON格式错误: {e}")
                raise ConfigLoadError(f"配置文件JSON格式错误: {e}")
            except Exception as e:
                logger.error(f"加载配置文件失败: {e}")
                raise ConfigLoadError(f"加载配置文件失败: {e}")
                
    def save_config(self) -> bool:
        """保存配置到文件（自动备份旧配置）
        
        Returns:
            是否保存成功
            
        Raises:
            ConfigSaveError: 保存失败时抛出
        """
        with self._lock:
            try:
                # 确保配置目录存在
                self.config_file.parent.mkdir(parents=True, exist_ok=True)
                
                # 备份旧配置
                if self.config_file.exists():
                    backup_dir = self.config_file.parent / "backups"
                    backup_dir.mkdir(exist_ok=True)
                    
                    from datetime import datetime
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    backup_file = backup_dir / f"config_{timestamp}.json"
                    
                    shutil.copy2(self.config_file, backup_file)
                    
                    # 只保留最近N个备份
                    backups = sorted(backup_dir.glob("config_*.json"), reverse=True)
                    for old_backup in backups[MAX_BACKUP_COUNT:]:
                        old_backup.unlink()
                
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(self.config_data, f, ensure_ascii=False, indent=2)
                    
                return True
                
            except Exception as e:
                logger.error(f"保存配置文件失败: {e}")
                raise ConfigSaveError(f"保存配置文件失败: {e}")
                
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值
        
        Args:
            key: 配置键，支持点号分隔的嵌套键，如 'wechat.enabled'
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key.split('.')
        value = self.config_data
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
            
    def set(self, key: str, value: Any) -> bool:
        """设置配置值
        
        Args:
            key: 配置键，支持点号分隔的嵌套键
            value: 配置值
            
        Returns:
            是否设置成功
        """
        with self._lock:
            keys = key.split('.')
            config = self.config_data
            
            try:
                # 导航到最后一级的父级
                for k in keys[:-1]:
                    if k not in config:
                        config[k] = {}
                    config = config[k]
                    
                # 设置值
                config[keys[-1]] = value
                return True
                
            except Exception as e:
                logger.error(f"设置配置值失败: {e}")
                return False
                
    def update(self, updates: Dict[str, Any]) -> bool:
        """批量更新配置
        
        Args:
            updates: 要更新的配置字典
            
        Returns:
            是否更新成功
        """
        with self._lock:
            try:
                self.config_data = self._merge_config(self.config_data, updates)
                return True
            except Exception as e:
                logger.error(f"批量更新配置失败: {e}")
                return False
                
    def get_all(self) -> Dict[str, Any]:
        """获取所有配置
        
        Returns:
            配置字典的副本
        """
        return self.config_data.copy()
        
    def validate_config(self, config: Optional[Dict[str, Any]] = None) -> List[str]:
        """验证配置格式
        
        Args:
            config: 要验证的配置，默认使用当前配置
            
        Returns:
            错误消息列表，空列表表示验证通过
            
        Raises:
            ConfigValidationError: 验证失败时抛出
        """
        errors = []
        config_to_validate = config or self.config_data
        
        try:
            validate(instance=config_to_validate, schema=self.config_schema)
        except ValidationError as e:
            errors.append(f"配置格式错误: {e.message} (路径: {'/'.join(str(p) for p in e.absolute_path)})")
        except Exception as e:
            errors.append(f"配置验证失败: {str(e)}")
            
        return errors
        
    def reset_to_default(self) -> bool:
        """重置为默认配置
        
        Returns:
            是否重置成功
        """
        with self._lock:
            try:
                self.config_data = self.default_config.copy()
                return self.save_config()
            except Exception as e:
                logger.error(f"重置配置失败: {e}")
                return False
                
    def add_monitor_user(self, user_data) -> bool:
        """添加监听用户
        
        Args:
            user_data: 用户数据，可以是字符串（昵称）或字典（包含nickname和user_id）
            
        Returns:
            是否添加成功
        """
        monitor_users = self.get('wechat.monitor_users', [])
        
        # 检查是否已存在
        if isinstance(user_data, str):
            # 字符串格式
            if user_data not in monitor_users:
                monitor_users.append(user_data)
                return self.set('wechat.monitor_users', monitor_users)
        else:
            # 字典格式
            nickname = user_data.get('nickname')
            # 检查是否已存在相同昵称的用户
            for user in monitor_users:
                if isinstance(user, dict) and user.get('nickname') == nickname:
                    return True  # 已存在
                elif isinstance(user, str) and user == nickname:
                    return True  # 已存在
            
            monitor_users.append(user_data)
            return self.set('wechat.monitor_users', monitor_users)
        
        return True
        
    def remove_monitor_user(self, username: str) -> bool:
        """移除监听用户
        
        Args:
            username: 用户昵称
            
        Returns:
            是否移除成功
        """
        monitor_users = self.get('wechat.monitor_users', [])
        
        # 查找并移除匹配的用户
        for i, user in enumerate(monitor_users):
            if isinstance(user, str) and user == username:
                monitor_users.pop(i)
                return self.set('wechat.monitor_users', monitor_users)
            elif isinstance(user, dict) and user.get('nickname') == username:
                monitor_users.pop(i)
                return self.set('wechat.monitor_users', monitor_users)
        
        return False  # 未找到匹配的用户
        
    def get_monitor_users(self) -> List:
        """获取监听用户列表
        
        Returns:
            用户列表，可能包含字符串（昵称）或字典（包含nickname和user_id）
        """
        return self.get('wechat.monitor_users', [])
        
    def _merge_config(self, base: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
        """递归合并配置字典
        
        Args:
            base: 基础配置
            updates: 更新配置
            
        Returns:
            合并后的配置
        """
        result = base.copy()
        
        for key, value in updates.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value
                
        return result