from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QComboBox, QTableWidget,
                               QTableWidgetItem, QHeaderView, QMessageBox,
                               QDateEdit, QTimeEdit, QScrollArea, QWidget,
                               QSizePolicy)
from PyQt6.QtCore import Qt, QDate, QTime
from PyQt6.QtGui import QFont, QColor
from datetime import datetime

from core.database import db


class CourseEditorDialog(QDialog):
    """课程表编辑对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('编辑课程表')
        self.setMinimumSize(700, 550)
        self.resize(750, 550)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # 标题
        title = QLabel('📅 课程表编辑')
        title.setFont(QFont('Microsoft YaHei', 16, QFont.Weight.Bold))
        title.setStyleSheet('color: #333333;')
        layout.addWidget(title)
        
        # 添加新课程区域
        add_box = QWidget()
        add_box.setStyleSheet('''
            QWidget {
                background-color: #f8f9fa;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
        ''')
        add_layout = QVBoxLayout(add_box)
        add_layout.setContentsMargins(12, 10, 12, 10)
        add_layout.setSpacing(8)
        
        add_title = QLabel('添加/修改课程')
        add_title.setFont(QFont('Microsoft YaHei', 11, QFont.Weight.Bold))
        add_title.setStyleSheet('color: #0066CC;')
        add_layout.addWidget(add_title)
        
        # 输入行
        input_row = QHBoxLayout()
        input_row.setSpacing(8)
        
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setDisplayFormat('yyyy-MM-dd')
        self.date_edit.setMinimumHeight(28)
        input_row.addWidget(QLabel('日期:'))
        input_row.addWidget(self.date_edit)
        
        self.weekday_combo = QComboBox()
        self.weekday_combo.addItems(['周一', '周二', '周三', '周四', '周五', '周六', '周日'])
        self.weekday_combo.setMinimumHeight(28)
        input_row.addWidget(QLabel('星期:'))
        input_row.addWidget(self.weekday_combo)
        
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText('课程名称')
        self.title_edit.setMinimumHeight(28)
        input_row.addWidget(QLabel('课程:'))
        input_row.addWidget(self.title_edit, 1)
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(['上课', '项目', '自习', '休息'])
        self.type_combo.setMinimumHeight(28)
        input_row.addWidget(QLabel('类型:'))
        input_row.addWidget(self.type_combo)
        
        add_layout.addLayout(input_row)
        
        # 时间行
        time_row = QHBoxLayout()
        time_row.setSpacing(8)
        
        self.start_time = QTimeEdit()
        self.start_time.setDisplayFormat('HH:mm')
        self.start_time.setTime(QTime(9, 0))
        self.start_time.setMinimumHeight(28)
        time_row.addWidget(QLabel('开始时间:'))
        time_row.addWidget(self.start_time)
        
        self.end_time = QTimeEdit()
        self.end_time.setDisplayFormat('HH:mm')
        self.end_time.setTime(QTime(12, 0))
        self.end_time.setMinimumHeight(28)
        time_row.addWidget(QLabel('结束时间:'))
        time_row.addWidget(self.end_time)
        
        time_row.addStretch()
        
        add_btn = QPushButton('➕ 添加课程')
        add_btn.setMinimumHeight(32)
        add_btn.setStyleSheet('''
            QPushButton {
                background-color: #00AA66;
                color: white;
                font-size: 12px;
                padding: 6px 16px;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #008855;
            }
        ''')
        add_btn.clicked.connect(self.add_course)
        time_row.addWidget(add_btn)
        
        add_layout.addLayout(time_row)
        layout.addWidget(add_box)
        
        # 课程列表表格
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['日期', '星期', '课程名称', '类型', '开始', '结束', '操作'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(4, 60)
        self.table.setColumnWidth(5, 60)
        self.table.setColumnWidth(6, 80)
        self.table.setStyleSheet('''
            QTableWidget {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                font-size: 12px;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 8px;
                font-weight: bold;
                border: none;
                border-bottom: 2px solid #0066CC;
            }
        ''')
        layout.addWidget(self.table, 1)
        
        # 底部按钮
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        
        refresh_btn = QPushButton('🔄 刷新列表')
        refresh_btn.setMinimumHeight(36)
        refresh_btn.setStyleSheet('''
            QPushButton {
                background-color: #f0f0f0;
                color: #666666;
                font-size: 12px;
                padding: 8px 16px;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        ''')
        refresh_btn.clicked.connect(self.load_courses)
        btn_row.addWidget(refresh_btn)
        
        close_btn = QPushButton('关闭')
        close_btn.setMinimumHeight(36)
        close_btn.setStyleSheet('''
            QPushButton {
                background-color: #0066CC;
                color: white;
                font-size: 12px;
                padding: 8px 24px;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #0055aa;
            }
        ''')
        close_btn.clicked.connect(self.accept)
        btn_row.addWidget(close_btn)
        
        layout.addLayout(btn_row)
        
        self.load_courses()
    
    def load_courses(self):
        courses = db.get_all_courses()
        self.table.setRowCount(len(courses))
        
        type_map = {'lecture': '上课', 'project': '项目', 'self_study': '自习', 'rest': '休息'}
        
        for row_idx, course in enumerate(courses):
            # 日期
            self.table.setItem(row_idx, 0, QTableWidgetItem(course[1]))
            # 星期
            self.table.setItem(row_idx, 1, QTableWidgetItem(course[2]))
            # 课程名称
            self.table.setItem(row_idx, 2, QTableWidgetItem(course[3]))
            # 类型
            type_text = type_map.get(course[4], course[4])
            self.table.setItem(row_idx, 3, QTableWidgetItem(type_text))
            # 开始时间
            self.table.setItem(row_idx, 4, QTableWidgetItem(course[5] or ''))
            # 结束时间
            self.table.setItem(row_idx, 5, QTableWidgetItem(course[6] or ''))
            
            # 删除按钮
            del_btn = QPushButton('删除')
            del_btn.setProperty('course_id', course[0])
            del_btn.setStyleSheet('''
                QPushButton {
                    background-color: #ff4444;
                    color: white;
                    font-size: 10px;
                    padding: 2px 8px;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #cc0000;
                }
            ''')
            del_btn.clicked.connect(self.delete_course)
            self.table.setCellWidget(row_idx, 6, del_btn)
    
    def add_course(self):
        date_str = self.date_edit.date().toString('yyyy-MM-dd')
        weekday = self.weekday_combo.currentText()
        title = self.title_edit.text().strip()
        
        if not title:
            QMessageBox.warning(self, '提示', '请输入课程名称')
            return
        
        type_map = {'上课': 'lecture', '项目': 'project', '自习': 'self_study', '休息': 'rest'}
        course_type = type_map.get(self.type_combo.currentText(), 'lecture')
        
        start_time = self.start_time.time().toString('HH:mm')
        end_time = self.end_time.time().toString('HH:mm')
        
        is_rest = 1 if course_type == 'rest' else 0
        is_self_study = 1 if course_type == 'self_study' else 0
        
        db.insert_course(
            date=date_str,
            weekday=weekday,
            title=title,
            course_type=course_type,
            start_time=start_time,
            end_time=end_time,
            is_rest=is_rest,
            is_self_study=is_self_study
        )
        
        self.title_edit.clear()
        self.load_courses()
        QMessageBox.information(self, '成功', '课程已添加')
    
    def delete_course(self):
        btn = self.sender()
        course_id = btn.property('course_id')
        
        reply = QMessageBox.question(
            self, '确认', '确定要删除这门课程吗？',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM courses WHERE id = ?', (course_id,))
            conn.commit()
            conn.close()
            self.load_courses()
