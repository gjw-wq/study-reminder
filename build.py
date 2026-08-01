import os
import re
import shutil
import subprocess
import sys
import traceback

# 设置 Python 输出编码，确保在 Windows cmd/cp936 下中文正常显示
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(errors='replace')
        sys.stderr.reconfigure(errors='replace')
    except Exception:
        pass


# ============================================================
#  [0/6] 关键环境检查（防止 Anaconda/DLL 冲突）
# ============================================================
def check_environment():
    print('[0/6] 环境检查...')

    # 0.1 检查当前 Python 解释器路径
    python_path = sys.executable
    print(f'   Python 路径: {python_path}')

    # 0.2 检查是否在 Anaconda 环境
    anaconda_keywords = ['anaconda', 'miniconda', 'conda']
    if any(kw in python_path.lower() for kw in anaconda_keywords):
        print('\n   [!] 警告: 当前 Python 来自 Anaconda/conda 环境')
        print('   这会导致 PyQt6 DLL 加载失败，打包后在其他机器无法运行')
        print('\n   解决方案:')
        print('   1. 退出 conda: conda deactivate (执行两次)')
        print('   2. 用官网 Python 3.12+ 创建独立 venv')
        print('   3. 激活 venv 后重新运行本脚本')
        print('\n   不会在 conda 环境继续打包，以免产生坏产物')
        input('\n按回车键退出...')
        sys.exit(1)

    # 0.3 检查是否需要激活虚拟环境
    project_venv = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'venv', 'Scripts', 'python.exe')
    if os.path.exists(project_venv) and 'venv' not in python_path.lower():
        print('   发现项目 venv 目录但未激活，建议:')
        print(r'   venv\Scripts\activate 后重新运行本脚本')
        print()

    # 0.4 验证 PyQt6 DLL 能正确导入
    try:
        import PyQt6.QtWidgets
        import PyQt6.QtCore
        print('   [OK] PyQt6 DLL 检查通过')
    except ImportError as e:
        print(f'\n   [!] 警告: PyQt6 DLL 导入失败 ({e})')
        print('   尝试修复（用 --no-cache-dir 重新安装 PyQt6）...')
        try:
            subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '--no-cache-dir',
                 '--force-reinstall', 'PyQt6', 'PyQt6-Qt6', 'PyQt6-sip'],
                check=False
            )
            import PyQt6.QtWidgets
            import PyQt6.QtCore
            print('   [OK] PyQt6 DLL 重新验证通过')
        except Exception:
            print('\n   [ERROR] PyQt6 DLL 仍然无法导入！')
            print('\n   最终解决方案:')
            print('   1. 下载安装官网 Python 3.12+ (https://www.python.org/)')
            print('   2. 用它创建干净的 venv: python -m venv venv')
            print(r'   3. 激活 venv: venv\Scripts\activate')
            print('   4. 重新安装依赖: pip install --no-cache-dir PyQt6 Pillow pyinstaller')
            print('   5. 重新运行本脚本')
            input('\n按回车键退出...')
            sys.exit(1)

    print('   [OK] 环境检查完成')
    print()


# ============================================================
#  [1/6] 检查旧 exe 是否在运行（防止 PermissionError）
# ============================================================
def check_running_exe():
    print('[1/6] 检查旧打包产物是否在运行...')
    exe_path = os.path.join('dist', '学习纪律官.exe')

    if os.path.exists(exe_path):
        try:
            result = subprocess.run(
                ['tasklist', '/fi', 'imagename eq 学习纪律官.exe'],
                capture_output=True, text=True, encoding='gbk', errors='replace'
            )
            if '学习纪律官.exe' in result.stdout:
                print('   [!] 发现 dist\\学习纪律官.exe 正在运行！')
                print('   请先关闭程序，然后按任意键继续...')
                input()

                result2 = subprocess.run(
                    ['tasklist', '/fi', 'imagename eq 学习纪律官.exe'],
                    capture_output=True, text=True, encoding='gbk', errors='replace'
                )
                if '学习纪律官.exe' in result2.stdout:
                    print('   [ERROR] 程序仍在运行，无法继续')
                    print('   请手动关闭后重试')
                    input('按回车键退出...')
                    sys.exit(1)
        except Exception:
            pass

        print('   [OK] 确认程序未运行')
    else:
        print('   [OK] 无旧打包产物')

    print()


# ============================================================
#  [2/6] 清理旧的打包文件和 Python 缓存
# ============================================================
def clean_build_files():
    print('[2/6] 清理旧的打包文件和缓存...')
    dirs_to_remove = ['build', 'dist']

    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name, ignore_errors=True)

    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            shutil.rmtree(os.path.join(root, '__pycache__'), ignore_errors=True)
        for file in files:
            if file.endswith('.pyc') or file.endswith('.pyo'):
                try:
                    os.remove(os.path.join(root, file))
                except OSError:
                    pass

    print('   [OK] 清理完成')
    print()


# ============================================================
#  [3/6] 检查图标文件
# ============================================================
def ensure_icon():
    print('[3/6] 检查图标文件...')
    icon_path = os.path.join('icons', 'app.ico')

    if os.path.exists(icon_path):
        print('   [OK] 图标文件已存在')
    else:
        print('   图标文件不存在，尝试生成...')
        try:
            subprocess.run([sys.executable, 'generate_icon.py'], check=False)
            if os.path.exists(icon_path):
                print('   [OK] 图标生成成功')
            else:
                print('   [!] 图标生成失败，将使用默认图标')
        except Exception:
            print('   [!] 图标生成失败，将使用默认图标')

    print()


# ============================================================
#  [4/6] 检查并安装依赖
# ============================================================
def install_dependencies():
    print('[4/6] 检查并安装依赖...')

    packages = [
        ('PyInstaller', 'pyinstaller>=6.0.0'),
        ('PyQt6', 'PyQt6>=6.0.0'),
        ('PIL', 'Pillow>=9.0.0'),
    ]

    for import_name, pip_name in packages:
        try:
            __import__(import_name)
            print(f'   [OK] {pip_name.split(">")[0]} 已安装')
        except ImportError:
            print(f'   正在安装 {pip_name}...')
            try:
                # 不用 capture_output，让用户看到安装进度
                result = subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', '--no-cache-dir', pip_name],
                    check=False
                )
                if result.returncode == 0:
                    print(f'   [OK] {pip_name.split(">")[0]} 安装完成')
                else:
                    print(f'   [ERROR] {pip_name.split(">")[0]} 安装失败，请手动安装')
            except Exception as e:
                print(f'   [ERROR] 安装过程出错: {e}')

    print()


# ============================================================
#  [5/6] 选择打包模式并更新 spec 文件
# ============================================================
def update_spec_file(use_upx, include_debug):
    spec_path = '学习纪律官.spec'

    if not os.path.exists(spec_path):
        print('   [ERROR] spec 文件不存在，无法继续')
        return False

    with open(spec_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 用正则替换，比简单 replace 更可靠（支持任意空格）
    content = re.sub(
        r'upx\s*=\s*(True|False)',
        f'upx={"True" if use_upx else "False"}',
        content
    )
    content = re.sub(
        r'console\s*=\s*(True|False)',
        f'console={"True" if include_debug else "False"}',
        content
    )

    with open(spec_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'   [OK] spec 文件已更新 (upx={use_upx}, console={include_debug})')
    return True


# ============================================================
#  [6/6] 执行打包
# ============================================================
def run_pyinstaller():
    print('\n[6/6] 开始打包，请稍候... (可能需要 1-3 分钟)')
    print('=' * 60)
    print()

    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--noconfirm', '--clean',
        '学习纪律官.spec'
    ]

    try:
        # 直接运行，不捕获 stdout/stderr，让用户看到实时输出
        result = subprocess.run(cmd, check=False)
        return result.returncode == 0
    except Exception as e:
        print(f'   [ERROR] 执行失败: {e}')
        traceback.print_exc()
        return False


# ============================================================
#  验证打包产物
# ============================================================
def verify_build():
    exe_path = os.path.join('dist', '学习纪律官.exe')

    if os.path.exists(exe_path):
        size_bytes = os.path.getsize(exe_path)
        size_mb = size_bytes / (1024 * 1024)

        print()
        print('=' * 60)
        print('[SUCCESS] 打包完成！')
        print('=' * 60)
        print()
        print(f'[FILE] 可执行文件位置: {os.path.abspath(exe_path)}')
        print(f'[SIZE] 文件大小: {size_mb:.1f} MB')
        print()
        print('[NOTE] 使用说明:')
        print('   - 首次运行会在同目录创建 data 文件夹')
        print('   - 拷贝 dist\\学习纪律官.exe 到任意 Windows 机器即可运行')
        print('   - 如需迁移用户数据: 把 data 文件夹一并拷贝')
        print('   - 若其他机器运行失败: 请用"完整兼容模式"重新打包')
        print()
        return True
    else:
        print()
        print('=' * 60)
        print('[ERROR] 打包失败！')
        print('=' * 60)
        print()
        print('常见问题及解决方案:')
        print('   1. DLL 加载失败: 当前环境是 Anaconda，请退出 conda 并用官网 Python 重建 venv')
        print('   2. PermissionError (权限不足): dist\\学习纪律官.exe 正在运行，请先关闭')
        print('   3. NameError (__file__ 未定义): spec 文件已修复，请勿手动修改标记行')
        print('   4. collect_binaries 错误: 已改用 collect_all，如仍报错请删除 venv 重建')
        print('   5. 内存不足: 关闭其他程序后重试')
        print('   6. 依赖缺失: 执行 pip install --no-cache-dir -r requirements.txt')
        print()
        return False


# ============================================================
#  主流程
# ============================================================
def main():
    print('=' * 60)
    print('     学习纪律官 - 打包工具 v4.0')
    print('     完整兼容版 - 保证即插即用')
    print('=' * 60)
    print()

    try:
        check_environment()
        check_running_exe()
        clean_build_files()
        ensure_icon()
        install_dependencies()

        print('[5/6] 选择打包模式:')
        print('   1) 完整兼容模式 (约 90MB，无 UPX 压缩，最佳兼容性，推荐分发)')
        print('   2) 标准压缩模式 (约 30MB，UPX 压缩，可能导致某些机器 DLL 加载失败)')
        print('   3) 调试模式 (带控制台窗口，用于排查打包后问题)')
        print()

        while True:
            try:
                choice = input('   请选择 [1-3]: ').strip()
            except (EOFError, KeyboardInterrupt):
                print('\n   取消操作')
                sys.exit(0)

            if choice == '1':
                use_upx, include_debug = False, False
                print('   选择: 完整兼容模式')
                break
            elif choice == '2':
                use_upx, include_debug = True, False
                print('   选择: 标准压缩模式')
                break
            elif choice == '3':
                use_upx, include_debug = False, True
                print('   选择: 调试模式')
                break
            else:
                print('   请输入有效数字 (1-3)')

        print()
        update_spec_file(use_upx, include_debug)
        print()

        success = run_pyinstaller()
        build_ok = verify_build()

        print()
        input('按回车键退出...')
        sys.exit(0 if build_ok else 1)

    except SystemExit:
        raise
    except Exception as e:
        print(f'\n   [ERROR] 发生异常: {e}')
        traceback.print_exc()
        print()
        input('按回车键退出...')
        sys.exit(1)


if __name__ == '__main__':
    main()
