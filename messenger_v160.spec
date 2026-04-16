# -*- mode: python ; coding: utf-8 -*-
# messenger_v160.spec  -  PyInstaller 폴더형 빌드 설정
# 위치 : 프로젝트 루트 (py 파일과 동일 폴더)
# 업데이트: v1.60 (2026-03-16)
#   - 진입 파일 : messenger_allInOne_v1.57.py -> messenger_allInOne_v1.60.py
#   - hiddenimports : urllib.request, urllib.error, hashlib, subprocess, platform 추가
#                     (v1.60 auto_updater 모듈 신규 사용)
#   - hiddenimports : math 추가 (v1.60 ETA 계산 신규 사용)
#   - datas : auto_updater.py 포함 (앱과 동일 폴더에 배치)

import sys, os
from pathlib import Path

# ── CWD 기반으로 루트 결정 (build.bat 이 cd /d 로 이동시켜 줌) ──
def _find_root():
    cwd  = Path(os.getcwd())
    spec = Path(os.path.abspath(SPECPATH))
    py   = "messenger_allInOne_v1.60.py"
    for candidate in [cwd, spec, spec.parent]:
        if (candidate / py).exists():
            return candidate
    raise FileNotFoundError(
        f"[spec] {py} 를 찾을 수 없습니다.\n"
        f"  시도한 경로:\n"
        f"    CWD  : {cwd}\n"
        f"    SPEC : {spec}\n"
        f"    PARENT: {spec.parent}"
    )

ROOT_DIR    = _find_root()
SCRIPT_PATH = str(ROOT_DIR / "messenger_allInOne_v1.60.py")

HIDDEN = [
    # ── UI 프레임워크 ──
    "tkinter", "tkinter.ttk", "tkinter.filedialog", "tkinter.messagebox",
    "ttkbootstrap", "ttkbootstrap.constants",

    # ── 자동화 / 클립보드 / 윈도우 제어 ──
    "pyautogui", "pyperclip", "pygetwindow",

    # ── 이미지 / OCR ──
    "PIL", "PIL.Image", "PIL.ImageGrab", "pytesseract",

    # ── Windows API ──
    "win32gui", "win32clipboard",

    # ── 엑셀 ──
    "openpyxl", "openpyxl.styles", "openpyxl.utils",

    # ── 네트워크 (구글시트 로그인) ──
    "requests", "requests.adapters", "requests.auth",
    "urllib3", "urllib3.util.retry",
    "certifi",

    # ── 네트워크 (v1.60 auto_updater 신규) ──
    "urllib.request", "urllib.error", "urllib.parse",

    # ── 표준 라이브러리 ──
    "json", "threading", "pathlib", "datetime", "logging",
    "csv", "shutil", "queue",
    "io", "copy", "typing",
    "re", "os", "sys", "time", "random", "string",
    "hashlib",      # v1.60 auto_updater: MD5 검증
    "subprocess",   # v1.60 auto_updater: .bat 실행
    "platform",     # v1.60 auto_updater: OS 분기
    "math",         # v1.60 ETA 계산
    "collections",
    "traceback",
]

# ── auto_updater.py 를 exe 와 동일 폴더에 포함 ──────────────────────
_auto_updater_src = str(ROOT_DIR / "auto_updater.py")
DATAS = []
if (ROOT_DIR / "auto_updater.py").exists():
    DATAS.append((_auto_updater_src, "."))

a = Analysis(
    [SCRIPT_PATH],
    pathex=[str(ROOT_DIR)],
    binaries=[],
    datas=DATAS,
    hiddenimports=HIDDEN,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "matplotlib", "numpy", "pandas", "scipy",
        "IPython", "jupyter", "notebook",
        "pytest", "setuptools", "pkg_resources", "_pytest",
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="메신저올인원",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon="icon.ico",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="메신저올인원",
)
