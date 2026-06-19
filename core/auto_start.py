"""Windows 开机自启管理模块

通过操作注册表 HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run
实现开机自动启动，无需管理员权限。
"""

import os
import sys
import winreg


def get_exe_path():
    """获取当前程序的可执行文件路径

    打包后（PyInstaller）返回 .exe 路径
    开发模式返回 main.py 脚本路径
    """
    if getattr(sys, 'frozen', False):
        return sys.executable
    return os.path.abspath(sys.argv[0])


def set_auto_start(enable: bool) -> bool:
    """设置或取消开机自启

    Args:
        enable: True 开启开机自启，False 取消

    Returns:
        操作是否成功
    """
    app_name = 'StudyReminder'
    reg_path = r'Software\Microsoft\Windows\CurrentVersion\Run'

    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, reg_path, 0,
            winreg.KEY_SET_VALUE
        )
        if enable:
            exe_path = get_exe_path()
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, exe_path)
        else:
            try:
                winreg.DeleteValue(key, app_name)
            except FileNotFoundError:
                pass  # 本来就不存在，无需报错
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f'设置开机自启失败: {e}')
        return False


def is_auto_start_enabled() -> bool:
    """检查当前是否已设置开机自启

    Returns:
        True 已设置且路径匹配，False 未设置或路径不匹配
    """
    app_name = 'StudyReminder'
    reg_path = r'Software\Microsoft\Windows\CurrentVersion\Run'

    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, reg_path, 0,
            winreg.KEY_READ
        )
        value, _ = winreg.QueryValueEx(key, app_name)
        winreg.CloseKey(key)
        # 额外检查路径是否匹配（防止用户移动了程序位置）
        return value == get_exe_path()
    except FileNotFoundError:
        return False
    except Exception:
        return False
