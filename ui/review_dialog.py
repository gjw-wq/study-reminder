from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                               QTextEdit, QPushButton, QMessageBox, QScrollArea,
                               QWidget, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from datetime import datetime, timedelta

from core.database import db

TECH_STYLE = {
    'bg': '#0a0a0a', 'bg_card': '#111111', 'bg_module': '#0a0a0a', 'bg_input': '#111111',
    'border': '#1f1f1f', 'accent': '#3ddc84', 'accent_dim': '#2a9d5f',
    'text_primary': '#ffffff', 'text_secondary': '#a0a0a0', 'text_dim': '#555555',
    'text_on_accent': '#0a0a0a',
}

class ReviewDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('每日学习复盘')
        self.setMinimumSize(500, 650)
        self.resize(500, 650)
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
        title = QLabel('今日学习复盘')
        title.setFont(QFont('Microsoft YaHei', 16, QFont.Weight.Bold))
        title.setStyleSheet(f'color: {TECH_STYLE["text_primary"]};')
        layout.addWidget(title)

        # 日期
        today_str = datetime.now().strftime('%Y-%m-%d')
        date_label = QLabel(today_str)
        date_label.setFont(QFont('Microsoft YaHei', 10))
        date_label.setStyleSheet(f'color: {TECH_STYLE["text_secondary"]};')
        layout.addWidget(date_label)

        # 可滚动内容区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setStyleSheet(f'border: none; background-color: transparent;')

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(12)

        # 今日课程回顾
        courses = db.get_courses_by_date(today_str)
        # 只显示非休息且非自习的课程
        study_courses = [c for c in courses if c[4] not in ('rest', 'self_study') and not c[8] and not c[9]]

        if study_courses:
            review_label = QLabel('今日所学课程:')
            review_label.setFont(QFont('Microsoft YaHei', 11, QFont.Weight.Bold))
            review_label.setStyleSheet(f'color: {TECH_STYLE["accent"]};')
            content_layout.addWidget(review_label)

            # 去重：同一门课只显示一次
            seen = set()
            unique_courses = []
            for c in study_courses:
                if c[3] not in seen:
                    seen.add(c[3])
                    unique_courses.append(c)

            courses_text = '、'.join([c[3] for c in unique_courses])
            courses_info = QLabel(courses_text)
            courses_info.setFont(QFont('Microsoft YaHei', 10))
            courses_info.setStyleSheet(f'color: {TECH_STYLE["text_secondary"]};')
            courses_info.setWordWrap(True)
            content_layout.addWidget(courses_info)
        else:
            # 休息日或自习日提示
            rest_label = QLabel('今日无课程安排')
            rest_label.setFont(QFont('Microsoft YaHei', 11))
            rest_label.setStyleSheet(f'color: {TECH_STYLE["text_secondary"]};')
            content_layout.addWidget(rest_label)

        # 收获输入
        gains_box = QWidget()
        gains_box.setStyleSheet(f'''
            QWidget {{
                background-color: {TECH_STYLE['bg_card']};
                border-radius: 8px;
                border: 1px solid {TECH_STYLE['border']};
            }}
        ''')
        gains_layout = QVBoxLayout(gains_box)
        gains_layout.setContentsMargins(12, 10, 12, 10)
        gains_layout.setSpacing(8)

        gains_title = QLabel('今日收获')
        gains_title.setFont(QFont('Microsoft YaHei', 11, QFont.Weight.Bold))
        gains_title.setStyleSheet(f'color: {TECH_STYLE["text_primary"]};')
        gains_layout.addWidget(gains_title)

        self.gain1_edit = QTextEdit()
        self.gain1_edit.setPlaceholderText('收获 1（必填）...')
        self.gain1_edit.setFixedHeight(60)
        self.gain1_edit.setStyleSheet(f'''
            QTextEdit {{
                border: 1px solid {TECH_STYLE['border']};
                border-radius: 6px;
                padding: 6px;
                font-size: 12px;
                background-color: {TECH_STYLE['bg_input']};
                color: {TECH_STYLE['text_primary']};
            }}
        ''')
        gains_layout.addWidget(self.gain1_edit)

        self.gain2_edit = QTextEdit()
        self.gain2_edit.setPlaceholderText('收获 2（选填）...')
        self.gain2_edit.setFixedHeight(60)
        self.gain2_edit.setStyleSheet(f'''
            QTextEdit {{
                border: 1px solid {TECH_STYLE['border']};
                border-radius: 6px;
                padding: 6px;
                font-size: 12px;
                background-color: {TECH_STYLE['bg_input']};
                color: {TECH_STYLE['text_primary']};
            }}
        ''')
        gains_layout.addWidget(self.gain2_edit)

        self.gain3_edit = QTextEdit()
        self.gain3_edit.setPlaceholderText('收获 3（选填）...')
        self.gain3_edit.setFixedHeight(60)
        self.gain3_edit.setStyleSheet(f'''
            QTextEdit {{
                border: 1px solid {TECH_STYLE['border']};
                border-radius: 6px;
                padding: 6px;
                font-size: 12px;
                background-color: {TECH_STYLE['bg_input']};
                color: {TECH_STYLE['text_primary']};
            }}
        ''')
        gains_layout.addWidget(self.gain3_edit)

        content_layout.addWidget(gains_box)

        # 疑问
        question_box = QWidget()
        question_box.setStyleSheet(f'''
            QWidget {{
                background-color: {TECH_STYLE['bg_card']};
                border-radius: 8px;
                border: 1px solid {TECH_STYLE['border']};
            }}
        ''')
        question_layout = QVBoxLayout(question_box)
        question_layout.setContentsMargins(12, 10, 12, 10)
        question_layout.setSpacing(8)

        q_title = QLabel('遗留疑问')
        q_title.setFont(QFont('Microsoft YaHei', 11, QFont.Weight.Bold))
        q_title.setStyleSheet(f'color: {TECH_STYLE["accent"]};')
        question_layout.addWidget(q_title)

        self.question_edit = QTextEdit()
        self.question_edit.setPlaceholderText('有什么没搞懂的问题？明天记得问老师或同学...')
        self.question_edit.setFixedHeight(60)
        self.question_edit.setStyleSheet(f'''
            QTextEdit {{
                border: 1px solid {TECH_STYLE['border']};
                border-radius: 6px;
                padding: 6px;
                font-size: 12px;
                background-color: {TECH_STYLE['bg_input']};
                color: {TECH_STYLE['text_primary']};
            }}
        ''')
        question_layout.addWidget(self.question_edit)

        content_layout.addWidget(question_box)

        # 明日预习
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        tomorrow_courses = db.get_courses_by_date(tomorrow)
        if tomorrow_courses:
            preview_box = QWidget()
            preview_box.setStyleSheet(f'''
                QWidget {{
                    background-color: {TECH_STYLE['bg_card']};
                    border-radius: 8px;
                    border: 1px solid {TECH_STYLE['border']};
                }}
            ''')
            preview_layout = QVBoxLayout(preview_box)
            preview_layout.setContentsMargins(12, 10, 12, 10)
            preview_layout.setSpacing(6)

            t_label = QLabel('明日课程预告:')
            t_label.setFont(QFont('Microsoft YaHei', 11, QFont.Weight.Bold))
            t_label.setStyleSheet(f'color: {TECH_STYLE["accent"]};')
            preview_layout.addWidget(t_label)

            tomorrow_text = '、'.join([c[3] for c in tomorrow_courses if not c[8]])
            if tomorrow_text:
                t_info = QLabel(tomorrow_text)
                t_info.setFont(QFont('Microsoft YaHei', 10))
                t_info.setStyleSheet(f'color: {TECH_STYLE["text_secondary"]};')
                t_info.setWordWrap(True)
                preview_layout.addWidget(t_info)

            content_layout.addWidget(preview_box)

        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll, 1)

        # 底部按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        cancel_btn = QPushButton('稍后再说')
        cancel_btn.setFont(QFont('Microsoft YaHei', 11))
        cancel_btn.setMinimumHeight(36)
        cancel_btn.setStyleSheet(f'''
            QPushButton {{
                background-color: {TECH_STYLE['bg']};
                color: {TECH_STYLE['text_secondary']};
                font-size: 12px;
                padding: 8px 20px;
                border: 1px solid {TECH_STYLE['border']};
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: {TECH_STYLE['accent']};
                color: {TECH_STYLE['text_on_accent']};
                border-color: {TECH_STYLE['accent']};
            }}
        ''')
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        submit_btn = QPushButton('提交复盘')
        submit_btn.setFont(QFont('Microsoft YaHei', 11))
        submit_btn.setMinimumHeight(36)
        submit_btn.setStyleSheet(f'''
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
        submit_btn.clicked.connect(self.submit)
        btn_layout.addWidget(submit_btn)

        layout.addLayout(btn_layout)

    def submit(self):
        gain1 = self.gain1_edit.toPlainText().strip()
        if not gain1:
            QMessageBox.warning(self, '提示', '请至少填写一个收获')
            return

        today_str = datetime.now().strftime('%Y-%m-%d')
        # 获取今日课程名称（去重，排除休息和自习）
        courses = db.get_courses_by_date(today_str)
        study_courses = [c for c in courses if c[4] not in ('rest', 'self_study') and not c[8] and not c[9]]
        seen = set()
        unique_names = []
        for c in study_courses:
            if c[3] not in seen:
                seen.add(c[3])
                unique_names.append(c[3])
        courses_text = '、'.join(unique_names) if unique_names else '无课程'

        db.save_study_log(
            today_str,
            gain1,
            self.gain2_edit.toPlainText().strip(),
            self.gain3_edit.toPlainText().strip(),
            self.question_edit.toPlainText().strip(),
            courses_text
        )

        QMessageBox.information(self, '完成', '今日复盘已保存，继续保持！')
        self.accept()
