@echo off
cd /d "%~dp0"

echo ========================================
echo       TRAVORA - FLASK + MYSQL
echo ========================================

where py >nul 2>&1
if %errorlevel%==0 (
    py -m pip install -r requirements.txt
    start "Travora Flask Server" cmd /k "py app.py"
) else (
    where python >nul 2>&1
    if %errorlevel%==0 (
        python -m pip install -r requirements.txt
        start "Travora Flask Server" cmd /k "python app.py"
    ) else (
        echo Python is not installed or not available in PATH.
        pause
        exit /b
    )
)

timeout /t 3 >nul
start http://127.0.0.1:5000/
