from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                               QSpinBox, QCheckBox, QPushButton, QComboBox,
                               QLineEdit, QFormLayout, QMessageBox, QScrollArea,
                               QWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from core.config import config
from core.theme import get_theme


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('设置')
        self.setMinimumSize(440, 520)
        self.resize(440, 520)
        self._build_ui_structure()

    def _build_ui_structure(self):
        """构建UI结构（只创建控件，不设置样式）"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # 标题
        self.title_label = QLabel('设置')
        self.title_label.setFont(QFont('Microsoft YaHei', 16, QFont.Weight.Bold))
        layout.addWidget(self.title_label)

        # 可滚动表单区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        self.form_widget = QWidget()
        form = QFormLayout(self.form_widget)
        form.setSpacing(14)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        # === 提醒设置 ===
        self.section1 = QLabel('提醒设置')
        self.section1.setFont(QFont('Microsoft YaHei', 11, QFont.Weight.Bold))
        form.addRow(self.section1)

        self.advance_spin = QSpinBox()
        self.advance_spin.setRange(1, 60)
        self.advance_spin.setSuffix(' 分钟')
        self.advance_spin.setMinimumHeight(30)
        form.addRow('课程提前提醒:', self.advance_spin)

        self.popup_check = QCheckBox('弹窗提醒')
        form.addRow('', self.popup_check)

        self.sound_check = QCheckBox('声音提醒')
        form.addRow('', self.sound_check)

        self.tray_check = QCheckBox('托盘闪烁')
        form.addRow('', self.tray_check)

        # === 外观设置 ===
        self.section2 = QLabel('外观')
        self.section2.setFont(QFont('Microsoft YaHei', 11, QFont.Weight.Bold))
        form.addRow(self.section2)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(['深色模式', '浅色模式'])
        self.theme_combo.setMinimumHeight(30)
        form.addRow('主题:', self.theme_combo)

        # === 作息时间 ===
        self.section3 = QLabel('作息时间')
        self.section3.setFont(QFont('Microsoft YaHei', 11, QFont.Weight.Bold))
        form.addRow(self.section3)

        self.wake_edit = QLineEdit()
        self.wake_edit.setMinimumHeight(30)
        form.addRow('起床时间:', self.wake_edit)

        self.evening_start_edit = QLineEdit()
        self.evening_start_edit.setMinimumHeight(30)
        form.addRow('晚自习开始:', self.evening_start_edit)

        self.evening_end_edit = QLineEdit()
        self.evening_end_edit.setMinimumHeight(30)
        form.addRow('晚自习结束:', self.evening_end_edit)

        # === 启动设置 ===
        self.section4 = QLabel('启动')
        self.section4.setFont(QFont('Microsoft YaHei', 11, QFont.Weight.Bold))
        form.addRow(self.section4)

        self.autostart_check = QCheckBox('开机自动启动')
        form.addRow('', self.autostart_check)

        # === 快捷键 ===
        self.section5 = QLabel('快捷键')
        self.section5.setFont(QFont('Microsoft YaHei', 11, QFont.Weight.Bold))
        form.addRow(self.section5)

        self.shortcut_rows = []
        shortcuts_info = [
            ('Esc', '最小化到托盘'),
            ('Ctrl + Shift + H', '最小化到托盘'),
            ('Ctrl + Shift + S', '显示 / 隐藏切换'),
            ('Ctrl + W', '退出程序'),
            ('双击托盘图标', '恢复显示'),
        ]
        for key, desc in shortcuts_info:
            row = QHBoxLayout()
            key_label = QLabel(key)
            key_label.setFont(QFont('Consolas', 10))
            key_label.setFixedWidth(140)
            desc_label = QLabel(desc)
            desc_label.setFont(QFont('Microsoft YaHei', 10))
            row.addWidget(key_label)
            row.addWidget(desc_label)
            row.addStretch()
            form.addRow(row)
            self.shortcut_rows.append((key_label, desc_label))

        scroll.setWidget(self.form_widget)
        layout.addWidget(scroll, 1)

        # 底部按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.cancel_btn = QPushButton('取消')
        self.cancel_btn.setFont(QFont('Microsoft YaHei', 11))
        self.cancel_btn.setMinimumHeight(36)
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)

        self.save_btn = QPushButton('保存设置')
        self.save_btn.setFont(QFont('Microsoft YaHei', 11))
        self.save_btn.setMinimumHeight(36)
        self.save_btn.clicked.connect(self.save_settings)
        btn_layout.addWidget(self.save_btn)

        layout.addLayout(btn_layout)

    def showEvent(self, event):
        """每次显示前重新应用当前主题并刷新数据"""
        self.apply_theme()
        self.load_data()
        super().showEvent(event)

    def apply_theme(self):
        """应用当前主题到所有控件"""
        S = get_theme()

        self.setStyleSheet(f'''
            QDialog {{
                background-color: {S['bg']};
                color: {S['text_primary']};
            }}
            QLabel {{
                color: {S['text_primary']};
            }}
            QSpinBox, QComboBox, QLineEdit {{
                background-color: {S['bg_input']};
                border: 1px solid {S['border']};
                border-radius: 6px;
                padding: 4px 8px;
                color: {S['text_primary']};
                font-size: 12px;
                min-height: 30px;
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                background-color: {S['bg_card']};
                border: none;
                width: 20px;
            }}
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
                background-color: {S['border']};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 24px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {S['bg_card']};
                border: 1px solid {S['border']};
                color: {S['text_primary']};
                selection-background-color: {S['accent']};
                selection-color: {S['text_on_accent']};
            }}
            QCheckBox {{
                color: {S['text_secondary']};
                font-size: 12px;
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border-radius: 4px;
                border: 1px solid {S['border']};
                background-color: {S['bg_input']};
            }}
            QCheckBox::indicator:checked {{
                background-color: {S['accent']};
                border-color: {S['accent']};
            }}
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
        ''')

        self.form_widget.setStyleSheet(f'''
            QWidget {{
                background-color: {S['bg']};
            }}
        ''')

        self.title_label.setStyleSheet(f'color: {S["text_primary"]};')
        self.section1.setStyleSheet(f'color: {S["accent"]};')
        self.section2.setStyleSheet(f'color: {S["accent"]};')
        self.section3.setStyleSheet(f'color: {S["accent"]};')
        self.section4.setStyleSheet(f'color: {S["accent"]};')
        self.section5.setStyleSheet(f'color: {S["accent"]};')

        for key_label, desc_label in self.shortcut_rows:
            key_label.setStyleSheet(f'''
                color: {S['accent']};
                background-color: {S['bg_input']};
                border: 1px solid {S['border']};
                border-radius: 4px;
                padding: 3px 8px;
            ''')
            desc_label.setStyleSheet(f'color: {S["text_secondary"]};')

        self.cancel_btn.setStyleSheet(f'''
            QPushButton {{
                background-color: {S['bg']};
                color: {S['text_secondary']};
                font-size: 12px;
                padding: 8px 20px;
                border: 1px solid {S['border']};
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: {S['accent']};
                color: {S['text_on_accent']};
                border-color: {S['accent']};
            }}
        ''')

        self.save_btn.setStyleSheet(f'''
            QPushButton {{
                background-color: {S['accent']};
                color: {S['text_on_accent']};
                font-size: 12px;
                padding: 8px 24px;
                border: none;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: {S['accent_dim']};
            }}
        ''')

    def load_data(self):
        """加载配置数据到控件"""
        self.advance_spin.setValue(config.get('reminder_advance_minutes', 15))
        self.popup_check.setChecked(config.get('reminder_popup', True))
        self.sound_check.setChecked(config.get('reminder_sound', True))
        self.tray_check.setChecked(config.get('reminder_tray_flash', True))

        current_theme = config.get('theme', 'dark')
        self.theme_combo.setCurrentIndex(0 if current_theme == 'dark' else 1)

        self.wake_edit.setText(config.get('wake_up_time', '07:00'))
        self.evening_start_edit.setText(config.get('evening_study_start', '19:00'))
        self.evening_end_edit.setText(config.get('evening_study_end', '21:30'))

        self.autostart_check.setChecked(config.get('auto_start', False))

    def save_settings(self):
        from core.auto_start import set_auto_start

        config.set('reminder_advance_minutes', self.advance_spin.value())
        config.set('reminder_popup', self.popup_check.isChecked())
        config.set('reminder_sound', self.sound_check.isChecked())
        config.set('reminder_tray_flash', self.tray_check.isChecked())
        config.set('theme', 'dark' if self.theme_combo.currentIndex() == 0 else 'light')
        config.set('wake_up_time', self.wake_edit.text())
        config.set('evening_study_start', self.evening_start_edit.text())
        config.set('evening_study_end', self.evening_end_edit.text())

        auto_start = self.autostart_check.isChecked()
        config.set('auto_start', auto_start)

        if not set_auto_start(auto_start):
            QMessageBox.warning(self, '设置失败', '开机自启设置失败，请检查系统权限')
            return

        QMessageBox.information(self, '保存成功', '设置已保存')
        self.accept()
