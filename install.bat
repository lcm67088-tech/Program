@echo off
chcp 65001 >nul
setlocal

echo.
echo ============================================================
echo  messenger_allInOne  의존성 설치 스크립트
echo ============================================================
echo.

:: ── Python 설치 여부 확인 ────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo [오류] Python이 설치되어 있지 않습니다.
    echo.
    echo  아래 주소에서 Python 3.11 이상을 설치하세요:
    echo  https://www.python.org/downloads/
    echo.
    echo  설치 시 반드시 "Add python.exe to PATH" 체크박스를 선택하세요.
    echo.
    pause
    exit /b 1
)

python --version
echo.

:: ── pip 최신화 ───────────────────────────────────────────────
echo [1/4] pip 업그레이드 중...
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo [경고] pip 업그레이드 실패 - 계속 진행합니다.
)
echo       완료.
echo.

:: ── 필수 패키지 설치 ─────────────────────────────────────────
echo [2/4] 필수 패키지 설치 중... (requirements.txt)
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [오류] 필수 패키지 설치 중 문제가 발생했습니다.
    echo        위 오류 메시지를 확인하세요.
    pause
    exit /b 1
)
echo       완료.
echo.

:: ── 선택 패키지 설치 ─────────────────────────────────────────
echo [3/4] 선택 패키지 설치 여부 확인...
echo.
echo  [선택 패키지 안내]
echo   - pyautogui  : Telethon 미설치 시 Chrome GUI 자동화 폴백
echo   - pygetwindow: 창 감지 (파일 대화상자 등)
echo   - pytesseract: 카카오 친구추가 OCR 기능
echo.
set /p INSTALL_OPT=선택 패키지도 설치하시겠습니까? (y/N): 
if /i "%INSTALL_OPT%"=="y" (
    echo.
    echo    선택 패키지 설치 중... (requirements-optional.txt)
    pip install -r requirements-optional.txt
    if errorlevel 1 (
        echo [경고] 선택 패키지 일부 설치 실패 - 계속 진행합니다.
    )
    echo    완료.
) else (
    echo    선택 패키지 설치를 건너뜁니다.
)
echo.

:: ── 설치 검증 ─────────────────────────────────────────────────
echo [4/4] 설치 검증 중...
python -c "import ttkbootstrap, telethon, PIL, openpyxl, pyperclip, requests, win32api; print('  [OK] 필수 패키지 모두 정상 확인')"
if errorlevel 1 (
    echo.
    echo [오류] 일부 패키지가 올바르게 설치되지 않았습니다.
    echo        위 오류 메시지를 확인하고 다시 시도하세요.
    pause
    exit /b 1
)
echo.

echo ============================================================
echo  설치 완료!
echo  messenger_allInOne_v1.61.py 를 실행하세요:
echo    python messenger_allInOne_v1.61.py
echo ============================================================
echo.
pause
endlocal
