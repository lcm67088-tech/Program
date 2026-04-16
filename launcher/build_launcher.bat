@echo off
chcp 65001 > nul
echo ================================================
echo   메신저 올인원 런처 빌드
echo ================================================
echo.

:: Python / pip 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo [오류] Python이 설치되어 있지 않습니다.
    pause
    exit /b 1
)

:: PyInstaller 설치 확인
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo PyInstaller 설치 중...
    pip install pyinstaller
)

:: 이전 빌드 정리
if exist dist\메신저올인원_런처.exe (
    del /f dist\메신저올인원_런처.exe
    echo 기존 빌드 파일 삭제 완료
)
if exist build (
    rmdir /s /q build
)

echo.
echo 런처 빌드 시작...
echo.

:: PyInstaller로 단일 exe 빌드
pyinstaller launcher.spec --clean

if errorlevel 1 (
    echo.
    echo [오류] 빌드 실패!
    pause
    exit /b 1
)

echo.
echo ================================================
echo   빌드 완료!
echo   파일 위치: dist\메신저올인원_런처.exe
echo ================================================
echo.
echo 이 파일을 GitHub의 launcher\ 폴더에 업로드하세요.
echo.
pause
