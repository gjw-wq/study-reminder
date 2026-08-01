import threading
import time
from datetime import datetime, timedelta
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from .database import db
from .config import config
from .course_data import DAILY_ROUTINE

class ReminderEngine(QObject):
    reminder_triggered = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_reminders)
        self.timer.start(30000)  # 每30秒检查一次
        self.triggered_today = set()
        self.last_check_date = datetime.now().date()
    
    def check_reminders(self):
        now = datetime.now()
        today = now.date()
        
        # 新的一天，重置触发记录
        if today != self.last_check_date:
            self.triggered_today.clear()
            self.last_check_date = today
        
        current_time = now.strftime('%H:%M')
        today_str = today.strftime('%Y-%m-%d')
        
        # 检查课程提醒
        self._check_course_reminders(today_str, current_time, now)
        
        # 检查作息提醒
        self._check_routine_reminders(current_time)
        
        # 检查晚自习结束复盘提醒
        self._check_evening_review(today_str, current_time)
    
    def _check_course_reminders(self, today_str, current_time, now):
        advance = config.get('reminder_advance_minutes', 15)
        courses = db.get_courses_by_date(today_str)
        
        for course in courses:
            if course[8]:  # is_rest
                continue
            
            start_time = course[5]  # start_time
            course_type = course[4]  # course_type
            is_self_study = course[9] if len(course) > 9 else False
            if not start_time:
                continue
            
            # 计算提醒时间
            course_dt = datetime.strptime(f"{today_str} {start_time}", '%Y-%m-%d %H:%M')
            reminder_dt = course_dt - timedelta(minutes=advance)
            reminder_time = reminder_dt.strftime('%H:%M')
            
            reminder_key = f"course_{course[0]}_{reminder_time}"
            if current_time == reminder_time and reminder_key not in self.triggered_today:
                self.triggered_today.add(reminder_key)
                
                if is_self_study:
                    description = f'自习时间到！请自觉学习，每隔一小时休息10分钟'
                elif course_type == 'lecture':
                    description = f'讲师课程即将开始，请准备好笔记本和学习用品'
                elif course_type == 'self_study':
                    description = f'自习时间到！请自觉学习，每隔一小时休息10分钟'
                else:
                    description = f'课程即将开始，请做好准备'
                
                self.reminder_triggered.emit({
                    'type': 'course',
                    'title': course[3],  # title
                    'time': start_time,
                    'description': description,
                    'priority': 'normal'
                })
    
    def _check_routine_reminders(self, current_time):
        for routine in DAILY_ROUTINE:
            reminder_key = f"routine_{routine['time']}"
            if current_time == routine['time'] and reminder_key not in self.triggered_today:
                self.triggered_today.add(reminder_key)
                self.reminder_triggered.emit({
                    'type': routine['type'],
                    'title': routine['title'],
                    'time': routine['time'],
                    'description': routine['description'],
                    'priority': 'low' if routine['type'] == 'routine' else 'normal'
                })
    
    def _check_evening_review(self, today_str, current_time):
        evening_end = config.get('evening_study_end', '22:30')
        if current_time == evening_end:
            reminder_key = f"evening_review_{today_str}"
            if reminder_key not in self.triggered_today:
                self.triggered_today.add(reminder_key)
                self.reminder_triggered.emit({
                    'type': 'review',
                    'title': '每日学习复盘',
                    'time': evening_end,
                    'description': '晚自习结束了！请完成今日学习复盘：1. 今日学到了什么？2. 有哪些问题需要解决？3. 明日学习计划是什么？',
                    'priority': 'high'
                })
    
    def get_next_reminder(self):
        """获取下一个即将到来的提醒"""
        now = datetime.now()
        today_str = now.strftime('%Y-%m-%d')
        current_time = now.strftime('%H:%M')
        
        # 收集所有未来的提醒
        future_reminders = []
        
        # 课程提醒
        advance = config.get('reminder_advance_minutes', 15)
        courses = db.get_courses_by_date(today_str)
        for course in courses:
            if course[8]:  # is_rest
                continue
            start_time = course[5]
            if start_time:
                course_dt = datetime.strptime(f"{today_str} {start_time}", '%Y-%m-%d %H:%M')
                reminder_dt = course_dt - timedelta(minutes=advance)
                if reminder_dt > now:
                    future_reminders.append({
                        'type': 'course',
                        'title': course[3],
                        'time': reminder_dt,
                        'original_time': start_time
                    })
        
        # 作息提醒
        for routine in DAILY_ROUTINE:
            routine_dt = datetime.strptime(f"{today_str} {routine['time']}", '%Y-%m-%d %H:%M')
            if routine_dt > now:
                future_reminders.append({
                    'type': routine['type'],
                    'title': routine['title'],
                    'time': routine_dt,
                    'original_time': routine['time']
                })
        
        if future_reminders:
            future_reminders.sort(key=lambda x: x['time'])
            return future_reminders[0]
        return None
