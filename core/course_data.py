# 黑马程序员AI大模型就业6期课程表数据
# 根据用户提供的课表图片精确整理
# 日期范围: 2026-06-15 至 2026-06-28

COURSE_SCHEDULE = [
    # === 第一周 ===
    # 6月15日 星期一 — 休息
    {'date': '2026-06-15', 'weekday': '星期一', 'title': '休息', 'course_type': 'rest', 'is_rest': 1},
    
    # 6月16日 星期二 — 大模型开发入门V6.0
    {'date': '2026-06-16', 'weekday': '星期二', 'title': '大模型开发入门V6.0', 'course_type': 'lecture', 'start_time': '09:00', 'end_time': '12:00'},
    {'date': '2026-06-16', 'weekday': '星期二', 'title': '大模型开发入门V6.0', 'course_type': 'lecture', 'start_time': '14:00', 'end_time': '18:00'},
    
    # 6月17日 星期三 — 大模型开发入门V6.0
    {'date': '2026-06-17', 'weekday': '星期三', 'title': '大模型开发入门V6.0', 'course_type': 'lecture', 'start_time': '09:00', 'end_time': '12:00'},
    {'date': '2026-06-17', 'weekday': '星期三', 'title': '大模型开发入门V6.0', 'course_type': 'lecture', 'start_time': '14:00', 'end_time': '18:00'},
    
    # 6月18日 星期四 — 休息
    {'date': '2026-06-18', 'weekday': '星期四', 'title': '休息', 'course_type': 'rest', 'is_rest': 1},
    
    # 6月19日 星期五 — 端午休息
    {'date': '2026-06-19', 'weekday': '星期五', 'title': '端午休息', 'course_type': 'rest', 'is_rest': 1},
    
    # 6月20日 星期六 — 大模型开发入门V6.0
    {'date': '2026-06-20', 'weekday': '星期六', 'title': '大模型开发入门V6.0', 'course_type': 'lecture', 'start_time': '09:00', 'end_time': '12:00'},
    {'date': '2026-06-20', 'weekday': '星期六', 'title': '大模型开发入门V6.0', 'course_type': 'lecture', 'start_time': '14:00', 'end_time': '18:00'},
    
    # 6月21日 星期日 — 大模型开发入门V6.0
    {'date': '2026-06-21', 'weekday': '星期日', 'title': '大模型开发入门V6.0', 'course_type': 'lecture', 'start_time': '09:00', 'end_time': '12:00'},
    {'date': '2026-06-21', 'weekday': '星期日', 'title': '大模型开发入门V6.0', 'course_type': 'lecture', 'start_time': '14:00', 'end_time': '18:00'},
    
    # === 第二周 ===
    # 6月22日 星期一 — 自习
    {'date': '2026-06-22', 'weekday': '星期一', 'title': '自习', 'course_type': 'self_study', 'is_self_study': 1, 'start_time': '09:00', 'end_time': '18:00'},
    
    # 6月23日 星期二 — 大模型开发入门V6.0
    {'date': '2026-06-23', 'weekday': '星期二', 'title': '大模型开发入门V6.0', 'course_type': 'lecture', 'start_time': '09:00', 'end_time': '12:00'},
    {'date': '2026-06-23', 'weekday': '星期二', 'title': '大模型开发入门V6.0', 'course_type': 'lecture', 'start_time': '14:00', 'end_time': '18:00'},
    
    # 6月24日 星期三 — 大模型开发入门V6.0
    {'date': '2026-06-24', 'weekday': '星期三', 'title': '大模型开发入门V6.0', 'course_type': 'lecture', 'start_time': '09:00', 'end_time': '12:00'},
    {'date': '2026-06-24', 'weekday': '星期三', 'title': '大模型开发入门V6.0', 'course_type': 'lecture', 'start_time': '14:00', 'end_time': '18:00'},
    
    # 6月25日 星期四 — 休息
    {'date': '2026-06-25', 'weekday': '星期四', 'title': '休息', 'course_type': 'rest', 'is_rest': 1},
    
    # 6月26日 星期五 — 大模型开发入门V6.0
    {'date': '2026-06-26', 'weekday': '星期五', 'title': '大模型开发入门V6.0', 'course_type': 'lecture', 'start_time': '09:00', 'end_time': '12:00'},
    {'date': '2026-06-26', 'weekday': '星期五', 'title': '大模型开发入门V6.0', 'course_type': 'lecture', 'start_time': '14:00', 'end_time': '18:00'},
    
    # 6月27日 星期六 — 大模型开发入门V6.0
    {'date': '2026-06-27', 'weekday': '星期六', 'title': '大模型开发入门V6.0', 'course_type': 'lecture', 'start_time': '09:00', 'end_time': '12:00'},
    {'date': '2026-06-27', 'weekday': '星期六', 'title': '大模型开发入门V6.0', 'course_type': 'lecture', 'start_time': '14:00', 'end_time': '18:00'},
    
    # 6月28日 星期日 — 自习
    {'date': '2026-06-28', 'weekday': '星期日', 'title': '自习', 'course_type': 'self_study', 'is_self_study': 1, 'start_time': '09:00', 'end_time': '18:00'},
]

# 课程模块完整列表（课表右侧列表）
COURSE_MODULES = [
    '大模型开发入门V6.0',
    '大模型语言进阶V4.0',
    '智能体开发（Coze+Dify）',
    '大模型核心开发技术（ML）',
    '大模型核心开发技术（Transformer）',
    'NewsCompass投满分项目',
    'LangChain',
    'RAG项目',
    '智能体项目1',
    '智能体项目2',
    '大模型开发进阶V6.0-智能体实战',
    '大模型核心运行机制',
    '大模型微调开发',
    '计算机视觉基础',
    '多模态大模型'
]

# 作息提醒时间点
DAILY_ROUTINE = [
    {'time': '07:00', 'title': '起床时间', 'type': 'routine', 'description': '拒绝睡懒觉，新的一天开始！'},
    {'time': '08:30', 'title': '晨检打卡', 'type': 'routine', 'description': '准备上课，检查学习用品'},
    {'time': '09:00', 'title': '上午课程开始', 'type': 'course_start', 'description': '集中精力，抓住重点'},
    {'time': '12:00', 'title': '午休时间', 'type': 'routine', 'description': '适当休息，为下午充电'},
    {'time': '14:00', 'title': '下午课程开始', 'type': 'course_start', 'description': '保持专注，善于总结'},
    {'time': '18:00', 'title': '晚自习准备', 'type': 'routine', 'description': '整理白天所学，准备晚自习'},
    {'time': '19:00', 'title': '晚自习开始', 'type': 'evening_start', 'description': '拒绝晚自习下课即跑'},
    {'time': '21:30', 'title': '晚自习结束', 'type': 'evening_end', 'description': '完成今日复盘，记录收获'},
    {'time': '23:00', 'title': '就寝提醒', 'type': 'routine', 'description': '保证睡眠，明日再战'},
]

COURSE_DATA_VERSION = '2026-06-v1'


def init_course_data(db):
    """初始化课程表数据到数据库（幂等：已有数据不会重复导入）"""
    conn = db.get_connection()
    cursor = conn.cursor()

    # 检查当前数据版本
    cursor.execute("SELECT value FROM app_meta WHERE key = 'course_data_version'")
    row = cursor.fetchone()

    if row and row[0] == COURSE_DATA_VERSION:
        conn.close()
        return  # 已是最新版本，跳过初始化

    # 版本不匹配或首次启动：清空旧数据并重新导入
    cursor.execute('DELETE FROM courses')
    for course in COURSE_SCHEDULE:
        cursor.execute('''
            INSERT INTO courses
            (date, weekday, title, course_type, start_time, end_time, description, is_rest, is_self_study)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            course.get('date'), course.get('weekday'), course.get('title'),
            course.get('course_type', 'lecture'), course.get('start_time'),
            course.get('end_time'), course.get('description'),
            course.get('is_rest', 0), course.get('is_self_study', 0)
        ))

    # 记录版本号
    cursor.execute(
        "INSERT OR REPLACE INTO app_meta (key, value) VALUES (?, ?)",
        ('course_data_version', COURSE_DATA_VERSION)
    )

    conn.commit()
    conn.close()
