import sqlite3
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path


def get_app_dir():
    """获取应用数据目录（打包后为exe所在目录，开发时为项目根目录）"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Database:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.join(get_app_dir(), 'data', 'study_reminder.db')
        self.db_path = str(db_path)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_tables()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 课程表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                weekday TEXT NOT NULL,
                title TEXT NOT NULL,
                course_type TEXT DEFAULT 'lecture',
                start_time TEXT,
                end_time TEXT,
                description TEXT,
                is_rest INTEGER DEFAULT 0,
                is_self_study INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 习惯打卡
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habit_checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_name TEXT NOT NULL,
                habit_index INTEGER NOT NULL,
                check_date TEXT NOT NULL,
                checked INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(habit_index, check_date)
            )
        ''')
        
        # 学习日志（复盘）
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS study_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                log_date TEXT NOT NULL UNIQUE,
                gain1 TEXT,
                gain2 TEXT,
                gain3 TEXT,
                question TEXT,
                courses_today TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 提醒记录
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reminder_type TEXT NOT NULL,
                title TEXT NOT NULL,
                trigger_time TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 应用元数据（用于版本控制，避免数据被重复初始化）
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_meta (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')

        conn.commit()
        conn.close()
    
    def insert_course(self, date, weekday, title, course_type='lecture', 
                      start_time=None, end_time=None, description=None,
                      is_rest=0, is_self_study=0):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO courses 
            (date, weekday, title, course_type, start_time, end_time, description, is_rest, is_self_study)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (date, weekday, title, course_type, start_time, end_time, description, is_rest, is_self_study))
        conn.commit()
        conn.close()
    
    def get_courses_by_date(self, date):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM courses WHERE date = ? ORDER BY start_time', (date,))
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def get_all_courses(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM courses ORDER BY date, start_time')
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def check_habit(self, habit_index, habit_name, check_date, checked=1):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO habit_checks (habit_index, habit_name, check_date, checked)
            VALUES (?, ?, ?, ?)
        ''', (habit_index, habit_name, check_date, checked))
        conn.commit()
        conn.close()
    
    def get_habit_status(self, check_date):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT habit_index, habit_name, checked FROM habit_checks 
            WHERE check_date = ?
        ''', (check_date,))
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def get_streak(self, habit_index):
        conn = self.get_connection()
        cursor = conn.cursor()
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT check_date FROM habit_checks 
            WHERE habit_index = ? AND checked = 1 AND check_date <= ?
            ORDER BY check_date DESC
        ''', (habit_index, today))
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return 0
        
        streak = 0
        check_date = datetime.strptime(today, '%Y-%m-%d')
        for row in rows:
            row_date = datetime.strptime(row[0], '%Y-%m-%d')
            if (check_date - row_date).days == streak:
                streak += 1
            else:
                break
        return streak
    
    def save_study_log(self, log_date, gain1, gain2, gain3, question, courses_today):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO study_logs 
            (log_date, gain1, gain2, gain3, question, courses_today)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (log_date, gain1, gain2, gain3, question, courses_today))
        conn.commit()
        conn.close()
    
    def get_study_log(self, log_date):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM study_logs WHERE log_date = ?', (log_date,))
        row = cursor.fetchone()
        conn.close()
        return row
    
    def get_week_stats(self, start_date, end_date):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 打卡统计
        cursor.execute('''
            SELECT check_date, COUNT(*) as count FROM habit_checks 
            WHERE check_date BETWEEN ? AND ? AND checked = 1
            GROUP BY check_date
        ''', (start_date, end_date))
        habit_stats = cursor.fetchall()
        
        # 日志统计
        cursor.execute('''
            SELECT COUNT(*) FROM study_logs 
            WHERE log_date BETWEEN ? AND ?
        ''', (start_date, end_date))
        log_count = cursor.fetchone()[0]
        
        conn.close()
        return {'habit_stats': habit_stats, 'log_count': log_count}

# 全局数据库实例
db = Database()
