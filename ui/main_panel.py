from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSystemTrayIcon, QMenu, QGraphicsDropShadowEffect, QApplication,
    QProgressBar
)
from PyQt6.QtCore import Qt, QTimer, QPoint, QSize, QRect
from PyQt6.QtGui import QFont, QColor, QIcon, QAction, QShortcut, QKeySequence, QPainter, QPixmap, QBrush, QPen
from datetime import datetime, timedelta

from core.database import db
from core.config import config
from core.reminder_engine import ReminderEngine
from .habit_panel import HabitPanel
from .course_view import CourseView
from .review_dialog import ReviewDialog
from .settings_dialog import SettingsDialog
from .reminder_popup import ReminderPopup


from core.theme import get_theme


def _create_tray_icon():
    """程序化生成托盘图标（绿色圆形 + 白色 A 字母）"""
    pixmap = QPixmap(64, 64)
    pixmap.fill(QColor(0, 0, 0, 0))
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(QBrush(QColor(61, 220, 132)))
    painter.setPen(QPen(QColor(61, 220, 132)))
    painter.drawEllipse(4, 4, 56, 56)
    painter.setPen(QPen(QColor(255, 255, 255)))
    font = QFont('Arial', 36, QFont.Weight.Bold)
    painter.setFont(font)
    painter.drawText(QRect(4, 4, 56, 56), Qt.AlignmentFlag.AlignCenter, 'A')
    painter.end()
    return QIcon(pixmap)


class MainPanel(QWidget):
    """主面板 - TRAE 纯黑极简风格"""

    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        self.setFixedSize(340, 480)

        self.drag_position = QPoint()

        self.init_ui()
        self.init_tray()
        self.init_shortcuts()
        self.init_reminders()
        self.apply_theme()

        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.update_all)
        self.refresh_timer.start(1000)
        self.update_all()

    # ========== UI 构建 ==========

    def init_ui(self):
        S = get_theme()

        # 主容器
        self.card = QWidget(self)
        self.card.setObjectName('mainCard')
        self.card.setStyleSheet(f'''
            #mainCard {{
                background-color: {S['bg_card']};
                border-radius: 16px;
                border: 1px solid {S['border']};
            }}
        ''')

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        r, g, b, a = S['shadow_color']
        shadow.setColor(QColor(r, g, b, a))
        shadow.setOffset(0, 6)
        self.card.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.card)

        inner = QVBoxLayout(self.card)
        inner.setContentsMargins(18, 16, 18, 16)
        inner.setSpacing(10)

        # --- 标题栏 ---
        header = QHBoxLayout()
        header.setSpacing(10)

        # 绿色状态点
        status = QLabel()
        status.setFixedSize(8, 8)
        status.setStyleSheet(f'''
            QLabel {{
                background-color: {S['accent']};
                border-radius: 4px;
            }}
        ''')
        header.addWidget(status)

        self.title_label = QLabel('学习纪律官')
        self.title_label.setFont(QFont('Microsoft YaHei', 14, QFont.Weight.Bold))
        self.title_label.setStyleSheet(f'color: {S["text_primary"]};')
        header.addWidget(self.title_label)

        header.addStretch()

        # 最小化
        min_btn = QPushButton('−')
        min_btn.setFixedSize(24, 24)
        min_btn.setFont(QFont('Microsoft YaHei', 11))
        min_btn.setStyleSheet(f'''
            QPushButton {{
                background-color: transparent;
                color: {S['text_dim']};
                border: none;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {S['border']};
                color: {S['text_secondary']};
            }}
        ''')
        min_btn.clicked.connect(self.minimize_to_tray)
        header.addWidget(min_btn)

        # 关闭
        close_btn = QPushButton('×')
        close_btn.setFixedSize(24, 24)
        close_btn.setFont(QFont('Microsoft YaHei', 11))
        close_btn.setStyleSheet(f'''
            QPushButton {{
                background-color: transparent;
                color: {S['text_dim']};
                border: none;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {S['accent_dim']};
                color: {S['text_primary']};
            }}
        ''')
        close_btn.clicked.connect(self.quit_app)
        header.addWidget(close_btn)

        inner.addLayout(header)

        # --- 日期 ---
        self.date_label = QLabel()
        self.date_label.setFont(QFont('Consolas', 9))
        self.date_label.setStyleSheet(f'color: {S["text_dim"]};')
        inner.addWidget(self.date_label)

        # --- 今日课程 ---
        course_box = QWidget()
        course_box.setObjectName('moduleBox')
        course_box.setStyleSheet(f'''
            #moduleBox {{
                background-color: {S['bg_module']};
                border-radius: 10px;
                border: 1px solid {S['border']};
            }}
        ''')
        cl = QVBoxLayout(course_box)
        cl.setContentsMargins(12, 10, 12, 10)
        cl.setSpacing(6)

        ch = QHBoxLayout()
        ch.addWidget(self._create_section_label('今日课程'))
        ch.addStretch()
        cl.addLayout(ch)

        self.course_list_label = QLabel()
        self.course_list_label.setFont(QFont('Microsoft YaHei', 10))
        self.course_list_label.setStyleSheet(f'color: {S["text_secondary"]};')
        self.course_list_label.setWordWrap(True)
        cl.addWidget(self.course_list_label)

        inner.addWidget(course_box)

        # --- 倒计时 ---
        cd_box = QWidget()
        cd_box.setObjectName('countdownBox')
        cd_box.setStyleSheet(f'''
            #countdownBox {{
                background-color: {S['bg_module']};
                border-radius: 10px;
                border: 1px solid {S['border']};
                border-left: 3px solid {S['accent']};
            }}
        ''')
        cdl = QVBoxLayout(cd_box)
        cdl.setContentsMargins(12, 10, 12, 10)
        cdl.setSpacing(4)

        self.countdown_title_label = QLabel('下一个提醒')
        self.countdown_title_label.setFont(QFont('Microsoft YaHei', 10))
        self.countdown_title_label.setStyleSheet(f'color: {S["text_secondary"]};')
        cdl.addWidget(self.countdown_title_label)

        self.countdown_label = QLabel('00:00:00')
        self.countdown_label.setFont(QFont('Consolas', 26, QFont.Weight.Bold))
        self.countdown_label.setStyleSheet(f'color: {S["accent"]};')
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cdl.addWidget(self.countdown_label)

        inner.addWidget(cd_box)

        # --- 功能按钮 ---
        btn_grid = QHBoxLayout()
        btn_grid.setSpacing(8)

        buttons = [
            ('打卡', self.open_habit),
            ('课表', self.open_course),
            ('复盘', self.open_review),
            ('设置', self.open_settings),
        ]
        self.habit_btn = None
        self.course_btn = None
        self.review_btn = None
        self.settings_btn = None
        for i, (text, slot) in enumerate(buttons):
            btn = self._create_action_button(text)
            btn.clicked.connect(slot)
            btn_grid.addWidget(btn)
            if i == 0: self.habit_btn = btn
            elif i == 1: self.course_btn = btn
            elif i == 2: self.review_btn = btn
            elif i == 3: self.settings_btn = btn

        inner.addLayout(btn_grid)

        # --- 统计 ---
        self.stats_bar = QWidget()
        self.stats_bar.setStyleSheet(f'''
            QWidget {{
                background-color: {S['bg']};
                border-radius: 6px;
                border: 1px solid {S['border']};
            }}
        ''')
        sl = QHBoxLayout(self.stats_bar)
        sl.setContentsMargins(10, 5, 10, 5)

        self.stats_label = QLabel()
        self.stats_label.setFont(QFont('Consolas', 9))
        self.stats_label.setStyleSheet(f'color: {S["text_dim"]};')
        sl.addWidget(self.stats_label)
        sl.addStretch()

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedSize(60, 4)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet(f'''
            QProgressBar {{
                background-color: {S['border']};
                border: none;
                border-radius: 2px;
            }}
            QProgressBar::chunk {{
                background-color: {S['accent']};
                border-radius: 2px;
            }}
        ''')
        sl.addWidget(self.progress_bar)

        inner.addWidget(self.stats_bar)

    def _create_section_label(self, text):
        S = get_theme()
        lbl = QLabel(text)
        lbl.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        lbl.setStyleSheet(f'color: {S["text_primary"]};')
        return lbl

    def _create_action_button(self, text):
        S = get_theme()
        btn = QPushButton(text)
        btn.setFont(QFont('Microsoft YaHei', 11, QFont.Weight.Bold))
        btn.setFixedSize(68, 44)
        btn.setStyleSheet(f'''
            QPushButton {{
                background-color: {S['bg_module']};
                color: {S['text_primary']};
                border: 1px solid {S['border']};
                border-radius: 8px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {S['accent']};
                color: {S['text_on_accent']};
                border-color: {S['accent']};
            }}
        ''')
        return btn

    # ========== 系统托盘 ==========

    def init_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(_create_tray_icon())
        self.tray_icon.setToolTip('学习纪律官')

        tray_menu = QMenu()
        S = get_theme()
        tray_menu.setStyleSheet(f'''
            QMenu {{
                background-color: {S['bg_card']};
                border: 1px solid {S['border']};
                border-radius: 8px;
                padding: 6px;
                color: {S['text_primary']};
            }}
            QMenu::item {{
                padding: 6px 20px;
                border-radius: 4px;
            }}
            QMenu::item:selected {{
                background-color: {S['border']};
            }}
            QMenu::separator {{
                height: 1px;
                background-color: {S['border']};
                margin: 4px 6px;
            }}
        ''')

        show_action = QAction('显示主面板', self)
        show_action.triggered.connect(self.show_and_raise)
        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        quit_action = QAction('退出', self)
        quit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.on_tray_activated)

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_and_raise()

    def show_and_raise(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def minimize_to_tray(self):
        self.hide()
        self.tray_icon.showMessage(
            '学习纪律官', '已最小化到系统托盘，双击图标可恢复',
            QSystemTrayIcon.MessageIcon.Information, 2000
        )

    def quit_app(self):
        self.tray_icon.hide()
        QApplication.instance().quit()

    # ========== 快捷键 ==========

    def init_shortcuts(self):
        QShortcut(QKeySequence('Ctrl+Shift+H'), self, self.minimize_to_tray)
        QShortcut(QKeySequence('Ctrl+Shift+S'), self, self.toggle_visibility)
        QShortcut(QKeySequence(Qt.Key.Key_Escape), self, self.minimize_to_tray)
        QShortcut(QKeySequence('Ctrl+W'), self, self.quit_app)

    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.show_and_raise()

    # ========== 提醒引擎 ==========

    def init_reminders(self):
        self.reminder_engine = ReminderEngine()
        self.reminder_engine.reminder_triggered.connect(self.on_reminder)

    def on_reminder(self, data):
        popup = ReminderPopup(data, self)
        popup.show()
        self.tray_icon.showMessage(
            data['title'], data['description'],
            QSystemTrayIcon.MessageIcon.Information, 5000
        )

    # ========== 功能打开 ==========

    def open_habit(self):
        HabitPanel(self).exec()

    def open_course(self):
        CourseView(self).exec()

    def open_review(self):
        ReviewDialog(self).exec()

    def open_settings(self):
        old_theme = config.get('theme', 'dark')
        SettingsDialog(self).exec()
        new_theme = config.get('theme', 'dark')
        if old_theme != new_theme:
            self.apply_theme()

    def _refresh_buttons(self, S):
        btns = [self.habit_btn, self.course_btn, self.review_btn, self.settings_btn]
        for btn in btns:
            if btn:
                btn.setStyleSheet(f'''
                    QPushButton {{
                        background-color: {S['bg_module']};
                        color: {S['text_primary']};
                        border: 1px solid {S['border']};
                        border-radius: 8px;
                        font-size: 12px;
                    }}
                    QPushButton:hover {{
                        background-color: {S['accent']};
                        color: {S['text_on_accent']};
                        border-color: {S['accent']};
                    }}
                ''')

    def apply_theme(self):
        """应用主题"""
        S = get_theme()

        self.card.setStyleSheet(f'''
            #mainCard {{
                background-color: {S['bg_card']};
                border-radius: 16px;
                border: 1px solid {S['border']};
            }}
        ''')

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        r, g, b, a = S['shadow_color']
        shadow.setColor(QColor(r, g, b, a))
        shadow.setOffset(0, 6)
        self.card.setGraphicsEffect(shadow)

        glow = self.findChild(QLabel, 'glowBar')
        if glow:
            glow.setStyleSheet(f'''
                QLabel {{ background-color: {S['accent']}; border-radius: 1px; }}
            ''')

        self.title_label.setStyleSheet(f'color: {S["text_primary"]};')
        self.date_label.setStyleSheet(f'color: {S["text_dim"]};')

        for w in self.card.findChildren(QWidget):
            if w.objectName() == 'moduleBox':
                w.setStyleSheet(f'''
                    #moduleBox {{
                        background-color: {S['bg_module']};
                        border-radius: 10px;
                        border: 1px solid {S['border']};
                    }}
                ''')
            elif w.objectName() == 'countdownBox':
                w.setStyleSheet(f'''
                    #countdownBox {{
                        background-color: {S['bg_module']};
                        border-radius: 10px;
                        border: 1px solid {S['border']};
                        border-left: 3px solid {S['accent']};
                    }}
                ''')

        self.course_list_label.setStyleSheet(f'color: {S["text_secondary"]};')
        self.countdown_title_label.setStyleSheet(f'color: {S["text_secondary"]};')
        self.countdown_label.setStyleSheet(f'color: {S["accent"]};')
        self.stats_label.setStyleSheet(f'color: {S["text_dim"]};')
        self.stats_bar.setStyleSheet(f'''
            QWidget {{
                background-color: {S['bg']};
                border-radius: 6px;
                border: 1px solid {S['border']};
            }}
        ''')
        self.progress_bar.setStyleSheet(f'''
            QProgressBar {{
                background-color: {S['border']};
                border: none;
                border-radius: 2px;
            }}
            QProgressBar::chunk {{
                background-color: {S['accent']};
                border-radius: 2px;
            }}
        ''')

        self._refresh_buttons(S)
        self.update_all()

    # ========== 数据更新 ==========

    def update_all(self):
        now = datetime.now()
        today_str = now.strftime('%Y-%m-%d')

        self.date_label.setText(
            f'{now.strftime("%Y.%m.%d")}  {now.strftime("%H:%M:%S")}  '
            f'{["MON","TUE","WED","THU","FRI","SAT","SUN"][now.weekday()]}'
        )

        courses = db.get_courses_by_date(today_str)
        if courses:
            lines = []
            for c in courses:
                if c[8]:
                    lines.append('  [REST]  休息日')
                elif c[9]:
                    lines.append('  [STUDY] 自习')
                else:
                    t = f'{c[5]}~{c[6]}' if c[5] and c[6] else ''
                    lines.append(f'  {t}  {c[3]}')
            self.course_list_label.setText('\n'.join(lines))
        else:
            self.course_list_label.setText('  NO SCHEDULE')

        self.update_countdown()
        self.update_stats()

    def update_countdown(self):
        next_reminder = self.reminder_engine.get_next_reminder()
        S = get_theme()
        if next_reminder is None:
            self.countdown_title_label.setText('ALL DONE')
            self.countdown_label.setText('--:--:--')
            self.countdown_label.setStyleSheet(f'color: {S["text_dim"]};')
            return

        now = datetime.now()
        reminder_time = next_reminder['time']
        seconds_left = int((reminder_time - now).total_seconds())

        self.countdown_title_label.setText(next_reminder['title'])

        if seconds_left <= 0:
            self.countdown_label.setText('NOW!')
            self.countdown_label.setStyleSheet(f'color: {S["accent"]};')
            return

        if seconds_left < 300:
            self.countdown_label.setStyleSheet(f'color: {S["accent"]};')
        else:
            self.countdown_label.setStyleSheet(f'color: {S["accent_dim"]};')

        h = seconds_left // 3600
        m = (seconds_left % 3600) // 60
        s = seconds_left % 60
        self.countdown_label.setText(f'{h:02d}:{m:02d}:{s:02d}')

    def update_stats(self):
        today_str = datetime.now().strftime('%Y-%m-%d')
        habits = config.get_habits()
        checked_status = {r[0]: r[2] for r in db.get_habit_status(today_str)}
        checked = sum(1 for h in habits if checked_status.get(h['index'], 0))
        total = len(habits)

        courses = db.get_courses_by_date(today_str)
        has_rest = any(c[8] for c in courses)

        self.stats_label.setText(f'HABIT {checked}/{total}')
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(checked)

        if has_rest:
            self.stats_label.setText(f'HABIT {checked}/{total}  |  REST DAY')

    # ========== 拖拽移动 ==========

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.minimize_to_tray()
