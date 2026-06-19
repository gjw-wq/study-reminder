@echo off
chcp 65001 >nul
echo ====================================
echo       学习纪律官 - 一键打包脚本
echo ====================================
echo.

echo [1/5] 检查并清理旧的打包文件...
if exist "build" (
    echo   正在删除 build 目录...
    rmdir /s /q "build" 2>nul
)
if exist "dist" (
    echo   正在删除 dist 目录...
    rmdir /s /q "dist" 2>nul
)
echo   清理完成！
echo.

echo [2/5] 清理 Python 缓存文件...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d" 2>nul
echo   缓存清理完成！
echo.

echo [3/5] 检查 PyInstaller 是否安装...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo   PyInstaller 未安装，正在安装...
    pip install pyinstaller
) else (
    echo   PyInstaller 已安装
)
echo.

echo [4/5] 开始打包...
echo   正在使用 PyInstaller 打包项目，这可能需要 1-3 分钟...
echo.

python -m PyInstaller --noconfirm --clean "学习纪律官.spec"

if errorlevel 1 (
    echo.
    echo [ERROR] 打包失败！
    echo.
    pause
    exit /b 1
)

echo.
echo [5/5] 打包完成！
echo ====================================
echo.
echo 可执行文件位置: dist\学习纪律官.exe
echo.
echo 提示: 首次运行会在同目录创建 data 文件夹，
echo       用于存储课程数据和用户配置。
echo.
pause
