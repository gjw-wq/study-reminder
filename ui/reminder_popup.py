from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint
from PyQt6.QtGui import QFont, QColor

TECH_STYLE = {
    'bg': '#0a0a0a', 'bg_card': '#111111', 'bg_module': '#0a0a0a', 'bg_input': '#111111',
    'border': '#1f1f1f', 'accent': '#3ddc84', 'accent_dim': '#2a9d5f',
    'text_primary': '#ffffff', 'text_secondary': '#a0a0a0', 'text_dim': '#555555',
    'text_on_accent': '#0a0a0a',
}

class ReminderPopup(QWidget):
    def __init__(self, reminder_data, parent=None):
        super().__init__(parent)
        self.reminder_data = reminder_data
        self.init_ui()
        self.show_animation()

        # 自动关闭计时器
        self.close_timer = QTimer(self)
        self.close_timer.timeout.connect(self.hide_animation)
        self.close_timer.start(10000)  # 10秒后自动关闭

    def init_ui(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setFixedSize(360, 160)

        # 定位到屏幕右下角
        screen = self.screen().geometry()
        self.move(screen.width() - 380, screen.height() - 180)

        # 主容器
        container = QWidget(self)
        container.setObjectName('popupContainer')

        # 统一使用绿色强调色
        accent_color = TECH_STYLE['accent']

        container.setStyleSheet(f'''
            #popupContainer {{
                background-color: {TECH_STYLE['bg_card']};
                border-radius: 10px;
                border: 1px solid {TECH_STYLE['border']};
                border-left: 4px solid {accent_color};
            }}
        ''')

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(61, 220, 132, 40))
        shadow.setOffset(0, 4)
        container.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(container)

        inner = QVBoxLayout(container)
        inner.setContentsMargins(16, 16, 16, 16)
        inner.setSpacing(8)

        # 标题行
        header = QHBoxLayout()
        type_label = QLabel(self._get_type_label())
        type_label.setFont(QFont('Microsoft YaHei', 9))
        type_label.setStyleSheet(f'color: {accent_color};')
        header.addWidget(type_label)
        header.addStretch()

        time_label = QLabel(self.reminder_data.get('time', ''))
        time_label.setFont(QFont('Microsoft YaHei', 9))
        time_label.setStyleSheet(f'color: {TECH_STYLE["text_secondary"]};')
        header.addWidget(time_label)
        inner.addLayout(header)

        # 标题
        title = QLabel(self.reminder_data.get('title', ''))
        title.setFont(QFont('Microsoft YaHei', 13, QFont.Weight.Bold))
        title.setStyleSheet(f'color: {TECH_STYLE["text_primary"]};')
        inner.addWidget(title)

        # 描述
        desc = QLabel(self.reminder_data.get('description', ''))
        desc.setFont(QFont('Microsoft YaHei', 10))
        desc.setStyleSheet(f'color: {TECH_STYLE["text_secondary"]};')
        desc.setWordWrap(True)
        inner.addWidget(desc)

        # 按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        delay_btn = QPushButton('延迟5分钟')
        delay_btn.setStyleSheet(f'''
            QPushButton {{
                background-color: {TECH_STYLE['bg']};
                color: {TECH_STYLE['text_secondary']};
                font-size: 11px;
                padding: 6px 12px;
                border: 1px solid {TECH_STYLE['border']};
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: {TECH_STYLE['accent']};
                color: {TECH_STYLE['text_on_accent']};
                border-color: {TECH_STYLE['accent']};
            }}
        ''')
        delay_btn.clicked.connect(self.delay_reminder)
        btn_layout.addWidget(delay_btn)

        ok_btn = QPushButton('我知道了')
        ok_btn.setStyleSheet(f'''
            QPushButton {{
                background-color: {TECH_STYLE['accent']};
                color: {TECH_STYLE['text_on_accent']};
                font-size: 11px;
                padding: 6px 16px;
                border: none;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: {TECH_STYLE['accent_dim']};
            }}
        ''')
        ok_btn.clicked.connect(self.hide_animation)
        btn_layout.addWidget(ok_btn)

        inner.addLayout(btn_layout)

    def _get_type_label(self):
        type_map = {
            'course': '课程提醒',
            'routine': '作息提醒',
            'course_start': '课程开始',
            'evening_start': '晚自习',
            'evening_end': '晚自习结束',
            'review': '每日复盘'
        }
        return type_map.get(self.reminder_data.get('type', ''), '提醒')

    def show_animation(self):
        self.show()
        self.anim = QPropertyAnimation(self, b'windowOpacity')
        self.anim.setDuration(300)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.anim.start()

    def hide_animation(self):
        self.anim = QPropertyAnimation(self, b'windowOpacity')
        self.anim.setDuration(300)
        self.anim.setStartValue(1)
        self.anim.setEndValue(0)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.anim.finished.connect(self.close)
        self.anim.start()

    def delay_reminder(self):
        # 延迟5分钟再提醒
        self.close_timer.stop()
        QTimer.singleShot(300000, lambda: self.parent().reminder_engine.reminder_triggered.emit(self.reminder_data))
        self.hide_animation()

    def enterEvent(self, event):
        # 鼠标进入时暂停自动关闭
        self.close_timer.stop()

    def leaveEvent(self, event):
        # 鼠标离开时恢复自动关闭
        self.close_timer.start(5000)
