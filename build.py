import os
import shutil
import subprocess
import sys

def update_spec_file(use_upx, include_debug):
    """
    根据用户选择更新 spec 文件中的配置
    """
    spec_path = '学习纪律官.spec'
    if not os.path.exists(spec_path):
        return
    
    with open(spec_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新 UPX 设置
    if use_upx:
        content = content.replace('upx=False', 'upx=True')
        content = content.replace('# upx=True', 'upx=True')
    else:
        content = content.replace('upx=True', 'upx=False')
        content = content.replace('# upx=False', 'upx=False')
    
    # 更新 console 设置
    if include_debug:
        content = content.replace('console=False', 'console=True')
        content = content.replace('# console=True', 'console=True')
    else:
        content = content.replace('console=True', 'console=False')
        content = content.replace('# console=False', 'console=False')
    
    with open(spec_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'   ✓ 更新 spec 文件: UPX={use_upx}, console={include_debug}')

def build_with_options(use_upx=True, include_debug=False):
    """
    执行 PyInstaller 打包
    
    参数:
        use_upx: 是否使用 UPX 压缩 (默认 True，体积约30M；False时约90M)
        include_debug: 是否包含调试信息
    """
    print(f"\n[打包配置] UPX压缩: {'启用' if use_upx else '禁用'}, 调试信息: {'包含' if include_debug else '不包含'}")
    
    # 根据配置更新 spec 文件
    update_spec_file(use_upx, include_debug)
    
    # 构建命令（使用 spec 文件时不能在命令行指定 --onefile/--windowed 等参数）
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--noconfirm',
        '--clean',
        '学习纪律官.spec'
    ]
    
    print(f"\n执行命令: {' '.join(cmd)}")
    print()
    
    # 使用 gbk 编码处理 Windows 命令行输出
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='gbk', errors='replace')
    
    if result.stdout:
        # 只显示最后3000字符
        output = result.stdout[-3000:] if len(result.stdout) > 3000 else result.stdout
        print(output)
    
    if result.stderr:
        stderr_output = result.stderr[-1500:] if len(result.stderr) > 1500 else result.stderr
        if 'error' in stderr_output.lower() or 'exception' in stderr_output.lower():
            print('STDERR:', stderr_output)
    
    return result.returncode == 0

def main():
    print('=' * 50)
    print('     学习纪律官 - 打包工具 v2.0')
    print('=' * 50)
    print()
    
    # [1/5] 清理旧文件
    print('[1/5] 清理旧的打包文件...')
    if os.path.exists('build'):
        shutil.rmtree('build', ignore_errors=True)
        print('   ✓ 删除 build 目录')
    if os.path.exists('dist'):
        shutil.rmtree('dist', ignore_errors=True)
        print('   ✓ 删除 dist 目录')
    print()
    
    # [2/5] 清理缓存
    print('[2/5] 清理 Python 缓存...')
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            shutil.rmtree(os.path.join(root, '__pycache__'), ignore_errors=True)
    print('   ✓ 缓存清理完成')
    print()
    
    # [3/5] 检查 PyInstaller
    print('[3/5] 检查 PyInstaller...')
    try:
        import PyInstaller
        print(f'   ✓ PyInstaller {PyInstaller.__version__} 已安装')
    except ImportError:
        print('   安装 PyInstaller...')
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
        print('   ✓ 安装完成')
    print()
    
    # [4/5] 选择打包模式
    print('[4/5] 选择打包模式:')
    print('   1) 完整兼容模式 (约90MB，无压缩，最佳兼容性)')
    print('   2) 标准压缩模式 (约30MB，UPX压缩，推荐)')
    print('   3) 调试模式 (带控制台窗口，用于调试)')
    
    while True:
        try:
            choice = input('   请选择 [1-3]: ')
            if choice in ['1', '2', '3']:
                break
            print('   请输入有效数字 (1-3)')
        except KeyboardInterrupt:
            print('\n   取消操作')
            sys.exit(0)
    
    print()
    print('[5/5] 开始打包...')
    print('=' * 50)
    
    success = False
    if choice == '1':
        success = build_with_options(use_upx=False, include_debug=False)
    elif choice == '2':
        success = build_with_options(use_upx=True, include_debug=False)
    elif choice == '3':
        success = build_with_options(use_upx=False, include_debug=True)
    
    print('=' * 50)
    if success:
        exe_path = os.path.join('dist', '学习纪律官.exe')
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f'\n✅ 打包成功！')
            print(f'   文件位置: {exe_path}')
            print(f'   文件大小: {size_mb:.1f} MB')
            print()
            print('📝 使用说明:')
            print('   - 首次运行会在同目录创建 data 文件夹')
            print('   - 若出现"找不到模块"错误，请使用完整兼容模式重新打包')
    else:
        print('\n❌ 打包失败！')
        print('   请检查错误信息并尝试解决')
    
    print()
    input('按回车键退出...')

if __name__ == '__main__':
    main()
