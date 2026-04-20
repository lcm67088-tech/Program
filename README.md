# messenger_allInOne

카카오 / 텔레그램 자동 메시지 발송 올인원 프로그램

---

## 빠른 시작 — 의존성 설치

### 방법 1: 원클릭 (권장)
```
install.bat  ← 더블클릭
```
Python 설치 확인 → pip 업그레이드 → 필수 패키지 → 선택 패키지 → 검증까지 자동 진행

### 방법 2: 수동 설치
```bash
# 필수 패키지 (반드시 설치)
python -m pip install -r requirements.txt

# 선택 패키지 (GUI 폴백 / OCR / community_poster 사용 시)
python -m pip install -r requirements-optional.txt
```

### 필수 패키지 목록 (requirements.txt)

| 패키지 | 버전 | 용도 |
|--------|------|------|
| ttkbootstrap | ≥1.10.1 | UI 프레임워크 (Tkinter 테마) |
| telethon | ≥1.36.0 | Telegram API (MTProto) — 그룹 가입·메시지 발송 |
| Pillow | ≥10.0.0 | 이미지 처리, 스크린샷 저장 |
| openpyxl | ≥3.1.0 | .xlsx 대상 목록 읽기/저장 |
| pyperclip | ≥1.8.2 | 텍스트 클립보드 복사 |
| requests | ≥2.31.0 | 자동 업데이트 체크 |
| pywin32 | ≥306 | Windows API (클립보드·창 핸들) |

### 선택 패키지 목록 (requirements-optional.txt)

| 패키지 | 버전 | 용도 |
|--------|------|------|
| pyautogui | ≥0.9.54 | Chrome GUI 자동화 폴백 |
| pygetwindow | ≥0.0.9 | 활성 창 감지 |
| pytesseract | ≥0.3.10 | 카카오 OCR (Tesseract 엔진 별도 설치 필요) |
| selenium | ≥4.18.0 | community_poster 전용 |
| undetected-chromedriver | ≥3.5.5 | community_poster 전용 |

> **참고**: Telethon 계정을 등록하면 pyautogui 없이도 텔레그램 기능이 완전히 동작합니다.

---

## Python 버전

- **권장**: Python 3.9 ~ 3.13
- **최적**: Python 3.11
- **3.14+**: ttkbootstrap 호환 패치 필요 → `python fix_ttkbootstrap.py` 실행

---

## 실행 방법

```bash
python messenger_allInOne_v1.61.py
```

---

## 주요 기능

- **텔레그램**: Telethon API 기반 그룹 가입·메시지 발송 (최대 15계정 동시)
- **카카오**: 오픈채팅·친구추가 자동화
- **작업 관리**: 스케줄 등록, 순차 반복 실행 (v1.69)
- **계정 관리**: Telethon .session 파일 기반, 일일 발송 제한·웜업 모드
- **자동 업데이트**: GitHub 버전 체크

---

## 버전 히스토리 (최근)

| 버전 | 주요 변경 |
|------|-----------|
| v1.72 | 가입 후 발송 체크박스 미표시 버그 수정 |
| v1.71 | Telethon 모드에서 좌표 UI 자동 숨김 |
| v1.70 | telegram_message Telethon 경로 join_first 버그 수정 |
| v1.69 | 순차 반복 실행 기능 추가 |
| v1.68 | 가입 후 메시지 발송 워크플로우 추가 |
| v1.61 | Telethon 엔진 도입 (pyautogui → MTProto) |

---

## GitHub

https://github.com/lcm67088-tech/Program
