@echo off
setlocal

echo.
echo ============================================================
echo  messenger_allInOne - Dependency Installer
echo ============================================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed.
    echo.
    echo  Please install Python 3.11 from:
    echo  https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
    echo.
    echo  IMPORTANT: Check "Add python.exe to PATH" during install.
    echo.
    pause
    exit /b 1
)

python --version
echo.

:: Upgrade pip
echo [1/4] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo      Done.
echo.

:: Install required packages
echo [2/4] Installing required packages... (requirements.txt)
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install required packages.
    echo         Please check the error message above.
    pause
    exit /b 1
)
echo      Done.
echo.

:: Optional packages
echo [3/4] Optional packages:
echo   - pyautogui   : Chrome GUI automation fallback
echo   - pygetwindow : Window detection
echo   - pytesseract : Kakao OCR feature
echo.
set /p INSTALL_OPT=Install optional packages? (y/N): 
if /i "%INSTALL_OPT%"=="y" (
    echo.
    echo    Installing optional packages...
    python -m pip install -r requirements-optional.txt
    if errorlevel 1 (
        echo [WARNING] Some optional packages failed - continuing.
    )
    echo    Done.
) else (
    echo    Skipping optional packages.
)
echo.

:: Verify
echo [4/4] Verifying installation...
python -c "import ttkbootstrap, telethon, PIL, openpyxl, pyperclip, requests, win32api; print('  [OK] All required packages verified')"
if errorlevel 1 (
    echo.
    echo [ERROR] Some packages are not installed correctly.
    echo         Please check the error message above.
    pause
    exit /b 1
)
echo.

echo ============================================================
echo  Installation complete!
echo  Run the program with:
echo    python messenger_allInOne_v1.61.py
echo ============================================================
echo.
pause
endlocal
