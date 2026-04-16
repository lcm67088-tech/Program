@echo off
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 pip install pyinstaller

if exist build rmdir /s /q build

pyinstaller --onefile --noconsole --name=dev_launcher dev_launcher.py

if errorlevel 1 (
    echo Build failed!
    pause
    exit /b 1
)

echo Done! dist\dev_launcher.exe
pause
