from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                               QScrollArea, QPushButton, QTabWidget, QSizePolicy,
                               QGraphicsDropShadowEffect, QWidget)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QFont, QColor
from datetime import datetime, timedelta

from core.database import db
from .course_editor import CourseEditorDialog

TECH_STYLE = {
    'bg': '#0a0a0a', 'bg_card': '#111111', 'bg_module': '#0a0a0a', 'bg_input': '#111111',
    'border': '#1f1f1f', 'accent': '#3ddc84', 'accent_dim': '#2a9d5f',
    'text_primary': '#ffffff', 'text_secondary': '#a0a0a0', 'text_dim': '#555555',
    'text_on_accent': '#0a0a0a',
}


class CourseView(QDialog):
    """课程表视图 - 使用标准QDialog弹窗"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('AI大模型就业6期课程表')
        self.setMinimumSize(560, 480)
        self.resize(600, 520)
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
        title = QLabel('AI大模型就业6期课程表')
        title.setFont(QFont('Microsoft YaHei', 16, QFont.Weight.Bold))
        title.setStyleSheet(f'color: {TECH_STYLE["text_primary"]};')
        layout.addWidget(title)

        # 编辑按钮行
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        edit_btn = QPushButton('编辑课表')
        edit_btn.setFont(QFont('Microsoft YaHei', 10))
        edit_btn.setFixedHeight(30)
        edit_btn.setStyleSheet(f'''
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
        edit_btn.clicked.connect(self.open_editor)
        btn_row.addWidget(edit_btn)
        layout.addLayout(btn_row)

        # 标签页
        tabs = QTabWidget()
        tabs.setStyleSheet(f'''
            QTabWidget::pane {{
                border: 1px solid {TECH_STYLE['border']};
                border-radius: 8px;
                background-color: {TECH_STYLE['bg']};
                top: -1px;
            }}
            QTabBar::tab {{
                padding: 8px 20px;
                margin-right: 2px;
                border-radius: 6px 6px 0px 0px;
                font-size: 12px;
                background-color: transparent;
                color: {TECH_STYLE['text_dim']};
                border: none;
                border-bottom: 2px solid transparent;
            }}
            QTabBar::tab:selected {{
                color: {TECH_STYLE['accent']};
                border-bottom: 2px solid {TECH_STYLE['accent']};
                background-color: transparent;
            }}
            QTabBar::tab:!selected {{
                background-color: transparent;
                color: {TECH_STYLE['text_dim']};
            }}
        ''')

        tabs.addTab(self._create_week_view(), '周视图')
        tabs.addTab(self._create_today_view(), '今日')

        layout.addWidget(tabs, 1)

    def open_editor(self):
        editor = CourseEditorDialog(self)
        editor.exec()

    def _create_week_view(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f'border: none; background: transparent;')
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(6)

        courses = db.get_all_courses()
        today_str = datetime.now().strftime('%Y-%m-%d')

        # 按日期分组显示
        current_date = None
        for course in courses:
            if course[1] != current_date:
                current_date = course[1]
                date_header = self._create_date_header(course)
                content_layout.addWidget(date_header)

            item = self._create_course_item(course, course[1] == today_str)
            content_layout.addWidget(item)

        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)

        return widget

    def _create_today_view(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        today_str = datetime.now().strftime('%Y-%m-%d')
        courses = db.get_courses_by_date(today_str)

        if not courses:
            empty = QLabel('今日无课程安排，好好休息！')
            empty.setFont(QFont('Microsoft YaHei', 14))
            empty.setStyleSheet(f'color: {TECH_STYLE["text_secondary"]}; padding: 40px;')
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(empty)
        else:
            date_header = self._create_date_header(courses[0])
            layout.addWidget(date_header)
            for course in courses:
                item = self._create_course_item(course, True)
                layout.addWidget(item)

        layout.addStretch()
        return widget

    def _create_date_header(self, course):
        """创建日期分组标题"""
        header = QWidget()
        header.setStyleSheet(f'''
            QWidget {{
                background-color: {TECH_STYLE['bg_card']};
                border-radius: 6px;
            }}
        ''')
        layout = QHBoxLayout(header)
        layout.setContentsMargins(12, 6, 12, 6)

        date_label = QLabel(f"{course[1]} {course[2]}")
        date_label.setFont(QFont('Microsoft YaHei', 11, QFont.Weight.Bold))
        date_label.setStyleSheet(f'color: {TECH_STYLE["text_secondary"]};')
        layout.addWidget(date_label)
        layout.addStretch()

        return header

    def _create_course_item(self, course, is_today):
        item = QWidget()

        if course[8]:  # is_rest
            border_left_color = TECH_STYLE['accent_dim']
            type_tag = '休息'
        elif course[9]:  # is_self_study
            border_left_color = TECH_STYLE['accent']
            type_tag = '自习'
        elif course[4] == 'project':  # project
            border_left_color = TECH_STYLE['accent']
            type_tag = '项目'
        else:
            border_left_color = TECH_STYLE['accent']
            type_tag = '上课'

        border_w = '3px' if is_today else '1px'
        border_side = f'border-left: {border_w} solid {border_left_color};'
        item.setStyleSheet(f'''
            QWidget {{
                background-color: {TECH_STYLE['bg_card']};
                border: 1px solid {TECH_STYLE['border']};
                {border_side}
                border-radius: 8px;
            }}
        ''')
        item.setFixedHeight(52)

        layout = QHBoxLayout(item)
        layout.setContentsMargins(12, 6, 12, 6)

        # 类型标签
        tag = QLabel(type_tag)
        tag.setFont(QFont('Microsoft YaHei', 9))
        tag.setFixedWidth(40)
        tag.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tag.setStyleSheet(f'''
            color: {TECH_STYLE['text_on_accent']};
            background-color: {border_left_color};
            padding: 2px 4px;
            border-radius: 4px;
        ''')
        layout.addWidget(tag)

        # 时间
        time_str = f"{course[5]}~{course[6]}" if course[5] and course[6] else ''
        time_label = QLabel(time_str)
        time_label.setFont(QFont('Consolas', 10))
        time_label.setStyleSheet(f'color: {TECH_STYLE["text_secondary"]};')
        time_label.setFixedWidth(90)
        layout.addWidget(time_label)

        # 课程名称
        title = QLabel(course[3])
        title.setFont(QFont('Microsoft YaHei', 11, QFont.Weight.Bold))
        title.setStyleSheet(f'color: {TECH_STYLE["text_primary"]};')
        layout.addWidget(title)

        layout.addStretch()

        if is_today:
            badge = QLabel('今天')
            badge.setFont(QFont('Microsoft YaHei', 9, QFont.Weight.Bold))
            badge.setStyleSheet(f'''
                background-color: {TECH_STYLE['accent']};
                color: {TECH_STYLE['text_on_accent']};
                padding: 3px 10px;
                border-radius: 10px;
            ''')
            layout.addWidget(badge)

        return item
