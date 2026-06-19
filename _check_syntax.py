import py_compile
import os
import sys

project_root = os.path.dirname(os.path.abspath(__file__))
files_to_check = []

files_to_check.append(os.path.join(project_root, 'main.py'))

core_dir = os.path.join(project_root, 'core')
for f in os.listdir(core_dir):
    if f.endswith('.py'):
        files_to_check.append(os.path.join(core_dir, f))

ui_dir = os.path.join(project_root, 'ui')
for f in os.listdir(ui_dir):
    if f.endswith('.py'):
        files_to_check.append(os.path.join(ui_dir, f))

print('=== Python 语法检查 ===')
errors = 0
for filepath in files_to_check:
    rel_path = os.path.relpath(filepath, project_root)
    try:
        py_compile.compile(filepath, doraise=True)
        print(f'  OK   {rel_path}')
    except py_compile.PyCompileError as e:
        print(f'  FAIL {rel_path}')
        print(f'       {e}')
        errors += 1

print()
if errors == 0:
    print('=== 所有文件语法检查通过 ===')
    sys.exit(0)
else:
    print(f'=== 发现 {errors} 个语法错误 ===')
    sys.exit(1)
