# 메신저 올인원 v1.61 업데이트 계획서

> 작성일: 2026-04-17  
> 최종수정: 2026-04-17 (전면 재작성 — UI 리디자인 + 스케줄 버그 + Telethon 방향성 포함)  
> 기준 버전: v1.60.2  
> 목표 버전: v1.61  

---

## 0. 업데이트 방향 요약

| 영역 | v1.60 상태 | v1.61 목표 |
|---|---|---|
| **텔레그램 엔진** | pyautogui 좌표 기반 (1계정 순차) | **Telethon API로 전면 교체** (15계정 동시) |
| **카카오 엔진** | pyautogui 좌표 기반 (유지) | 현행 유지 (API 없음) |
| **UI 전반** | 기능 중심, 섹션 혼재 | community_poster v5.20 스타일로 정비 |
| **스케줄러** | 오류 있음 (아래 상세 기술) | 완전 수정 + community_poster 방식 벤치마킹 |

### v1.61 핵심 3대 목표

1. **텔레그램 엔진 → Telethon 교체** (PC 1대, 15계정 동시 24시간 풀가동)
2. **UI 전반 리디자인** (community_poster v5.20 벤치마킹 — 깔끔·직관적)
3. **스케줄 기능 완전 수정** (community_poster 방식 벤치마킹 — 신뢰성 확보)

---

## 1. [엔진 교체] 텔레그램 Telethon 전환

### 1-1. 왜 Telethon인가

| 비교 항목 | pyautogui (현행) | Telethon (v1.61) |
|---|---|---|
| 실행 방식 | 마우스/키보드 클릭 | Telegram API 직접 호출 |
| 동시 계정 수 | **1개** (물리적 한계) | **15개 동시** (스레드) |
| PC당 24h 운영 | 불가 (순차 → 분할) | 가능 (계정별 독립 스레드) |
| Chrome 필요 | 필요 | **불필요** |
| 좌표 설정 | 필요 | **불필요** |
| 백그라운드 실행 | 불가 (창 필요) | **가능** |
| 밴 리스크 | 패턴 기반 → 딜레이 관리 | 동일 (패턴 기반) |

**핵심:** pyautogui는 물리 마우스가 1개이므로 PC 1대에서 동시 실행이 구조적으로 불가능.  
Telethon은 네트워크 요청이므로 스레드로 진정한 동시 실행이 가능.

---

### 1-2. 시스템 구성 변경

```
[현행 v1.60]
   카카오 ──→ pyautogui (좌표 클릭)
   텔레그램 ──→ pyautogui (좌표 클릭)

[v1.61]
   카카오 ──→ pyautogui (기존 유지)
   텔레그램 ──→ Telethon (API 직접)
                  ├── 계정1 스레드 (24h)
                  ├── 계정2 스레드 (24h)
                  ├── ...
                  └── 계정15 스레드 (24h)
```

---

### 1-3. API 인증 구조

**각 계정에서 개별 API 발급 필요**

```
발급 위치: https://my.telegram.org/apps
필요 정보:
  - api_id   (숫자)
  - api_hash (문자열)
  - session  (자동 생성 — 최초 로그인 1회)
```

**계정별 세션 관리:**
```python
# 세션 파일: accounts/계정1.session, 계정2.session, ...
client = TelegramClient(f"accounts/{name}", api_id, api_hash)
```

---

### 1-4. 텔레그램 기능 구현 계획

#### (A) 그룹 가입 (`telegram_join`)

```python
async def join_group(client, link):
    """t.me/xxx 링크로 그룹/채널 가입"""
    try:
        result = await client(JoinChannelRequest(link))
        return "success"
    except UserAlreadyParticipantError:
        return "already_joined"
    except FloodWaitError as e:
        await asyncio.sleep(e.seconds)
        return "flood_wait"
    except Exception as e:
        return f"error: {e}"
```

#### (B) 메시지 발송 (`telegram_message`)

```python
async def send_message(client, link, text, image_path=None):
    """채널/그룹에 메시지 + 이미지 발송"""
    entity = await client.get_entity(link)
    if image_path:
        await client.send_file(entity, image_path, caption=text)
    else:
        await client.send_message(entity, text)
```

#### (C) 15계정 동시 실행

```python
def run_all_accounts():
    threads = []
    for account in accounts:
        t = threading.Thread(
            target=asyncio.run,
            args=(account_loop(account),),
            daemon=True
        )
        threads.append(t)
        t.start()
    # 각 계정 스레드가 24시간 독립 실행
```

---

### 1-5. 제재 탐지 및 대응

#### 제재 유형별 처리

| 오류 | 의미 | 대응 |
|---|---|---|
| `FloodWaitError(n)` | 속도 제한 — n초 대기 필요 | n초 대기 후 재시도, 다른 계정은 계속 실행 |
| `PeerFloodError` | 스팸 감지 — 계정 위험 | 해당 계정 당일 중지, 익일 재개 |
| `UserBannedInChannelError` | 채널에서 차단 | 해당 채널 블랙리스트 추가, 스킵 |
| `ChatWriteForbiddenError` | 메시지 권한 없음 | 실패 로그 + 스킵 |
| `AccountBannedError` | 계정 완전 정지 | 즉시 전체 중지 + 사용자 알림 |

#### 계정 상태 모니터링 UI

```
┌──────────────────────────────────────────┐
│ 계정 상태 모니터                          │
├──────┬────────┬──────┬───────────────────┤
│ 계정 │ 상태   │ 발송 │ 비고              │
├──────┼────────┼──────┼───────────────────┤
│ 계정1│ 🟢 실행│  234 │                   │
│ 계정2│ 🟡 대기│  189 │ FloodWait 32초    │
│ 계정3│ 🔴 중지│   45 │ PeerFlood — 중지  │
│ 계정4│ ⚫ 밴  │    0 │ AccountBanned ⚠️  │
└──────┴────────┴──────┴───────────────────┘
```

#### 예방 설정

```python
# 계정별 일일 발송 한도
daily_limit = 500  # 기본값

# 신규 계정 워밍업 스케줄
warmup_schedule = {
    "day1": 50,
    "day2": 100,
    "day3": 200,
    "day7+": 500
}

# 연속 실패 후 일시 중지
max_consecutive_fail = 3  # 3회 연속 실패 시 10분 휴식
```

---

### 1-6. UI 변경 — 텔레그램 계정 관리 탭

기존 `TemplateTab`의 좌표 설정 영역을 **텔레그램 계정 관리** 섹션으로 교체.

```
┌────────────────────────────────────────────────────┐
│ 텔레그램 계정 관리                    [+ 계정 추가] │
├────────────────────────────────────────────────────┤
│ 계정명   API ID    상태    발송수   [수정] [삭제]   │
│ 계정1    12345678  🟢 실행   234                   │
│ 계정2    87654321  🟡 대기   189                   │
│ 계정3    11111111  🔴 정지    45                   │
├────────────────────────────────────────────────────┤
│ [▶ 선택 계정 시작]  [■ 전체 중지]  [↻ 상태 갱신]  │
└────────────────────────────────────────────────────┘
```

**계정 추가 다이얼로그:**
```
계정명:    [__________]
API ID:    [__________]
API Hash:  [__________]
전화번호:  [__________]  ← 최초 로그인용
일일 한도: [____] 건    기본값 500
워밍업:    [✓] 신규 계정 워밍업 모드
```

---

## 2. [UI 리디자인] community_poster v5.20 벤치마킹

### 2-1. 현재 UI 문제점

| 문제 | 현행 v1.60 상태 | v1.61 목표 |
|---|---|---|
| **스타일 헬퍼 없음** | 각 탭에서 `tk.Button`, `tk.Label` 직접 생성, 스타일 분산 | `App` 클래스에 `_button()`, `_card()`, `_label()`, `_badge()`, `_separator()` 중앙화 |
| **hover 효과 없음** | 버튼에 hover 없음 | 모든 클릭 요소에 hover 색상 전환 + `_darken()` 헬퍼 |
| **카드 컨테이너 없음** | 섹션 구분 없이 나열 | border 1px + padding 16px 카드 단위 레이아웃 |
| **탭 선택 시각화 미흡** | PALETTE["selected"] bg 변경만 | **폰트 bold + fg white + bg sidebar_h** 동시 변경 |
| **사이드바 활성 탭 구분 불명확** | `tk.Label`로 탭 버튼 구현 | `tk.Button`으로 교체 + 활성/비활성 명확 분리 |
| **헤더 상태 정보 없음** | 의존성 뱃지만 표시 | **실행 중인 작업 수 + 스케줄 ON/OFF 상태** 실시간 표시 |
| **도움말 없음** | ❓ 버튼 없음 | 각 탭에 `_HELP_DATA` 딕셔너리 + 팝업 도움말 |

---

### 2-2. community_poster에서 직접 이식할 패턴

#### (A) 스타일 헬퍼 메서드 (App 클래스)

```python
# community_poster v5.20 에서 직접 이식
def _styled_frame(self, parent, bg=None, padx=0, pady=0):
    return tk.Frame(parent, bg=bg or PALETTE["card"],
                    padx=padx, pady=pady)

def _card(self, parent, padx=16, pady=12):
    """border 1px + 내부 padding 카드 컨테이너"""
    outer = tk.Frame(parent, bg=PALETTE["bg"])
    inner = tk.Frame(outer, bg=PALETTE["card"],
                     highlightbackground=PALETTE["border"],
                     highlightthickness=1)
    inner.pack(fill="both", expand=True, padx=2, pady=2)
    inner._pad = tk.Frame(inner, bg=PALETTE["card"])
    inner._pad.pack(fill="both", expand=True, padx=padx, pady=pady)
    return outer, inner._pad

def _label(self, parent, text, size=10, weight="normal", color=None, **kw):
    return tk.Label(parent, text=text,
                    font=(_FF, size, weight),
                    fg=color or PALETTE["text"],
                    bg=parent.cget("bg"), **kw)

def _button(self, parent, text, command, color=None,
            text_color="#FFFFFF", size=9, width=None, **kw):
    """hover 효과 내장 버튼"""
    orig = color or PALETTE["primary"]
    cfg = dict(text=text, command=command,
               font=(_FF, size, "bold"),
               bg=orig, fg=text_color,
               activebackground=orig, activeforeground=text_color,
               relief="flat", cursor="hand2",
               padx=12, pady=5, bd=0)
    if width: cfg["width"] = width
    cfg.update(kw)
    b = tk.Button(parent, **cfg)
    b.bind("<Enter>", lambda e: b.config(bg=self._darken(orig)))
    b.bind("<Leave>", lambda e: b.config(bg=orig))
    return b

def _darken(self, hex_color, factor=0.85):
    """hover 시 색상 어둡게"""
    h = hex_color.lstrip("#")
    r,g,b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return "#{:02x}{:02x}{:02x}".format(
        int(r*factor), int(g*factor), int(b*factor))

def _separator(self, parent, orient="horizontal", color=None):
    c = color or PALETTE["border"]
    if orient == "horizontal":
        return tk.Frame(parent, bg=c, height=1)
    return tk.Frame(parent, bg=c, width=1)

def _badge(self, parent, text, color):
    """색상 배경 작은 뱃지"""
    f = tk.Frame(parent, bg=color, padx=6, pady=2)
    tk.Label(f, text=text, font=(_FF,8,"bold"),
             fg="#fff", bg=color).pack()
    return f
```

---

#### (B) 헤더 — 실시간 상태 표시

**현행:** 로고 + 버전 + 의존성 뱃지만  
**변경:** 현행 유지 + **우측에 "실행 중 N개" + "스케줄 ON/OFF"** 동적 레이블 추가

```python
def _build_header(self):
    hdr = tk.Frame(self, bg=PALETTE["sidebar"], height=56)
    hdr.pack(fill="x")
    hdr.pack_propagate(False)

    # 로고 + 타이틀
    logo = tk.Frame(hdr, bg=PALETTE["sidebar"])
    logo.pack(side="left", padx=20)
    tk.Label(logo, text="💬", font=F_ICON,
             fg=PALETTE["primary"], bg=PALETTE["sidebar"]).pack(side="left")
    tk.Label(logo, text=" 메신저 올인원",
             font=F_TITLE, fg="#F1F5F9",
             bg=PALETTE["sidebar"]).pack(side="left")
    tk.Label(logo, text=f" v{APP_VERSION}",
             font=F_SMALL, fg=PALETTE["muted"],
             bg=PALETTE["sidebar"]).pack(side="left")

    # 우측 — 상태 뱃지 (community_poster 방식)
    right = tk.Frame(hdr, bg=PALETTE["sidebar"])
    right.pack(side="right", padx=20)

    self._queue_var = tk.StringVar(value="실행 없음")    # ← 신규
    self._sched_var = tk.StringVar(value="스케줄 OFF")   # ← 신규

    tk.Label(right, textvariable=self._queue_var,
             font=F_SMALL, fg=PALETTE["muted"],
             bg=PALETTE["sidebar"]).pack(side="right", padx=8)
    tk.Label(right, textvariable=self._sched_var,
             font=F_SMALL, fg=PALETTE["muted"],
             bg=PALETTE["sidebar"]).pack(side="right", padx=8)
```

---

#### (C) 사이드바 — tk.Button 전환 + hover/active 명확화

**현행:** `tk.Label` + `bind(<Button-1>)` 조합  
**변경:** `tk.Button` 으로 전환, `PALETTE["sidebar_h"]` 활성 배경 명확히

```python
def _build_sidebar(self, parent):
    sb = tk.Frame(parent, bg=PALETTE["sidebar"], width=200)
    sb.pack(side="left", fill="y")
    sb.pack_propagate(False)

    tk.Frame(sb, bg=PALETTE["sidebar"], height=16).pack()

    self._nav_buttons = {}
    for tab_id, label in SIDEBAR_TABS:
        btn = tk.Button(sb,
            text=f"  {label}",
            font=(_FF, 10),
            fg="#94A3B8", bg=PALETTE["sidebar"],
            activeforeground="#FFFFFF",
            activebackground=PALETTE["sidebar_h"],
            relief="flat", anchor="w", cursor="hand2",
            padx=16, pady=10,
            command=lambda k=tab_id: self._switch_tab(k))
        btn.pack(fill="x")
        self._nav_buttons[tab_id] = btn

    # 하단 버전
    tk.Frame(sb, bg=PALETTE["sidebar"]).pack(fill="y", expand=True)
    tk.Label(sb, text=f"v{APP_VERSION}",
             font=F_SMALL, fg="#334155",
             bg=PALETTE["sidebar"]).pack(pady=10)

def _switch_tab(self, tab_id):
    for k, btn in self._nav_buttons.items():
        if k == tab_id:
            btn.config(fg="#FFFFFF", bg=PALETTE["sidebar_h"],
                       font=(_FF, 10, "bold"))
        else:
            btn.config(fg="#94A3B8", bg=PALETTE["sidebar"],
                       font=(_FF, 10))
    # 탭 전환
    for tid, frame in self._tab_frames.items():
        frame.lift() if tid == tab_id else frame.lower()
    self._active_tab = tab_id
    # refresh 콜백
    refresh = getattr(self, f"_refresh_{tab_id}", None)
    if refresh: refresh()
```

---

#### (D) 도움말 팝업 — `_HELP_DATA` 딕셔너리 방식

community_poster의 각 탭 도움말 구조를 그대로 이식:

```python
_HELP_DATA = {
    "templates": {
        "title": "🗂️  작업 템플릿 – 사용 방법",
        "steps": [
            ("템플릿이란?",
             "플랫폼(카카오/텔레그램) + 작업 유형 + 대상 CSV + 메시지 설정의 묶음.\n"
             "한 번 만들어두면 작업 관리에서 반복 사용 가능."),
            ("① 템플릿 추가",
             "+ 버튼 클릭 → 플랫폼/작업유형 선택 → 저장."),
            ("② 좌표 캡처",
             "📸 캡처 버튼 클릭 → 3초 카운트다운 → 마우스 위치 자동 저장."),
        ],
        "tips": [
            "💡 카카오 친구추가는 id_add_btn, status_dot, friend_add_btn 3개 좌표 필요.",
            "💡 텔레그램은 v1.61부터 좌표 불필요 — Telethon API 사용.",
        ]
    },
    "jobs": { ... },    # 기존 도움말 유지 + 스케줄 안내 강화
    "log":  { ... },
    "stats":{ ... },
    "settings": { ... },
}
```

---

#### (E) TreeView 행 스타일 — community_poster 방식

```python
# 현행: 단순 bg/fg만
# 변경: community_poster의 site_color 방식 참조

tv.tag_configure("enabled",  background="#FFFFFF", foreground=PALETTE["text"])
tv.tag_configure("disabled", background="#F8F9FA", foreground=PALETTE["muted"])
tv.tag_configure("running",  background="#DBEAFE", foreground=PALETTE["primary"])
tv.tag_configure("success",  background="#F0FDF4", foreground=PALETTE["success_text"])
tv.tag_configure("failed",   background="#FEF2F2", foreground=PALETTE["danger"])

# 카카오 작업 행: 노란 포인트
tv.tag_configure("kakao",    background="#FEFCE8", foreground="#92400E")
# 텔레그램 작업 행: 파란 포인트
tv.tag_configure("telegram", background="#EFF6FF", foreground="#1D4ED8")
```

---

### 2-3. TemplateTab 레이아웃 개선

**현행 문제:** 좌표 섹션 + 스케줄 섹션 + 딜레이 섹션이 길게 나열되어 가독성 저하

**변경:** 카드 단위 분리 + 접기/펼치기(Accordion) 지원

```
┌──────────────────────────────────────────┐
│ 🗂️ 작업 템플릿                  [❓ 도움말] │
├──────────┬───────────────────────────────┤
│ [+ 추가] │  템플릿 편집                   │
│ ──────── │  ┌─ 기본 설정 ──────────────┐ │
│ 카카오친추│  │ 이름: [___________]      │ │
│ 텔레그램  │  │ 플랫폼: [카카오▼]        │ │
│ 오픈채팅  │  │ 작업:  [친구추가▼]       │ │
│          │  └──────────────────────────┘ │
│          │  ┌─ 대상 파일 ──────────────┐ │
│          │  │ [파일 선택] 예시_카카오... │ │
│          │  └──────────────────────────┘ │
│          │  ┌─ 메시지 ─────────────────┐ │
│          │  │ [텍스트 영역]             │ │
│          │  └──────────────────────────┘ │
│          │  ┌─ 좌표 설정 ▼ ──────────┐ │
│          │  │ (카카오만 표시, 접기/펼치기)│ │
│          │  └──────────────────────────┘ │
│          │  ┌─ 딜레이 설정 ▼ ─────────┐ │
│          │  │ (접기/펼치기)              │ │
│          │  └──────────────────────────┘ │
│          │  [💾 저장]  [🗑 삭제]          │
└──────────┴───────────────────────────────┘
```

---

### 2-4. JobsTab 레이아웃 개선

```
┌────────────────────────────────────────────────────────┐
│ 📋 작업 관리                             [❓ 도움말]    │
├────────────────────────────────────────────────────────┤
│ [+ 추가] [✎ 수정] [⧉ 복제] [✕ 삭제]  [▶ 선택실행] [▶▶ 전체실행] │
├────────────────────────────────────────────────────────┤
│ 이름 │ 플랫폼 │ 작업 │ 활성 │ 스케줄    │ 마지막 실행  │
│ ──── │ ────── │ ──── │ ──── │ ────────  │ ──────────── │
│ 작업1│ 🟡카카오│ 친추 │  ⊙  │ 🟢 09:00  │ 10분 전      │
│ 작업2│ 🔵텔레그│ 메시지│ ⊙  │ ⚫ OFF    │ 1시간 전     │
├────────────────────────────────────────────────────────┤
│ ⏱ 예상 소요: 45분 (3개 작업)  🏁 예상 완료: 오후 3:25 [↻] │
└────────────────────────────────────────────────────────┘
```

---

## 3. [스케줄 버그 수정] community_poster 방식 벤치마킹

### 3-1. 현재 스케줄러 문제 목록

#### 문제 1: `after()` 기반 단일 틱 — 잠재적 누락

**현행 구조:**
```python
# JobsTab.__init__
self.after(1_000, self._start_scheduler)

def _start_scheduler(self):
    self._stop_scheduler()
    self._scheduler_running = True
    self._scheduler_tick()   # 첫 틱 즉시

def _scheduler_tick(self):
    # ... 작업 루프 ...
    self._scheduler_after_id = self.after(30_000, self._scheduler_tick)
    # ↑ after()는 Tkinter 메인 스레드 의존
    # UI가 무거운 작업(좌표 캡처, 대화상자 등) 중이면 30초 지연이 늘어남
```

**문제:** `after(30_000)` 은 메인 스레드(Tkinter event loop)에 예약되므로,  
무거운 UI 작업 중엔 실제 30초보다 훨씬 늦게 실행될 수 있음.  
→ `time` 모드에서 정각 트리거 실패 가능성.

#### 문제 2: `_fired_set` 정리 조건 버그

```python
# 현행 (BUG-05 수정 코드)
self._fired_set = {k for k in self._fired_set
                   if k.split("_")[-2] == today_str
                   or len(k.split("_")) < 3}
```
키 형식: `"{job_name}_{YYYY-MM-DD}_{HH:MM}"`  
작업 이름에 `_` 포함 시 `split("_")[-2]` 가 날짜가 아닌 이름 일부를 반환 → 오작동 가능.

#### 문제 3: `interval` 모드 첫 실행 즉시 트리거

```python
if not last_raw:
    fired = True   # 첫 실행 — 즉시
```
프로그램을 재시작할 때마다 interval 모드 작업이 즉시 실행됨.  
`last_run`이 당일이면 skip 해야 하는데 무조건 실행.

#### 문제 4: 자정 경계 처리 복잡성 과잉

`BUG-N1` 수정 코드가 있지만 여전히 edge case 존재:  
스케줄 `23:55`, 실행 직후 `00:01`로 넘어가면 `_key_date` 계산이 맞지 않음.

#### 문제 5: 스케줄 저장 후 즉시 반영 안 됨

작업 편집 후 스케줄 저장 시 `_restart_scheduler()` 호출하지만,  
기존 `after()` 체인이 남아 있어 이전 설정으로 30초 더 실행 가능.

---

### 3-2. community_poster 방식 벤치마킹

community_poster v5.20의 스케줄러는 **독립 스레드** 방식을 사용:

```python
# community_poster 방식
def _start_job_scheduler(self, job):
    stop_flag = threading.Event()
    self._job_sched_threads[jname] = stop_flag

    def _job_loop():
        last_run = 0.0
        while not stop_flag.is_set():
            now  = datetime.now()
            mode = jsched.get("mode", "interval")

            if mode == "times":
                for t in jsched.get("times", []):
                    h2, m2 = map(int, t.split(":"))
                    target = now.replace(hour=h2, minute=m2, second=0)
                    if 0 <= (target - now).total_seconds() < 60:
                        if (now.timestamp() - last_run) >= 50:
                            last_run = now.timestamp()
                            self.after(0, lambda j=job: self._execute(j))
            elif mode == "interval":
                if (now.timestamp() - last_run) >= interval_sec:
                    last_run = now.timestamp()
                    self.after(0, lambda j=job: self._execute(j))

            stop_flag.wait(30)   # 30초 대기

    t = threading.Thread(target=_job_loop, daemon=True)
    t.start()
```

**핵심 차이:**
- `after()` 체인 대신 **독립 데몬 스레드** → UI 블로킹과 완전히 분리
- `stop_flag.wait(30)` → 스레드가 30초 대기 (UI 영향 없음)
- `self.after(0, callback)` → 실행은 메인 스레드에서 안전하게

---

### 3-3. v1.61 스케줄러 수정 방안

#### 수정 1: 스레드 기반으로 전환

```python
# messenger_allInOne_v1.61
# 기존 after() 체인 완전 제거
# community_poster 스타일 스레드로 교체

def _start_scheduler(self):
    if hasattr(self, '_sched_stop_flag'):
        self._sched_stop_flag.set()  # 기존 스레드 중지

    self._sched_stop_flag = threading.Event()
    self._scheduler_running = True

    def _sched_loop():
        while not self._sched_stop_flag.is_set():
            try:
                self._check_and_fire_jobs()
            except Exception as e:
                self._log_error(f"[스케줄러 오류] {e}")
            self._sched_stop_flag.wait(30)

    t = threading.Thread(target=_sched_loop, daemon=True, name="scheduler")
    t.start()
    self._scheduler_thread = t
```

#### 수정 2: `_fired_set` 키 형식 변경 — 밑줄 문제 해결

```python
# 기존: f"{name}_{date}_{time}"  ← 이름에 _ 포함 시 파싱 오류
# 변경: f"{hash(name)}|{date}|{time}"  ← 구분자를 | 로 변경

fired_key = f"{abs(hash(name))}|{key_date}|{t}"

# 정리 로직도 단순화
self._fired_set = {k for k in self._fired_set
                   if k.split("|")[1] == today_str}
```

#### 수정 3: interval 첫 실행 로직 개선

```python
# 기존: last_raw 없으면 즉시 실행
# 변경: last_run_date가 오늘이면 skip

if not last_raw:
    # 최초 등록: 다음 interval 사이클까지 대기 (즉시 실행 안 함)
    fired = False
elif last_run_date == today_str and elapsed_h < interval:
    fired = False
else:
    fired = elapsed_h >= interval
```

#### 수정 4: 스케줄 저장 즉시 반영

```python
def _save_job(self):
    # ... 저장 로직 ...
    save_json(path, data)
    self._restart_scheduler()   # 기존 스레드 중지 + 새 스레드 시작

def _restart_scheduler(self):
    self._stop_scheduler()       # stop_flag.set() → 스레드 자연 종료
    time.sleep(0.1)              # 스레드 종료 대기
    self._start_scheduler()      # 새 스레드 시작
```

#### 수정 5: 스케줄 상태 표시 연동 (헤더)

```python
def _update_schedule_header(self):
    """헤더의 스케줄 상태 레이블 갱신"""
    if not self._scheduler_running:
        self.app._sched_var.set("스케줄 OFF")
        return

    active_count = sum(1 for j in self._jobs
                       if j.get("schedule_on") and j.get("enabled", True))
    if active_count:
        self.app._sched_var.set(f"🟢 스케줄 {active_count}개")
    else:
        self.app._sched_var.set("🟡 스케줄 ON (대기)")
```

---

### 3-4. 스케줄 UI 개선

**현행 문제:** 스케줄 설정이 JobDialog 안에 숨어 있어 한눈에 보기 어려움

**변경:** JobsTab 하단에 **스케줄 상태 패널** 추가 (community_poster 방식)

```
┌─────────────────────────────────────────────────┐
│ 🕐 스케줄 상태                                   │
├─────────────────────────────────────────────────┤
│ 스케줄러: 🟢 실행 중   활성 작업: 3개            │
│                                                  │
│ 작업1  time 모드  09:00, 14:00  🟢 다음: 14:00  │
│ 작업2  interval  매 3시간       🟡 다음: 2시간 후│
│ 작업3  time 모드  21:00         ⚫ 비활성         │
│                                                  │
│ [▶ 스케줄러 시작]  [■ 스케줄러 중지]             │
└─────────────────────────────────────────────────┘
```

---

## 4. 상세 벤치마킹 항목 정리

community_poster v5.20에서 messenger_allInOne v1.61에 적용할 항목 전체 목록:

### UI 컴포넌트

| # | 벤치마킹 항목 | 위치 | 우선순위 |
|---|---|---|---|
| UI-01 | `_card()` 메서드 — border+padding 카드 컨테이너 | App 클래스 | 🔴 필수 |
| UI-02 | `_button()` 메서드 — hover 내장 버튼 | App 클래스 | 🔴 필수 |
| UI-03 | `_darken()` 메서드 — hover 색상 계산 | App 클래스 | 🔴 필수 |
| UI-04 | `_label()` 메서드 — 중앙화 레이블 | App 클래스 | 🟡 권장 |
| UI-05 | `_badge()` 메서드 — 색상 뱃지 | App 클래스 | 🟡 권장 |
| UI-06 | `_separator()` 메서드 — 구분선 | App 클래스 | 🟡 권장 |
| UI-07 | 사이드바 `tk.Button` 전환 + `sidebar_h` 배경 | App._build_sidebar | 🔴 필수 |
| UI-08 | `_switch_tab()` — font bold + fg white + bg sidebar_h | App._switch_tab | 🔴 필수 |
| UI-09 | 헤더 우측 `_queue_var` + `_sched_var` 실시간 레이블 | App._build_header | 🔴 필수 |
| UI-10 | `_HELP_DATA` 딕셔너리 + `_show_help()` 팝업 | 각 탭 | 🟡 권장 |
| UI-11 | Treeview 행 태그 컬러링 (platform별 배경색) | JobsTab | 🟡 권장 |
| UI-12 | 스케줄 상태 아이콘: 🟢/🟡/⚫/⚪ 패턴 | JobsTab | 🔴 필수 |
| UI-13 | `_resolve_job_account()` — 이름→객체 해석 | JobsTab | 🟡 권장 |
| UI-14 | 딜레이 표시 "전역 설정" / "N~Msec" | JobsTab | 🟢 선택 |

### 스케줄러

| # | 벤치마킹 항목 | 위치 | 우선순위 |
|---|---|---|---|
| SC-01 | 독립 데몬 스레드 기반 스케줄러 | JobsTab | 🔴 필수 |
| SC-02 | `stop_flag = threading.Event()` 패턴 | JobsTab | 🔴 필수 |
| SC-03 | `_job_sched_threads` dict 관리 | JobsTab | 🔴 필수 |
| SC-04 | `_restore_scheduler_on_startup()` | JobsTab | 🔴 필수 |
| SC-05 | `_sync_scheduler()` — 작업 변경 후 동기화 | JobsTab | 🔴 필수 |
| SC-06 | 50초 중복 가드 — `last_run` 기반 | 스케줄 루프 | 🔴 필수 |
| SC-07 | 스케줄 저장 즉시 재시작 | `_save_job()` | 🔴 필수 |
| SC-08 | `_fired_set` 키 구분자 `|` 변경 | 스케줄 루프 | 🔴 필수 |

### 데이터 구조

| # | 벤치마킹 항목 | 위치 | 우선순위 |
|---|---|---|---|
| DS-01 | 스케줄 설정을 `schedule` 서브딕셔너리로 분리 | Job JSON | 🟡 권장 |
| DS-02 | `use_global` 플래그 — 전역/개별 스케줄 구분 | schedule dict | 🟡 권장 |
| DS-03 | `interval_variance` 분 단위 (현재 시간 단위) | schedule dict | 🟢 선택 |

---

## 5. 구현 순서 (개발 단계)

### Phase 1. 스케줄러 수정 (SC-01 ~ SC-08) 🔴 최우선

- [ ] `_start_scheduler()` 스레드 방식으로 교체
- [ ] `_stop_scheduler()` `stop_flag.set()` 방식으로 교체
- [ ] `_restart_scheduler()` 원자적 재시작
- [ ] `_fired_set` 키 형식 `|` 구분자로 변경
- [ ] interval 첫 실행 로직 수정 (즉시 실행 방지)
- [ ] `_restore_scheduler_on_startup()` 이식
- [ ] `_sync_scheduler()` 이식
- [ ] 스케줄 저장 즉시 반영

### Phase 2. App 스타일 헬퍼 추가 (UI-01 ~ UI-06) 🔴

- [ ] `_card()`, `_button()`, `_darken()` 추가
- [ ] `_label()`, `_badge()`, `_separator()` 추가
- [ ] 기존 직접 `tk.Button()` 호출을 `_button()` 헬퍼로 점진적 교체

### Phase 3. 헤더 + 사이드바 개선 (UI-07 ~ UI-09) 🔴

- [ ] 사이드바 `tk.Label` → `tk.Button` 전환
- [ ] `_switch_tab()` — bold/fg/bg 3중 변경
- [ ] 헤더 우측 `_queue_var` + `_sched_var` 추가
- [ ] 스케줄 상태 헤더 갱신 함수 연동

### Phase 4. JobsTab 개선 (UI-11 ~ UI-14) 🟡

- [ ] Treeview 태그 컬러링 (platform별)
- [ ] 스케줄 상태 아이콘 🟢/🟡/⚫/⚪ 통합
- [ ] 스케줄 상태 패널 추가 (하단)
- [ ] ETA 패널 — 멀티계정 Telethon 방식에 맞게 수정

### Phase 5. Telethon 엔진 통합 🔴

- [ ] `TelethonEngine` 클래스 신규 작성
- [ ] 계정별 세션 파일 관리
- [ ] `join_group()`, `send_message()` 비동기 구현
- [ ] 15계정 동시 스레드 실행
- [ ] 제재 탐지 (`FloodWaitError`, `PeerFloodError` 등) 처리
- [ ] 계정 상태 모니터 UI (상태 다이얼로그 또는 탭)
- [ ] 기존 `_run_telegram_join`, `_run_telegram_message` 라우팅 교체

### Phase 6. TemplateTab 리디자인 🟡

- [ ] 카드 단위 섹션 분리
- [ ] 접기/펼치기 Accordion UI
- [ ] 텔레그램 워크플로우: 좌표 섹션 → Telethon 계정 선택으로 교체
- [ ] 카카오 워크플로우: 좌표 섹션 기존 유지

### Phase 7. 도움말 팝업 (UI-10) 🟡

- [ ] `_HELP_DATA` 딕셔너리 정의 (모든 탭)
- [ ] `_show_help(tab_id)` 팝업 메서드 구현
- [ ] 각 탭 헤더에 `[❓ 도움말]` 버튼 추가

### Phase 8. 테스트 및 빌드

- [ ] 스케줄러 단위 테스트 (time 모드 / interval 모드 / 재시작 후 복원)
- [ ] Telethon 연결 테스트 (FloodWait 시뮬레이션 포함)
- [ ] 카카오 기존 기능 회귀 테스트
- [ ] PyInstaller 빌드 (`messenger_v161.spec`)
- [ ] `version.json` 업데이트 (1.61)
- [ ] GitHub 푸시

---

## 6. 파일 변경 사항

| 파일 | 변경 내용 |
|---|---|
| `messenger_allInOne_v1.60.py` → `messenger_allInOne_v1.61.py` | 전체 변경 적용 |
| `messenger_v160.spec` → `messenger_v161.spec` | 파일명 업데이트 |
| `version.json` | `"version": "1.61"` |

---

## 7. 버전 상수 변경

```python
APP_VERSION = "1.61"
APP_TITLE   = f"메신저 올인원 v{APP_VERSION}"
```

---

## 8. 향후 v1.62+ 고려 사항

- 계정별 발송 통계 분리 (StatsTab)
- Telethon 자동 재연결 로직 (네트워크 끊김 대응)
- 채널 블랙리스트 영구 저장 및 UI 관리
- 계정별 워밍업 자동 스케줄 (신규 계정 50→100→200→500)
- 카카오 오픈채팅 멀티계정 지원 (별도 분석 필요)
- 전체 발송 현황 대시보드 탭 추가
