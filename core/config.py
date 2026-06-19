import json
import os
import sys
from pathlib import Path


def get_app_dir():
    """获取应用数据目录（打包后为exe所在目录，开发时为项目根目录）"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DEFAULT_CONFIG = {
    'reminder_advance_minutes': 15,
    'reminder_sound': True,
    'reminder_popup': True,
    'reminder_tray_flash': True,
    'theme': 'dark',
    'auto_start': False,
    'peer_board_enabled': False,
    'check_in_time': '08:30',
    'evening_study_start': '19:00',
    'evening_study_end': '21:30',
    'wake_up_time': '07:00',
    'habits': [
        {'index': 0, 'name': '拒绝睡懒觉', 'icon': 'bed'},
        {'index': 1, 'name': '拒绝为了女朋友请假', 'icon': 'heart'},
        {'index': 2, 'name': '拒绝晚自习下课即跑', 'icon': 'run'},
        {'index': 3, 'name': '拒绝不交作业', 'icon': 'book'},
        {'index': 4, 'name': '拒绝打游戏、看游戏', 'icon': 'game'},
        {'index': 5, 'name': '拒绝离不开手机', 'icon': 'phone'}
    ],
    'window_position': {'x': 100, 'y': 100},
    'window_collapsed': False
}

class Config:
    def __init__(self):
        self.config_path = os.path.join(get_app_dir(), 'data', 'config.json')
        self.config = self.load()
    
    def load(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return DEFAULT_CONFIG.copy()
        return DEFAULT_CONFIG.copy()
    
    def save(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def get(self, key, default=None):
        return self.config.get(key, default)
    
    def set(self, key, value):
        self.config[key] = value
        self.save()
    
    def get_habits(self):
        return self.config.get('habits', DEFAULT_CONFIG['habits'])

# 全局配置实例
config = Config()
