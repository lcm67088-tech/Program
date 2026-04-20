@echo off
chcp 65001 >nul 2>&1
setlocal

echo.
echo ============================================================
echo  messenger_allInOne v1.72 - 의존성 설치 스크립트
echo ============================================================
echo.

:: ── Python 확인 ──────────────────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo [오류] Python 이 설치되어 있지 않거나 PATH 에 없습니다.
    echo.
    echo  Python 3.11 설치 URL:
    echo  https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
    echo.
    echo  설치 시 "Add python.exe to PATH" 를 반드시 체크하세요!
    echo.
    pause
    exit /b 1
)

python --version
echo.

:: Python 버전 경고 (3.14 이상은 ttkbootstrap 호환 이슈 있음)
for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PY_VER=%%v
echo  감지된 Python 버전: %PY_VER%
echo  * Python 3.9 ~ 3.13 권장 / 3.14+ 는 일부 호환성 문제 가능
echo.

:: ── pip 업그레이드 ───────────────────────────────────────────
echo [1/5] pip 업그레이드 중...
python -m pip install --upgrade pip --quiet
echo      완료.
echo.

:: ── 필수 패키지 설치 ─────────────────────────────────────────
echo [2/5] 필수 패키지 설치 중... (requirements.txt)
echo       ttkbootstrap, telethon, Pillow, openpyxl,
echo       pyperclip, requests, pywin32
echo.
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [오류] 필수 패키지 설치 실패.
    echo        위 오류 메시지를 확인하세요.
    pause
    exit /b 1
)
echo      완료.
echo.

:: ── 선택 패키지 ──────────────────────────────────────────────
echo [3/5] 선택(Optional) 패키지:
echo   - pyautogui          : Chrome GUI 자동화 폴백
echo   - pygetwindow        : 창 감지
echo   - pytesseract        : 카카오 OCR 기능
echo   - selenium           : community_poster 용
echo   - undetected-chromedriver : community_poster 용
echo.
set /p INSTALL_OPT=선택 패키지를 설치하시겠습니까? (y/N): 
if /i "%INSTALL_OPT%"=="y" (
    echo.
    echo    선택 패키지 설치 중...
    python -m pip install -r requirements-optional.txt
    if errorlevel 1 (
        echo [경고] 일부 선택 패키지 설치 실패 - 계속 진행합니다.
    )
    echo    완료.
) else (
    echo    선택 패키지 건너뜀.
)
echo.

:: ── ttkbootstrap 호환 패치 (Python 3.14+ 대비) ───────────────
echo [4/5] ttkbootstrap 호환성 확인 중...
python -c "import ttkbootstrap" >nul 2>&1
if errorlevel 1 (
    echo  ttkbootstrap 임포트 실패 - 호환 패치 시도 중...
    if exist fix_ttkbootstrap.py (
        python fix_ttkbootstrap.py
    ) else (
        echo  [경고] fix_ttkbootstrap.py 없음 - 패치 건너뜀.
    )
) else (
    echo      ttkbootstrap 정상 확인.
)
echo.

:: ── 최종 검증 ─────────────────────────────────────────────────
echo [5/5] 설치 검증 중...
python -c "import ttkbootstrap, telethon, PIL, openpyxl, pyperclip, requests, win32api; print('  [OK] 모든 필수 패키지 정상 확인')"
if errorlevel 1 (
    echo.
    echo [오류] 일부 패키지가 올바르게 설치되지 않았습니다.
    echo        위 오류 메시지를 확인하세요.
    pause
    exit /b 1
)
echo.

echo ============================================================
echo  설치 완료!
echo  실행 방법:
echo    python messenger_allInOne_v1.61.py
echo ============================================================
echo.
pause
endlocal
