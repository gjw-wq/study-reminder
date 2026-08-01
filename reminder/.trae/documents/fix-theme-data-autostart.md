# 修复计划：主题切换、数据持久化与开机自启

## 摘要

修复三个独立但相互关联的问题：
1. 设置对话框的 UI 配色在深色/浅色主题切换时未随之改变（硬编码颜色值）
2. 打包后 exe 每次启动都会重置数据库中的课程数据（无条件 `DELETE FROM courses`）
3. 开机启动设置仅保存配置到 JSON，未实际写入 Windows 注册表

## 当前状态分析

### 问题 1：设置对话框硬编码配色

`ui/settings_dialog.py` 第 10-15 行定义了独立的 `TECH_STYLE` 字典，全部使用深色主题配色。`init_ui()` 中所有 `setStyleSheet` 都直接引用 `TECH_STYLE`，完全没有读取 `config.get('theme')`。`MainPanel.apply_theme()` 仅更新主面板自身控件，不会将主题应用到已打开的 `SettingsDialog`。

### 问题 2：数据库课程数据被无条件重置

`main.py` 第 43-48 行每次启动都执行 `DELETE FROM courses`，随后调用 `core/course_data.py` 的 `init_course_data()` 重新插入静态数据。即使用户通过 SQL 或其他方式修改了课程数据，下次启动也会被清空。`core/database.py` 的 `insert_course()` 使用 `INSERT OR REPLACE`，但由于 `courses` 表没有 `UNIQUE` 约束，该语句退化为普通 `INSERT`。

### 问题 3：开机自启未实现

`ui/settings_dialog.py` 的 `save_settings()` 仅将 `auto_start` 布尔值写入 `config.json`，完全没有调用 Windows 注册表 API 或创建启动文件夹快捷方式。整个项目代码中不存在 `winreg`、`HKCU`、`Startup` 等相关逻辑。

## 拟议修改

### 文件 1：`ui/settings_dialog.py`

**修改内容**：移除 `TECH_STYLE` 硬编码字典，改为从 `ui.main_panel` 导入 `get_theme()` 函数。在 `init_ui()` 开头调用 `S = get_theme()`，所有样式引用 `S` 字典。

**原因**：消除硬编码，使设置对话框随系统主题动态变化。

**实现方式**：
- 删除第 10-16 行的 `TECH_STYLE` 定义
- 添加 `from ui.main_panel import get_theme`
- `init_ui()` 开头 `S = get_theme()`
- 所有 `TECH_STYLE['xxx']` 替换为 `S['xxx']`
- 确保 `QComboBox::drop-down` 和 `QComboBox QAbstractItemView` 也使用 `S`

### 文件 2：`main.py`

**修改内容**：删除启动时无条件清空 `courses` 表的逻辑（第 43-48 行）。添加开机自启状态同步代码。

**原因**：避免用户数据被重置；确保注册表状态与配置一致。

**实现方式**：
- 删除 `DELETE FROM courses` 代码块
- 在 `main()` 中添加：
  ```python
  from core.auto_start import is_auto_start_enabled, set_auto_start
  if config.get('auto_start', False) != is_auto_start_enabled():
      set_auto_start(config.get('auto_start', False))
  ```

### 文件 3：`core/database.py`

**修改内容**：在 `init_tables()` 中新增 `app_meta` 表创建逻辑。

**原因**：为课程数据版本控制提供存储机制。

**实现方式**：
```python
cursor.execute('''
    CREATE TABLE IF NOT EXISTS app_meta (
        key TEXT PRIMARY KEY,
        value TEXT
    )
''')
```

### 文件 4：`core/course_data.py`

**修改内容**：修改 `init_course_data()` 为带版本检查的幂等初始化。

**原因**：仅在首次启动或课程表版本更新时才重新导入数据，保留用户修改。

**实现方式**：
```python
def init_course_data(db):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM app_meta WHERE key = 'course_data_version'")
    row = cursor.fetchone()
    current_version = '2026-06-v1'
    if row and row[0] == current_version:
        conn.close()
        return
    cursor.execute('DELETE FROM courses')
    for course in COURSE_SCHEDULE:
        db.insert_course(**course)
    cursor.execute('INSERT OR REPLACE INTO app_meta (key, value) VALUES (?, ?)',
                   ('course_data_version', current_version))
    conn.commit()
    conn.close()
```

### 文件 5：`core/auto_start.py`（新建）

**修改内容**：创建 Windows 注册表开机自启管理模块。

**原因**：实现实际的开机自启功能。

**实现方式**：
```python
import os, sys, winreg

def get_exe_path():
    if getattr(sys, 'frozen', False):
        return sys.executable
    return sys.argv[0]

def set_auto_start(enable: bool) -> bool:
    app_name = 'StudyReminder'
    reg_path = r'Software\Microsoft\Windows\CurrentVersion\Run'
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE)
        if enable:
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, get_exe_path())
        else:
            try: winreg.DeleteValue(key, app_name)
            except FileNotFoundError: pass
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f"设置开机自启失败: {e}")
        return False

def is_auto_start_enabled() -> bool:
    app_name = 'StudyReminder'
    reg_path = r'Software\Microsoft\Windows\CurrentVersion\Run'
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(key, app_name)
        winreg.CloseKey(key)
        return value == get_exe_path()
    except FileNotFoundError:
        return False
    except Exception:
        return False
```

### 文件 6：`ui/settings_dialog.py`（再次修改）

**修改内容**：在 `save_settings()` 中调用 `set_auto_start()` 实际写入注册表。

**原因**：将配置变更同步到操作系统层面。

**实现方式**：
```python
from core.auto_start import set_auto_start

def save_settings(self):
    # ... 保存其他配置 ...
    auto_start = self.autostart_check.isChecked()
    config.set('auto_start', auto_start)
    if not set_auto_start(auto_start):
        QMessageBox.warning(self, '设置失败', '开机自启设置失败')
        return
    QMessageBox.information(self, '保存成功', '设置已保存')
    self.accept()
```

## 假设与决策

- 使用 `winreg` 标准库操作 `HKEY_CURRENT_USER` 注册表，无需管理员权限
- 课程数据版本号硬编码为 `'2026-06-v1'`，后续课程表更新时手动递增版本号即可触发重新导入
- 打包后 `sys.executable` 指向 `.exe` 文件本身，注册表路径正确
- 开发模式下（非打包）`sys.argv[0]` 指向 `main.py`，设置开机自启会注册 Python 脚本路径，这是可接受的行为

## 验证步骤

1. 启动程序，打开设置对话框，切换主题为浅色，确认设置对话框背景变为浅色、文字变为深色
2. 关闭程序，用 SQLite 工具修改 `courses` 表中的某条课程数据
3. 重新启动程序，确认修改后的课程数据仍然保留
4. 在设置中勾选"开机自动启动"，保存后检查注册表 `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` 是否存在 `StudyReminder` 项
5. 取消勾选"开机自动启动"，确认注册表项被删除
