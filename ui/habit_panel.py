from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QScrollArea, QMessageBox, QSizePolicy,
                               QTableWidget, QTableWidgetItem, QHeaderView, QWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from datetime import datetime, timedelta

from core.database import db
from core.config import config

TECH_STYLE = {
    'bg': '#0a0a0a', 'bg_card': '#111111', 'bg_module': '#0a0a0a', 'bg_input': '#111111',
    'border': '#1f1f1f', 'accent': '#3ddc84', 'accent_dim': '#2a9d5f',
    'text_primary': '#ffffff', 'text_secondary': '#a0a0a0', 'text_dim': '#555555',
    'text_on_accent': '#0a0a0a',
}


class HabitHistoryDialog(QDialog):
    """打卡记录查看对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('打卡记录')
        self.setMinimumSize(500, 400)
        self.resize(500, 450)
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet(f'''
            QDialog {{
                background-color: {TECH_STYLE['bg']};
                color: {TECH_STYLE['text_primary']};
            }}
        ''')

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel('打卡记录')
        title.setFont(QFont('Microsoft YaHei', 16, QFont.Weight.Bold))
        title.setStyleSheet(f'color: {TECH_STYLE["text_primary"]};')
        layout.addWidget(title)

        # 最近7天数据
        today = datetime.now()
        dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]

        table = QTableWidget()
        table.setColumnCount(8)
        headers = ['日期'] + [h['name'] for h in config.get_habits()]
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        table.setColumnWidth(0, 100)
        table.setRowCount(len(dates))
        table.setStyleSheet(f'''
            QTableWidget {{
                border: 1px solid {TECH_STYLE['border']};
                border-radius: 8px;
                font-size: 12px;
                background-color: {TECH_STYLE['bg']};
                color: {TECH_STYLE['text_primary']};
                gridline-color: {TECH_STYLE['border']};
            }}
            QTableWidget::item {{
                padding: 6px;
            }}
            QHeaderView::section {{
                background-color: {TECH_STYLE['bg_card']};
                color: {TECH_STYLE['text_secondary']};
                padding: 8px;
                font-weight: bold;
                border: none;
                border-bottom: 2px solid {TECH_STYLE['accent']};
            }}
        ''')

        habits = config.get_habits()
        for row_idx, date_str in enumerate(dates):
            # 日期列
            date_item = QTableWidgetItem(date_str)
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            date_item.setForeground(QColor(TECH_STYLE['text_secondary']))
            table.setItem(row_idx, 0, date_item)

            # 各习惯打卡状态
            checked_status = {r[0]: r[2] for r in db.get_habit_status(date_str)}
            for col_idx, habit in enumerate(habits, 1):
                checked = checked_status.get(habit['index'], 0)
                item = QTableWidgetItem('✓' if checked else '')
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if checked:
                    item.setBackground(QColor(TECH_STYLE['accent']))
                    item.setForeground(QColor(TECH_STYLE['text_on_accent']))
                else:
                    item.setForeground(QColor(TECH_STYLE['text_dim']))
                table.setItem(row_idx, col_idx, item)

        layout.addWidget(table)

        # 统计摘要
        stats = QLabel()
        total_days = len(dates)
        total_possible = total_days * len(habits)
        total_checked = 0
        for date_str in dates:
            checked_status = {r[0]: r[2] for r in db.get_habit_status(date_str)}
            total_checked += sum(1 for h in habits if checked_status.get(h['index'], 0))

        rate = (total_checked / total_possible * 100) if total_possible > 0 else 0
        stats.setText(f'最近7天完成率: {total_checked}/{total_possible} ({rate:.1f}%)')
        stats.setFont(QFont('Microsoft YaHei', 11, QFont.Weight.Bold))
        stats.setStyleSheet(f'color: {TECH_STYLE["accent"]};')
        stats.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(stats)

        close_btn = QPushButton('关闭')
        close_btn.setMinimumHeight(36)
        close_btn.setStyleSheet(f'''
            QPushButton {{
                background-color: {TECH_STYLE['accent']};
                color: {TECH_STYLE['text_on_accent']};
                font-size: 12px;
                padding: 8px 24px;
                border: none;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: {TECH_STYLE['accent_dim']};
            }}
        ''')
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)


class HabitPanel(QDialog):
    """习惯打卡面板 - 使用标准QDialog弹窗"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('今日习惯打卡')
        self.setMinimumSize(420, 480)
        self.resize(420, 500)
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet(f'''
            QDialog {{
                background-color: {TECH_STYLE['bg']};
                color: {TECH_STYLE['text_primary']};
            }}
        ''')

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # 标题
        title = QLabel('今日习惯打卡')
        title.setFont(QFont('Microsoft YaHei', 16, QFont.Weight.Bold))
        title.setStyleSheet(f'color: {TECH_STYLE["text_primary"]};')
        layout.addWidget(title)

        # 日期行
        date_row = QHBoxLayout()
        today_str = datetime.now().strftime('%Y-%m-%d')
        date_label = QLabel(today_str)
        date_label.setFont(QFont('Microsoft YaHei', 10))
        date_label.setStyleSheet(f'color: {TECH_STYLE["text_secondary"]};')
        date_row.addWidget(date_label)
        date_row.addStretch()

        # 查看记录按钮
        history_btn = QPushButton('查看记录')
        history_btn.setFont(QFont('Microsoft YaHei', 10))
        history_btn.setFixedHeight(30)
        history_btn.setStyleSheet(f'''
            QPushButton {{
                background-color: {TECH_STYLE['bg']};
                color: {TECH_STYLE['text_secondary']};
                font-size: 11px;
                padding: 4px 12px;
                border: 1px solid {TECH_STYLE['border']};
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: {TECH_STYLE['accent']};
                color: {TECH_STYLE['text_on_accent']};
                border-color: {TECH_STYLE['accent']};
            }}
        ''')
        history_btn.clicked.connect(self.show_history)
        date_row.addWidget(history_btn)
        layout.addLayout(date_row)

        # 打卡列表
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f'border: none; background-color: transparent;')
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)
        list_layout.setSpacing(10)

        habits = config.get_habits()
        checked_status = {row[0]: row[2] for row in db.get_habit_status(today_str)}

        self.habit_buttons = {}
        for habit in habits:
            item = self._create_habit_item(habit, checked_status.get(habit['index'], 0))
            list_layout.addWidget(item)

        list_layout.addStretch()
        scroll.setWidget(list_widget)
        layout.addWidget(scroll)

        # 统计
        self.stats_label = QLabel()
        self.stats_label.setFont(QFont('Microsoft YaHei', 12, QFont.Weight.Bold))
        self.stats_label.setStyleSheet(f'color: {TECH_STYLE["accent"]};')
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.stats_label)
        self.update_stats()

        # 底部按钮
        check_all_btn = QPushButton('一键全部打卡')
        check_all_btn.setFont(QFont('Microsoft YaHei', 11))
        check_all_btn.setMinimumHeight(38)
        check_all_btn.setStyleSheet(f'''
            QPushButton {{
                background-color: {TECH_STYLE['accent']};
                color: {TECH_STYLE['text_on_accent']};
                font-size: 12px;
                padding: 8px 20px;
                border: none;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: {TECH_STYLE['accent_dim']};
            }}
        ''')
        check_all_btn.clicked.connect(self.check_all)
        layout.addWidget(check_all_btn)

    def _create_habit_item(self, habit, checked):
        item = QWidget()
        item.setStyleSheet(f'''
            QWidget {{
                background-color: {TECH_STYLE['bg_card']};
                border-radius: 10px;
                border: 1px solid {TECH_STYLE['border']};
            }}
        ''')
        item.setFixedHeight(52)

        layout = QHBoxLayout(item)
        layout.setContentsMargins(14, 8, 14, 8)

        # 序号
        idx_label = QLabel(str(habit['index'] + 1))
        idx_label.setFont(QFont('Microsoft YaHei', 10, QFont.Weight.Bold))
        idx_label.setFixedWidth(24)
        idx_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        idx_label.setStyleSheet(f'''
            color: {TECH_STYLE['text_secondary']};
            background-color: {TECH_STYLE['border']};
            border-radius: 12px;
            padding: 2px 0px;
        ''')
        layout.addWidget(idx_label)

        # 名称
        name_label = QLabel(habit['name'])
        name_label.setFont(QFont('Microsoft YaHei', 11))
        name_label.setStyleSheet(f'color: {TECH_STYLE["text_primary"]};')
        layout.addWidget(name_label)

        layout.addStretch()

        # 连续天数
        streak = db.get_streak(habit['index'])
        if streak > 0:
            streak_label = QLabel(f'{streak}天')
            streak_label.setFont(QFont('Microsoft YaHei', 9, QFont.Weight.Bold))
            streak_label.setStyleSheet(f'color: {TECH_STYLE["accent"]};')
            layout.addWidget(streak_label)

        # 打卡按钮
        check_btn = QPushButton('已打卡 ✓' if checked else '打卡')
        check_btn.setFixedSize(80, 34)
        check_btn.setProperty('habit_index', habit['index'])
        check_btn.setProperty('habit_name', habit['name'])

        if checked:
            check_btn.setStyleSheet(f'''
                QPushButton {{
                    background-color: {TECH_STYLE['accent']};
                    color: {TECH_STYLE['text_on_accent']};
                    font-size: 11px;
                    border: none;
                    border-radius: 8px;
                }}
            ''')
            check_btn.setEnabled(False)
        else:
            check_btn.setStyleSheet(f'''
                QPushButton {{
                    background-color: {TECH_STYLE['bg']};
                    color: {TECH_STYLE['text_primary']};
                    font-size: 11px;
                    border: 1px solid {TECH_STYLE['border']};
                    border-radius: 8px;
                }}
                QPushButton:hover {{
                    background-color: {TECH_STYLE['accent']};
                    color: {TECH_STYLE['text_on_accent']};
                    border-color: {TECH_STYLE['accent']};
                }}
            ''')
            check_btn.clicked.connect(self.on_check)

        self.habit_buttons[habit['index']] = check_btn
        layout.addWidget(check_btn)
        return item

    def on_check(self):
        btn = self.sender()
        habit_index = btn.property('habit_index')
        habit_name = btn.property('habit_name')
        today_str = datetime.now().strftime('%Y-%m-%d')

        db.check_habit(habit_index, habit_name, today_str, 1)

        btn.setText('已打卡 ✓')
        btn.setStyleSheet(f'''
            QPushButton {{
                background-color: {TECH_STYLE['accent']};
                color: {TECH_STYLE['text_on_accent']};
                font-size: 11px;
                border: none;
                border-radius: 8px;
            }}
        ''')
        btn.setEnabled(False)

        self.update_stats()

    def check_all(self):
        reply = QMessageBox.question(
            self, '确认', '确定要一键打卡所有习惯吗？',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            habits = config.get_habits()
            today_str = datetime.now().strftime('%Y-%m-%d')
            for habit in habits:
                db.check_habit(habit['index'], habit['name'], today_str, 1)

            for habit in habits:
                btn = self.habit_buttons.get(habit['index'])
                if btn and btn.isEnabled():
                    btn.setText('已打卡 ✓')
                    btn.setStyleSheet(f'''
                        QPushButton {{
                            background-color: {TECH_STYLE['accent']};
                            color: {TECH_STYLE['text_on_accent']};
                            font-size: 11px;
                            border: none;
                            border-radius: 8px;
                        }}
                    ''')
                    btn.setEnabled(False)

            self.update_stats()

    def update_stats(self):
        today_str = datetime.now().strftime('%Y-%m-%d')
        habits = config.get_habits()
        checked_status = {row[0]: row[2] for row in db.get_habit_status(today_str)}

        total = len(habits)
        checked = sum(1 for h in habits if checked_status.get(h['index'], 0))

        self.stats_label.setText(f'今日完成: {checked}/{total} 项')

    def show_history(self):
        dialog = HabitHistoryDialog(self)
        dialog.exec()
