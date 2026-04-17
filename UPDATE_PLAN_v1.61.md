# 메신저 올인원 v1.61 업데이트 계획서

> 작성일: 2026-04-17  
> 기준 버전: v1.60.2  
> 목표 버전: v1.61  

---

## 1. 업데이트 배경 및 목적

### 현재 v1.60의 병목 구조

현재 텔레그램 작업(`telegram_join`, `telegram_message`)은 아래 흐름으로 동작한다.

```
[크롬 주소창 좌표 클릭]
    → t.me/링크 입력 + Enter
    → 크롬이 OS 프로토콜 핸들러(tg://)로 전달
    → OS가 기본 등록된 텔레그램 앱 1개로만 전달
    → 텔레그램 앱에서 가입/메시지 좌표 클릭
```

**핵심 문제:**  
- `pyautogui`는 단일 마우스/키보드를 사용하므로 동시 실행 불가
- OS 프로토콜 핸들러는 텔레그램 앱을 1개만 받으므로, V5 등으로 멀티 인스턴스를 열어도 어느 계정이 링크를 받는지 제어 불가
- 결과적으로 **1개 계정 순차 실행만 가능** → 처리 속도 병목

### 해결 방향

크롬 앱이 아닌 **`web.telegram.org`를 크롬 독립 세션(--user-data-dir)으로 N개 열어**,  
각 크롬 창을 계정별로 매핑하고 순차 전환하며 작업을 처리한다.

- 구글 계정 불필요
- 텔레그램 앱 설치 불필요
- 로그인 세션 영구 유지 (게스트 모드와 달리 창을 닫아도 유지)
- 계정 수 무제한

---

## 2. 핵심 아이디어: 크롬 독립 세션 방식

### 원리

크롬 실행 시 `--user-data-dir` 옵션으로 데이터 저장 폴더를 지정하면,  
해당 폴더가 다른 크롬끼리는 완전히 독립된 브라우저로 동작한다.

```
chrome.exe --user-data-dir="C:\TelegramAccounts\계정1" --new-window
chrome.exe --user-data-dir="C:\TelegramAccounts\계정2" --new-window
chrome.exe --user-data-dir="C:\TelegramAccounts\계정3" --new-window
```

```
C:\TelegramAccounts\
├── 계정1\   ← 텔레그램 계정 A 로그인 세션 저장
├── 계정2\   ← 텔레그램 계정 B 로그인 세션 저장
├── 계정3\   ← 텔레그램 계정 C 로그인 세션 저장
```

### 로그인 과정 (최초 1회만)

1. 프로그램에서 "계정 추가" 클릭
2. 해당 폴더로 크롬 창이 자동으로 열림
3. `web.telegram.org` 접속
4. 텔레그램 전화번호로 로그인 (QR 또는 SMS 인증)
5. 이후 해당 폴더로 크롬을 열 때마다 로그인 유지

### 게스트 모드와 비교

| 구분 | 게스트 모드 | --user-data-dir |
|---|---|---|
| 계정 수 제한 | 없음 | 없음 |
| 구글 계정 필요 | 불필요 | 불필요 |
| 세션 유지 | 창 닫으면 삭제 | 영구 유지 |
| 재로그인 | 매번 필요 | 최초 1회만 |
| 관리 편의 | 구분 어려움 | 폴더명으로 구분 |

---

## 3. 실행 모드 2가지

### 모드 A: 반복 모드 (All Accounts)

링크 목록 전체를 등록된 모든 계정이 각각 처리한다.

```
링크 목록: [t.me/aaa, t.me/bbb, t.me/ccc ... 100개]
계정: [계정1, 계정2, 계정3]

→ 계정1: t.me/aaa ~ t.me/ccc (100개 전부)
→ 계정2: t.me/aaa ~ t.me/ccc (100개 전부)
→ 계정3: t.me/aaa ~ t.me/ccc (100개 전부)

총 발송: 300회
```

**용도:** 같은 메시지를 여러 계정으로 반복 발송할 때

---

### 모드 B: 분배 모드 (Split)

링크 목록을 계정 수만큼 균등 분배해 처리한다.

```
링크 목록: [t.me/aaa ~ t.me/ccc ... 100개]
계정: [계정1, 계정2, 계정3]

→ 계정1: 1~34번 링크
→ 계정2: 35~67번 링크
→ 계정3: 68~100번 링크

총 발송: 100회 (3배 속도)
```

**용도:** 처리 속도를 높이고 싶을 때, 계정별 발송 이력을 분리하고 싶을 때

---

## 4. 변경이 필요한 코드 구조

### 4-1. 현재 좌표 구조 (1세트)

```python
# 현재: 템플릿 1개에 좌표 1세트
template = {
    "coords": {
        "chrome_addr":   {"x": 100, "y": 50},
        "join_btn":      {"x": 500, "y": 300},
        "close_tab":     {"x": 800, "y": 30},
        "message_input": {"x": 500, "y": 600},
        "send_btn":      {"x": 750, "y": 600},
    }
}
```

### 4-2. 변경 후 좌표 구조 (N세트)

```python
# 변경 후: 계정별 좌표 세트 리스트
template = {
    "multi_account": True,          # 멀티 계정 모드 활성화 여부
    "account_mode": "split",        # "split" | "all"
    "accounts": [
        {
            "name":       "계정1",
            "profile_dir": "C:\\TelegramAccounts\\계정1",
            "coords": {
                "chrome_addr":   {"x": 100, "y": 50},
                "join_btn":      {"x": 500, "y": 300},
                "close_tab":     {"x": 800, "y": 30},
                "message_input": {"x": 500, "y": 600},
                "send_btn":      {"x": 750, "y": 600},
            }
        },
        {
            "name":       "계정2",
            "profile_dir": "C:\\TelegramAccounts\\계정2",
            "coords": {
                "chrome_addr":   {"x": 1060, "y": 50},
                "join_btn":      {"x": 1460, "y": 300},
                "close_tab":     {"x": 1760, "y": 30},
                "message_input": {"x": 1460, "y": 600},
                "send_btn":      {"x": 1710, "y": 600},
            }
        },
    ]
}
```

### 4-3. 하위 호환성

- `accounts` 키가 없으면 기존 단일 `coords` 구조로 동작 (v1.60과 동일)
- 기존 저장된 JSON 작업 파일에 영향 없음
- `_migrate_legacy_json()` 에 MIGRATE-11 항목 추가 예정

---

## 5. WorkflowExecutor 변경 계획

### 5-1. 현재 실행 흐름

```python
def _run_telegram_message(self):
    rows = self._read_targets()
    for idx, row in enumerate(rows):
        self._click("chrome_addr")    # ← 단일 coords 사용
        self._type(link)
        ...
```

### 5-2. 변경 후 실행 흐름

```python
def _run_telegram_message(self):
    rows     = self._read_targets()
    accounts = self._get_accounts()   # 계정 목록 반환

    if len(accounts) <= 1:
        # 기존 단일 계정 로직 그대로 실행
        self._run_telegram_message_single(rows, accounts[0])
        return

    mode = self.tmpl.get("account_mode", "split")

    if mode == "split":
        # 링크 목록을 계정별로 분배
        chunks = self._split_rows(rows, len(accounts))
        for account, chunk in zip(accounts, chunks):
            self._activate_chrome(account)      # 크롬 창 포그라운드
            self.coords = account["coords"]     # 좌표 세트 교체
            self._run_telegram_message_single(chunk, account)

    elif mode == "all":
        # 모든 계정이 전체 링크 처리
        for account in accounts:
            self._activate_chrome(account)
            self.coords = account["coords"]
            self._run_telegram_message_single(rows, account)

def _activate_chrome(self, account: dict):
    """해당 계정의 크롬 창을 포그라운드로 가져옴"""
    # chrome_addr 좌표 클릭으로 해당 창 활성화
    # (또는 창 제목으로 구분 가능하면 win32gui 보조 사용)
    addr = account["coords"].get("chrome_addr", {})
    x, y = addr.get("x", 0), addr.get("y", 0)
    if x and y:
        pyautogui.click(x, y)
        time.sleep(0.5)

def _split_rows(self, rows: list, n: int) -> list[list]:
    """rows를 n개로 균등 분배"""
    chunk_size = math.ceil(len(rows) / n)
    return [rows[i:i+chunk_size] for i in range(0, len(rows), chunk_size)]
```

---

## 6. UI 변경 계획 (TemplateTab)

### 6-1. 싱글 계정 / 멀티 계정 전환 토글

```
[ 단일 계정 ] ←→ [ 멀티 계정 ]    (라디오 버튼 또는 체크박스)
```

- 단일 계정: 현재 v1.60과 동일한 좌표 섹션 표시
- 멀티 계정: 계정 목록 + 계정별 좌표 섹션 표시

### 6-2. 멀티 계정 UI 구성

```
┌─────────────────────────────────────────────────────┐
│ 멀티 계정 설정                          [+ 계정 추가] │
├─────────────────────────────────────────────────────┤
│ 실행 모드:  ○ 분배 모드 (Split)  ○ 반복 모드 (All)   │
├─────────────────────────────────────────────────────┤
│ [계정1 ▼]  프로필 경로: C:\TelegramAccounts\계정1    │
│            [크롬 열기]  [좌표 캡처]  [삭제]           │
│                                                      │
│   chrome_addr  x:[____] y:[____]  [📸 캡처]          │
│   join_btn     x:[____] y:[____]  [📸 캡처]          │
│   close_tab    x:[____] y:[____]  [📸 캡처]          │
│   message_input x:[___] y:[____]  [📸 캡처]          │
│   send_btn     x:[____] y:[____]  [📸 캡처]          │
├─────────────────────────────────────────────────────┤
│ [계정2 ▼]  프로필 경로: C:\TelegramAccounts\계정2    │
│            [크롬 열기]  [좌표 캡처]  [삭제]           │
│   ...                                                │
└─────────────────────────────────────────────────────┘
```

### 6-3. "크롬 열기" 버튼 동작

버튼 클릭 시 해당 계정 프로필 폴더로 크롬 실행:

```python
def _open_chrome(self, profile_dir: str):
    import subprocess
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for path in chrome_paths:
        if Path(path).exists():
            subprocess.Popen([
                path,
                f"--user-data-dir={profile_dir}",
                "--new-window",
                "https://web.telegram.org"
            ])
            return
    messagebox.showerror("오류", "크롬 경로를 찾을 수 없습니다.")
```

### 6-4. 기본 프로필 경로 자동 설정

- 기본값: 프로그램 실행 파일 옆에 `TelegramAccounts\계정N` 폴더 자동 생성
- 사용자가 직접 경로 변경 가능

---

## 7. 데이터 스키마 변경

### 7-1. 템플릿 JSON 변경

```json
{
  "name": "텔레그램 메시지 템플릿",
  "workflow": "telegram_message",
  "multi_account": true,
  "account_mode": "split",
  "accounts": [
    {
      "name": "계정1",
      "profile_dir": "C:\\TelegramAccounts\\계정1",
      "coords": {
        "chrome_addr":   {"x": 100, "y": 50},
        "message_input": {"x": 500, "y": 600},
        "send_btn":      {"x": 750, "y": 600}
      }
    },
    {
      "name": "계정2",
      "profile_dir": "C:\\TelegramAccounts\\계정2",
      "coords": {
        "chrome_addr":   {"x": 1060, "y": 50},
        "message_input": {"x": 1460, "y": 600},
        "send_btn":      {"x": 1710, "y": 600}
      }
    }
  ],
  "message": "안녕하세요! {이름}님",
  "tg_chrome_load": 2.0,
  "tg_between_min": 20.0,
  "tg_between_max": 30.0
}
```

### 7-2. 마이그레이션 (MIGRATE-11)

기존 단일 계정 템플릿을 멀티 계정 구조로 자동 변환:

```python
# MIGRATE-11: 단일 coords → accounts[0] 래핑
if "coords" in d and "accounts" not in d:
    d["accounts"] = [{
        "name": "계정1",
        "profile_dir": "",
        "coords": d.pop("coords")
    }]
    d["multi_account"] = False
    d["account_mode"] = "split"
```

---

## 8. ETA 패널 연동

v1.60에서 추가된 ETA(예상 완료 시간) 패널을 멀티 계정에 맞게 확장한다.

### 현재 ETA 계산

```
예상 시간 = 링크 수 × 워크플로우 기본 소요시간
```

### v1.61 ETA 계산

```
[분배 모드]
예상 시간 = (링크 수 ÷ 계정 수) × 워크플로우 기본 소요시간

[반복 모드]
예상 시간 = 링크 수 × 계정 수 × 워크플로우 기본 소요시간
```

ETA 패널 표시 예시:

```
┌─────────────────────────────────────┐
│ 전체 예상: 약 45분                   │
│ 완료 예상: 오후 3:25                 │
│                                      │
│ 계정1: 1~50번 처리 중 (23/50)        │
│ 계정2: 51~100번 대기 중              │
│                                      │
│ [새로고침]                            │
└─────────────────────────────────────┘
```

---

## 9. 로그 출력 변경

멀티 계정 실행 시 로그에 계정명 prefix 추가:

```
[계정1] [1/50] https://t.me/channel_a
[계정1]   ✅ 발송 완료
[계정1] [2/50] https://t.me/channel_b
[계정1]   ✅ 발송 완료
...
[계정2] [51/100] https://t.me/channel_c  (계정1 완료 후)
[계정2]   ✅ 발송 완료
...
```

---

## 10. 버전 및 파일 변경 사항

### APP_VERSION

```python
APP_VERSION = "1.61"
```

### 변경 파일

| 파일 | 변경 내용 |
|---|---|
| `messenger_allInOne_v1.60.py` → `messenger_allInOne_v1.61.py` | 전체 변경사항 적용 |
| `messenger_v160.spec` → `messenger_v161.spec` | 파일명 업데이트 |
| `version.json` | 버전 1.61 반영 |

### PyInstaller spec 변경

```python
# messenger_v161.spec
a = Analysis(
    ['messenger_allInOne_v1.61.py'],
    ...
)
exe = EXE(
    pyz,
    name="메신저올인원",
    ...
)
```

---

## 11. 구현 순서 (개발 단계)

### Phase 1. 데이터 구조 변경
- [ ] `PLATFORMS` 딕셔너리에 `multi_account` 관련 키 추가
- [ ] 템플릿 JSON 스키마 확장 (`accounts` 배열)
- [ ] `_migrate_legacy_json()` MIGRATE-11 추가

### Phase 2. WorkflowExecutor 변경
- [ ] `_get_accounts()` 메서드 추가 (단일/멀티 계정 통합 반환)
- [ ] `_activate_chrome()` 메서드 추가 (크롬 창 전환)
- [ ] `_split_rows()` 메서드 추가 (링크 균등 분배)
- [ ] `_run_telegram_join()` 멀티 계정 분기 처리
- [ ] `_run_telegram_message()` 멀티 계정 분기 처리

### Phase 3. TemplateTab UI 변경
- [ ] 단일/멀티 계정 전환 토글 추가
- [ ] 계정 목록 UI 구성 (추가/삭제/순서 변경)
- [ ] 계정별 좌표 캡처 섹션 (접기/펼치기 지원)
- [ ] "크롬 열기" 버튼 구현
- [ ] 프로필 기본 경로 자동 설정
- [ ] 실행 모드 선택 (분배/반복)

### Phase 4. ETA 패널 연동
- [ ] 멀티 계정 ETA 계산 로직 수정
- [ ] 계정별 진행상황 표시

### Phase 5. 로그 연동
- [ ] 계정명 prefix 로그 출력

### Phase 6. 테스트 및 빌드
- [ ] 단일 계정 하위 호환 테스트
- [ ] 2계정 분배 모드 테스트
- [ ] 2계정 반복 모드 테스트
- [ ] PyInstaller 빌드 (`messenger_v161.spec`)
- [ ] `version.json` 업데이트
- [ ] GitHub 푸시 → Actions 자동 빌드

---

## 12. 주의사항 및 제약

### 좌표 기반 방식의 특성
- 계정별 크롬 창 위치가 달라야 좌표가 겹치지 않음
- 사용자가 창 배치 후 각 계정 좌표를 직접 캡처해야 함
- 실행 중 창 이동 시 오작동 가능 → 실행 중 창 이동 금지 안내 메시지 추가 필요

### 크롬 경로
- 크롬 설치 경로가 다를 수 있으므로 다중 경로 탐색 로직 필요
- 크롬 미설치 시 안내 메시지 표시

### web.telegram.org 특성
- 링크 입력 후 web.telegram.org 내에서 채널/그룹 페이지가 열리는 방식
- 현재 t.me 링크를 크롬 주소창에 입력하면 web.telegram.org로 리다이렉트되는 구조 활용 가능
- 단, web UI의 버튼 위치가 텔레그램 앱과 다를 수 있으므로 좌표 재캡처 필요

### 딜레이 설정
- 멀티 계정이라도 순차 실행이므로 계정 전환 시 추가 딜레이 필요
- `account_switch_delay` 파라미터 추가 예정 (기본값: 1.0s)

---

## 13. 향후 고려 사항 (v1.62+)

- 계정별 발송 통계 분리 (StatsTab)
- 계정별 실패 재시도 로직
- 크롬 창 자동 배치 기능 (화면 분할)
- 계정별 딜레이 개별 설정
