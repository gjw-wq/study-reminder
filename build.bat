@echo off
chcp 936 >nul
title Study Reminder - Build Tool

rem ============================================================
rem  Study Reminder - One-Click Build Script v4.0
rem  Double-click this file to start packaging.
rem  All complex logic (env check / deps install / build)
rem  is handled by build.py (Python handles encoding properly).
rem ============================================================

rem Switch to script directory (works from any location)
cd /d "%~dp0"

echo.
echo ============================================================
echo   Study Reminder Build Tool v4.0
echo ============================================================
echo.

rem Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found in PATH
    echo Please install Python 3.12+ from https://www.python.org/
    echo and make sure "Add Python to PATH" is checked during install.
    echo.
    pause
    exit /b 1
)

echo Launching build process...
echo (all messages below are from build.py)
echo.
echo ============================================================
echo.

rem Call build.py (handles everything in Python with proper encoding)
python build.py

rem Capture exit code from build.py
set EXIT_CODE=%ERRORLEVEL%

echo.
if %EXIT_CODE%==0 (
    echo ============================================================
    echo   [SUCCESS] Build completed successfully
    echo ============================================================
) else (
    echo ============================================================
    echo   [ERROR] Build failed (exit code: %EXIT_CODE%)
    echo ============================================================
)
echo.
pause
exit /b %EXIT_CODE%
