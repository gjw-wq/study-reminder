"""
执行 SQL 脚本更新数据库

用法:
    python run_sql.py                    # 使用默认路径（1.sql -> data/study_reminder.db）
    python run_sql.py 2.sql              # 指定 SQL 文件
    python run_sql.py 2.sql dist/data/study_reminder.db  # 指定 SQL 文件和数据库路径
"""
import sqlite3
import os
import sys
import argparse

# 设置输出编码为 UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def execute_sql(sql_file, db_path):
    """执行 SQL 文件更新数据库"""
    # 检查 SQL 文件是否存在
    if not os.path.exists(sql_file):
        print(f"错误: SQL 文件不存在: {sql_file}")
        return False

    # 检查数据库目录是否存在
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
        print(f"创建数据库目录: {db_dir}")

    # 读取 SQL 文件
    try:
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        print(f"读取 SQL 文件: {sql_file}")
    except Exception as e:
        print(f"读取 SQL 文件失败: {e}")
        return False

    # 连接数据库并执行
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.executescript(sql_script)
        conn.commit()
        print("数据库更新成功！")

        # 查询课程总数
        cursor.execute("SELECT COUNT(*) FROM courses")
        total_count = cursor.fetchone()[0]
        print(f"课程表总记录数: {total_count}")

        # 查询日期范围
        cursor.execute("SELECT MIN(date), MAX(date) FROM courses")
        min_date, max_date = cursor.fetchone()
        if min_date and max_date:
            print(f"课程日期范围: {min_date} 至 {max_date}")

        return True

    except Exception as e:
        conn.rollback()
        print(f"更新失败: {e}")
        return False
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(
        description='执行 SQL 脚本更新数据库',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python run_sql.py                                    # 使用默认路径
  python run_sql.py 2.sql                              # 指定 SQL 文件
  python run_sql.py 1.sql dist/data/study_reminder.db  # 指定 SQL 和数据库
        """
    )
    parser.add_argument('sql_file', nargs='?', default='1.sql',
                        help='SQL 文件路径（默认: 1.sql）')
    parser.add_argument('db_path', nargs='?',
                        default=os.path.join('data', 'study_reminder.db'),
                        help='数据库文件路径（默认: data/study_reminder.db）')

    args = parser.parse_args()

    # 检查参数是否看起来像数据库文件（.db 或 .sqlite）
    if args.sql_file.endswith(('.db', '.sqlite', '.sqlite3')):
        print(f"警告: 第一个参数 '{args.sql_file}' 看起来像数据库文件")
        print(f"正确用法: python run_sql.py <SQL文件> <数据库文件>")
        print(f"例如: python run_sql.py 1.sql dist/data/study_reminder.db")
        response = input("是否继续？(y/n): ")
        if response.lower() != 'y':
            return

    print("=" * 50)
    print(f"SQL 文件: {args.sql_file}")
    print(f"数据库: {args.db_path}")
    print("=" * 50)

    success = execute_sql(args.sql_file, args.db_path)

    if success:
        print("\n执行完成！")
        sys.exit(0)
    else:
        print("\n执行失败！")
        sys.exit(1)


if __name__ == '__main__':
    main()