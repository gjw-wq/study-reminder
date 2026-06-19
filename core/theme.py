"""主题管理模块

集中管理深色/浅色主题配色，避免循环导入。
"""

from core.config import config


THEME_DARK = {
    'bg': '#0a0a0a',
    'bg_card': '#111111',
    'bg_module': '#0a0a0a',
    'bg_input': '#111111',
    'border': '#1f1f1f',
    'border_hover': '#333333',
    'accent': '#3ddc84',
    'accent_hover': '#4ee895',
    'accent_dim': '#2a9d5f',
    'text_primary': '#ffffff',
    'text_secondary': '#a0a0a0',
    'text_dim': '#555555',
    'text_on_accent': '#0a0a0a',
    'shadow_color': (61, 220, 132, 20),
}

THEME_LIGHT = {
    'bg': '#f5f5f5',
    'bg_card': '#ffffff',
    'bg_module': '#f8f8f8',
    'bg_input': '#ffffff',
    'border': '#e0e0e0',
    'border_hover': '#cccccc',
    'accent': '#2a9d5f',
    'accent_hover': '#3ddc84',
    'accent_dim': '#1a7a47',
    'text_primary': '#1a1a1a',
    'text_secondary': '#666666',
    'text_dim': '#aaaaaa',
    'text_on_accent': '#ffffff',
    'shadow_color': (0, 0, 0, 15),
}


def get_theme():
    """根据配置返回当前主题配色字典"""
    theme = config.get('theme', 'dark')
    return THEME_DARK if theme == 'dark' else THEME_LIGHT
