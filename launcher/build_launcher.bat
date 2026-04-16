@echo off
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found!
    pause
    exit /b 1
)

python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    pip install pyinstaller
)

if exist build rmdir /s /q build

pyinstaller --onefile --noconsole --name=launcher launcher.py

if errorlevel 1 (
    echo Build failed!
    pause
    exit /b 1
)

echo Done! dist\launcher.exe
pause
