import sys
import os
import traceback

# 添加项目根目录到路径（开发环境需要，打包后PyInstaller自动处理）
_project_root = os.path.dirname(os.path.abspath(__file__))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from core.database import db
from core.course_data import init_course_data
from core.config import config
from ui.main_panel import MainPanel


def global_exception_hook(exc_type, exc_value, exc_tb):
    """全局异常捕获，防止打包后静默闪退"""
    error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print(f"ERROR:\n{error_msg}", file=sys.stderr)
    try:
        app = QApplication.instance()
        if app:
            QMessageBox.critical(None, '程序错误', f'发生未预期的错误:\n\n{exc_value}')
    except:
        pass


def main():
    # 设置全局异常捕获
    sys.excepthook = global_exception_hook

    # 启用高DPI支持
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setFont(QFont('Microsoft YaHei', 10))

    # 同步开机自启注册表状态（处理配置与注册表不一致的情况）
    try:
        from core.auto_start import is_auto_start_enabled, set_auto_start
        if config.get('auto_start', False) != is_auto_start_enabled():
            set_auto_start(config.get('auto_start', False))
    except Exception:
        pass  # 非Windows环境或权限不足时忽略

    # 初始化数据库和课程数据（幂等：已有数据不会重复导入）
    init_course_data(db)

    # 创建主面板
    panel = MainPanel()
    panel.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
