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

        # 检查数据库文件是否已存在且包含数据：有则直接使用，不重新初始化
        if self._db_has_data():
            # 已有数据库，仅确保表结构存在（CREATE TABLE IF NOT EXISTS 不会破坏数据）
            self.init_tables(skip_if_exists=True)
        else:
            # 全新数据库：创建表结构
            self.init_tables(skip_if_exists=False)

    def _db_has_data(self):
        """检查数据库文件是否已存在且包含有效数据（courses 或 habit_checks 非空）"""
        if not os.path.exists(self.db_path):
            return False
        # 文件存在但可能是空文件（0 字节），也视为无数据
        if os.path.getsize(self.db_path) == 0:
            return False
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            # 检查是否存在 courses 或 habit_checks 表且有数据
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('courses', 'habit_checks', 'study_logs')")
            tables = [r[0] for r in cursor.fetchall()]
            if not tables:
                conn.close()
                return False
            # 任意一个表有数据就认为是有数据的数据库
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                if cursor.fetchone()[0] > 0:
                    conn.close()
                    return True
            conn.close()
            return False
        except Exception:
            return False
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_tables(self, skip_if_exists=False):
        """初始化数据库表结构

        参数:
            skip_if_exists: 如果为 True，且数据库已包含 app_meta.initial_completed='1'，
                           则跳过表结构检查（极大减少对已有数据的任何写入操作）。
                           如果为 False，则执行 CREATE TABLE IF NOT EXISTS 创建表。
        """
        # 如果数据库已有数据且已标记为初始化完成，则完全跳过，不做任何修改
        if skip_if_exists:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT value FROM app_meta WHERE key = 'initial_completed'")
                row = cursor.fetchone()
                conn.close()
                if row and row[0] == '1':
                    return  # 已完成初始化，直接返回，不做任何写入
            except Exception:
                pass  # app_meta 可能不存在，继续执行创建

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

    def get_db_path(self):
        """返回当前数据库文件路径，便于排查问题"""
        return self.db_path
    
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
