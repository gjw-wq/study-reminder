# 打包后打卡无反应、课表点击退出 — Bug修复计划

## 一、问题诊断

通过逐行审查全部源码，定位到以下根因：

### Bug 1：打卡点击无反应
**根因**：`SubWindowBase._build_title_bar()` 的布局结构有严重缺陷。

`_build_title_bar()` 创建了一个 `outer` QWidget（作为self的子控件），但从未将 `outer` 添加到任何布局中。`outer` 是一个"孤儿"控件，永远不可见。而 `card_layout` 是 `card`（outer的子控件）的布局，后续 `HabitPanel.init_ui()` 中调用 `card_layout.addWidget(content)` 把内容添加到了 card 里，但 card 本身不可见，所以整个窗口内容为空——用户看到的是一个透明窗口，点击任何位置都无效。

**关键代码**（`course_view.py` 第25-98行）：
```python
def _build_title_bar(self):
    outer = QWidget(self)        # 创建了但没添加到self的布局
    outer_layout = QVBoxLayout(outer)
    ...
    return outer_layout, card_layout  # 返回的outer_layout无法被外部使用
```

`habit_panel.py` 第18行：
```python
outer_layout, card_layout = self._build_title_bar()
# outer_layout 从未被使用，outer控件从未被添加到self
card_layout.addWidget(content)  # 添加到了不可见的card中
```

### Bug 2：课表点击后直接退出
**根因**：与Bug 1相同。`CourseView` 也继承 `SubWindowBase`，同样存在布局结构缺陷。窗口内容完全不可见，用户点击到透明区域可能触发系统行为导致程序退出。

### Bug 3（潜在）：打包后路径问题
**根因**：`database.py` 和 `config.py` 使用 `Path(__file__).parent.parent` 定位数据目录。PyInstaller `--onefile` 打包后，`__file__` 指向临时解压目录（`_MEIPASS`），程序退出后临时目录被删除，数据库和配置文件丢失。

`main.py` 第5行：
```python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```
这在打包后指向临时目录，虽然不影响import（因为PyInstaller会处理），但 `database.py` 和 `config.py` 的数据文件路径需要指向exe所在目录而非临时目录。

## 二、修复方案

### 修复1：重写 `SubWindowBase._build_title_bar()` 布局结构
**文件**：`ui/course_view.py`（SubWindowBase类）

**方案**：不再返回两个布局，而是让 `_build_title_bar()` 直接将所有控件添加到 `self` 上。使用 `self.setLayout()` 设置主布局，确保所有子控件可见。

```python
def _build_title_bar(self):
    """创建标题栏，将内容添加到self上，返回content_layout供子类继续添加"""
    self.setStyleSheet('''
        background-color: transparent;
    ''')
    
    # 主布局
    main_layout = QVBoxLayout(self)
    main_layout.setContentsMargins(0, 0, 0, 0)
    main_layout.setSpacing(0)
    
    # 白色卡片
    card = QWidget()
    card.setObjectName('subCard')
    card.setStyleSheet('''...''')
    ...
    
    card_layout = QVBoxLayout(card)
    card_layout.setContentsMargins(0, 0, 0, 0)
    
    # 标题栏
    ...
    card_layout.addWidget(title_bar)
    
    main_layout.addWidget(card)
    
    return card_layout  # 子类用这个添加内容
```

### 修复2：修复 `HabitPanel.init_ui()` 和 `CourseView.init_ui()`
**文件**：`ui/habit_panel.py`、`ui/course_view.py`

移除 `outer_layout.parent().addWidget(outer_layout)` 这行无效代码，直接使用 `_build_title_bar()` 返回的 `card_layout` 添加内容。

### 修复3：修复打包后数据文件路径
**文件**：`core/database.py`、`core/config.py`、`main.py`

添加 `_MEIPASS` 检测，打包后数据文件存储在exe所在目录：

```python
import sys
import os

def get_app_dir():
    """获取应用数据目录（打包后为exe所在目录，开发时为项目根目录）"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))
```

`database.py` 和 `config.py` 中的 `Path(__file__).parent.parent` 替换为 `get_app_dir()`。

### 修复4：添加全局异常捕获
**文件**：`main.py`

打包后如果发生未捕获异常，程序会直接闪退。添加异常捕获，弹出错误对话框而非静默退出：

```python
import traceback
sys.excepthook = lambda *args: QMessageBox.critical(None, '错误', str(args[1]))
```

## 三、修改文件清单

| 文件 | 修改内容 |
|------|---------|
| `ui/course_view.py` | 重写 `SubWindowBase._build_title_bar()`，修复布局结构；修复 `CourseView.init_ui()` |
| `ui/habit_panel.py` | 修复 `HabitPanel.init_ui()` 中的布局调用 |
| `core/database.py` | 修复数据文件路径，支持打包后exe目录 |
| `core/config.py` | 修复配置文件路径，支持打包后exe目录 |
| `main.py` | 添加全局异常捕获，修复sys.path设置 |

## 四、验证步骤

1. 先用 `python main.py` 直接运行，验证打卡和课表窗口正常显示且可交互
2. 用虚拟环境PyInstaller打包：`.\venv\Scripts\pyinstaller.exe --onefile --windowed --name "学习纪律官" --clean --noconfirm --hidden-import PyQt6 --collect-all PyQt6 --collect-all PyQt6-Qt6 main.py`
3. 运行打包后的exe，验证打卡和课表功能正常
4. 验证数据库文件创建在exe同级目录
5. 验证配置文件创建在exe同级目录
