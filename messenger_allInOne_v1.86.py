# ============================================================
# messenger_allInOne_v1.86  변경 이력
# ============================================================
#
# v1.86 (2026-04-21) ─── 작업 실행 시 workflow 템플릿 우선 적용 버그 수정
#
# [v1.86-1]  WorkflowExecutor — self.wk 결정 로직 수정
#   · 기존: job.get("workflow") 우선 → 작업 저장 시점의 workflow가 고정됨
#   · 수정: template.get("workflow") 우선 → 템플릿 변경 시 항상 반영됨
#   · 배경: 작업 생성 당시 메시지발송 템플릿 선택 → 나중에 그룹가입 복사본으로
#           템플릿만 교체했는데 job JSON의 workflow는 갱신 안 됨 → 여전히
#           telegram_message로 실행되는 버그 발생
#
# v1.85 (2026-04-21) ─── join_first FROZEN 즉시 감지 + message 루프 FROZEN 계정 추적
#
# v1.81 (2026-04-21) ─── 대화방 전송 권한 점검 기능
#
# [v1.81-1]  check_peer_permission send_media 항목 추가
#   · 텍스트 전송 가능 여부(send_messages) + 이미지/파일 전송(send_media) 동시 확인
#
# [v1.81-2]  대화방 목록 팝업 전송 권한 점검 UI
#   · Treeview에 텍스트/이미지 컬럼 추가 (—: 미점검, ✅: 가능, ❌: 불가)
#   · 🔍 선택 항목 점검 — 선택한 채팅방만 빠르게 점검
#   · 🔍 전체 점검 — 모든 채팅방 순차 점검 (백그라운드 스레드)
#   · 실시간 진행 상황 표시 (N/전체, ✅가능, ❌불가, 📎이미지만불가)
#   · 팝업 창 720x560으로 확장
#
# v1.80 (2026-04-21) ─── 대화방 목록 t.me 링크 추출 기능 추가
#
# [v1.80-1]  _show_dialogs 팝업 내 링크 추출/복사 기능
#   · 📋 선택 링크 복사 — Treeview에서 선택한 항목의 t.me URL만 복사
#   · 🌐 전체 링크 복사 — username이 있는 채팅방 전체 t.me URL 일괄 복사
#   · 추출 가능 링크 수 실시간 표시
#   · private 그룹(username 없음)은 자동 제외 안내
#
# v1.79 (2026-04-21) ─── UI/UX 버그 수정 + flood_threshold per-account 반영
#
# [v1.79-1]  flood_threshold per-account 엔진 반영
#   · _retry_run에 flood_threshold 파라미터 추가
#   · join_group / send_message 호출 시 acct["flood_threshold"] 읽어 전달
#   · 계정별 개별 FloodWait 임계값이 실제 엔진에 반영됨
#
# [v1.79-2]  LogTab 긴급 패널 UI 수정
#   · 초기 레이블에 이모지 포함 (🚨/🛑/🗑) — 일관성 통일
#   · _clear 시 긴급 카운터 및 패널 배경 리셋
#
# v1.78 (2026-04-21) ─── 로그 분석 기반 긴급 조치 기능 추가
#
# [v1.78-1]  없는 채팅방 자동 블랙리스트 (dead_links 영구 집합)
#   · Nobody is using / No user has / InvalidPeer → add_dead_link()
#   · join_group 진입 전 is_dead_link() 체크 → 즉시 스킵
#
# [v1.78-2]  FROZEN 계정 자동 감지 + 즉시 중단
#   · _handle_error: "frozen" 문자열 감지 → mark_frozen(phone)
#   · mark_frozen: _frozen_accounts 에 추가, status=ST_FROZEN, alert_fn 콜백
#   · join_group / _retry_run 진입 전 is_frozen() 체크 → 즉시 차단
#   · TelegramAccountsTab: 🚨 아이콘, 🔓 Frozen 해제 버튼
#
# [v1.78-3]  FloodWait 임계값 초과 당일 자동 중단
#   · _retry_run: FloodWait >= flood_threshold → mark_flood_stopped()
#   · 계정 설정 UI에 FloodWait 임계값 스피너 추가 (기본 600초)
#
# [v1.78-4]  일일 가입 횟수 한도 별도 제어 (frozen 예방)
#   · _join_cnt: 오늘 가입 횟수 독립 카운터
#   · 계정 설정 UI에 daily_join_limit 스피너 추가 (기본 50회)
#
# [v1.78-5]  계정 상태 체크 강화 (_check_account_status)
#   · get_me() 후 restriction_reason 에서 frozen 명시 확인
#   · 이미 frozen 마킹된 계정은 조회 없이 즉시 반환
#
# [v1.78-6]  t.me 링크 자동 추출기 (TelegramAccountsTab)
#   · 🔗 링크 추출 버튼 → 자유 형식 텍스트에서 t.me URL 추출
#   · https://t.me/xxx 형식으로 정규화 + 중복 제거 + 클립보드 복사
#
# [v1.78-7]  LogTab 긴급 조치 패널
#   · FROZEN/FloodWait/없는채팅방 실시간 카운터 표시
#   · ⏹ 전체 즉시 중단 / 🔍 ERROR만 보기 / 🗑 없는채팅방 목록 버튼
#
# [v1.78-8]  작업 완료 결과 리포트
#   · _jobs_on_job_done: 성공/실패/성공률/FROZEN/FloodStop/없는채팅방 요약
#   · LogTab에 박스 형태로 자동 출력
#
# v1.61 (2026-04-17) ─── Telethon 엔진 / UI 리디자인 / 스케줄 완전 수정
#
# ── 텔레그램 엔진 교체 (pyautogui → Telethon) ─────────────────
#
# [TG-1]  TelethonEngine 클래스 신규 (asyncio + threading)
#   · 15계정 동시 실행 (독립 스레드 + asyncio 이벤트 루프)
#   · 계정별 .session 파일 영구 저장
#   · join_group / send_message 비동기 구현
#
# [TG-2]  제재 탐지 및 자동 대응
#   · FloodWaitError  → n초 대기 후 재시도
#   · PeerFloodError  → 해당 계정 당일 중지
#   · UserBannedInChannel → 채널 블랙리스트 등록
#   · AccountBannedError  → 전체 중지 + 사용자 알림
#
# [TG-3]  계정 상태 모니터 UI (TelegramAccountsDialog)
#   · 계정별 상태: 🟢실행 / 🟡대기 / 🔴중지 / ⚫밴
#   · 계정별 일일 발송 수 + 비고 표시
#
# [TG-4]  TelegramAccountsTab 신규 탭 추가
#   · 계정 추가/수정/삭제 (API ID, API Hash, 전화번호)
#   · 일일 한도 설정 (기본 500건)
#   · 워밍업 모드 (신규 계정 50→100→200→500 자동 조절)
#
# [TG-5]  기존 _run_telegram_join / _run_telegram_message 라우팅
#   · 텔레그램 워크플로우 → TelethonEngine으로 전달
#   · 카카오 워크플로우 → 기존 pyautogui 유지
#
# ── UI 리디자인 (community_poster v5.20 벤치마킹) ──────────────
#
# [UI-1]  App 스타일 헬퍼 메서드 추가
#   · _card()      border 1px + padding 카드 컨테이너
#   · _button()    hover 효과 내장 버튼 (_darken 연동)
#   · _darken()    hover 색상 계산 (factor=0.85)
#   · _label()     중앙화 레이블
#   · _badge()     색상 배경 뱃지
#   · _separator() 수평/수직 구분선
#
# [UI-2]  헤더 우측 실시간 상태 레이블
#   · _queue_var: "실행 중 N개" 또는 "실행 없음"
#   · _sched_var: "🟢 스케줄 N개" / "스케줄 OFF"
#
# [UI-3]  사이드바 tk.Label → tk.Button 전환
#   · 활성 탭: fg white + bg sidebar_h + font bold
#   · 비활성: fg #94A3B8 + bg sidebar
#   · _switch_tab() 3중 강조 (font/fg/bg 동시)
#   · 텔레그램 계정 탭 추가 ("telegram_accounts")
#
# [UI-4]  Treeview 행 태그 컬러링
#   · kakao 행: #FEFCE8 배경 (노란 포인트)
#   · telegram 행: #EFF6FF 배경 (파란 포인트)
#   · running: #DBEAFE / success: #F0FDF4 / failed: #FEF2F2
#
# [UI-5]  도움말 팝업 _HELP_DATA 딕셔너리
#   · 각 탭 ❓ 버튼 → step/tips 구조 팝업
#
# [UI-6]  JobsTab 스케줄 상태 패널 추가 (하단)
#   · 작업별 스케줄 상태 + 다음 실행 시각 표시
#
# ── 스케줄러 완전 수정 (community_poster 방식 이식) ─────────────
#
# [SC-1]  threading.Event 기반 독립 데몬 스레드로 교체
#   · 기존 after() 체인 방식 완전 제거 → UI 블로킹 무관
#   · _sched_stop_flag (threading.Event) 로 중지 제어
#
# [SC-2]  _fired_set 키 구분자 | 로 변경
#   · 기존: "{name}_{date}_{time}" (name에 _ 포함 시 파싱 오류)
#   · 변경: "{hash}|{date}|{time}" (구분자 오염 완전 차단)
#
# [SC-3]  interval 모드 첫 실행 즉시 트리거 방지
#   · last_run이 당일이면 skip (재시작 후 중복 실행 방지)
#
# [SC-4]  _restore_scheduler_on_startup() 이식
#   · 앱 시작 시 enabled 작업 스케줄 자동 복원
#
# [SC-5]  _sync_scheduler() 이식
#   · 작업 추가/수정/삭제 후 스케줄 자동 동기화
#
# [SC-6]  스케줄 저장 즉시 재시작
#   · _save_job 후 _restart_scheduler() 호출 → 즉시 반영
#
# ── v1.61 실제 구현 완료 목록 (2026-04-17) ─────────────────────
#
# [IMPL-1]  SIDEBAR_TABS 에 ("telegram_accounts", "✈️  텔레그램 계정") 추가
#
# [IMPL-2]  Treeview 행 태그 색상 추가 (UI-4)
#   · kakao: #FEFCE8 배경 / telegram: #EFF6FF 배경
#   · running: #DBEAFE / success: #F0FDF4 / failed: #FEF2F2
#
# [IMPL-3]  _refresh_tv 플랫폼 태그 적용 (UI-4)
#   · 스케줄 상태 아이콘: ⚪⚫🟢🔵 + 시각/간격 표시
#   · 실행 상태(_run_status) 우선 → 플랫폼 태그 → disabled 순
#
# [IMPL-4]  _restore_scheduler_on_startup 구현 (SC-4)
#   · _load_jobs 완료 후 after(100) 으로 자동 호출
#   · schedule_on=True 인 작업 목록 수집 → _start_scheduler + 복원 로그
#
# [IMPL-5]  _sync_scheduler 구현 (SC-5)
#   · 작업 저장(_save_job) / 삭제(_del_job) 후 자동 호출
#   · 활성 스케줄 작업 0개면 스케줄러 중지, 1개 이상이면 재시작
#
# [IMPL-6]  헤더 _queue_var / _sched_var 실시간 업데이트
#   · 실행 시작(_run_job), 완료(_on_job_done) 시 queue_var 갱신
#   · _sync_scheduler / _restore_scheduler 에서 sched_var 갱신
#
# [IMPL-7]  _update_job_status 에 행 태그 동적 변경 추가 (UI-4)
#   · 실행 중 → running 태그, 완료 → success, 실패 → failed
#   · 중지/취소 → 플랫폼 원래 색으로 복원
#
# ── 기존 v1.60 이력 (유지) ─────────────────────────────────────
#
# v1.60 (2026-03-16) ─── ETA 예상시간 / 버그수정 3종 / v5.20 벤치마킹 보완
#
# ── ETA 예상 작업시간 / 종료시간 표시 ──────────────────────────
#
# [ETA-1] WORKFLOW_BASE_DURATION 상수 추가  (전역, PLATFORM_WORKFLOWS 직후)
#   · kakao_friend=90s  kakao_openchat=120s
#     telegram_join=60s  telegram_message=75s
#   · WORKFLOW_BASE_DURATION_DEFAULT = 90
#
# [ETA-2] _calc_single_job_duration(job) 유틸 함수 추가
#   · 우선순위: estimated_duration(사용자 설정) → last_duration(지수평활)
#              → WORKFLOW_BASE_DURATION + delay_avg + pre_delay_avg
#   · v1.60: pre_delay_min/max 반영 (v1.59 누락 수정)
#
# [ETA-3] _calc_queue_eta(jobs, engine_current_name) 유틸 함수 추가
#   · time 모드 + interval 모드 작업 모두 포함 (v1.59 누락 수정)
#   · interval: last_run + interval_h 기반 next_run 계산
#   · next_run 기준 정렬 후 순차 start/finish 계산
#   · 반환: [{"name","start","finish","dur_s","mode"}, ...]
#
# [ETA-4] ETA 패널 UI 추가  (_build_ui 내 진행바 하단)
#   · _eta_total_var  : "⏱ 예상 소요: N분 M초  (K개 작업)"
#   · _eta_finish_var : "🏁 예상 완료: HH:MM"
#   · ↻ 갱신 버튼    : _refresh_time_estimate() 수동 호출
#
# [ETA-5] _refresh_time_estimate() 메서드 추가  (JobsTab 클래스 내)
#   · 활성+스케줄ON 작업 대상 ETA 계산 후 레이블 갱신
#   · 작업 없으면 "-" 표시
#
# [ETA-6] ETA 자동 갱신 트리거 추가
#   · _load_jobs / _del_job / _dup_job / _save_job / _on_job_done 완료 후 호출
#
# [ETA-7] last_duration 지수평활 기록  (_jobs_on_job_done)
#   · α=0.3: new = elapsed×0.3 + old×0.7  (첫 실행이면 그대로)
#   · monotonic 클럭 기반 (_run_started_at 저장 시점 기준)
#
# [ETA-8] DEFAULT_SCHEDULE에 last_duration / estimated_duration 필드 추가
#   · last_duration:     0.0  ← 지수평활 실측값 (초)
#   · estimated_duration: 0.0 ← 사용자 직접 설정 (0=자동)
#
# ── 버그 수정 ──────────────────────────────────────────────────
#
# [BUG-N1] 자정 경계 중복 트리거 수정  (_jobs_scheduler_tick)
#   · 원인: fired_key 날짜가 now 기준 → 23:58 예약이 00:02에 실행되면
#           다른 날짜 키 생성 → _fired_set 미hit → 재실행
#   · 수정: schedule 시각 23:xx + 현재 00:xx 조건 시 전날 날짜 사용
#           fired_key = f"{name}_{_key_date}_{t}"
#
# [BUG-N2] 중복 작업명 영구 차단 버그 수정  (_save_job)
#   · 원인: _fired_set 키가 name 기반 → 동일 이름 두 번째 작업 영구 스킵
#   · 수정: _save_job 내 중복명 체크 + showwarning 다이얼로그
#           동일 이름 존재 시 저장 자체를 차단
#
# [BUG-N3] interval 모드 last_run 갱신 위치 수정
#   · 원인: tick 내부에서 last_run 갱신 → 큐 적재 시점 기록
#           → 작업 실행 전 10분이 지나버리는 문제
#   · 수정: tick에서 last_run 설정 완전 제거
#           _jobs_on_job_done 완료 콜백에서만 갱신
#
# ── v5.20 벤치마킹 보완 ────────────────────────────────────────
#
# [BENCH-1] _trigger_with_wait 패턴 적용
#   · engine.is_busy=True 시 wait_until_idle() 후 실행 (별도 스레드)
#   · interval 모드 자동 실행에 적용 → 이전 작업 완료 대기 보장
#   · _jobs_trigger_with_wait() 함수 추가 + monkey-patch 등록
#
# [BENCH-2] _log_scheduler_restore 추가
#   · 앱 시작 시 스케줄 복원 대상 작업명 로그 기록
#   · _jobs_log_scheduler_restore(job_names) 함수 추가 + monkey-patch 등록
#
# [BENCH-3] 50초 중복 가드 삽입  (_jobs_scheduler_tick, time 모드)
#   · time.monotonic() 기반 (시스템 클럭 변경 무관)
#   · _50sec_guard dict: fired_key → monotonic 타임스탬프
#   · 50초 이내 동일 fired_key 재진입 차단
#   · self._50sec_guard = {} 를 __init__에서 초기화
#
# [BENCH-4] DEFAULT_SCHEDULE 필드 확장 (ETA-8 과 동일)
#
# ── 자동 배포 연동 ─────────────────────────────────────────────
#
# [AUTO-1] auto_updater.check_update_async 연동
#   · 앱 시작 3초 후 백그라운드 스레드에서 GitHub Releases API 조회
#   · 신규 버전 발견 시 tkinter 다이얼로그 표시 (업데이트/나중에/건너뛰기)
#   · timeout=5초, 실패 시 조용히 무시 (앱 시작 지연 없음)
#   · auto_updater.py 미존재 시 ImportError 무시
#
# ══════════════════════════════════════════════════════════════
# v1.59 (2026-03-16) ─── 내부 검증용 (실제 배포: v1.60)
# ══════════════════════════════════════════════════════════════
#
# ── ETA 예상 작업시간 / 종료시간 (초기 구현) ──────────────────
#
# [V59-ETA-1] WORKFLOW_BASE_DURATION 상수 추가
#   · 위치: PLATFORM_WORKFLOWS 직후 (전역 상수)
#   · 값: kakao_friend=90s, kakao_openchat=120s,
#          telegram_join=60s, telegram_message=75s
#   · WORKFLOW_BASE_DURATION_DEFAULT = 90
#
# [V59-ETA-2] _calc_single_job_duration(job) 함수 추가
#   · 우선순위: estimated_duration → last_duration 지수평활 → 기본값
#   · ⚠ pre_delay 미반영 버그 있음 → v1.60 [ETA-2]에서 수정
#
# [V59-ETA-3] _calc_queue_eta(jobs, engine_current_name) 함수 추가
#   · time 모드 작업만 처리
#   · ⚠ interval 모드 누락 → v1.60 [ETA-3]에서 수정
#
# [V59-ETA-4] ETA 패널 UI 추가 (_build_ui 내 진행바 하단)
#   · _eta_total_var  : "⏱ 예상 소요: N분 M초  (K개 작업)"
#   · _eta_finish_var : "🏁 예상 완료: HH:MM"
#   · ↻ 갱신 버튼    : _refresh_time_estimate() 수동 호출
#
# [V59-ETA-5] _refresh_time_estimate() 메서드 추가 (JobsTab 내)
#   · 활성+스케줄ON 작업 대상 ETA 계산 → 레이블 갱신
#
# [V59-ETA-6] ETA 자동 갱신 트리거
#   · _load_jobs / _del_job / _dup_job / _on_job_done 완료 후 호출
#   · ⚠ _save_job 내 schedule_on 토글 후 갱신 누락 → v1.60 [P-17]에서 수정
#
# [V59-ETA-7] last_duration 지수평활 기록 (_jobs_on_job_done)
#   · α=0.3 / time.monotonic() 기반 elapsed 계산
#   · _run_started_at = time.monotonic() 저장 (_jobs_run_job 내)
#
# [V59-ETA-8] DEFAULT_SCHEDULE 필드 확장
#   · last_duration: 0.0  /  estimated_duration: 0.0 추가
#
# ── 버그 수정 (v1.59 적용) ─────────────────────────────────────
#
# [V59-BUG-N1] 자정 경계 중복 트리거 (부분 수정)
#   · fired_key 날짜 고정 로직 도입
#   · ⚠ 엣지케이스 잔존 → v1.60 [BUG-N1]에서 완전 수정
#
# [V59-BUG-N3] interval 모드 last_run 갱신 위치
#   · tick 내부 last_run 설정 제거
#   · _jobs_on_job_done 완료 콜백에서만 갱신하도록 변경
#
# ── v5.20 벤치마킹 보완 (v1.59 적용) ─────────────────────────
#
# [V59-BENCH-1] _trigger_with_wait 패턴 추가
#   · engine.is_busy=True 시 wait_until_idle() 후 실행
#   · 별도 daemon 스레드에서 대기 후 after(0) 으로 UI 스레드 복귀
#
# [V59-BENCH-2] _log_scheduler_restore 추가
#   · 앱 시작 시 스케줄 복원 작업명 LogTab에 INFO 기록
#
# [V59-BENCH-3] 50초 중복 가드 삽입 (time.time() 기반)
#   · ⚠ 시스템 클럭 변경 취약 → v1.60 [BENCH-3]에서 monotonic으로 교체
#
# [V59-BENCH-4] DEFAULT_SCHEDULE 필드 확장 (V59-ETA-8 동일)
#
# ── 자동 배포 연동 (v1.59 적용) ───────────────────────────────
#
# [V59-AUTO-1] auto_updater.check_update_async 연동
#   · 앱 시작 3초 후 백그라운드에서 GitHub Releases API 조회
#   · 신규 버전 발견 시 tkinter 다이얼로그 (업데이트/나중에/건너뛰기)
#   · timeout/폴백 미구현 → v1.60 [AUTO-1]에서 timeout=5 + 폴백 추가
#
# ── v1.59 미해결 이슈 (v1.60에서 수정) ───────────────────────
#   · BUG-N2 미구현: 중복 작업명 체크 없음 → v1.60 [BUG-N2]
#   · pre_delay ETA 미반영              → v1.60 [ETA-2]
#   · interval 모드 ETA 제외            → v1.60 [ETA-3]
#   · 50초 가드 time.time() 사용        → v1.60 [BENCH-3] monotonic 전환
#   · auto_updater 타임아웃 없음        → v1.60 [AUTO-1]
#   · schedule_on 토글 후 ETA 미갱신    → v1.60 [P-17]
#
# ══════════════════════════════════════════════════════════════
#
# v1.58 (2026-03-15) ─── 마이그레이션 통합 / 스레드 스케줄러 / 기본값 중앙화
#
# [CHANGE-X1] DEFAULT_SCHEDULE 딕셔너리 도입
#   · 위치: 전역 상수 (APP_VERSION 아래)
#   · days, schedule_on, schedule_mode, schedule_times, schedule_time
#     schedule_interval, interval_variance, enabled, last_run, last_run_date
#   · _CURRENT_MIG_VER = 10  (마이그레이션 최고 버전)
#   · _KR_TO_INT = {"월":0 … "일":6}  (요일 변환 테이블)
#
# [CHANGE-X2] _migrate_legacy_json() 전면 재작성
#   · MIGRATE-1:  safe read with encoding fallback (utf-8 → cp949 → latin-1)
#   · MIGRATE-2:  schedule_days(KR list) → days(int list) 변환
#   · MIGRATE-3:  DEFAULT_SCHEDULE 기반 누락 키 보충
#   · MIGRATE-4:  jobs.json 단일파일 → jobs/ 폴더 분리 (레거시)
#   · MIGRATE-5:  _migrated_version 플래그 기록
#   · MIGRATE-6:  stats.json 구조 검증 및 복구
#   · MIGRATE-7:  업그레이드 카운트 반환
#   · MIGRATE-8:  마이그레이션 전 .bak 자동 백업
#   · MIGRATE-9:  UTF-8 BOM 파일 처리
#   · MIGRATE-10: 스케줄 시각 포맷 검증 및 정제
#
# [CHANGE-X3] _show_migration_notice() 전역 함수 추가
#   · 업그레이드 카운트 > 0 시 팝업 표시 (MIGRATE-7 연결)
#   · 위치: _migrate_legacy_json 직후
#
# [CHANGE-X4] _check_time_match() 유틸리티 추가
#   · ±N분 허용 비교 (interval_variance 구현)
#
# [CHANGE-X5] 스케줄러 제어 함수 신규 (_jobs_stop/_start/_restart_scheduler)
#   · after-callback id 기반 안전한 after_cancel
#   · threading.Thread 기반 백그라운드 틱
#   · _jobs_restart_scheduler = stop + start 원자적 실행
#
# [CHANGE-X6] _jobs_scheduler_tick() 전면 재작성 (threading 기반)
#   · threading.Thread(daemon=True)로 백그라운드 실행
#   · 미실행 복구: ±interval_variance 분 허용
#   · 예외 격리: 작업 단위 try/except
#   · 30초 after-loop 유지 (메인스레드 재예약)
#
# [CHANGE-X7] monkey-patch 블록 갱신
#   · _stop_scheduler / _start_scheduler / _restart_scheduler 추가
#   · _scheduler_after_id 상태 변수 초기화
#
# [CHANGE-X8] JobsTab.__init__ 수정
#   · after(1_000, self._start_scheduler) 로 변경 (10초→1초)
#   · _scheduler_after_id = None 초기화
#
# [CHANGE-X9] _save_job setdefault 블록 전면 교체
#   · DEFAULT_SCHEDULE 기반 days/interval_variance/schedule_on 기본값
#   · 저장 후 self._restart_scheduler() 호출
#
# [CHANGE-X10] _edit_job days 보존
#   · dlg.result.setdefault("days", j.get("days", DEFAULT_SCHEDULE["days"]))
#
# [CHANGE-X11] _build_schedule_section 업데이트
#   · 숫자 인덱스 기반 _sched_day_vars (list of BooleanVar)
#   · 한글 라벨 유지, 숫자 인덱스로 저장
#   · variance StringVar 초기화 추가
#
# [CHANGE-X12] _build_sched_detail 전면 교체
#   · interval_variance 입력 필드 추가
#   · 끝에 self._toggle_sched() 강제 호출
#
# [CHANGE-X13] JobDialog._ok 전면 교체
#   · _sched_day_vars(list) 우선, _sched_days(dict) 폴백
#   · days = 숫자 인덱스 리스트
#   · interval_variance 수집 (_sched_variance StringVar)
#   · result 에 days + schedule_days(KR 하위호환) + interval_variance 포함
#
# [CHANGE-X14] _jobs_load_template_for_job WARNING 로그
#   · 템플릿 파일 미발견 시 logging.warning() 기록
#
# [CHANGE-X15] App.__init__ 마이그레이션 팝업 삽입
#   · _build_ui() 직후 _migrate_legacy_json() 호출 → 카운트>0 시 팝업
#
# [CHANGE-X16] interval_variance 연산 (_check_time_match 적용)
#   · time 모드: abs(now_min - target_min) <= variance 범위 허용
#
# [CHANGE-X17] 버전 문자열 갱신
#   · APP_VERSION: "1.57" → "1.58"
#
# v1.57 (2026-03-13) ─── 스케줄 요일 선택 / 복수 시각 / 팝업 버그 수정
# v1.56 (2026-03-13) ─── 스케줄러 실제 구동 + 로그 연동
#
# [핵심 문제] v1.55 까지 schedule_on / schedule_time / schedule_interval
#   데이터는 JobDialog 에서 저장되었으나,
#   실제로 스케줄을 확인·실행하는 백그라운드 루프가 전혀 없었음.
#   → schedule_on=True 작업이 자동 실행되지 않음
#   → 스케줄 트리거 없음 → 로그 탭 완전히 비어 있음
#   → 활성 토글(enabled)이 스케줄러와 미연결
#
# [CHANGE-S1] _jobs_scheduler_tick 신규 함수 (핵심)
#   · 위치: _jobs_load_template_for_job 아래, monkey-patch 블록 위
#   · 동작: tkinter self.after(30_000, ...) 기반 30초 폴링 루프
#           schedule_on=True & enabled=True 작업만 대상
#   · time   모드: schedule_time(HH:MM) == 현재시각(HH:MM)
#                 today last_run_date 비교로 하루 1회 중복 실행 방지
#   · interval 모드: (now - last_run) 경과시간 >= schedule_interval 시간
#                    last_run="" (첫 실행) → 즉시 실행
#   · 실행 트리거 시 LogTab 에 [스케줄] INFO 로그 기록
#   · try/except 로 전체 감싸 오류 시 ERROR 로그 후 재예약 유지
#
# [CHANGE-S2] JobsTab.__init__ 스케줄러 시작
#   · self._engine.start() 아래에 self.after(10_000, self._scheduler_tick) 추가
#   · 앱 시작 10초 후 첫 틱 — UI 로드 완료 시점 보장
#
# [CHANGE-S3] _save_job last_run 기본값 추가
#   · data.setdefault("last_run",      "")  ← interval 경과시간 계산
#   · data.setdefault("last_run_date", "")  ← time 중복 실행 방지
#
# [CHANGE-S4] _jobs_on_job_done 완료 시 last_run 갱신 + JSON 저장
#   · 완료 시 last_run = now.strftime("%Y-%m-%d %H:%M:%S")
#   · last_run_date = now.strftime("%Y-%m-%d")
#   · 개별 JSON 파일에 저장 (_file / _status 키 제거 후)
#   · 재시작 후에도 interval 스케줄 이어받기 가능
#
# [CHANGE-S5] monkey-patch 블록에 _scheduler_tick 추가
#   · JobsTab._scheduler_tick = _jobs_scheduler_tick
#
# [CHANGE-S6] _jobs_toggle_job schedule_on=False 경고 메시지 개선
#   · 스케줄 미설정 작업을 활성화 시 상태바에 경고 안내
#   · "스케줄 미설정 — 수동 실행만 가능" 메시지 표시
#
# [CHANGE-S7] 버전 문자열 전체 갱신
#   · APP_VERSION: "1.55" → "1.56"
#   · 파일명·헤더·변경이력테이블·로그인 타이틀 동기화
#
# v1.55 (2026-03-12) ─── UI 개선: 활성 토글 / 안내 카드
#
# [A] 활성화 토글 기능 추가 (CHANGE-A1 ~ A6)
#   · 이전(v1.54): 모든 작업이 항상 활성 상태 — 비활성화 방법 없음
#     → "전체 실행" 시 비활성화하고 싶은 작업도 무조건 실행됨
#   · 변경: 작업별 "enabled" 플래그 도입
#     → JOBS_DIR의 개별 JSON 파일에 "enabled": true/false 저장
#     → 재시작 후에도 활성화 상태 유지 (영구 저장)
#     → "⊙ 활성 토글" 버튼: 선택 작업의 활성/비활성 즉시 전환
#     → Treeview "활성" 컬럼: ✓ 활성 / ✗ 비활성 표시
#     → 비활성 행: foreground PALETTE["muted"](#475569) + bg #F8F9FA
#     → "전체 실행": enabled=False 작업 자동 스킵
#     → 활성 작업이 0개이면 경고 다이얼로그 표시 후 실행 중단
#   · community_poster v5.20 활성 토글 패턴 벤치마킹 적용
#   · 관련 코드:
#       JobsTab._build_ui()     : 툴바 토글 버튼(CHANGE-A1), cols/headers(CHANGE-A2),
#                                 tag_configure(CHANGE-A3)
#       JobsTab._refresh_tv()   : values 7개 + row_tag 적용 (CHANGE-A4)
#       _jobs_toggle_job()      : 토글 함수 신규 (CHANGE-A5)
#       _jobs_run_all()         : enabled 필터링 추가 (CHANGE-A6)
#       JobsTab._toggle_job     : monkey-patch 연결
#
# [B] 인라인 안내 카드 추가 (CHANGE-B)
#   · 이전(v1.54): ❓ 도움말 버튼 클릭 시만 안내 내용 확인 가능
#   · 변경: 툴바 아래 Treeview 위에 항상 노출되는 파란 안내 카드 삽입
#     → 배경 #EFF6FF / 테두리 #BFDBFE / 텍스트 #1D4ED8
#     → 내용: "작업 = 템플릿 + 대상 목록" 정의 + 활성 토글 설명
#     → community_poster v5.20 팁 카드 배색 벤치마킹
#   · 관련 코드: JobsTab._build_ui() tip_frame (툴바 pack 직후)
#
# [C] _save_job enabled 기본값 보장 (CHANGE-C)
#   · 이전(v1.54): 신규 작업 저장 시 "enabled" 키 미포함
#     → 기존 JSON에 키 없으면 _refresh_tv에서 j.get("enabled", True) 폴백
#     → 하지만 저장 파일에 키 자체가 없어 명시적 상태 관리 불가
#   · 변경: _save_job() 첫 줄에 data.setdefault("enabled", True) 추가
#     → 신규·복제 작업 저장 시 항상 "enabled": true 포함
#     → 기존 JSON(키 없음)도 최초 저장 시 자동 추가
#   · 관련 코드: JobsTab._save_job()
#
# [D] _edit_job 수정 시 enabled 상태 보존 (CHANGE-D)
#   · 이전(v1.54): JobDialog.result dict에 "enabled" 키 없음
#     → 작업 수정 후 저장 시 기존 enabled=False 작업이 True로 리셋
#     → 비활성화해둔 작업이 수정 후 자동 활성화되는 버그
#   · 변경: _edit_job()에서 dlg.result.setdefault("enabled", j.get("enabled", True))
#     → 수정 전 기존 enabled 값을 그대로 보존
#   · 관련 코드: JobsTab._edit_job()
#
# v1.54 (2026-03-11) ─── 작업관리 구조 전면 개선 (큐 기반 단일 워커)
#
# [A] PostingEngine 클래스 신규 (queue.Queue + 단일 worker 스레드)
#   · 이전(v1.53): JobWorker(threading.Thread)를 작업마다 생성하는 멀티워커 구조
#     → dict[str, Thread]/_stop_events 로 관리, 동기화 프리미티브 전혀 없음
#     → pyautogui(마우스·키보드)는 단일 물리 자원이므로 동시 실행 시 충돌
#     → 실제로는 _run_all 내부에서 순차 실행하도록 조정했으나 구조와 불일치
#   · 변경: queue.Queue + 단일 worker 스레드로 직렬 처리 (동시 실행 원천 차단)
#     → PostingEngine._worker 루프가 q.get() → WorkflowExecutor.run() 반복
#     → add_task() 로 큐 추가만 하면 worker 가 순서대로 소비
#   · _busy/_idle threading.Event 쌍으로 엔진 상태 외부 관찰 가능
#   · _current_name / _current_stop 으로 현재 실행 작업 실시간 추적
#   · cancel_job(name): 대기 중이면 _cancelled set 등록 → worker skip
#                       실행 중이면 _current_stop.set() 으로 즉시 중단
#   · community_poster v5.20 큐 패턴 벤치마킹 적용
#   · 관련 코드: class PostingEngine (파일 하단 monkey-patch 블록 위)
#
# [B] _sleep_or_stop() 헬퍼 추가 (WorkflowExecutor 메서드)
#   · 이전(v1.53): 68개 time.sleep() 호출이 blocking 대기
#     → stop 신호 발생 시 남은 sleep 시간 동안 응답 없음 (최대 7초 대기)
#   · 변경: 0.1 s 단위로 _stop Event 를 polling 하는 인터럽트 가능 sleep
#     → stop 신호 감지 즉시 True 반환, 호출부에서 return 으로 즉시 중단
#     → 기존 time.sleep(x) → if self._sleep_or_stop(x): return 패턴
#   · 반환값: True = 중단됨, False = 정상 완료 (호출부에서 분기 가능)
#   · 관련 코드: WorkflowExecutor._sleep_or_stop() (_jitter 바로 아래)
#
# [C] time.sleep() → _sleep_or_stop() 교체
#   · 이전(v1.53): 실행 함수 내 time.sleep() 호출 다수
#   · 변경: 아래 위치 전부 _sleep_or_stop() 으로 교체 (총 16곳 적용)
#       _run_kakao_friend     : 재시도 대기(1.5s), 채팅 간격(_jitter())
#       _run_kakao_openchat   : oc_after_open / oc_after_click(×2) /
#                               oc_after_type / oc_after_send /
#                               oc_after_close / gap_t (타일 간격)
#       _run_telegram_join    : tg_between(random) / tg_chrome_load /
#                               tg_join_click / tg_telegram_open
#       _run_telegram_message : tg_chrome_load(×2) / tg_between(random×2)
#   · 계획서 11곳 대비 실제 16곳 적용 (추가 누락 없이 전부 교체 완료)
#   · 관련 코드: 각 _run_* 메서드 내 # BUG-03 fix 주석 위치
#
# [D] BUG-01 수정: _stop_all 후 재실행 시 작업이 영구 스킵되는 문제
#   · 원인(v1.53): _jobs_stop_all() 이 _stop_events dict 를 clear 하지 않음
#     → 다음 실행 시 _jobs_run_job() 에서 키 존재 여부를 is_alive() 없이 체크
#     → 이미 종료된 stop event 가 남아 있어 "이미 실행 중" 판단 후 skip
#   · 수정: PostingEngine 구조 전환으로 _stop_events dict 자체가 제거됨
#     → _stop_all() 시 engine.stop() + self._cancelled_jobs.clear() 로 완전 초기화
#   · 관련 코드: _jobs_stop_all()
#
# [E] BUG-02 수정: 중지 후 재실행 불가 (스레드 종료 미대기)
#   · 원인(v1.53): is_alive() True → "이미 실행 중" 메시지 후 return
#     → stop 이벤트 설정 후 스레드가 종료될 때까지 join() 미호출
#     → 사용자가 중지 버튼 → 바로 재실행 누르면 이전 스레드가 살아있어 skip
#   · 수정: 단일 워커 구조로 전환 → 스레드 충돌 구조 자체가 제거됨
#     → 실행 중 작업은 engine._current_name 으로만 확인, stop 후 다음 큐 작업 자동 진행
#   · 관련 코드: PostingEngine._worker() 루프
#
# [F] BUG-03 수정: time.sleep() 중 stop 신호 무시
#   · 원인(v1.53): blocking time.sleep() 사용 — [B][C] 항목으로 통합 수정
#   · 수정 결과: stop 버튼 클릭 후 최대 0.1 s 내 실행 중단 (체감 즉시 반응)
#
# [G] BUG-04 수정: 실행 경로에서 _migrate_template() 미호출
#   · 원인(v1.53): TemplateTab._load_templates() → _migrate_template() 호출
#     → UI 탭에서 템플릿 목록 로드 시는 마이그레이션 적용
#     → 그러나 _jobs_load_template_for_job() 는 직접 JSON 읽어 변환 없이 반환
#     → v1.52 이전 템플릿(action_delay, column_gap 등 구 키) 실행 시 KeyError/오동작
#   · 수정: _jobs_load_template_for_job() 내 JSON 로드 직후
#     TemplateTab._migrate_template(d) 호출 1줄 추가
#   · 효과: v1.52 이전 JSON 파일 수정 없이 그대로 사용 가능 (인메모리 변환)
#   · 관련 코드: _jobs_load_template_for_job() # BUG-04 fix 주석
#
# [H] _cancelled_jobs set 추가 (JobsTab 멤버)
#   · 목적: PostingEngine 과 JobsTab 이 동일 set 객체 공유
#     → cancel_job(name) 호출 시 set 에 등록 → worker 가 큐에서 꺼낼 때 skip
#     → engine.stop() / _stop_all() 시 clear() 로 완전 초기화
#   · 관련 코드: JobsTab.__init__() self._cancelled_jobs / PostingEngine.__init__()
#
# [I] JobWorker 클래스 제거
#   · 이전(v1.53): class JobWorker(threading.Thread) — 작업 1개당 스레드 1개
#   · 제거 이유: PostingEngine 내부의 단일 worker 스레드가 동일 역할 수행
#     → 불필요한 스레드 생성·관리 코드 25줄 제거
#
# [J] _jobs_run_job_sync() 제거
#   · 이전(v1.53): _run_all() 내부에서 done_event.wait() 로 순차 처리하기 위해 사용
#   · 제거 이유: PostingEngine 이 큐 기반 단일 워커로 순차 처리 보장
#     → 별도 동기 버전 함수 불필요 (40줄 제거)
#
# [K] 중지 버튼 동작 개선 (CHANGE-18)
#   · 이전(v1.53): ⏹ 중지 버튼 → 항상 _stop_all() (전체 중지만 가능)
#   · 변경: Treeview 에서 작업 선택 중이면 → _stop_job() (개별 중지)
#           선택 없으면 → _stop_all() (전체 중지)
#   · _stop_job(): engine.cancel_job(name) 호출 → 대기/실행 모두 즉시 처리
#   · 관련 코드: JobsTab._build_ui() 중지 버튼 lambda / _jobs_stop_job()
#
# v1.53 (2026-03-11) ─── 딜레이 설정 UI 플로우 기반 재구성
#
# [A] 카카오 오픈채팅 딜레이 설정 UI 전면 개선 (_render_timing_section)
#   · 기존: 채팅창 단계 / 전송닫기 단계 / 타일 간격 — 그룹 라벨 3줄
#   · 변경: 실제 동작 순서 기반 단계별 row 6개
#       ① 채팅방 더블클릭 → 창 열림      (oc_after_open,  열림 대기)
#       ② 입력창 클릭/포커싱 → 활성화    (oc_after_click, 클릭/포커싱 후)
#       ③ 메시지 입력 → 완료             (oc_after_type,  입력 후)
#       ④ 전송(Enter/버튼) → 완료        (oc_after_send,  전송 후)
#       ⑤ 창 닫기 → 완전히 닫힘          (oc_after_close, 닫힘 후 / 이중전송 방지)
#       ⑥ 다음 채팅방으로 이동           (between_chats ± between_jitter)
#   · 구분선(──)으로 채팅방 진입 / 전송·닫기 / 다음 채팅방 3구역 분리
#   · "클릭후" → "클릭/포커싱 후" 라벨 변경 (의미 명확화)
#
# [B] 변수명·저장키·실행 로직 100% 유지
#   · self._oc_after_open/click/type/send/close 변수명 동일
#   · self._between_chats_var / _jitter_val_var 동일
#   · _save_template / _run_kakao_openchat 코드 수정 없음
#

# ============================================================
# v1.52 (2026-03-11) ─── 딜레이 세분화 / 이중전송 버그수정 / 좌표계산 통일
#
# [A] 카카오 오픈채팅/아침인사/가망뿌리기 딜레이 세분화 (oc_ 접두사)
#   · 기존 action_delay(1개) → 7개 독립 설정으로 분리
#       oc_after_open  (기본 1.5s) : 더블클릭 후 채팅창 열림 대기
#       oc_after_click (기본 0.3s) : 입력창 클릭/포커스 후 대기
#       oc_after_type  (기본 0.3s) : 메시지 입력 완료 후 대기
#       oc_after_send  (기본 1.0s) : 전송 후 대기
#       oc_after_close (기본 0.8s) : 창 닫기 후 대기 (이중전송 방지 핵심)
#       between_chats  (기본 0.5s) : 다음 채팅방 이동 전 간격
#       between_jitter (기본 0.3s) : 간격 ± 랜덤 지터
#   · 이유: 단일 action_delay로는 채팅창 열림/전송/닫힘 타이밍
#     불일치로 인한 중복전송·좌표누락 오류 발생
#   · 하위호환: 기존 action_delay가 있으면 oc_after_open/oc_after_send
#     기본값으로 자동 마이그레이션
#
# [B] 이중전송 버그 수정
#   · 원인: oc_after_close 부재 → 이전 창이 닫히기 전에 다음 더블클릭
#     → 같은 방에 두 번 발송
#   · 수정: oc_after_close 적용 + _last_sent_coord 가드 추가
#     (동일 좌표 연속 클릭 시 WARNING 로그 출력)
#
# [C] 좌표 계산 로직 수정 (calculate_coordinates)
#   · 기존: column_gap 파라미터로 X간격 계산
#   · 변경: cell_width 파라미터로 통일 (카카오 플로팅 가로 슬롯 크기)
#     x = start_x + col * cell_width  (기존 column_gap 로직과 동일)
#   · 이유: UI에서 cell_width(가로)와 column_gap(열간격)을 별도 입력하는
#     구조가 혼란을 유발함 → cell_width=열간격으로 단일화
#   · 하위호환: _run_kakao_openchat에서 column_gap 값이 있으면 cell_width
#     fallback으로 사용
#
# [D] 그리드 셀 크기 UI 개선
#   · 가로 라벨을 "가로(열간격):" 으로 변경 → cell_width = 열 간격임을 명확히 표시
#   · 1칸 크기 가로/세로 입력 변경 시 미리보기 즉시 자동 갱신
#   · 플로팅 모드 라디오버튼 제거 (고정값이 아닌 자유 입력 방식 유지)
#   · 셀 기본값 수정: cell_width 0 → 46px, cell_height 0 → 38px
#     (카카오 플로팅 접힘 모드 실측값 기준, 기존 30.8 오류 정정)
#     신규 템플릿 생성 시 미리 채워지므로 사용자가 직접 입력하지 않아도 됨
#
# [E] 그리드 좌표 무제한 보장
#   · row_count 기본값: 5 → 1 (사용자가 직접 설정)
#   · column_gap 입력란 제거 → cell_width(가로) 값을 열간격으로 사용
#   · 미리보기: 첫 좌표 + 마지막 좌표 + 총 N개 표시
#   · 열/행 설정에 제한 없음 (이전 하드코딩 20개 제한 완전 제거)
#
# [F] 로그 상세화
#   · _run_kakao_openchat: 각 단계별 상세 로그
#       ① 더블클릭 좌표 출력
#       ② 채팅창 열림 대기 시간 출력
#       ③ 입력창 클릭/포커스 방식 출력
#       ④ 메시지 입력 글자수 출력
#       ⑤ 전송 방식 출력
#       ⑥ 이미지 첨부 단계별 좌표·딜레이 출력
#       ⑦ 창 닫기 방식·딜레이 출력
#       ⑧ 다음 방 이동 전 대기시간 출력
#   · _drag_drop_image: 소스좌표/드롭좌표/각 딜레이 단계별 로그
#
# [G] 템플릿 마이그레이션 (_migrate_template)
#   · _load_templates() 시 자동 호출
#   · kakao_openchat 템플릿:
#       - action_delay → oc_after_open / oc_after_send 자동 변환
#       - 신규 oc_ 키 누락 시 기본값 채움
#       - grid_config.column_gap → grid_config.cell_width 자동 변환
#   · 파일은 수정하지 않음 (인메모리 변환만 수행, 저장 시 반영)
#
# [H] 파일명·내부 버전 v1.51 → v1.52 동기화
# ============================================================

# ============================================================
# messenger_allInOne_v1.57
# 구조: 작업 템플릿 관리 → 작업 관리 → 로그/통계/설정
# ------------------------------------------------------------
# 업데이트 히스토리:
#   v1.58 | 2026-03-15 00:00 | 마이그레이션 통합·스레드 스케줄러·기본값 중앙화 (CHANGE-X1~X17)
#   v1.57 | 2026-03-13 00:00 | 스케줄 요일·복수시각·팝업버그 수정 (CHANGE-W1~W11)
#   v1.56 | 2026-03-13 00:00 | 스케줄러 실제 구동, 로그 연동 (CHANGE-S1~S7)
#   v1.55 | 2026-03-12 00:00 | 활성 토글, 안내 카드, enabled 보존 (CHANGE-A~D)
#   v1.54 | 2026-03-11 00:00 | PostingEngine 큐 기반 단일 워커, BUG-01~04 수정
#   v1.53 | 2026-03-11 00:00 | 카카오 오픈채팅 딜레이 설정 UI 전면 재구성
#   v1.52 | 2026-03-11 00:00 | 딜레이 세분화, 이중전송 버그수정, 좌표계산 통일
#   v1.51 | 2026-03-10 00:00 | Google Sheet CSV 로그인 추가
#   v1.00 | 2026-03-05 00:00 | 최초 릴리즈
#   v1.01 | 2026-03-05 12:00 | 이미지 첨부 순서(전/후) 선택 추가
#                              전송 방식(좌표/Enter) 선택 추가
#                              닫기 방식(좌표/ESC) 선택 추가
#                              친추 ID = 키워드+시작순번 방식으로 교체
#                              UI/UX 가독성 개선
#   v1.02 | 2026-03-05 17:00 | [버그픽스] _toggle_image_path 메서드 누락 복구
#                              [버그픽스] 작업유형/플랫폼 변경 시
#                              전송·닫기 방식 섹션 미갱신 수정
#   v1.03 | 2026-03-05 18:00 | 코드 상단에 전체 구조 맵 주석 추가
#                              (클래스·메서드·상수·흐름 한눈에 파악 가능)
#   v1.04 | 2026-03-05 20:00 | [기능추가] 이미지 소스/드롭 좌표 설정 UI 추가
#                              [기능추가] 이미지 드래그앤드롭 딜레이 설정
#                              [기능추가] 타이밍 설정 섹션 (단계딜레이/타일간격/지터)
#                              [기능추가] 카카오 그리드 좌표 자동 계산 섹션
#                              [기능추가] 전송방식 Ctrl+Enter 옵션 추가
#                              [기능추가] 닫기방식 Alt+F4 옵션 추가
#                              [기능추가] 전송 후 창닫기 여부 토글 추가
#                              [기능추가] calculate_coordinates() 유틸 함수 추가
#                              [개선] _drag_drop_image → kakao_drag_drop 방식으로 개선
#                              [통합] 오픈채팅/아침인사/가망뿌리기로 통합
#   v1.05 | 2026-03-05 21:00 | [버그픽스] 작업유형 전환 시 TclError 수정
#                              _toggle_image_path 중간 호출 제거
#                              winfo_exists() 방어 코드 추가
#   v1.06 | 2026-03-05 22:00 | [UX개선] 대상CSV·메시지를 JobDialog→TemplateTab으로 이동
#                              [간소화] 작업관리(JobDialog)는 스케줄 설정 전용으로 변경
#                              [신규] 템플릿에 _render_target_section 추가
#                              [신규] 템플릿에 _render_message_section 추가
#                              [개선] WorkflowExecutor: target_file/message tmpl 우선 읽기
#   v1.07 | 2026-03-05 23:00 | [UI전면개편] 색상 팔레트 / 폰트 체계 완전 재설계
#                              [개선] 섹션 헤더·카드·버튼·입력창 스타일 통일
#                              [개선] 사이드바 탭 가독성, Treeview 스타일 개선
#                              [개선] 폰트 상수 F_TITLE/F_BODY/F_LABEL/F_SMALL/F_MONO 도입
#   v1.08 | 2026-03-06 00:00 | [색상개선] 인디고 기반 다크 테마로 전면 재설계
#                              배경 순검정→채도 있는 딥 인디고 (가독성 대폭 향상)
#                              보색 원리 적용: primary(보라) ↔ accent(황금)
#                              muted 텍스트 인디고 틴트 → 배경과 자연스러운 조화
#                              [폰트] 하드코딩 폰트 완전 제거, 상수 통일
#                              F_SMALL/F_BTN_S 8pt→9pt (가독성 개선)
#                              F_ICON(이모지), F_MONO_B(굵은 모노) 추가
#   v1.09 | 2026-03-06 01:00 | [가독성] muted 텍스트 대비비 3.2→5.5:1 개선
#                              text2 #9499C4→#B2B8DC, muted #6B7099→#9499C4
#                              힌트/설명 텍스트 전 영역 WCAG AA 기준 충족
#   v1.10 | 2026-03-06 02:00 | [테마전환] 다크→라이트 테마 전면 전환
#                              community_poster v5.20 팔레트 벤치마킹
#                              bg/card 라이트화, 사이드바 다크 슬레이트 유지
#                              포인트색: Tailwind blue/green/amber/red/violet
#                              카카오 #FEE500 · 텔레그램 #229ED9 원색 유지
#   v1.11 | 2026-03-06 03:00 | [가독성] 라이트 테마 전수 대비비 검토 & 수정
#                              card/bg 위 fg=success(2.3:1)→success_text(7.4:1)
#                              sidebar 위 fg=text2/muted/primary→sidebar_text
#                              primary/danger 버튼 fg→#FFFFFF
#                              bg/card 위 fg=muted→text2 (47건 충돌 해소)
#   v1.12 | 2026-03-06 04:00 | [가독성2] 잔여 충돌 10건 추가 해소
#                              success_text #16A34A→#15803D (card 위 5.0:1)
#                              primary #3B82F6→#2563EB (흰글 5.2:1)
#                              danger  #EF4444→#DC2626 (흰글 4.8:1)
#                              hover 위 text2→text (대비 4.3→13.3:1)
#                              [개선] 섹션 헤더·카드·버튼·입력창 스타일 통일
#                              [개선] 사이드바 탭 가독성, Treeview 스타일 개선
#                              [개선] 폰트 상수 F_TITLE/F_BODY/F_LABEL/F_SMALL/F_MONO 도입
#   v1.13 | 2026-03-06 05:00 | [가독성3] WCAG 대비비 전수 패치
#                              muted #6B7EA0→#475569 (card 위 4.1→7.6:1, AAA)
#                              warning_text #B45309 팔레트 신규 추가
#                              Treeview SUCCESS/WARN 태그 고대비 색상으로 교체
#                              Treeview 헤딩 fg text2→sidebar_text (3.1→13.4:1)
#                              sidebar muted→sidebar_text (3.6→13.4:1)
#   v1.14 | 2026-03-06 06:00 | [가독성4] 라이트 배경 회색 텍스트 전면 제거
#                              라이트 배경 text2/muted fg 73건 → text(#1E293B) 일괄 교체
#                              라이트 배경 대비 실패 0건 달성
#   v1.15 | 2026-03-06 07:00 | [가독성5] 잔여 text2/muted fg 완전 제거
#                              Treeview.Heading fg text2→sidebar_text
#                              INFO 태그 fg muted→text
#                              전체 회색 텍스트 사용처 0건 달성
#   v1.16 | 2026-03-06 08:00 | [기능개편] 카카오 친구추가 kakao_friendbot_v3.0 기준 동기화
#                              CSV: 이름/번호 → 카카오아이디 단일 컬럼으로 변경
#                              OCR 전처리 강화 (그레이스케일+3× 스케일업)
#                              상태 판별 3단계 fuzzy 매칭 적용
#                              친추 후 가망N 이름 자동 부여 시퀀스 추가
#                              (Tab×2+Enter→채팅→프로필→Tab×6→이름입력→확인→닫기)
#   v1.17 | 2026-03-06 09:00 | [UI텍스트] CSV 필수 컬럼 힌트 업데이트
#                              도움말 ⑧항: "이름/번호 패턴 설정" →
#                              "OCR 영역 설정 (CSV: 카카오아이디 컬럼만 필요)"
#   v1.18 | 2026-03-06 10:00 | [기능추가] 대상 목록 섹션 예시 CSV 다운로드 버튼
#                              SAMPLE_CSV_DATA 전역 상수 추가 (6개 워크플로우)
#                              📥 예시 파일 버튼 → 작업 유형에 맞는 CSV 자동 생성
#                              _download_sample_csv 메서드 추가
#   v1.19 | 2026-03-06 11:00 | [기능추가] 워크플로우별 딜레이 설정 UI 완성
#                              ┌ 카카오 친구추가 (원본: kakao_friendbot_v3.0)
#                              │   after_ctrlA  : Ctrl+A 후 대기  (기본 2.0s)
#                              │   after_click  : 좌표 클릭 후 대기 (기본 1.5s)
#                              │   after_input  : ID 입력 후 대기  (기본 2.5s)
#                              │   after_ocr    : OCR 판독 전 대기 (→v1.24에서 after_color_wait로 교체)
#                              │   after_tab    : Tab 키 후 대기   (기본 0.5s)
#                              │   between_chats: ID 간 간격       (기본 1.0s)
#                              │   between_jitter: ±랜덤 오차      (기본 0.3s)
#                              ├ 텔레그램 3종 (원본: TelegramAllInOne_v2)
#                              │   tg_chrome_load   : Chrome 로딩 대기  (기본 2.0s)
#                              │   tg_telegram_open : 앱 전환 대기      (기본 1.5s)
#                              │   tg_join_click    : 가입 클릭 후 대기 (기본 2.0s)
#                              │   tg_after_type    : 메시지 입력 후    (기본 0.5s)
#                              │   tg_after_send    : 전송 후 대기      (기본 1.0s)
#                              │   tg_after_back    : 뒤로가기 후 대기  (기본 0.8s)
#                              │   tg_between_min   : 링크 간 최소 대기 (기본 3.0s)
#                              │   tg_between_max   : 링크 간 최대 대기 (기본 7.0s)
#                              ├ _render_timing_section: wk 분기로 항목 자동 전환
#                              │   kakao_openchat → 단계딜레이/타일간격/지터
#                              │   kakao_friend           → 단계타이밍 5종 + 간격/지터
#                              │   telegram_*             → 로딩/전환/클릭 + 메시지 3종
#                              │                            + 링크 간격(min/max)
#                              ├ _save_template: 워크플로우별 딜레이 키 JSON 저장
#                              └ 텔레그램 실행 함수 하드코딩 sleep
#                                → tmpl.get('tg_*') 로 전면 교체
#   v1.20 | 2026-03-06 12:00 | [주석개선] 업데이트 이력 & 구조 맵 상세화
#                              v1.19 이력: 딜레이 키/기본값 전체 명시
#                              구조 맵 _save_template 저장 필드:
#                              친추 딜레이 5키 + 텔레그램 딜레이 8키 추가
#                              구조 맵 WorkflowExecutor 딜레이 파라미터 명시
#   v1.21 | 2026-03-06 13:00 | [버그수정] 전체 코드 디버깅 & 검수
#                              [BUG-01] _click() 헬퍼 timing 중간 dict 버그
#                                       tmpl.get("timing",{}).get("after_click")
#                                       → tmpl.get("after_click", 0.3) 직접 읽기
#                              [BUG-02] _save_template에서 미정의 _id_pattern_var
#                                       호출 → AttributeError 수정
#                                       (id_pattern은 v1.16에서 제거된 필드)
#                              [BUG-03] _save_template 내 미사용 wk_save
#                                       dead code 제거
#                              [BUG-04] 친추 Ctrl+A 후 sleep(0.15) 하드코딩
#                                       → timing["after_ctrlA"] 로 교체
#                              [BUG-05] message_input 클릭 후 중복 sleep(0.3)
#                                       제거 (kakao_openchat)
#                              [BUG-06] _run_kakao_openchat rows 빈 체크 누락
#                                       → if not rows: return 추가
#                              [BUG-07] _run_telegram_join rows 빈 체크 누락
#                                       → if not rows: return 추가
#   v1.22 | 2026-03-06 14:00 | [기능추가] 대상 목록 직접 입력 모드
#          |                  |   - kakao_friend / telegram_* 워크플로우에
#          |                  |     📂 CSV 파일 / ✏️ 직접 입력 라디오 토글 추가
#          |                  |   - 직접입력: Text 위젯 (7줄, 스크롤바)
#          |                  |   - 줄 수 카운트 실시간 표시
#          |                  |   - target_mode / target_direct JSON 저장
#          |                  |   - WorkflowExecutor._read_targets() 통합 함수 추가
#   v1.23 | 2026-03-06 15:00 | [버그수정] v1.22 검수 결과 반영
#   v1.24 | 2026-03-06 16:00 | [기능개편] 카카오 친추 로직 OCR→색상탐지 전면교체
#   v1.25 | 2026-03-06 17:00 | [버그수정] 친추 공통 로직 순서 교정
#          |                  |   - ID 입력 후 Enter 추가 (검색 실행)
#          |                  |   - 색상 탐지 클릭 제거 → 픽셀 읽기만
#          |                  |   - 순차 탐지: status_dot 먼저 → 흰색이면 friend_add_btn
#          |                  |   - Tesseract/pytesseract 의존성 제거
#          |                  |   - 좌표 6개: id_add_btn/status_dot/friend_add_btn
#   v1.26 | 2026-03-06 18:00 | [삭제] kakao_message(가망카톡 뿌리기) 완전 제거
#          |                  | [변경] kakao_openchat → 오픈채팅/아침인사/가망뿌리기
#          |                  | [삭제] 그리드 캡쳐 방식 전체 제거
#          |                  |   - calculate_coordinates() / filter_valid_coords() 삭제
#          |                  |   - _render_grid_section() / _update_grid_preview() 삭제
#          |                  |   - grid_config 저장/로드 코드 삭제
#   v1.27 | 2026-03-06 20:00 | [개선] 캡처 오버레이 팝업 제거
#          |                  |   - 캡처 버튼 클릭 시 팝업창 없이 상태바에 카운트다운
#          |                  | [복원] 좌표 자동 계산 섹션 (오픈채팅/가망뿌리기)
#          |                  |   - calculate_coordinates / filter_valid_coords 재복원
#          |                  |   - 시작좌표 포인트 캡처 방식
#          |                  |   - 미리보기: 열N × 행N = 총 N개
#          |                  | [추가] 전송버튼 좌표 / 닫기버튼 좌표 UI
#          |                  |   - send_btn_coord / close_btn_coord JSON 저장
#   v1.28 | 2026-03-06 21:00 | [주석정리] 업데이트 히스토리 및 구조맵 정돈
#   v1.29 | 2026-03-06 22:00 | [UI개선] 오픈채팅 대상 목록 섹션 제거
#   v1.30 | 2026-03-06 23:00 | [버그수정] _run_kakao_openchat 실행 로직 재작성
#   v1.51 | 2026-03-10 | [기능추가] 구글 시트(CSV) 기반 로그인 인증 기능
#          |            |   ■ 개요
#          |            |   · 카카오톡_올인원_v2.6 의 LoginDialog 로직을 이식
#          |            |   · 앱 최초 실행 시 ID / PW 입력 창이 먼저 뜨며,
#          |            |     인증 성공 시에만 메인 App 이 열림
#          |            |   · 인증 실패(창 닫기/종료 클릭) 시 프로그램 즉시 종료
#          |            |
#          |            |   ■ 구글 시트 구조 (gid=0, 첫 번째 탭)
#          |            |     열 이름: ID / PASSWORD(PW) / EXPIRE(만료일) / STATUS(활성여부)
#          |            |     STATUS 허용값: 활성 / ACTIVE / 1 / TRUE / YES
#          |            |     EXPIRE 형식:  YYYY-MM-DD  (비어있으면 무기한)
#          |            |
#          |            |   ■ 추가된 상수
#          |            |     SHEET_URL  : 구글 시트 CSV 내보내기 URL
#          |            |                 (Config/config.json 의 "sheet_url" 키로 덮어쓰기 가능)
#          |            |     HAS_REQUESTS : requests 패키지 가용 여부 (bool)
#          |            |
#          |            |   ■ 추가된 클래스: LoginDialog
#          |            |     __init__(sheet_url, debug)  — Tk 창 초기화
#          |            |     _center()                   — 화면 중앙 배치
#          |            |     _build()                    — ID/PW 입력 UI 구성
#          |            |     _load_users() → dict|None   — CSV fetch & 파싱
#          |            |     _check_expire(exp_str) → bool — 만료일 검사
#          |            |     _login()                    — 인증 검증 및 결과 설정
#          |            |     _exit()                     — 창 닫기 (미인증 종료)
#          |            |     show() → (bool, str|None)   — 메인루프 실행 후 결과 반환
#          |            |
#          |            |   ■ main() 변경
#          |            |     App() 생성 전 LoginDialog(sheet_url).show() 호출
#          |            |     authenticated=False 이면 sys.exit(0) 로 종료
#          |            |     sheet_url 은 config.json → SHEET_URL 순으로 결정
#          |            |
#          |            |   ■ 의존성
#          |            |     requests : pip install requests
#          |            |     (없으면 HAS_REQUESTS=False, 로그인 창에 경고 표시)
#          |            |
#   v1.50 | 2026-03-09 | [버그픽스] 이미지 첨부 사용함↔사용안함 토글 / 저장 오작동 수정
#          |            |   ■ 버그 A — _save_template: elif 체인으로 인한 설정 미저장
#          |            |   · 원인
#          |            |     저장 블록 구조:
#          |            |       if needs_image:          ← kakao_openchat/telegram_message 여기 진입
#          |            |           data["use_image"] = ...
#          |            |       elif wk=="kakao_openchat":  ← needs_image=True 이므로 건너뜀
#          |            |           data["grid_config"] = ...  ← 저장 안 됨!
#          |            |       else:                    ← 마찬가지로 건너뜀
#          |            |           data["tg_chrome_load"] = ...  ← 저장 안 됨!
#          |            |     → kakao_openchat: 이미지 사용함→사용안함 저장 후
#          |            |       grid_config / action_delay 등이 이전 값으로 덮여쓰기 안 됨
#          |            |     → telegram_message: tg_chrome_load 등 딜레이 설정 미저장
#          |            |   · 수정 (_save_template)
#          |            |     elif wk=="kakao_openchat" → if wk=="kakao_openchat"  (독립 if)
#          |            |     else(텔레그램)            → if wk not in ("kakao_friend","kakao_openchat")
#          |            |     → 이미지 설정 블록과 워크플로우 전용 블록이 항상 둘 다 실행됨
#          |            |   ■ 버그 B — _toggle_image_path: 사용안함 시 좌표 행 숨김 안 됨
#          |            |   · 원인
#          |            |     _img_path_row  : 렌더 시 항상 .pack() → 사용안함 눌러도 행 표시 유지
#          |            |     _img_order_row : 동일
#          |            |     _img_src_row   : 카카오라면 항상 .pack()
#          |            |     _img_drop_row  : 카카오라면 항상 .pack()
#          |            |     → _set_row_state 로 Entry/Button 만 disable → 행 자체는 안 사라짐
#          |            |     → 사용안함 눌러도 경로/좌표 입력란이 회색으로만 보임
#          |            |   · 수정 (_toggle_image_path + 렌더 코드)
#          |            |     1) _img_path_row / _img_order_row 초기 .pack() 제거
#          |            |        → 렌더 시 pack_forget 상태로 생성
#          |            |     2) _toggle_image_path 에 _show_row() 헬퍼 추가
#          |            |        use=False → 모든 상세 행 pack_forget (숨김)
#          |            |        use=True  → mode 에 맞는 행만 pack (표시)
#          |            |     3) mode="none" 분기도 동일 정책 적용
#          |            |   · 적용 범위: 카카오(file/dragdrop) + 텔레그램(clipboard/file) 동일
#          |            |   ■ 결과 — 의도한 동작
#          |            |     사용함 클릭  → 현재 mode 에 맞는 행 표시 + 활성
#          |            |     사용안함 클릭 → 모든 상세 행 숨김, 방식 선택 행만 비활성으로 남음
#          |            |     다시 사용함  → 이전 mode 값 그대로 복원되어 해당 행 재표시
#          |            |     저장 시      → use_image + grid_config/딜레이 등 전부 저장됨
#   v1.49 | 2026-03-09 | [버그픽스] _run_kakao_openchat: cell_height=0 / column_gap=0 허용
#          |            |   ■ 증상
#          |            |   · 좌표 자동계산 섹션에서 "1칸 크기 0, 0 / 열간격 0" 으로 두면
#          |            |     실행 시 "[실행불가] 셀 높이(cell_height)가 0" ERROR 로그 + 즉시 종료
#          |            |   · UI의 ↺ 미리보기는 ch=0 을 이미 허용(좌표 표시됨)하여 미리보기와
#          |            |     실행 동작이 불일치하는 문제 발생
#          |            |   ■ 원인
#          |            |   · 실행 코드(_run_kakao_openchat, ~5113줄)의 조기 차단 조건:
#          |            |       if not sx or not ch:  → ch=0.0 이면 not ch == True → 무조건 차단
#          |            |   · 원래 의도: "셀 높이=0이면 좌표 계산 무의미" 방어 로직
#          |            |   · 실제: calculate_coordinates(ch=0) 는 start_xy를 row_count 개 반환
#          |            |     → 차단할 이유가 없음 (filter_valid_coords 통과 가능)
#          |            |   ■ 수정 (_run_kakao_openchat, ~5113줄)
#          |            |   · 조건 변경:
#          |            |       이전: if not sx or not ch:
#          |            |       이후: if gc.get("start_x") is None:
#          |            |       → start_x 키 자체가 없으면(캡처 미완료)만 차단
#          |            |       → sx==0(화면 좌측 끝), ch==0(셀높이 미설정) 모두 허용
#          |            |   · 에러 메시지도 "시작좌표 미캡처" 로 교체
#          |            |   ■ ch=0 허용 후 동작
#          |            |   · calculate_coordinates 결과: 모든 row가 start_y 동일
#          |            |     → col=1, row=1, ch=0 : [(sx,sy)] 1개 → start_xy 1회 더블클릭
#          |            |     → col=1, row=5, ch=0 : [(sx,sy)×5] → 같은 위치 5회 반복
#          |            |   · filter_valid_coords 통과 → grid_coords 비어있으면 기존 ERROR 유지
#   v1.48 | 2026-03-09 | [버그픽스] 텔레그램 이미지 첨부 "사용함" 클릭 시 섹션 비활성 버그
#          |            |   - 원인: _toggle_image_path 에서 mode=="none" 이면
#          |            |     use 를 False 로 강제 덮어써 "사용함" 클릭이 무효화됨
#          |            |     (텔레그램 신규 템플릿 기본 mode="none" 이므로 항상 발생)
#          |            |   - 수정: mode=="none" + use==True 이면
#          |            |     · _img_mode_row(첨부 방식 선택 행)만 활성화
#          |            |     · 경로/좌표/딜레이/순서 행은 비활성 유지
#          |            |     · early return 으로 이하 처리 스킵
#          |            |     → 사용자가 방식(클립보드/파일경로)을 선택하면
#          |            |       _toggle_image_path 재호출로 해당 섹션 활성화
#          |            |   - mode=="none" + use==False: 전부 비활성 (기존 동일)
#   v1.47 | 2026-03-09 | [버그픽스] _tg_wait_dialog 다이얼로그 판정 로직 수정
#          |            |   - 원인: 'Telegram (124251) (응답 없음)' 처럼 타이틀이 변하기만 해도
#          |            |     성공으로 판정하는 단순 비교 로직의 허점
#          |            |   - 수정: 화이트리스트 키워드 포함 여부로 판정 방식 변경
#          |            |     성공: 타이틀에 파일 다이얼로그 키워드 포함 시에만
#          |            |       ('Choose Files' / '열기' / 'Open' / '파일 선택' /
#          |            |        '파일 열기' / 'Select File' / '파일' / 'File')
#          |            |     실패: 응답없음 / 다른 톡방 / 앱 전환 등 그 외 모든 변화
#          |            |   - 타이틀이 바뀌었으나 키워드 없는 경우:
#          |            |     WARN 로그 출력 + 폴링 계속 (오판정 방지)
#          |            |   - 3회 모두 실패 → _DialogSkipError → 항목 skip (기존 동일)
#   v1.46 | 2026-03-09 | [버그픽스] _tg_wait_dialog 재시도 로직 수정 (ESC 제거)
#          |            |   - 원인: 첨부버튼 미감지 시 ESC를 눌러 현재 톡방이 닫힘
#          |            |     → 2번째 재시도에서 엉뚱한 톡방이 열리며 타이틀 변화 오판정
#          |            |     → 잘못된 방에 메시지 발송되는 치명적 오작동 발생
#          |            |   - 수정: ESC 라인 제거, 0.5초 대기 후 동일 톡방에서 첨부버튼 재클릭
#          |            |   - 재시도 흐름:
#          |            |     버튼 클릭 → 0.3s 폴링 → 미감지 → 0.5s 대기 → 재클릭 (최대 3회)
#          |            |     3회 모두 실패 → _DialogSkipError → 해당 항목 skip + WARN 로그
#          |            |   - v1.45 대비: '실패→ESC→재시도' 방식 → 'ESC없이 바로 재시도'로 변경
#          |            | [통합] telegram_join_msg 작업유형 제거 → telegram_message에 흡수
#          |            |   - 배경: 그룹가입+메시지 / 메시지만 두 유형의 실행 코드가 거의 동일
#          |            |     → '가입 후 발송' 체크박스 하나로 통합, 코드 중복 제거
#          |            |   - 작업유형 정리 (이전 3개 → 이후 2개):
#          |            |     이전: telegram_join / telegram_join_msg / telegram_message
#          |            |     이후: telegram_join / telegram_message (join_first 옵션 포함)
#          |            |   - UI 변경 (_render_send_close_section):
#          |            |     telegram_message 전용 '가입 옵션' 행 추가
#          |            |     · '✅ 가입 후 발송' Checkbutton (self._join_first_var)
#          |            |     · 체크 시 → 가입버튼 좌표 X/Y 입력란 + 캡처 버튼 동적 표시
#          |            |     · 체크 해제 시 → 좌표 행 pack_forget() 으로 숨김
#          |            |   - 실행 흐름 (_run_telegram_message):
#          |            |     크롬 주소창 → 링크 입력 → 로딩 대기
#          |            |     → [join_first=True] join_btn_coord 클릭 → tg_join_click 대기
#          |            |     → 이미지 첨부(none/clipboard/file 분기)
#          |            |     → 메시지 입력 · 전송 → 닫기(esc/altf4/click_btn)
#          |            |   - 신규 템플릿 저장 키:
#          |            |     join_first (bool) — 가입 후 발송 여부
#          |            |     join_btn_coord {x, y} — 가입버튼 좌표
#          |            |   - 구버전 자동 마이그레이션 (_load_templates):
#          |            |     JSON workflow=="telegram_join_msg" 감지 시 자동 변환
#          |            |     workflow → "telegram_message"
#          |            |     join_first → True
#          |            |     coords["join_btn"] → join_btn_coord (최상위 키로 복사)
#          |            |   - 제거된 항목:
#          |            |     PLATFORM_WORKFLOWS["telegram_join_msg"]
#          |            |     SAMPLE_CSV_DATA["telegram_join_msg"]
#          |            |     dispatch 매핑 "telegram_join_msg"
#          |            |     _run_telegram_join_msg 함수 (주석 비활성화)
#          |            |     _is_tg / _is_tg_sc / DIRECT_SUPPORT 내 join_msg 참조 전부
#   v1.45 | 2026-03-09 13:00 | [안정성] 첨부버튼 클릭 후 다이얼로그 열림 확인 + 재시도
#          |                  |   - _tg_wait_dialog() 헬퍼 추가
#          |                  |     · 클릭 전 포그라운드 창 타이틀 저장
#          |                  |     · 클릭 후 0.3 초 간격 폴링으로 창 변화 감지
#          |                  |     · 실패 시 ESC 후 재시도 (최대 3회)  ← ESC는 v1.46에서 제거됨
#          |                  |   - 감지 우선순위: win32gui → pygetwindow → 단순 대기
#          |                  |   - 3회 모두 실패: _DialogSkipError 발생
#          |                  |     → 해당 항목 _fail 카운트 + WARN 로그 + skip(continue)
#          |                  |   - telegram_join_msg / telegram_message 두 워크플로우 적용
#          |                  |     (telegram_join_msg 는 v1.46 에서 telegram_message 로 통합됨)
#   v1.44 | 2026-03-09 12:00 | [UI/로직] 이미지 첨부 딜레이 모드별 분리
#          |                  |   - 기존 단일 딜레이 행 → 3개 행으로 분리
#          |                  |     · 드래그앤드롭: 클릭후/드래그후/드롭후/Enter후 (Kakao 전용)
#          |                  |     · 클립보드: 붙여넣기후/전송후
#          |                  |     · 파일경로: 다이얼로그대기/폴더이동후/파일열기후
#          |                  |   - 모드 전환 시 해당 딜레이 행만 표시 (_toggle_image_path)
#          |                  |   - 소스/드롭 좌표 행 텔레그램에서 완전 숨김 (_is_tg 가드)
#          |                  |   - image_delays JSON 키 확장
#          |                  |     cb_after_paste / cb_after_send
#          |                  |     file_dialog_open / file_folder_move / file_after_open
#          |                  |   - _tg_attach_file: image_delays.file_* 키 기반 딜레이 적용
#          |                  |   - 클립보드 분기: cb_after_paste 키 적용
#   v1.43 | 2026-03-09 10:00 | [기능] 텔레그램 파일첨부 로직 개선 + 파일명 입력란 좌표 추가
#          |                  |   - _tg_filename_row UI 추가 (파일명 입력란 X/Y + 캡처)
#          |                  |     파일경로 모드일 때만 표시 (_toggle_image_path 연동)
#          |                  |   - tg_filename_input_coord 템플릿 저장 키 추가
#          |                  |   - _tg_attach_file 로직 변경
#          |                  |     (구) 파일명란 Ctrl+V → Enter
#          |                  |     (신) 폴더경로 입력→Enter → 파일명좌표 클릭 → 파일명입력→Enter
#          |                  |   - tg_filename_input_coord 미설정 시 명확한 에러 로그
#   v1.42 | 2026-03-09 09:00 | [버그수정] NameError: TemplateEditor not defined
#          |                  |   - _set_row_state 재귀 호출 내 TemplateEditor → TemplateTab 교정
#          |                  |     (패치 중 존재하지 않는 클래스명 오참조)
#          |                  |   - 영향 범위: _toggle_image_path → _apply() → _set_row_state
#          |                  |     이미지 모드 행 토글 시 Tkinter 콜백 에러 발생 수정
#   v1.41 | 2026-03-09 08:00 | [분리] 텔레그램 좌표 키 Kakao 와 완전 독립
#          |                  |   - 신규 저장 키: tg_input_method / tg_message_input_coord
#          |                  |   - UI 변수: _tg_mi_x/_tg_mi_y (기존 _sc_mi_x/_sc_mi_y 대체)
#          |                  |   - 파일첨부 버튼 좌표: tg_attach_btn_coord 추가
#          |                  |     (파일경로 모드 전용, 미설정 시 실행 불가)
#          |                  |   - 좌표 읽기: tmpl.get("tg_message_input_coord") 사용
#          |                  |     (기존 self.coords["message_input"] → KeyError 수정)
#          |                  |   - 이미지 모드 옵션: none/clipboard/file (dragdrop 제거)
#          |                  |   - _render_friend_option_section 이름 교정
#          |                  |     (기존 _render_ocr_section → 잘못된 이름 수정)
#          |                  |   - _tg_input_w 분리 (중복 _input_w 함수명 충돌 해소)
#   v1.40 | 2026-03-09 07:00 | [UI개선] 이미지 토글 버튼 + 닫기 방식 통일
#          |                  |   - 이미지 첨부 체크박스 → "✅ 사용함" / "🚫 사용 안함" 토글 버튼
#          |                  |     선택된 버튼 파란색(#2563EB) 강조
#          |                  |   - _set_row_state() 헬퍼 추가
#          |                  |     Entry/Button/Radiobutton/Checkbutton 만 재귀 state 변경
#          |                  |     Label 은 state 미지원이므로 건너뜀
#          |                  |   - 닫기 방식 Kakao/Telegram 통일: ESC 기본값
#          |                  |     (기존 Telegram 기본값 ctrlw → esc)
#          |                  |   - _tg_close: ESC(ctrlw 호환) / Alt+F4 / 버튼클릭
#          |                  |   - ctrlw 는 구버전 호환용으로 esc 와 동일 처리 유지
#   v1.39 | 2026-03-09 04:00 | [기능] 텔레그램 이미지 첨부 (없음/클립보드/파일경로)
#          |                  |   - 전송/닫기 방식 선택 (Enter/Ctrl+Enter/버튼클릭)
#          |                  |   - 닫기: Ctrl+W / Alt+F4 / 버튼클릭
#   v1.38 | 2026-03-09 02:00 | [기능] 이미지 첨부 방식 선택(파일경로/드래그앤드롭)
#          |                  |   - 방식별 필수값 미설정 시 실행 불가 처리
#          |                  |   - 작업관리 treeview 템플릿명 컬럼 추가
#   v1.37 | 2026-03-09 00:00 | [버그수정] cell_height 소수점 처리
#          |                  |   - safe_int: int(float()) 방식으로 수정
#          |                  |   - grid_config cell_height/cell_width/column_gap
#          |                  |     저장 시 float 유지, 읽기 시 safe_float 사용
#          |                  |   - calculate_coordinates float 파라미터 허용
#   v1.36 | 2026-03-07 12:00 | [정리] 오픈채팅 불필요 코드 제거
#          |                  |   - chat_open_coord UI/저장/실행 완전 제거
#          |                  |   - PLATFORM_WORKFLOWS kakao_openchat coord_keys 제거
#          |                  |   - _run_kakao_openchat: target_type 분기 제거
#          |                  |     grid_coords 없으면 설정오류 에러만
#          |                  |   - dummy_row / 불필요 주석 정리
#   v1.35 | 2026-03-07 11:00 | [UI] 메시지 입력방식/전송방식/닫기방식 선택 추가
#          |                  |   - 입력 방식: 바로입력(direct) / 좌표클릭(coord)
#          |                  |   - 전송 방식: enter / ctrl_enter / click_btn
#          |                  |   - 닫기 방식: esc / altf4 / click_btn
#          |                  |   - 좌표 행은 해당 방식 선택 시에만 표시
#          |                  |   - 좌표 없이도 바로입력+enter+esc 조합으로 동작
#   v1.34 | 2026-03-07 10:00 | [분리] kakao_friend / kakao_openchat 완전 독립
#          |                  |   - _render_friend_option_section: kakao_friend 전용 변수
#          |                  |     중복 생성(L2245/2365 등) 제거, OCR 블록 제거
#          |                  |   - _render_timing_section: 공유 변수명 분리
#          |                  |     (_between_chats_var/_jitter_val_var)
#          |                  |   - _save_template: hasattr 기반 → wk 분기로 재작성
#          |                  |     kakao_friend/kakao_openchat 설정 서로 불간섭
#   v1.33 | 2026-03-07 02:00 | [버그수정] kakao_openchat 좌표 설정 UI 누락 수정
#          |                  |   근본원인: v1.29 coords 섹션 완전 숨김 →
#          |                  |     message_input/chat_open 좌표 설정 방법 없음
#          |                  |   [A] 전송·닫기 섹션에 "✏️ 입력창 좌표" 캡처 행 추가
#          |                  |   [B] 좌표자동계산 섹션에 "💬 채팅방 좌표" 캡처 행 추가
#          |                  |   [C] _save_template: message_input/chat_open 저장
#          |                  |   [D~F] 실행 로직: coords 대신 tmpl 직접 읽기
#   v1.32 | 2026-03-07 01:00 | [디버깅] _drag_drop_image / _run_kakao_openchat 심층 버그 수정
#          |                  |   BUG-A: 클립보드 방식 tx/ty=0 → click 스킵 (FailSafe 방지)
#          |                  |   BUG-B: win32clipboard ImportError → WARN 후 return
#          |                  |   BUG-C: _click() FailSafeException 명시 re-raise
#          |                  |   BUG-D: use_img=True & img_path 없음 → 사전 경고 + False
#          |                  |   BUG-E: cell_height==0 → calculate_coordinates 호출 방지
#          |                  |   BUG-F: 이미지 첨부 오류 격리 (메시지/닫기 단계 계속)
#   v1.31 | 2026-03-07 00:00 | [디버깅] PyAutoGUI FailSafe 관련 종합 버그 수정
#          |                  |   BUG-01: _click() 좌표 0,0 → RuntimeError
#          |                  |   BUG-02: FailSafeException 별도 catch
#          |                  |   BUG-03: _drag_drop_image 드롭좌표 0,0 → skip
#          |                  |   BUG-04: escape 시도 시 FailSafe 재발동 방지
#          |                  |   BUG-05: WorkflowExecutor 시작 시 FAILSAFE 설정
#          |                  |   BUG-06: 실행 전 좌표 사전검증 (명확한 에러)
#          |                  |   - rows(_read_csv) 의존성 완전 제거
#          |                  |   - grid_coords 있으면: N개 타일 순회 실행
#          |                  |   - grid_coords 없으면: chat_open 좌표 1회 실행
#          |                  |   - '대상 CSV 파일이 없습니다' 에러 더 이상 발생 안함
#          |                  |   - kakao_openchat: 그리드 자동계산으로 채팅방 순회
#          |                  |     → CSV/직접입력 대상 목록 불필요
#          |                  | [UI개선] 오픈채팅 좌표 설정 섹션 제거
#          |                  |   - 이미지 소스/드롭 → 이미지 첨부 섹션
#          |                  |   - 시작좌표 → 좌표 자동계산 섹션
#          |                  |   - 전송/닫기 버튼 → 전송·닫기 방식 섹션
#          |                  | [기능추가] 직접 입력 중복 제거 버튼
#          |                  |   - kakao_friend / telegram_* 직접입력 모드
#          |                  |   - 🔁 중복 제거 버튼: 대소문자 무관 중복 제거
#          |                  |   - 제거 결과 카운트 실시간 표시
#          |                  |   - 헤더 버전명 v1.25 → v1.28
#          |                  |   - v1.26 / v1.27 순서 시간순 정상화
#          |                  |   - v1.26 항목 내 혼입된 v1.22/v1.24 내용 제거
#          |                  |   - 구조맵 grid_config 복원 반영
#          |                  |   - 구조맵 after_ocr → after_color_wait 교정
#          |                  |   - 구조맵 _run_kakao_openchat 중복 항목 제거
#          |                  |   - kakao_message 잔재 참조 모두 정리
# ============================================================
#
# ┌─────────────────────────────────────────────────────────┐
# │                  📦 전역 상수 & 설정                     │
# ├─────────────────────────────────────────────────────────┤
# │  APP_VERSION / APP_TITLE     버전 문자열 (UI 표시용)    │
# │  APP_DIR / CONFIG_DIR        실행 파일 기준 경로        │
# │  TEMPLATE_DIR / JOBS_DIR     JSON 저장 경로             │
# │  LOGS_DIR / DATA_DIR         로그·데이터 경로           │
# │  CONFIG_PATH / STATS_PATH    설정·통계 JSON 파일 경로   │
# │  PALETTE{}                   UI 다크 테마 색상 팔레트   │
# │  SIDEBAR_TABS[]              사이드바 탭 목록           │
# │  PLATFORMS{}                 플랫폼 메타 (kakao/telegram)│
# │  PLATFORM_WORKFLOWS{}        작업 유형별 정의           │
# │    ├─ kakao_friend           가망 친구추가              │
# │    ├─ kakao_openchat         오픈채팅/아침인사/가망뿌리기│
# │    ├─ telegram_join          그룹 가입                  │
# │    └─ telegram_message       메시지 발송 (join_first 옵션) │
# │  MSG_TOKENS{}                메시지 내 치환 토큰 목록   │
# └─────────────────────────────────────────────────────────┘
#
# ┌─────────────────────────────────────────────────────────┐
# │                  🔧 유틸 함수                           │
# ├─────────────────────────────────────────────────────────┤
# │  load_json(path, default)    JSON 파일 안전 로드        │
# │  save_json(path, data)       JSON 파일 저장             │
# │  now_str()                   현재 시각 "HH:MM:SS"       │
# │  fmt_ts()                    현재 일시 "YYYY-MM-DD ..." │
# │  safe_int(val, default)      예외 없는 int 변환         │
# │  safe_float(val, default)    예외 없는 float 변환       │
# │  _lighten(hex, factor)       hex 색상 밝게              │
# │  _find_tesseract()           Tesseract 실행파일 자동탐색│
# │  resolve_name_number(pattern, row)                      │
# │                              메시지 토큰 치환           │
# │  build_search_id(kw, start, idx, digits)                │
# │                              친추 검색ID 생성           │
# │                              예) 가망+101+0 → "가망101"│
# └─────────────────────────────────────────────────────────┘
#
# ┌─────────────────────────────────────────────────────────┐
# │              🖼️  class App(tk.Tk)  ── 메인 윈도우       │
# ├─────────────────────────────────────────────────────────┤
# │  __init__          윈도우 초기화, config/stats 로드     │
# │  _default_config   기본 설정값 반환                     │
# │  _build_ui         헤더+사이드바+콘텐츠+상태바 조립     │
# │  _build_header     상단 타이틀/버전 바                  │
# │  _build_sidebar    좌측 탭 버튼 목록                    │
# │  _make_tab_btn     사이드바 탭 버튼 생성                │
# │  _build_content    우측 탭 프레임 영역                  │
# │  _switch_tab       탭 전환 처리                         │
# │  _build_statusbar  하단 상태바                          │
# │  _set_status       상태바 메시지 업데이트               │
# │  _on_close         종료 처리                            │
# └─────────────────────────────────────────────────────────┘
#
# ┌─────────────────────────────────────────────────────────┐
# │         📋 class TemplateTab  ── 작업 템플릿 관리       │
# ├─────────────────────────────────────────────────────────┤
# │  _build_ui             좌측 목록 + 우측 편집 패널 분할  │
# │  _build_list_panel     템플릿 목록 리스트박스           │
# │  _build_edit_panel     편집 패널 스크롤 프레임 초기화   │
# │  _refresh_edit_panel   편집 패널 전체 재렌더링          │
# │                                                         │
# │  ── 섹션 렌더링 메서드 ──                               │
# │  _on_platform_change   플랫폼 버튼 → 섹션 전체 갱신    │
# │  _on_wtype_change      작업유형 버튼 → 섹션 전체 갱신  │
# │  _render_wtype_buttons 작업유형 버튼 그룹 재그리기      │
# │  _render_image_section 이미지 첨부 설정 섹션            │
# │    └─ img_order        📎 첨부 순서 (before / after)   │
# │  _toggle_image_path    이미지 사용 체크 시 경로 활성화  │
# │  _browse_image         이미지 파일 선택 다이얼로그      │
# │  _render_coord_section 좌표 입력 섹션                   │
# │  _build_coord_row      좌표 행 1개 생성 (point / area) │
# │  _render_send_close_section                             │
# │    ├─ send_method      ⌨️ Enter / 🖱️ 좌표 클릭         │
# │    └─ close_method     ⌨️ ESC  / 🖱️ 좌표 클릭         │
# │  _render_friend_option_section   OCR / 친구추가 검색ID 설정 섹션  │
# │    ├─ id_keyword       검색 키워드 (예: "가망")         │
# │    ├─ id_start_num     시작 번호  (예: 101)             │
# │    ├─ id_digits        자리수 고정 (0=자동)             │
# │    └─ retry_count      OCR 재시도 횟수                  │
# │  _update_id_preview    키워드+번호 미리보기 갱신        │
# │  _browse_tesseract     Tesseract 실행파일 선택          │
# │                                                         │
# │  ── 좌표 캡처 ──                                        │
# │  _capture_point        단일 좌표 3초 카운트 후 캡처     │
# │  _capture_area         드래그 영역 캡처                 │
# │                                                         │
# │  ── 저장 / 로드 ──                                      │
# │  _save_template        편집 내용 → JSON 저장            │
# │    저장 필드 목록:                                      │
# │      name, platform, workflow, coords                   │
# │      target_mode ('csv'|'direct'), target_direct        │
# │      use_image, image_path, img_order                   │
# │      image_source_coord, image_drop_coord, image_delays │
# │      send_method, close_after_send, close_method        │
# │      action_delay, between_chats, between_jitter        │
# │      grid_config (좌표 자동계산: 시작XY·셀크기·열/행)   │
# │      tesseract_path, id_pattern, retry_count            │
# │      id_keyword, id_start_num, id_digits                │
# │      [친추 딜레이] after_ctrlA, after_click, after_input│
# │                    after_color_wait(0.6), after_tab(0.5) │
# │      [텔레그램]    tg_chrome_load, tg_telegram_open     │
# │                    tg_join_click, tg_after_type          │
# │                    tg_after_send, tg_after_back          │
# │                    tg_between_min, tg_between_max        │
# │  _load_templates       TEMPLATE_DIR *.json 전체 로드    │
# │  _refresh_list         리스트박스 재표시                │
# │  _on_select            리스트 선택 → 편집 패널 갱신     │
# │  _add_template         새 템플릿 초기화                 │
# │  _dup_template         선택 템플릿 복제                 │
# │  _del_template         선택 템플릿 삭제                 │
# │  _show_help            도움말 팝업                      │
# └─────────────────────────────────────────────────────────┘
#
# ┌─────────────────────────────────────────────────────────┐
# │           📋 class JobsTab  ── 작업 관리                │
# ├─────────────────────────────────────────────────────────┤
# │  _build_ui             툴바 + Treeview + 진행바 조립    │
# │  _load_jobs / _refresh_tv  JOBS_DIR 로드 + 트리 갱신   │
# │  _add_job / _edit_job  작업 추가·편집 (JobDialog 호출) │
# │  _dup_job / _del_job   작업 복제·삭제                   │
# │  _save_job             작업 JSON 저장                   │
# │  _run_selected         선택 작업 실행 → engine.add_task │
# │  _run_all              전체 작업 → engine 큐 일괄 추가  │
# │  _run_job              단일 작업 큐 추가 + 콜백 정의    │
# │  _stop_all             전체 중지 (engine.stop+clear)    │
# │  _stop_job             개별 작업 중지 (v1.54 신규)      │
# │  _on_job_done          완료 콜백 → UI 상태·통계 갱신   │
# │  _update_job_status    Treeview 상태 컬럼 갱신          │
# │  _load_template_for_job 템플릿 로드+migrate (BUG-04)   │
# │  set_progress          진행바 업데이트                  │
# │  set_counts            성공/실패 카운터 업데이트        │
# └─────────────────────────────────────────────────────────┘
#
# ┌─────────────────────────────────────────────────────────┐
# │           💬 class JobDialog  ── 작업 편집 다이얼로그   │
# ├─────────────────────────────────────────────────────────┤
# │  _build                전체 레이아웃 조립               │
# │  _get_templates        TEMPLATE_DIR 목록 반환           │
# │  _update_tmpl_info     템플릿 선택 시 정보 표시         │
# │  _build_target_section CSV/엑셀 타겟 파일 설정 섹션     │
# │  _build_message_section 메시지 입력 섹션               │
# │  _build_delay_section  딜레이 설정 섹션                 │
# │  _build_schedule_section 예약 실행 섹션                │
# │  _ok                   저장 후 다이얼로그 닫기          │
# └─────────────────────────────────────────────────────────┘
#
# ┌─────────────────────────────────────────────────────────┐
# │        ⚙️  class WorkflowExecutor  ── 실행 엔진         │
# ├─────────────────────────────────────────────────────────┤
# │  __init__(job, template, stop_evt, callbacks)           │
# │  run()                 workflow 종류 → 메서드 디스패치  │
# │                                                         │
# │  ── 카카오 ──                                           │
# │  _run_kakao_friend     친구추가 루프                    │
# │    build_search_id()   키워드+순번 검색ID 생성          │
# │    _kakao_friend_once  단일 친구추가 실행               │
# │    _decide_state       OCR 텍스트로 상태 판별           │
# │  _run_kakao_openchat   오픈채팅/아침인사/가망뿌리기     │
# │    img_order=before/after  이미지 첨부 순서             │
# │    send_method=enter/ctrl_enter/coord  전송 방식        │
# │    close_after_send=T/F    전송 후 창닫기 여부          │
# │    close_method=esc/altf4/coord  닫기 방식             │
# │    action_delay / between_chats / between_jitter       │
# │    grid_config → calculate_coordinates() 그리드 계산   │
# │  _run_kakao_friend     친구추가 딜레이 파라미터         │
# │    after_ctrlA(2.0) after_click(1.5) after_input(2.5)  │
# │    after_color_wait(0.6) after_tab(0.5)                │
# │    between_chats(1.0) between_jitter(0.3)              │
# │                                                         │
# │  ── 텔레그램 ──                                         │
# │  공통 딜레이 파라미터 (원본: TelegramAllInOne_v2)       │
# │    tg_chrome_load(2.0)  tg_telegram_open(1.5)          │
# │    tg_join_click(2.0)   tg_after_type(0.5)             │
# │    tg_after_send(1.0)   tg_after_back(0.8)             │
# │    tg_between_min(3.0)  tg_between_max(7.0)            │
# │  _run_telegram_join        그룹 가입                   │
# │  _run_telegram_message     메시지 발송 (join_first 옵션) │
# │                                                         │
# │  ── 공통 헬퍼 ──                                        │
# │  _click(key, double)   coords[key] 좌표 클릭            │
# │  _type(text)           pyperclip→paste / 직접입력       │
# │  _hotkey(*keys)        pyautogui.hotkey                 │
# │  _read_csv()           CSV 파일 읽기                    │
# │  _read_targets()       CSV or 직접입력 통합 읽기        │
# │                        (target_mode 에 따라 분기)       │
# │  _apply_vars(text,row) 메시지 토큰 치환                 │
# │  _drag_drop_image      이미지 드래그앤드롭 (소스좌표+딜레이)│
# │  _jitter()             랜덤 딜레이 반환                 │
# │  calculate_coordinates() 그리드 좌표 자동 계산          │
# │  filter_valid_coords()  화면 밖 좌표 필터링             │
# │  _is_stopped()         중지 이벤트 확인                 │
# │  _log / _progress      콜백 호출                        │
# └─────────────────────────────────────────────────────────┘
#
# ┌─────────────────────────────────────────────────────────┐
# │        🧵 PostingEngine(Queue)  ── 큐 기반 단일 실행    │
# ├─────────────────────────────────────────────────────────┤
# │  run()   WorkflowExecutor 를 별도 스레드에서 실행       │
# │          완료 시 JobsTab._job_done() 콜백 호출          │
# │          (monkey-patch 로 JobsTab 메서드에 연결됨)      │
# └─────────────────────────────────────────────────────────┘
#
# ┌─────────────────────────────────────────────────────────┐
# │        🗒️  class LogTab  ── 실시간 로그                 │
# ├─────────────────────────────────────────────────────────┤
# │  append(message, level, source)  로그 행 추가           │
# │  _apply_filter     소스/레벨 필터 적용                  │
# │  _update_summary   성공/경고/오류 요약 카운터           │
# │  _clear            로그 초기화                          │
# │  _export_csv       로그 CSV 내보내기                    │
# └─────────────────────────────────────────────────────────┘
#
# ┌─────────────────────────────────────────────────────────┐
# │        📊 class StatsTab  ── 통계                       │
# ├─────────────────────────────────────────────────────────┤
# │  add_record(job, succ, fail, wf)  실행 결과 기록        │
# │  refresh()         통계 뷰 갱신                         │
# │  _export_csv       통계 CSV 내보내기                    │
# │  _reset            통계 초기화                          │
# └─────────────────────────────────────────────────────────┘
#
# ┌─────────────────────────────────────────────────────────┐
# │        ⚙️  class SettingsTab  ── 설정                   │
# ├─────────────────────────────────────────────────────────┤
# │  _build     딜레이·스케줄·경로·테마 설정 UI 구성        │
# │  _load      config.json → UI 위젯에 반영                │
# │  _save      UI 위젯 값 → config.json 저장               │
# └─────────────────────────────────────────────────────────┘
#
# ┌─────────────────────────────────────────────────────────┐
# │        🔗 Monkey-Patch 연결 목록                        │
# ├─────────────────────────────────────────────────────────┤
# │  App._build_templates_tab  → TemplateTab 인스턴스화     │
# │  App._build_jobs_tab       → JobsTab 인스턴스화         │
# │  App._build_log_tab        → LogTab 인스턴스화          │
# │  App._build_stats_tab      → StatsTab 인스턴스화        │
# │  App._build_settings_tab   → SettingsTab 인스턴스화     │
# │  JobsTab._run_selected     → PostingEngine 큐에 추가     │
# │  JobsTab._run_all          → 전체 작업 순차 큐 추가      │
# │  JobsTab._run_job          → 단일 작업 큐 추가 핵심 함수 │
# │  JobsTab._stop_all         → engine.stop()+clear (BUG-01)│
# │  JobsTab._stop_job         → 개별 취소 [v1.54 신규]      │
# │  JobsTab._on_job_done      → 완료 후 UI·통계 갱신        │
# │  JobsTab._update_job_status→ Treeview 상태 컬럼 갱신     │
# │  JobsTab._load_template_for_job → migrate 포함 로드      │
# └─────────────────────────────────────────────────────────┘
#
from __future__ import annotations

import json, sys, threading, time, random, string, re, queue, asyncio
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from datetime import datetime
from typing import Any

# ── ttkbootstrap (있으면 사용, 없으면 순수 tkinter 폴백) ──
try:
    import ttkbootstrap as tbs
    from ttkbootstrap.constants import *
    HAS_TBS = True
except ImportError:
    tbs = None
    HAS_TBS = False

# ── 선택적 패키지 ──────────────────────────────────────────
try:
    import pyautogui
    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False

try:
    import pyperclip
    HAS_PYPERCLIP = True
except ImportError:
    HAS_PYPERCLIP = False

try:
    import pytesseract
    from PIL import ImageGrab, Image
    HAS_OCR = True
except ImportError:
    HAS_OCR = False

try:
    import openpyxl
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False

try:
    import requests as _requests
    from io import StringIO as _StringIO
    import csv as _csv_login
    HAS_REQUESTS = True
except ImportError:
    _requests = None          # type: ignore
    _StringIO  = None         # type: ignore
    _csv_login = None         # type: ignore
    HAS_REQUESTS = False

# ── 구글 시트 로그인 URL ──────────────────────────────────
# · 기본값: 아래 SHEET_URL 상수
# · 덮어쓰기: Config/config.json → "sheet_url" 키 사용 가능
SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "17FeZ6QSDjfVJanOly36jsGPaImZCMzol7bM8HvnUuRA"
    "/export?format=csv&gid=0"
)

# ── 버전 ───────────────────────────────────────────────────
APP_VERSION = "1.61"
APP_TITLE   = f"메신저 올인원 v{APP_VERSION}"

# ─────────────────────────────────────────────────────────────────────────────
# Code F: DEFAULT_SCHEDULE — 중앙 관리 스케줄 기본값  [v1.58 CHANGE-X1]
# ─────────────────────────────────────────────────────────────────────────────
_CURRENT_MIG_VER = 10   # 마이그레이션 최고 버전

_KR_TO_INT: dict = {        # 한글 요일 → 숫자 인덱스 (datetime.weekday() 기준)
    "월": 0, "화": 1, "수": 2, "목": 3, "금": 4, "토": 5, "일": 6,
}
_INT_TO_KR: list = ["월", "화", "수", "목", "금", "토", "일"]

DEFAULT_SCHEDULE: dict = {
    "days":              [0, 1, 2, 3, 4],   # 월~금 (숫자 인덱스)
    "schedule_on":       False,
    "schedule_mode":     "time",
    "schedule_times":    [],
    "schedule_time":     "09:00",
    "schedule_interval": 24,
    "interval_variance": 0,
    "enabled":           True,
    "last_run":          "",
    "last_run_date":     "",
    "last_duration":     0.0,   # v1.60: 마지막 실행 소요시간(초)
    "estimated_duration": 0.0,  # v1.60: 예상 소요시간(초, 0=자동)
}

# ─────────────────────────────────────────────────────────────────────────────
# Code D: _migrate_legacy_json()  [v1.58 CHANGE-X2]
# ─────────────────────────────────────────────────────────────────────────────
def _migrate_legacy_json() -> int:
    """레거시 작업 JSON 파일을 v1.58 스키마로 마이그레이션.

    반환값: 업그레이드된 작업 수 (0이면 모두 최신)

    MIGRATE-1  인코딩 폴백 (utf-8 → cp949 → latin-1)
    MIGRATE-2  schedule_days(KR) → days(int) 변환
    MIGRATE-3  DEFAULT_SCHEDULE 기반 누락 키 보충
    MIGRATE-4  레거시 jobs.json 단일파일 → jobs/ 폴더 분리
    MIGRATE-5  _migrated_version 플래그 기록
    MIGRATE-6  stats.json 구조 검증 및 복구
    MIGRATE-7  업그레이드 카운트 반환
    MIGRATE-8  마이그레이션 전 .bak 자동 백업
    MIGRATE-9  UTF-8 BOM 파일 처리
    MIGRATE-10 schedule_times 포맷 검증 및 정제
    """
    import json as _json
    import re as _re_mig
    import shutil as _shutil
    import logging as _log

    upgraded = 0

    # ── MIGRATE-4: 레거시 jobs.json 단일파일 분리 ─────────────────────────────
    legacy_jobs_path = CONFIG_DIR / "jobs.json"
    if legacy_jobs_path.exists():
        try:
            raw = None
            for enc in ("utf-8-sig", "utf-8", "cp949", "latin-1"):
                try:
                    raw = legacy_jobs_path.read_text(encoding=enc)
                    break
                except (UnicodeDecodeError, LookupError):
                    continue
            if raw:
                jobs_list = _json.loads(raw)
                if isinstance(jobs_list, list):
                    for job in jobs_list:
                        if not isinstance(job, dict) or not job.get("name"):
                            continue
                        fname = (job["name"].replace(" ", "_")
                                            .replace("/", "_") + ".json")
                        out = JOBS_DIR / fname
                        if not out.exists():
                            # BUG-F4: 분리 시 키 변환 통합 (2번 쓰기 방지)
                            if "schedule_days" in job and "days" not in job:
                                _kr = job["schedule_days"]
                                if isinstance(_kr, list):
                                    job["days"] = sorted(set(
                                        _KR_TO_INT[d] for d in _kr
                                        if isinstance(d, str) and d in _KR_TO_INT
                                    ))
                            import copy as _cp4
                            for _k4, _v4 in DEFAULT_SCHEDULE.items():
                                job.setdefault(_k4, _cp4.deepcopy(_v4))
                            job["_migrated_version"] = _CURRENT_MIG_VER
                            out.write_text(
                                _json.dumps(job, ensure_ascii=False, indent=2),
                                encoding="utf-8")
                            upgraded += 1
            legacy_jobs_path.rename(legacy_jobs_path.with_suffix(".json.bak"))
        except Exception as _e:
            _log.warning(f"[MIGRATE-4] jobs.json 분리 실패: {_e}")

    # ── 각 작업 JSON 파일 처리 ──────────────────────────────────────────────
    for fpath in sorted(JOBS_DIR.glob("*.json")):
        # ── MIGRATE-1 + MIGRATE-9: 인코딩 폴백 읽기 ─────────────────────────
        raw = None
        for enc in ("utf-8-sig", "utf-8", "cp949", "latin-1"):
            try:
                raw = fpath.read_text(encoding=enc)
                break
            except (UnicodeDecodeError, LookupError):
                continue
        if raw is None:
            _log.warning(f"[MIGRATE-1] {fpath.name} 읽기 실패 — 모든 인코딩 시도 후 포기")
            continue

        try:
            data = _json.loads(raw)
        except _json.JSONDecodeError as _e:
            _log.warning(f"[MIGRATE] {fpath.name} JSON 파싱 오류: {_e}")
            continue

        if not isinstance(data, dict):
            continue

        # 이미 최신 버전이면 스킵
        if data.get("_migrated_version", 0) >= _CURRENT_MIG_VER:
            continue

        changed = False

        # ── MIGRATE-8: 마이그레이션 전 백업 ─────────────────────────────────
        bak_path = fpath.with_suffix(".json.bak")
        if not bak_path.exists():
            try:
                _shutil.copy2(fpath, bak_path)
            except Exception:
                pass

        # ── MIGRATE-2: schedule_days(KR) → days(int) ────────────────────────
        if "schedule_days" in data and "days" not in data:
            kr_list = data["schedule_days"]
            if isinstance(kr_list, list):
                int_days = []
                for d in kr_list:
                    if isinstance(d, str) and d in _KR_TO_INT:
                        int_days.append(_KR_TO_INT[d])
                    elif isinstance(d, int) and 0 <= d <= 6:
                        int_days.append(d)
                data["days"] = sorted(set(int_days))
                changed = True

        # ── MIGRATE-3: DEFAULT_SCHEDULE 기반 누락 키 보충 ───────────────────
        for k, v in DEFAULT_SCHEDULE.items():
            if k not in data:
                import copy as _copy
                data[k] = _copy.deepcopy(v)
                changed = True

        # schedule_days(KR) 하위호환 동기화
        if "days" in data and "schedule_days" not in data:
            data["schedule_days"] = [_INT_TO_KR[i] for i in data["days"]
                                     if 0 <= i <= 6]
            changed = True

        # ── MIGRATE-10: schedule_times 포맷 검증 ────────────────────────────
        if "schedule_times" in data and isinstance(data["schedule_times"], list):
            valid_times = []
            for t in data["schedule_times"]:
                if isinstance(t, str) and _re_mig.fullmatch(r"\d{2}:\d{2}", t):
                    h, m = int(t[:2]), int(t[3:])
                    if 0 <= h <= 23 and 0 <= m <= 59:
                        valid_times.append(t)
            if valid_times != data["schedule_times"]:
                data["schedule_times"] = valid_times
                changed = True

        # ── MIGRATE-5: _migrated_version 플래그 ─────────────────────────────
        if changed or data.get("_migrated_version", 0) < _CURRENT_MIG_VER:
            data["_migrated_version"] = _CURRENT_MIG_VER
            try:
                fpath.write_text(
                    _json.dumps(data, ensure_ascii=False, indent=2),
                    encoding="utf-8")
                upgraded += 1
            except Exception as _e:
                _log.warning(f"[MIGRATE-5] {fpath.name} 저장 실패: {_e}")

    # ── MIGRATE-6: stats.json 구조 검증 ─────────────────────────────────────
    try:
        stats = load_json(STATS_PATH, None)
        if not isinstance(stats, dict) or "stats" not in stats:
            save_json(STATS_PATH, {"stats": [], "total": {}})
    except Exception:
        pass

    return upgraded

# ─────────────────────────────────────────────────────────────────────────────
# Code E: _show_migration_notice()  [v1.58 CHANGE-X3]
# ─────────────────────────────────────────────────────────────────────────────
def _show_migration_notice(count: int) -> None:
    """마이그레이션 완료 팝업 (MIGRATE-7 연결)"""
    import tkinter.messagebox as _mb
    if count <= 0:
        return
    _mb.showinfo(
        "데이터 업그레이드 완료",
        f"✅ {count}개 작업 파일이 v1.58 형식으로 업그레이드되었습니다.\n\n"
        "【확인 필요 사항】\n"
        "· 스케줄이 꺼진 작업은 직접 다시 켜주세요\n"
        "  (이전에 schedule_on 키가 없던 작업은 OFF로 초기화됨)\n"
        "· 요일 설정이 평일(월~금)로 초기화된 작업이 있을 수 있습니다\n"
        "  → 작업 수정 > 스케줄 탭에서 요일을 다시 선택하세요\n\n"
        "【구형 PC 권장 사항】\n"
        "· Windows 시계를 인터넷 시간과 동기화해 주세요\n"
        "  (설정 > 시간 및 언어 > 지금 동기화)\n\n"
        "· 백업: Config/jobs/*.json.bak 파일로 복원 가능\n"
        "· 문제 발생 시 .bak 파일을 .json으로 이름 변경 후 재시작",
    )

# ─────────────────────────────────────────────────────────────────────────────
# Code X4: _check_time_match()  [v1.58 CHANGE-X4]
# ─────────────────────────────────────────────────────────────────────────────
def _check_time_match(now_hm: str, target_hm: str, variance: int = 0) -> bool:
    """현재 시각(HH:MM)과 목표 시각(HH:MM)이 ±variance 분 이내인지 확인
    BUG-F2 수정: 자정 경계(23:58~00:02) 처리 — min(diff, 1440-diff) 사용
    """
    try:
        nh, nm = int(now_hm[:2]), int(now_hm[3:])
        th, tm = int(target_hm[:2]), int(target_hm[3:])
        now_min    = nh * 60 + nm
        target_min = th * 60 + tm
        diff = abs(now_min - target_min)
        # 자정 경계: 23:58~00:02 = 실제 4분 차이이지만 단순 abs는 1436분
        diff = min(diff, 1440 - diff)
        return diff <= variance
    except Exception:
        return now_hm == target_hm

# ── 경로 설정 ───────────────────────────────────────────────
def _app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).parent

APP_DIR      = _app_dir()
CONFIG_DIR   = APP_DIR / "Config"
TEMPLATE_DIR = CONFIG_DIR / "templates"   # 작업 템플릿 저장
JOBS_DIR     = CONFIG_DIR / "jobs"        # 작업 저장
LOGS_DIR        = APP_DIR  / "logs"
DATA_DIR        = APP_DIR  / "data"
SCREENSHOTS_DIR = APP_DIR  / "screenshots"   # 스크린샷 저장 폴더

def _open_folder(path):
    """탐색기(Windows) 또는 파인더(Mac)/파일관리자(Linux)로 폴더 열기"""
    import subprocess as _sp, sys as _sys
    try:
        if _sys.platform == "win32":
            import os as _os; _os.startfile(str(path))
        elif _sys.platform == "darwin":
            _sp.Popen(["open", str(path)])
        else:
            _sp.Popen(["xdg-open", str(path)])
    except Exception:
        pass

for _d in (CONFIG_DIR, TEMPLATE_DIR, JOBS_DIR, LOGS_DIR, DATA_DIR, SCREENSHOTS_DIR):
    _d.mkdir(parents=True, exist_ok=True)

CONFIG_PATH = CONFIG_DIR / "config.json"
STATS_PATH  = CONFIG_DIR / "stats.json"

# ── UI 팔레트 (v1.10 라이트 테마 — community_poster 벤치마킹) ─
PALETTE = {
    # ── 배경 계층 ─────────────────────────────────────────────
    "bg":       "#F0F2F5",   # 메인 배경 — 차분한 회청
    "sidebar":  "#0F172A",   # 사이드바 — 딥 네이비
    "sidebar_h":"#1E3A5F",   # 사이드바 활성 — 미드 블루
    "card":     "#FFFFFF",   # 카드/패널 흰색
    "card2":    "#F8FAFC",   # 입력창 배경
    # ── 테두리/구분선 ─────────────────────────────────────────
    "border":   "#E2E8F0",   # 일반 테두리
    "border2":  "#CBD5E1",   # 강조 테두리
    # ── 인터랙션 ─────────────────────────────────────────────
    "hover":    "#EFF6FF",   # hover 배경
    "active":   "#DBEAFE",   # 활성 배경
    "selected": "#BFDBFE",   # 트리뷰 선택 행
    # ── 포인트 컬러 ───────────────────────────────────────────
    "primary":  "#1D4ED8",   # 블루 포인트
    "primary2": "#1E40AF",   # 블루 호버
    "success":  "#059669",   # 성공 초록 (emerald-600)
    "success_text": "#065F46",
    "warning_text": "#92400E",
    "warning":  "#D97706",   # 경고 앰버
    "danger":   "#DC2626",   # 위험 레드
    "accent":   "#7C3AED",   # 강조 바이올렛
    # ── 텍스트 계층 ───────────────────────────────────────────
    "text":     "#0F172A",   # 기본 텍스트
    "text2":    "#475569",   # 보조 텍스트
    "muted":    "#64748B",   # 힌트 텍스트
    # ── 사이드바 전용 ─────────────────────────────────────────
    "sidebar_text": "#E2E8F0",
    # ── 플랫폼 원색 ───────────────────────────────────────────
    "kakao":    "#FEE500",
    "telegram": "#229ED9",
}

# ── 폰트 상수 (v1.61 UI 리디자인) ────────────────────────
_FF  = "Malgun Gothic"
_FFM = "Consolas"
F_TITLE  = (_FF,  14, "bold")  # 탭 제목
F_HEAD   = (_FF,  10, "bold")  # 섹션 헤더
F_BODY   = (_FF,  10)          # 본문
F_LABEL  = (_FF,   9)          # 라벨 (입력 필드 라벨, 일반 항목)
F_SMALL  = (_FF,   8)          # 보조/힌트 (경고문, 설명, 캡션) ← 8pt로 분리
F_BTN    = (_FF,  10, "bold")  # 주요 버튼
F_BTN_S  = (_FF,   9, "bold")  # 소형 버튼
F_MONO   = (_FFM,  9)          # 입력창/좌표
F_MONO_S = (_FFM,  8)          # 보조 모노 (힌트용) ← 8pt로 분리
F_MONO_B = (_FFM, 10, "bold")
F_ICON   = ("Segoe UI Emoji", 16)

# ============================================================
# ToolTip — 마우스 호버 시 간단 설명 표시
# ============================================================

class ToolTip:
    """위젯에 마우스를 올리면 작은 팝업 설명 표시"""
    _delay = 600  # ms

    def __init__(self, widget, text: str):
        self._widget = widget
        self._text   = text
        self._tip    = None
        self._job    = None
        widget.bind("<Enter>",  self._schedule, add="+")
        widget.bind("<Leave>",  self._cancel,   add="+")
        widget.bind("<Button>", self._cancel,   add="+")

    def _schedule(self, _e=None):
        self._cancel()
        self._job = self._widget.after(self._delay, self._show)

    def _cancel(self, _e=None):
        if self._job:
            self._widget.after_cancel(self._job)
            self._job = None
        self._hide()

    def _show(self):
        if self._tip: return
        x = self._widget.winfo_rootx() + self._widget.winfo_width() // 2
        y = self._widget.winfo_rooty() + self._widget.winfo_height() + 6
        self._tip = tk.Toplevel(self._widget)
        self._tip.wm_overrideredirect(True)
        self._tip.wm_geometry(f"+{x}+{y}")
        lbl = tk.Label(self._tip, text=self._text,
                       font=(_FF, 8), justify=tk.LEFT,
                       bg="#FFFDE7", fg="#333333",
                       relief=tk.SOLID, bd=1,
                       padx=6, pady=4, wraplength=260)
        lbl.pack()

    def _hide(self):
        if self._tip:
            self._tip.destroy()
            self._tip = None


def add_tip(widget, text: str) -> "ToolTip":
    """위젯에 ToolTip을 붙이고 반환"""
    return ToolTip(widget, text)


# ── 사이드바 탭 ─────────────────────────────────────────────
SIDEBAR_TABS = [
    ("templates",         "🗂️  작업 템플릿"),
    ("jobs",              "📋  작업 관리"),
    ("telegram_accounts", "✈️  텔레그램 계정"),
    ("log",               "🗒️  로그"),
    ("stats",             "📊  통계"),
    ("settings",          "⚙️   설정"),
]

# ── 플랫폼 정의 ─────────────────────────────────────────────
PLATFORMS = {
    "kakao":    {"name": "카카오톡", "color": "#FEE500", "text": "#333333"},
    "telegram": {"name": "텔레그램", "color": "#229ED9", "text": "#ffffff"},
}
# ── 플랫폼별 작업 유형 정의 ────────────────────────────────
PLATFORM_WORKFLOWS = {
    "kakao_friend": {
        "name":         "가망 친구추가",
        "platform":     "kakao",
        "needs_ocr":    False,  # 색상 탐지 방식 (Tesseract 불필요)
        "needs_message":False,
        "needs_image":  False,
        "coord_keys":   ["id_add_btn", "status_dot", "friend_add_btn",
                         "profile_area", "confirm_btn", "close_btn"],
        "coord_labels": ["🔑 ID로 추가 좌표", "🎨 친추가능 확인 색상좌표",
                         "➕ 친구추가 버튼 좌표", "👤 프로필 좌표",
                         "✅ 확인 좌표", "❌ 닫기 좌표"],
        "coord_types":  ["point", "point", "point", "point", "point", "point"],
    },
    "kakao_openchat": {
        "name":         "오픈채팅/아침인사/가망뿌리기",
        "platform":     "kakao",
        "needs_ocr":    False,
        "needs_message":True,
        "needs_image":  True,
        # 좌표는 모두 전용 섹션에서 관리 (coord_keys 미사용)
        # - 채팅방 시작좌표 → 좌표 자동계산 섹션 (grid_config)
        # - 전송/닫기 버튼  → 전송·닫기 방식 섹션
    },
    "telegram_join": {
        "name":         "그룹 가입",
        "platform":     "telegram",
        "needs_ocr":    False,
        "needs_message":False,
        "needs_image":  False,
        # Telethon 있으면 API 방식, 없으면 pyautogui(크롬) 방식 폴백
        "needs_telethon": False,   # 없어도 동작 (pyautogui 폴백)
        "telethon_preferred": True,  # Telethon 권장
        "coord_keys":   ["chrome_addr", "join_btn", "close_tab"],
        "coord_labels": ["🌐 크롬 주소창", "✅ 가입 버튼", "❌ 탭 닫기"],
        "coord_types":  ["point", "point", "point"],
        "coord_note":   "Telethon 계정 설정 시 좌표 불필요 (API 방식 사용)",
    },
    "telegram_message": {
        "name":         "메시지 발송",
        "platform":     "telegram",
        "needs_ocr":    False,
        "needs_message":True,
        "needs_image":  True,   # 이미지 첨부 지원
        "needs_telethon": False,   # 없어도 동작 (pyautogui 폴백)
        "telethon_preferred": True,  # Telethon 권장
        "coord_keys":   ["chrome_addr", "message_input", "send_btn"],
        "coord_labels": ["🌐 크롬 주소창", "✏️ 메시지 입력창", "📤 전송 버튼"],
        "coord_types":  ["point", "point", "point"],
        "coord_note":   "Telethon 계정 설정 시 좌표 불필요 (API 방식 사용)",
    },
    "telegram_join_and_message": {
        "name":         "가입 후 메시지 발송",
        "platform":     "telegram",
        "needs_ocr":    False,
        "needs_message":True,
        "needs_image":  True,   # 이미지 첨부 지원
        "needs_telethon": False,   # Telethon 권장, 없어도 join_first 옵션으로 동작
        "telethon_preferred": True,
        "coord_keys":   ["chrome_addr", "join_btn", "message_input", "send_btn"],
        "coord_labels": ["🌐 크롬 주소창", "✅ 가입 버튼", "✏️ 메시지 입력창", "📤 전송 버튼"],
        "coord_types":  ["point", "point", "point", "point"],
        "coord_note":   "Telethon 계정 설정 시 좌표 불필요 (API 방식 사용)",
    },
}


# ── v1.60: 워크플로우별 기본 예상 소요시간(초) ────────────────────────
WORKFLOW_BASE_DURATION: dict = {
    "kakao_friend":    90,
    "kakao_openchat": 120,
    "telegram_join":   60,
    "telegram_message": 75,
    "telegram_join_and_message": 120,   # 가입(60s) + 메시지(60s) 합산
}
WORKFLOW_BASE_DURATION_DEFAULT = 90

# ── 카카오 친구추가 이름/번호 패턴 ────────────────────────
# 사용자가 자유 조합 가능한 변수 토큰

# ── 워크플로우별 예시 CSV 데이터 ───────────────────────────
SAMPLE_CSV_DATA = {
    "kakao_friend": {
        "filename": "예시_카카오친추.csv",
        "header":   "카카오아이디",
        "rows": [
            ("honggildong",),
            ("kimcs1990",),
            ("lee_yh",),
            ("park_mj2",),
            ("choi_jw88",),
        ],
        "hint": "※ 첫 번째 컬럼만 읽습니다 (헤더: 카카오아이디 / id / kakao_id / 아이디)",
    },
    "telegram_join": {
        "filename": "예시_텔레그램가입.csv",
        "header":   "이름,텔레그램링크",
        "rows": [
            ("채널A",  "https://t.me/channel_a"),
            ("채널B",  "https://t.me/channel_b"),
            ("그룹C",  "https://t.me/group_c"),
            ("채널D",  "t.me/channel_d"),
            ("그룹E",  "https://t.me/joinchat/XXXXXXXXXX"),
        ],
        "hint": "※ 텔레그램링크: https://t.me/xxx 또는 t.me/xxx 형식",
    },
    "telegram_message": {
        "filename": "예시_텔레그램메시지.csv",
        "header":   "이름,텔레그램링크",
        "rows": [
            ("홍길동",  "https://t.me/honggildong"),
            ("김철수",  "https://t.me/kimcs1990"),
            ("이영희",  "https://t.me/lee_yh"),
            ("박민준",  "https://t.me/park_mj2"),
            ("최지원",  "https://t.me/choi_jw88"),
        ],
        "hint": "※ 텔레그램링크: 개인 사용자 t.me/username 형식",
    },
    "telegram_join_and_message": {
        "filename": "예시_텔레그램가입후발송.csv",
        "header":   "이름,텔레그램링크",
        "rows": [
            ("채널A", "https://t.me/channel_a"),
            ("채널B", "https://t.me/channel_b"),
            ("그룹C", "https://t.me/group_c"),
            ("채널D", "t.me/channel_d"),
            ("그룹E", "https://t.me/joinchat/XXXXXXXXXX"),
        ],
        "hint": "※ 텔레그램링크: 그룹/채널 t.me/xxx 형식 — 가입 후 메시지 자동 발송",
    },
}

# ── 메시지 변수 토큰 (메시지 내 치환용) ────────────────────
MSG_TOKENS = {
    "{이름}":        "CSV의 이름 컬럼",
    "{랜덤숫자2}":   "랜덤 숫자 2자리",
    "{랜덤숫자3}":   "랜덤 숫자 3자리",
    "{랜덤영숫자3}": "랜덤 영숫자 3자리",
}

# ── 유틸 함수 ───────────────────────────────────────────────

# ════════════════════════════════════════════════════════
# OCR 강화 엔진 (kakao_friendbot_v3.0 동일)
# ════════════════════════════════════════════════════════

# OCR 오류 수정 맵 (자주 틀리는 한글 OCR 결과)
# ── 카카오 친추 색상 탐지 헬퍼 ─────────────────────────────
# 색상 유사도: RGB 유클리드 거리
def _kf_color_distance(c1: tuple, c2: tuple) -> float:
    return ((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2) ** 0.5

# 기준 색상 상수 (카카오 PC 기준 근사값, 허용 오차 40)
_KF_COLOR_YELLOW = (247, 190, 0)   # 카카오 노란색 (친구 버튼 활성/기존친구)
_KF_COLOR_WHITE  = (255, 255, 255) # 흰색 (버튼 비활성 / 검색결과 배경)
_KF_COLOR_THRESH = 40              # 색상 판별 허용 오차

def _kf_get_pixel(x: int, y: int) -> tuple:
    """(x,y) 픽셀 RGB 반환. 실패 시 (0,0,0)"""
    try:
        from PIL import ImageGrab as _IG
        img = _IG.grab(bbox=(x, y, x+1, y+1))
        return img.getpixel((0, 0))[:3]
    except Exception:
        return (0, 0, 0)

def _kf_is_yellow(x: int, y: int) -> bool:
    """해당 픽셀이 노란색 계열이면 True"""
    return _kf_color_distance(_kf_get_pixel(x, y), _KF_COLOR_YELLOW) < _KF_COLOR_THRESH

def _kf_is_white(x: int, y: int) -> bool:
    """해당 픽셀이 흰색 계열이면 True"""
    return _kf_color_distance(_kf_get_pixel(x, y), _KF_COLOR_WHITE) < _KF_COLOR_THRESH

def _kf_decide_state_color(status_x: int, status_y: int,
                            friend_x:  int, friend_y:  int) -> str:
    """
    색상 기반 상태 판별
      status_dot  노란색 → 'existing' (기존 친구)
      status_dot  흰색 + friend_add_btn 노란색 → 'new'      (신규, 친추 가능)
      status_dot  흰색 + friend_add_btn 흰색   → 'not_found'(없는 ID)
      그 외                                    → 'error'
    반환: 'new' / 'existing' / 'not_found' / 'error'
    """
    status_yellow = _kf_is_yellow(status_x, status_y)
    status_white  = _kf_is_white(status_x,  status_y)
    friend_yellow = _kf_is_yellow(friend_x, friend_y)

    if status_yellow:
        return 'existing'
    if status_white and friend_yellow:
        return 'new'
    if status_white and not friend_yellow:
        return 'not_found'
    return 'error'


def load_json(path: Path, default: Any = None) -> Any:
    try:
        if path.exists():
            with open(path, encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return default if default is not None else {}

def save_json(path: Path, data: Any) -> bool:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as _e:
        # v1.75: 오류 내용을 stderr에 출력 (디버깅용)
        import sys as _sys_sj, traceback as _tb_sj
        print(f"[save_json ERROR] path={path}  error={_e}", file=_sys_sj.stderr)
        _tb_sj.print_exc(file=_sys_sj.stderr)
        return False

def now_str() -> str:
    return datetime.now().strftime("%H:%M:%S")

def fmt_ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def safe_int(val: Any, default: int = 0) -> int:
    try: return int(float(val))   # "30.8" → 30 (소수 문자열 대응)
    except: return default

def safe_float(val: Any, default: float = 0.0) -> float:
    try: return float(val)
    except: return default

def _lighten(hex_color: str, factor: float = 0.15) -> str:
    """hex 색상을 밝게(factor>0) 또는 어둡게(factor<0) 조정. 결과는 항상 유효한 색상."""
    h = hex_color.lstrip("#")
    if len(h) != 6:
        return hex_color
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    if factor >= 0:
        # 밝게: 흰색 방향으로 블렌드
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
    else:
        # 어둡게: 검정 방향으로 블렌드 (|factor| 비율)
        d = abs(factor)
        r = max(0, int(r * (1 - d)))
        g = max(0, int(g * (1 - d)))
        b = max(0, int(b * (1 - d)))
    return f"#{r:02x}{g:02x}{b:02x}"

def _find_tesseract() -> str | None:
    candidates = [
        APP_DIR / "tesseract.exe",
        APP_DIR / "Tesseract-OCR" / "tesseract.exe",
        Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe"),
        Path(r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"),
    ]
    for c in candidates:
        if c.exists(): return str(c)
    import shutil
    return shutil.which("tesseract")

def resolve_name_number(pattern: str, row: dict) -> str:
    """메시지 내 변수 토큰 치환 (메시지 뿌리기용)"""
    result = pattern
    name   = str(row.get("이름", row.get("name", "")))
    result = result.replace("{이름}", name)
    result = result.replace("{랜덤숫자2}",
        "".join(random.choices(string.digits, k=2)))
    result = result.replace("{랜덤숫자3}",
        "".join(random.choices(string.digits, k=3)))
    result = result.replace("{랜덤영숫자3}",
        "".join(random.choices(
            string.ascii_letters + string.digits, k=3)))
    return result


def build_search_id(keyword: str, start_num: int,
                    idx: int, digits: int = 0) -> str:
    """
    친구추가 검색 ID 생성 (키워드 + 순번)
    keyword="가망", start_num=101, idx=0  → "가망101"
    keyword="가망", start_num=101, idx=1  → "가망102"
    digits=3 이면 번호를 3자리 고정: "가망001"
    """
    num = start_num + idx
    if digits > 0:
        num_str = str(num).zfill(digits)
    else:
        num_str = str(num)
    return f"{keyword}{num_str}"



# ============================================================
# Block 1-C : App 클래스 — 윈도우 초기화 + 헤더 + 사이드바
# ============================================================

def calculate_coordinates(start_x: float, start_y: float,
                           cell_height: float,
                           column_count: int, row_count: int,
                           cell_width: float,
                           scan_dir: str = "col") -> list:
    """
    그리드 좌표 자동 계산 (카카오 채팅 타일 대응)  [v1.52 수정]
    cell_width  : 가로 슬롯 크기 = 열 간격 (column_gap 역할 통합)
    cell_height : 세로 슬롯 크기 (0이면 모든 행이 start_y 동일)
    scan_dir="col" : 열 우선 (↓→)  ex) col0 row0..N → col1 row0..N
    scan_dir="row" : 행 우선 (→↓)  ex) row0 col0..N → row1 col0..N
    열·행 수에 제한 없음 (무제한 좌표 생성)
    """
    coords = []
    if scan_dir == "col":
        for col in range(column_count):
            for row in range(row_count):
                x = start_x + col * cell_width
                y = start_y + row * cell_height
                coords.append((round(x), round(y)))
    else:
        for row in range(row_count):
            for col in range(column_count):
                x = start_x + col * cell_width
                y = start_y + row * cell_height
                coords.append((round(x), round(y)))
    return coords

def filter_valid_coords(coords: list) -> list:
    """화면 밖 좌표 필터링 (음수 허용 → 듀얼 모니터 고려)"""
    try:
        sw, sh = pyautogui.size()
    except Exception:
        sw, sh = 1920 * 3, 1080 * 3
    return [(x, y) for x, y in coords
            if -sw < x < sw * 2 and -sh < y < sh * 2]


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1280x800")
        self.minsize(1100, 700)
        self.configure(bg=PALETTE["bg"])

        # ── 전역 ttk 스타일 초기화 ─────────────────────────
        _style = ttk.Style(self)
        _style.theme_use("default")
        # Treeview 공통 스타일
        _style.configure("Treeview",
                         background=PALETTE["card"],
                         foreground=PALETTE["text"],
                         fieldbackground=PALETTE["card"],
                         rowheight=30,
                         borderwidth=0,
                         font=(_FF, 9))
        _style.configure("Treeview.Heading",
                         background=PALETTE["sidebar"],
                         foreground="#CBD5E1",
                         relief="flat",
                         font=(_FF, 9, "bold"),
                         padding=(8, 7))
        _style.map("Treeview",
                   background=[("selected", PALETTE["primary"])],
                   foreground=[("selected", "#FFFFFF")])
        _style.layout("Treeview",
                      [("Treeview.treearea", {"sticky": "nswe"})])
        # Combobox 스타일
        _style.configure("TCombobox",
                         fieldbackground=PALETTE["card2"],
                         background=PALETTE["card2"],
                         foreground=PALETTE["text"],
                         selectbackground=PALETTE["primary"],
                         selectforeground="#FFFFFF",
                         bordercolor=PALETTE["border"],
                         lightcolor=PALETTE["border"],
                         darkcolor=PALETTE["border"])
        # Scrollbar 스타일
        _style.configure("Vertical.TScrollbar",
                         background=PALETTE["border"],
                         troughcolor=PALETTE["bg"],
                         bordercolor=PALETTE["border"],
                         arrowcolor=PALETTE["muted"])

        # ── 데이터 로드 ────────────────────────────────────
        self.config_data = load_json(CONFIG_PATH, self._default_config())
        self.stats_data  = load_json(STATS_PATH,  {"stats": [], "total": {}})

        # ── 상태 변수 ──────────────────────────────────────
        self._active_tab: str = "templates"
        self._tab_btns:   dict = {}
        self._tab_frames: dict[str, tk.Frame] = {}
        self._status_var  = tk.StringVar(value="준비")
        self._queue_var   = tk.StringVar(value="실행 없음")
        self._sched_var   = tk.StringVar(value="스케줄 OFF")

        # ── UI 빌드 ────────────────────────────────────────
        self._build_ui()

        # ── v1.58 CHANGE-X15: 마이그레이션 수행 및 팝업 ──────────────────────
        try:
            _mig_count = _migrate_legacy_json()
            if _mig_count > 0:
                self.after(500, lambda: _show_migration_notice(_mig_count))
        except Exception as _mig_err:
            import logging as _mig_log
            _mig_log.warning(f"[App.__init__] 마이그레이션 오류: {_mig_err}")

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ── 기본 설정 ───────────────────────────────────────────
    def _default_config(self) -> dict:
        return {
            "paths": {
                "logs":      str(LOGS_DIR),
                "output":    str(DATA_DIR),
                "tesseract": _find_tesseract() or "",
            },
            "mouse": {
                "click_delay": 0.15,
                "type_delay":  0.05,
                "jitter":      0.3,
                "failsafe":    True,
            },
            "global_delay": {
                "min": 2.0,
                "max": 5.0,
            },
            # 스크린샷 캡처 설정
            "screenshot": {
                "enabled":      True,   # 캡처 기능 ON/OFF
                "interval_min": 60.0,   # 주기적 캡처 간격 (초, 기본 60초=1분)
                "on_error":     True,   # 오류 발생 시 즉시 캡처
            },
            # Telegram API 앱 인증 정보 — 계정 공통 (my.telegram.org 에서 1회 발급)
            "tg_api": {
                "api_id":   "",
                "api_hash": "",
            },
            # Telethon API 모드 기본 딜레이 (템플릿에서 개별 오버라이드 가능)
            "tg_api_defaults": {
                "connect_delay": 2.0,   # 계정 연결 간격(s)
                "retry_delay":   5.0,   # 재시도 대기(s)
                "before_send":   0.5,   # 발송 전 대기(s)
                "after_send":    1.0,   # 발송 후 대기(s)
                "capture_delay": 2.0,   # 채팅 캡처 전 대기(s)
                "capture_msgs":  5,     # 캡처할 최근 메시지 수
                "capture_on":    True,  # 발송 후 채팅 캡처 ON
                "acct_warmup":   0.5,   # 계정 전환 시 추가 대기(s)
            },
        }

    # ─────────────────────────────────────────────────────────
    # [UI-1] 스타일 헬퍼 메서드 (community_poster v5.20 이식)
    # ─────────────────────────────────────────────────────────
    def _card(self, parent, padx=16, pady=12):
        """border 1px + padding 카드 컨테이너"""
        outer = tk.Frame(parent, bg=PALETTE["bg"])
        inner = tk.Frame(outer, bg=PALETTE["card"],
                         highlightbackground=PALETTE["border"],
                         highlightthickness=1)
        inner.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        pad = tk.Frame(inner, bg=PALETTE["card"])
        pad.pack(fill=tk.BOTH, expand=True, padx=padx, pady=pady)
        return outer, pad

    def _button(self, parent, text, command, color=None,
                text_color="#FFFFFF", size=9, width=None, **kw):
        """hover 효과 내장 버튼"""
        orig = color or PALETTE["primary"]
        cfg = dict(text=text, command=command,
                   font=(_FF, size, "bold"),
                   bg=orig, fg=text_color,
                   activebackground=orig,
                   activeforeground=text_color,
                   relief="flat", cursor="hand2",
                   padx=12, pady=5, bd=0)
        if width:
            cfg["width"] = width
        cfg.update(kw)
        b = tk.Button(parent, **cfg)
        b.bind("<Enter>", lambda e: b.config(bg=self._darken(orig)))
        b.bind("<Leave>", lambda e: b.config(bg=orig))
        return b

    def _darken(self, hex_color: str, factor: float = 0.85) -> str:
        """hover 시 색상 어둡게"""
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return "#{:02x}{:02x}{:02x}".format(
            int(r * factor), int(g * factor), int(b * factor))

    def _label(self, parent, text, size=10, weight="normal",
               color=None, **kw):
        return tk.Label(parent, text=text,
                        font=(_FF, size, weight),
                        fg=color or PALETTE["text"],
                        bg=parent.cget("bg"), **kw)

    def _badge(self, parent, text, color):
        """색상 배경 작은 뱃지"""
        f = tk.Frame(parent, bg=color, padx=6, pady=2)
        tk.Label(f, text=text, font=(_FF, 8, "bold"),
                 fg="#fff", bg=color).pack()
        return f

    def _separator(self, parent, orient="horizontal", color=None):
        c = color or PALETTE["border"]
        if orient == "horizontal":
            return tk.Frame(parent, bg=c, height=1)
        return tk.Frame(parent, bg=c, width=1)

    # ─────────────────────────────────────────────────────────
    # 전체 UI
    # ─────────────────────────────────────────────────────────
    def _build_ui(self):
        self._build_header()
        body = tk.Frame(self, bg=PALETTE["bg"])
        body.pack(fill=tk.BOTH, expand=True)
        self._build_sidebar(body)
        self._build_content(body)
        self._build_statusbar()

    # ── [UI-2] 헤더 — 실시간 상태 표시 ──────────────────────
    def _build_header(self):
        hdr = tk.Frame(self, bg=PALETTE["sidebar"], height=52)
        hdr.pack(fill=tk.X, side=tk.TOP)
        hdr.pack_propagate(False)

        # 좌: 로고 영역
        logo = tk.Frame(hdr, bg=PALETTE["sidebar"])
        logo.pack(side=tk.LEFT, padx=(18, 0))
        tk.Label(logo, text="💬", font=("Segoe UI Emoji", 18),
                 fg="#60A5FA", bg=PALETTE["sidebar"]
                 ).pack(side=tk.LEFT)
        tk.Label(logo, text=" 메신저 올인원",
                 font=(_FF, 14, "bold"), fg="#F8FAFC",
                 bg=PALETTE["sidebar"]).pack(side=tk.LEFT)
        tk.Label(logo, text=f"  v{APP_VERSION}",
                 font=(_FF, 9), fg="#475569",
                 bg=PALETTE["sidebar"]).pack(side=tk.LEFT)

        # 우: 상태 알약형 뱃지
        right = tk.Frame(hdr, bg=PALETTE["sidebar"])
        right.pack(side=tk.RIGHT, padx=18)

        # 의존성 표시
        dep_parts = []
        dep_parts.append(("PyAG", HAS_PYAUTOGUI))
        dep_parts.append(("OCR",  HAS_OCR))
        dep_parts.append(("CB",   HAS_PYPERCLIP))
        for name, ok in dep_parts:
            pill = tk.Frame(right, bg="#1E3A5F" if ok else "#3B1919",
                            padx=7, pady=2)
            pill.pack(side=tk.RIGHT, padx=3)
            tk.Label(pill,
                     text=f"{'✓' if ok else '✗'} {name}",
                     font=(_FF, 8, "bold"),
                     fg="#86EFAC" if ok else "#FCA5A5",
                     bg="#1E3A5F" if ok else "#3B1919"
                     ).pack()

        tk.Frame(right, bg="#1E293B", width=1, height=24
                 ).pack(side=tk.RIGHT, padx=10, fill=tk.Y)

        # 스케줄/실행 상태
        for var, ico in [(self._sched_var, "🗓"), (self._queue_var, "⚙")]:
            f = tk.Frame(right, bg=PALETTE["sidebar"])
            f.pack(side=tk.RIGHT, padx=(0, 6))
            tk.Label(f, text=ico, font=("Segoe UI Emoji", 10),
                     fg="#94A3B8", bg=PALETTE["sidebar"]).pack(side=tk.LEFT)
            tk.Label(f, textvariable=var,
                     font=(_FF, 9), fg="#CBD5E1",
                     bg=PALETTE["sidebar"]).pack(side=tk.LEFT, padx=(2, 0))

    # ── [UI-3] 사이드바 — tk.Button 전환 + 활성 탭 명확화 ──
    def _build_sidebar(self, parent: tk.Frame):
        sb = tk.Frame(parent, bg=PALETTE["sidebar"], width=220)
        sb.pack(fill=tk.Y, side=tk.LEFT)
        sb.pack_propagate(False)
        # 우측 얇은 그림자 구분선
        tk.Frame(parent, bg="#1E293B", width=1
                 ).pack(fill=tk.Y, side=tk.LEFT)

        tk.Frame(sb, bg=PALETTE["sidebar"], height=12).pack()

        # 섹션 레이블
        tk.Label(sb, text="  MENU",
                 font=(_FF, 8, "bold"), fg="#334155",
                 bg=PALETTE["sidebar"], anchor="w"
                 ).pack(fill=tk.X, padx=12, pady=(4, 6))

        self._nav_buttons: dict = {}
        _tab_icons = {
            "templates":         "🗂",
            "jobs":              "📋",
            "telegram_accounts": "✈",
            "log":               "🗒",
            "stats":             "📊",
            "settings":          "⚙",
        }
        _tab_labels = {
            "templates":         "작업 템플릿",
            "jobs":              "작업 관리",
            "telegram_accounts": "텔레그램 계정",
            "log":               "로그",
            "stats":             "통계",
            "settings":          "설정",
        }
        for tab_id, _ in SIDEBAR_TABS:
            ico   = _tab_icons.get(tab_id, "•")
            label = _tab_labels.get(tab_id, tab_id)
            btn = tk.Button(
                sb,
                text=f" {ico}  {label}",
                font=(_FF, 10),
                fg="#94A3B8", bg=PALETTE["sidebar"],
                activeforeground="#FFFFFF",
                activebackground=PALETTE["sidebar_h"],
                relief="flat", anchor="w", cursor="hand2",
                padx=8, pady=9,
                command=lambda k=tab_id: self._switch_tab(k)
            )
            btn.pack(fill=tk.X, padx=4, pady=1)
            self._nav_buttons[tab_id] = btn

        # 하단 버전 영역
        tk.Frame(sb, bg=PALETTE["sidebar"]).pack(fill=tk.Y, expand=True)
        sep = tk.Frame(sb, bg="#1E293B", height=1)
        sep.pack(fill=tk.X, padx=12, pady=(0, 6))
        tk.Label(sb, text=f"v{APP_VERSION}  메신저 올인원",
                 font=(_FF, 8), fg="#334155",
                 bg=PALETTE["sidebar"]).pack(pady=(0, 10))

        self._tab_btns = self._nav_buttons

    def _make_tab_btn(self, parent, tab_id: str, label: str):
        """하위호환용 stub — _build_sidebar로 대체됨"""
        pass

    # ── [UI-3] 탭 전환 — 3중 강조 (font/fg/bg) ──────────────
    def _switch_tab(self, tab_id: str):
        for k, btn in self._nav_buttons.items():
            if k == tab_id:
                btn.config(fg="#FFFFFF",
                           bg=PALETTE["sidebar_h"],
                           font=(_FF, 10, "bold"))
            else:
                btn.config(fg="#64748B",
                           bg=PALETTE["sidebar"],
                           font=(_FF, 10))
        for tid, frame in self._tab_frames.items():
            frame.lift() if tid == tab_id else frame.lower()
        self._active_tab = tab_id

    # ── 콘텐츠 영역 ──────────────────────────────────────────
    def _build_content(self, parent: tk.Frame):
        content = tk.Frame(parent, bg=PALETTE["bg"])
        content.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self._content_frame = tk.Frame(content, bg=PALETTE["bg"])
        self._content_frame.pack(fill=tk.BOTH, expand=True,
                                  padx=20, pady=(14, 0))

        builders = {
            "templates":         self._build_templates_tab,
            "jobs":              self._build_jobs_tab,
            "telegram_accounts": self._build_telegram_accounts_tab,
            "log":               self._build_log_tab,
            "stats":             self._build_stats_tab,
            "settings":          self._build_settings_tab,
        }
        for tab_id, builder in builders.items():
            frame = tk.Frame(self._content_frame, bg=PALETTE["bg"])
            self._tab_frames[tab_id] = frame
            builder(frame)
            frame.place(relwidth=1, relheight=1)
            frame.lower()

        self._switch_tab("templates")

    # ── 상태바 ───────────────────────────────────────────────
    def _build_statusbar(self):
        bar = tk.Frame(self, bg="#0F172A", height=26)
        bar.pack(fill=tk.X, side=tk.BOTTOM)
        bar.pack_propagate(False)
        tk.Frame(bar, bg="#1E293B", height=1
                 ).place(relx=0, rely=0, relwidth=1.0)
        # 좌: 상태 메시지
        tk.Label(bar, text="●",
                 font=(_FF, 9), fg="#22D3EE",
                 bg="#0F172A").pack(side=tk.LEFT, padx=(12, 4))
        tk.Label(bar, textvariable=self._status_var,
                 font=(_FF, 9),
                 bg="#0F172A", fg="#94A3B8",
                 anchor=tk.W).pack(side=tk.LEFT, fill=tk.Y)
        # 우: 날짜
        tk.Label(bar, text=datetime.now().strftime("%Y-%m-%d"),
                 font=(_FFM, 8),
                 bg="#0F172A", fg="#334155",
                 padx=14).pack(side=tk.RIGHT, fill=tk.Y)

    def _set_status(self, msg: str):
        self._status_var.set(msg)

    # ── Placeholder (이후 Block에서 채워짐) ───────────────────
    def _build_templates_tab(self, f):         pass
    def _build_jobs_tab(self, f):              pass
    def _build_telegram_accounts_tab(self, f): pass
    def _build_log_tab(self, f):               pass
    def _build_stats_tab(self, f):             pass
    def _build_settings_tab(self, f):          pass

    # ── 종료 ─────────────────────────────────────────────────
    def _on_close(self):
        save_json(CONFIG_PATH, self.config_data)
        save_json(STATS_PATH,  self.stats_data)
        self.destroy()
# ============================================================
# UI 공용 헬퍼 — 섹션 헤더 (4px 컬러바 + 우측 수평선 + 카드)
# ============================================================

def _make_section_header(parent: tk.Frame, title: str) -> tk.Frame:
    """
    편집 패널 어디서든 쓸 수 있는 통일된 섹션 헤더 + 카드 컨테이너.
    반환값: 카드 Frame (내부 위젯을 이 안에 배치)
    """
    wrap = tk.Frame(parent, bg=PALETTE["bg"])
    wrap.pack(fill=tk.X, padx=16, pady=(0, 10))
    # 제목 행
    title_row = tk.Frame(wrap, bg=PALETTE["bg"])
    title_row.pack(fill=tk.X, pady=(0, 4))
    tk.Frame(title_row, bg=PALETTE["primary"], width=4
             ).pack(side=tk.LEFT, fill=tk.Y)
    tk.Label(title_row, text=f"  {title}",
             font=F_HEAD,
             bg=PALETTE["bg"], fg=PALETTE["text"]
             ).pack(side=tk.LEFT)
    tk.Frame(title_row, bg=PALETTE["border"], height=1
             ).pack(side=tk.LEFT, fill=tk.X, expand=True,
                    padx=(12, 0), pady=6)
    # 카드
    card = tk.Frame(wrap, bg=PALETTE["card"],
                    highlightbackground=PALETTE["border"],
                    highlightthickness=1)
    card.pack(fill=tk.X)
    return card


def _make_section_header_in(wrap: tk.Frame, title: str) -> tk.Frame:
    """
    기존 wrap 프레임에 헤더+카드를 추가 (wrap 자체는 외부에서 pack)
    반환값: 카드 Frame
    """
    title_row = tk.Frame(wrap, bg=PALETTE["bg"])
    title_row.pack(fill=tk.X, pady=(0, 4))
    tk.Frame(title_row, bg=PALETTE["primary"], width=4
             ).pack(side=tk.LEFT, fill=tk.Y)
    tk.Label(title_row, text=f"  {title}",
             font=F_HEAD,
             bg=PALETTE["bg"], fg=PALETTE["text"]
             ).pack(side=tk.LEFT)
    tk.Frame(title_row, bg=PALETTE["border"], height=1
             ).pack(side=tk.LEFT, fill=tk.X, expand=True,
                    padx=(12, 0), pady=6)
    card = tk.Frame(wrap, bg=PALETTE["card"],
                    highlightbackground=PALETTE["border"],
                    highlightthickness=1)
    card.pack(fill=tk.X)
    return card


# ============================================================
# Block 2-A : TemplateTab — 작업 템플릿 관리
# ============================================================

class TemplateTab(tk.Frame):
    """
    작업 템플릿 = 플랫폼 + 작업유형 + 대상CSV + 메시지 + 이미지 + 좌표 + 스케줄 설정
    한 번 만들어두면 작업 관리에서 선택 후 스케줄만 설정하면 됨
    """
    def __init__(self, master, app: "App"):
        super().__init__(master, bg=PALETTE["bg"])
        self.app = app
        self._templates: list[dict] = []   # 로드된 템플릿 목록
        self._sel_idx:   int        = -1   # 현재 선택 인덱스

        # 편집 패널 위젯 추적용
        self._coord_rows:  list[dict] = []  # 좌표 행 위젯 목록
        self._ocr_frame:   tk.Frame | None = None
        self._img_frame:   tk.Frame | None = None

        self._build_ui()
        self._load_templates()

    # ── 전체 UI ─────────────────────────────────────────────
    def _build_ui(self):
        # ── 탭 헤더 바 ───────────────────────────────────────
        hdr = tk.Frame(self, bg=PALETTE["bg"])
        hdr.pack(fill=tk.X, pady=(0, 12))

        # 제목 영역
        title_f = tk.Frame(hdr, bg=PALETTE["bg"])
        title_f.pack(side=tk.LEFT)
        tk.Label(title_f, text="🗂",
                 font=("Segoe UI Emoji", 16),
                 bg=PALETTE["bg"], fg=PALETTE["primary"]
                 ).pack(side=tk.LEFT)
        tk.Label(title_f, text="  작업 템플릿 관리",
                 font=F_TITLE,
                 bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        tk.Label(title_f,
                 text="  템플릿을 먼저 만들고 → 작업 관리에서 선택하세요",
                 font=F_SMALL,
                 bg=PALETTE["bg"], fg=PALETTE["muted"]
                 ).pack(side=tk.LEFT)

        # 도움말 버튼
        tk.Button(hdr, text="❓  도움말",
                  command=self._show_help,
                  bg=PALETTE["card"], fg=PALETTE["text2"],
                  relief=tk.FLAT, font=F_BTN_S,
                  highlightbackground=PALETTE["border"],
                  highlightthickness=1,
                  activebackground=PALETTE["hover"],
                  cursor="hand2", padx=10, pady=4
                  ).pack(side=tk.RIGHT)

        # 구분선
        tk.Frame(self, bg=PALETTE["border"], height=1
                 ).pack(fill=tk.X, pady=(0, 10))

        # ── 좌우 분할 ─────────────────────────────────────────
        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL,
                               bg=PALETTE["border2"], sashwidth=5,
                               sashrelief=tk.FLAT)
        paned.pack(fill=tk.BOTH, expand=True)

        # 왼쪽: 템플릿 목록
        left = tk.Frame(paned, bg=PALETTE["card"],
                        highlightbackground=PALETTE["border"],
                        highlightthickness=1)
        paned.add(left, minsize=180)
        self._build_list_panel(left)

        # 오른쪽: 편집 패널 (스크롤 가능)
        right = tk.Frame(paned, bg=PALETTE["bg"])
        paned.add(right, minsize=560)
        self._build_edit_panel(right)

    # ── 왼쪽: 템플릿 목록 패널 ──────────────────────────────
    def _build_list_panel(self, parent: tk.Frame):
        # ── 컬러 헤더 바 ──
        hdr_bar = tk.Frame(parent, bg=PALETTE["primary"])
        hdr_bar.pack(fill=tk.X)
        tk.Label(hdr_bar, text="  📄  템플릿 목록",
                 font=(_FF, 9, "bold"),
                 bg=PALETTE["primary"], fg="#FFFFFF"
                 ).pack(side=tk.LEFT, pady=9)
        # 템플릿 수 뱃지
        self._tmpl_count_lbl = tk.Label(hdr_bar, text="0",
                 font=(_FF, 8, "bold"),
                 bg="#1E40AF", fg="#BFDBFE",
                 padx=7, pady=2)
        self._tmpl_count_lbl.pack(side=tk.RIGHT, padx=8, pady=6)

        # 리스트박스 + 스크롤
        lf = tk.Frame(parent, bg=PALETTE["card"])
        lf.pack(fill=tk.BOTH, expand=True)

        sb = tk.Scrollbar(lf, orient=tk.VERTICAL)
        self._tmpl_lb = tk.Listbox(
            lf, yscrollcommand=sb.set,
            bg=PALETTE["card"], fg=PALETTE["text"],
            selectbackground=PALETTE["primary"],
            selectforeground="#FFFFFF",
            font=(_FF, 9),
            relief=tk.FLAT, bd=0, activestyle="none",
            highlightthickness=0,
        )
        sb.config(command=self._tmpl_lb.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self._tmpl_lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._tmpl_lb.bind("<<ListboxSelect>>", self._on_select)
        # 더블클릭 → 이름 필드로 포커스 이동 (편집 모드 강조)
        self._tmpl_lb.bind("<Double-Button-1>", self._on_dbl_click)

        # 구분선
        tk.Frame(parent, bg=PALETTE["border"], height=1).pack(fill=tk.X)

        # ── 버튼 영역 ──
        bf = tk.Frame(parent, bg=PALETTE["card"])
        bf.pack(fill=tk.X, padx=8, pady=8)
        btn_defs = [
            ("＋ 새 템플릿", self._add_template, PALETTE["primary"],  "#FFFFFF"),
            ("⧉ 복제",       self._dup_template, "#F1F5F9",           PALETTE["text2"]),
            ("✕ 삭제",       self._del_template, "#FEF2F2",           PALETTE["danger"]),
        ]
        for txt, cmd, bg, fg in btn_defs:
            b = tk.Button(bf, text=txt, command=cmd,
                      bg=bg, fg=fg,
                      relief=tk.FLAT, font=(_FF, 8, "bold"),
                      activebackground=_lighten(bg, 0.08),
                      activeforeground=fg,
                      cursor="hand2", padx=8, pady=5, bd=0,
                      )
            b.pack(side=tk.LEFT, padx=2)
            b.bind("<Enter>", lambda e, b=b, bg=bg: b.config(bg=_lighten(bg)))
            b.bind("<Leave>", lambda e, b=b, bg=bg: b.config(bg=bg))

    # ── 오른쪽: 편집 패널 (스크롤 컨테이너) ─────────────────
    def _build_edit_panel(self, parent: tk.Frame):
        # Canvas + Scrollbar 로 스크롤 가능하게
        canvas = tk.Canvas(parent, bg=PALETTE["bg"],
                           highlightthickness=0)
        vsb = tk.Scrollbar(parent, orient=tk.VERTICAL,
                           command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._edit_inner = tk.Frame(canvas, bg=PALETTE["bg"])
        self._edit_win   = canvas.create_window(
            (0, 0), window=self._edit_inner, anchor="nw")

        def _on_configure(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
        def _on_canvas_resize(e):
            canvas.itemconfig(self._edit_win, width=e.width)

        self._edit_inner.bind("<Configure>", _on_configure)
        canvas.bind("<Configure>",           _on_canvas_resize)
        canvas.bind("<MouseWheel>",
                    lambda e: canvas.yview_scroll(
                        int(-1*(e.delta/120)), "units"))

        # 편집 패널 내용은 _refresh_edit_panel() 에서 동적 생성
        self._edit_canvas = canvas
        self._refresh_edit_panel()
    # ── 편집 패널 동적 렌더링 ────────────────────────────────
    def _refresh_edit_panel(self):
        """선택된 템플릿 데이터로 편집 패널 전체를 다시 그림"""
        for w in self._edit_inner.winfo_children():
            w.destroy()
        self._coord_rows = []

        pad = {"padx": 16, "pady": (0, 10)}

        # ── 섹션 헬퍼 (개선판) ───────────────────────────────
        def section(title: str) -> tk.Frame:
            wrap = tk.Frame(self._edit_inner, bg=PALETTE["bg"])
            wrap.pack(fill=tk.X, **pad)
            # 섹션 제목 행 — 좌측 컬러 바 강조
            title_row = tk.Frame(wrap, bg=PALETTE["bg"])
            title_row.pack(fill=tk.X, pady=(0, 4))
            # 4px 컬러 바
            tk.Frame(title_row, bg=PALETTE["primary"], width=4
                     ).pack(side=tk.LEFT, fill=tk.Y)
            tk.Label(title_row, text=f"  {title}",
                     font=F_HEAD,
                     bg=PALETTE["bg"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT)
            tk.Frame(title_row, bg=PALETTE["border"], height=1
                     ).pack(side=tk.LEFT, fill=tk.X, expand=True,
                            padx=(12, 0), pady=6)
            # 카드 영역
            card = tk.Frame(wrap, bg=PALETTE["card"],
                            highlightbackground=PALETTE["border"],
                            highlightthickness=1)
            card.pack(fill=tk.X)
            return card

        def row(parent, label: str, widget_fn):
            r = tk.Frame(parent, bg=PALETTE["card"])
            r.pack(fill=tk.X, padx=0, pady=0)
            # 구분선
            tk.Frame(r, bg=PALETTE["border"], height=1
                     ).pack(fill=tk.X)
            inner = tk.Frame(r, bg=PALETTE["card"])
            inner.pack(fill=tk.X, padx=14, pady=7)
            lbl = tk.Label(inner, text=label, width=16, anchor=tk.W,
                     font=F_LABEL,
                     bg=PALETTE["card"], fg=PALETTE["text2"]
                     )
            lbl.pack(side=tk.LEFT)
            widget_fn(inner)
            return inner

        # ════════════════════════════════════════════════════
        # 섹션 1 : 기본 정보
        # ════════════════════════════════════════════════════
        s1 = section("📌 기본 정보")

        # 템플릿명
        self._name_var = tk.StringVar(
            value=self._cur("name", "새 템플릿"))
        def _name_w(p):
            e = tk.Entry(p, textvariable=self._name_var,
                     bg=PALETTE["card2"], fg=PALETTE["text"],
                     insertbackground=PALETTE["primary"],
                     relief=tk.FLAT, font=F_BODY,
                     highlightbackground=PALETTE["border"],
                     highlightthickness=1,
                     width=30)
            e.pack(side=tk.LEFT, ipady=3)
            self._name_entry = e   # 더블클릭 포커스용 참조
        row(s1, "템플릿명", _name_w)

        # ════════════════════════════════════════════════════
        # 섹션 2 : 플랫폼 선택
        # ════════════════════════════════════════════════════
        s2 = section("📱 플랫폼 선택")
        plat_row = tk.Frame(s2, bg=PALETTE["card"])
        plat_row.pack(fill=tk.X, padx=12, pady=10)

        self._platform_var = tk.StringVar(
            value=self._cur("platform", "kakao"))

        for pid, pinfo in PLATFORMS.items():
            is_sel = (self._platform_var.get() == pid)
            btn = tk.Button(
                plat_row,
                text=f"  {pinfo['name']}  ",
                font=F_BTN,
                bg=pinfo["color"] if is_sel else PALETTE["hover"],
                fg=pinfo["text"]  if is_sel else PALETTE["text2"],
                relief=tk.FLAT, cursor="hand2",
                padx=22, pady=9,
                bd=0,
                activebackground=_lighten(pinfo["color"], 0.1),
                activeforeground=pinfo["text"],
            )
            btn.pack(side=tk.LEFT, padx=(0, 10))
            btn.bind("<Button-1>",
                     lambda e, p=pid: self._on_platform_change(p))
            setattr(self, f"_plat_btn_{pid}", btn)

        # ════════════════════════════════════════════════════
        # 섹션 3 : 작업 유형 선택 (플랫폼에 따라 동적)
        # ════════════════════════════════════════════════════
        s3 = section("⚙️ 작업 유형")
        self._wtype_frame = tk.Frame(s3, bg=PALETTE["card"])
        self._wtype_frame.pack(fill=tk.X, padx=12, pady=10)
        self._wtype_var = tk.StringVar(
            value=self._cur("workflow", "kakao_friend"))
        self._render_wtype_buttons()

        # ════════════════════════════════════════════════════
        # 섹션 3-A : 대상 목록 CSV
        # ════════════════════════════════════════════════════
        self._target_section_wrap = tk.Frame(
            self._edit_inner, bg=PALETTE["bg"])
        self._target_section_wrap.pack(fill=tk.X, **pad)
        self._render_target_section()

        # ════════════════════════════════════════════════════
        # 섹션 3-B : 메시지 (needs_message 인 경우만 표시)
        # ════════════════════════════════════════════════════
        self._msg_section_wrap = tk.Frame(
            self._edit_inner, bg=PALETTE["bg"])
        self._msg_section_wrap.pack(fill=tk.X, **pad)
        self._render_message_section()

        # ════════════════════════════════════════════════════
        # 섹션 4 : 이미지 첨부 (needs_image 인 경우만 표시)
        # ════════════════════════════════════════════════════
        self._img_section_wrap = tk.Frame(
            self._edit_inner, bg=PALETTE["bg"])
        self._img_section_wrap.pack(fill=tk.X, **pad)
        self._render_image_section()

        # ════════════════════════════════════════════════════
        # 섹션 5 : 좌표 설정
        # ════════════════════════════════════════════════════
        self._coord_section_wrap = tk.Frame(
            self._edit_inner, bg=PALETTE["bg"])
        self._coord_section_wrap.pack(fill=tk.X, **pad)
        self._render_coord_section()

        # ════════════════════════════════════════════════════
        # 섹션 5-B : 타이밍 설정 (카카오 메시지/오픈채팅 전용)
        # ════════════════════════════════════════════════════
        self._timing_section_wrap = tk.Frame(
            self._edit_inner, bg=PALETTE["bg"])
        self._timing_section_wrap.pack(fill=tk.X, **pad)
        self._render_timing_section()

        # ════════════════════════════════════════════════════
        # 섹션 5-C : 그리드 좌표 자동 계산 (카카오 오픈채팅 전용)
        # ════════════════════════════════════════════════════
        self._grid_section_wrap = tk.Frame(
            self._edit_inner, bg=PALETTE["bg"])
        self._grid_section_wrap.pack(fill=tk.X, **pad)
        self._render_grid_section()

        # ════════════════════════════════════════════════════
        # 섹션 5-D : 전송·닫기 방식 (카카오 메시지/오픈채팅 전용)
        # ════════════════════════════════════════════════════
        self._sc_section_wrap = tk.Frame(
            self._edit_inner, bg=PALETTE["bg"])
        self._sc_section_wrap.pack(fill=tk.X, **pad)
        self._render_send_close_section()

        # ════════════════════════════════════════════════════
        # 섹션 6 : OCR 설정 (친구추가일 때만 표시)
        # ════════════════════════════════════════════════════
        self._ocr_section_wrap = tk.Frame(
            self._edit_inner, bg=PALETTE["bg"])
        self._ocr_section_wrap.pack(fill=tk.X, **pad)
        self._render_friend_option_section()

        # ════════════════════════════════════════════════════
        # 저장 버튼 영역
        # ════════════════════════════════════════════════════
        save_wrap = tk.Frame(self._edit_inner, bg=PALETTE["border"],
                             highlightthickness=0)
        save_wrap.pack(fill=tk.X, padx=16, pady=(8, 20))
        save_inner = tk.Frame(save_wrap, bg=PALETTE["card"],
                              highlightbackground=PALETTE["border"],
                              highlightthickness=1)
        save_inner.pack(fill=tk.X)
        save_row = tk.Frame(save_inner, bg=PALETTE["card"])
        save_row.pack(fill=tk.X, padx=16, pady=12)

        save_btn = tk.Button(save_row, text="💾  템플릿 저장",
                  command=self._save_template,
                  bg=PALETTE["primary"], fg="#FFFFFF",
                  relief=tk.FLAT,
                  font=(_FF, 10, "bold"),
                  activebackground=PALETTE["primary2"],
                  cursor="hand2", padx=24, pady=9
                  )
        save_btn.pack(side=tk.LEFT)
        save_btn.bind("<Enter>", lambda e: save_btn.config(bg=PALETTE["primary2"]))
        save_btn.bind("<Leave>", lambda e: save_btn.config(bg=PALETTE["primary"]))

        tk.Label(save_row,
                 text="  변경 사항을 저장하면 작업 관리에 즉시 반영됩니다",
                 font=F_SMALL, fg=PALETTE["muted"],
                 bg=PALETTE["card"]).pack(side=tk.LEFT, padx=(12, 0))

    # ── 플랫폼 버튼 스타일 갱신 ─────────────────────────────
    def _on_platform_change(self, pid: str):
        self._platform_var.set(pid)
        for p, pinfo in PLATFORMS.items():
            btn = getattr(self, f"_plat_btn_{p}", None)
            if btn:
                sel = (p == pid)
                btn.config(
                    bg=pinfo["color"] if sel else PALETTE["card"],
                    fg=pinfo["text"]  if sel else PALETTE["text2"],
                )
        # 작업유형 목록 갱신
        wf_list = [k for k,v in PLATFORM_WORKFLOWS.items()
                   if v["platform"] == pid]
        if wf_list:
            self._wtype_var.set(wf_list[0])
        self._render_wtype_buttons()
        self._render_target_section()       # ← 대상CSV 재렌더
        self._render_message_section()      # ← 메시지 재렌더
        self._render_image_section()
        self._render_coord_section()
        self._render_timing_section()       # ← 타이밍 재렌더
        self._render_grid_section()         # ← 그리드 재렌더
        self._render_send_close_section()   # ← 전송·닫기 방식 재렌더
        self._render_friend_option_section()

    # ── 작업 유형 버튼 렌더링 ───────────────────────────────
    def _render_wtype_buttons(self):
        for w in self._wtype_frame.winfo_children():
            w.destroy()
        pid      = self._platform_var.get()
        pinfo    = PLATFORMS[pid]
        cur_wf   = self._wtype_var.get()
        wf_items = [(k, v) for k,v in PLATFORM_WORKFLOWS.items()
                    if v["platform"] == pid]

        for wk, wv in wf_items:
            is_sel = (wk == cur_wf)
            btn = tk.Button(
                self._wtype_frame,
                text=wv["name"],
                font=F_BTN if is_sel else F_LABEL,
                bg=pinfo["color"] if is_sel else PALETTE["hover"],
                fg=pinfo["text"]  if is_sel else PALETTE["text2"],
                relief=tk.FLAT, cursor="hand2",
                padx=14, pady=7, bd=0,
                activebackground=_lighten(
                    pinfo["color"] if is_sel else PALETTE["hover"], 0.05),
                activeforeground=pinfo["text"] if is_sel else PALETTE["text"],
            )
            btn.pack(side=tk.LEFT, padx=(0, 6), pady=4)
            btn.bind("<Button-1>",
                     lambda e, k=wk: self._on_wtype_change(k))

    # ── 작업 유형 변경 ───────────────────────────────────────
    def _on_wtype_change(self, wk: str):
        self._wtype_var.set(wk)
        self._render_wtype_buttons()
        self._render_target_section()       # ← 대상CSV 재렌더
        self._render_message_section()      # ← 메시지 재렌더
        self._render_image_section()
        self._render_coord_section()
        self._render_timing_section()       # ← 타이밍 재렌더
        self._render_grid_section()         # ← 그리드 재렌더
        self._render_send_close_section()   # ← 전송·닫기 방식 재렌더
        self._render_friend_option_section()

    # ── 현재 편집 중인 값 가져오기 헬퍼 ────────────────────
    def _cur(self, key: str, default: Any = "") -> Any:
        if self._sel_idx >= 0 and self._sel_idx < len(self._templates):
            return self._templates[self._sel_idx].get(key, default)
        return default
    # ── 섹션 4 : 이미지 첨부 렌더링 ────────────────────────
    # ── 대상 CSV 섹션 ────────────────────────────────────────
    def _render_target_section(self):
        """대상 목록 — CSV 파일 or 직접 입력 (워크플로우별 분기)"""
        for w in self._target_section_wrap.winfo_children():
            w.destroy()

        wrap = self._target_section_wrap
        wk   = self._wtype_var.get()

        # ★ 오픈채팅/가망뿌리기: 대상 목록 불필요 (그리드 자동계산으로 채팅방 순회)
        if wk == "kakao_openchat":
            return

        # 직접 입력을 지원하는 워크플로우 & 힌트 텍스트
        DIRECT_SUPPORT = {
            "kakao_friend":    ("카카오 ID",     "한 줄에 카카오ID 1개씩 입력  예) honggildong"),
            "telegram_join":   ("텔레그램 링크", "한 줄에 링크 1개씩 입력  예) https://t.me/channel_a"),
            "telegram_message":("텔레그램 링크","한 줄에 링크 1개씩 입력  예) https://t.me/channel_a"),
        }
        supports_direct = wk in DIRECT_SUPPORT
        direct_label, direct_hint = DIRECT_SUPPORT.get(wk, ("직접 입력", ""))

        tk.Label(wrap, text="👤 대상 목록",
                 font=F_HEAD,
                 bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(anchor=tk.W, pady=(0, 6))
        card = tk.Frame(wrap, bg=PALETTE["card"],
                        highlightbackground=PALETTE["border"],
                        highlightthickness=1)
        card.pack(fill=tk.X)

        # ── 모드 선택 라디오 (직접입력 지원 워크플로우만 표시) ──
        if supports_direct:
            saved_mode = self._cur("target_mode", "csv")
            self._tgt_mode_var = tk.StringVar(value=saved_mode)

            mode_row = tk.Frame(card, bg=PALETTE["card"])
            mode_row.pack(fill=tk.X, padx=12, pady=(10, 4))
            tk.Label(mode_row, text="입력 방식",
                     width=16, anchor=tk.W,
                     font=F_LABEL,
                     bg=PALETTE["card"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT)
            tk.Radiobutton(mode_row, text="📂 CSV 파일",
                           variable=self._tgt_mode_var, value="csv",
                           bg=PALETTE["card"], fg=PALETTE["text"],
                           selectcolor=PALETTE["active"],
                           activebackground=PALETTE["card"],
                           font=F_LABEL,
                           command=self._on_tgt_mode_change
                           ).pack(side=tk.LEFT, padx=(0, 16))
            tk.Radiobutton(mode_row, text=f"✏️ 직접 입력  ({direct_label})",
                           variable=self._tgt_mode_var, value="direct",
                           bg=PALETTE["card"], fg=PALETTE["text"],
                           selectcolor=PALETTE["active"],
                           activebackground=PALETTE["card"],
                           font=F_LABEL,
                           command=self._on_tgt_mode_change
                           ).pack(side=tk.LEFT)

            # 구분선
            tk.Frame(card, bg=PALETTE["border"], height=1
                     ).pack(fill=tk.X, padx=12, pady=(4, 0))

        # ── CSV 파일 선택 영역 ────────────────────────────────
        self._tgt_csv_frame = tk.Frame(card, bg=PALETTE["card"])
        self._tgt_csv_frame.pack(fill=tk.X, padx=12, pady=8)

        r = self._tgt_csv_frame
        tk.Label(r, text="CSV 파일", width=16, anchor=tk.W,
                 font=F_LABEL,
                 bg=PALETTE["card"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        self._tgt_path_var = tk.StringVar(
            value=self._cur("target_file", ""))
        tk.Entry(r, textvariable=self._tgt_path_var,
                 bg=PALETTE["card2"], fg=PALETTE["text"],
                 insertbackground=PALETTE["text"],
                 relief=tk.FLAT, font=F_LABEL,
                 width=26
                 ).pack(side=tk.LEFT, padx=(0, 6))
        tk.Button(r, text="📂 찾기",
                  command=self._browse_target_csv,
                  bg=PALETTE["hover"], fg=PALETTE["text"],
                  relief=tk.FLAT, cursor="hand2",
                  font=F_SMALL, padx=6
                  ).pack(side=tk.LEFT)
        self._tgt_sample_btn = tk.Button(r, text="📥 예시 파일",
                  command=self._download_sample_csv,
                  bg=PALETTE["selected"], fg=PALETTE["primary"],
                  relief=tk.FLAT, cursor="hand2",
                  font=F_SMALL, padx=6)
        self._tgt_sample_btn.pack(side=tk.LEFT, padx=(4, 0))
        self._tgt_count_lbl = tk.Label(
            r, text="",
            font=F_SMALL,
            bg=PALETTE["card"], fg=PALETTE["text"])
        self._tgt_count_lbl.pack(side=tk.LEFT, padx=(8, 0))
        self._update_tgt_count()

        # ── 직접 입력 영역 ────────────────────────────────────
        self._tgt_direct_frame = tk.Frame(card, bg=PALETTE["card"])
        self._tgt_direct_frame.pack(fill=tk.X, padx=12, pady=(4, 8))

        di_top = tk.Frame(self._tgt_direct_frame, bg=PALETTE["card"])
        di_top.pack(fill=tk.X)
        tk.Label(di_top, text=direct_label,
                 width=16, anchor=tk.W,
                 font=F_LABEL,
                 bg=PALETTE["card"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        self._tgt_direct_count_lbl = tk.Label(
            di_top, text="",
            font=F_SMALL,
            bg=PALETTE["card"], fg=PALETTE["success_text"])
        self._tgt_direct_count_lbl.pack(side=tk.LEFT)

        # Text 위젯 + 스크롤바
        txt_frame = tk.Frame(self._tgt_direct_frame, bg=PALETTE["card"])
        txt_frame.pack(fill=tk.X, pady=(4, 0))
        sb = tk.Scrollbar(txt_frame, orient=tk.VERTICAL)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self._tgt_direct_text = tk.Text(
            txt_frame,
            height=7,
            bg=PALETTE["bg"], fg=PALETTE["text"],
            insertbackground=PALETTE["text"],
            relief=tk.FLAT, font=F_MONO,
            wrap=tk.NONE,
            yscrollcommand=sb.set)
        self._tgt_direct_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
        sb.config(command=self._tgt_direct_text.yview)

        # ── 중복 제거 버튼 ────────────────────────────────
        dedup_row = tk.Frame(self._tgt_direct_frame, bg=PALETTE["card"])
        dedup_row.pack(fill=tk.X, pady=(4, 0))
        tk.Button(
            dedup_row,
            text="🔁 중복 제거",
            command=self._dedup_direct_input,
            bg=PALETTE["hover"], fg=PALETTE["text"],
            relief=tk.FLAT, cursor="hand2",
            font=F_SMALL, padx=8, pady=3
        ).pack(side=tk.LEFT)
        self._tgt_dedup_lbl = tk.Label(
            dedup_row, text="",
            font=F_SMALL,
            bg=PALETTE["card"], fg=PALETTE["success_text"])
        self._tgt_dedup_lbl.pack(side=tk.LEFT, padx=(8, 0))

        # 저장된 직접입력 내용 복원
        saved_direct = self._cur("target_direct", "")
        if saved_direct:
            self._tgt_direct_text.insert("1.0", saved_direct)

        # 줄 수 카운트 바인딩
        self._tgt_direct_text.bind(
            "<KeyRelease>", lambda e: self._update_direct_count())
        self._tgt_direct_text.bind(
            "<ButtonRelease>", lambda e: self._update_direct_count())
        self._update_direct_count()

        # 힌트
        if direct_hint:
            tk.Label(self._tgt_direct_frame,
                     text=f"💡 {direct_hint}",
                     font=F_SMALL,
                     bg=PALETTE["card"], fg=PALETTE["text"],
                     justify=tk.LEFT
                     ).pack(anchor=tk.W, pady=(4, 0))

        # CSV 컬럼 안내
        hint_row = tk.Frame(card, bg=PALETTE["card"])
        hint_row.pack(fill=tk.X, padx=12, pady=(0, 8))
        tk.Label(hint_row,
                 text="💡 필수 컬럼: 카카오아이디 (친구추가) / 카카오ID (메시지) / 텔레그램링크 (가입)",
                 font=F_SMALL,
                 bg=PALETTE["card"], fg=PALETTE["text"]
                 ).pack(anchor=tk.W)

        # 초기 표시 상태 적용
        if supports_direct:
            self._on_tgt_mode_change()
        else:
            # 직접입력 미지원: 직접입력 영역 숨김
            self._tgt_direct_frame.pack_forget()

    def _on_tgt_mode_change(self):
        """CSV / 직접입력 라디오 전환"""
        try:
            mode = self._tgt_mode_var.get()
        except AttributeError:
            return
        if mode == "csv":
            self._tgt_csv_frame.pack(fill=tk.X, padx=12, pady=8)
            self._tgt_direct_frame.pack_forget()
            # CSV 모드: 예시 파일 버튼 표시
            if hasattr(self, "_tgt_sample_btn"):
                self._tgt_sample_btn.pack(side=tk.LEFT, padx=(4, 0))
        else:
            self._tgt_csv_frame.pack_forget()
            self._tgt_direct_frame.pack(fill=tk.X, padx=12, pady=(4, 8))
            # 직접입력 모드: 예시 파일 버튼 숨김
            if hasattr(self, "_tgt_sample_btn"):
                self._tgt_sample_btn.pack_forget()

    def _update_direct_count(self):
        """직접입력 텍스트 줄 수 업데이트"""
        try:
            raw = self._tgt_direct_text.get("1.0", tk.END)
            lines = [l.strip() for l in raw.splitlines() if l.strip()]
            cnt = len(lines)
            self._tgt_direct_count_lbl.config(
                text=f"  총 {cnt:,}개" if cnt else "")
        except Exception:
            pass

    def _dedup_direct_input(self):
        """직접 입력 텍스트에서 중복 줄 제거 (순서 유지)"""
        try:
            raw   = self._tgt_direct_text.get("1.0", tk.END)
            lines = [l.strip() for l in raw.splitlines() if l.strip()]
            seen  = set()
            unique = []
            dup_cnt = 0
            for line in lines:
                key = line.lower()          # 대소문자 무관 중복 판별
                if key not in seen:
                    seen.add(key)
                    unique.append(line)
                else:
                    dup_cnt += 1
            self._tgt_direct_text.delete("1.0", tk.END)
            self._tgt_direct_text.insert("1.0", "\n".join(unique))
            self._update_direct_count()
            if hasattr(self, "_tgt_dedup_lbl"):
                if dup_cnt:
                    self._tgt_dedup_lbl.config(
                        text=f"  ✅ 중복 {dup_cnt}개 제거 → {len(unique)}개 남음")
                else:
                    self._tgt_dedup_lbl.config(text="  ✅ 중복 없음")
        except Exception:
            pass

    def _browse_target_csv(self):
        from tkinter import filedialog
        path = filedialog.askopenfilename(
            title="대상 CSV 파일 선택",
            filetypes=[("CSV", "*.csv"), ("전체", "*.*")])
        if path:
            self._tgt_path_var.set(path)
            self._update_tgt_count()

    def _download_sample_csv(self):
        """현재 워크플로우에 맞는 예시 CSV 파일 저장"""
        from tkinter import filedialog, messagebox
        import csv as _csv_mod

        wk   = self._cur("workflow", "kakao_friend")
        data = SAMPLE_CSV_DATA.get(wk)
        if not data:
            messagebox.showwarning("예시 파일", "이 작업 유형은 예시 파일이 없습니다.")
            return

        save_path = filedialog.asksaveasfilename(
            title="예시 CSV 저장",
            initialfile=data["filename"],
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv"), ("전체", "*.*")],
        )
        if not save_path:
            return

        try:
            headers = [h.strip() for h in data["header"].split(",")]
            with open(save_path, "w", newline="", encoding="utf-8-sig") as f:
                writer = _csv_mod.writer(f)
                writer.writerow(headers)
                for row in data["rows"]:
                    writer.writerow(list(row))
            # 힌트 텍스트 업데이트
            hint_text = f"✅ 저장됨: {Path(save_path).name}   {data['hint']}"
            # hint 라벨이 있으면 업데이트, 없으면 messagebox
            try:
                self._csv_hint_lbl.config(text=hint_text)
            except Exception:
                pass
            # 정상 완료 → 상태바로 표시 (팝업 없음)
            self.app._set_status(
                f"✅ 예시 파일 저장: {Path(save_path).name}")
        except Exception as e:
            messagebox.showerror("저장 실패", str(e))

    def _update_tgt_count(self):
        try:
            path = self._tgt_path_var.get().strip()
            if not path or not Path(path).exists():
                self._tgt_count_lbl.config(text="")
                return
            import csv as _csv2
            with open(path, encoding="utf-8-sig") as f:
                count = sum(1 for _ in _csv2.reader(f)) - 1
            self._tgt_count_lbl.config(
                text=f"총 {max(count, 0):,}명")
        except Exception:
            try:
                self._tgt_count_lbl.config(text="읽기 실패")
            except Exception:
                pass

    # ── 메시지 섹션 ──────────────────────────────────────────
    def _render_message_section(self):
        """메시지 내용 입력 (needs_message 인 경우만)"""
        for w in self._msg_section_wrap.winfo_children():
            w.destroy()

        wk   = self._wtype_var.get()
        wdef = PLATFORM_WORKFLOWS.get(wk, {})
        if not wdef.get("needs_message", False):
            return  # 메시지 불필요 → 숨김

        wrap = self._msg_section_wrap
        card = _make_section_header_in(wrap, "💬 메시지")

        msg_frame = tk.Frame(card, bg=PALETTE["card"])
        msg_frame.pack(fill=tk.X, padx=12, pady=8)
        tk.Label(msg_frame, text="메시지 내용",
                 width=16, anchor=tk.W,
                 font=F_LABEL,
                 bg=PALETTE["card"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT, anchor=tk.N, pady=2)

        txt_wrap = tk.Frame(msg_frame, bg=PALETTE["card"])
        txt_wrap.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._msg_text = tk.Text(
            txt_wrap, height=5, width=36,
            bg=PALETTE["bg"], fg=PALETTE["text"],
            insertbackground=PALETTE["text"],
            relief=tk.FLAT, font=F_LABEL,
            wrap=tk.WORD)
        self._msg_text.pack(side=tk.LEFT,
                            fill=tk.BOTH, expand=True)
        msg_sb = tk.Scrollbar(txt_wrap,
                              command=self._msg_text.yview)
        self._msg_text.configure(yscrollcommand=msg_sb.set)
        msg_sb.pack(side=tk.RIGHT, fill=tk.Y)

        saved = self._cur("message", "")
        if saved:
            self._msg_text.insert("1.0", saved)

        # 변수 토큰 버튼
        tok_row = tk.Frame(card, bg=PALETTE["card"])
        tok_row.pack(fill=tk.X, padx=12, pady=(0, 8))
        tk.Label(tok_row, text="변수 삽입:",
                 font=F_SMALL,
                 bg=PALETTE["card"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT, padx=(0, 6))
        for tok in ["{이름}", "{번호}", "{번호뒤4}",
                    "{랜덤숫자3}", "{랜덤영숫자3}"]:
            tk.Button(tok_row, text=tok,
                      font=F_MONO_S,
                      bg=PALETTE["hover"], fg=PALETTE["text"],
                      relief=tk.FLAT, cursor="hand2",
                      padx=4, pady=1,
                      command=lambda t=tok:
                          self._msg_text.insert(tk.INSERT, t)
                      ).pack(side=tk.LEFT, padx=2)

    # ── 이미지 첨부 섹션 ─────────────────────────────────────
    def _render_image_section(self):
        for w in self._img_section_wrap.winfo_children():
            w.destroy()

        wk   = self._wtype_var.get()
        wdef = PLATFORM_WORKFLOWS.get(wk, {})
        if not wdef.get("needs_image", False):
            return  # 이미지 불필요한 작업유형은 숨김

        card = _make_section_header_in(self._img_section_wrap, "🖼️ 이미지 첨부 설정")

        # ── 이미지 사용 여부 토글 ──────────────────────────
        img_row = tk.Frame(card, bg=PALETTE["card"])
        img_row.pack(fill=tk.X, padx=12, pady=8)
        tk.Label(img_row, text="이미지 첨부",
                 width=16, anchor=tk.W,
                 font=F_LABEL,
                 bg=PALETTE["card"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        _use_init = self._cur("use_image", False)
        self._use_image_var = tk.BooleanVar(value=_use_init)

        def _set_use_img(val, _btn_on=None, _btn_off=None):
            self._use_image_var.set(val)
            # 버튼 강조 색상 갱신
            try:
                if val:
                    _btn_on.config(
                        bg=PALETTE["primary"], fg="#FFFFFF",
                        relief=tk.FLAT)
                    _btn_off.config(
                        bg=PALETTE["hover"], fg=PALETTE["text2"],
                        relief=tk.FLAT)
                else:
                    _btn_on.config(
                        bg=PALETTE["hover"], fg=PALETTE["text2"],
                        relief=tk.FLAT)
                    _btn_off.config(
                        bg=PALETTE["primary"], fg="#FFFFFF",
                        relief=tk.FLAT)
            except Exception:
                pass
            self._toggle_image_path()

        _on_bg  = PALETTE["primary"] if _use_init else PALETTE["hover"]
        _on_fg  = "#FFFFFF"           if _use_init else PALETTE["text2"]
        _off_bg = PALETTE["hover"]    if _use_init else PALETTE["primary"]
        _off_fg = PALETTE["text2"]    if _use_init else "#FFFFFF"

        self._img_on_btn = tk.Button(
            img_row, text="✅ 사용함",
            bg=_on_bg, fg=_on_fg,
            relief=tk.FLAT, font=F_LABEL,
            cursor="hand2", padx=10, pady=2)
        self._img_on_btn.pack(side=tk.LEFT, padx=(0, 4))

        self._img_off_btn = tk.Button(
            img_row, text="🚫 사용 안함",
            bg=_off_bg, fg=_off_fg,
            relief=tk.FLAT, font=F_LABEL,
            cursor="hand2", padx=10, pady=2)
        self._img_off_btn.pack(side=tk.LEFT)

        # command 는 버튼 생성 이후에 연결 (서로 참조)
        self._img_on_btn.config(
            command=lambda: _set_use_img(True,
                self._img_on_btn, self._img_off_btn))
        self._img_off_btn.config(
            command=lambda: _set_use_img(False,
                self._img_on_btn, self._img_off_btn))

        # ── 첨부 방식 선택 (파일경로 / 드래그앤드롭) ─────────
        self._img_mode_row = tk.Frame(card, bg=PALETTE["card"])
        self._img_mode_row.pack(fill=tk.X, padx=12, pady=(0, 6))
        tk.Label(self._img_mode_row, text="첨부 방식",
                 width=16, anchor=tk.W,
                 font=F_LABEL,
                 bg=PALETTE["card"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        # 텔레그램: none/clipboard/file
        # 카카오:   file/dragdrop
        _wk_now = self._wtype_var.get()
        _is_tg  = _wk_now in ("telegram_message", "telegram_join_and_message")
        # Telethon API 모드 여부: Telethon 설치 + 계정 존재 시 True
        _is_tg_api = (
            _is_tg
            and HAS_TELETHON
            and bool(load_json(TG_ACCOUNTS_PATH, []))
        )
        _img_mode_default = self._cur("image_mode", "none" if _is_tg else "file")
        self._img_mode_var = tk.StringVar(value=_img_mode_default)
        if _is_tg:
            # 텔레그램 전용: 드래그앤드롭 없음
            _img_mode_opts = [("none",      "🚫 첨부 없음"),
                              ("clipboard", "📋 클립보드"),
                              ("file",      "📁 파일 경로")]
        else:
            # 카카오 전용: 클립보드 없음
            _img_mode_opts = [("file",    "📁 파일 경로"),
                              ("dragdrop","🖱️ 드래그 앤 드롭")]

        # ── 버튼형 탭 (Radiobutton 대신 토글 버튼 스타일) ──────────────
        _img_mode_btns = {}

        def _select_img_mode(val):
            self._img_mode_var.set(val)
            for v, btn in _img_mode_btns.items():
                if v == val:
                    btn.config(bg=PALETTE["primary"], fg="#FFFFFF",
                               relief=tk.FLAT)
                else:
                    btn.config(bg=PALETTE["bg"], fg=PALETTE["text"],
                               relief=tk.FLAT)
            self._toggle_image_path()

        for val, lbl in _img_mode_opts:
            btn = tk.Button(
                self._img_mode_row, text=lbl,
                font=F_BTN_S,
                relief=tk.FLAT,
                cursor="hand2",
                padx=10, pady=4,
                command=lambda v=val: _select_img_mode(v),
            )
            btn.pack(side=tk.LEFT, padx=(0, 4))
            _img_mode_btns[val] = btn

        # 초기 선택 상태 반영
        _select_img_mode(_img_mode_default)

        # ── 텔레그램 전용: 파일첨부 버튼 좌표 / Telethon API 안내 ──────────────────
        # · Telethon API 모드(계정 있음): 좌표 불필요 → 한 줄 인라인 안내만 표시
        # · pyautogui 폴백 모드: 좌표 입력 필요 → 좌표 행 표시
        if _is_tg:
            if _is_tg_api:
                # ── Telethon API 모드: 파일은 API로 직접 전송 → 좌표 불필요 ──
                # (좌표 섹션에도 이미 API 배너가 있으므로 여기선 간결하게 한 줄만)
                _api_note = tk.Frame(card, bg=PALETTE["card"])
                _api_note.pack(fill=tk.X, padx=12, pady=(2, 8))
                tk.Label(_api_note,
                         text="ℹ️  API 모드: 파일 경로 선택 시 첨부버튼/파일명 좌표 입력 불필요",
                         font=F_SMALL, bg=PALETTE["card"],
                         fg="#065F46", padx=0, pady=4
                         ).pack(anchor="w")
                # _toggle_image_path 에서 참조하므로 더미 Frame 생성 (pack 안 함)
                self._tg_attach_row   = tk.Frame(card, bg=PALETTE["card"])
                self._tg_filename_row = tk.Frame(card, bg=PALETTE["card"])
                self._tg_attach_x   = tk.StringVar(value="0")
                self._tg_attach_y   = tk.StringVar(value="0")
                self._tg_fname_x    = tk.StringVar(value="0")
                self._tg_fname_y    = tk.StringVar(value="0")
                self._tg_attach_disp = tk.Label(self._tg_attach_row)
                self._tg_fname_disp  = tk.Label(self._tg_filename_row)
            else:
                # ── pyautogui 폴백 모드: 좌표 입력 필요 ──
                self._tg_attach_row = tk.Frame(card, bg=PALETTE["card"])
                # 초기에는 숨김 (pack 안 함) — _toggle_image_path 에서 표시
                tk.Label(self._tg_attach_row, text="첨부버튼 좌표",
                         width=16, anchor=tk.W,
                         font=F_LABEL, bg=PALETTE["card"],
                         fg=PALETTE["accent"]).pack(side=tk.LEFT)
                self._tg_attach_x = tk.StringVar(
                    value=str(self._cur("tg_attach_btn_coord", {}).get("x", 0)))
                self._tg_attach_y = tk.StringVar(
                    value=str(self._cur("tg_attach_btn_coord", {}).get("y", 0)))
                for lbl_t, var in [("X:", self._tg_attach_x),
                                    ("Y:", self._tg_attach_y)]:
                    tk.Label(self._tg_attach_row, text=lbl_t, font=F_MONO_S,
                             bg=PALETTE["card"], fg=PALETTE["text"]
                             ).pack(side=tk.LEFT, padx=(4, 0))
                    tk.Entry(self._tg_attach_row, textvariable=var,
                             width=6, bg=PALETTE["card2"], fg=PALETTE["text"],
                             insertbackground=PALETTE["text"],
                             relief=tk.FLAT, font=F_MONO
                             ).pack(side=tk.LEFT)
                self._tg_attach_disp = tk.Label(self._tg_attach_row, text="",
                    font=F_MONO_S, bg=PALETTE["card"], fg=PALETTE["success_text"])
                self._tg_attach_disp.pack(side=tk.LEFT, padx=(6, 0))
                tk.Button(self._tg_attach_row, text="📸 캡처",
                          command=lambda: self._capture_point(
                              "tg_attach_btn_coord",
                              self._tg_attach_x, self._tg_attach_y,
                              self._tg_attach_disp),
                          bg=PALETTE["accent"], fg="#FFFFFF",
                          relief=tk.FLAT, font=F_SMALL,
                          cursor="hand2", padx=8, pady=3, bd=0
                          ).pack(side=tk.LEFT, padx=(8, 0))
                tk.Label(self._tg_attach_row,
                         text=" ← 파일경로 모드 시 필수 (pyautogui 모드)",
                         font=F_SMALL, bg=PALETTE["card"],
                         fg=PALETTE["warning_text"]
                         ).pack(side=tk.LEFT, padx=(4, 0))

                # ── 텔레그램 전용: 파일명 입력란 좌표 ──────────────
                self._tg_filename_row = tk.Frame(card, bg=PALETTE["card"])
                # 초기에는 숨김 (_toggle_image_path 에서 표시)
                tk.Label(self._tg_filename_row, text="파일명입력 좌표",
                         width=16, anchor=tk.W,
                         font=F_LABEL, bg=PALETTE["card"],
                         fg=PALETTE["accent"]).pack(side=tk.LEFT)
                self._tg_fname_x = tk.StringVar(
                    value=str(self._cur("tg_filename_input_coord", {}).get("x", 0)))
                self._tg_fname_y = tk.StringVar(
                    value=str(self._cur("tg_filename_input_coord", {}).get("y", 0)))
                for lbl_t, var in [("X:", self._tg_fname_x),
                                    ("Y:", self._tg_fname_y)]:
                    tk.Label(self._tg_filename_row, text=lbl_t, font=F_MONO_S,
                             bg=PALETTE["card"], fg=PALETTE["text"]
                             ).pack(side=tk.LEFT, padx=(4, 0))
                    tk.Entry(self._tg_filename_row, textvariable=var,
                             width=6, bg=PALETTE["card2"], fg=PALETTE["text"],
                             insertbackground=PALETTE["text"],
                             relief=tk.FLAT, font=F_MONO
                             ).pack(side=tk.LEFT)
                self._tg_fname_disp = tk.Label(self._tg_filename_row, text="",
                    font=F_MONO_S, bg=PALETTE["card"], fg=PALETTE["success_text"])
                self._tg_fname_disp.pack(side=tk.LEFT, padx=(6, 0))
                tk.Button(self._tg_filename_row, text="📸 캡처",
                          command=lambda: self._capture_point(
                              "tg_filename_input_coord",
                              self._tg_fname_x, self._tg_fname_y,
                              self._tg_fname_disp),
                          bg=PALETTE["accent"], fg="#FFFFFF",
                          relief=tk.FLAT, font=F_SMALL,
                          cursor="hand2", padx=8, pady=3, bd=0
                          ).pack(side=tk.LEFT, padx=(8, 0))
                tk.Label(self._tg_filename_row,
                         text=" ← 파일명 입력란 클릭 좌표 (pyautogui 모드)",
                         font=F_SMALL, bg=PALETTE["card"],
                         fg=PALETTE["warning_text"]
                         ).pack(side=tk.LEFT, padx=(4, 0))

        # ── 이미지 파일 경로 (파일경로 방식) ──────────────────
        self._img_path_row = tk.Frame(card, bg=PALETTE["card"])
        # pack 여부는 _toggle_image_path 가 결정 (초기 pack 제거)
        tk.Label(self._img_path_row, text="이미지 경로",
                 width=16, anchor=tk.W,
                 font=F_LABEL,
                 bg=PALETTE["card"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        self._img_path_var = tk.StringVar(
            value=self._cur("image_path", ""))
        tk.Entry(self._img_path_row,
                 textvariable=self._img_path_var,
                 bg=PALETTE["card2"], fg=PALETTE["text"],
                 insertbackground=PALETTE["text"],
                 relief=tk.FLAT, font=F_LABEL,
                 width=30).pack(side=tk.LEFT, padx=(0, 6))
        tk.Button(self._img_path_row, text="📂 찾기",
                  command=self._browse_image,
                  bg=PALETTE["card"], fg=PALETTE["text"],
                  relief=tk.FLAT, font=F_SMALL,
                  cursor="hand2", padx=6
                  ).pack(side=tk.LEFT)

        # ── 이미지 첨부 순서 (메시지 전 / 후) ──────────────────
        self._img_order_row = tk.Frame(card, bg=PALETTE["card"])
        # pack 여부는 _toggle_image_path 가 결정 (초기 pack 제거)
        order_row = self._img_order_row
        tk.Label(order_row, text="첨부 순서",
                 width=16, anchor=tk.W,
                 font=F_LABEL,
                 bg=PALETTE["card"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        self._img_order_var = tk.StringVar(
            value=self._cur("img_order", "before"))
        for val, lbl in [("before", "📎 메시지 전"),
                         ("after",  "📎 메시지 후")]:
            tk.Radiobutton(
                order_row, text=lbl,
                variable=self._img_order_var,
                value=val,
                bg=PALETTE["card"], fg=PALETTE["text"],
                selectcolor=PALETTE["active"],
                activebackground=PALETTE["card"],
                font=F_LABEL,
            ).pack(side=tk.LEFT, padx=(0, 20))

        # ── 이미지 소스 좌표 (Kakao 전용 — 텔레그램은 드래그앤드롭 없음) ──
        self._img_src_row = tk.Frame(card, bg=PALETTE["card"])
        if not _is_tg:
            self._img_src_row.pack(fill=tk.X, padx=12, pady=(0, 4))
        tk.Label(self._img_src_row, text="소스 좌표",
                 width=16, anchor=tk.W,
                 font=F_LABEL,
                 bg=PALETTE["card"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        self._img_src_x = tk.StringVar(value=str(
            self._cur("image_source_coord", {}).get("x", 0)))
        self._img_src_y = tk.StringVar(value=str(
            self._cur("image_source_coord", {}).get("y", 0)))
        for lbl_t, var in [("X:", self._img_src_x),
                           ("Y:", self._img_src_y)]:
            tk.Label(self._img_src_row, text=lbl_t,
                     font=F_MONO_S,
                     bg=PALETTE["card"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT, padx=(4, 0))
            tk.Entry(self._img_src_row, textvariable=var,
                     width=6, bg=PALETTE["card2"], fg=PALETTE["text"],
                     insertbackground=PALETTE["text"],
                     relief=tk.FLAT, font=F_MONO
                     ).pack(side=tk.LEFT)
        self._img_src_disp = tk.Label(self._img_src_row, text="",
            font=F_MONO_S, bg=PALETTE["card"],
            fg=PALETTE["success_text"])
        self._img_src_disp.pack(side=tk.LEFT, padx=(6, 0))
        tk.Button(self._img_src_row, text="📸 캡처",
                  command=lambda: self._capture_point(
                      "image_source_coord",
                      self._img_src_x, self._img_src_y,
                      self._img_src_disp),
                  bg=PALETTE["primary2"], fg="#FFFFFF",
                  relief=tk.FLAT, font=F_SMALL,
                  cursor="hand2", padx=8, pady=3, bd=0
                  ).pack(side=tk.LEFT, padx=(8, 0))

        # ── 이미지 드롭 좌표 (Kakao 전용 — 텔레그램은 드래그앤드롭 없음) ──
        self._img_drop_row = tk.Frame(card, bg=PALETTE["card"])
        if not _is_tg:
            self._img_drop_row.pack(fill=tk.X, padx=12, pady=(0, 4))
        tk.Label(self._img_drop_row, text="드롭 좌표",
                 width=16, anchor=tk.W,
                 font=F_LABEL,
                 bg=PALETTE["card"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        self._img_drop_x = tk.StringVar(value=str(
            self._cur("image_drop_coord", {}).get("x", 0)))
        self._img_drop_y = tk.StringVar(value=str(
            self._cur("image_drop_coord", {}).get("y", 0)))
        for lbl_t, var in [("X:", self._img_drop_x),
                           ("Y:", self._img_drop_y)]:
            tk.Label(self._img_drop_row, text=lbl_t,
                     font=F_MONO_S,
                     bg=PALETTE["card"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT, padx=(4, 0))
            tk.Entry(self._img_drop_row, textvariable=var,
                     width=6, bg=PALETTE["card2"], fg=PALETTE["text"],
                     insertbackground=PALETTE["text"],
                     relief=tk.FLAT, font=F_MONO
                     ).pack(side=tk.LEFT)
        self._img_drop_disp = tk.Label(self._img_drop_row, text="",
            font=F_MONO_S, bg=PALETTE["card"],
            fg=PALETTE["success_text"])
        self._img_drop_disp.pack(side=tk.LEFT, padx=(6, 0))
        tk.Button(self._img_drop_row, text="📸 캡처",
                  command=lambda: self._capture_point(
                      "image_drop_coord",
                      self._img_drop_x, self._img_drop_y,
                      self._img_drop_disp),
                  bg=PALETTE["primary2"], fg="#FFFFFF",
                  relief=tk.FLAT, font=F_SMALL,
                  cursor="hand2", padx=8, pady=3, bd=0
                  ).pack(side=tk.LEFT, padx=(8, 0))

        img_delays = self._cur("image_delays", {})

        # ── [드래그앤드롭] 딜레이 (Kakao 전용) ────────────────
        self._img_delay_dd_row = tk.Frame(card, bg=PALETTE["card"])
        # pack 여부는 _toggle_image_path 가 결정
        tk.Label(self._img_delay_dd_row, text="딜레이(s)",
                 width=14, anchor=tk.W,
                 font=F_LABEL, bg=PALETTE["card"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        self._img_d_click = tk.StringVar(
            value=str(img_delays.get("after_image_click", 0.5)))
        self._img_d_drag  = tk.StringVar(
            value=str(img_delays.get("after_drag_start", 0.2)))
        self._img_d_drop  = tk.StringVar(
            value=str(img_delays.get("after_drop", 0.3)))
        self._img_d_enter = tk.StringVar(
            value=str(img_delays.get("after_enter", 0.5)))
        for lbl_t, var in [
            ("클릭후",   self._img_d_click),
            ("드래그후", self._img_d_drag),
            ("드롭후",   self._img_d_drop),
            ("Enter후",  self._img_d_enter),
        ]:
            tk.Label(self._img_delay_dd_row, text=lbl_t,
                     font=F_SMALL, bg=PALETTE["card"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT, padx=(6, 2))
            tk.Entry(self._img_delay_dd_row, textvariable=var,
                     width=5, bg=PALETTE["card2"], fg=PALETTE["text"],
                     insertbackground=PALETTE["text"],
                     relief=tk.FLAT, font=F_MONO
                     ).pack(side=tk.LEFT)

        # ── [클립보드] 딜레이 ──────────────────────────────────
        self._img_delay_cb_row = tk.Frame(card, bg=PALETTE["card"])
        tk.Label(self._img_delay_cb_row, text="딜레이(s)",
                 width=14, anchor=tk.W,
                 font=F_LABEL, bg=PALETTE["card"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        self._img_d_cb_paste = tk.StringVar(
            value=str(img_delays.get("cb_after_paste", 0.5)))
        self._img_d_cb_send  = tk.StringVar(
            value=str(img_delays.get("cb_after_send",  0.5)))
        for lbl_t, var in [
            ("붙여넣기후", self._img_d_cb_paste),
            ("전송후",     self._img_d_cb_send),
        ]:
            tk.Label(self._img_delay_cb_row, text=lbl_t,
                     font=F_SMALL, bg=PALETTE["card"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT, padx=(6, 2))
            tk.Entry(self._img_delay_cb_row, textvariable=var,
                     width=5, bg=PALETTE["card2"], fg=PALETTE["text"],
                     insertbackground=PALETTE["text"],
                     relief=tk.FLAT, font=F_MONO
                     ).pack(side=tk.LEFT)

        # ── [파일경로] 딜레이 ──────────────────────────────────
        self._img_delay_file_row = tk.Frame(card, bg=PALETTE["card"])
        tk.Label(self._img_delay_file_row, text="딜레이(s)",
                 width=14, anchor=tk.W,
                 font=F_LABEL, bg=PALETTE["card"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        self._img_d_file_dialog = tk.StringVar(
            value=str(img_delays.get("file_dialog_open",  1.0)))
        self._img_d_file_folder = tk.StringVar(
            value=str(img_delays.get("file_folder_move",  0.8)))
        self._img_d_file_open   = tk.StringVar(
            value=str(img_delays.get("file_after_open",   0.5)))
        for lbl_t, var in [
            ("다이얼로그대기", self._img_d_file_dialog),
            ("폴더이동후",     self._img_d_file_folder),
            ("파일열기후",     self._img_d_file_open),
        ]:
            tk.Label(self._img_delay_file_row, text=lbl_t,
                     font=F_SMALL, bg=PALETTE["card"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT, padx=(6, 2))
            tk.Entry(self._img_delay_file_row, textvariable=var,
                     width=5, bg=PALETTE["card2"], fg=PALETTE["text"],
                     insertbackground=PALETTE["text"],
                     relief=tk.FLAT, font=F_MONO
                     ).pack(side=tk.LEFT)

        # 초기 상태 적용
        self._toggle_image_path()

    def _browse_image(self):
        path = filedialog.askopenfilename(
            title="이미지 파일 선택",
            filetypes=[("이미지", "*.png *.jpg *.jpeg *.bmp *.gif"),
                       ("전체", "*.*")])
        if path:
            self._img_path_var.set(path)

    # ── 위젯 state 재귀 설정 헬퍼 ──────────────────────────
    @staticmethod
    def _set_row_state(frame, state):
        """Frame 안의 Entry/Button/Radiobutton/Checkbutton 만 재귀적으로 state 변경
        Label 은 state 미지원이므로 건너뜀."""
        try:
            if not frame.winfo_exists():
                return
        except Exception:
            return
        for w in frame.winfo_children():
            try:
                if isinstance(w, (tk.Entry, tk.Button,
                                  tk.Radiobutton, tk.Checkbutton)):
                    w.config(state=state)
                elif isinstance(w, tk.Frame):
                    TemplateTab._set_row_state(w, state)
            except Exception:
                pass

    def _toggle_image_path(self):
        """이미지 사용/방식에 따라 위젯 활성화 + show/hide 전환

        ▶ 호출 시점
          · 사용함/사용안함 버튼 클릭  (_set_use_img)
          · 첨부 방식 라디오 변경      (Radiobutton command)
          · 섹션 초기 렌더 완료 후     (_render_image_section 말미)

        ▶ 행 show/hide 정책 (v1.50~)
          use=False  → 모든 상세 행 숨김 (pack_forget)
                       방식 선택 행(_img_mode_row)만 DISABLED 상태로 표시 유지
          use=True   → 현재 mode 에 맞는 행만 표시 (pack)
                       해당 없는 행은 숨김
        """
        use  = self._use_image_var.get() if hasattr(self, "_use_image_var") else False
        mode = self._img_mode_var.get()  if hasattr(self, "_img_mode_var")  else "file"

        def _apply(attr, state):
            if not hasattr(self, attr):
                return
            TemplateTab._set_row_state(getattr(self, attr), state)

        def _show_row(attr, visible, padx=12, pady=(0, 6)):
            """행 Frame 을 pack/pack_forget 으로 show/hide"""
            if not hasattr(self, attr):
                return
            w = getattr(self, attr)
            try:
                if visible:
                    w.pack(fill=tk.X, padx=padx, pady=pady)
                else:
                    w.pack_forget()
            except Exception:
                pass

        def _hide_delay_rows():
            for attr in ("_img_delay_dd_row", "_img_delay_cb_row",
                         "_img_delay_file_row"):
                _show_row(attr, False)

        # ── mode="none" 분기 (텔레그램 신규 템플릿 기본값) ────────
        # use=False → 방식 선택 행 포함 전부 비활성 + 상세 행 숨김
        # use=True  → 방식 선택 행만 NORMAL → 사용자가 방식 선택 후 재호출됨
        if mode == "none":
            _apply("_img_mode_row", tk.NORMAL if use else tk.DISABLED)
            # 상세 행 전부 숨김
            _show_row("_img_path_row",  False)
            _show_row("_img_order_row", False)
            _show_row("_img_src_row",   False)
            _show_row("_img_drop_row",  False)
            _show_row("_tg_attach_row",   False)
            _show_row("_tg_filename_row", False)
            _hide_delay_rows()
            return

        # ── 방식 선택 행: use 여부에 따라 활성/비활성 ──────────────
        _apply("_img_mode_row", tk.NORMAL if use else tk.DISABLED)

        # ── 이미지 경로 행 (파일경로 방식 + use=True) ──────────────
        show_path = use and mode == "file"
        _show_row("_img_path_row", show_path, pady=(0, 8))
        _apply("_img_path_row", tk.NORMAL if show_path else tk.DISABLED)

        # ── 소스/드롭 좌표 행 (드래그앤드롭 방식 + use=True) ────────
        show_dd = use and mode == "dragdrop"
        _show_row("_img_src_row",  show_dd, pady=(0, 4))
        _show_row("_img_drop_row", show_dd, pady=(0, 4))
        _apply("_img_src_row",  tk.NORMAL if show_dd else tk.DISABLED)
        _apply("_img_drop_row", tk.NORMAL if show_dd else tk.DISABLED)

        # ── 텔레그램 전용: 첨부버튼/파일명 좌표 행 ───────────────────
        # Telethon API 모드(계정 있음)에서는 좌표 행을 절대 표시하지 않음
        # (API가 직접 파일을 전송하므로 좌표 불필요)
        _is_tg_api_now = (
            HAS_TELETHON
            and bool(load_json(TG_ACCOUNTS_PATH, []))
        )
        show_tg_file = use and mode == "file" and not _is_tg_api_now
        _show_row("_tg_attach_row",   show_tg_file, pady=(0, 4))
        _show_row("_tg_filename_row", show_tg_file, pady=(0, 4))

        # ── 첨부 순서 행: use=True 이면 방식 불문 표시 ─────────────
        _show_row("_img_order_row", use, pady=(0, 10))
        _apply("_img_order_row", tk.NORMAL if use else tk.DISABLED)

        # ── 모드별 딜레이 행 show/hide ──────────────────────────────
        _show_row("_img_delay_dd_row",   use and mode == "dragdrop",  pady=(0, 10))
        _show_row("_img_delay_cb_row",   use and mode == "clipboard", pady=(0, 10))
        _show_row("_img_delay_file_row", use and mode == "file",      pady=(0, 10))

    # ── 섹션 5 : 좌표 설정 렌더링 ───────────────────────────
    def _render_coord_section(self):
        for w in self._coord_section_wrap.winfo_children():
            w.destroy()
        self._coord_rows = []

        wk   = self._wtype_var.get()

        # ★ 오픈채팅/가망뿌리기: 좌표 설정 섹션 불필요
        #   - 채팅창 시작좌표 → ⚙️ 좌표 자동계산 섹션
        #   - 이미지 소스/드롭 → 🖼 이미지 첨부 섹션
        #   - 전송/닫기 버튼  → ⚙️ 전송·닫기 방식 섹션
        if wk == "kakao_openchat":
            return

        wdef = PLATFORM_WORKFLOWS.get(wk, {})
        keys   = wdef.get("coord_keys",   [])
        labels = wdef.get("coord_labels", [])
        types  = wdef.get("coord_types",  [])
        saved  = self._cur("coords", {})

        # ── Telethon 권장 워크플로우: 설치 여부에 따라 안내 배너 표시 ──
        if wdef.get("telethon_preferred"):
            if HAS_TELETHON:
                tg_accounts = load_json(TG_ACCOUNTS_PATH, [])
                if tg_accounts:
                    # Telethon 설치 + 계정 있음 → 좌표 불필요, 섹션 전체 숨김
                    # (이미지 섹션에 간결한 인라인 안내가 있으므로 여기선 배너만)
                    banner = tk.Frame(self._coord_section_wrap,
                                      bg="#D1FAE5",
                                      highlightbackground="#6EE7B7",
                                      highlightthickness=1)
                    banner.pack(fill=tk.X, pady=(0, 4))
                    tk.Label(banner,
                             text="✅  Telethon API 모드 — 메시지 발송·이미지 첨부·좌표 설정이 모두 API로 처리됩니다.\n"
                                  "    아래 마우스 좌표 항목은 사용되지 않으므로 설정하지 않아도 됩니다.",
                             font=F_SMALL, bg="#D1FAE5",
                             fg="#065F46", padx=10, pady=7, justify="left"
                             ).pack(anchor="w")
                    return   # 좌표 섹션 렌더 불필요
                else:
                    # Telethon 설치됐지만 계정 없음
                    banner = tk.Frame(self._coord_section_wrap,
                                      bg="#FEF9C3",
                                      highlightbackground="#FDE047",
                                      highlightthickness=1)
                    banner.pack(fill=tk.X, pady=(0, 8))
                    tk.Label(banner,
                             text="⚠️  Telethon 설치됨 — 텔레그램 계정 탭에서 계정을 추가하면\n"
                                  "    API 방식으로 자동 전환되어 아래 좌표가 필요 없어집니다.",
                             font=F_SMALL, bg="#FEF9C3",
                             fg="#713F12", padx=10, pady=6, justify="left"
                             ).pack(anchor="w")
            else:
                # Telethon 미설치 → pyautogui 폴백 안내
                banner = tk.Frame(self._coord_section_wrap,
                                  bg="#FEF3C7",
                                  highlightbackground="#FCD34D",
                                  highlightthickness=1)
                banner.pack(fill=tk.X, pady=(0, 8))
                tk.Label(banner,
                         text="ℹ️  현재 pyautogui(크롬 자동화) 모드입니다.\n"
                              "    pip install telethon 설치 후 계정 추가 시\n"
                              "    API 방식으로 전환되어 더 안정적으로 동작합니다.",
                         font=F_SMALL, bg="#FEF3C7",
                         fg="#92400E", padx=10, pady=6, justify="left"
                         ).pack(anchor="w")

        card = _make_section_header_in(self._coord_section_wrap, "🖱️ 좌표 설정")
        # 캡처 안내 (카드 상단에 작은 캡션)
        _cap_row = tk.Frame(card, bg=PALETTE["card"])
        _cap_row.pack(fill=tk.X, padx=12, pady=(6, 0))
        tk.Label(_cap_row,
                 text="📸 캡처 버튼 클릭 → 3초 후 마우스 위치 저장  /  영역은 드래그로 지정",
                 font=F_SMALL,
                 bg=PALETTE["card"], fg=PALETTE["muted"]
                 ).pack(anchor=tk.W)

        for i, (key, label, ctype) in enumerate(
                zip(keys, labels, types)):
            sv = saved.get(key, {})
            self._build_coord_row(card, i, key, label, ctype, sv)

    def _build_coord_row(self, parent, idx, key, label, ctype, saved):
        r = tk.Frame(parent, bg=PALETTE["card"])
        r.pack(fill=tk.X, padx=12, pady=5)

        # 라벨
        tk.Label(r, text=label, width=16, anchor=tk.W,
                 font=F_LABEL,
                 bg=PALETTE["card"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)

        if ctype == "area":
            # 영역: x1, y1, x2, y2
            vars_ = {}
            for k, default in [("x1", saved.get("x1", 0)),
                                ("y1", saved.get("y1", 0)),
                                ("x2", saved.get("x2", 0)),
                                ("y2", saved.get("y2", 0))]:
                v = tk.StringVar(value=str(default))
                vars_[k] = v
                tk.Label(r, text=k+":",
                         font=F_MONO_S,
                         bg=PALETTE["card"],
                         fg=PALETTE["text"]
                         ).pack(side=tk.LEFT, padx=(4, 0))
                tk.Entry(r, textvariable=v, width=5,
                         bg=PALETTE["card2"], fg=PALETTE["text"],
                         insertbackground=PALETTE["text"],
                         relief=tk.FLAT,
                         font=F_MONO
                         ).pack(side=tk.LEFT)
            tk.Button(r, text="📸 드래그",
                      command=lambda k=key, vs=vars_:
                          self._capture_area(k, vs),
                      bg=PALETTE["primary"], fg="#FFFFFF",
                      relief=tk.FLAT, font=F_SMALL,
                      cursor="hand2", padx=6, pady=2
                      ).pack(side=tk.LEFT, padx=(8, 0))
            self._coord_rows.append(
                {"key": key, "type": "area", "vars": vars_})
        else:
            # 포인트: x, y
            xv = tk.StringVar(value=str(saved.get("x", 0)))
            yv = tk.StringVar(value=str(saved.get("y", 0)))
            for lbl, v in [("X:", xv), ("Y:", yv)]:
                tk.Label(r, text=lbl,
                         font=F_MONO_S,
                         bg=PALETTE["card"],
                         fg=PALETTE["text"]
                         ).pack(side=tk.LEFT, padx=(4, 0))
                tk.Entry(r, textvariable=v, width=6,
                         bg=PALETTE["card2"], fg=PALETTE["text"],
                         insertbackground=PALETTE["text"],
                         relief=tk.FLAT,
                         font=F_MONO
                         ).pack(side=tk.LEFT)
            # 현재 좌표 표시 라벨 (캡처 성공 시 연초록 배경 + 굵게 강조)
            disp_wrap = tk.Frame(r, bg=PALETTE["card"])
            disp_wrap.pack(side=tk.LEFT, padx=(6, 0))
            disp = tk.Label(disp_wrap, text="",
                            font=(_FFM, 8, "bold"),
                            bg=PALETTE["card"],
                            fg=PALETTE["success_text"],
                            padx=5, pady=2)
            disp.pack()
            tk.Button(r, text="📸 캡처",
                      command=lambda k=key, x=xv, y=yv, d=disp, dw=disp_wrap:
                          self._capture_point(k, x, y, d, dw),
                      bg=PALETTE["primary"], fg="#FFFFFF",
                      relief=tk.FLAT, font=F_SMALL,
                      cursor="hand2", padx=6, pady=2
                      ).pack(side=tk.LEFT, padx=(8, 0))
            self._coord_rows.append(
                {"key": key, "type": "point",
                 "xv": xv, "yv": yv})
    # ── 섹션 6 : OCR 설정 (친구추가 전용) ──────────────────
    def _render_friend_option_section(self):
        for w in self._ocr_section_wrap.winfo_children():
            w.destroy()

        wk = self._wtype_var.get()

        # ── kakao_openchat: 이 섹션 표시 안 함 ──────────────
        if wk != "kakao_friend":
            return

        # ══ kakao_friend 전용 옵션 섹션 ═════════════════════
        if wk == "kakao_friend":
            tk.Label(self._ocr_section_wrap,
                     text="⚙️ 친구추가 옵션",
                     font=F_HEAD,
                     bg=PALETTE["bg"], fg=PALETTE["text"]
                     ).pack(anchor=tk.W, pady=(0, 6))
            card = tk.Frame(self._ocr_section_wrap,
                            bg=PALETTE["card"],
                            highlightbackground=PALETTE["border"],
                            highlightthickness=1)
            card.pack(fill=tk.X)
            opt_row = tk.Frame(card, bg=PALETTE["card"])
            opt_row.pack(fill=tk.X, padx=12, pady=10)
            self._rename_existing_var = tk.BooleanVar(
                value=self._cur("rename_existing", False))
            tk.Checkbutton(opt_row,
                           text="기존 친구도 이름 변경 포함 (분기점 3)",
                           variable=self._rename_existing_var,
                           bg=PALETTE["card"], fg=PALETTE["text"],
                           selectcolor=PALETTE["active"],
                           activebackground=PALETTE["card"],
                           font=F_LABEL
                           ).pack(side=tk.LEFT)
            tk.Label(opt_row,
                     text="  ← 체크 시 이미 친구인 ID도 이름변경 수행",
                     font=F_SMALL,
                     bg=PALETTE["card"], fg=PALETTE["muted"]
                     ).pack(side=tk.LEFT)
            # 키워드/시작번호/자릿수/재시도 설정
            tk.Frame(card, bg=PALETTE["border"], height=1
                     ).pack(fill=tk.X, padx=12, pady=(0, 4))

            def _row2(label, widget_fn):
                r = tk.Frame(card, bg=PALETTE["card"])
                r.pack(fill=tk.X, padx=12, pady=6)
                tk.Label(r, text=label, width=16, anchor=tk.W,
                         font=F_LABEL,
                         bg=PALETTE["card"], fg=PALETTE["text"]
                         ).pack(side=tk.LEFT)
                widget_fn(r)

            # 키워드
            def _kw_w(p):
                self._id_keyword_var = tk.StringVar(
                    value=self._cur("id_keyword", "가망"))
                e = tk.Entry(p, textvariable=self._id_keyword_var,
                             bg=PALETTE["card2"], fg=PALETTE["text"],
                             insertbackground=PALETTE["text"],
                             relief=tk.FLAT, font=F_MONO, width=14)
                e.pack(side=tk.LEFT, padx=(0, 8))
                e.bind("<KeyRelease>", lambda ev: self._update_id_preview())
                tk.Label(p, text="(이름 접두사, 예: 가망, test 등)",
                         font=F_SMALL, bg=PALETTE["card"], fg=PALETTE["text"]
                         ).pack(side=tk.LEFT)
            _row2("키워드", _kw_w)

            # 시작 번호
            def _startnum_w(p):
                self._id_start_var = tk.StringVar(
                    value=str(self._cur("id_start_num", 1)))
                tk.Entry(p, textvariable=self._id_start_var,
                         bg=PALETTE["card2"], fg=PALETTE["text"],
                         insertbackground=PALETTE["text"],
                         relief=tk.FLAT, font=F_MONO, width=8
                         ).pack(side=tk.LEFT, padx=(0, 8))
                tk.Label(p, text="부터 시작  (예: 1 → 가망1, 가망2...)",
                         font=F_SMALL, bg=PALETTE["card"], fg=PALETTE["text"]
                         ).pack(side=tk.LEFT)
                self._id_start_var.trace_add(
                    "write", lambda *a: self._update_id_preview())
            _row2("시작 번호", _startnum_w)

            # 자릿수
            def _digits_w(p):
                self._id_digits_var = tk.StringVar(
                    value=str(self._cur("id_digits", 0)))
                tk.Label(p, text="자릿수 고정",
                         font=F_LABEL, bg=PALETTE["card"], fg=PALETTE["text"]
                         ).pack(side=tk.LEFT)
                tk.Spinbox(p, from_=0, to=6,
                           textvariable=self._id_digits_var,
                           width=4, font=F_MONO,
                           bg=PALETTE["card2"], fg=PALETTE["text"],
                           buttonbackground=PALETTE["card"], relief=tk.FLAT
                           ).pack(side=tk.LEFT, padx=(6, 8))
                tk.Label(p, text="0=자동  3이면 001,002...",
                         font=F_SMALL, bg=PALETTE["card"], fg=PALETTE["text"]
                         ).pack(side=tk.LEFT)
                self._id_digits_var.trace_add(
                    "write", lambda *a: self._update_id_preview())
            _row2("자릿수", _digits_w)

            # 미리보기
            prev_row = tk.Frame(card, bg=PALETTE["card"])
            prev_row.pack(fill=tk.X, padx=12, pady=(2, 8))
            tk.Label(prev_row, text="미리보기", width=16, anchor=tk.W,
                     font=F_LABEL, bg=PALETTE["card"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT)
            self._id_preview_lbl = tk.Label(
                prev_row, text="",
                font=F_MONO, bg=PALETTE["card"], fg=PALETTE["success_text"])
            self._id_preview_lbl.pack(side=tk.LEFT)
            self._update_id_preview()
            return  # kakao_friend 는 여기서 종료

    def _update_id_preview(self):
        """ID 미리보기 갱신"""
        try:
            kw     = self._id_keyword_var.get()
            start  = safe_int(self._id_start_var.get(), 1)
            digits = safe_int(self._id_digits_var.get(), 0)
            ex0 = build_search_id(kw, start, 0, digits)
            ex1 = build_search_id(kw, start, 1, digits)
            ex2 = build_search_id(kw, start, 2, digits)
            self._id_preview_lbl.config(
                text=f"{ex0},  {ex1},  {ex2},  ...")
        except Exception:
            pass

    def _browse_tesseract(self):
        path = filedialog.askopenfilename(
            title="tesseract.exe 선택",
            filetypes=[("\uc2e4\ud589\ud30c\uc77c", "*.exe"),
                       ("\uc804\uccb4", "*.*")])
        if path:
            self._tess_var.set(path)


    # ── 타이밍 설정 섹션 ────────────────────────────────────
    def _render_timing_section(self):
        """동작 타이밍 설정 (워크플로우별)"""
        for w in self._timing_section_wrap.winfo_children():
            w.destroy()

        wk = self._wtype_var.get()

        # ─ 섹션 제목 & 카드 헬퍼 (통일된 4px 컬러바 방식) ──
        def _make_card():
            return _make_section_header_in(
                self._timing_section_wrap, "⏱️ 딜레이 설정")

        def _row(parent):
            r = tk.Frame(parent, bg=PALETTE["card"])
            r.pack(fill=tk.X, padx=12, pady=(8, 4))
            return r

        def _field(row, label, var, width=6):
            tk.Label(row, text=label, font=F_SMALL,
                     bg=PALETTE["card"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT, padx=(10, 2))
            tk.Entry(row, textvariable=var, width=width,
                     bg=PALETTE["card2"], fg=PALETTE["text"],
                     insertbackground=PALETTE["text"],
                     relief=tk.FLAT, font=F_MONO
                     ).pack(side=tk.LEFT)

        # ════════════════════════════════════════════════
        # 카카오 메시지 / 오픈채팅 : v1.52 — 7개 단계별 딜레이
        # ════════════════════════════════════════════════
        if wk == "kakao_openchat":
            # ── v1.53: 플로우 순서 기반 단계별 행 레이아웃 ──────────────
            # 변수명(self._oc_after_*, _between_chats_var, _jitter_val_var) 유지
            # → _save_template / _run_kakao_openchat 충돌 없음
            card = _make_card()

            # StringVar 선언 (저장 키와 1:1 대응, 절대 변경 금지)
            self._oc_after_open  = tk.StringVar(value=str(self._cur("oc_after_open",  1.5)))
            self._oc_after_click = tk.StringVar(value=str(self._cur("oc_after_click", 0.3)))
            self._oc_after_type  = tk.StringVar(value=str(self._cur("oc_after_type",  0.3)))
            self._oc_after_send  = tk.StringVar(value=str(self._cur("oc_after_send",  1.0)))
            self._oc_after_close = tk.StringVar(value=str(self._cur("oc_after_close", 0.8)))
            self._between_chats_var = tk.StringVar(value=str(self._cur("between_chats",  0.5)))
            self._jitter_val_var    = tk.StringVar(value=str(self._cur("between_jitter", 0.3)))

            # 플로우 행 헬퍼 ─ (단계번호, 동작 설명, 딜레이 라벨, 변수)
            def _flow_row(step, action_txt, delay_lbl, var, hint=""):
                r = tk.Frame(card, bg=PALETTE["card"])
                r.pack(fill=tk.X, padx=12, pady=(6, 2))
                # 단계 번호
                tk.Label(r, text=step, font=F_LABEL,
                         width=3, anchor=tk.CENTER,
                         bg=PALETTE["primary2"], fg="#FFFFFF"
                         ).pack(side=tk.LEFT, padx=(0, 8))
                # 동작 설명
                tk.Label(r, text=action_txt, font=F_LABEL,
                         width=22, anchor=tk.W,
                         bg=PALETTE["card"], fg=PALETTE["text"]
                         ).pack(side=tk.LEFT)
                # 딜레이 라벨 + 입력
                tk.Label(r, text=delay_lbl, font=F_SMALL,
                         bg=PALETTE["card"], fg=PALETTE["text"]
                         ).pack(side=tk.LEFT, padx=(8, 2))
                tk.Entry(r, textvariable=var, width=5,
                         bg=PALETTE["card2"], fg=PALETTE["text"],
                         insertbackground=PALETTE["text"],
                         relief=tk.FLAT, font=F_MONO
                         ).pack(side=tk.LEFT)
                tk.Label(r, text="s", font=F_SMALL,
                         bg=PALETTE["card"], fg=PALETTE["text"]
                         ).pack(side=tk.LEFT, padx=(2, 0))
                if hint:
                    tk.Label(r, text=hint, font=F_SMALL,
                             bg=PALETTE["card"], fg=PALETTE["muted"]
                             ).pack(side=tk.LEFT, padx=(8, 0))

            # ── 구분선 헬퍼 ──
            def _divider(txt):
                d = tk.Frame(card, bg=PALETTE["card"])
                d.pack(fill=tk.X, padx=12, pady=(8, 0))
                tk.Label(d, text=txt, font=F_SMALL,
                         bg=PALETTE["card"], fg=PALETTE["muted"]
                         ).pack(side=tk.LEFT)
                tk.Frame(d, bg=PALETTE["border"], height=1
                         ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 0))

            _divider("── 채팅방 진입")
            _flow_row("①", "채팅방 더블클릭 → 창 열림",
                      "열림 대기", self._oc_after_open,
                      "(앱 로딩 시간)")
            _flow_row("②", "입력창 클릭/포커싱 → 활성화",
                      "클릭/포커싱 후", self._oc_after_click)
            _flow_row("③", "메시지 입력 → 완료",
                      "입력 후", self._oc_after_type)

            _divider("── 전송 · 닫기")
            _flow_row("④", "전송 (Enter / 버튼) → 완료",
                      "전송 후", self._oc_after_send)
            _flow_row("⑤", "창 닫기 → 완전히 닫힘",
                      "닫힘 후", self._oc_after_close,
                      "💡 클수록 이중전송 방지↑")

            _divider("── 다음 채팅방")
            _flow_row("⑥", "다음 채팅방으로 이동",
                      "간격", self._between_chats_var)
            # 지터는 ⑥ 행 옆에 붙임 (별도 행 불필요)
            r_jitter = tk.Frame(card, bg=PALETTE["card"])
            r_jitter.pack(fill=tk.X, padx=12, pady=(2, 0))
            tk.Label(r_jitter, text="   ", width=3,
                     bg=PALETTE["card"]).pack(side=tk.LEFT, padx=(0, 8))
            tk.Label(r_jitter, text="", width=22,
                     bg=PALETTE["card"]).pack(side=tk.LEFT)
            tk.Label(r_jitter, text="±지터", font=F_SMALL,
                     bg=PALETTE["card"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT, padx=(8, 2))
            tk.Entry(r_jitter, textvariable=self._jitter_val_var, width=5,
                     bg=PALETTE["card2"], fg=PALETTE["text"],
                     insertbackground=PALETTE["text"],
                     relief=tk.FLAT, font=F_MONO
                     ).pack(side=tk.LEFT)
            tk.Label(r_jitter, text="s", font=F_SMALL,
                     bg=PALETTE["card"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT, padx=(2, 0))

            tk.Frame(card, bg=PALETTE["card"], height=8).pack()

        # ════════════════════════════════════════════════
        # 카카오 친구추가 : 원본 봇 v3.0 타이밍 5개 + 간격/지터
        # ════════════════════════════════════════════════
        elif wk == "kakao_friend":
            card = _make_card()
            # 행1: OCR/입력 관련
            r1 = _row(card)
            tk.Label(r1, text="단계 타이밍", width=16, anchor=tk.W,
                     font=F_LABEL, bg=PALETTE["card"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT)
            self._kf_after_ctrlA      = tk.StringVar(value=str(self._cur("after_ctrlA",      2.0)))
            self._kf_after_click      = tk.StringVar(value=str(self._cur("after_click",      1.5)))
            self._kf_after_input      = tk.StringVar(value=str(self._cur("after_input",      2.5)))
            self._kf_after_color_wait = tk.StringVar(value=str(self._cur("after_color_wait", 0.6)))
            self._kf_after_tab        = tk.StringVar(value=str(self._cur("after_tab",        0.5)))
            for lbl_t, var in [
                ("Ctrl+A 후(s)", self._kf_after_ctrlA),
                ("클릭 후(s)",   self._kf_after_click),
                ("입력 후(s)",   self._kf_after_input),
            ]:
                _field(r1, lbl_t, var)
            # 행2
            r2 = _row(card)
            tk.Label(r2, text="", width=16, anchor=tk.W,
                     font=F_LABEL, bg=PALETTE["card"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT)
            for lbl_t, var in [
                ("색판별대기(s)", self._kf_after_color_wait),
                ("Tab 후(s)",     self._kf_after_tab),
            ]:
                _field(r2, lbl_t, var)
            # 행3: 간격/지터 (kakao_friend 전용 변수명 사용)
            r3 = _row(card)
            tk.Label(r3, text="ID 간격", width=16, anchor=tk.W,
                     font=F_LABEL, bg=PALETTE["card"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT)
            self._kf_between_var = tk.StringVar(
                value=str(self._cur("between_chats",  1.0)))
            self._kf_jitter_var  = tk.StringVar(
                value=str(self._cur("between_jitter", 0.3)))
            for lbl_t, var in [
                ("간격(s)",  self._kf_between_var),
                ("±지터(s)", self._kf_jitter_var),
            ]:
                _field(r3, lbl_t, var)
            tk.Frame(card, bg=PALETTE["card"], height=4).pack()

        # ════════════════════════════════════════════════
        # 텔레그램: API 모드 / 일반(pyautogui) 모드 분리
        # ════════════════════════════════════════════════
        elif wk in ("telegram_join", "telegram_message", "telegram_join_and_message"):
            _is_tg_api_delay = (
                HAS_TELETHON
                and bool(load_json(TG_ACCOUNTS_PATH, []))
            )

            # ── 섹션 헤더 (4px 컬러바) + 카드 ──────────────────
            card = _make_card()

            # ── 모드 표시 배너 (카드 내부 최상단) ─────────────
            _banner_bg  = "#D1FAE5" if _is_tg_api_delay else "#FEF3C7"
            _banner_bdr = "#6EE7B7" if _is_tg_api_delay else "#FCD34D"
            _banner_fg  = "#065F46" if _is_tg_api_delay else "#92400E"
            _banner_txt = ("📡  Telethon API 모드  ·  단계별 딜레이 설정"
                           if _is_tg_api_delay else
                           "🖱️  일반(pyautogui) 모드  ·  크롬 자동화 딜레이 설정")
            _banner_frame = tk.Frame(card,
                                     bg=_banner_bg,
                                     highlightbackground=_banner_bdr,
                                     highlightthickness=1)
            _banner_frame.pack(fill=tk.X, padx=12, pady=(8, 4))
            tk.Label(_banner_frame,
                     text=_banner_txt,
                     font=(_FF, 9, "bold"),
                     bg=_banner_bg, fg=_banner_fg,
                     padx=10, pady=5
                     ).pack(anchor="w")

            if _is_tg_api_delay:
                # ════ Telethon API 모드 딜레이 ════════════════
                # 서브 헤더
                _sh = tk.Frame(card, bg=PALETTE["card"])
                _sh.pack(fill=tk.X, padx=12, pady=(4, 2))
                tk.Label(_sh, text="[API 단계별 딜레이]",
                         font=(_FF, 9, "bold"), bg=PALETTE["card"],
                         fg=PALETTE["primary"]).pack(anchor="w")

                # 행A: 연결 / 재연결
                rA = _row(card)
                tk.Label(rA, text="연결 단계", width=16, anchor=tk.W,
                         font=F_LABEL, bg=PALETTE["card"], fg=PALETTE["text"]
                         ).pack(side=tk.LEFT)
                self._tg_api_connect_delay = tk.StringVar(
                    value=str(self._cur("tg_api_connect_delay", 2.0)))
                self._tg_api_retry_delay   = tk.StringVar(
                    value=str(self._cur("tg_api_retry_delay",   5.0)))
                for lbl_t, var in [
                    ("계정연결(s)",   self._tg_api_connect_delay),
                    ("재시도대기(s)", self._tg_api_retry_delay),
                ]:
                    _field(rA, lbl_t, var)

                # 행B: 발송 전후
                rB = _row(card)
                tk.Label(rB, text="발송 전후", width=16, anchor=tk.W,
                         font=F_LABEL, bg=PALETTE["card"], fg=PALETTE["text"]
                         ).pack(side=tk.LEFT)
                self._tg_api_before_send = tk.StringVar(
                    value=str(self._cur("tg_api_before_send", 0.5)))
                self._tg_api_after_send  = tk.StringVar(
                    value=str(self._cur("tg_api_after_send",  1.0)))
                for lbl_t, var in [
                    ("발송 전(s)", self._tg_api_before_send),
                    ("발송 후(s)", self._tg_api_after_send),
                ]:
                    _field(rB, lbl_t, var)

                # 행C: 캡처
                rC = _row(card)
                tk.Label(rC, text="발송 후 캡처", width=16, anchor=tk.W,
                         font=F_LABEL, bg=PALETTE["card"], fg=PALETTE["text"]
                         ).pack(side=tk.LEFT)
                self._tg_api_capture_delay = tk.StringVar(
                    value=str(self._cur("tg_api_capture_delay", 2.0)))
                self._tg_api_capture_msgs  = tk.StringVar(
                    value=str(self._cur("tg_api_capture_msgs",  5)))
                for lbl_t, var in [
                    ("캡처대기(s)",  self._tg_api_capture_delay),
                    ("최근메시지수", self._tg_api_capture_msgs),
                ]:
                    _field(rC, lbl_t, var)
                # 캡처 ON/OFF (v1.62: 채팅캡처 ON = 텍스트+말풍선PNG 동시 저장)
                self._tg_api_capture_on = tk.BooleanVar(
                    value=self._cur("tg_api_capture_on", False))
                tk.Checkbutton(rC, text="발송 후 채팅 캡처 ON",
                               variable=self._tg_api_capture_on,
                               bg=PALETTE["card"], fg=PALETTE["text"],
                               selectcolor=PALETTE["card2"],
                               activebackground=PALETTE["card"],
                               font=F_LABEL
                               ).pack(side=tk.LEFT, padx=(10, 0))
                tk.Label(rC,
                         text="(텍스트 로그 + 말풍선 PNG 동시 저장)",
                         font=F_SMALL,
                         bg=PALETTE["card"], fg=PALETTE["muted"]
                         ).pack(side=tk.LEFT, padx=(6, 0))

                # 행G: 발송 전 사전 체크 옵션
                rG = _row(card)
                tk.Label(rG, text="발송 전 체크", width=16, anchor=tk.W,
                         font=F_LABEL, bg=PALETTE["card"], fg=PALETTE["text"]
                         ).pack(side=tk.LEFT)
                self._tg_pre_check_acct = tk.BooleanVar(
                    value=self._cur("tg_pre_check_acct", True))
                self._tg_pre_check_perm = tk.BooleanVar(
                    value=self._cur("tg_pre_check_perm", True))
                tk.Checkbutton(rG, text="계정 상태 확인",
                               variable=self._tg_pre_check_acct,
                               bg=PALETTE["card"], fg=PALETTE["text"],
                               selectcolor=PALETTE["card2"],
                               activebackground=PALETTE["card"],
                               font=F_LABEL
                               ).pack(side=tk.LEFT)
                _tip_acct = tk.Label(rG, text="?",
                                     font=(_FF, 7, "bold"),
                                     bg=PALETTE["primary"], fg="#FFFFFF",
                                     width=2, cursor="question_arrow",
                                     relief=tk.FLAT)
                _tip_acct.pack(side=tk.LEFT, padx=(2, 10))
                add_tip(_tip_acct,
                    "발송 전 get_me() 로 계정 제재/밴/스캠 여부 확인\n"
                    "이상 감지 시 해당 계정 발송 건너뜀\n"
                    "(OFF: 빠르지만 제재 계정도 시도)")
                tk.Checkbutton(rG, text="채팅방 권한 확인",
                               variable=self._tg_pre_check_perm,
                               bg=PALETTE["card"], fg=PALETTE["text"],
                               selectcolor=PALETTE["card2"],
                               activebackground=PALETTE["card"],
                               font=F_LABEL
                               ).pack(side=tk.LEFT)
                _tip_perm = tk.Label(rG, text="?",
                                     font=(_FF, 7, "bold"),
                                     bg=PALETTE["primary"], fg="#FFFFFF",
                                     width=2, cursor="question_arrow",
                                     relief=tk.FLAT)
                _tip_perm.pack(side=tk.LEFT, padx=(2, 0))
                add_tip(_tip_perm,
                    "발송 전 get_permissions() 로 밴/비멤버/전송권한 확인\n"
                    "권한 없는 채팅방 자동 스킵\n"
                    "(OFF: 빠르지만 권한없는 방도 시도)")

                # 행D: 링크 간격
                rD = _row(card)
                tk.Label(rD, text="링크 간격", width=16, anchor=tk.W,
                         font=F_LABEL, bg=PALETTE["card"], fg=PALETTE["text"]
                         ).pack(side=tk.LEFT)
                self._tg_between_min = tk.StringVar(
                    value=str(self._cur("tg_between_min", 3.0)))
                self._tg_between_max = tk.StringVar(
                    value=str(self._cur("tg_between_max", 7.0)))
                for lbl_t, var in [
                    ("최소(s)", self._tg_between_min),
                    ("최대(s)", self._tg_between_max),
                ]:
                    _field(rD, lbl_t, var)

                # 행E: 계정 분배
                rE = _row(card)
                tk.Label(rE, text="계정 분배 모드", width=16, anchor=tk.W,
                         font=F_LABEL, bg=PALETTE["card"], fg=PALETTE["text"]
                         ).pack(side=tk.LEFT)
                self._account_mode_var = tk.StringVar(
                    value=self._cur("account_mode", "zigzag"))
                for mode_val, mode_lbl in [
                    ("zigzag", "🔄 순환"),
                    ("split",  "⚖️ 균등분배"),
                    ("all",    "📢 전체"),
                ]:
                    tk.Radiobutton(
                        rE, text=mode_lbl,
                        variable=self._account_mode_var, value=mode_val,
                        font=F_LABEL, bg=PALETTE["card"],
                        fg=PALETTE["text"],
                        selectcolor=PALETTE["card2"],
                        activebackground=PALETTE["card"]
                    ).pack(side=tk.LEFT, padx=(0, 8))

                # 행F: 계정 전환
                rF = _row(card)
                tk.Label(rF, text="계정 전환", width=16, anchor=tk.W,
                         font=F_LABEL, bg=PALETTE["card"], fg=PALETTE["text"]
                         ).pack(side=tk.LEFT)
                self._account_sw_delay = tk.StringVar(
                    value=str(self._cur("account_switch_delay", 1.0)))
                self._tg_api_acct_warmup = tk.StringVar(
                    value=str(self._cur("tg_api_acct_warmup", 0.5)))
                for lbl_t, var, hint in [
                    ("전환대기(s)",   self._account_sw_delay,
                     "계정을 바꿀 때마다 기다리는 시간\n(너무 짧으면 Flood 오류 가능)"),
                    ("워밍업추가(s)", self._tg_api_acct_warmup,
                     "신규 or 장기 미사용 계정 첫 전송 시\n추가로 기다리는 준비 시간"),
                ]:
                    _field(rF, lbl_t, var)
                    tip_lbl = tk.Label(rF, text="?",
                                       font=(_FF, 7, "bold"),
                                       bg=PALETTE["primary"], fg="#FFFFFF",
                                       width=2, cursor="question_arrow",
                                       relief=tk.FLAT)
                    tip_lbl.pack(side=tk.LEFT, padx=(2, 8))
                    add_tip(tip_lbl, hint)

                # 더미 변수: 저장 시 hasattr 체크용 (pyautogui 전용 키 채우기)
                self._tg_chrome_load = tk.StringVar(value="2.0")
                self._tg_tg_open     = tk.StringVar(value="1.5")
                self._tg_join_click  = tk.StringVar(value="2.0")
                self._tg_after_type  = tk.StringVar(value="0.5")
                self._tg_after_send  = tk.StringVar(value="1.0")
                self._tg_after_back  = tk.StringVar(value="0.8")

                tk.Frame(card, bg=PALETTE["card"], height=4).pack()

            else:
                # ════ pyautogui(일반) 모드 딜레이 ═════════════
                # 서브 헤더
                _sh = tk.Frame(card, bg=PALETTE["card"])
                _sh.pack(fill=tk.X, padx=12, pady=(4, 2))
                tk.Label(_sh, text="[크롬 자동화 단계별 딜레이]",
                         font=(_FF, 9, "bold"), bg=PALETTE["card"],
                         fg=PALETTE["accent"]).pack(anchor="w")

                # 행1: 로딩/전환
                r1 = _row(card)
                tk.Label(r1, text="로딩 대기", width=16, anchor=tk.W,
                         font=F_LABEL, bg=PALETTE["card"], fg=PALETTE["text"]
                         ).pack(side=tk.LEFT)
                self._tg_chrome_load = tk.StringVar(
                    value=str(self._cur("tg_chrome_load",   2.0)))
                self._tg_tg_open     = tk.StringVar(
                    value=str(self._cur("tg_telegram_open", 1.5)))
                self._tg_join_click  = tk.StringVar(
                    value=str(self._cur("tg_join_click",    2.0)))
                for lbl_t, var in [
                    ("Chrome(s)",   self._tg_chrome_load),
                    ("앱전환(s)",   self._tg_tg_open),
                    ("가입클릭(s)", self._tg_join_click),
                ]:
                    _field(r1, lbl_t, var)

                # 행2: 메시지 관련
                r2 = _row(card)
                tk.Label(r2, text="메시지 딜레이", width=16, anchor=tk.W,
                         font=F_LABEL, bg=PALETTE["card"], fg=PALETTE["text"]
                         ).pack(side=tk.LEFT)
                self._tg_after_type = tk.StringVar(
                    value=str(self._cur("tg_after_type", 0.5)))
                self._tg_after_send = tk.StringVar(
                    value=str(self._cur("tg_after_send", 1.0)))
                self._tg_after_back = tk.StringVar(
                    value=str(self._cur("tg_after_back", 0.8)))
                for lbl_t, var in [
                    ("타이핑 후(s)", self._tg_after_type),
                    ("전송 후(s)",   self._tg_after_send),
                    ("뒤로가기(s)",  self._tg_after_back),
                ]:
                    _field(r2, lbl_t, var)

                # 행3: 링크 간격
                r3 = _row(card)
                tk.Label(r3, text="링크 간격", width=16, anchor=tk.W,
                         font=F_LABEL, bg=PALETTE["card"], fg=PALETTE["text"]
                         ).pack(side=tk.LEFT)
                self._tg_between_min = tk.StringVar(
                    value=str(self._cur("tg_between_min", 3.0)))
                self._tg_between_max = tk.StringVar(
                    value=str(self._cur("tg_between_max", 7.0)))
                for lbl_t, var in [
                    ("최소(s)", self._tg_between_min),
                    ("최대(s)", self._tg_between_max),
                ]:
                    _field(r3, lbl_t, var)

                # 행4: 계정 분배 (pyautogui 모드에서도 표시, 추후 API 전환 대비)
                r4 = _row(card)
                tk.Label(r4, text="계정 분배 모드", width=16, anchor=tk.W,
                         font=F_LABEL, bg=PALETTE["card"], fg=PALETTE["text"]
                         ).pack(side=tk.LEFT)
                self._account_mode_var = tk.StringVar(
                    value=self._cur("account_mode", "zigzag"))
                for mode_val, mode_lbl in [
                    ("zigzag", "🔄 순환"),
                    ("split",  "⚖️ 균등분배"),
                    ("all",    "📢 전체"),
                ]:
                    tk.Radiobutton(
                        r4, text=mode_lbl,
                        variable=self._account_mode_var, value=mode_val,
                        font=F_LABEL, bg=PALETTE["card"],
                        fg=PALETTE["text"],
                        selectcolor=PALETTE["card2"],
                        activebackground=PALETTE["card"]
                    ).pack(side=tk.LEFT, padx=(0, 8))

                r5 = _row(card)
                tk.Label(r5, text="계정 전환 딜레이", width=16, anchor=tk.W,
                         font=F_LABEL, bg=PALETTE["card"], fg=PALETTE["text"]
                         ).pack(side=tk.LEFT)
                self._account_sw_delay = tk.StringVar(
                    value=str(self._cur("account_switch_delay", 1.0)))
                _field(r5, "전환(s)", self._account_sw_delay)

                # 더미 변수: API 전용 키 (저장 시 기본값 유지)
                self._tg_api_connect_delay = tk.StringVar(value="2.0")
                self._tg_api_retry_delay   = tk.StringVar(value="5.0")
                self._tg_api_before_send   = tk.StringVar(value="0.5")
                self._tg_api_after_send    = tk.StringVar(value="1.0")
                self._tg_api_capture_delay = tk.StringVar(value="2.0")
                self._tg_api_capture_msgs  = tk.StringVar(value="5")
                self._tg_api_capture_on    = tk.BooleanVar(value=False)
                self._tg_api_acct_warmup   = tk.StringVar(value="0.5")
                self._tg_pre_check_acct    = tk.BooleanVar(value=True)
                self._tg_pre_check_perm    = tk.BooleanVar(value=True)

                tk.Frame(card, bg=PALETTE["card"], height=4).pack()

    # ── 그리드 좌표 자동 계산 섹션 ──────────────────────────
    def _render_grid_section(self):
        """카카오 채팅 타일 그리드 좌표 자동 계산 (오픈채팅/가망뿌리기)"""
        for w in self._grid_section_wrap.winfo_children():
            w.destroy()

        wk = self._wtype_var.get()
        if wk != "kakao_openchat":
            return

        tk.Label(self._grid_section_wrap,
                 text="🎯 좌표 자동 계산",
                 font=F_HEAD,
                 bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(anchor=tk.W, pady=(0, 6))
        tk.Label(self._grid_section_wrap,
                 text="시작 좌표 + 셀 크기 + 구성 입력 → ↺ 계산 클릭",
                 font=F_SMALL,
                 bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(anchor=tk.W, pady=(0, 4))

        card = tk.Frame(self._grid_section_wrap,
                        bg=PALETTE["card"],
                        highlightbackground=PALETTE["border"],
                        highlightthickness=1)
        card.pack(fill=tk.X)

        grid_cfg = self._cur("grid_config", {})

        # ── 시작 좌표 ─────────────────────────────────────
        r0 = tk.Frame(card, bg=PALETTE["card"])
        r0.pack(fill=tk.X, padx=12, pady=(10, 4))
        tk.Label(r0, text="시작 좌표", width=16, anchor=tk.W,
                 font=F_LABEL,
                 bg=PALETTE["card"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        self._grid_sx = tk.StringVar(value=str(grid_cfg.get("start_x", 0)))
        self._grid_sy = tk.StringVar(value=str(grid_cfg.get("start_y", 0)))
        for lbl_t, var in [("X:", self._grid_sx), ("Y:", self._grid_sy)]:
            tk.Label(r0, text=lbl_t, font=F_MONO_S,
                     bg=PALETTE["card"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT, padx=(4, 0))
            tk.Entry(r0, textvariable=var, width=7,
                     bg=PALETTE["card2"], fg=PALETTE["text"],
                     insertbackground=PALETTE["text"],
                     relief=tk.FLAT, font=F_MONO
                     ).pack(side=tk.LEFT)
        self._grid_sx_disp = tk.Label(r0, text="",
            font=F_MONO_S, bg=PALETTE["card"], fg=PALETTE["success_text"])
        self._grid_sx_disp.pack(side=tk.LEFT, padx=(6, 0))
        tk.Button(r0, text="📸 캡처",
                  command=lambda: self._capture_point(
                      "grid_start", self._grid_sx, self._grid_sy,
                      self._grid_sx_disp),
                  bg=PALETTE["primary2"], fg="#FFFFFF",
                  relief=tk.FLAT, font=F_SMALL,
                  cursor="hand2", padx=8, pady=3, bd=0
                  ).pack(side=tk.LEFT, padx=(8, 0))

        # ── 셀 크기 ────────────────────────────────────────
        r1 = tk.Frame(card, bg=PALETTE["card"])
        r1.pack(fill=tk.X, padx=12, pady=4)
        tk.Label(r1, text="1칸 크기", width=16, anchor=tk.W,
                 font=F_LABEL,
                 bg=PALETTE["card"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        self._grid_cw = tk.StringVar(
            value=str(grid_cfg.get("cell_width",  46)))   # v1.52: 카카오 플로팅 접힘 기본 46px
        self._grid_ch = tk.StringVar(
            value=str(grid_cfg.get("cell_height", 38)))   # v1.52: 카카오 플로팅 세로 실측 38px
        for lbl_t, var in [("가로(열간격):", self._grid_cw),
                           ("세로:", self._grid_ch)]:
            tk.Label(r1, text=lbl_t, font=F_SMALL,
                     bg=PALETTE["card"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT, padx=(6, 2))
            tk.Entry(r1, textvariable=var, width=6,
                     bg=PALETTE["card2"], fg=PALETTE["text"],
                     insertbackground=PALETTE["text"],
                     relief=tk.FLAT, font=F_MONO
                     ).pack(side=tk.LEFT)
        tk.Label(r1, text="px", font=F_SMALL,
                 bg=PALETTE["card"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT, padx=(4, 0))

        # ── 구성 (열·행) ──────────────────────────────────── v1.52
        r2 = tk.Frame(card, bg=PALETTE["card"])
        r2.pack(fill=tk.X, padx=12, pady=4)
        tk.Label(r2, text="구성", width=16, anchor=tk.W,
                 font=F_LABEL,
                 bg=PALETTE["card"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        self._grid_col = tk.StringVar(value=str(grid_cfg.get("column_count", 1)))
        self._grid_row = tk.StringVar(value=str(grid_cfg.get("row_count",    1)))
        # v1.52: column_gap 입력란 제거, cell_width(가로) 값을 열 간격으로 사용
        # 하위호환: 저장된 column_gap이 있으면 표시
        for lbl_t, var in [
            ("열",  self._grid_col),
            ("행",  self._grid_row),
        ]:
            tk.Label(r2, text=lbl_t, font=F_SMALL,
                     bg=PALETTE["card"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT, padx=(6, 2))
            tk.Entry(r2, textvariable=var, width=6,
                     bg=PALETTE["card2"], fg=PALETTE["text"],
                     insertbackground=PALETTE["text"],
                     relief=tk.FLAT, font=F_MONO
                     ).pack(side=tk.LEFT)
        tk.Label(r2,
                 text="  (열×행 = 총 방 수, 제한 없음)",
                 font=F_SMALL, bg=PALETTE["card"], fg=PALETTE["muted"]
                 ).pack(side=tk.LEFT, padx=(8, 0))

        # ── 스캔 방향 ──────────────────────────────────────
        r3 = tk.Frame(card, bg=PALETTE["card"])
        r3.pack(fill=tk.X, padx=12, pady=4)
        tk.Label(r3, text="방향", width=16, anchor=tk.W,
                 font=F_LABEL,
                 bg=PALETTE["card"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        self._grid_scan = tk.StringVar(
            value=grid_cfg.get("scan_dir", "col"))
        for val, lbl_t in [("col", "열 우선 (↓→)"),
                           ("row", "행 우선 (→↓)")]:
            tk.Radiobutton(r3, text=lbl_t, value=val,
                           variable=self._grid_scan,
                           bg=PALETTE["card"], fg=PALETTE["text"],
                           selectcolor=PALETTE["active"],
                           activebackground=PALETTE["card"],
                           font=F_LABEL,
                           command=self._update_grid_preview
                           ).pack(side=tk.LEFT, padx=(0, 16))

        # ── 미리보기 ───────────────────────────────────────
        r4 = tk.Frame(card, bg=PALETTE["card"])
        r4.pack(fill=tk.X, padx=12, pady=(4, 10))
        tk.Label(r4, text="미리보기", width=16, anchor=tk.W,
                 font=F_LABEL,
                 bg=PALETTE["card"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        self._grid_preview_lbl = tk.Label(
            r4, text="",
            font=F_MONO,
            bg=PALETTE["card"], fg=PALETTE["success_text"])
        self._grid_preview_lbl.pack(side=tk.LEFT)
        tk.Button(r4, text="↺ 계산",
                  command=self._update_grid_preview,
                  bg=PALETTE["primary2"], fg="#FFFFFF",
                  relief=tk.FLAT, font=F_SMALL,
                  cursor="hand2", padx=8, pady=3, bd=0
                  ).pack(side=tk.LEFT, padx=(8, 0))


        for v in (self._grid_cw, self._grid_ch, self._grid_col, self._grid_row):
            v.trace_add("write", lambda *_: self._update_grid_preview())
        self._update_grid_preview()

    def _update_grid_preview(self):
        """그리드 좌표 계산 미리보기 갱신  [v1.52: cell_width 기준, 미리보기 개선]"""
        try:
            sx  = safe_int  (self._grid_sx.get(),  0)
            sy  = safe_int  (self._grid_sy.get(),  0)
            cw  = safe_float(self._grid_cw.get(),  0.0)   # cell_width = 열 간격
            ch  = safe_float(self._grid_ch.get(),  0.0)   # 세로 슬롯 크기
            col = safe_int  (self._grid_col.get(), 1)
            row = safe_int  (self._grid_row.get(), 1)
            sd  = self._grid_scan.get()
            # v1.52: cell_width를 column_gap 역할로 사용
            coords = calculate_coordinates(sx, sy, ch, col, row, cw, sd)
            total  = len(coords)
            if total == 0:
                self._grid_preview_lbl.config(text="(0개)")
                return
            # 첫 좌표 + 마지막 좌표 + 총 개수 표시
            first = f"({coords[0][0]},{coords[0][1]})"
            last  = f"({coords[-1][0]},{coords[-1][1]})"
            if total == 1:
                preview = f"{first}  (총 {total}개)"
            else:
                preview = f"{first} ~ {last}  (총 {total}개 / {col}열×{row}행)"
            self._grid_preview_lbl.config(text=preview)
        except Exception:
            pass

    # ── 전송·닫기 방식 선택 섹션 ─────────────────────────────
    def _render_send_close_section(self):
        """전송/닫기 방식 선택 (카카오 메시지, 오픈채팅 전용)"""
        for w in self._sc_section_wrap.winfo_children():
            w.destroy()

        wk = self._wtype_var.get()
        if wk not in ("kakao_openchat", "telegram_message"):
            return

        tk.Label(self._sc_section_wrap,
                 text="⚙️ 메시지 입력 · 전송 · 닫기 방식",
                 font=F_HEAD,
                 bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(anchor=tk.W, pady=(0, 6))

        card = tk.Frame(self._sc_section_wrap,
                        bg=PALETTE["card"],
                        highlightbackground=PALETTE["border"],
                        highlightthickness=1)
        card.pack(fill=tk.X)

        def row(label, widget_fn):
            r = tk.Frame(card, bg=PALETTE["card"])
            r.pack(fill=tk.X, padx=12, pady=8)
            tk.Label(r, text=label, width=16, anchor=tk.W,
                     font=F_LABEL,
                     bg=PALETTE["card"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT)
            widget_fn(r)

        def sep():
            tk.Frame(card, bg=PALETTE["border"], height=1
                     ).pack(fill=tk.X, padx=12, pady=2)

        # ════════════════════════════════════════
        # ① 메시지 입력 방식
        #    카카오: message_input_coord (coords 하위)
        #    텔레그램: tg_message_input_coord (tmpl 최상위)  ← 완전 분리
        # ════════════════════════════════════════
        _is_tg_sc = wk in ("telegram_message", "telegram_join_and_message")

        if not _is_tg_sc:
            # ── 카카오 전용: 바로입력 / 좌표클릭 ──────────────
            self._input_method_var = tk.StringVar(
                value=self._cur("input_method", "direct"))

            self._sc_mi_x = tk.StringVar(
                value=str(self._cur("message_input_coord", {}).get("x", 0)))
            self._sc_mi_y = tk.StringVar(
                value=str(self._cur("message_input_coord", {}).get("y", 0)))

            r_mi_coord = tk.Frame(card, bg=PALETTE["card"])
            tk.Label(r_mi_coord, text="입력창 좌표", width=16, anchor=tk.W,
                     font=F_LABEL, bg=PALETTE["card"],
                     fg=PALETTE["accent"]).pack(side=tk.LEFT)
            for lbl_t, var in [("X:", self._sc_mi_x), ("Y:", self._sc_mi_y)]:
                tk.Label(r_mi_coord, text=lbl_t, font=F_MONO_S,
                         bg=PALETTE["card"], fg=PALETTE["text"]
                         ).pack(side=tk.LEFT, padx=(4, 0))
                tk.Entry(r_mi_coord, textvariable=var, width=6,
                         bg=PALETTE["card2"], fg=PALETTE["text"],
                         insertbackground=PALETTE["text"],
                         relief=tk.FLAT, font=F_MONO
                         ).pack(side=tk.LEFT)
            self._sc_mi_disp = tk.Label(r_mi_coord, text="",
                font=F_MONO_S, bg=PALETTE["card"], fg=PALETTE["success_text"])
            self._sc_mi_disp.pack(side=tk.LEFT, padx=(6, 0))
            tk.Button(r_mi_coord, text="📸 캡처",
                      command=lambda: self._capture_point(
                          "message_input_coord",
                          self._sc_mi_x, self._sc_mi_y,
                          self._sc_mi_disp),
                      bg=PALETTE["accent"], fg="#FFFFFF",
                      relief=tk.FLAT, font=F_SMALL,
                      cursor="hand2", padx=8, pady=3, bd=0
                      ).pack(side=tk.LEFT, padx=(8, 0))
            tk.Label(r_mi_coord, text=" ← 좌표클릭 선택 시 필수",
                     font=F_SMALL, bg=PALETTE["card"],
                     fg=PALETTE["warning_text"]
                     ).pack(side=tk.LEFT, padx=(4, 0))

            def _toggle_mi_coord(*_):
                if self._input_method_var.get() == "coord":
                    r_mi_coord.pack(fill=tk.X, padx=12, pady=(0, 6))
                else:
                    r_mi_coord.pack_forget()

            def _input_w(p):
                for val, lbl, hint in [
                    ("direct", "⚡ 바로입력",  "채팅창 열리면 포커스 자동"),
                    ("coord",  "🖱️ 좌표클릭", "입력창 좌표 직접 클릭"),
                ]:
                    tk.Radiobutton(
                        p, text=lbl,
                        variable=self._input_method_var,
                        value=val,
                        command=_toggle_mi_coord,
                        bg=PALETTE["card"], fg=PALETTE["text"],
                        selectcolor=PALETTE["active"],
                        activebackground=PALETTE["card"],
                        font=F_LABEL,
                    ).pack(side=tk.LEFT, padx=(0, 4))
                    tk.Label(p, text=f"({hint})",
                             font=F_SMALL, bg=PALETTE["card"],
                             fg=PALETTE["muted"]
                             ).pack(side=tk.LEFT, padx=(0, 14))
            row("입력 방식", _input_w)
            _toggle_mi_coord()

        else:
            # ── 텔레그램 전용: 입력창 좌표 (tg_message_input_coord) ──
            # 바로입력 / 좌표클릭 동일하게 제공하되 저장 키가 다름
            self._tg_input_method_var = tk.StringVar(
                value=self._cur("tg_input_method", "direct"))

            self._tg_mi_x = tk.StringVar(
                value=str(self._cur("tg_message_input_coord", {}).get("x", 0)))
            self._tg_mi_y = tk.StringVar(
                value=str(self._cur("tg_message_input_coord", {}).get("y", 0)))

            r_tg_mi = tk.Frame(card, bg=PALETTE["card"])
            tk.Label(r_tg_mi, text="입력창 좌표", width=16, anchor=tk.W,
                     font=F_LABEL, bg=PALETTE["card"],
                     fg=PALETTE["accent"]).pack(side=tk.LEFT)
            for lbl_t, var in [("X:", self._tg_mi_x), ("Y:", self._tg_mi_y)]:
                tk.Label(r_tg_mi, text=lbl_t, font=F_MONO_S,
                         bg=PALETTE["card"], fg=PALETTE["text"]
                         ).pack(side=tk.LEFT, padx=(4, 0))
                tk.Entry(r_tg_mi, textvariable=var, width=6,
                         bg=PALETTE["card2"], fg=PALETTE["text"],
                         insertbackground=PALETTE["text"],
                         relief=tk.FLAT, font=F_MONO
                         ).pack(side=tk.LEFT)
            self._tg_mi_disp = tk.Label(r_tg_mi, text="",
                font=F_MONO_S, bg=PALETTE["card"], fg=PALETTE["success_text"])
            self._tg_mi_disp.pack(side=tk.LEFT, padx=(6, 0))
            tk.Button(r_tg_mi, text="📸 캡처",
                      command=lambda: self._capture_point(
                          "tg_message_input_coord",
                          self._tg_mi_x, self._tg_mi_y,
                          self._tg_mi_disp),
                      bg=PALETTE["accent"], fg="#FFFFFF",
                      relief=tk.FLAT, font=F_SMALL,
                      cursor="hand2", padx=8, pady=3, bd=0
                      ).pack(side=tk.LEFT, padx=(8, 0))
            tk.Label(r_tg_mi, text=" ← 좌표클릭 선택 시 필수",
                     font=F_SMALL, bg=PALETTE["card"],
                     fg=PALETTE["warning_text"]
                     ).pack(side=tk.LEFT, padx=(4, 0))

            def _toggle_tg_mi_coord(*_):
                if self._tg_input_method_var.get() == "coord":
                    r_tg_mi.pack(fill=tk.X, padx=12, pady=(0, 6))
                else:
                    r_tg_mi.pack_forget()

            def _tg_input_w(p):
                for val, lbl, hint in [
                    ("direct", "⚡ 바로입력",  "링크 열리면 포커스 자동"),
                    ("coord",  "🖱️ 좌표클릭", "입력창 좌표 직접 클릭"),
                ]:
                    tk.Radiobutton(
                        p, text=lbl,
                        variable=self._tg_input_method_var,
                        value=val,
                        command=_toggle_tg_mi_coord,
                        bg=PALETTE["card"], fg=PALETTE["text"],
                        selectcolor=PALETTE["active"],
                        activebackground=PALETTE["card"],
                        font=F_LABEL,
                    ).pack(side=tk.LEFT, padx=(0, 4))
                    tk.Label(p, text=f"({hint})",
                             font=F_SMALL, bg=PALETTE["card"],
                             fg=PALETTE["muted"]
                             ).pack(side=tk.LEFT, padx=(0, 14))
            row("입력 방식", _tg_input_w)
            _toggle_tg_mi_coord()

        sep()

        # ════════════════════════════════════════
        # ② 전송 방식
        # ════════════════════════════════════════
        # 전송버튼 좌표 행 — click_btn 선택 시만 표시
        self._sc_send_btn_x = tk.StringVar(
            value=str(self._cur("send_btn_coord", {}).get("x", 0)))
        self._sc_send_btn_y = tk.StringVar(
            value=str(self._cur("send_btn_coord", {}).get("y", 0)))

        r_sbtn = tk.Frame(card, bg=PALETTE["card"])
        tk.Label(r_sbtn, text="전송버튼 좌표", width=16, anchor=tk.W,
                 font=F_LABEL, bg=PALETTE["card"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        for lbl_t, var in [("X:", self._sc_send_btn_x),
                            ("Y:", self._sc_send_btn_y)]:
            tk.Label(r_sbtn, text=lbl_t, font=F_MONO_S,
                     bg=PALETTE["card"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT, padx=(4, 0))
            tk.Entry(r_sbtn, textvariable=var, width=6,
                     bg=PALETTE["card2"], fg=PALETTE["text"],
                     insertbackground=PALETTE["text"],
                     relief=tk.FLAT, font=F_MONO
                     ).pack(side=tk.LEFT)
        self._sc_send_disp = tk.Label(r_sbtn, text="",
            font=F_MONO_S, bg=PALETTE["card"], fg=PALETTE["success_text"])
        self._sc_send_disp.pack(side=tk.LEFT, padx=(6, 0))
        tk.Button(r_sbtn, text="📸 캡처",
                  command=lambda: self._capture_point(
                      "send_btn_coord",
                      self._sc_send_btn_x, self._sc_send_btn_y,
                      self._sc_send_disp),
                  bg=PALETTE["primary2"], fg="#FFFFFF",
                  relief=tk.FLAT, font=F_SMALL,
                  cursor="hand2", padx=8, pady=3, bd=0
                  ).pack(side=tk.LEFT, padx=(8, 0))

        self._send_method_var = tk.StringVar(
            value=self._cur("send_method", "enter"))

        def _toggle_send_coord(*_):
            if self._send_method_var.get() == "click_btn":
                r_sbtn.pack(fill=tk.X, padx=12, pady=(0, 6))
            else:
                r_sbtn.pack_forget()

        def _send_w(p):
            for val, lbl in [("enter",      "⌨️ Enter"),
                              ("ctrl_enter", "⌨️ Ctrl+Enter"),
                              ("click_btn",  "🖱️ 버튼클릭")]:
                tk.Radiobutton(
                    p, text=lbl,
                    variable=self._send_method_var,
                    value=val,
                    command=_toggle_send_coord,
                    bg=PALETTE["card"], fg=PALETTE["text"],
                    selectcolor=PALETTE["active"],
                    activebackground=PALETTE["card"],
                    font=F_LABEL,
                ).pack(side=tk.LEFT, padx=(0, 14))
        row("전송 방식", _send_w)
        _toggle_send_coord()   # 초기 상태 반영

        sep()

        # ════════════════════════════════════════
        # ③ 채팅방 닫기
        # ════════════════════════════════════════
        def _close_after_w(p):
            self._close_after_var = tk.BooleanVar(
                value=self._cur("close_after_send", True))
            tk.Checkbutton(p, text="전송 후 창 닫기",
                           variable=self._close_after_var,
                           bg=PALETTE["card"], fg=PALETTE["text"],
                           selectcolor=PALETTE["active"],
                           activebackground=PALETTE["card"],
                           font=F_LABEL,
                           ).pack(side=tk.LEFT)
        row("닫기 여부", _close_after_w)

        # 닫기버튼 좌표 행 — click_btn 선택 시만 표시
        self._sc_close_btn_x = tk.StringVar(
            value=str(self._cur("close_btn_coord", {}).get("x", 0)))
        self._sc_close_btn_y = tk.StringVar(
            value=str(self._cur("close_btn_coord", {}).get("y", 0)))

        r_cbtn = tk.Frame(card, bg=PALETTE["card"])
        tk.Label(r_cbtn, text="닫기버튼 좌표", width=16, anchor=tk.W,
                 font=F_LABEL, bg=PALETTE["card"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        for lbl_t, var in [("X:", self._sc_close_btn_x),
                            ("Y:", self._sc_close_btn_y)]:
            tk.Label(r_cbtn, text=lbl_t, font=F_MONO_S,
                     bg=PALETTE["card"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT, padx=(4, 0))
            tk.Entry(r_cbtn, textvariable=var, width=6,
                     bg=PALETTE["card2"], fg=PALETTE["text"],
                     insertbackground=PALETTE["text"],
                     relief=tk.FLAT, font=F_MONO
                     ).pack(side=tk.LEFT)
        self._sc_close_disp = tk.Label(r_cbtn, text="",
            font=F_MONO_S, bg=PALETTE["card"], fg=PALETTE["success_text"])
        self._sc_close_disp.pack(side=tk.LEFT, padx=(6, 0))
        tk.Button(r_cbtn, text="📸 캡처",
                  command=lambda: self._capture_point(
                      "close_btn_coord",
                      self._sc_close_btn_x, self._sc_close_btn_y,
                      self._sc_close_disp),
                  bg=PALETTE["primary2"], fg="#FFFFFF",
                  relief=tk.FLAT, font=F_SMALL,
                  cursor="hand2", padx=8, pady=3, bd=0
                  ).pack(side=tk.LEFT, padx=(8, 0))

        # 모든 워크플로우 닫기 기본값 = esc
        self._close_method_var = tk.StringVar(
            value=self._cur("close_method", "esc"))

        def _toggle_close_coord(*_):
            if self._close_method_var.get() == "click_btn":
                r_cbtn.pack(fill=tk.X, padx=12, pady=(0, 8))
            else:
                r_cbtn.pack_forget()

        def _close_w(p):
            # 모든 워크플로우 동일 옵션: ESC / Alt+F4 / 버튼클릭
            _close_opts = [("esc",       "⌨️ ESC"),
                           ("altf4",     "⌨️ Alt+F4"),
                           ("click_btn", "🖱️ 버튼클릭")]
            for val, lbl in _close_opts:
                tk.Radiobutton(
                    p, text=lbl,
                    variable=self._close_method_var,
                    value=val,
                    command=_toggle_close_coord,
                    bg=PALETTE["card"], fg=PALETTE["text"],
                    selectcolor=PALETTE["active"],
                    activebackground=PALETTE["card"],
                    font=F_LABEL,
                ).pack(side=tk.LEFT, padx=(0, 14))
        row("닫기 방식", _close_w)
        _toggle_close_coord()   # 초기 상태 반영

        # ════════════════════════════════════════
        # ④ 가입 후 발송 옵션 (telegram_message 전용)
        # ════════════════════════════════════════
        if wk in ("telegram_message", "telegram_join_and_message"):
            sep()

            # Telethon API 모드 여부 (계정 있으면 API 모드 → 좌표 불필요)
            _is_tg_api_join = (
                HAS_TELETHON
                and bool(load_json(TG_ACCOUNTS_PATH, []))
            )

            # join_first 체크박스
            self._join_first_var = tk.BooleanVar(
                value=self._cur("join_first", False))

            # ── _toggle_jb_coord 먼저 정의 (클로저 순서 버그 방지) ──
            if not _is_tg_api_join:
                # pyautogui 모드 — 좌표 행 show/hide
                self._tg_jb_x = tk.StringVar(
                    value=str(self._cur("join_btn_coord", {}).get("x", 0)))
                self._tg_jb_y = tk.StringVar(
                    value=str(self._cur("join_btn_coord", {}).get("y", 0)))

                r_jb = tk.Frame(card, bg=PALETTE["card"])
                tk.Label(r_jb, text="가입버튼 좌표", width=16, anchor=tk.W,
                         font=F_LABEL, bg=PALETTE["card"],
                         fg=PALETTE["accent"]).pack(side=tk.LEFT)
                for lbl_t, var in [("X:", self._tg_jb_x), ("Y:", self._tg_jb_y)]:
                    tk.Label(r_jb, text=lbl_t, font=F_MONO_S,
                             bg=PALETTE["card"], fg=PALETTE["text"]
                             ).pack(side=tk.LEFT, padx=(4, 0))
                    tk.Entry(r_jb, textvariable=var, width=6,
                             bg=PALETTE["card2"], fg=PALETTE["text"],
                             insertbackground=PALETTE["text"],
                             relief=tk.FLAT, font=F_MONO
                             ).pack(side=tk.LEFT)
                self._tg_jb_disp = tk.Label(r_jb, text="",
                    font=F_MONO_S, bg=PALETTE["card"], fg=PALETTE["success_text"])
                self._tg_jb_disp.pack(side=tk.LEFT, padx=(6, 0))
                tk.Button(r_jb, text="📸 캡처",
                          command=lambda: self._capture_point(
                              "join_btn_coord",
                              self._tg_jb_x, self._tg_jb_y,
                              self._tg_jb_disp),
                          bg=PALETTE["accent"], fg="#FFFFFF",
                          relief=tk.FLAT, font=F_SMALL,
                          cursor="hand2", padx=8, pady=3, bd=0
                          ).pack(side=tk.LEFT, padx=(8, 0))
                tk.Label(r_jb, text=" ← 가입 후 발송 체크 시 필수",
                         font=F_SMALL, bg=PALETTE["card"],
                         fg=PALETTE["warning_text"]
                         ).pack(side=tk.LEFT, padx=(4, 0))

                def _toggle_jb_coord(*_):
                    if self._join_first_var.get():
                        r_jb.pack(fill=tk.X, padx=12, pady=(0, 6))
                    else:
                        r_jb.pack_forget()
            else:
                # Telethon API 모드 — 좌표 행 없음, no-op
                def _toggle_jb_coord(*_):
                    pass

            # ── 체크박스 row 생성 (_toggle_jb_coord 정의 이후) ──────
            def _join_first_w(p):
                tk.Checkbutton(p, text="✅ 가입 후 발송",
                               variable=self._join_first_var,
                               command=_toggle_jb_coord,
                               bg=PALETTE["card"], fg=PALETTE["text"],
                               selectcolor=PALETTE["active"],
                               activebackground=PALETTE["card"],
                               font=F_LABEL,
                               ).pack(side=tk.LEFT)
                if _is_tg_api_join:
                    tk.Label(p, text="(Telethon API — 좌표 설정 불필요, 자동 가입 후 발송)",
                             font=F_SMALL, bg=PALETTE["card"],
                             fg=PALETTE["muted"]
                             ).pack(side=tk.LEFT, padx=(6, 0))
                else:
                    tk.Label(p, text="(그룹 링크 열고 가입 버튼 클릭 후 메시지 발송)",
                             font=F_SMALL, bg=PALETTE["card"],
                             fg=PALETTE["muted"]
                             ).pack(side=tk.LEFT, padx=(6, 0))
            row("가입 옵션", _join_first_w)

            # 초기 좌표 행 표시 상태 반영 (pyautogui 모드에서만 의미 있음)
            _toggle_jb_coord()

    # ── 좌표 캡처 — 포인트 ──────────────────────────────────
    def _capture_point(self, key, xv, yv, disp_lbl, disp_wrap=None):
        """3초 카운트다운 후 마우스 좌표 캡처 (오버레이 없음)"""
        if not HAS_PYAUTOGUI:
            messagebox.showwarning("패키지 없음",
                "pyautogui 가 설치되지 않았습니다.")
            return

        def _do_capture():
            for i in range(3, 0, -1):
                self.app._set_status(f"⏳ [{key}] {i}초 후 캡처…")
                time.sleep(1)
            try:
                x, y = pyautogui.position()
                xv.set(str(x)); yv.set(str(y))
                if disp_lbl:
                    # 캡처 성공: 연초록 배경 + 굵은 좌표 표시
                    # x, y를 기본인자로 캡처해야 람다 클로저 버그 방지
                    self.after(0, lambda _x=x, _y=y, _d=disp_lbl: _d.config(
                        text=f"✓ ({_x}, {_y})",
                        bg="#ECFDF5", fg="#065F46"))
                    if disp_wrap:
                        self.after(0, lambda _dw=disp_wrap: _dw.config(bg="#ECFDF5"))
                self.app._set_status(f"✅ [{key}] 캡처: ({x}, {y})")
            except Exception as ex:
                messagebox.showerror("캡처 실패", str(ex))

        import threading as _th
        _th.Thread(target=_do_capture, daemon=True).start()
    # ── 좌표 캡처 — 영역 드래그 ─────────────────────────────
    def _capture_area(self, key: str, vars_: dict):
        if not HAS_PYAUTOGUI:
            messagebox.showwarning("패키지 없음",
                "pyautogui 가 설치되지 않았습니다.")
            return
        # 전체화면 반투명 오버레이
        sel = tk.Toplevel(self)
        sel.overrideredirect(True)
        sel.attributes("-topmost", True)
        sel.attributes("-alpha", 0.30)
        sel.configure(bg="black")
        sw = sel.winfo_screenwidth()
        sh = sel.winfo_screenheight()
        sel.geometry(f"{sw}x{sh}+0+0")

        canvas = tk.Canvas(sel, bg="black",
                           cursor="crosshair",
                           highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_text(
            sw//2, 30,
            text=f"[{key}]  드래그하여 OCR 영역 선택  (ESC=취소)",
            fill="white",
            font=F_HEAD)

        start  = [0, 0]
        rect_id = [None]

        def on_press(e):
            start[0], start[1] = e.x, e.y
            if rect_id[0]:
                canvas.delete(rect_id[0])
            rect_id[0] = canvas.create_rectangle(
                e.x, e.y, e.x, e.y,
                outline=PALETTE["primary"],
                width=2, fill="")

        def on_drag(e):
            if rect_id[0]:
                canvas.coords(
                    rect_id[0],
                    start[0], start[1], e.x, e.y)

        def on_release(e):
            x1 = min(start[0], e.x)
            y1 = min(start[1], e.y)
            x2 = max(start[0], e.x)
            y2 = max(start[1], e.y)
            sel.destroy()
            vars_["x1"].set(str(x1))
            vars_["y1"].set(str(y1))
            vars_["x2"].set(str(x2))
            vars_["y2"].set(str(y2))
            self.app._set_status(
                f"✅ [{key}] 영역: ({x1},{y1})-({x2},{y2})")

        canvas.bind("<ButtonPress-1>",   on_press)
        canvas.bind("<B1-Motion>",       on_drag)
        canvas.bind("<ButtonRelease-1>", on_release)
        canvas.bind("<Escape>",          lambda e: sel.destroy())
        canvas.focus_set()

    # ── 템플릿 저장 ──────────────────────────────────────────
    def _save_template(self):
        name = self._name_var.get().strip()
        if not name:
            messagebox.showwarning("입력 오류",
                "템플릿명을 입력하세요.")
            return

        wk   = self._wtype_var.get()
        wdef = PLATFORM_WORKFLOWS.get(wk, {})

        # 좌표 수집
        coords = {}
        for cr in self._coord_rows:
            k = cr["key"]
            if cr["type"] == "area":
                coords[k] = {
                    "x1": safe_int(cr["vars"]["x1"].get()),
                    "y1": safe_int(cr["vars"]["y1"].get()),
                    "x2": safe_int(cr["vars"]["x2"].get()),
                    "y2": safe_int(cr["vars"]["y2"].get()),
                }
            else:
                coords[k] = {
                    "x": safe_int(cr["xv"].get()),
                    "y": safe_int(cr["yv"].get()),
                }

        # 메시지 텍스트 수집
        message_text = ""
        if hasattr(self, "_msg_text"):
            try:
                message_text = self._msg_text.get(
                    "1.0", tk.END).strip()
            except Exception:
                pass

        # 대상 CSV 경로 수집
        target_file = ""
        if hasattr(self, "_tgt_path_var"):
            target_file = self._tgt_path_var.get().strip()

        # 직접 입력 모드 저장
        target_mode   = "csv"
        target_direct = ""
        if hasattr(self, "_tgt_mode_var"):
            target_mode = self._tgt_mode_var.get()
        if hasattr(self, "_tgt_direct_text"):
            try:
                target_direct = self._tgt_direct_text.get(
                    "1.0", tk.END).strip()
            except Exception:
                pass

        data = {
            "name":          name,
            "platform":      self._platform_var.get(),
            "workflow":      wk,
            "coords":        coords,
            "target_file":   target_file,
            "target_mode":   target_mode,
            "target_direct": target_direct,
            "message":       message_text,
        }

        # 이미지 설정
        if wdef.get("needs_image", False):
            data["use_image"]   = self._use_image_var.get()
            data["image_mode"]  = self._img_mode_var.get() \
                                  if hasattr(self, "_img_mode_var") else "file"
            data["image_path"]  = self._img_path_var.get().strip()
            # 이미지 첨부 순서 (before / after)
            if hasattr(self, "_img_order_var"):
                data["img_order"] = self._img_order_var.get()
            # 이미지 소스/드롭 좌표
            if hasattr(self, "_img_src_x"):
                data["image_source_coord"] = {
                    "x": safe_int(self._img_src_x.get()),
                    "y": safe_int(self._img_src_y.get()),
                }
            if hasattr(self, "_img_drop_x"):
                data["image_drop_coord"] = {
                    "x": safe_int(self._img_drop_x.get()),
                    "y": safe_int(self._img_drop_y.get()),
                }
            # 드래그앤드롭 딜레이
            if hasattr(self, "_img_d_click"):
                data["image_delays"] = {
                    # 드래그앤드롭 딜레이 (Kakao)
                    "after_image_click": safe_float(self._img_d_click.get(), 0.5),
                    "after_drag_start":  safe_float(self._img_d_drag.get(),  0.2),
                    "after_drop":        safe_float(self._img_d_drop.get(),  0.3),
                    "after_enter":       safe_float(self._img_d_enter.get(), 0.5),
                    # 클립보드 딜레이
                    "cb_after_paste": safe_float(
                        getattr(self, "_img_d_cb_paste", type("", (), {"get": lambda s: "0.5"})()).get(), 0.5),
                    "cb_after_send":  safe_float(
                        getattr(self, "_img_d_cb_send",  type("", (), {"get": lambda s: "0.5"})()).get(), 0.5),
                    # 파일경로 딜레이
                    "file_dialog_open": safe_float(
                        getattr(self, "_img_d_file_dialog", type("", (), {"get": lambda s: "1.0"})()).get(), 1.0),
                    "file_folder_move": safe_float(
                        getattr(self, "_img_d_file_folder", type("", (), {"get": lambda s: "0.8"})()).get(), 0.8),
                    "file_after_open":  safe_float(
                        getattr(self, "_img_d_file_open",   type("", (), {"get": lambda s: "0.5"})()).get(), 0.5),
                }

        # ── 워크플로우별 완전 분리 저장 ──────────────────────
        if wk == "kakao_friend":
            # ▶ kakao_friend 전용 설정만 저장
            if hasattr(self, "_rename_existing_var"):
                data["rename_existing"] = self._rename_existing_var.get()
            if hasattr(self, "_id_keyword_var"):
                data["id_keyword"]   = self._id_keyword_var.get().strip()
            if hasattr(self, "_id_start_var"):
                data["id_start_num"] = safe_int(self._id_start_var.get(), 1)
            if hasattr(self, "_id_digits_var"):
                data["id_digits"]    = safe_int(self._id_digits_var.get(), 0)
            if hasattr(self, "_kf_after_ctrlA"):
                data["after_ctrlA"]      = safe_float(self._kf_after_ctrlA.get(),      2.0)
                data["after_click"]      = safe_float(self._kf_after_click.get(),      1.5)
                data["after_input"]      = safe_float(self._kf_after_input.get(),      2.5)
                data["after_color_wait"] = safe_float(self._kf_after_color_wait.get(), 0.6)
                data["after_tab"]        = safe_float(self._kf_after_tab.get(),        0.5)
            if hasattr(self, "_kf_between_var"):
                data["between_chats"]  = safe_float(self._kf_between_var.get(), 1.0)
            if hasattr(self, "_kf_jitter_var"):
                data["between_jitter"] = safe_float(self._kf_jitter_var.get(),  0.3)

        if wk == "kakao_openchat":  # needs_image 블록과 독립 (elif → if)
            # ▶ kakao_openchat 전용 단계별 딜레이 저장 (v1.52: oc_ 접두사)
            if hasattr(self, "_oc_after_open"):
                data["oc_after_open"]  = safe_float(self._oc_after_open.get(),  1.5)
            if hasattr(self, "_oc_after_click"):
                data["oc_after_click"] = safe_float(self._oc_after_click.get(), 0.3)
            if hasattr(self, "_oc_after_type"):
                data["oc_after_type"]  = safe_float(self._oc_after_type.get(),  0.3)
            if hasattr(self, "_oc_after_send"):
                data["oc_after_send"]  = safe_float(self._oc_after_send.get(),  1.0)
            if hasattr(self, "_oc_after_close"):
                data["oc_after_close"] = safe_float(self._oc_after_close.get(), 0.8)
            if hasattr(self, "_between_chats_var"):
                data["between_chats"]  = safe_float(self._between_chats_var.get(), 0.5)
            if hasattr(self, "_jitter_val_var"):
                data["between_jitter"] = safe_float(self._jitter_val_var.get(),    0.3)
            # 그리드 좌표 설정 (v1.52: column_gap = cell_width 로 동기화 저장)
            if hasattr(self, "_grid_sx"):
                cw_val = safe_float(self._grid_cw.get())
                data["grid_config"] = {
                    "start_x":      safe_int  (self._grid_sx.get()),
                    "start_y":      safe_int  (self._grid_sy.get()),
                    "cell_width":   cw_val,                              # 열 간격 = 가로 슬롯
                    "cell_height":  safe_float(self._grid_ch.get()),
                    "column_count": safe_int  (self._grid_col.get(), 1),
                    "row_count":    safe_int  (self._grid_row.get(), 1),
                    "column_gap":   cw_val,                              # 하위호환용 동기화
                    "scan_dir":     self._grid_scan.get(),
                }
            # 전송/닫기 방식 설정
            if hasattr(self, "_input_method_var"):
                data["input_method"]     = self._input_method_var.get()
            if hasattr(self, "_send_method_var"):
                data["send_method"]      = self._send_method_var.get()
            if hasattr(self, "_close_after_var"):
                data["close_after_send"] = self._close_after_var.get()
            if hasattr(self, "_close_method_var"):
                data["close_method"]     = self._close_method_var.get()
            if hasattr(self, "_sc_send_btn_x"):
                data["send_btn_coord"] = {
                    "x": safe_int(self._sc_send_btn_x.get()),
                    "y": safe_int(self._sc_send_btn_y.get()),
                }
            if hasattr(self, "_sc_close_btn_x"):
                data["close_btn_coord"] = {
                    "x": safe_int(self._sc_close_btn_x.get()),
                    "y": safe_int(self._sc_close_btn_y.get()),
                }
            if hasattr(self, "_sc_mi_x"):
                data["message_input_coord"] = {
                    "x": safe_int(self._sc_mi_x.get()),
                    "y": safe_int(self._sc_mi_y.get()),
                }
            # chat_open_coord 제거됨 (grid_config 시작좌표로 대체)

        if wk not in ("kakao_friend", "kakao_openchat"):  # 텔레그램 계열 — kakao_friend/kakao_openchat 과 독립
            # ▶ 텔레그램 계열 딜레이 저장 — 각 변수를 개별 hasattr 로 체크 (일부만 생성된 경우 대비)
            _tg_delay_map = [
                ("_tg_chrome_load",  "tg_chrome_load",   2.0),
                ("_tg_tg_open",      "tg_telegram_open", 1.5),
                ("_tg_join_click",   "tg_join_click",    2.0),
                ("_tg_after_type",   "tg_after_type",    0.5),
                ("_tg_after_send",   "tg_after_send",    1.0),
                ("_tg_after_back",   "tg_after_back",    0.8),
                ("_tg_between_min",  "tg_between_min",   3.0),
                ("_tg_between_max",  "tg_between_max",   7.0),
            ]
            for _attr, _key, _default in _tg_delay_map:
                if hasattr(self, _attr):
                    data[_key] = safe_float(getattr(self, _attr).get(), _default)
            # ▶ Telethon API 전용 딜레이 저장
            _tg_api_delay_map = [
                ("_tg_api_connect_delay", "tg_api_connect_delay", 2.0),
                ("_tg_api_retry_delay",   "tg_api_retry_delay",   5.0),
                ("_tg_api_before_send",   "tg_api_before_send",   0.5),
                ("_tg_api_after_send",    "tg_api_after_send",    1.0),
                ("_tg_api_capture_delay", "tg_api_capture_delay", 2.0),
                ("_tg_api_capture_msgs",  "tg_api_capture_msgs",  5),
                ("_tg_api_acct_warmup",   "tg_api_acct_warmup",   0.5),
            ]
            for _attr, _key, _default in _tg_api_delay_map:
                if hasattr(self, _attr):
                    try:
                        data[_key] = safe_float(getattr(self, _attr).get(), _default)
                    except Exception:
                        data[_key] = _default
            if hasattr(self, "_tg_api_capture_on"):
                data["tg_api_capture_on"] = bool(self._tg_api_capture_on.get())
            # ▶ 발송 전 사전 체크 ON/OFF 저장
            if hasattr(self, "_tg_pre_check_acct"):
                data["tg_pre_check_acct"] = bool(self._tg_pre_check_acct.get())
            if hasattr(self, "_tg_pre_check_perm"):
                data["tg_pre_check_perm"] = bool(self._tg_pre_check_perm.get())

            # ▶ Telethon 다계정 모드 저장
            if hasattr(self, "_account_mode_var"):
                data["account_mode"] = self._account_mode_var.get()
            if hasattr(self, "_account_sw_delay"):
                data["account_switch_delay"] = safe_float(
                    self._account_sw_delay.get(), 1.0)
            # ▶ 텔레그램 전송/닫기 방식 저장 (메시지 계열)
            if wk in ("telegram_message", "telegram_join_and_message"):
                if hasattr(self, "_send_method_var"):
                    data["send_method"]      = self._send_method_var.get()
                if hasattr(self, "_close_after_var"):
                    data["close_after_send"] = self._close_after_var.get()
                if hasattr(self, "_close_method_var"):
                    data["close_method"]     = self._close_method_var.get()
                if hasattr(self, "_sc_send_btn_x"):
                    data["send_btn_coord"] = {
                        "x": safe_int(self._sc_send_btn_x.get()),
                        "y": safe_int(self._sc_send_btn_y.get()),
                    }
                if hasattr(self, "_sc_close_btn_x"):
                    data["close_btn_coord"] = {
                        "x": safe_int(self._sc_close_btn_x.get()),
                        "y": safe_int(self._sc_close_btn_y.get()),
                    }
                # ── 텔레그램 전용 좌표 (카카오와 키 분리) ──────────
                if hasattr(self, "_tg_input_method_var"):
                    data["tg_input_method"] = self._tg_input_method_var.get()
                if hasattr(self, "_tg_mi_x"):
                    data["tg_message_input_coord"] = {
                        "x": safe_int(self._tg_mi_x.get()),
                        "y": safe_int(self._tg_mi_y.get()),
                    }
                if hasattr(self, "_tg_attach_x"):
                    data["tg_attach_btn_coord"] = {
                        "x": safe_int(self._tg_attach_x.get()),
                        "y": safe_int(self._tg_attach_y.get()),
                    }
                # join_first 옵션 + join_btn 좌표
                if hasattr(self, "_join_first_var"):
                    data["join_first"] = self._join_first_var.get()
                if hasattr(self, "_tg_jb_x"):
                    data["join_btn_coord"] = {
                        "x": safe_int(self._tg_jb_x.get()),
                        "y": safe_int(self._tg_jb_y.get()),
                    }
                if hasattr(self, "_tg_fname_x"):
                    data["tg_filename_input_coord"] = {
                        "x": safe_int(self._tg_fname_x.get()),
                        "y": safe_int(self._tg_fname_y.get()),
                    }

        # 파일 저장
        fname = name.replace(" ", "_").replace("/", "_") + ".json"
        path  = TEMPLATE_DIR / fname
        if save_json(path, data):
            self.app._set_status(f"✅ 템플릿 [{name}] 저장 완료")
            self._load_templates()
            # 저장 후 해당 항목 재선택
            for i, t in enumerate(self._templates):
                if t.get("name") == name:
                    self._tmpl_lb.selection_clear(0, tk.END)
                    self._tmpl_lb.selection_set(i)
                    self._sel_idx = i
                    break
        else:
            messagebox.showerror("저장 실패",
                "파일 저장 중 오류가 발생했습니다.")

    # ── 템플릿 로드 ──────────────────────────────────────────
    @staticmethod
    def _migrate_template(d: dict) -> dict:
        """구버전 템플릿 키 → 신버전 자동 변환  [v1.52 신규]
        · kakao_openchat: action_delay → oc_after_open / oc_after_send
        · kakao_openchat: grid_config.column_gap → grid_config.cell_width
        · kakao_openchat: 신규 oc_ 키 누락 시 기본값 채움
        파일을 직접 수정하지 않음 (인메모리 변환만 수행)
        """
        wk = d.get("workflow", "")
        if wk == "kakao_openchat":
            # action_delay → oc_after_open / oc_after_send (하위호환 변환)
            old_ad = d.get("action_delay")
            if old_ad is not None:
                if "oc_after_open" not in d:
                    d["oc_after_open"] = old_ad
                if "oc_after_send" not in d:
                    d["oc_after_send"] = old_ad
            # 신규 oc_ 키 기본값 채움
            oc_defaults = {
                "oc_after_open":  1.5,
                "oc_after_click": 0.3,
                "oc_after_type":  0.3,
                "oc_after_send":  1.0,
                "oc_after_close": 0.8,
            }
            for k, v in oc_defaults.items():
                if k not in d:
                    d[k] = v
            # grid_config: column_gap → cell_width (하위호환 변환)
            gc = d.get("grid_config", {})
            if gc and "cell_width" not in gc and "column_gap" in gc:
                gc["cell_width"] = gc["column_gap"]
            # row_count 기본값 보정 (5 → 실제 저장값 유지, 없으면 1)
            if gc and "row_count" not in gc:
                gc["row_count"] = 1
        return d

    def _load_templates(self):
        self._templates = []
        if TEMPLATE_DIR.exists():
            for f in sorted(TEMPLATE_DIR.glob("*.json")):
                d = load_json(f, {})
                if d.get("name"):
                    # ── 구버전 telegram_join_msg → telegram_message 마이그레이션 ──
                    if d.get("workflow") == "telegram_join_msg":
                        d["workflow"]   = "telegram_message"
                        d["join_first"] = True
                        jb = d.get("coords", {}).get("join_btn")
                        if jb and not d.get("join_btn_coord"):
                            d["join_btn_coord"] = jb
                    # ── v1.52 신규: 전체 템플릿 키 마이그레이션 ──
                    d = self._migrate_template(d)
                    d["_file"] = str(f)
                    self._templates.append(d)
        self._refresh_list()

    def _refresh_list(self):
        self._tmpl_lb.delete(0, tk.END)
        for t in self._templates:
            plat = t.get("platform", "")
            icon = "🟡" if plat == "kakao" else "🔵"
            self._tmpl_lb.insert(
                tk.END,
                f"  {icon}  {t.get('name','?')}")
        # 뱃지 업데이트
        if hasattr(self, "_tmpl_count_lbl"):
            cnt = len(self._templates)
            self._tmpl_count_lbl.config(text=str(cnt))

    # ── 리스트 선택 ──────────────────────────────────────────
    def _on_select(self, _event=None):
        sel = self._tmpl_lb.curselection()
        if not sel:
            return
        self._sel_idx = sel[0]
        # 플랫폼/유형 변수 먼저 세팅 후 패널 재렌더링
        t = self._templates[self._sel_idx]
        self._platform_var = tk.StringVar(
            value=t.get("platform", "kakao"))
        self._wtype_var = tk.StringVar(
            value=t.get("workflow", "kakao_friend"))
        self._refresh_edit_panel()

    def _on_dbl_click(self, _event=None):
        """더블클릭 시 템플릿 이름 입력 필드로 포커스 이동 (편집 유도)"""
        # 먼저 선택 처리
        self._on_select()
        # 이름 Entry 위젯이 있으면 포커스 이동 + 짧게 강조 효과
        try:
            if hasattr(self, "_name_entry") and self._name_entry.winfo_exists():
                self._name_entry.focus_set()
                self._name_entry.select_range(0, tk.END)
                # 노란 배경으로 0.5초 강조 (orig_bg를 기본인자로 캡처)
                orig_bg = self._name_entry.cget("bg")
                self._name_entry.config(bg="#FEF9C3")
                self.after(500, lambda bg=orig_bg: self._name_entry.config(bg=bg))
        except Exception:
            pass

    # ── 새 템플릿 ────────────────────────────────────────────
    def _add_template(self):
        self._sel_idx = -1
        self._platform_var = tk.StringVar(value="kakao")
        self._wtype_var    = tk.StringVar(value="kakao_friend")
        self._refresh_edit_panel()
        self._tmpl_lb.selection_clear(0, tk.END)

    # ── 복제 ────────────────────────────────────────────────
    def _dup_template(self):
        sel = self._tmpl_lb.curselection()
        if not sel:
            messagebox.showwarning("선택 없음",
                "복제할 템플릿을 선택하세요.")
            return
        import copy
        t    = copy.deepcopy(self._templates[sel[0]])
        t["name"] = t.get("name", "") + "_복사본"
        if "_file" in t: del t["_file"]
        fname = (t["name"].replace(" ","_")
                          .replace("/","_") + ".json")
        save_json(TEMPLATE_DIR / fname, t)
        self._load_templates()

    # ── 삭제 ────────────────────────────────────────────────
    def _del_template(self):
        sel = self._tmpl_lb.curselection()
        if not sel:
            return
        t = self._templates[sel[0]]
        if not messagebox.askyesno("삭제 확인",
                f"[{t.get('name','')}] 을 삭제할까요?"):
            return
        fpath = t.get("_file")
        if fpath and Path(fpath).exists():
            Path(fpath).unlink()
        self._sel_idx = -1
        self._load_templates()
        self._refresh_edit_panel()

    # ── 도움말 ──────────────────────────────────────────────
    def _show_help(self):
        msg = (
            "📌 작업 템플릿 사용 방법\n\n"
            "① 새 템플릿 버튼 클릭\n"
            "② 플랫폼 선택 (카카오톡 / 텔레그램)\n"
            "③ 작업 유형 선택\n"
            "④ 대상 CSV 파일 선택\n"
            "⑤ 메시지 입력 (변수 {이름} 등 사용 가능)\n"
            "⑥ 좌표를 📸 캡처 버튼으로 등록\n"
            "⑦ 이미지 첨부 필요 시 ON 후 파일 선택\n"
            "⑧ 친구추가는 OCR 영역 설정 (CSV: 카카오아이디 컬럼만 필요)\n"
            "⑨ 💾 템플릿 저장\n\n"
            "저장된 템플릿은 [작업 관리] 탭에서 선택 후\n"
            "스케줄만 설정하면 됩니다."
        )
        messagebox.showinfo("도움말", msg)
# ============================================================
# Block 3-A : App._build_templates_tab 연결 +
#             JobsTab 기본 구조
# ============================================================

# ── App 에 TemplateTab 연결 (monkey-patch) ──────────────────
def _app_build_templates_tab(self, frame: tk.Frame):
    tab = TemplateTab(frame, self)
    tab.pack(fill=tk.BOTH, expand=True)
    self._templates_tab = tab   # 작업 관리에서 참조용

App._build_templates_tab = _app_build_templates_tab


# ============================================================
# JobsTab — 작업 관리
# ============================================================

class JobsTab(tk.Frame):
    """
    작업 = 템플릿 선택 + 대상 목록 + 메시지 + 딜레이 + 스케줄
    기승전결의 '전·결' 파트
    """
    def __init__(self, master, app: "App"):
        super().__init__(master, bg=PALETTE["bg"])
        self.app    = app
        self._jobs: list[dict] = []          # 로드된 작업 목록
        # v1.54 CHANGE-06: _workers/_stop_events dict 제거 → engine + cancelled_jobs 로 교체
        # 이전(v1.53): self._workers: dict[str, Thread] = {}
        #              self._stop_events: dict[str, Event] = {}
        # 변경(v1.54): PostingEngine 이 스레드·stop_event 를 내부 관리
        self._cancelled_jobs: set[str] = set()           # 대기 중 취소 작업명 set
        self._engine = PostingEngine(self._cancelled_jobs)# 큐 기반 단일 워커 엔진
        self._engine.start()                              # daemon worker 스레드 시작
        # ── v1.56 CHANGE-S2: 스케줄러 틱 등록 ──────────────────────────────────────
        # 이전(v1.55): 스케줄러 없음 — schedule_on 데이터 저장만, 자동 실행 불가
        # 변경(v1.56): after(10_000) 으로 UI 로드 완료(약 10초) 후 첫 틱 실행
        #              이후 _scheduler_tick 내부에서 after(30_000) 으로 30초 재예약
        # ── v1.58 CHANGE-X8: 스레드 기반 스케줄러 즉시 시작 (1초 후) ──────────
        self._scheduler_after_id = None          # after-callback ID (cancel 용)
        self._50sec_guard: dict   = {}             # v1.60 BENCH-3: 50초 가드 맵
        # [NEW-BUG-01 fix] self → self.app 전달 (_check_update_on_start 인자는 App 인스턴스)
        self.after(3000, lambda: _check_update_on_start(self.app))  # v1.60 자동업데이터
        self._scheduler_running  = False         # 스레드 중복 방지 플래그
        self.after(1_000, self._start_scheduler)  # 1초 후 첫 스케줄러 시작
        # ── v1.57 CHANGE-W8: _fired_set 초기화 ──────────────────────────────────────
        # 복수 시각(schedule_times) 중복 실행 방지용 set
        # 키 형식: "{job_name}_{YYYY-MM-DD}_{HH:MM}"
        # 틱 시작 시 당일 이전 키 자동 정리 (BUG-05)
        self._fired_set: set = set()
        self._build_ui()
        self._load_jobs()

    # ── 전체 UI ─────────────────────────────────────────────
    def _build_ui(self):
        # ── 탭 헤더 바 ──────────────────────────────────────
        hdr = tk.Frame(self, bg=PALETTE["bg"])
        hdr.pack(fill=tk.X, pady=(0, 10))

        title_f = tk.Frame(hdr, bg=PALETTE["bg"])
        title_f.pack(side=tk.LEFT)
        tk.Label(title_f, text="📋",
                 font=("Segoe UI Emoji", 15),
                 bg=PALETTE["bg"], fg=PALETTE["primary"]
                 ).pack(side=tk.LEFT)
        tk.Label(title_f, text="  작업 관리",
                 font=F_TITLE,
                 bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        tk.Label(title_f,
                 text="  템플릿을 선택하고 스케줄을 설정해 작업을 실행합니다",
                 font=F_SMALL, bg=PALETTE["bg"], fg=PALETTE["muted"]
                 ).pack(side=tk.LEFT)
        tk.Button(hdr, text="❓  도움말",
                  command=self._show_help,
                  bg=PALETTE["card"], fg=PALETTE["text2"],
                  relief=tk.FLAT, font=F_BTN_S,
                  highlightbackground=PALETTE["border"],
                  highlightthickness=1,
                  cursor="hand2", padx=10, pady=4,
                  activebackground=PALETTE["hover"],
                  ).pack(side=tk.RIGHT)

        # 구분선
        tk.Frame(self, bg=PALETTE["border"], height=1
                 ).pack(fill=tk.X, pady=(0, 8))

        # ── 툴바 ─────────────────────────────────────────────
        tb_wrap = tk.Frame(self, bg=PALETTE["card"],
                           highlightbackground=PALETTE["border"],
                           highlightthickness=1)
        tb_wrap.pack(fill=tk.X, pady=(0, 8))
        tb = tk.Frame(tb_wrap, bg=PALETTE["card"])
        tb.pack(fill=tk.X, padx=10, pady=7)

        # 왼쪽: 편집 버튼들
        left_btns = [
            ("＋ 작업 추가", self._add_job,   PALETTE["primary"], "#FFFFFF"),
            ("✎  수정",      self._edit_job,  "#F1F5F9",          PALETTE["text"]),
            ("⧉  복제",      self._dup_job,   "#F1F5F9",          PALETTE["text2"]),
            ("✕  삭제",      self._del_job,   "#FEF2F2",          PALETTE["danger"]),
        ]
        for txt, cmd, bg, fg in left_btns:
            b = tk.Button(tb, text=txt, command=cmd,
                      bg=bg, fg=fg, relief=tk.FLAT,
                      font=(_FF, 9, "bold"),
                      activebackground=_lighten(bg),
                      activeforeground=fg,
                      cursor="hand2", padx=12, pady=6, bd=0)
            b.pack(side=tk.LEFT, padx=(0, 3))
            b.bind("<Enter>", lambda e, b=b, bg=bg: b.config(bg=_lighten(bg)))
            b.bind("<Leave>", lambda e, b=b, bg=bg: b.config(bg=bg))

        # 세로 구분선
        tk.Frame(tb, bg=PALETTE["border2"], width=1, height=26
                 ).pack(side=tk.LEFT, padx=(6, 6), fill=tk.Y)

        # 활성 토글
        b_toggle = tk.Button(tb, text="⊙  활성 토글",
                  command=self._toggle_job,
                  bg="#F8FAFC", fg="#475569",
                  relief=tk.FLAT, font=(_FF, 9, "bold"),
                  cursor="hand2", padx=10, pady=6, bd=0,
                  activebackground="#E2E8F0",
                  activeforeground="#1E293B")
        b_toggle.pack(side=tk.LEFT, padx=(0, 3))

        # 오른쪽: 실행 버튼들
        b_stop = tk.Button(tb, text="⏹  중지",
                  command=lambda: (
                      self._stop_job(self._get_selected_job())
                      if self._get_selected_job()
                      else self._stop_all()),
                  bg=PALETTE["danger"], fg="#FFFFFF",
                  relief=tk.FLAT, font=(_FF, 9, "bold"),
                  cursor="hand2", padx=12, pady=6, bd=0,
                  activebackground=_lighten(PALETTE["danger"]))
        b_stop.pack(side=tk.RIGHT, padx=(3, 0))

        b_run_all = tk.Button(tb, text="▶▶  전체 실행",
                  command=self._run_all,
                  bg=PALETTE["success"], fg="#FFFFFF",
                  relief=tk.FLAT, font=(_FF, 9, "bold"),
                  cursor="hand2", padx=14, pady=6, bd=0,
                  activebackground=_lighten(PALETTE["success"]))
        b_run_all.pack(side=tk.RIGHT, padx=(3, 0))

        b_run_sel = tk.Button(tb, text="▶  선택 실행",
                  command=self._run_selected,
                  bg=PALETTE["primary"], fg="#FFFFFF",
                  relief=tk.FLAT, font=(_FF, 9, "bold"),
                  cursor="hand2", padx=14, pady=6, bd=0,
                  activebackground=PALETTE["primary2"])
        b_run_sel.pack(side=tk.RIGHT, padx=(3, 0))

        # hover 효과
        for b, c in [(b_stop, PALETTE["danger"]),
                     (b_run_all, PALETTE["success"]),
                     (b_run_sel, PALETTE["primary"])]:
            b.bind("<Enter>", lambda e, b=b, c=c: b.config(bg=_lighten(c)))
            b.bind("<Leave>", lambda e, b=b, c=c: b.config(bg=c))

        # 툴팁 등록
        add_tip(b_run_sel, "선택한 작업 1개를 즉시 실행합니다")
        add_tip(b_run_all, "활성화된 모든 작업을 순차적으로 실행합니다")
        add_tip(b_stop,    "현재 실행 중인 작업을 중지합니다 (선택 없으면 전체 중지)")
        add_tip(b_toggle,  "선택한 작업의 활성/비활성 상태를 전환합니다")

        # ── 인라인 팁 카드 ─────────────────────────────────
        tip_frame = tk.Frame(self,
                             bg="#EFF6FF",
                             highlightbackground="#BFDBFE",
                             highlightthickness=1)
        tip_frame.pack(fill=tk.X, pady=(0, 6))
        tk.Label(tip_frame,
                 text=("💡  각 작업 = 템플릿 1개 + 대상 목록 조합   "
                       "·   더블클릭으로 빠른 수정   "
                       "·   ⊙ 활성 토글로 특정 작업 일시 비활성화"),
                 font=F_SMALL,
                 bg="#EFF6FF", fg="#1D4ED8",
                 anchor=tk.W, padx=14, pady=6,
                 ).pack(fill=tk.X)

        # ── 작업 목록 Treeview ──────────────────────────────
        tv_frame = tk.Frame(self,
                            bg=PALETTE["card"],
                            highlightbackground=PALETTE["border"],
                            highlightthickness=1)
        tv_frame.pack(fill=tk.BOTH, expand=True)

        # ── v1.55 CHANGE-A2: "active" 컬럼 추가 ────────────────────────
        # 이전(v1.54): 6개 컬럼 (name/template/platform/workflow/schedule/status)
        # 변경(v1.55): 7번째 "active" 컬럼 추가 → ✓ 활성 / ✗ 비활성 표시
        # v1.62: 8번째 "account" 컬럼 추가 → 지정 텔레 계정 표시
        cols = ("name", "template", "platform", "workflow",
                "schedule", "status", "active", "account")
        self._tv = ttk.Treeview(
            tv_frame, columns=cols,
            show="headings", height=14)

        headers = [
            # (col, 헤더명, 기본너비, 정렬, stretch)
            ("name",     "작업명",    160, tk.W,      True),
            ("template", "템플릿명",  140, tk.W,      True),
            ("platform", "플랫폼",     80, tk.CENTER, False),
            ("workflow", "작업유형",  120, tk.CENTER, False),
            ("schedule", "스케줄",    120, tk.CENTER, False),
            ("status",   "상태",       90, tk.CENTER, False),
            ("active",   "활성",       52, tk.CENTER, False),
            ("account",  "텔레 계정", 130, tk.W,      True),
        ]
        for col, hd, w, anch, strch in headers:
            self._tv.heading(col, text=hd, anchor=anch)
            self._tv.column(col, width=w,
                            anchor=anch, stretch=strch, minwidth=w//2)

        # Treeview 스타일
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background=PALETTE["card"],
                        foreground=PALETTE["text"],
                        rowheight=34,
                        fieldbackground=PALETTE["card"],
                        borderwidth=0,
                        font=(_FF, 9))
        style.configure("Treeview.Heading",
                        background=PALETTE["sidebar"],
                        foreground="#CBD5E1",
                        relief="flat",
                        font=(_FF, 9, "bold"),
                        padding=(8, 8))
        style.map("Treeview",
                  background=[("selected", PALETTE["primary"])],
                  foreground=[("selected", "#FFFFFF")])
        style.layout("Treeview", [
            ("Treeview.treearea", {"sticky": "nswe"})])

        # ── v1.55 CHANGE-A3: 비활성/활성 태그 ───────────────────────────
        self._tv.tag_configure("disabled",
                               foreground=PALETTE["muted"],
                               background="#F8F9FA")
        self._tv.tag_configure("enabled",
                               foreground=PALETTE["text"],
                               background=PALETTE["card"])
        # ── [UI-4] v1.61: 플랫폼별 행 색상 + 실행 상태 색상 ──────────
        # kakao 행: 노란 포인트 (#FEFCE8)
        # telegram 행: 파란 포인트 (#EFF6FF)
        self._tv.tag_configure("kakao",
                               background="#FEFCE8",
                               foreground="#78350F")
        self._tv.tag_configure("telegram",
                               background="#EFF6FF",
                               foreground="#1E3A5F")
        self._tv.tag_configure("running",
                               background="#DBEAFE",
                               foreground="#1D4ED8")
        self._tv.tag_configure("success",
                               background="#F0FDF4",
                               foreground="#15803D")
        self._tv.tag_configure("failed",
                               background="#FEF2F2",
                               foreground="#B91C1C")

        tv_sb = ttk.Scrollbar(tv_frame, orient=tk.VERTICAL,
                              command=self._tv.yview)
        self._tv.configure(yscrollcommand=tv_sb.set)
        tv_sb.pack(side=tk.RIGHT, fill=tk.Y)
        self._tv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._tv.bind("<Double-1>", lambda e: self._edit_job())

        # ── 진행 상태 바 ─────────────────────────────────────
        prog_outer = tk.Frame(self, bg=PALETTE["card"],
                              highlightbackground=PALETTE["border"],
                              highlightthickness=1)
        prog_outer.pack(fill=tk.X, pady=(8, 0))
        prog_frame = tk.Frame(prog_outer, bg=PALETTE["card"])
        prog_frame.pack(fill=tk.X, padx=12, pady=8)

        self._prog_var    = tk.DoubleVar(value=0)
        self._prog_label  = tk.StringVar(value="⏳ 대기 중")
        self._prog_target = tk.StringVar(value="")   # 현재 처리 대상

        # 상태 레이블 (작업상태)
        tk.Label(prog_frame, textvariable=self._prog_label,
                 font=(_FF, 9, "bold"),
                 bg=PALETTE["card"], fg=PALETTE["text2"],
                 width=10, anchor=tk.W,
                 ).pack(side=tk.LEFT, padx=(0, 6))
        # 현재 처리 대상 (계정 → 링크 / 번호)
        tk.Label(prog_frame, textvariable=self._prog_target,
                 font=(_FFM, 8),
                 bg=PALETTE["card"], fg=PALETTE["muted"],
                 anchor=tk.W,
                 ).pack(side=tk.LEFT, padx=(0, 8))

        # 프로그레스 바
        style2 = ttk.Style()
        style2.configure("Jobs.Horizontal.TProgressbar",
                         troughcolor=PALETTE["bg"],
                         background=PALETTE["primary"],
                         bordercolor=PALETTE["border"],
                         lightcolor=PALETTE["primary"],
                         darkcolor=PALETTE["primary2"])
        prog_bar = ttk.Progressbar(
            prog_frame, variable=self._prog_var,
            maximum=100, mode="determinate",
            style="Jobs.Horizontal.TProgressbar")
        prog_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 구분선
        tk.Frame(prog_frame, bg=PALETTE["border2"], width=1, height=20
                 ).pack(side=tk.LEFT, padx=(12, 12), fill=tk.Y)

        # 성공/실패 카운터
        self._succ_var = tk.StringVar(value="✅  0")
        self._fail_var = tk.StringVar(value="❌  0")
        tk.Label(prog_frame, textvariable=self._succ_var,
                 font=(_FF, 9, "bold"),
                 bg=PALETTE["card"],
                 fg="#059669"
                 ).pack(side=tk.LEFT, padx=(0, 8))
        tk.Label(prog_frame, textvariable=self._fail_var,
                 font=(_FF, 9, "bold"),
                 bg=PALETTE["card"],
                 fg=PALETTE["danger"]
                 ).pack(side=tk.LEFT)

        # ── v1.60 STEP-5: ETA 패널 (예상 소요시간 / 예상 완료시각) ─────────────
        eta_outer = tk.Frame(self, bg=PALETTE["card"],
                             highlightbackground=PALETTE["border"],
                             highlightthickness=1)
        eta_outer.pack(fill=tk.X, pady=(4, 0))
        eta_frame = tk.Frame(eta_outer, bg=PALETTE["card"])
        eta_frame.pack(fill=tk.X, padx=12, pady=6)

        self._eta_total_var  = tk.StringVar(value="⏱ 예상 소요: —")
        self._eta_finish_var = tk.StringVar(value="🏁 예상 완료: —")

        tk.Label(eta_frame, textvariable=self._eta_total_var,
                 font=F_SMALL, bg=PALETTE["card"],
                 fg=PALETTE["text2"], anchor=tk.W
                 ).pack(side=tk.LEFT, padx=(0, 20))
        tk.Label(eta_frame, textvariable=self._eta_finish_var,
                 font=F_SMALL, bg=PALETTE["card"],
                 fg=PALETTE["text2"], anchor=tk.W
                 ).pack(side=tk.LEFT)
        self._eta_refresh_btn = tk.Button(
            eta_frame, text="  ↻  새로고침",
            font=(_FF, 8), bg=PALETTE["bg"],
            fg=PALETTE["muted"],
            relief=tk.FLAT, bd=0, cursor="hand2",
            padx=8, pady=2,
            activebackground=PALETTE["hover"],
            command=self._refresh_time_estimate)
        self._eta_refresh_btn.pack(side=tk.RIGHT, padx=(0, 2))
        # ────────────────────────────────────────────────────────

    # ── 작업 로드/저장 ───────────────────────────────────────
    def _refresh_time_estimate(self):
        """v1.60 STEP-6: ETA 패널 갱신 — 전체 소요시간 / 예상 완료시각 계산"""
        try:
            active = [j for j in self._jobs
                      if j.get("schedule_on") and j.get("enabled", True)]
            if not active:
                self._eta_total_var.set("⏱ 예상 소요: -")
                self._eta_finish_var.set("🏁 예상 완료: -")
                return

            cur_name = getattr(self._engine, "_current_name", "")
            eta_list = _calc_queue_eta(self._jobs, cur_name)

            if not eta_list:
                self._eta_total_var.set("⏱ 예상 소요: -")
                self._eta_finish_var.set("🏁 예상 완료: -")
                return

            total_s  = sum(e["dur_s"] for e in eta_list)
            finish   = eta_list[-1]["finish"]
            count    = len(eta_list)

            m, s = divmod(int(total_s), 60)
            h, m = divmod(m, 60)
            if h > 0:
                dur_str = f"{h}시간 {m}분"
            elif m > 0:
                dur_str = f"{m}분 {s}초"
            else:
                dur_str = f"{s}초"

            self._eta_total_var.set(f"⏱ 예상 소요: {dur_str}  ({count}개 작업)")
            self._eta_finish_var.set(f"🏁 예상 완료: {finish.strftime('%H:%M')}")
        except Exception:
            self._eta_total_var.set("⏱ 예상 소요: -")
            self._eta_finish_var.set("🏁 예상 완료: -")

    def _load_jobs(self):
        self._jobs = []
        if JOBS_DIR.exists():
            for f in sorted(JOBS_DIR.glob("*.json")):
                d = load_json(f, {})
                if d.get("name"):
                    d["_file"] = str(f)
                    self._jobs.append(d)
        self._refresh_tv()

        # v1.60 STEP-7: 작업 로드 후 ETA 갱신
        self.after(0, self._refresh_time_estimate)
        # v1.61 SC-4: 앱 시작 시 스케줄 복원
        if hasattr(self, "_restore_scheduler_on_startup"):
            self.after(100, self._restore_scheduler_on_startup)

    def _refresh_tv(self):
        """[v1.61 UI-4] 플랫폼별 행 색상 + 스케줄 상태 아이콘 + 실행 상태 태그 적용
        [v1.62] 텔레 계정 컬럼 추가
        """
        self._tv.delete(*self._tv.get_children())

        # ── v1.62: 계정 이름 조회용 phone→name 매핑 캐시 ─────────────────
        _all_accts = load_json(TG_ACCOUNTS_PATH, [])
        _phone_to_name: dict[str, str] = {
            TelethonEngine._normalize_phone(a.get("phone", "")): a.get("name", "")
            for a in _all_accts if a.get("phone")
        }
        _total_acct_cnt = len(_all_accts)

        for j in self._jobs:
            wk    = j.get("workflow", "")
            wdef  = PLATFORM_WORKFLOWS.get(wk, {})
            plat  = j.get("platform", "")
            icon  = "🟡 카카오" if plat == "kakao" else "🔵 텔레그램"

            # ── 스케줄 상태 아이콘 (v1.61 UI-6) ──────────────────────────
            # ⚪ 스케줄 OFF  ⚫ 비활성  🟢 활성(time모드)  🔵 활성(interval모드)
            sched_on  = j.get("schedule_on", False)
            enabled   = j.get("enabled", True)
            sched_mode= j.get("schedule_mode", "time")
            if not enabled:
                sched_icon = "⚫"
            elif not sched_on:
                sched_icon = "⚪"
            elif sched_mode == "interval":
                sched_icon = "🔵"
            else:
                sched_icon = "🟢"
            sched_times = j.get("schedule_times", [])
            sched_time  = j.get("schedule_time", "")
            if sched_on and sched_times:
                sched_lbl = ",".join(sched_times)
            elif sched_on and sched_time:
                sched_lbl = sched_time
            elif sched_on and sched_mode == "interval":
                sched_lbl = f"매 {j.get('schedule_interval', 24)}시간"
            else:
                sched_lbl = "없음"
            sched = f"{sched_icon} {sched_lbl}"

            # ── v1.69/v1.73: 반복 정보 스케줄 컬럼에 병기 ───────────
            # repeat_on=True 일 때만 표시
            _rc  = j.get("repeat_count", 1)
            _ron = j.get("repeat_on", False)
            if _ron and _rc == 0:
                sched += "  🔁∞"
            elif _ron and _rc > 1:
                sched += f"  🔁{_rc}회"

            stat  = j.get("_status", "대기")

            # ── 태그 결정 (v1.61 UI-4) ───────────────────────────────────
            # 우선순위: running > failed > success > kakao/telegram > disabled
            _run_stat = j.get("_run_status", "")
            if _run_stat == "running":
                row_tag = "running"
            elif _run_stat == "failed":
                row_tag = "failed"
            elif _run_stat == "success":
                row_tag = "success"
            elif not enabled:
                row_tag = "disabled"
            elif plat == "kakao":
                row_tag = "kakao"
            elif plat == "telegram":
                row_tag = "telegram"
            else:
                row_tag = "enabled"

            # ── v1.62: 텔레 계정 표시 ────────────────────────────────────
            # 카카오 작업: "-"
            # 텔레 작업 + assigned_accounts 없음: "전체 N개"
            # 텔레 작업 + assigned_accounts 있음: 이름 나열 (2개 초과 시 "외 N명")
            if plat != "telegram" or not _all_accts:
                acct_txt = "-"
            else:
                assigned = j.get("assigned_accounts", [])
                if not assigned:
                    acct_txt = f"전체 {_total_acct_cnt}개"
                else:
                    names = [_phone_to_name.get(p, p) for p in assigned]
                    if len(names) <= 2:
                        acct_txt = ", ".join(names)
                    else:
                        acct_txt = f"{names[0]}, {names[1]} 외 {len(names)-2}명"

            act_txt  = "✓ 활성" if enabled else "✗ 비활성"
            self._tv.insert("", tk.END, iid=j.get("name"),
                values=(j.get("name", ""),
                        j.get("template_name", ""),
                        icon,
                        wdef.get("name", ""),
                        sched, stat,
                        act_txt,
                        acct_txt),
                tags=(row_tag,))

    def _get_selected_job(self) -> dict | None:
        sel = self._tv.selection()
        if not sel: return None
        name = sel[0]
        for j in self._jobs:
            if j.get("name") == name:
                return j
        return None

    def _add_job(self):
        dlg = JobDialog(self, self.app, mode="add")
        self.wait_window(dlg)
        if dlg.result:
            self._save_job(dlg.result)

    def _edit_job(self):
        j = self._get_selected_job()
        if not j:
            messagebox.showwarning("선택 없음",
                "수정할 작업을 선택하세요.")
            return
        dlg = JobDialog(self, self.app, mode="edit", data=j)
        self.wait_window(dlg)
        if dlg.result:
            # ── v1.55 CHANGE-D: 수정 시 기존 enabled 상태 보존 ──────────
            # 이전(v1.54): JobDialog.result에 "enabled" 키 없음
            #   → 수정 저장 시 _save_job의 setdefault(True)로 리셋
            #   → 비활성화(False)해둔 작업이 수정 후 자동 활성화되는 버그
            # 변경(v1.55): setdefault로 기존 j["enabled"] 값 우선 보존
            dlg.result.setdefault("enabled", j.get("enabled", True))
            # ── v1.57 CHANGE-W6: schedule_days / times / last_run* 보존 ──
            # 이전(v1.56): 수정 후 저장 시 이 키들이 없으면 _save_job의
            #   setdefault 로 초기화 → last_run_date="" → 당일 재실행 버그(BUG-08)
            #   schedule_days / times 도 초기화 → 설정한 요일·시각 리셋
            # 변경(v1.57): 기존 값 setdefault 로 우선 보존
            # v1.58 CHANGE-X10: days (숫자 인덱스) 보존 추가
            dlg.result.setdefault("days",
                j.get("days", list(DEFAULT_SCHEDULE["days"])))
            dlg.result.setdefault("schedule_days",
                j.get("schedule_days",  ["월","화","수","목","금"]))
            dlg.result.setdefault("schedule_times",
                j.get("schedule_times", []))
            dlg.result.setdefault("last_run",
                j.get("last_run",       ""))
            dlg.result.setdefault("last_run_date",
                j.get("last_run_date",  ""))
            # ── v1.73: 수정 저장 시 반복 설정 보존 ───────────────────────
            # 이전(v1.69): repeat_count/interval 을 setdefault 하지 않아
            #   수정 후 저장하면 다이얼로그에서 읽어온 값으로 덮임
            #   (체크박스 OFF 저장 시 0으로 덮어써지는 문제)
            # 변경: 다이얼로그가 이미 최신값을 반환하므로 보존 불필요.
            #   단, _file 키만 기존 j에서 이어받아야 함 (파일명 일치)
            dlg.result.setdefault("_file", j.get("_file", ""))
            old = j.get("_file")
            if old and Path(old).exists():
                Path(old).unlink()
            self._save_job(dlg.result)

        self.after(0, self._refresh_time_estimate)  # v1.60

    def _dup_job(self):
        j = self._get_selected_job()
        if not j:
            messagebox.showwarning("선택 없음",
                "복제할 작업을 선택하세요.")
            return
        import copy
        new_j = copy.deepcopy(j)
        new_j["name"] = new_j.get("name","") + "_복사본"
        if "_file"   in new_j: del new_j["_file"]
        if "_status" in new_j: del new_j["_status"]
        # ── v1.57 CHANGE-W7: 복제 시 last_run* 초기화 ──────────────────
        # 이전(v1.56): 원본의 last_run / last_run_date 그대로 복사
        #   → interval 모드 복제본이 "이미 실행됨"으로 인식되어 즉시 실행 안될 수 있음
        # 변경(v1.57): 복제본은 항상 "처음 실행" 상태로 초기화
        new_j["last_run"]      = ""
        new_j["last_run_date"] = ""
        self.after(0, self._refresh_time_estimate)  # v1.60
        self._save_job(new_j)

    def _del_job(self):
        j = self._get_selected_job()
        if not j: return
        if not messagebox.askyesno("삭제 확인",
                f"[{j.get('name','')}] 을 삭제할까요?"):
            return
        fpath = j.get("_file")
        if fpath and Path(fpath).exists():
            Path(fpath).unlink()
        self._load_jobs()
        # v1.61 SC-5: 삭제 후 스케줄 동기화
        if hasattr(self, "_sync_scheduler"):
            self.after(100, self._sync_scheduler)

    def _save_job(self, data: dict):
        # ── v1.55 CHANGE-C: enabled 기본값 보장 ─────────────────────────
        # 이전(v1.54): enabled 키 미포함으로 저장 → JSON에 명시적 상태 없음
        # 변경(v1.55): setdefault로 신규·복제 작업에 항상 "enabled": true 포함
        #   기존 JSON(키 없음)도 최초 저장 시 자동 추가됨
        data.setdefault("enabled", True)
        # ── v1.56 CHANGE-S3: 스케줄 실행 시간 추적용 필드 초기화 ────────────────
        # 이전(v1.55): last_run 키 없음 → interval 모드 경과시간 계산 불가
        # 변경(v1.56): 신규·복제 작업 저장 시 빈 문자열로 초기화
        #   last_run      ← interval 모드: (now - last_run) 경과시간 계산
        #   last_run_date ← time    모드: 오늘 날짜와 비교해 중복 실행 방지
        data.setdefault("last_run",      "")
        data.setdefault("last_run_date", "")
        # ── v1.60 BUG-N2: 중복 작업명 체크 ─────────────────────────────────────
        _new_name = data.get("name", "").strip()
        if _new_name:
            _dup_found = [
                j["name"] for j in self._jobs
                if j.get("name", "").strip() == _new_name
                   and j.get("_file") != data.get("_file")
            ]
            if _dup_found:
                import tkinter.messagebox as _mb_dup
                _mb_dup.showwarning(
                    "작업명 중복",
                    f"'{_new_name}' 이름의 작업이 이미 존재합니다.\n"
                    "다른 이름을 사용하거나 기존 작업을 삭제하세요.\n\n"
                    "⚠️ 동일 이름 사용 시 스케줄러가 두 번째 작업을 차단합니다."
                )
                return
        # ── v1.58 CHANGE-X9: DEFAULT_SCHEDULE 기반 기본값 전체 보충 ─────────────
        import copy as _copy_save
        for _k, _v in DEFAULT_SCHEDULE.items():
            data.setdefault(_k, _copy_save.deepcopy(_v))
        # 하위호환: schedule_days(KR) 동기화
        if "days" in data and not data.get("schedule_days"):
            data["schedule_days"] = [_INT_TO_KR[i] for i in data["days"]
                                     if 0 <= i <= 6]
        fname = (data["name"].replace(" ","_")
                             .replace("/","_") + ".json")
        _save_path = JOBS_DIR / fname
        if save_json(_save_path, data):
            self.app._set_status(
                f"✅ 작업 [{data['name']}] 저장")
            self._load_jobs()
            # v1.61 SC-5: _sync_scheduler 로 통합 (기존 _restart_scheduler 대체)
            if hasattr(self, "_sync_scheduler"):
                self._sync_scheduler()
            elif hasattr(self, "_restart_scheduler"):
                self._restart_scheduler()
            self.after(0, self._refresh_time_estimate)  # v1.60 P-17
        else:
            # v1.75: 저장 실패 시 경로 + 권한 정보 포함 상세 메시지
            _path_info = str(_save_path)
            _parent_exists = _save_path.parent.exists()
            messagebox.showerror("저장 실패",
                f"작업 파일 저장 중 오류가 발생했습니다.\n\n"
                f"저장 경로: {_path_info}\n"
                f"폴더 존재: {'✅' if _parent_exists else '❌ 없음'}\n\n"
                f"해결 방법:\n"
                f"• 프로그램을 관리자 권한으로 실행하세요\n"
                f"• Config/jobs 폴더 쓰기 권한을 확인하세요\n"
                f"• 바탕화면·다운로드 폴더에서 실행하세요")

    def _show_help(self):
        msg = (
            "📋 작업 관리 사용 방법\n\n"
            "① 작업 템플릿 탭에서 템플릿을 먼저 만드세요\n"
            "② ＋ 작업 추가 클릭\n"
            "③ 템플릿 선택 → 대상 목록 → 메시지 입력\n"
            "④ 딜레이 · 스케줄 설정 후 저장\n"
            "⑤ ▶ 선택 실행 or ▶▶ 전체 실행\n\n"
            "실행 중 ⏹ 중지 버튼으로 언제든 중단 가능합니다."
        )
        messagebox.showinfo("도움말", msg)

    # ── 실행 관련 (Block 4에서 채워짐) ──────────────────────
    def _run_selected(self): pass
    def _run_all(self):      pass
    def _stop_all(self):     pass
    def set_progress(self, val, label="", target=""):
        """진행률 + 상태 레이블 + 현재 처리 대상 업데이트"""
        self._prog_var.set(val)
        if label:
            self._prog_label.set(label)
        if target is not None:
            self._prog_target.set(target)
    def set_target(self, acct: str = "", peer: str = "",
                   cur: int = 0, total: int = 0):
        """현재 처리 대상 표시 갱신 (계정명, 링크/전화번호, N/전체)"""
        if not acct and not peer:
            self._prog_target.set("")
            return
        parts = []
        if acct:
            parts.append(f"[{acct}]")
        if peer:
            short = peer if len(peer) <= 20 else peer[:18] + "…"
            parts.append(f"→ {short}")
        if total > 0:
            parts.append(f"({cur}/{total})")
        self._prog_target.set("  ".join(parts))
    def set_counts(self, succ: int, fail: int):
        self._succ_var.set(f"✅ {succ}")
        self._fail_var.set(f"❌ {fail}")


# ============================================================
# JobDialog — 작업 추가 / 수정 다이얼로그
# ============================================================

class JobDialog(tk.Toplevel):
    def __init__(self, master, app: "App",
                 mode: str = "add", data: dict = None):
        super().__init__(master)
        self.app    = app
        self.mode   = mode
        self.data   = data or {}
        self.result = None
        self.title("작업 추가" if mode == "add" else "작업 수정")
        self.resizable(False, False)
        self.configure(bg=PALETTE["bg"])
        self.grab_set()
        # v1.75: _build 예외 포착 — 예외 시에도 창이 뜨고 오류 메시지 표시
        try:
            self._build()
        except Exception as _be:
            import traceback as _tb_b
            tk.Label(self,
                     text=f"⚠️ UI 빌드 오류:\n{type(_be).__name__}: {_be}\n\n"
                          f"개발자에게 문의하세요.",
                     bg=PALETTE.get("bg", "#F0F2F5"),
                     fg=PALETTE.get("danger", "#DC2626"),
                     font=("Helvetica", 9),
                     justify=tk.LEFT, wraplength=480,
                     padx=20, pady=20
                     ).pack(fill=tk.BOTH, expand=True)
            print(f"[JobDialog._build ERROR] {_be}", flush=True)
            _tb_b.print_exc()
        self.geometry("520x500")

    def _build(self):
        # 스크롤 영역
        canvas = tk.Canvas(self, bg=PALETTE["card"],
                           highlightthickness=0)
        vsb = tk.Scrollbar(self, orient=tk.VERTICAL,
                           command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        inner = tk.Frame(canvas, bg=PALETTE["card"])
        win = canvas.create_window((0,0), window=inner,
                                    anchor="nw")
        inner.bind("<Configure>",
                   lambda e: canvas.configure(
                       scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfig(
                        win, width=e.width))
        canvas.bind("<MouseWheel>",
                    lambda e: canvas.yview_scroll(
                        int(-1*(e.delta/120)), "units"))

        def section(title):
            title_fr = tk.Frame(inner, bg=PALETTE["bg"])
            title_fr.pack(fill=tk.X, padx=20, pady=(14, 4))
            tk.Frame(title_fr, bg=PALETTE["primary"], width=4
                     ).pack(side=tk.LEFT, fill=tk.Y)
            tk.Label(title_fr, text=f"  {title}",
                     font=F_HEAD,
                     bg=PALETTE["bg"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT)
            tk.Frame(title_fr, bg=PALETTE["border"], height=1
                     ).pack(side=tk.LEFT, fill=tk.X, expand=True,
                            padx=(12, 0), pady=7)
            f = tk.Frame(inner, bg=PALETTE["card"],
                         highlightbackground=PALETTE["border"],
                         highlightthickness=1)
            f.pack(fill=tk.X, padx=20, pady=(0, 4))
            return f

        def row(parent, label, widget_fn):
            r = tk.Frame(parent, bg=PALETTE["card"])
            r.pack(fill=tk.X, padx=0, pady=0)
            tk.Frame(r, bg=PALETTE["border"], height=1
                     ).pack(fill=tk.X)
            inner_r = tk.Frame(r, bg=PALETTE["card"])
            inner_r.pack(fill=tk.X, padx=14, pady=8)
            tk.Label(inner_r, text=label, width=16, anchor=tk.W,
                     font=F_LABEL,
                     bg=PALETTE["card"],
                     fg=PALETTE["text2"]
                     ).pack(side=tk.LEFT)
            widget_fn(inner_r)

        # ── 작업명 ──────────────────────────────────────────
        s1 = section("📌 기본 정보")
        self._jname_var = tk.StringVar(
            value=self.data.get("name", "새 작업"))
        def _jname_w(p):
            tk.Entry(p, textvariable=self._jname_var,
                     bg=PALETTE["card2"], fg=PALETTE["text"],
                     insertbackground=PALETTE["text"],
                     relief=tk.FLAT,
                     font=F_BODY, width=28
                     ).pack(side=tk.LEFT)
        row(s1, "작업명", _jname_w)

        # ── 템플릿 선택 ─────────────────────────────────────
        s2 = section("🗂️ 작업 템플릿 선택")
        templates = self._get_templates()
        tmpl_names = [t.get("name","") for t in templates]
        self._tmpl_var = tk.StringVar(
            value=self.data.get("template_name",
                  tmpl_names[0] if tmpl_names else ""))
        def _tmpl_w(p):
            cb = ttk.Combobox(p,
                     textvariable=self._tmpl_var,
                     values=tmpl_names, width=26,
                     state="readonly")
            cb.pack(side=tk.LEFT)
            # 선택된 템플릿 정보 표시
            self._tmpl_info = tk.Label(
                p, text="", font=F_SMALL,
                bg=PALETTE["bg"], fg=PALETTE["text"])
            self._tmpl_info.pack(side=tk.LEFT, padx=(8,0))
            cb.bind("<<ComboboxSelected>>",
                    lambda e: self._update_tmpl_info())
            self._update_tmpl_info()
        row(s2, "템플릿", _tmpl_w)

        # ── 텔레그램 계정 선택 (Telethon 계정이 있을 때만 표시) ────────────────
        tg_accounts = load_json(TG_ACCOUNTS_PATH, [])
        if tg_accounts and HAS_TELETHON:
            s_acct = section("📱 텔레그램 계정 선택")
            hint_acct = tk.Label(
                s_acct,
                text="이 작업에 사용할 계정을 선택하세요. (미선택 시 전체 계정 사용)",
                font=F_SMALL, bg=PALETTE["bg"], fg=PALETTE["muted"])
            hint_acct.pack(anchor=tk.W, padx=12, pady=(0, 6))

            # 저장된 계정 선택 상태 불러오기
            _saved_assigned = set(self.data.get("assigned_accounts", []))

            self._acct_check_vars: list[tuple[str, tk.BooleanVar]] = []
            acct_frame = tk.Frame(s_acct, bg=PALETTE["bg"])
            acct_frame.pack(fill=tk.X, padx=12, pady=(0, 8))

            for _ac in tg_accounts:
                _phone = TelethonEngine._normalize_phone(_ac.get("phone", ""))
                _name  = _ac.get("name", _phone)
                _var   = tk.BooleanVar(
                    value=(_phone in _saved_assigned) or (not _saved_assigned))
                self._acct_check_vars.append((_phone, _var))
                _row = tk.Frame(acct_frame, bg=PALETTE["bg"])
                _row.pack(fill=tk.X, pady=1)
                tk.Checkbutton(
                    _row, text=f"{_name}  ({_phone})",
                    variable=_var,
                    font=F_LABEL,
                    bg=PALETTE["bg"], fg=PALETTE["text"],
                    selectcolor=PALETTE["card2"],
                    activebackground=PALETTE["bg"]
                ).pack(side=tk.LEFT)

            # 전체선택 / 전체해제 버튼
            _btn_row = tk.Frame(s_acct, bg=PALETTE["bg"])
            _btn_row.pack(anchor=tk.W, padx=12, pady=(0, 8))
            def _sel_all():
                for _, v in self._acct_check_vars: v.set(True)
            def _sel_none():
                for _, v in self._acct_check_vars: v.set(False)
            tk.Button(_btn_row, text="전체선택", font=F_SMALL,
                      bg=PALETTE["hover"], fg=PALETTE["text"],
                      relief=tk.FLAT, cursor="hand2", padx=8,
                      command=_sel_all).pack(side=tk.LEFT, padx=(0, 6))
            tk.Button(_btn_row, text="전체해제", font=F_SMALL,
                      bg=PALETTE["hover"], fg=PALETTE["text"],
                      relief=tk.FLAT, cursor="hand2", padx=8,
                      command=_sel_none).pack(side=tk.LEFT)
        else:
            self._acct_check_vars = []

        self._build_schedule_section(inner, row, section)

        # ── 순차 반복 실행 설정 (v1.69) ─────────────────────
        self._build_repeat_section(inner, section)

        # ── 저장 버튼 ───────────────────────────────────────
        btn_row = tk.Frame(inner, bg=PALETTE["card"])
        btn_row.pack(fill=tk.X, padx=20, pady=(16, 24))
        save_btn = tk.Button(btn_row, text="💾  저장",
                  command=self._ok,
                  bg=PALETTE["primary"], fg="#FFFFFF",
                  relief=tk.FLAT,
                  font=(_FF, 10, "bold"),
                  cursor="hand2", padx=32, pady=10, bd=0,
                  activebackground=PALETTE["primary2"])
        save_btn.pack(side=tk.LEFT)
        save_btn.bind("<Enter>",
                      lambda e: save_btn.config(bg=PALETTE["primary2"]))
        save_btn.bind("<Leave>",
                      lambda e: save_btn.config(bg=PALETTE["primary"]))
    # ── 템플릿 정보 표시 ─────────────────────────────────────
    def _get_templates(self) -> list[dict]:
        templates = []
        if TEMPLATE_DIR.exists():
            for f in sorted(TEMPLATE_DIR.glob("*.json")):
                d = load_json(f, {})
                if d.get("name"):
                    templates.append(d)
        return templates

    def _update_tmpl_info(self):
        name  = self._tmpl_var.get()
        tmpls = self._get_templates()
        for t in tmpls:
            if t.get("name") == name:
                wk   = t.get("workflow", "")
                wdef = PLATFORM_WORKFLOWS.get(wk, {})
                plat = t.get("platform", "")
                icon = "🟡" if plat == "kakao" else "🔵"
                self._tmpl_info.config(
                    text=f"{icon} {wdef.get('name','')}")
                return
        self._tmpl_info.config(text="")

    # ── 대상 목록 섹션 ───────────────────────────────────────
    def _build_target_section(self, inner, row, section):
        s = section("👤 대상 목록")

        # CSV 파일 경로
        self._target_var = tk.StringVar(
            value=self.data.get("target_file", ""))
        def _target_w(p):
            tk.Entry(p, textvariable=self._target_var,
                     bg=PALETTE["card2"], fg=PALETTE["text"],
                     insertbackground=PALETTE["text"],
                     relief=tk.FLAT,
                     font=F_LABEL, width=24
                     ).pack(side=tk.LEFT, padx=(0,6))
            tk.Button(p, text="📂 찾기",
                      command=self._browse_target,
                      bg=PALETTE["hover"], fg=PALETTE["text"],
                      relief=tk.FLAT, cursor="hand2",
                      font=F_SMALL, padx=6
                      ).pack(side=tk.LEFT)
            self._target_count = tk.Label(
                p, text="",
                font=F_SMALL,
                bg=PALETTE["bg"], fg=PALETTE["text"])
            self._target_count.pack(side=tk.LEFT, padx=(8,0))
        row(s, "CSV 파일", _target_w)
        self._update_target_count()

        # CSV 컬럼 매핑 안내
        hint = tk.Frame(s, bg=PALETTE["bg"])
        hint.pack(fill=tk.X, padx=12, pady=(0,8))
        tk.Label(hint,
                 text="💡 CSV 필수 컬럼: 카카오아이디 (친구추가) "
                      "/ 카카오ID, 텔레그램링크 (메시지/가입)",
                 font=F_SMALL,
                 bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(anchor=tk.W)

    def _browse_target(self):
        path = filedialog.askopenfilename(
            title="대상 CSV 파일 선택",
            filetypes=[("CSV", "*.csv"), ("전체", "*.*")])
        if path:
            self._target_var.set(path)
            self._update_target_count()

    def _update_target_count(self):
        path = self._target_var.get().strip()
        if not path or not Path(path).exists():
            try: self._target_count.config(text="")
            except: pass
            return
        try:
            import csv
            with open(path, encoding="utf-8-sig") as f:
                count = sum(1 for _ in csv.reader(f)) - 1
            self._target_count.config(
                text=f"총 {max(count,0):,}명")
        except Exception:
            try: self._target_count.config(text="읽기 실패")
            except: pass

    # ── 메시지 섹션 ──────────────────────────────────────────
    def _build_message_section(self, inner, row, section):
        s = section("💬 메시지")

        # 메시지 텍스트
        msg_frame = tk.Frame(s, bg=PALETTE["bg"])
        msg_frame.pack(fill=tk.X, padx=12, pady=6)
        tk.Label(msg_frame, text="메시지 내용",
                 width=16, anchor=tk.W,
                 font=F_LABEL,
                 bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT, anchor=tk.N, pady=2)

        txt_wrap = tk.Frame(msg_frame, bg=PALETTE["bg"])
        txt_wrap.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._msg_text = tk.Text(
            txt_wrap, height=5, width=36,
            bg=PALETTE["card2"], fg=PALETTE["text"],
            insertbackground=PALETTE["text"],
            relief=tk.FLAT, font=F_LABEL,
            wrap=tk.WORD)
        self._msg_text.pack(side=tk.LEFT,
                            fill=tk.BOTH, expand=True)
        msg_sb = tk.Scrollbar(txt_wrap,
                              command=self._msg_text.yview)
        self._msg_text.configure(
            yscrollcommand=msg_sb.set)
        msg_sb.pack(side=tk.RIGHT, fill=tk.Y)

        # 기존 메시지 삽입
        saved_msg = self.data.get("message", "")
        if saved_msg:
            self._msg_text.insert("1.0", saved_msg)

        # 변수 토큰 버튼
        tok_row = tk.Frame(s, bg=PALETTE["bg"])
        tok_row.pack(fill=tk.X, padx=12, pady=(0,6))
        tk.Label(tok_row, text="변수 삽입:",
                 font=F_SMALL,
                 bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT, padx=(0,6))
        for tok in ["{이름}", "{번호}", "{번호뒤4}",
                    "{랜덤숫자3}", "{랜덤영숫자3}"]:
            tk.Button(tok_row, text=tok,
                      font=F_MONO_S,
                      bg=PALETTE["hover"], fg=PALETTE["text"],
                      relief=tk.FLAT, cursor="hand2",
                      padx=4, pady=1,
                      command=lambda t=tok:
                          self._msg_text.insert(tk.INSERT, t)
                      ).pack(side=tk.LEFT, padx=2)

    # ── 딜레이 섹션 ──────────────────────────────────────────
    def _build_delay_section(self, inner, row, section):
        s = section("⏱️ 딜레이 설정")

        delay_row = tk.Frame(s, bg=PALETTE["bg"])
        delay_row.pack(fill=tk.X, padx=12, pady=8)

        self._delay_min = tk.StringVar(
            value=str(self.data.get("delay_min", 2.0)))
        self._delay_max = tk.StringVar(
            value=str(self.data.get("delay_max", 5.0)))
        self._retry_var = tk.StringVar(
            value=str(self.data.get("retry", 2)))

        for lbl, var in [("최소(초)", self._delay_min),
                         ("최대(초)", self._delay_max)]:
            tk.Label(delay_row, text=lbl,
                     font=F_LABEL,
                     bg=PALETTE["bg"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT, padx=(0,4))
            tk.Entry(delay_row, textvariable=var,
                     width=6, relief=tk.FLAT,
                     bg=PALETTE["card2"], fg=PALETTE["text"],
                     insertbackground=PALETTE["text"],
                     font=F_MONO
                     ).pack(side=tk.LEFT, padx=(0,16))

        tk.Label(delay_row, text="재시도",
                 font=F_LABEL,
                 bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT, padx=(0,4))
        tk.Spinbox(delay_row, from_=0, to=5,
                   textvariable=self._retry_var,
                   width=4, relief=tk.FLAT,
                   bg=PALETTE["card2"], fg=PALETTE["text"],
                   buttonbackground=PALETTE["card"],
                   font=F_MONO
                   ).pack(side=tk.LEFT)
        tk.Label(delay_row, text="회",
                 font=F_LABEL,
                 bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT, padx=(4,0))

    # ── 순차 반복 실행 섹션 (v1.69) ─────────────────────────
    def _build_repeat_section(self, inner, section):
        """전체 실행 시 이 작업을 N회 반복하는 설정 UI.

        저장 키:
          repeat_count    : int  (0 = 무제한, 1 = 1회만, N = N회)
          repeat_interval : int  (초 단위, 작업 완료 → 다음 반복 전 대기)
        """
        s = section("🔁 순차 반복 실행 (선택)")

        # ── ON / OFF 체크박스 행 ─────────────────────────────
        top_row = tk.Frame(s, bg=PALETTE["bg"])
        top_row.pack(fill=tk.X, padx=12, pady=8)

        # v1.73: repeat_on 키 직접 읽기 (이전: repeat_count!=0 으로 판단 → count=1이면 True가 되는 버그)
        self._repeat_on = tk.BooleanVar(
            value=bool(self.data.get("repeat_on", False)))
        cb = tk.Checkbutton(top_row, text="반복 실행 사용",
                            variable=self._repeat_on,
                            bg=PALETTE["bg"], fg=PALETTE["text"],
                            selectcolor=PALETTE["active"],
                            activebackground=PALETTE["bg"],
                            font=F_LABEL,
                            command=self._toggle_repeat)
        cb.pack(side=tk.LEFT, padx=(0, 16))
        tk.Label(top_row,
                 text="(전체 실행 시 목록 순서대로 N번 반복합니다)",
                 font=("Helvetica", 8),
                 bg=PALETTE["bg"],
                 fg=PALETTE.get("muted", "#888888")
                 ).pack(side=tk.LEFT)

        # ── 세부 설정 프레임 ──────────────────────────────────
        self._repeat_detail = tk.Frame(s, bg=PALETTE["bg"])
        self._repeat_detail.pack(fill=tk.X, padx=12, pady=(0, 10))

        # 반복 횟수
        cnt_row = tk.Frame(self._repeat_detail, bg=PALETTE["bg"])
        cnt_row.pack(fill=tk.X, pady=(0, 4))
        tk.Label(cnt_row, text="반복 횟수:",
                 font=F_LABEL, width=14, anchor=tk.W,
                 bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        # v1.73: 저장값 그대로 복원 (0=무제한도 "0"으로 표시, None이면 기본값 3)
        _saved_cnt = self.data.get("repeat_count", None)
        self._repeat_count_var = tk.StringVar(
            value=str(_saved_cnt) if _saved_cnt is not None else "3")
        tk.Entry(cnt_row, textvariable=self._repeat_count_var,
                 width=6, relief=tk.FLAT,
                 bg=PALETTE["card2"], fg=PALETTE["text"],
                 insertbackground=PALETTE["text"],
                 font=F_MONO).pack(side=tk.LEFT)
        tk.Label(cnt_row, text="회   (0 = 무제한)",
                 font=("Helvetica", 8),
                 bg=PALETTE["bg"],
                 fg=PALETTE.get("muted", "#888888")
                 ).pack(side=tk.LEFT, padx=(6, 0))

        # 반복 간격
        gap_row = tk.Frame(self._repeat_detail, bg=PALETTE["bg"])
        gap_row.pack(fill=tk.X)
        tk.Label(gap_row, text="반복 간격:",
                 font=F_LABEL, width=14, anchor=tk.W,
                 bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        _saved_gap = self.data.get("repeat_interval", 0)
        self._repeat_interval_var = tk.StringVar(value=str(_saved_gap))
        tk.Entry(gap_row, textvariable=self._repeat_interval_var,
                 width=6, relief=tk.FLAT,
                 bg=PALETTE["card2"], fg=PALETTE["text"],
                 insertbackground=PALETTE["text"],
                 font=F_MONO).pack(side=tk.LEFT)
        tk.Label(gap_row, text="초   (전체 1순환 완료 후 다음 순환 전 대기)",
                 font=("Helvetica", 8),
                 bg=PALETTE["bg"],
                 fg=PALETTE.get("muted", "#888888")
                 ).pack(side=tk.LEFT, padx=(6, 0))

        # 초기 토글 상태 동기화
        self._toggle_repeat()

    def _toggle_repeat(self):
        """반복 ON/OFF 에 따라 세부 입력 위젯 활성/비활성"""
        state = tk.NORMAL if self._repeat_on.get() else tk.DISABLED
        def _set(widget, st):
            try:
                widget.config(state=st)
            except Exception:
                pass
            for c in widget.winfo_children():
                _set(c, st)
        _set(self._repeat_detail, state)

    # ── 스케줄 섹션 ──────────────────────────────────────────
    def _build_schedule_section(self, inner, row, section):
        s = section("📅 스케줄 (선택)")

        sched_row = tk.Frame(s, bg=PALETTE["bg"])
        sched_row.pack(fill=tk.X, padx=12, pady=8)

        self._sched_on  = tk.BooleanVar(
            value=self.data.get("schedule_on", False))
        self._sched_mode = tk.StringVar(
            value=self.data.get("schedule_mode", "time"))
        # ── v1.57 BUG-A FIX: 편집 시 schedule_times 리스트를 Entry에 복원 ──
        _saved_times = self.data.get("schedule_times", [])
        _init_time   = ", ".join(_saved_times) if _saved_times \
                       else self.data.get("schedule_time", "09:00")
        self._sched_time = tk.StringVar(value=_init_time)
        self._sched_interval = tk.StringVar(
            value=str(self.data.get("schedule_interval", 24)))
        # ── v1.58 CHANGE-X11 Code N: interval_variance StringVar 초기화 ──────
        self._sched_variance = tk.StringVar(
            value=str(self.data.get("interval_variance",
                                    DEFAULT_SCHEDULE["interval_variance"])))

        tk.Checkbutton(sched_row, text="스케줄 사용",
                       variable=self._sched_on,
                       bg=PALETTE["bg"], fg=PALETTE["text"],
                       selectcolor=PALETTE["active"],
                       activebackground=PALETTE["bg"],
                       font=F_LABEL,
                       command=self._toggle_sched
                       ).pack(side=tk.LEFT, padx=(0,16))

        # ── v1.58 CHANGE-X11 Code M: 숫자 인덱스 기반 요일 체크박스 ─────────────
        # 이전(v1.57): schedule_days(KR list) dict 기반
        # 변경(v1.58): days(int list) 기반, 한글 라벨 유지
        _DAY_LABELS = ["월","화","수","목","금","토","일"]
        # days 우선, fallback: schedule_days(KR) → int 변환
        _saved_int_days = self.data.get("days", None)
        if _saved_int_days is None:
            _kr_days = self.data.get("schedule_days", ["월","화","수","목","금"])
            _saved_int_days = [_KR_TO_INT[d] for d in _kr_days
                               if d in _KR_TO_INT]
        self._sched_day_vars: list = []   # [BooleanVar] index 0=월 … 6=일
        self._sched_days: dict = {}       # 하위호환 dict (toggle_sched 참조용)
        days_row = tk.Frame(s, bg=PALETTE["bg"])
        days_row.pack(fill=tk.X, padx=12, pady=(0,4))
        self._sched_days_frame = days_row
        tk.Label(days_row, text="요일:",
                 font=F_LABEL,
                 bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT, padx=(0,6))
        for idx, d in enumerate(_DAY_LABELS):
            var = tk.BooleanVar(value=(idx in _saved_int_days))
            self._sched_day_vars.append(var)
            self._sched_days[d] = var          # 하위호환 dict 유지
            cb = tk.Checkbutton(days_row, text=d, variable=var,
                                bg=PALETTE["bg"], fg=PALETTE["text"],
                                selectcolor=PALETTE["active"],
                                activebackground=PALETTE["bg"],
                                font=F_LABEL)
            cb.pack(side=tk.LEFT, padx=2)

        self._sched_detail = tk.Frame(s, bg=PALETTE["bg"])
        self._sched_detail.pack(fill=tk.X, padx=12, pady=(0,8))
        self._build_sched_detail()
        self._toggle_sched()

    def _build_sched_detail(self):
        # ── v1.58 CHANGE-X12: interval_variance 필드 추가 + _toggle_sched 강제 호출 ─
        p = self._sched_detail
        for w in p.winfo_children(): w.destroy()

        # 모드 선택 라디오버튼
        mode_row = tk.Frame(p, bg=PALETTE["bg"])
        mode_row.pack(fill=tk.X, pady=(0, 4))
        for val, lbl in [("time","지정 시각"),
                         ("interval","반복 간격")]:
            tk.Radiobutton(mode_row, text=lbl,
                           variable=self._sched_mode,
                           value=val,
                           bg=PALETTE["bg"], fg=PALETTE["text"],
                           selectcolor=PALETTE["active"],
                           activebackground=PALETTE["bg"],
                           font=F_LABEL,
                           command=self._build_sched_detail
                           ).pack(side=tk.LEFT, padx=(0,12))

        input_row = tk.Frame(p, bg=PALETTE["bg"])
        input_row.pack(fill=tk.X)

        if self._sched_mode.get() == "time":
            # 지정 시각 모드
            tk.Label(input_row, text="실행 시각:",
                     font=F_LABEL,
                     bg=PALETTE["bg"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT, padx=(0,4))
            tk.Entry(input_row, textvariable=self._sched_time,
                     width=28, relief=tk.FLAT,
                     bg=PALETTE["card2"], fg=PALETTE["text"],
                     insertbackground=PALETTE["text"],
                     font=F_MONO
                     ).pack(side=tk.LEFT)
            tk.Label(input_row, text="(예: 09:00, 14:00)",
                     font=("Helvetica", 8),
                     bg=PALETTE["bg"], fg=PALETTE.get("muted", "#888888")
                     ).pack(side=tk.LEFT, padx=(6,0))
            # ── v1.58: interval_variance (±분 허용) ─────────────────────────
            var_row = tk.Frame(p, bg=PALETTE["bg"])
            var_row.pack(fill=tk.X, pady=(4,0))
            tk.Label(var_row, text="허용 오차(±분):",
                     font=F_LABEL,
                     bg=PALETTE["bg"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT, padx=(0,4))
            tk.Entry(var_row, textvariable=self._sched_variance,
                     width=5, relief=tk.FLAT,
                     bg=PALETTE["card2"], fg=PALETTE["text"],
                     insertbackground=PALETTE["text"],
                     font=F_MONO
                     ).pack(side=tk.LEFT)
            tk.Label(var_row, text="분  (0=정확히 일치)",
                     font=("Helvetica", 8),
                     bg=PALETTE["bg"], fg=PALETTE.get("muted", "#888888")
                     ).pack(side=tk.LEFT, padx=(4,0))
        else:
            # 반복 간격 모드
            tk.Label(input_row, text="간격(시간):",
                     font=F_LABEL,
                     bg=PALETTE["bg"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT, padx=(0,4))
            tk.Entry(input_row, textvariable=self._sched_interval,
                     width=6, relief=tk.FLAT,
                     bg=PALETTE["card2"], fg=PALETTE["text"],
                     insertbackground=PALETTE["text"],
                     font=F_MONO
                     ).pack(side=tk.LEFT)
            tk.Label(input_row, text="시간마다",
                     font=F_LABEL,
                     bg=PALETTE["bg"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT, padx=(4,0))
            # ── v1.58: interval_variance ─────────────────────────────────────
            var_row = tk.Frame(p, bg=PALETTE["bg"])
            var_row.pack(fill=tk.X, pady=(4,0))
            tk.Label(var_row, text="허용 오차(±분):",
                     font=F_LABEL,
                     bg=PALETTE["bg"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT, padx=(0,4))
            tk.Entry(var_row, textvariable=self._sched_variance,
                     width=5, relief=tk.FLAT,
                     bg=PALETTE["card2"], fg=PALETTE["text"],
                     insertbackground=PALETTE["text"],
                     font=F_MONO
                     ).pack(side=tk.LEFT)
            tk.Label(var_row, text="분",
                     font=F_LABEL,
                     bg=PALETTE["bg"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT, padx=(4,0))

        # v1.58 CHANGE-X12: 빌드 후 토글 상태 강제 동기화
        self._toggle_sched()

    def _toggle_sched(self):
        # ── v1.57 CHANGE-W3: 재귀 토글로 교체 ───────────────────────────────────
        # 이전(v1.56): _sched_detail 첫 레벨 자식만 처리
        #   → 요일 Frame 내부 Checkbutton 7개가 토글 안됨 (BUG-02)
        # 변경(v1.57): 재귀 함수로 Frame 중첩 구조 전체 처리
        #              _sched_days_frame (요일 행)도 명시적으로 처리
        state = tk.NORMAL if self._sched_on.get() \
                          else tk.DISABLED

        def _set_state_recursive(widget, st):
            try: widget.config(state=st)
            except Exception: pass
            for child in widget.winfo_children():
                _set_state_recursive(child, st)

        # _sched_detail (모드 라디오 + 시각/간격 입력)
        _set_state_recursive(self._sched_detail, state)
        # _sched_days_frame (요일 체크박스 행) — 별도 Frame이므로 명시 처리
        if hasattr(self, "_sched_days_frame"):
            _set_state_recursive(self._sched_days_frame, state)

    # ── 저장 처리 ────────────────────────────────────────────
    def _ok(self):
        # ── v1.75: 전체 try/except — 예외 발생 시 사용자에게 오류 메시지 표시 ──
        try:
            self._ok_inner()
        except Exception as _e:
            import traceback as _tb
            messagebox.showerror(
                "저장 오류",
                f"작업 저장 중 예상치 못한 오류가 발생했습니다.\n\n"
                f"{type(_e).__name__}: {_e}\n\n"
                f"개발자 로그:\n{_tb.format_exc()[-800:]}"
            )

    def _ok_inner(self):
        """실제 저장 처리 로직 (_ok의 try/except 내부에서 호출)"""
        name = self._jname_var.get().strip()
        if not name:
            messagebox.showwarning("입력 오류",
                "작업명을 입력하세요.")
            return
        tmpl_name = self._tmpl_var.get().strip()
        if not tmpl_name:
            messagebox.showwarning("입력 오류",
                "작업 템플릿을 선택하세요.\n\n"
                "⚠️ 작업 템플릿 탭에서 템플릿을 먼저 만들어야 합니다.")
            return

        # 선택된 템플릿 데이터 가져오기
        tmpls = self._get_templates()
        tmpl  = next((t for t in tmpls
                      if t.get("name") == tmpl_name), {})

        # ── v1.57 CHANGE-W4: schedule_days / schedule_times 저장 + 검증 ─────────
        # 이전(v1.56): schedule_time 단일 문자열, schedule_days/times 없음
        # 변경(v1.57): 요일 리스트·복수 시각 리스트 저장 + 입력 검증
        import re as _re_sched
        sched_on   = self._sched_on.get()
        sched_mode = self._sched_mode.get()

        # ── v1.58 CHANGE-X13: 요일 숫자 인덱스 수집 (_sched_day_vars 우선) ────
        _DAY_LABELS_OK = ["월","화","수","목","금","토","일"]
        if hasattr(self, "_sched_day_vars") and self._sched_day_vars:
            days = [idx for idx, v in enumerate(self._sched_day_vars) if v.get()]
        elif hasattr(self, "_sched_days"):
            days = [_KR_TO_INT[d] for d, var in self._sched_days.items()
                    if var.get() and d in _KR_TO_INT]
        else:
            days = list(DEFAULT_SCHEDULE["days"])
        # 하위호환 KR 리스트 (범위 보호: 0~6만 허용)
        sched_days = [_DAY_LABELS_OK[idx] for idx in days if 0 <= idx <= 6]

        # 복수 시각 파싱 + HH:MM 검증
        raw_times = self._sched_time.get()
        sched_times = []
        invalid_times = []
        for t in raw_times.split(","):
            t = t.strip()
            if not t:
                continue
            if _re_sched.fullmatch(r"\d{2}:\d{2}", t):
                _h, _m = int(t[:2]), int(t[3:])
                if 0 <= _h <= 23 and 0 <= _m <= 59:
                    sched_times.append(t)
                else:
                    invalid_times.append(t)  # 포맷은 맞지만 범위 초과
            else:
                invalid_times.append(t)

        # ── 스케줄 ON 시 입력 유효성 검사 — 형식 오류만 차단, 미입력은 저장 허용 ──
        # v1.75: 시각 미입력·요일 미선택은 저장을 막지 않음
        #        (반복 설정만 쓸 경우 스케줄 미완성 상태로도 저장 가능해야 함)
        if sched_on and invalid_times:
            messagebox.showwarning("시각 형식 오류",
                f"올바르지 않은 시각 형식이 있습니다:\n"
                f"{', '.join(invalid_times)}\n\n"
                f"HH:MM 형식으로 입력하세요. (예: 09:00, 14:00)\n"
                f"또는 '스케줄 사용' 체크를 해제하세요.")
            return

        # sched_label 생성 (Treeview 스케줄 컬럼 표시용)
        sched_label = "없음"
        if sched_on:
            day_str = "".join(sched_days) if sched_days else "매일"
            if sched_mode == "time":
                times_str = ", ".join(sched_times)
                # BUG-09: 컬럼 width 초과 방지 — 20자 이상 말줄임
                full_label = f"{day_str} {times_str}"
                sched_label = (full_label[:20] + "…") \
                               if len(full_label) > 22 else full_label
            else:
                sched_label = f"매 {self._sched_interval.get()}시간 ({day_str})"
                if len(sched_label) > 22:
                    sched_label = sched_label[:20] + "…"

        # ── v1.58 CHANGE-X13: interval_variance 수집 ───────────────────────────
        try:
            _variance_val = int(getattr(self, "_sched_variance",
                                        tk.StringVar(value="0")).get())
        except (ValueError, AttributeError):
            _variance_val = 0

        self.result = {
            "name":              name,
            "template_name":     tmpl_name,
            "platform":          tmpl.get("platform", ""),
            "workflow":          tmpl.get("workflow", ""),
            "schedule_on":       sched_on,
            "schedule_mode":     sched_mode,
            "days":              days,          # v1.58 숫자 인덱스
            "schedule_days":     sched_days,    # 하위호환 KR 리스트
            "schedule_times":    sched_times,
            # 하위호환: 첫 번째 시각을 schedule_time에도 저장
            "schedule_time":     sched_times[0] if sched_times else "",
            "schedule_interval": safe_int(
                                     self._sched_interval.get(), 24),
            "interval_variance": _variance_val, # v1.58 신규
            "schedule_label":    sched_label,
            # 계정 매칭: 선택된 전화번호 목록 (빈 리스트 = 전체 사용)
            "assigned_accounts": [p for p, v in
                                  getattr(self, "_acct_check_vars", [])
                                  if v.get()],
            # ── 순차 반복 실행 설정 (v1.69 / v1.73 fix) ──────────────────
            # repeat_on=OFF 여도 입력값 그대로 저장 (0이면 비활성으로 인식)
            # repeat_on=ON  이고 count=0 → 무제한 / count=1 → 1회(기존동작)
            "repeat_on":       getattr(self, "_repeat_on",
                                       tk.BooleanVar(value=False)).get(),
            "repeat_count":    safe_int(
                                   getattr(self, "_repeat_count_var",
                                           tk.StringVar(value="1")).get(), 1),
            "repeat_interval": safe_int(
                                   getattr(self, "_repeat_interval_var",
                                           tk.StringVar(value="0")).get(), 0),
        }
        self.destroy()
# ============================================================
# Block 4-A : WorkflowExecutor — 플랫폼별 실행 엔진
# ============================================================

import csv as _csv

class WorkflowExecutor:
    """
    작업 + 템플릿 데이터를 받아 플랫폼별 워크플로우 실행
    각 작업유형별 로직이 이 클래스 안에 내장됨
    """
    def __init__(self, job: dict, template: dict,
                 log_fn=None, progress_fn=None,
                 done_fn=None, stop_event=None):
        self.job        = job
        self.tmpl       = template
        # [v1.86-1] 템플릿 workflow 우선 — job에 박힌 snapshot 값 무시
        # 이유: 작업 생성 후 템플릿만 교체하면 job JSON의 workflow는
        #       구버전 값이 남아 있어 엉뚱한 워크플로우로 실행되는 버그 방지
        self.wk         = (template.get("workflow") or
                           job.get("workflow", ""))
        self.coords     = template.get("coords", {})
        self._log       = log_fn      or (lambda m, l="INFO": None)
        self._progress  = progress_fn or (lambda c, t: None)
        self._done      = done_fn     or (lambda s, f: None)
        self._stop      = stop_event  or threading.Event()
        self._succ      = 0
        self._fail      = 0
        self._report_rows: list[dict] = []   # 발행 결과 행 (리포트용)
        self._started_at = None              # 실행 시작 시각
        self._used_telethon = False          # ★ 실제 Telethon 경로 진입 여부 (화면 캡처 스킵 판별)

        # ── 스크린샷 설정 읽기 ─────────────────────────────
        _ss_cfg = load_json(CONFIG_PATH, {}).get("screenshot", {})
        self._ss_enabled  : bool  = _ss_cfg.get("enabled",  True)
        self._ss_interval : float = float(_ss_cfg.get("interval_min", 60.0))  # 초
        self._ss_on_error : bool  = _ss_cfg.get("on_error", True)
        self._ss_last_ts  : float = 0.0       # 마지막 주기적 캡처 시각(time.time())
        self._ss_timer_stop = threading.Event()  # 타이머 스레드 종료 신호

        # ★ 실행 시작 시 FAILSAFE 설정 적용 (설정탭 값 반영)
        if HAS_PYAUTOGUI:
            try:
                import json as _json
                _cfg = _json.loads(
                    Path(CONFIG_PATH).read_text(encoding="utf-8")
                ) if Path(CONFIG_PATH).exists() else {}
                pyautogui.FAILSAFE = _cfg.get(
                    "mouse", {}).get("failsafe", True)
            except Exception:
                pyautogui.FAILSAFE = True

    def _is_stopped(self) -> bool:
        return self._stop.is_set()

    def _jitter(self) -> float:
        """딜레이에 ±20% 지터 추가 (타이밍 설정 기반)"""
        # 템플릿의 between_chats를 기본 딜레이로 사용
        base = safe_float(self.tmpl.get("between_chats",
               self.job.get("delay_min", 2.0)))
        jitter_s = safe_float(self.tmpl.get("between_jitter",
                   self.job.get("delay_max", 0.3)))
        return max(0.1, base + random.uniform(-jitter_s, jitter_s))

    def _sleep_or_stop(self, seconds: float,
                       step: float = 0.1) -> bool:
        """
        인터럽트 가능한 sleep.  [v1.54 신규 — CHANGE-04]
        stop 신호 수신 시 즉시 True 반환, 정상 완료 시 False 반환.
        time.sleep() 대신 이 메서드를 사용해 중지 응답성 확보.
        """
        deadline = time.time() + seconds
        while time.time() < deadline:
            if self._is_stopped():
                return True
            remaining = min(step, deadline - time.time())
            if remaining > 0:
                self._stop.wait(remaining)
        return False

    def _click(self, key: str, double=False):
        """좌표 키로 클릭 (0,0 방어 + FailSafe re-raise 포함)"""
        if not HAS_PYAUTOGUI:
            raise RuntimeError("pyautogui 미설치")
        c = self.coords.get(key, {})
        x, y = c.get("x", 0), c.get("y", 0)
        # ★ 좌표 미설정(0,0) 방어
        if not x or not y:
            raise RuntimeError(
                f"좌표 미설정: '{key}' (x={x}, y={y})  "
                f"→ 템플릿에서 해당 좌표를 먼저 캡처하세요.")
        try:
            if double:
                pyautogui.doubleClick(x, y)
            else:
                pyautogui.click(x, y)
        except pyautogui.FailSafeException:
            # ★ BUG-C: FailSafe 를 상위 except Exception 이 삼키지 않도록 re-raise
            raise
        # after_click 키를 tmpl에서 직접 읽음 (timing 중간 dict 없음)
        time.sleep(safe_float(self.tmpl.get("after_click", 0.3)))

    def _type(self, text: str):
        """텍스트 입력 (pyperclip 우선)"""
        if HAS_PYPERCLIP:
            pyperclip.copy(text)
            pyautogui.hotkey("ctrl", "v")
        else:
            pyautogui.typewrite(text, interval=0.05)
        time.sleep(0.3)

    def _hotkey(self, *keys):
        pyautogui.hotkey(*keys)
        time.sleep(0.2)

    def _read_csv(self) -> list[dict]:
        """대상 CSV 읽기 (템플릿 우선, job fallback)"""
        path = (self.tmpl.get("target_file") or
                self.job.get("target_file", ""))
        if not path or not Path(path).exists():
            self._log("대상 CSV 파일이 없습니다.", "ERROR")
            return []
        rows = []
        try:
            with open(path, encoding="utf-8-sig") as f:
                reader = _csv.DictReader(f)
                for r in reader:
                    rows.append(dict(r))
        except Exception as e:
            self._log(f"CSV 읽기 실패: {e}", "ERROR")
        return rows

    def _read_targets(self) -> list[dict]:
        """CSV 파일 or 직접 입력 통합 읽기.
        target_mode == 'direct' 이면 target_direct 텍스트를 줄 단위 파싱.
          - kakao_friend    : {"카카오아이디": line}
          - telegram_*      : {"텔레그램링크": line}
        CSV 모드이면 _read_csv() 위임.
        """
        mode = self.tmpl.get("target_mode", "csv")
        if mode != "direct":
            return self._read_csv()

        raw = self.tmpl.get("target_direct", "")
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
        if not lines:
            self._log("직접 입력 목록이 비어 있습니다.", "ERROR")
            return []

        wk = self.wk
        rows = []
        if wk == "kakao_friend":
            for line in lines:
                rows.append({"카카오아이디": line})
        elif wk in ("telegram_join", "telegram_message", "telegram_join_and_message"):
            for line in lines:
                rows.append({"이름": "", "텔레그램링크": line})
        else:
            # 기타: 첫 컬럼에 그대로 넣기
            for line in lines:
                rows.append({"값": line})
        self._log(f"직접 입력 목록 {len(rows)}개 로드", "INFO")
        return rows

    # ── 스크린샷 캡처 ────────────────────────────────────────
    def _tg_capture_chat(self, eng, acct: dict, peer: str,
                          capture_delay: float = 2.0,
                          n_msgs: int = 5,
                          sent_msg_id: int = None) -> str:
        """Telethon API로 채팅방 최신 메시지를 가져와 텍스트 파일로 저장.

        · peer          : 채널/그룹 username 또는 링크
        · capture_delay : 발송 후 대기 시간(초) — 메시지 반영 대기
        · n_msgs        : 가져올 최근 메시지 수
        · sent_msg_id   : 직전에 보낸 메시지 ID (있으면 ID 기반으로 정확 조회)
        · 저장 위치     : screenshots/chatlog_{작업명}_{peer}_{시각}.txt
        · 반환값        : 저장 파일 경로 (실패 시 '')
        """
        if not HAS_TELETHON:
            return ""
        # 캡처 ON 설정 확인
        if not self.tmpl.get("tg_api_capture_on", False):
            return ""
        try:
            import datetime as _dt

            time.sleep(capture_delay)  # 메시지 서버 반영 대기

            phone = eng._normalize_phone(acct.get("phone", ""))
            client, loop = eng._ensure_client(acct)
            eng._start_loop_thread(phone, loop)

            captured_lines: list[str] = []
            msgs_raw:  list[dict]  = []   # PNG 렌더링용 구조화 데이터
            title = peer                   # 기본값 (엔티티 조회 성공 시 덮어씀)

            async def _fetch():
                nonlocal title
                if not client.is_connected():
                    await client.connect()
                # 채널/그룹 엔티티 가져오기 (제목 포함)
                try:
                    entity   = await client.get_entity(peer)
                    title    = getattr(entity, "title",
                               getattr(entity, "first_name", peer))
                    username = getattr(entity, "username", "") or peer
                except Exception as _ee:
                    username = peer
                    self._log(f"  [캡처] 엔티티 조회 실패: {_ee}", "WARN")

                captured_lines.append(f"=== 방 제목: {title} (@{username}) ===")
                captured_lines.append(
                    f"=== 캡처 시각: {_dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
                captured_lines.append("")

                # ── 메시지 조회: sent_msg_id 있으면 ID 기반(정확), 없으면 최근 N개 ──
                if sent_msg_id:
                    # 내가 보낸 메시지 ID 를 중심으로 ±(n_msgs//2) 범위 조회
                    # get_messages(ids=[...]) → 정확히 해당 메시지만
                    # min_id/max_id 를 활용해 전후 맥락 포함
                    half = max(1, n_msgs // 2)
                    msgs = await client.get_messages(
                        peer,
                        min_id=sent_msg_id - 1,
                        max_id=sent_msg_id + half + 1,
                        limit=n_msgs
                    )
                    # 내 메시지가 빠진 경우 직접 추가
                    ids_got = {m.id for m in msgs}
                    if sent_msg_id not in ids_got:
                        exact = await client.get_messages(peer, ids=[sent_msg_id])
                        msgs = list(msgs) + [m for m in exact if m is not None]
                    msgs = sorted(msgs, key=lambda m: m.id)
                else:
                    msgs = await client.get_messages(peer, limit=n_msgs)

                for m in reversed(msgs) if not sent_msg_id else msgs:
                    sender_name = ""
                    sender_id   = None
                    try:
                        if m.sender:
                            sender_name = (
                                getattr(m.sender, "first_name", "") + " " +
                                getattr(m.sender, "last_name",  "")
                            ).strip() or getattr(m.sender, "username", "unknown")
                            sender_id = getattr(m.sender, "id", None)
                    except Exception:
                        sender_name = "unknown"
                    ts_str = m.date.strftime("%H:%M:%S") if m.date else ""
                    text   = (m.text or "").replace("\n", " ")
                    media_note = ""
                    if m.media and not m.text:
                        media_note = f"[{type(m.media).__name__}]"
                    captured_lines.append(
                        f"[{ts_str}] {sender_name}: {text}{media_note}")
                    # PNG 렌더링용 raw 데이터
                    # out=True: 내가 보낸 메시지 (말풍선 오른쪽/파란색)
                    # · sent_msg_id 와 ID 일치 → 확실히 내 것
                    # · Telethon m.out 플래그도 함께 참조
                    is_out = bool(getattr(m, "out", False))
                    if sent_msg_id and m.id == sent_msg_id:
                        is_out = True
                    msgs_raw.append({
                        "sender":    sender_name,
                        "sender_id": sender_id,
                        "time":      ts_str,
                        "text":      text or media_note,
                        "is_media":  bool(m.media and not m.text),
                        "out":       is_out,    # ★ 내 메시지 여부
                        "msg_id":    m.id,      # ★ 메시지 ID
                    })

            eng._run_in_loop(loop, _fetch())

            if not captured_lines:
                return ""

            # 파일 저장
            job_name  = self.job.get("name", "job").replace(" ", "_")
            # ★ t.me/username 형식에서 username만 추출, 그 외는 금지문자 제거
            # Windows 파일명 금지문자(\/:*?"<>|)가 남지 않도록 처리
            import re as _re_ps
            _m_ps = _re_ps.search(r't\.me/([^/\s?#]+)', peer)
            if _m_ps:
                peer_safe = _m_ps.group(1)[:30]
            else:
                peer_safe = _re_ps.sub(r'[\\/:*?"<>|]', '_', peer.lstrip("@"))[:30]
            ts        = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
            fname     = f"chatlog_{job_name}_{peer_safe}_{ts}.txt"
            SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
            fpath     = SCREENSHOTS_DIR / fname
            fpath.write_text("\n".join(captured_lines), encoding="utf-8")

            self._log(f"📋 채팅 캡처 저장: {fname}", "INFO")
            # 리포트에 파일명 기록
            if self._report_rows:
                self._report_rows[-1]["비고"] += f" [채팅캡처:{fname}]"

            # ── v1.62: 말풍선 PNG 렌더링 ─────────────────────────────────
            # Telethon으로 가져온 메시지 데이터를 PIL로 말풍선 이미지로 저장
            # (별도 로그인/Chrome 설정 불필요 — 이미 연결된 세션 활용)
            png_path = self._render_chat_png(
                msgs_raw, title, peer_safe, ts,
                my_phone=phone
            )
            if png_path:
                if self._report_rows:
                    self._report_rows[-1]["비고"] += f" [이미지캡처:{png_path}]"

            return str(fpath)

        except Exception as _ce:
            self._log(f"  ⚠️ 채팅 캡처 실패: {_ce}", "WARN")
            return ""

    # ── v1.62: 말풍선 PNG 렌더러 ────────────────────────────────────────
    def _render_chat_png(self, msgs: list[dict], room_title: str,
                         peer_safe: str, ts: str,
                         my_phone: str = "") -> str:
        """Telethon으로 가져온 메시지 리스트를 텔레그램 스타일 말풍선 PNG로 저장.

        · msgs       : [{"sender", "sender_id", "time", "text", "is_media"}, ...]
        · room_title : 채팅방 이름
        · peer_safe  : 파일명용 정제 문자열
        · ts         : 타임스탬프 (chatlog 와 동일)
        · my_phone   : 발송 계정 전화번호 (오른쪽 말풍선 판별용)
        · 반환값     : 저장 파일명 (실패 시 '')

        PIL(Pillow) 이 설치되어 있어야 함.
        """
        try:
            from PIL import Image as _Img, ImageDraw as _Draw, ImageFont as _Font
        except ImportError:
            self._log("⚠️ 말풍선 PNG: Pillow 미설치 (pip install Pillow)", "WARN")
            return ""

        if not msgs:
            return ""

        try:
            import datetime as _dt

            # ── 디자인 상수 ───────────────────────────────────────────────
            W          = 640          # 이미지 너비
            PAD        = 16           # 외곽 여백
            BUBBLE_MAX = W - PAD*2 - 60  # 말풍선 최대 너비
            FONT_SZ    = 14
            FONT_SM    = 11
            BG_COLOR   = (20, 30, 48)          # 다크 배경 (텔레그램 다크모드)
            MY_BUBBLE  = (42, 130, 228)         # 내 메시지 (파란색)
            OTHER_BUB  = (40, 52, 68)           # 상대 메시지 (회색)
            MY_TEXT    = (255, 255, 255)
            OTHER_TEXT = (220, 230, 240)
            TIME_COLOR = (130, 150, 170)
            NAME_COLOR = (100, 180, 255)
            HEADER_BG  = (15, 22, 36)
            RADIUS     = 14

            # ── 폰트 로드 (없으면 기본 폰트 사용) ───────────────────────
            def _load_font(size):
                for path in [
                    "C:/Windows/Fonts/malgun.ttf",       # 맑은 고딕 (Windows)
                    "C:/Windows/Fonts/NanumGothic.ttf",
                    "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",  # Linux
                    "/System/Library/Fonts/AppleSDGothicNeo.ttc",       # macOS
                ]:
                    try:
                        return _Font.truetype(path, size)
                    except Exception:
                        continue
                return _Font.load_default()

            font      = _load_font(FONT_SZ)
            font_sm   = _load_font(FONT_SM)
            font_bold = _load_font(FONT_SZ)  # bold 폰트가 없으면 동일 폰트

            # ── 텍스트 줄바꿈 헬퍼 ───────────────────────────────────────
            def _wrap_text(draw, text, font, max_w):
                """텍스트를 max_w 픽셀 이내로 줄바꿈. 줄 리스트 반환."""
                words  = text.split(" ")
                lines  = []
                cur    = ""
                for w in words:
                    test = (cur + " " + w).strip()
                    if draw.textlength(test, font=font) <= max_w:
                        cur = test
                    else:
                        if cur:
                            lines.append(cur)
                        cur = w
                if cur:
                    lines.append(cur)
                return lines or [""]

            # ── 말풍선 높이 계산 패스 ────────────────────────────────────
            # 먼저 더미 이미지로 각 말풍선 높이를 계산
            dummy = _Img.new("RGB", (W, 100))
            d     = _Draw.Draw(dummy)

            bubble_infos = []   # (is_mine, name, lines, time_str, bh)
            for msg in msgs:
                # ── 내 메시지 판별 (우선순위 순) ────────────────────────────
                # 1순위: msgs_raw 에 "out" 필드가 True → Telethon 확인된 내 메시지
                # 2순위: "msg_id" 가 sent_msg_id 와 일치
                # 이 두 가지로 100% 정확하게 판별
                is_mine = bool(msg.get("out", False))
                name    = msg.get("sender", "")
                text    = msg.get("text", "")
                ts_str  = msg.get("time", "")
                bub_w   = BUBBLE_MAX
                lines   = _wrap_text(d, text, font, bub_w - 24)
                line_h  = FONT_SZ + 4
                bh      = PAD + len(lines) * line_h + 6 + FONT_SM + PAD
                if not is_mine:
                    bh += FONT_SM + 4   # 이름 줄 추가 높이
                bubble_infos.append((is_mine, name, lines, ts_str, bh))

            # ── 전체 이미지 높이 계산 ─────────────────────────────────────
            HEADER_H = 52
            total_h  = HEADER_H + PAD
            for _, _, _, _, bh in bubble_infos:
                total_h += bh + 8
            total_h += PAD

            # ── 실제 이미지 그리기 ───────────────────────────────────────
            img  = _Img.new("RGB", (W, total_h), BG_COLOR)
            draw = _Draw.Draw(img)

            # 헤더 (채팅방 이름 + 시각)
            draw.rectangle([0, 0, W, HEADER_H], fill=HEADER_BG)
            draw.text((PAD, 10), room_title, font=font_bold, fill=(255, 255, 255))
            cap_time = _dt.datetime.now().strftime("%Y-%m-%d %H:%M")
            draw.text((PAD, 10 + FONT_SZ + 4), cap_time, font=font_sm,
                      fill=TIME_COLOR)
            # 헤더 구분선
            draw.line([0, HEADER_H - 1, W, HEADER_H - 1], fill=(30, 44, 64), width=1)

            y = HEADER_H + PAD

            # ── 렌더링 루프: out 필드 기반으로 정확히 판별 ───────────────
            for idx, (msg, (_, name, lines, ts_str, bh)) in \
                    enumerate(zip(msgs, bubble_infos)):
                is_mine = bool(msg.get("out", False))  # ★ Telethon 확인된 내 메시지

                bub_color  = MY_BUBBLE  if is_mine else OTHER_BUB
                text_color = MY_TEXT    if is_mine else OTHER_TEXT
                bub_w = max(
                    120,
                    max((draw.textlength(ln, font=font) for ln in lines), default=60)
                    + 24
                )
                bub_w = min(bub_w, BUBBLE_MAX)

                # 말풍선 x 위치
                if is_mine:
                    bx = W - PAD - bub_w
                else:
                    bx = PAD

                # 발신자 이름 (상대방만)
                inner_y = y
                if not is_mine and name:
                    draw.text((bx + 10, inner_y + 6), name,
                              font=font_sm, fill=NAME_COLOR)
                    inner_y += FONT_SM + 4

                # 말풍선 배경 (둥근 사각형 근사)
                bub_rect = [bx, inner_y, bx + bub_w, inner_y + bh - (0 if is_mine else FONT_SM + 4)]
                draw.rounded_rectangle(bub_rect, radius=RADIUS, fill=bub_color)

                # 메시지 텍스트
                tx = bx + 10
                ty = inner_y + 10
                line_h = FONT_SZ + 4
                for ln in lines:
                    draw.text((tx, ty), ln, font=font, fill=text_color)
                    ty += line_h

                # 시각 (오른쪽 하단)
                time_w = draw.textlength(ts_str, font=font_sm)
                draw.text((bx + bub_w - time_w - 8, ty),
                          ts_str, font=font_sm, fill=TIME_COLOR)

                y += bh + 8

            # ── 저장 ──────────────────────────────────────────────────────
            job_name  = self.job.get("name", "job").replace(" ", "_")
            fname_png = f"chatimg_{job_name}_{peer_safe}_{ts}.png"
            SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
            fpath_png = SCREENSHOTS_DIR / fname_png
            img.save(str(fpath_png), "PNG")
            self._log(f"📸 채팅 이미지 저장: {fname_png}", "INFO")
            return fname_png

        except Exception as _re:
            self._log(f"  ⚠️ 말풍선 PNG 생성 실패: {_re}", "WARN")
            return ""

    def _capture_screen(self, reason: str = "periodic") -> str:
        """현재 화면을 캡처해 screenshots/ 에 저장. 저장 경로 반환(실패 시 '').

        reason: 'periodic' | 'error' | 'manual'
        파일명: screenshot_{작업명}_{reason}_{YYYYMMDD_HHMMSS}.png
        """
        if not self._ss_enabled:
            return ""
        try:
            import datetime as _dt
            # PIL.ImageGrab 우선, 없으면 pyautogui.screenshot
            try:
                from PIL import ImageGrab as _IG
                img = _IG.grab()
            except Exception:
                if HAS_PYAUTOGUI:
                    img = pyautogui.screenshot()
                else:
                    self._log("⚠️ 스크린샷: PIL/pyautogui 모두 없음", "WARN")
                    return ""

            job_name = self.job.get("name", "job").replace(" ", "_")
            ts       = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
            fname    = f"screenshot_{job_name}_{reason}_{ts}.png"
            fpath    = SCREENSHOTS_DIR / fname
            img.save(str(fpath), "PNG")
            self._log(f"📸 스크린샷 저장: {fname}", "INFO")
            # 리포트에도 기록
            if self._report_rows:
                self._report_rows[-1]["비고"] += f" [캡처:{fname}]"
            return str(fpath)
        except Exception as _se:
            self._log(f"⚠️ 스크린샷 실패: {_se}", "WARN")
            return ""

    def _start_periodic_capture(self):
        """백그라운드 스레드로 주기적 스크린샷 실행 (interval_min 초 간격)"""
        if not self._ss_enabled:
            return
        def _loop():
            while not self._ss_timer_stop.is_set():
                # stop_event 대기 (interval 초 또는 중지 신호)
                stopped = self._ss_timer_stop.wait(timeout=self._ss_interval)
                if stopped:
                    break
                if self._is_stopped():
                    break
                self._capture_screen("periodic")
        t = threading.Thread(target=_loop,
                             name="ss-periodic", daemon=True)
        t.start()

    def _stop_periodic_capture(self):
        """주기적 캡처 스레드 종료"""
        self._ss_timer_stop.set()

    # ── 메인 실행 진입점 ─────────────────────────────────────
    def _record(self, target: str, status: str, note: str = ""):
        """발행 결과를 리포트 버퍼에 기록"""
        import datetime as _dt
        self._report_rows.append({
            "시각":     _dt.datetime.now().strftime("%H:%M:%S"),
            "대상":     target,
            "결과":     status,          # 성공 / 실패 / 건너뜀
            "비고":     note,
            "계정":     "",              # 호출 측에서 덮어쓸 수 있음
            "msg_id":   "",              # Telethon 발송 시 메시지 ID
        })

    def _save_report(self):
        """실행 완료 후 CSV 리포트를 logs/ 에 저장"""
        import datetime as _dt
        import csv as _csv_rpt
        if not self._report_rows:
            return
        try:
            job_name  = self.job.get("name", "unknown")
            wk        = self.wk
            ts        = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
            fname     = f"report_{job_name}_{wk}_{ts}.csv".replace(" ", "_")
            rpt_path  = LOGS_DIR / fname
            LOGS_DIR.mkdir(parents=True, exist_ok=True)
            total     = len(self._report_rows)
            succ      = sum(1 for r in self._report_rows if r["결과"] == "성공")
            fail      = total - succ
            elapsed   = ""
            if self._started_at:
                secs = int((_dt.datetime.now() - self._started_at).total_seconds())
                elapsed = f"{secs // 60}분 {secs % 60}초"
            with open(rpt_path, "w", newline="", encoding="utf-8-sig") as f:
                # 헤더 요약 행
                writer = _csv_rpt.writer(f)
                writer.writerow(["# 리포트 요약"])
                writer.writerow(["작업명", job_name])
                writer.writerow(["워크플로우", wk])
                writer.writerow(["총 건수", total])
                writer.writerow(["성공", succ])
                writer.writerow(["실패", fail])
                writer.writerow(["소요시간", elapsed])
                writer.writerow([])
                # 상세 결과
                fields = ["시각", "대상", "결과", "계정", "msg_id", "비고"]
                writer.writerow(fields)
                for row in self._report_rows:
                    writer.writerow([row.get(k, "") for k in fields])
            self._log(f"📄 리포트 저장 완료: {rpt_path.name}", "INFO")
        except Exception as _re:
            self._log(f"⚠️ 리포트 저장 실패: {_re}", "WARN")

    def run(self):
        import datetime as _dt_run
        self._started_at = _dt_run.datetime.now()
        dispatch = {
            "kakao_friend":              self._run_kakao_friend,
            "kakao_openchat":            self._run_kakao_openchat,
            "telegram_join":             self._run_telegram_join,
            "telegram_message":          self._run_telegram_message,
            "telegram_join_and_message": self._run_telegram_join_and_message,
        }
        fn = dispatch.get(self.wk)
        if not fn:
            self._log(f"알 수 없는 작업유형: {self.wk}", "ERROR")
            self._done(0, 1)
            return

        # ── 사전 캡처: 아직 Telethon 여부 미확정 → GUI 모드에서만 start 캡처
        # _used_telethon 은 fn() 실행 중 실제 Telethon 경로 진입 시 True 로 세팅됨
        # (assigned_accounts 필터링 후 매칭 0건 → pyautogui 폴백 시는 False 유지)
        _pre_is_telethon = (
            self.wk in ("telegram_message", "telegram_join",
                        "telegram_join_and_message")
            and HAS_TELETHON
            and bool(load_json(TG_ACCOUNTS_PATH, []))
        )
        if not _pre_is_telethon:
            self._capture_screen("start")
            self._start_periodic_capture()

        try:
            fn()
        except Exception as e:
            self._log(f"실행 중 오류: {e}", "ERROR")
            # ★ 예외 발생 시 즉시 캡처 — 실제 GUI 모드 여부를 _used_telethon 로 판별
            if self._ss_on_error and not self._used_telethon:
                self._capture_screen("error")
        finally:
            # ★ fn() 실행 완료 후 _used_telethon 확정값으로 캡처 여부 결정
            # 케이스별 동작:
            #   [A] Telethon 정상 실행   → _used_telethon=True  → 캡처 없음
            #   [B] 매칭 실패 → 폴백     → _used_telethon=False → 캡처 + 스레드 종료
            #   [C] pyautogui 모드 처음부터 → _used_telethon=False → 캡처 + 스레드 종료
            if not self._used_telethon:
                if _pre_is_telethon:
                    # [B] 사전에 Telethon 예상했으나 실제론 폴백 → 캡처 스레드가 시작 안 됨
                    # → start/periodic 캡처는 이미 skip 됐으므로 finish만
                    self._capture_screen("finish")
                else:
                    # [C] 처음부터 pyautogui 모드 → 스레드 종료 + finish 캡처
                    self._stop_periodic_capture()
                    self._capture_screen("finish")
            # [A] Telethon 정상: 아무 캡처도 없음
            self._save_report()              # ★ 실행 완료 시 자동 리포트 저장
            self._done(self._succ, self._fail)

    # ════════════════════════════════════════════════════════
    # 카카오 친구추가
    # ════════════════════════════════════════════════════════
    def _run_kakao_friend(self):
        """
        카카오 친구추가 워크플로우 — 색상 탐지 방식
        ─────────────────────────────────────────
        좌표 설정:
          1. id_add_btn    : ID 입력창 (클릭 후 ID 붙여넣기)
          2. status_dot    : 친추 가능 확인 색상좌표
                             노란색 → 기존친구 / 흰색 → 신규 or 없음
          3. friend_add_btn: 친추 버튼 색상좌표
                             노란색 → 친추가능(신규) / 흰색 → 없는ID
          4. profile_area  : 프로필 영역 클릭
          5. confirm_btn   : 이름변경 확인 버튼
          6. close_btn     : 닫기 버튼

        분기점:
          new      → 친구추가 + 이름변경
          existing → rename_existing=True 일 때만 이름변경
          not_found→ 입력창 초기화 후 다음 ID
          error    → 재시도
        """
        if not HAS_PYAUTOGUI:
            self._log("pyautogui 가 필요합니다.", "ERROR"); return

        rows = self._read_targets()
        if not rows:
            self._log("대상 목록이 없거나 비어있습니다.", "ERROR"); return

        id_col = None
        allowed = {"카카오아이디", "id", "kakao_id", "아이디"}
        for col in rows[0].keys():
            if col.strip().lower().replace(" ", "") in allowed or id_col is None:
                id_col = col
                break

        kakao_ids = [str(r.get(id_col, "")).strip() for r in rows
                     if str(r.get(id_col, "")).strip()]
        if not kakao_ids:
            self._log("카카오ID를 읽지 못했습니다.", "ERROR"); return

        total          = len(kakao_ids)
        keyword        = self.tmpl.get("id_keyword",    "가망")
        start_num      = safe_int(self.tmpl.get("id_start_num",  1))
        digits         = safe_int(self.tmpl.get("id_digits",     0))
        retry          = safe_int(self.tmpl.get("retry_count",   2))
        rename_existing= bool(self.tmpl.get("rename_existing", False))

        self._log(
            f"친구추가 시작 — 총 {total}명 / "
            f"키워드: {keyword}{start_num}부터 / "
            f"기존친구 이름변경: {'포함' if rename_existing else '제외'}",
            "INFO")

        for idx, kakao_id in enumerate(kakao_ids):
            if self._is_stopped():
                self._log("사용자 중지", "WARN"); break

            counter  = start_num + idx
            name_tag = (f"{keyword}{str(counter).zfill(digits)}"
                        if digits else f"{keyword}{counter}")

            self._log(f"[{idx+1}/{total}] ID: {kakao_id} → 이름예정: {name_tag}")
            self._progress(idx+1, total)

            success = False
            for attempt in range(retry + 1):
                if self._is_stopped(): break
                result = self._kakao_friend_once(
                    kakao_id, name_tag, rename_existing)

                if result in ("success", "existing_skipped"):
                    self._succ += 1
                    msg = ("✅ 친구추가+이름변경 완료" if result == "success"
                           else "ℹ️ 기존친구 이름변경 제외 (스킵)")
                    self._log(f"  {msg}: {name_tag}", "SUCCESS")
                    success = True; break
                elif result == "existing_renamed":
                    self._succ += 1
                    self._log(f"  ✅ 기존친구 이름변경 완료: {name_tag}", "SUCCESS")
                    success = True; break
                elif result == "not_found":
                    self._log(f"  ⚠️ 없는 ID: {kakao_id}", "WARN")
                    success = True; break  # 없는 ID는 실패 카운트 제외
                else:  # error
                    if attempt < retry:
                        self._log(f"  🔄 재시도 {attempt+1}/{retry}", "WARN")
                        if self._sleep_or_stop(1.5): return  # BUG-03 fix
                    else:
                        self._log(f"  ❌ 실패: {kakao_id}", "ERROR")

            if not success:
                self._fail += 1

            if self._sleep_or_stop(self._jitter()): return  # BUG-03 fix

        self._log(
            f"완료 — 성공:{self._succ} / 실패:{self._fail}",
            "SUCCESS")

    def _kakao_friend_once(self, kakao_id: str,
                           name_tag: str,
                           rename_existing: bool = False) -> str:
        """
        색상 탐지 기반 단일 친구추가 실행
        반환: 'success' / 'existing_skipped' / 'existing_renamed' /
               'not_found' / 'error'

        공통 로직:
          1. Ctrl+A
          2. id_add_btn 좌클릭
          3. ID 붙여넣기 (Ctrl+V)
          4. Enter (검색 실행)
          [after_input 대기]
          5. status_dot 픽셀 읽기 (클릭 없음)
             → 노란색: existing (기존 친구) 바로 분기
             → 흰색:   6번으로
          6. friend_add_btn 픽셀 읽기 (클릭 없음)
             → 노란색: new (신규, 친추 가능)
             → 흰색:   not_found (없는 ID)
          [after_color_wait 대기 후 읽기]

        분기점 1 (new) / 분기점 3 (existing + rename_existing=True):
          friend_add_btn 좌클릭 → Tab×4 → Enter
          → profile_area 좌클릭 → Tab×6 → Enter
          → Ctrl+A → Delete → 이름 입력 (Ctrl+V)
          → confirm_btn 좌클릭 → close_btn 좌클릭

        분기점 2 (not_found):
          id_add_btn 좌클릭 → Ctrl+A → Delete

        분기점 3 기존친구 스킵 (rename_existing=False):
          ESC
        """
        timing = {
            "after_ctrlA":      safe_float(self.tmpl.get("after_ctrlA",      2.0)),
            "after_click":      safe_float(self.tmpl.get("after_click",      1.5)),
            "after_input":      safe_float(self.tmpl.get("after_input",      2.5)),
            "after_color_wait": safe_float(self.tmpl.get("after_color_wait", 0.6)),
            "after_tab":        safe_float(self.tmpl.get("after_tab",        0.5)),
        }

        # 좌표 추출 헬퍼
        def _c(key):
            c = self.coords.get(key, {})
            return c.get("x", 0), c.get("y", 0)

        id_x,      id_y      = _c("id_add_btn")
        status_x,  status_y  = _c("status_dot")
        friend_x,  friend_y  = _c("friend_add_btn")
        profile_x, profile_y = _c("profile_area")
        confirm_x, confirm_y = _c("confirm_btn")
        close_x,   close_y   = _c("close_btn")

        try:
            # ── 공통 로직 ──────────────────────────────────
            # 1) Ctrl+A (이전 입력 초기화)
            pyautogui.hotkey("ctrl", "a")
            time.sleep(timing["after_ctrlA"])

            # 2) ID로 추가 좌표 클릭
            self._log("  → [ID 입력창] 클릭")
            pyautogui.click(id_x, id_y)
            time.sleep(timing["after_click"])

            # 3) ID 입력 (Ctrl+A → Delete → Ctrl+V)
            pyautogui.hotkey("ctrl", "a")
            time.sleep(0.1)
            pyautogui.press("delete")
            time.sleep(0.1)
            pyperclip.copy(kakao_id)
            pyautogui.hotkey("ctrl", "v")
            time.sleep(0.2)

            # 4) Enter — 검색 실행
            self._log("  → [Enter] 검색 실행")
            pyautogui.press("enter")
            time.sleep(timing["after_input"])

            # ── 색상 탐지로 상태 판별 (클릭 없이 픽셀만 읽기) ─
            time.sleep(timing["after_color_wait"])

            # 5) status_dot 먼저 읽기
            status_rgb = _kf_get_pixel(status_x, status_y)
            self._log(f"    status_dot RGB={status_rgb}")

            if _kf_is_yellow(status_x, status_y):
                state = "existing"
            else:
                # 6) status_dot 흰색 → friend_add_btn 읽기
                friend_rgb = _kf_get_pixel(friend_x, friend_y)
                self._log(f"    friend_add_btn RGB={friend_rgb}")
                state = "new" if _kf_is_yellow(friend_x, friend_y) else "not_found"

            self._log(f"    → 판별 결과: {state}")

            # ── 분기점 2: 없는 ID ──────────────────────────
            if state == "not_found":
                self._log("  → 없는 ID — 입력창 초기화")
                pyautogui.click(id_x, id_y)
                time.sleep(timing["after_click"])
                pyautogui.hotkey("ctrl", "a")
                time.sleep(0.1)
                pyautogui.press("delete")
                return "not_found"

            # ── 분기점 3: 기존 친구 스킵 ───────────────────
            if state == "existing" and not rename_existing:
                self._log("  → 기존친구 이름변경 제외 — ESC")
                pyautogui.press("escape")
                return "existing_skipped"

            # ── 분기점 1 (new) 또는 분기점 3 (existing+rename) ─
            if state in ("new", "existing"):
                branch = "신규 친추+이름변경" if state == "new" else "기존친구 이름변경"
                self._log(f"  → [{branch}] 시작")

                # friend_add_btn 좌클릭
                self._log("  → [친추 버튼] 클릭")
                pyautogui.click(friend_x, friend_y)
                time.sleep(timing["after_click"])

                # Tab×4 → Enter (친구추가 확인 or 채팅 진입)
                self._log("  → Tab×4 + Enter")
                for _ in range(4):
                    pyautogui.press("tab")
                    time.sleep(0.12)
                pyautogui.press("enter")
                time.sleep(timing["after_click"])

                # profile_area 클릭
                self._log("  → [프로필] 클릭")
                pyautogui.click(profile_x, profile_y)
                time.sleep(timing["after_click"])

                # Tab×6 → Enter (이름편집 진입)
                self._log("  → Tab×6 + Enter (이름편집)")
                for _ in range(6):
                    pyautogui.press("tab")
                    time.sleep(timing["after_tab"])
                pyautogui.press("enter")
                time.sleep(0.3)

                # 이름 입력: Ctrl+A → Delete → 붙여넣기
                self._log(f"  → [이름 입력] {name_tag}")
                pyautogui.hotkey("ctrl", "a")
                time.sleep(0.1)
                pyautogui.press("delete")
                time.sleep(0.1)
                pyperclip.copy(name_tag)
                pyautogui.hotkey("ctrl", "v")
                time.sleep(0.2)

                # confirm_btn 클릭
                self._log("  → [확인] 클릭")
                pyautogui.click(confirm_x, confirm_y)
                time.sleep(timing["after_click"])

                # close_btn 클릭
                self._log("  → [닫기] 클릭")
                pyautogui.click(close_x, close_y)
                time.sleep(0.4)

                return "success" if state == "new" else "existing_renamed"

            # error
            pyautogui.press("escape")
            return "error"

        except Exception as e:
            self._log(f"    오류: {e}", "ERROR")
            try: pyautogui.press("escape")
            except: pass
            return "error"

    # ════════════════════════════════════════════════════════
    # 카카오 메시지 뿌리기
    # ════════════════════════════════════════════════════════

    # ════════════════════════════════════════════════════════
    # 카카오 오픈채팅 / 아침인사 / 가망뿌리기
    # ════════════════════════════════════════════════════════
    def _run_kakao_openchat(self):
        """카카오 오픈채팅/아침인사/가망뿌리기 실행  [v1.52 전면 개선]"""
        if not HAS_PYAUTOGUI:
            self._log("pyautogui 가 필요합니다.", "ERROR")
            return

        # ── 설정값 읽기 ─────────────────────────────────────
        message      = self.tmpl.get("message") or self.job.get("message", "")
        use_img      = self.tmpl.get("use_image",        False)
        img_path     = self.tmpl.get("image_path",       "")
        img_order    = self.tmpl.get("img_order",        "before")
        input_method = self.tmpl.get("input_method",     "direct")
        send_method  = self.tmpl.get("send_method",      "enter")
        close_after  = self.tmpl.get("close_after_send", True)
        close_method = self.tmpl.get("close_method",     "esc")
        # 하위호환: 구버전 "coord" 값 → "click_btn"
        if send_method  == "coord": send_method  = "click_btn"
        if close_method == "coord": close_method = "click_btn"
        img_delays   = self.tmpl.get("image_delays",  {})

        # ── v1.52: 단계별 딜레이 (oc_ 접두사, 하위호환 fallback) ────
        _old_ad      = safe_float(self.tmpl.get("action_delay", 1.0))
        oc_after_open  = safe_float(self.tmpl.get("oc_after_open",  _old_ad))
        oc_after_click = safe_float(self.tmpl.get("oc_after_click", 0.3))
        oc_after_type  = safe_float(self.tmpl.get("oc_after_type",  0.3))
        oc_after_send  = safe_float(self.tmpl.get("oc_after_send",  _old_ad))
        oc_after_close = safe_float(self.tmpl.get("oc_after_close", 0.8))
        between        = safe_float(self.tmpl.get("between_chats",  0.5))
        jitter_s       = safe_float(self.tmpl.get("between_jitter", 0.3))

        # ── 그리드 좌표 계산 (v1.52: cell_width 기준, column_gap fallback) ──
        gc   = self.tmpl.get("grid_config", {})
        sx   = safe_int  (gc.get("start_x"))
        sy   = safe_int  (gc.get("start_y"))
        ch   = safe_float(gc.get("cell_height", 0))
        col  = safe_int  (gc.get("column_count", 1))
        row  = safe_int  (gc.get("row_count",    1))
        sdir = gc.get("scan_dir", "col")
        # cell_width 우선, 없으면 column_gap fallback (하위호환)
        cw   = safe_float(gc.get("cell_width",
                                  gc.get("column_gap", 0)))

        # ── 시작좌표 미캡처 체크 ────────────────────────────────
        if gc.get("start_x") is None:
            self._log(
                "[실행불가] 시작좌표가 캡처되지 않았습니다. "
                "좌표 자동계산 섹션에서 📸 캡처 버튼으로 시작좌표를 먼저 설정하세요.",
                "ERROR")
            return

        grid_coords = filter_valid_coords(
            calculate_coordinates(sx, sy, ch, col, row, cw, sdir))

        if not grid_coords:
            self._log(
                "[실행불가] 좌표 계산 결과가 없습니다. "
                "시작좌표·행/열 수·셀 크기 설정을 확인하세요.",
                "ERROR")
            return

        total = len(grid_coords)

        # ── 입력창 좌표 검증 ──────────────────────────────────
        mi   = self.tmpl.get("message_input_coord", {})
        mi_x = safe_int(mi.get("x"))
        mi_y = safe_int(mi.get("y"))
        if input_method == "coord" and (not mi_x or not mi_y):
            self._log(
                "[실행불가] 입력 방식이 '좌표클릭'인데 입력창 좌표 미설정. "
                "전송·닫기 섹션에서 입력창 좌표를 캡처하거나 "
                "'바로입력'으로 변경하세요.",
                "ERROR")
            return

        # ── 이미지 방식 + 필수값 검증 ───────────────────────
        img_mode = self.tmpl.get("image_mode", "file")
        if img_mode == "none": use_img = False
        if use_img:
            if img_mode == "file":
                if not (img_path and Path(img_path).exists()):
                    self._log(
                        f"[실행불가] 이미지 첨부 방식이 '파일경로'인데 "
                        f"파일이 없습니다 ({img_path!r}).",
                        "ERROR")
                    return
            else:   # dragdrop
                src_c = self.tmpl.get("image_source_coord", {})
                drp_c = self.tmpl.get("image_drop_coord",   {})
                if not (src_c.get("x") and src_c.get("y")):
                    self._log(
                        "[실행불가] 드래그 앤 드롭 소스 좌표가 설정되지 않았습니다.",
                        "ERROR")
                    return
                if not (drp_c.get("x") and drp_c.get("y")):
                    self._log(
                        "[실행불가] 드래그 앤 드롭 드롭 좌표가 설정되지 않았습니다.",
                        "ERROR")
                    return

        # ── 시작 로그 ─────────────────────────────────────
        self._log(
            f"▶ 오픈채팅/아침인사/가망뿌리기 시작 — 총 {total}건 ({col}열×{row}행)",
            "INFO")
        self._log(
            f"  설정: 입력={input_method} / 전송={send_method} / "
            f"닫기={'ON('+close_method+')' if close_after else 'OFF'}",
            "INFO")
        self._log(
            f"  딜레이: 열림={oc_after_open}s / 클릭={oc_after_click}s / "
            f"입력={oc_after_type}s / 전송={oc_after_send}s / "
            f"닫기={oc_after_close}s / 간격={between}s±{jitter_s}s",
            "INFO")
        if use_img:
            self._log(
                f"  이미지: 모드={img_mode} / 순서={img_order} / "
                f"경로={img_path!r}",
                "INFO")

        # ── 이중전송 방지: 마지막으로 발송한 좌표 추적 ──────
        _last_sent_coord = None

        for idx in range(total):
            if self._is_stopped():
                self._log("사용자 중지", "WARN")
                break

            self._progress(idx + 1, total)
            msg = self._apply_vars(message, {})
            gx, gy = grid_coords[idx]

            # ── 이중전송 가드 ──────────────────────────────
            if _last_sent_coord == (gx, gy):
                self._log(
                    f"  ⚠️ [{idx+1}/{total}] 좌표({gx},{gy})가 직전 발송과 동일 — "
                    "닫기후(s) 딜레이를 늘리거나 좌표를 확인하세요.",
                    "WARN")

            self._log(f"[{idx+1}/{total}] 좌표({gx},{gy}) 발송 시작")

            try:
                # ① 채팅창 더블클릭
                self._log(f"  ① 더블클릭 → ({gx},{gy})")
                pyautogui.doubleClick(gx, gy)
                self._log(f"  ↳ 채팅창 열림 대기 {oc_after_open}s ...")
                if self._sleep_or_stop(oc_after_open): return  # BUG-03 fix

                # ② 이미지 첨부 — 메시지 전
                if use_img and img_order == "before":
                    self._log("  ② 이미지 첨부 (before) 시작")
                    try:
                        self._drag_drop_image(img_path=img_path,
                                              delays=img_delays,
                                              stop_event=self._stop)
                    except pyautogui.FailSafeException:
                        raise
                    except Exception as e:
                        self._log(f"  ⚠️ 이미지 첨부 실패(before): {e}", "WARN")

                # ③ 메시지 입력
                if input_method == "coord":
                    self._log(f"  ③ 입력창 클릭 → ({mi_x},{mi_y})")
                    pyautogui.click(mi_x, mi_y)
                    self._log(f"  ↳ 클릭 후 대기 {oc_after_click}s ...")
                    if self._sleep_or_stop(oc_after_click): return  # BUG-03 fix
                else:
                    self._log(f"  ③ 바로입력 모드 — 포커스 대기 {oc_after_click}s ...")
                    if self._sleep_or_stop(oc_after_click): return  # BUG-03 fix
                self._log(f"  ↳ 메시지 입력 ({len(msg)}자)")
                self._type(msg)
                self._log(f"  ↳ 입력 후 대기 {oc_after_type}s ...")
                if self._sleep_or_stop(oc_after_type): return  # BUG-03 fix

                # ④ 전송
                if send_method == "enter":
                    self._log("  ④ 전송 — Enter")
                    self._hotkey("return")
                elif send_method == "ctrl_enter":
                    self._log("  ④ 전송 — Ctrl+Enter")
                    self._hotkey("ctrl", "return")
                else:   # click_btn
                    sc = self.tmpl.get("send_btn_coord", {})
                    if sc.get("x") and sc.get("y"):
                        bx, by = safe_int(sc["x"]), safe_int(sc["y"])
                        self._log(f"  ④ 전송 — 버튼 클릭 ({bx},{by})")
                        pyautogui.click(bx, by)
                    else:
                        self._log("  ④ ⚠️ 전송버튼 좌표 미설정 → Enter 대체", "WARN")
                        self._hotkey("return")
                self._log(f"  ↳ 전송 후 대기 {oc_after_send}s ...")
                if self._sleep_or_stop(oc_after_send): return  # BUG-03 fix

                # ⑤ 이미지 첨부 — 메시지 후
                if use_img and img_order == "after":
                    self._log("  ⑤ 이미지 첨부 (after) 시작")
                    try:
                        self._drag_drop_image(img_path=img_path,
                                              delays=img_delays,
                                              stop_event=self._stop)
                    except pyautogui.FailSafeException:
                        raise
                    except Exception as e:
                        self._log(f"  ⚠️ 이미지 첨부 실패(after): {e}", "WARN")

                # ⑥ 창 닫기
                if close_after:
                    if close_method == "esc":
                        self._log("  ⑥ 창 닫기 — ESC")
                        pyautogui.press("escape")
                    elif close_method == "altf4":
                        self._log("  ⑥ 창 닫기 — Alt+F4")
                        pyautogui.hotkey("alt", "f4")
                    else:   # click_btn
                        cc = self.tmpl.get("close_btn_coord", {})
                        if cc.get("x") and cc.get("y"):
                            cx, cy = safe_int(cc["x"]), safe_int(cc["y"])
                            self._log(f"  ⑥ 창 닫기 — 버튼 클릭 ({cx},{cy})")
                            pyautogui.click(cx, cy)
                        else:
                            self._log("  ⑥ ⚠️ 닫기버튼 좌표 미설정 → ESC 대체", "WARN")
                            pyautogui.press("escape")
                    self._log(f"  ↳ 닫기 후 대기 {oc_after_close}s ... (이중전송 방지)")
                    if self._sleep_or_stop(oc_after_close): return  # BUG-03 fix

                _last_sent_coord = (gx, gy)
                self._succ += 1
                self._log(f"  ✅ [{idx+1}/{total}] 완료", "SUCCESS")

            except pyautogui.FailSafeException:
                self._fail += 1
                self._log("  ❌ FailSafe 발동 → 작업 중단", "ERROR")
                self._log("  💡 마우스를 화면 중앙에 두고 재실행하세요.", "WARN")
                if self._ss_on_error: self._capture_screen("error_failsafe")
                break
            except Exception as e:
                self._fail += 1
                self._log(f"  ❌ 실패: {e}", "ERROR")
                if self._ss_on_error: self._capture_screen("error")
                try:
                    mx, my = pyautogui.position()
                    sw = pyautogui.size()
                    if mx > 5 and my > 5 and mx < sw[0]-5 and my < sw[1]-5:
                        pyautogui.press("escape")
                except Exception:
                    pass

            if idx < total - 1:
                gap_t = between + jitter_s * random.uniform(0.7, 1.3)
                self._log(f"  ↳ 다음 방 이동 전 대기 {gap_t:.2f}s ...")
                if self._sleep_or_stop(gap_t): return  # BUG-03 fix

        self._log(f"▶ 완료 — 성공:{self._succ} / 실패:{self._fail}", "SUCCESS")

    # ════════════════════════════════════════════════════════
    # 텔레그램 그룹 가입
    # ════════════════════════════════════════════════════════
    def _run_telegram_join(self):
        """텔레그램 그룹 가입  [v1.61 TG-5 — Telethon 우선, pyautogui 폴백]

        · Telethon 설치됨 + 계정 설정 있음  → TelethonEngine 사용
        · Telethon 미설치 or 계정 없음       → 기존 pyautogui 방식
        """
        # ── [TG-5] Telethon 라우팅 ────────────────────────────
        if HAS_TELETHON:
            tg_accounts = load_json(TG_ACCOUNTS_PATH, [])
            if tg_accounts:
                # ★ 작업에 assigned_accounts 가 있으면 해당 계정만 필터링
                _assigned = self.job.get("assigned_accounts", [])
                if _assigned:
                    tg_accounts = [a for a in tg_accounts
                                   if TelethonEngine._normalize_phone(
                                       a.get("phone", "")) in _assigned]
                    self._log(f"[TG] 지정 계정 {len(tg_accounts)}개로 실행 "
                              f"(전체 중 {len(_assigned)}개 선택됨)")
                if tg_accounts:
                    self._used_telethon = True   # ★ 실제 Telethon 경로 진입 확정
                    self._run_telegram_join_telethon(tg_accounts)
                    return
                else:
                    self._log("[TG] 선택된 계정이 없거나 매칭 실패 → pyautogui 폴백", "WARN")
            else:
                self._log("[TG] Telethon 설치됨 — 계정 없음 → pyautogui 폴백 실행\n"
                          "     텔레그램 계정 탭에서 계정을 추가하면 API 방식으로 자동 전환됩니다.",
                          "WARN")
        else:
            self._log("[TG] Telethon 미설치 → pyautogui(크롬 자동화) 방식으로 실행\n"
                      "     pip install telethon 으로 설치하면 더 안정적인 API 방식을 사용할 수 있습니다.",
                      "INFO")

        # ── 폴백: 기존 pyautogui 방식 ─────────────────────────
        if not HAS_PYAUTOGUI:
            self._log("pyautogui 가 필요합니다. (Telethon 미설치 + pyautogui 없음)", "ERROR")
            return

        rows  = self._read_targets()
        total = len(rows)

        if not rows:
            self._log("대상 목록이 비어 있습니다.", "WARN")
            return

        self._log(f"텔레그램 그룹 가입 시작 (pyautogui 모드) — "
                  f"총 {total}개", "INFO")

        for idx, row in enumerate(rows):
            if self._is_stopped():
                self._log("사용자 중지", "WARN")
                break

            self._progress(idx+1, total)
            link = str(row.get("텔레그램링크",
                       row.get("link", ""))).strip()

            if not link:
                self._log("  ⚠️ 링크 없음 스킵", "WARN")
                self._fail += 1
                continue

            self._log(f"[{idx+1}/{total}] 가입: {link}")

            try:
                result = self._telegram_join_once(link)
                if result == "success":
                    self._succ += 1
                    self._log("  ✅ 가입 완료", "SUCCESS")
                elif result == "already":
                    self._succ += 1
                    self._log("  ℹ️ 이미 가입됨", "INFO")
                else:
                    self._fail += 1
                    self._log("  ❌ 가입 실패", "ERROR")

            except Exception as e:
                self._fail += 1
                self._log(f"  ❌ 오류: {e}", "ERROR")

            tg_min = safe_float(self.tmpl.get("tg_between_min", 3.0))
            tg_max = safe_float(self.tmpl.get("tg_between_max", 7.0))
            if self._sleep_or_stop(random.uniform(tg_min, tg_max)): return

        self._log(
            f"완료 — 성공:{self._succ} / 실패:{self._fail}",
            "SUCCESS")

    def _run_telegram_join_telethon(self, accounts: list):
        """Telethon 엔진으로 그룹 가입 — Zigzag 모드 (기본)  [v1.61 TG-5]

        account_mode 에 따라 분배:
          zigzag (기본) : 계정을 순환하며 링크 한 개씩 가입
          split         : 링크 목록을 계정 수로 균등 분배
          all           : 모든 계정이 전체 링크 목록 가입
        """
        rows  = self._read_targets()
        total = len(rows)
        if not rows:
            self._log("대상 목록이 비어 있습니다.", "WARN"); return

        mode = self.tmpl.get("account_mode", "zigzag")
        self._log(
            f"[Telethon] 그룹 가입 시작 — 총 {total}개 / "
            f"계정 {len(accounts)}개 / 모드: {mode}", "INFO")

        def _log_fn(msg, lv="INFO"):
            self._log(msg, lv)

        eng = _get_tg_engine(_log_fn)
        eng.load_accounts(accounts)

        # ── 계정 사전 연결 ─────────────────────────────────
        active_accounts = []
        for acct in accounts:
            if eng.connect(acct):
                active_accounts.append(acct)
        if not active_accounts:
            self._log("연결 가능한 계정이 없습니다. "
                      "텔레그램 계정 탭에서 연결 테스트를 먼저 진행하세요.",
                      "ERROR")
            return

        tg_min  = safe_float(self.tmpl.get("tg_between_min", 3.0))
        tg_max  = safe_float(self.tmpl.get("tg_between_max", 7.0))
        sw_dly  = safe_float(self.tmpl.get("account_switch_delay", 1.0))
        n_accts = len(active_accounts)

        # [v1.84] 실제 적용되는 링크 간격 로그 출력 (설정 미반영 문제 디버깅용)
        self._log(
            f"  ⏱ 링크 간격: {tg_min}s ~ {tg_max}s  "
            f"(템플릿: {self.tmpl.get('name','?')})", "INFO")
        if tg_min < 10:
            self._log(
                f"  ⚠️ 링크 간격이 {tg_min}s로 매우 짧습니다. "
                f"FROZEN 위험 — 템플릿 저장 후 재실행하세요.", "WARN")

        def _join_one(acct, link, idx, total_cnt):
            """단일 가입 시도 + FROZEN/FloodStop 즉시 감지 반환
            반환: 'ok' | 'fail' | 'frozen' | 'flood_stopped'
            """
            phone = eng._normalize_phone(acct.get("phone", ""))
            ok = eng.join_group(acct, link, self._stop)
            if ok:
                self._succ += 1
                _r = self._record(link, "성공")
                if self._report_rows: self._report_rows[-1]["계정"] = acct.get("name", "")
                return "ok"
            else:
                self._fail += 1
                _r = self._record(link, "실패")
                if self._report_rows: self._report_rows[-1]["계정"] = acct.get("name", "")
                # FROZEN / FloodStop 여부 확인 → 즉시 루프 탈출 신호
                if eng.is_frozen(phone):
                    self._log(
                        f"[{acct.get('name','')}] 🚨 FROZEN 감지 — 해당 계정 루프 중단",
                        "ERROR")
                    return "frozen"
                if eng.is_flood_stopped(phone):
                    self._log(
                        f"[{acct.get('name','')}] 🛑 FloodWait 당일 중단 — 해당 계정 루프 중단",
                        "ERROR")
                    return "flood_stopped"
                return "fail"

        if mode == "zigzag":
            # 계정 순환: link[0]→acct[0], link[1]→acct[1], ...
            # FROZEN/FloodStop 계정 추적 (zigzag는 계정이 섞이므로 per-account 관리)
            _skip_phones: set = set()
            for idx, row in enumerate(rows):
                if self._is_stopped(): break
                self._progress(idx+1, total)
                link = str(row.get("텔레그램링크",
                           row.get("link", ""))).strip()
                if not link:
                    self._fail += 1; continue
                acct = active_accounts[idx % n_accts]
                phone = eng._normalize_phone(acct.get("phone", ""))
                # 이미 FROZEN/FloodStop 된 계정은 즉시 스킵
                if phone in _skip_phones:
                    self._fail += 1
                    self._record(link, "실패")
                    continue
                self._log(f"[{idx+1}/{total}] [{acct['name']}] 가입: {link}")
                result = _join_one(acct, link, idx, total)
                if result in ("frozen", "flood_stopped"):
                    _skip_phones.add(phone)
                    # 모든 계정이 중단됐으면 루프 탈출
                    if len(_skip_phones) >= n_accts:
                        self._log("모든 계정 FROZEN/FloodStop — 가입 루프 종료", "ERROR")
                        break
                    continue  # 딜레이 없이 다음 링크(다른 계정)로
                # [v1.86 fix] 링크 간격은 항상 tg_min~tg_max 적용
                # 계정 경계(마지막 계정 → 첫 계정 순환) 시에만 추가로 sw_dly
                # n_accts=1 이면 매 링크마다 tg_min~tg_max 대기 (이전 코드는
                # n_accts=1 시 항상 sw_dly=1초만 적용되어 FROZEN 발생)
                if self._sleep_or_stop(random.uniform(tg_min, tg_max)): break
                if n_accts > 1 and idx % n_accts == n_accts - 1:
                    if self._sleep_or_stop(sw_dly): break

        elif mode == "split":
            chunk = max(1, (total + n_accts - 1) // n_accts)
            for i, acct in enumerate(active_accounts):
                if self._is_stopped(): break
                phone = eng._normalize_phone(acct.get("phone", ""))
                segment = rows[i*chunk : (i+1)*chunk]
                for idx, row in enumerate(segment):
                    if self._is_stopped(): break
                    link = str(row.get("텔레그램링크",
                               row.get("link", ""))).strip()
                    if not link:
                        self._fail += 1; continue
                    abs_idx = i*chunk + idx
                    self._progress(abs_idx+1, total)
                    self._log(f"[{abs_idx+1}/{total}] [{acct['name']}] 가입: {link}")
                    result = _join_one(acct, link, abs_idx, total)
                    if result in ("frozen", "flood_stopped"):
                        break  # 이 계정 세그먼트 즉시 탈출
                    if self._sleep_or_stop(
                            random.uniform(tg_min, tg_max)): break

        else:  # all — 모든 계정이 전체 링크 처리
            for acct in active_accounts:
                if self._is_stopped(): break
                self._log(f"[{acct['name']}] 전체 {total}개 가입 시작")
                for idx, row in enumerate(rows):
                    if self._is_stopped(): break
                    link = str(row.get("텔레그램링크",
                               row.get("link", ""))).strip()
                    if not link:
                        self._fail += 1; continue
                    self._progress(idx+1, total)
                    result = _join_one(acct, link, idx, total)
                    if result in ("frozen", "flood_stopped"):
                        break  # 이 계정 루프 즉시 탈출
                    if self._sleep_or_stop(
                            random.uniform(tg_min, tg_max)): break
                if self._sleep_or_stop(sw_dly): break

        self._log(f"[Telethon] 완료 — 성공:{self._succ} / 실패:{self._fail}",
                  "SUCCESS")

    def _telegram_join_once(self, link: str) -> str:
        tg_chrome  = safe_float(self.tmpl.get("tg_chrome_load",   2.0))
        tg_open    = safe_float(self.tmpl.get("tg_telegram_open", 1.5))
        tg_join    = safe_float(self.tmpl.get("tg_join_click",    2.0))
        try:
            # 1) 크롬 주소창 클릭 + 링크 입력
            self._click("chrome_addr")
            time.sleep(0.3)
            pyautogui.hotkey("ctrl", "a")
            self._type(link)
            self._hotkey("return")
            if self._sleep_or_stop(tg_chrome): return "stopped"  # BUG-03 fix

            # 2) 가입 버튼 클릭
            self._click("join_btn")
            if self._sleep_or_stop(tg_join): return "stopped"  # BUG-03 fix

            # 3) 탭 닫기
            self._click("close_tab")
            time.sleep(tg_open)

            return "success"

        except Exception as e:
            self._log(f"    가입 오류: {e}", "ERROR")
            try:
                pyautogui.press("escape")
            except: pass
            return "error"

    # ════════════════════════════════════════════════════════
    # [REMOVED v1.46] telegram_join_msg → telegram_message + join_first 통합
    # [BUG-01 fix v1.61] 고아 코드(orphaned body) 104줄 삭제
    # ════════════════════════════════════════════════════════

    # ════════════════════════════════════════════════════════
    # 텔레그램 메시지 발송
    # ════════════════════════════════════════════════════════
    def _run_telegram_message(self):
        """텔레그램 메시지 발송  [v1.61 TG-5 — Telethon 우선, pyautogui 폴백]"""
        # ── [TG-5] Telethon 라우팅 ────────────────────────────
        if HAS_TELETHON:
            tg_accounts = load_json(TG_ACCOUNTS_PATH, [])
            if tg_accounts:
                # ★ 작업에 assigned_accounts 가 있으면 해당 계정만 필터링
                _assigned = self.job.get("assigned_accounts", [])
                if _assigned:
                    tg_accounts = [a for a in tg_accounts
                                   if TelethonEngine._normalize_phone(
                                       a.get("phone", "")) in _assigned]
                    self._log(f"[TG] 지정 계정 {len(tg_accounts)}개로 실행 "
                              f"(전체 중 {len(_assigned)}개 선택됨)")
                if tg_accounts:
                    self._used_telethon = True   # ★ 실제 Telethon 경로 진입 확정
                    self._run_telegram_message_telethon(tg_accounts)
                    return
                else:
                    self._log("[TG] 선택된 계정이 없거나 매칭 실패 → pyautogui 폴백", "WARN")
            else:
                self._log("[TG] Telethon 설치됨 — 계정 없음 → pyautogui 폴백 실행\n"
                          "     텔레그램 계정 탭에서 계정을 추가하면 API 방식으로 자동 전환됩니다.",
                          "WARN")
        else:
            self._log("[TG] Telethon 미설치 → pyautogui(크롬 자동화) 방식으로 실행\n"
                      "     pip install telethon 으로 설치하면 더 안정적인 API 방식을 사용할 수 있습니다.",
                      "INFO")

        # ── 폴백: 기존 pyautogui 방식 ─────────────────────────
        if not HAS_PYAUTOGUI:
            self._log("pyautogui 가 필요합니다. (Telethon 미설치 + pyautogui 없음)", "ERROR")
            return

        rows    = self._read_targets()
        total   = len(rows)
        message = self.tmpl.get("message") or self.job.get("message", "")
        if not rows:
            return

        # ── 이미지 설정 읽기 ────────────────────────────────
        use_img  = self.tmpl.get("use_image", False)
        img_mode = self.tmpl.get("image_mode", "none")
        img_path = self.tmpl.get("image_path", "")
        if use_img and img_mode == "file":
            if not (img_path and Path(img_path).exists()):
                self._log(f"[실행불가] 파일경로 모드인데 파일 없음 ({img_path!r}). "
                          "이미지 경로를 설정하거나 이미지 첨부를 끄세요.", "ERROR")
                return
        # ── 전송/닫기 방식 읽기 ─────────────────────────────
        send_method  = self.tmpl.get("send_method",  "enter")
        close_after  = self.tmpl.get("close_after_send", True)
        close_method = self.tmpl.get("close_method", "esc")

        tg_chrome = safe_float(self.tmpl.get("tg_chrome_load", 2.0))
        tg_type   = safe_float(self.tmpl.get("tg_after_type",  0.5))
        tg_send   = safe_float(self.tmpl.get("tg_after_send",  1.0))
        tg_back   = safe_float(self.tmpl.get("tg_after_back",  0.8))
        tg_min    = safe_float(self.tmpl.get("tg_between_min", 3.0))
        tg_max    = safe_float(self.tmpl.get("tg_between_max", 7.0))

        join_first = self.tmpl.get("join_first", False)
        tg_join    = safe_float(self.tmpl.get("tg_join_click", 2.0))

        self._log(f"텔레그램 메시지 발송 시작 — 총 {total}명  "
                  f"[이미지:{img_mode if use_img else 'none'} / "
                  f"가입:{join_first} / "
                  f"전송:{send_method} / 닫기:{close_method}]", "INFO")

        for idx, row in enumerate(rows):
            if self._is_stopped():
                self._log("사용자 중지", "WARN"); break

            self._progress(idx+1, total)
            link = str(row.get("텔레그램링크", row.get("link", ""))).strip()
            msg  = self._apply_vars(message, row)
            if not link:
                self._fail += 1
                self._log("  ⚠️ 링크 없음 스킵", "WARN"); continue

            self._log(f"[{idx+1}/{total}] {link}")
            try:
                # ① 크롬 주소창 → 링크 입력 → 엔터
                self._click("chrome_addr")
                time.sleep(0.3)
                pyautogui.hotkey("ctrl", "a")
                self._type(link)
                self._hotkey("return")
                if self._sleep_or_stop(tg_chrome): return  # BUG-03 fix

                # ① 가입 버튼 클릭 (join_first=True인 경우)
                if join_first:
                    jb = self.tmpl.get("join_btn_coord") or {}
                    jb_x = safe_int(jb.get("x", 0))
                    jb_y = safe_int(jb.get("y", 0))
                    if jb_x and jb_y:
                        pyautogui.click(jb_x, jb_y)
                        self._log("  [가입버튼] 클릭")
                        time.sleep(tg_join)
                    else:
                        self._log("  ⚠️ join_btn_coord 미설정 → 가입 단계 건너뜀", "WARN")

                # ② 이미지 첨부 (클립보드) — 파일을 클립보드에 올린 뒤 Ctrl+V
                if use_img and img_mode == "clipboard":
                    _cb_ok = False
                    if img_path and Path(img_path).exists():
                        try:
                            from PIL import Image as _CbImg
                            import io as _CbIO
                            try:
                                import win32clipboard as _w32cb
                                _img = _CbImg.open(img_path)
                                _buf = _CbIO.BytesIO()
                                _img.convert("RGB").save(_buf, "BMP")
                                _bmp = _buf.getvalue()[14:]
                                _buf.close()
                                _w32cb.OpenClipboard()
                                _w32cb.EmptyClipboard()
                                _w32cb.SetClipboardData(_w32cb.CF_DIB, _bmp)
                                _w32cb.CloseClipboard()
                                _cb_ok = True
                                self._log(f"  [클립보드] 이미지 복사 완료: {Path(img_path).name}")
                            except ImportError:
                                # win32clipboard 없을 때 pyperclip 대체 (텍스트 경로)
                                self._log("  ⚠️ win32clipboard 미설치 — Ctrl+C 방식으로 대체", "WARN")
                                import pyperclip as _pc
                                _pc.copy(str(img_path))
                                _cb_ok = True
                        except Exception as _cbe:
                            self._log(f"  ⚠️ 클립보드 이미지 복사 실패: {_cbe}", "WARN")
                    else:
                        self._log("  ⚠️ 클립보드 모드인데 이미지 경로 없음 — 첨부 건너뜀", "WARN")
                    if _cb_ok:
                        time.sleep(0.3)   # 클립보드 안착 대기
                        pyautogui.hotkey("ctrl", "v")
                        time.sleep(tg_type)

                # ③ 이미지 첨부 (파일경로)
                elif use_img and img_mode == "file":
                    try:
                        self._tg_attach_file(img_path, tg_type)
                    except WorkflowExecutor._DialogSkipError as _dse:
                        self._fail += 1
                        self._log(f"  ⚠️ {_dse} → 다음 항목으로 건너뜀", "WARN")
                        continue

                # ④ 텍스트 입력 + 전송
                #    텔레그램 전용: tg_message_input_coord / tg_input_method
                tg_im     = self.tmpl.get("tg_input_method", "direct")
                tg_mi     = self.tmpl.get("tg_message_input_coord", {})
                tg_mi_x   = safe_int(tg_mi.get("x", 0))
                tg_mi_y   = safe_int(tg_mi.get("y", 0))
                if tg_im == "coord":
                    if not tg_mi_x or not tg_mi_y:
                        raise RuntimeError(
                            "좌표 미설정: 'tg_message_input_coord' "
                            f"(x={tg_mi_x}, y={tg_mi_y})  "
                            "→ 템플릿에서 입력창 좌표를 먼저 캡처하세요.")
                    pyautogui.click(tg_mi_x, tg_mi_y)
                    time.sleep(0.3)
                else:
                    # 바로입력: 링크 열린 후 입력창 자동 포커스
                    time.sleep(0.2)
                self._type(msg)
                time.sleep(tg_type)
                self._tg_send(send_method, tg_send)

                # ⑤ 닫기
                if close_after:
                    self._tg_close(close_method, tg_back)

                self._succ += 1
                self._log("  ✅ 발송 완료", "SUCCESS")

            except Exception as e:
                self._fail += 1
                self._log(f"  ❌ 오류: {e}", "ERROR")
                if self._ss_on_error: self._capture_screen("error")
                try: pyautogui.press("escape")
                except: pass

            if self._sleep_or_stop(random.uniform(tg_min, tg_max)): return  # BUG-03 fix

        self._log(f"완료 — 성공:{self._succ} / 실패:{self._fail}", "SUCCESS")

    # ════════════════════════════════════════════════════════
    # 텔레그램 가입 후 메시지 발송 (v1.68)
    # ════════════════════════════════════════════════════════
    def _run_telegram_join_and_message(self):
        """텔레그램 그룹/채널 가입 후 메시지 발송  [v1.68 — Telethon 우선, pyautogui 폴백]

        · 각 대상마다 join_group → send_message 순서로 실행
        · Telethon: join_group() + send_message() API 직접 호출
        · pyautogui 폴백: join_first=True 로 _run_telegram_message() 위임
        """
        # ── [TG-5] Telethon 라우팅 ────────────────────────────
        if HAS_TELETHON:
            tg_accounts = load_json(TG_ACCOUNTS_PATH, [])
            if tg_accounts:
                _assigned = self.job.get("assigned_accounts", [])
                if _assigned:
                    tg_accounts = [a for a in tg_accounts
                                   if TelethonEngine._normalize_phone(
                                       a.get("phone", "")) in _assigned]
                    self._log(f"[TG] 지정 계정 {len(tg_accounts)}개로 실행 "
                              f"(전체 중 {len(_assigned)}개 선택됨)")
                if tg_accounts:
                    self._used_telethon = True   # ★ 실제 Telethon 경로 진입 확정
                    self._run_telegram_join_and_message_telethon(tg_accounts)
                    return
                else:
                    self._log("[TG] 선택된 계정이 없거나 매칭 실패 → pyautogui 폴백", "WARN")
            else:
                self._log("[TG] Telethon 설치됨 — 계정 없음 → pyautogui 폴백 실행\n"
                          "     텔레그램 계정 탭에서 계정을 추가하면 API 방식으로 자동 전환됩니다.",
                          "WARN")
        else:
            self._log("[TG] Telethon 미설치 → pyautogui(크롬 자동화) 방식으로 실행\n"
                      "     pip install telethon 으로 설치하면 더 안정적인 API 방식을 사용할 수 있습니다.",
                      "INFO")

        # ── 폴백: join_first=True 강제 설정 후 기존 pyautogui 방식 위임 ──
        if not HAS_PYAUTOGUI:
            self._log("pyautogui 가 필요합니다. (Telethon 미설치 + pyautogui 없음)", "ERROR")
            return
        # 템플릿에 join_first 강제 적용 (폴백 시 가입 버튼 클릭 활성화)
        self.tmpl = dict(self.tmpl)
        self.tmpl["join_first"] = True
        self._log("[폴백] join_first=True 로 강제 설정 후 pyautogui 메시지 발송 실행", "INFO")
        self._run_telegram_message()

    def _run_telegram_join_and_message_telethon(self, accounts: list):
        """Telethon — 그룹/채널 가입 후 메시지 발송  [v1.68]

        각 대상 링크마다:
          1) join_group()   — 채널/그룹 가입
          2) send_message() — 메시지 발송
        가입 실패 시 해당 대상 건너뜀 (메시지 미발송).
        """
        rows    = self._read_targets()
        total   = len(rows)
        message = self.tmpl.get("message") or self.job.get("message", "")
        if not rows:
            self._log("대상 목록이 비어 있습니다.", "WARN"); return
        if not message:
            self._log("메시지가 비어 있습니다.", "ERROR"); return

        # ── 이미지 첨부 설정 ──────────────────────────────────
        use_img  = self.tmpl.get("use_image", False)
        img_mode = self.tmpl.get("image_mode", "none")
        img_path = self.tmpl.get("image_path", "").strip() if use_img else ""
        if use_img and img_mode == "file" and img_path:
            import os as _os
            if not _os.path.isfile(img_path):
                self._log(f"⚠️ 이미지 파일 없음: {img_path} — 이미지 없이 진행", "WARN")
                img_path = ""
        elif use_img and img_mode == "clipboard":
            self._log("⚠️ Telethon 모드에서 클립보드 첨부는 지원 안됨. "
                      "파일 경로 방식을 사용하세요.", "WARN")
            img_path = ""
        else:
            img_path = ""

        # ── 딜레이 설정 ────────────────────────────────────────
        api_connect_dly = safe_float(self.tmpl.get("tg_api_connect_delay", 2.0))
        api_before_send = safe_float(self.tmpl.get("tg_api_before_send",   0.5))
        api_after_send  = safe_float(self.tmpl.get("tg_api_after_send",    1.0))
        api_join_delay  = safe_float(self.tmpl.get("tg_join_click",        2.0))  # 가입 후 대기
        api_capture_dly = safe_float(self.tmpl.get("tg_api_capture_delay", 2.0))
        api_capture_n   = int(safe_float(self.tmpl.get("tg_api_capture_msgs", 5), 5))
        api_capture_on  = bool(self.tmpl.get("tg_api_capture_on", False))
        api_warmup_add  = safe_float(self.tmpl.get("tg_api_acct_warmup",   0.5))
        pre_check_acct  = bool(self.tmpl.get("tg_pre_check_acct", True))
        pre_check_perm  = bool(self.tmpl.get("tg_pre_check_perm", True))
        tg_min  = safe_float(self.tmpl.get("tg_between_min", 3.0))
        tg_max  = safe_float(self.tmpl.get("tg_between_max", 7.0))
        sw_dly  = safe_float(self.tmpl.get("account_switch_delay", 1.0))

        mode = self.tmpl.get("account_mode", "zigzag")
        self._log(
            f"[Telethon] 가입+메시지 발송 시작 — 총 {total}개 / "
            f"계정 {len(accounts)}개 / 모드: {mode}", "INFO")

        def _log_fn(msg, lv="INFO"):
            self._log(msg, lv)

        eng = _get_tg_engine(_log_fn)
        eng.load_accounts(accounts)

        # ── 계정 사전 연결 ─────────────────────────────────────
        active_accounts = []
        for i, acct in enumerate(accounts):
            if i > 0 and api_connect_dly > 0:
                time.sleep(api_connect_dly)
            if eng.connect(acct):
                active_accounts.append(acct)
        if not active_accounts:
            self._log("연결 가능한 계정이 없습니다.", "ERROR"); return

        n_accts = len(active_accounts)

        def _do_join_and_send(acct, peer, msg, idx, total_cnt):
            """단일 대상: 가입 → 메시지 발송"""
            self._log(f"[{idx+1}/{total_cnt}] [{acct.get('name','')}] → {peer}")

            # ① 가입
            join_ok = eng.join_group(acct, peer, self._stop)
            if not join_ok:
                self._fail += 1
                self._record(peer, "실패")
                if self._report_rows:
                    self._report_rows[-1]["계정"] = acct.get("name", "")
                    self._report_rows[-1]["비고"] = "가입 실패"
                return False

            self._log(f"  ✅ 가입 완료 — {api_join_delay}s 대기 후 메시지 발송", "INFO")
            time.sleep(api_join_delay)  # 가입 후 대기 (서버 반영)

            # ② 메시지 발송
            if api_before_send > 0:
                time.sleep(api_before_send)
            result = eng.send_message(acct, peer, msg, self._stop,
                                      img_path=img_path,
                                      pre_check_acct=pre_check_acct,
                                      pre_check_perm=pre_check_perm)
            ok     = result.get("ok", False)
            msg_id = result.get("msg_id")

            if ok:
                self._succ += 1
                self._record(peer, "성공")
            else:
                self._fail += 1
                self._record(peer, "실패")
                if self._report_rows:
                    self._report_rows[-1]["비고"] = "가입 성공 / 메시지 실패"
            if self._report_rows:
                self._report_rows[-1]["계정"] = acct.get("name", "")
                if msg_id:
                    self._report_rows[-1]["msg_id"] = str(msg_id)

            if api_after_send > 0:
                time.sleep(api_after_send)
            if ok and api_capture_on:
                self._tg_capture_chat(eng, acct, peer,
                                      capture_delay=api_capture_dly,
                                      n_msgs=api_capture_n,
                                      sent_msg_id=msg_id)
            return ok

        # ── 모드별 실행 ────────────────────────────────────────
        if mode == "zigzag":
            for idx, row in enumerate(rows):
                if self._is_stopped(): break
                peer = str(row.get("텔레그램링크",
                           row.get("link",
                           row.get("username", "")))).strip()
                if not peer:
                    self._fail += 1; continue
                acct = active_accounts[idx % n_accts]
                self._progress(idx+1, total,
                               acct=acct.get("name", ""),
                               peer=peer)
                msg = self._apply_vars(message, row)
                _do_join_and_send(acct, peer, msg, idx, total)
                if n_accts > 1 and idx % n_accts == n_accts - 1:
                    if self._sleep_or_stop(sw_dly + api_warmup_add): break
                else:
                    if self._sleep_or_stop(random.uniform(tg_min, tg_max)): break

        elif mode == "split":
            chunk = max(1, (total + n_accts - 1) // n_accts)
            for i, acct in enumerate(active_accounts):
                if self._is_stopped(): break
                if i > 0:
                    if self._sleep_or_stop(sw_dly + api_warmup_add): break
                segment = rows[i*chunk : (i+1)*chunk]
                for idx, row in enumerate(segment):
                    if self._is_stopped(): break
                    peer = str(row.get("텔레그램링크",
                               row.get("link",
                               row.get("username", "")))).strip()
                    if not peer:
                        self._fail += 1; continue
                    abs_idx = i*chunk + idx
                    self._progress(abs_idx+1, total,
                                   acct=acct.get("name", ""),
                                   peer=peer)
                    msg = self._apply_vars(message, row)
                    _do_join_and_send(acct, peer, msg, abs_idx, total)
                    if self._sleep_or_stop(random.uniform(tg_min, tg_max)): break

        else:  # all
            for i, acct in enumerate(active_accounts):
                if self._is_stopped(): break
                if i > 0:
                    if self._sleep_or_stop(sw_dly + api_warmup_add): break
                self._log(f"[{acct.get('name','')}] 전체 {total}개 가입+발송 시작")
                for idx, row in enumerate(rows):
                    if self._is_stopped(): break
                    peer = str(row.get("텔레그램링크",
                               row.get("link",
                               row.get("username", "")))).strip()
                    if not peer:
                        self._fail += 1; continue
                    self._progress(idx+1, total,
                                   acct=acct.get("name", ""),
                                   peer=peer)
                    msg = self._apply_vars(message, row)
                    _do_join_and_send(acct, peer, msg, idx, total)
                    if self._sleep_or_stop(random.uniform(tg_min, tg_max)): break

        self._log(f"[Telethon] 가입+메시지 완료 — 성공:{self._succ} / 실패:{self._fail}",
                  "SUCCESS")

    def _run_telegram_message_telethon(self, accounts: list):
        """Telethon 엔진으로 메시지 발송 — 단계별 딜레이 + 채팅 캡처  [v1.61 TG-5]"""
        rows    = self._read_targets()
        total   = len(rows)
        message = self.tmpl.get("message") or self.job.get("message", "")
        if not rows:
            self._log("대상 목록이 비어 있습니다.", "WARN"); return
        if not message:
            self._log("메시지가 비어 있습니다.", "ERROR"); return

        # ── 이미지 첨부 설정 ──────────────────────────────────
        use_img  = self.tmpl.get("use_image", False)
        img_mode = self.tmpl.get("image_mode", "none")
        img_path = self.tmpl.get("image_path", "").strip() if use_img else ""
        if use_img and img_mode == "file" and img_path:
            import os as _os
            if not _os.path.isfile(img_path):
                self._log(f"⚠️ 이미지 파일 없음: {img_path} — 이미지 없이 진행", "WARN")
                img_path = ""
            else:
                self._log(f"📎 이미지 첨부 모드: {img_path}", "INFO")
        elif use_img and img_mode == "clipboard":
            self._log("⚠️ Telethon 모드에서 클립보드 첨부는 지원 안됨. "
                      "파일 경로 방식을 사용하세요.", "WARN")
            img_path = ""
        else:
            img_path = ""

        # ── API 단계별 딜레이 읽기 ────────────────────────────
        api_connect_dly = safe_float(self.tmpl.get("tg_api_connect_delay", 2.0))
        api_before_send = safe_float(self.tmpl.get("tg_api_before_send",   0.5))
        api_after_send  = safe_float(self.tmpl.get("tg_api_after_send",    1.0))
        api_capture_dly = safe_float(self.tmpl.get("tg_api_capture_delay", 2.0))
        api_capture_n   = int(safe_float(self.tmpl.get("tg_api_capture_msgs", 5), 5))
        api_capture_on  = bool(self.tmpl.get("tg_api_capture_on", False))
        api_warmup_add  = safe_float(self.tmpl.get("tg_api_acct_warmup",   0.5))
        # ── 발송 전 사전 체크 ON/OFF (UI 체크박스 → 템플릿 저장값) ──
        pre_check_acct  = bool(self.tmpl.get("tg_pre_check_acct", True))
        pre_check_perm  = bool(self.tmpl.get("tg_pre_check_perm", True))
        tg_min  = safe_float(self.tmpl.get("tg_between_min", 3.0))
        tg_max  = safe_float(self.tmpl.get("tg_between_max", 7.0))
        sw_dly  = safe_float(self.tmpl.get("account_switch_delay", 1.0))
        # ── [v1.69 BUG-FIX] join_first 체크박스 값 반영 ──────────────
        # 이전: _run_telegram_message_telethon 이 join_first 를 완전히 무시
        # 수정: 체크 시 send_message 전 join_group() 먼저 호출
        join_first     = bool(self.tmpl.get("join_first", False))
        api_join_delay = safe_float(self.tmpl.get("tg_join_click", 2.0))

        mode = self.tmpl.get("account_mode", "zigzag")
        self._log(
            f"[Telethon] 메시지 발송 시작 — 총 {total}명 / "
            f"계정 {len(accounts)}개 / 모드: {mode}"
            + (f" / 이미지: {img_path}" if img_path else "")
            + (f" / 가입후발송: {'ON' if join_first else 'OFF'}")
            + (f" / 채팅캡처: {'ON' if api_capture_on else 'OFF'}"), "INFO")
        self._log(
            f"  딜레이 — 연결:{api_connect_dly}s / 발송전:{api_before_send}s / "
            f"발송후:{api_after_send}s / 캡처대기:{api_capture_dly}s / "
            f"링크간격:{tg_min}~{tg_max}s / 계정전환:{sw_dly}s", "INFO")

        def _log_fn(msg, lv="INFO"):
            self._log(msg, lv)

        eng = _get_tg_engine(_log_fn)
        eng.load_accounts(accounts)

        # ── 계정 사전 연결 (연결 딜레이 적용) ─────────────────
        active_accounts = []
        for i, acct in enumerate(accounts):
            if i > 0 and api_connect_dly > 0:
                time.sleep(api_connect_dly)  # 계정 간 연결 딜레이
            if eng.connect(acct):
                active_accounts.append(acct)
        if not active_accounts:
            self._log("연결 가능한 계정이 없습니다.", "ERROR")
            return

        n_accts = len(active_accounts)

        def _do_send_one(acct, peer, msg, idx, total_cnt):
            """단일 발송 + 캡처 + 딜레이 처리"""
            self._log(f"[{idx+1}/{total_cnt}] [{acct.get('name','')}] → {peer}")

            # ── [v1.69 BUG-FIX] join_first=True 시 가입 먼저 수행 ────
            if join_first:
                _jf_phone = eng._normalize_phone(acct.get("phone", ""))
                self._log(f"  [가입 후 발송] join_group 시도 → {peer}")
                join_ok = eng.join_group(acct, peer, self._stop)
                # [v1.86 BUG-FIX] join 후 즉시 FROZEN/FloodStop 체크 — 성공 여부와 무관하게
                if eng.is_frozen(_jf_phone):
                    self._log(
                        f"  🚨 가입 후 FROZEN 감지 — [{acct.get('name','')}] 발송 중단",
                        "ERROR")
                    self._fail += 1
                    self._record(peer, "실패")
                    if self._report_rows:
                        self._report_rows[-1]["계정"] = acct.get("name", "")
                        self._report_rows[-1]["비고"] = "FROZEN (join_first 후)"
                    return "frozen"   # 호출자가 루프 탈출 처리
                if eng.is_flood_stopped(_jf_phone):
                    self._log(
                        f"  🛑 가입 후 FloodStop 감지 — [{acct.get('name','')}] 발송 중단",
                        "ERROR")
                    self._fail += 1
                    self._record(peer, "실패")
                    if self._report_rows:
                        self._report_rows[-1]["계정"] = acct.get("name", "")
                        self._report_rows[-1]["비고"] = "FloodStop (join_first 후)"
                    return "flood_stopped"
                if not join_ok:
                    self._fail += 1
                    self._record(peer, "실패")
                    if self._report_rows:
                        self._report_rows[-1]["계정"] = acct.get("name", "")
                        self._report_rows[-1]["비고"] = "가입 실패 (join_first)"
                    return False
                self._log(f"  ✅ 가입 완료 — {api_join_delay}s 대기 후 메시지 발송")
                time.sleep(api_join_delay)

            # 발송 전 딜레이
            if api_before_send > 0:
                time.sleep(api_before_send)
            result  = eng.send_message(acct, peer, msg, self._stop,
                                       img_path=img_path,
                                       pre_check_acct=pre_check_acct,
                                       pre_check_perm=pre_check_perm)
            ok      = result.get("ok", False)
            msg_id  = result.get("msg_id")          # ★ 메시지 ID
            if ok:
                self._succ += 1
                self._record(peer, "성공")
            else:
                self._fail += 1
                self._record(peer, "실패")
            if self._report_rows:
                self._report_rows[-1]["계정"]   = acct.get("name", "")
                if msg_id:
                    self._report_rows[-1]["msg_id"] = str(msg_id)   # ★ 전용 컬럼
            # 발송 후 딜레이
            if api_after_send > 0:
                time.sleep(api_after_send)
            # 발송 후 채팅 캡처 (성공 시만) — sent_msg_id 전달로 정확한 캡처
            if ok and api_capture_on:
                self._tg_capture_chat(eng, acct, peer,
                                      capture_delay=api_capture_dly,
                                      n_msgs=api_capture_n,
                                      sent_msg_id=msg_id)
            return ok

        if mode == "zigzag":
            _msg_skip_phones: set = set()   # [v1.86] FROZEN/FloodStop 계정 추적
            for idx, row in enumerate(rows):
                if self._is_stopped(): break
                peer = str(row.get("텔레그램링크",
                           row.get("link",
                           row.get("username", "")))).strip()
                if not peer:
                    self._fail += 1; continue
                acct = active_accounts[idx % n_accts]
                _ms_phone = eng._normalize_phone(acct.get("phone", ""))
                # [v1.86] 이미 FROZEN/FloodStop된 계정이면 즉시 스킵
                if _ms_phone in _msg_skip_phones:
                    self._fail += 1
                    self._record(peer, "실패")
                    continue
                self._progress(idx+1, total,
                               acct=acct.get("name", ""),
                               peer=peer)
                msg  = self._apply_vars(message, row)
                _send_result = _do_send_one(acct, peer, msg, idx, total)
                # [v1.86] join_first FROZEN/FloodStop 즉시 탈출
                if _send_result in ("frozen", "flood_stopped"):
                    _msg_skip_phones.add(_ms_phone)
                    if len(_msg_skip_phones) >= n_accts:
                        self._log("모든 계정 FROZEN/FloodStop — 발송 루프 종료", "ERROR")
                        break
                    continue  # 딜레이 없이 다음 링크(다른 계정)로
                # [CRIT-04 fix] 계정 경계에서 sw_dly 또는 tg_min~max 중 하나만
                if n_accts > 1 and idx % n_accts == n_accts - 1:
                    # 계정 전환 시 warmup 추가
                    if self._sleep_or_stop(sw_dly + api_warmup_add): break
                else:
                    if self._sleep_or_stop(
                            random.uniform(tg_min, tg_max)): break

        elif mode == "split":
            chunk = max(1, (total + n_accts - 1) // n_accts)
            for i, acct in enumerate(active_accounts):
                if self._is_stopped(): break
                if i > 0:
                    if self._sleep_or_stop(sw_dly + api_warmup_add): break
                segment = rows[i*chunk : (i+1)*chunk]
                for idx, row in enumerate(segment):
                    if self._is_stopped(): break
                    peer = str(row.get("텔레그램링크",
                               row.get("link",
                               row.get("username", "")))).strip()
                    if not peer:
                        self._fail += 1; continue
                    abs_idx = i*chunk + idx
                    self._progress(abs_idx+1, total,
                                   acct=acct.get("name", ""),
                                   peer=peer)
                    msg = self._apply_vars(message, row)
                    _sr = _do_send_one(acct, peer, msg, abs_idx, total)
                    if _sr in ("frozen", "flood_stopped"):
                        break  # 이 계정 세그먼트 즉시 탈출
                    if self._sleep_or_stop(
                            random.uniform(tg_min, tg_max)): break

        else:  # all
            for i, acct in enumerate(active_accounts):
                if self._is_stopped(): break
                if i > 0:
                    if self._sleep_or_stop(sw_dly + api_warmup_add): break
                self._log(f"[{acct.get('name','')}] 전체 {total}명 발송 시작")
                for idx, row in enumerate(rows):
                    if self._is_stopped(): break
                    peer = str(row.get("텔레그램링크",
                               row.get("link",
                               row.get("username", "")))).strip()
                    if not peer:
                        self._fail += 1; continue
                    self._progress(idx+1, total,
                                   acct=acct.get("name", ""),
                                   peer=peer)
                    msg = self._apply_vars(message, row)
                    _sr = _do_send_one(acct, peer, msg, idx, total)
                    if _sr in ("frozen", "flood_stopped"):
                        break  # 이 계정 루프 즉시 탈출
                    if self._sleep_or_stop(
                            random.uniform(tg_min, tg_max)): break

        self._log(f"[Telethon] 완료 — 성공:{self._succ} / 실패:{self._fail}",
                  "SUCCESS")

    # ── 텔레그램 공통 유틸 ──────────────────────────────────
    def _tg_send(self, send_method: str, delay: float):
        """텔레그램 전송 방식 실행"""
        if send_method == "enter":
            self._hotkey("return")
        elif send_method == "ctrl_enter":
            self._hotkey("ctrl", "return")
        else:   # click_btn
            sc = self.tmpl.get("send_btn_coord", {})
            if sc.get("x") and sc.get("y"):
                pyautogui.click(safe_int(sc["x"]), safe_int(sc["y"]))
            else:
                self._log("  ⚠️ 전송버튼 좌표 미설정 → Enter 대체", "WARN")
                self._hotkey("return")
        time.sleep(delay)


    # ── 파일 다이얼로그 열림 대기 (재시도 포함) ───────────────
    class _DialogSkipError(RuntimeError):
        """첨부 버튼 재시도 횟수 초과 — 해당 항목 skip 용"""

    def _tg_wait_dialog(self, ab_x: int, ab_y: int,
                        d_dialog: float, max_retry: int = 3) -> None:
        """첨부 버튼 클릭 후 파일 다이얼로그가 열렸는지 확인.
        포그라운드 창 타이틀 변화를 감지해 판정한다.
        max_retry 회 모두 실패 시 _DialogSkipError 발생.

        감지 우선순위:
          1) win32gui  — GetForegroundWindow / GetWindowText
          2) pygetwindow — getActiveWindowTitle
          3) fallback — 단순 대기 후 성공 간주 (감지 불가 환경)

        성공 판정 조건 (화이트리스트):
          창 타이틀에 다음 키워드 중 하나 이상 포함 시에만 성공
          'Choose Files', '열기', 'Open', '파일 선택', '파일 열기',
          'Select File', '파일', 'File'
          → 그 외 변화(응답 없음, 다른 톡방, 앱 전환 등)는 모두 실패
        """
        # ── 포그라운드 창 타이틀 읽기 함수 구성 ──────────────
        def _make_get_title():
            """win32gui → pygetwindow 순으로 폴백하여 타이틀 함수 반환"""
            try:
                import win32gui as _wg
                def _fn():
                    try:
                        return _wg.GetWindowText(_wg.GetForegroundWindow())
                    except Exception:
                        return ""
                return _fn
            except ImportError:
                pass
            try:
                import pygetwindow as _pgw
                def _fn():
                    try:
                        return _pgw.getActiveWindowTitle() or ""
                    except Exception:
                        return ""
                return _fn
            except ImportError:
                pass
            return None

        _get_title = _make_get_title()

        # ── 감지 불가 환경: 단순 대기 후 성공 간주 ───────────
        if _get_title is None:
            self._log("  ⚠️ [첨부버튼] 창 감지 라이브러리 없음 → 단순 대기", "WARN")
            pyautogui.click(ab_x, ab_y)
            time.sleep(d_dialog)
            return

        # ── 재시도 루프 ───────────────────────────────────────
        for attempt in range(1, max_retry + 1):
            before_title = _get_title()

            pyautogui.click(ab_x, ab_y)
            self._log(
                f"  [첨부버튼] 클릭 시도 {attempt}/{max_retry} "
                f"(현재창: {before_title!r})")

            # ── 파일 다이얼로그 화이트리스트 키워드 ──────────────
            _DIALOG_KW = (
                "Choose Files", "열기", "Open", "파일 선택",
                "파일 열기", "Select File", "파일", "File",
            )

            # 최대 d_dialog 초 동안 0.3 초 간격으로 폴링
            elapsed   = 0.0
            poll      = 0.3
            opened    = False
            while elapsed < d_dialog:
                time.sleep(poll)
                elapsed += poll
                after_title = _get_title()
                # 화이트리스트 키워드 포함 여부로 성공 판정
                is_dialog = any(kw in after_title for kw in _DIALOG_KW)
                if is_dialog:
                    self._log(
                        f"  ✅ [첨부버튼] 다이얼로그 열림 확인 "
                        f"(새 창: {after_title!r})")
                    opened = True
                    break
                elif after_title != before_title:
                    # 타이틀은 바뀌었지만 다이얼로그가 아님 (오판정 방지)
                    self._log(
                        f"  ⚠️ [첨부버튼] 타이틀 변화 감지됐으나 다이얼로그 아님 "
                        f"({after_title!r}) — 계속 폴링", "WARN")

            if opened:
                return   # 성공 → 호출부에서 이후 로직 진행

            # 실패 — ESC 없이 0.5초 대기 후 재시도 (톡방 유지)
            self._log(
                f"  ⚠️ [첨부버튼] 다이얼로그 미감지 "
                f"(시도 {attempt}/{max_retry}) — 재시도", "WARN")
            time.sleep(0.5)

        # 3회 모두 실패
        raise WorkflowExecutor._DialogSkipError(
            f"첨부 버튼 {max_retry}회 재시도 후 다이얼로그 미열림 → 항목 skip")

    def _tg_close(self, close_method: str, delay: float):
        """텔레그램 닫기 방식 실행 (ESC / Alt+F4 / 버튼클릭)"""
        if close_method == "esc" or close_method == "ctrlw":
            # ctrlw 는 구버전 호환용 — esc 와 동일 처리
            pyautogui.press("escape")
        elif close_method == "altf4":
            pyautogui.hotkey("alt", "f4")
        else:   # click_btn
            cc = self.tmpl.get("close_btn_coord", {})
            if cc.get("x") and cc.get("y"):
                pyautogui.click(safe_int(cc["x"]), safe_int(cc["y"]))
            else:
                self._log("  ⚠️ 닫기버튼 좌표 미설정 → ESC 대체", "WARN")
                pyautogui.press("escape")
        time.sleep(delay)

    def _tg_attach_file(self, img_path: str, delay: float):
        """텔레그램 파일경로 첨부 (텔레그램 전용 로직)
        순서:
          ① tg_attach_btn_coord 클릭 → 파일다이얼로그 열림
          ② Alt+D 로 주소창 포커스
          ③ 폴더 경로 Ctrl+A → Ctrl+V → Enter (폴더 이동)
          ④ tg_filename_input_coord 좌표 클릭 (파일명 입력란)
          ⑤ 파일명 Ctrl+A → Ctrl+V → Enter (파일 선택+열기)
        딜레이는 image_delays.file_* 키 우선, 없으면 delay 인자 사용
        """
        from pathlib import Path as _P
        p      = _P(img_path)
        folder = str(p.parent)
        fname  = p.name

        # 파일경로 전용 딜레이 읽기
        d = self.tmpl.get("image_delays", {})
        d_dialog = safe_float(d.get("file_dialog_open", 0), 0) or delay
        d_folder = safe_float(d.get("file_folder_move", 0), 0) or delay * 0.8
        d_open   = safe_float(d.get("file_after_open",  0), 0) or delay * 0.5

        # ① 첨부 버튼 클릭 → 다이얼로그 열림 확인 (최대 3회 재시도)
        ab = self.tmpl.get("tg_attach_btn_coord", {})
        ab_x = safe_int(ab.get("x", 0))
        ab_y = safe_int(ab.get("y", 0))
        if not ab_x or not ab_y:
            self._log(
                "  ❌ [파일첨부] tg_attach_btn_coord 미설정 (x=0, y=0). "
                "템플릿에서 📎 파일첨부 버튼 좌표를 먼저 캡처하세요.",
                "ERROR")
            raise RuntimeError("tg_attach_btn_coord 미설정")
        # _tg_wait_dialog: 클릭 + 폴링 + 3회 재시도 포함
        # DialogSkipError 발생 시 호출부에서 해당 항목 skip
        self._tg_wait_dialog(ab_x, ab_y, d_dialog, max_retry=3)

        try:
            import pyperclip as _pc

            # ② Alt+D → 파일다이얼로그 주소창 포커스
            pyautogui.hotkey("alt", "d")
            time.sleep(d_dialog * 0.4)

            # ③ 폴더 경로 입력 → Enter (폴더 이동)
            _pc.copy(folder)
            pyautogui.hotkey("ctrl", "a")
            pyautogui.hotkey("ctrl", "v")
            time.sleep(d_dialog * 0.3)
            pyautogui.press("return")
            time.sleep(d_folder)       # 폴더 이동 대기

            # ④ 파일명 입력란 좌표 클릭 (tg_filename_input_coord)
            fn = self.tmpl.get("tg_filename_input_coord", {})
            fn_x = safe_int(fn.get("x", 0))
            fn_y = safe_int(fn.get("y", 0))
            if not fn_x or not fn_y:
                self._log(
                    "  ❌ [파일첨부] tg_filename_input_coord 미설정 (x=0, y=0). "
                    "템플릿에서 파일명 입력란 좌표를 먼저 캡처하세요.",
                    "ERROR")
                raise RuntimeError("tg_filename_input_coord 미설정")
            pyautogui.click(fn_x, fn_y)
            time.sleep(d_open * 0.5)

            # ⑤ 파일명 입력 → Enter (파일 선택+열기)
            _pc.copy(fname)
            pyautogui.hotkey("ctrl", "a")
            pyautogui.hotkey("ctrl", "v")
            time.sleep(d_open * 0.3)
            pyautogui.press("return")
            time.sleep(d_open)         # 파일 열기 완료 대기

            self._log(f"  [이미지] 파일 다이얼로그 첨부 완료: {fname}")
        except RuntimeError:
            raise
        except Exception as e:
            self._log(f"  ⚠️ 파일 첨부 실패: {e}", "WARN")
            raise

    # ── 공통 유틸 ────────────────────────────────────────────
    def _apply_vars(self, text: str, row: dict) -> str:
        """메시지 변수 치환 + 랜덤 토큰"""
        return resolve_name_number(text, row)

    def _drag_drop_image(self, img_path: str = "",
                          src_coord: dict = None,
                          drop_coord: dict = None,
                          delays: dict = None,
                          stop_event=None):
        """이미지 드래그 앤 드롭 (kakao_drag_drop 방식)
        src_coord  : {"x":..., "y":...} 이미지 소스 위치
        drop_coord : {"x":..., "y":...} 채팅창 입력 위치
        delays     : after_image_click / after_drag_start / after_drop / after_enter
        """
        d = delays or {}
        # 소스/드롭 좌표 결정
        sc = src_coord  or self.tmpl.get("image_source_coord") or {}
        dc = drop_coord or self.tmpl.get("image_drop_coord")              or self.coords.get("image_drop_target", {})
        sx = sc.get("x", 0)
        sy = sc.get("y", 0)
        tx = dc.get("x", 0)
        ty = dc.get("y", 0)

        def _chk():
            return stop_event and stop_event.is_set()

        # ★ 드롭 대상 좌표도 0,0이면 클립보드 방식으로만 진행
        if tx == 0 and ty == 0:
            self._log("[이미지] 드롭 대상 좌표 미설정 → 클립보드 방식으로 전환", "WARN")
            sc = {}  # 소스 좌표를 비워 클립보드 경로로 유도

        if not (sx or sy):
            # 소스 좌표 없으면 클립보드 방식으로 폴백
            if img_path and Path(img_path).exists():
                try:
                    from PIL import Image as _Img
                    import io
                    try:
                        import win32clipboard
                    except ImportError:
                        self._log("[이미지] win32clipboard 미설치 → 클립보드 전송 불가", "WARN")
                        return
                    img = _Img.open(img_path)
                    output = io.BytesIO()
                    img.convert("RGB").save(output, "BMP")
                    data_bmp = output.getvalue()[14:]
                    output.close()
                    win32clipboard.OpenClipboard()
                    win32clipboard.EmptyClipboard()
                    win32clipboard.SetClipboardData(
                        win32clipboard.CF_DIB, data_bmp)
                    win32clipboard.CloseClipboard()
                    # ★ BUG-A: tx/ty==0 이면 FailSafe 발동 → 드롭 좌표 있을 때만 클릭
                    if tx and ty:
                        pyautogui.click(tx, ty)
                        time.sleep(d.get("after_image_click", 0.3))
                    pyautogui.hotkey("ctrl", "v")
                    time.sleep(d.get("after_enter", 0.8))
                    self._log(f"[이미지] ✅ 클립보드 전송 완료  드롭좌표=({tx},{ty})")
                    return
                except Exception as e:
                    self._log(f"[이미지] 클립보드 실패: {e}", "WARN")
            else:
                self._log("[이미지] 소스 좌표 및 파일 경로 없음 → 건너뜀", "WARN")
            return

        # v1.52: 각 단계별 상세 로그 추가
        self._log(f"[이미지] 드래그 앤 드롭 시작  소스({sx},{sy}) → 드롭({tx},{ty})")

        if _chk(): return
        _d1 = d.get("after_image_click", 0.5)
        self._log(f"  ↳ 소스 좌표 이동 ({sx},{sy}), 대기 {_d1}s")
        pyautogui.moveTo(sx, sy, duration=0.05)
        time.sleep(_d1)

        if _chk(): return
        _d2 = d.get("after_drag_start", 0.2)
        self._log(f"  ↳ 마우스 누름(드래그 시작), 대기 {_d2}s")
        pyautogui.mouseDown()
        time.sleep(_d2)

        if _chk():
            pyautogui.mouseUp()
            return
        self._log(f"  ↳ 드롭 위치({tx},{ty})로 이동 중 ...")
        pyautogui.moveTo(tx, ty, duration=0.3)

        if _chk():
            pyautogui.mouseUp()
            return
        _d3 = d.get("after_drop", 0.3)
        self._log(f"  ↳ 마우스 놓음(드롭 완료), 대기 {_d3}s")
        pyautogui.mouseUp()
        time.sleep(_d3)

        if _chk(): return
        _d4 = d.get("after_enter", 0.5)
        self._log(f"  ↳ Enter 전송, 대기 {_d4}s")
        pyautogui.press("enter")
        time.sleep(_d4)

        self._log("[이미지] ✅ 드래그 앤 드롭 완료")
# ============================================================
# PostingEngine — 큐 기반 단일 워커 실행 엔진  [v1.54 신규 — CHANGE-03]
# community_poster v5.20 벤치마킹
# ============================================================

class PostingEngine:
    """
    queue.Queue 기반 단일 워커 실행 엔진  [v1.54 신규 — CHANGE-03]

    설계 배경
    ---------
    v1.53 까지는 작업마다 JobWorker(Thread) 를 생성하는 멀티워커 구조였으나
    pyautogui (마우스·키보드) 는 단일 물리 자원이므로 동시 실행 시 입력 충돌
    발생. 실제 _run_all() 도 내부에서 done_event.wait() 로 순차 처리하도록
    우회하고 있었으므로 멀티워커 구조를 유지할 이유가 없었음.

    구조
    ----
    add_task() 로 (job, template, callbacks) 튜플을 queue.Queue 에 적재
    → _worker() 루프가 1개씩 꺼내 WorkflowExecutor.run() 블로킹 실행
    → 완료 후 다음 항목 처리 (단일 스레드 직렬 보장)

    상태 관리
    ---------
    · _busy / _idle : threading.Event 쌍 (is_busy 프로퍼티로 외부 관찰)
    · _current_name : 현재 실행 중인 작업 이름 (None 이면 idle)
    · _current_stop : 현재 작업의 stop_event (cancel_job 에서 set 호출)

    취소 지원
    ---------
    · cancel_job(name) :
        대기 중 → _cancelled set 에 등록 → worker 가 skip 후 discard
        실행 중 → _current_stop.set() → _sleep_or_stop() 가 True 반환 후 return
    · drain() / stop() : 전체 중지 (큐 비우기 + 현재 작업 중단)
    """
    def __init__(self, cancelled_jobs: set):
        self.q                             = queue.Queue()
        self._busy                         = threading.Event()
        self._idle                         = threading.Event()
        self._idle.set()
        self.running                       = False
        self._stopping                     = False  # v1.77: 중지 신호
        self._cancelled                    = cancelled_jobs   # JobsTab과 공유
        self._current_name: str | None     = None
        self._current_stop: threading.Event | None = None
        self._thread: threading.Thread | None      = None

    def start(self):
        self.running = True
        self._thread = threading.Thread(
            target=self._worker, daemon=True)
        self._thread.start()

    def stop(self):
        """전체 중지: 큐 비우기 + 현재 실행 업무 중단"""
        self._stopping = True         # v1.77: 중지 신호 (running은 worker가 확인)
        self.drain()
        if self._current_stop:
            self._current_stop.set()
        self._idle.set()              # v1.77: wait_until_idle() 블로킹 해제

    def drain(self):
        """대기 중인 작업 전부 제거"""
        while not self.q.empty():
            try:
                self.q.get_nowait()
                self.q.task_done()
            except queue.Empty:
                break

    def add_task(self, job: dict, template: dict,
                 log_fn, progress_fn, done_fn):
        """작업을 큐에 추가"""
        # v1.77: stop 후 재실행 시 worker 재시작
        if self._stopping or not self.running:
            self._stopping = False
            self.running   = True
            self._thread   = threading.Thread(
                target=self._worker, daemon=True)
            self._thread.start()
        # 큐 적재 전 idle 이벤트 미리 clear — race condition 방지
        # add_task → wait_until_idle 즉시 호출 시 worker가 아직 busy 세팅
        # 전이면 idle 상태 그대로라 대기 없이 통과하는 버그 수정
        self._idle.clear()
        self._busy.set()
        self.q.put((job, template, log_fn, progress_fn, done_fn))

    def cancel_job(self, name: str):
        """개별 작업 취소.
        대기 중: _cancelled set에 등록 → worker가 skip.
        실행 중: stop_event 신호 전송.
        """
        self._cancelled.add(name)
        if self._current_name == name and self._current_stop:
            self._current_stop.set()

    @property
    def is_busy(self) -> bool:
        return self._busy.is_set()

    def wait_until_idle(self, timeout=None):
        # v1.77: q.join() 기반으로 교체 — 큐에 남은 모든 task_done() 완료 대기
        # 기존 _idle.wait() 는 race condition 으로 조기 종료될 수 있었음
        if timeout is None:
            self.q.join()
        else:
            import threading as _th_wait
            _done = _th_wait.Event()
            def _waiter():
                self.q.join()
                _done.set()
            _th_wait.Thread(target=_waiter, daemon=True).start()
            _done.wait(timeout)

    def _worker(self):
        while self.running and not self._stopping:
            try:
                job, tmpl, log_fn, progress_fn, done_fn =                     self.q.get(timeout=1)
            except queue.Empty:
                continue

            name = job.get("name", "")

            # 취소된 작업이면 skip
            if name in self._cancelled:
                self._cancelled.discard(name)
                self.q.task_done()
                continue

            # 실행 시작
            self._busy.set()
            self._idle.clear()
            self._current_name = name
            self._current_stop = threading.Event()

            executor = WorkflowExecutor(
                job         = job,
                template    = tmpl,
                log_fn      = log_fn,
                progress_fn = progress_fn,
                done_fn     = done_fn,
                stop_event  = self._current_stop,
            )
            executor.run()          # 블로킹 (단일 스레드라 OK)

            self.q.task_done()
            self._current_name = None
            self._current_stop = None

            # 큐가 비면 idle 상태로 전환
            if self.q.empty():
                self._busy.clear()
                self._current_name = None
                self._current_stop = None
                self._idle.set()


# ── JobsTab 실행 메서드 (monkey-patch) ──────────────────────

def _jobs_run_selected(self):
    """선택된 작업 단일 실행"""
    j = self._get_selected_job()
    if not j:
        messagebox.showwarning("선택 없음",
            "실행할 작업을 선택하세요.")
        return
    self._run_job(j)


def _jobs_run_all(self):
    """활성 작업 전체 순차 실행  [v1.54: engine 큐에 일괄 추가 — CHANGE-09]
                                 [v1.55: 비활성 작업 스킵 추가 — CHANGE-A6]
                                 [v1.69: 순차 반복(repeat_count) 지원 추가]

    repeat_count > 0 인 작업이 하나라도 있으면 별도 daemon thread 에서
    순환 실행. engine 의 wait_until_idle() 로 1순환 완료를 대기한 후
    repeat_interval 초 쉬고 다음 순환을 진행.

    · repeat_count = 0  → 무제한 반복 (중지 버튼으로만 종료)
    · repeat_count = 1  → 1회 실행 (반복 없음, 기존 동작)
    · repeat_count = N  → N회 반복 후 자동 종료
    · repeat_interval   → 전체 1순환 완료 후 다음 순환 전 대기(초)
    """
    if not self._jobs:
        messagebox.showwarning("작업 없음",
            "등록된 작업이 없습니다.")
        return

    # ── v1.55 CHANGE-A6: 비활성 작업 필터링 ─────────────────────────
    active_jobs = [j for j in self._jobs if j.get("enabled", True)]
    if not active_jobs:
        messagebox.showwarning("활성 작업 없음",
            "활성화된 작업이 없습니다.\n"
            "⊙ 활성 토글 버튼으로 작업을 활성화하세요.")
        return

    # ── v1.69/v1.73: 반복 설정 확인 ─────────────────────────────────
    # repeat_on=True 이고 repeat_count != 1 인 작업이 하나라도 있으면 반복 모드
    # repeat_on=False 이면 repeat_count 값과 관계없이 1회 실행
    def _is_repeat_job(j):
        if not j.get("repeat_on", False):
            return False
        rc = j.get("repeat_count", 1)
        return rc != 1  # 0(무제한) 또는 2+ 이면 반복

    _any_repeat = any(_is_repeat_job(j) for j in active_jobs)

    if not _any_repeat:
        # ── 기존 동작: 1회 순차 실행 ────────────────────────────────
        for j in active_jobs:
            self._run_job(j)
        return

    # ── 반복 실행 모드 ───────────────────────────────────────────────
    import threading as _th_repeat
    import time as _t_repeat

    # 반복 횟수: repeat_on=True 이고 repeat_count > 1 인 작업만 유한 반복
    # 0 = 무제한, 1 = 1회(기본·비반복), 2+ = N회
    _finite = [j.get("repeat_count", 1) for j in active_jobs
               if _is_repeat_job(j) and j.get("repeat_count", 1) > 1]
    _max_rounds = max(_finite) if _finite else 0  # 0 = 무제한

    # 순환 간 대기: repeat_on=True 인 작업들 중 최대 interval
    _gap = max((j.get("repeat_interval", 0) for j in active_jobs
                if j.get("repeat_on", False)), default=0)

    # 중지 이벤트: _stop_all 시 engine.stop()이 호출되므로 그것으로 감지
    _stop_flag = [False]

    def _repeat_loop():
        _round = 0
        while True:
            _round += 1
            _label = f"{_round}" if _max_rounds == 0 else f"{_round}/{_max_rounds}"

            # ── 이번 순환에 실행할 작업 결정 ────────────────────────
            # repeat_on=False  → 첫 라운드만 실행 (비반복 작업)
            # repeat_on=True, rc=0  → 무제한 반복
            # repeat_on=True, rc=1  → 첫 라운드만 (1회)
            # repeat_on=True, rc>1  → N라운드까지
            jobs_this_round = []
            for j in active_jobs:
                rc = j.get("repeat_count", 1)
                ron = j.get("repeat_on", False)
                if not ron:                        # 반복 OFF → 1라운드만
                    if _round == 1:
                        jobs_this_round.append(j)
                elif rc == 0:                      # 무제한 반복
                    jobs_this_round.append(j)
                elif rc == 1 and _round == 1:      # 1회만
                    jobs_this_round.append(j)
                elif rc > 1 and _round <= rc:      # N회
                    jobs_this_round.append(j)
                # rc > 1 and _round > rc → 횟수 소진, 스킵

            if not jobs_this_round:
                # 모든 작업이 횟수 소진 → 반복 종료
                break

            # UI 상태 로그
            self.after(0, lambda r=_label: self.app._set_status(
                f"🔁 [{r}순환] 작업 {len(jobs_this_round)}개 시작"))
            if hasattr(self.app, "_log_tab"):
                self.after(0, lambda r=_label, n=len(jobs_this_round):
                    self.app._log_tab.append(
                        f"[반복실행] {r}순환 시작 — {n}개 작업",
                        "INFO", "반복실행"))

            # 이번 순환 작업 큐 적재
            for j in jobs_this_round:
                self._run_job(j)

            # engine 이 이번 순환 모두 완료할 때까지 대기
            self._engine.wait_until_idle(timeout=None)

            # 엔진이 stop 됐으면 (중지 버튼) 루프 종료
            if self._engine._stopping or not self._engine.running:
                break

            # 최대 횟수 도달 판단
            if _max_rounds > 0 and _round >= _max_rounds:
                self.after(0, lambda: self.app._set_status(
                    "✅ 반복 실행 완료"))
                if hasattr(self.app, "_log_tab"):
                    self.after(0, lambda r=_max_rounds:
                        self.app._log_tab.append(
                            f"[반복실행] 전체 {r}순환 완료",
                            "INFO", "반복실행"))
                break

            # 순환 간 대기
            if _gap > 0:
                self.after(0, lambda g=_gap: self.app._set_status(
                    f"⏳ 다음 순환까지 {g}초 대기 중…"))
                _t_repeat.sleep(_gap)

            # 대기 중 엔진 stop 됐으면 종료
            if self._engine._stopping or not self._engine.running:
                break

    _th = _th_repeat.Thread(target=_repeat_loop, daemon=True,
                            name="repeat-runner-v169")
    _th.start()


def _jobs_run_job(self, job: dict, silent: bool = False):
    """단일 작업 큐 추가  [v1.54: PostingEngine 방식 — CHANGE-10]
                           [v1.57: silent 파라미터 추가 — BUG-FIX-01]

    BUG-FIX-01 (v1.57)
    ------------------
    이전(v1.56): 스케줄러 자동 실행 시 messagebox.showinfo/showerror 팝업 발생
      → 야간 무인 실행 중 팝업이 쌓이면 다음 틱 블록, 사용자 경험 저하
    변경(v1.57): silent=True 시 messagebox 대신 LogTab에 경고 기록만
      → _scheduler_tick에서 자동 실행 시 항상 silent=True로 호출
    """
    name = job.get("name", "")

    # 현재 실행 중인 작업과 동일하면 알림
    if self._engine._current_name == name:
        if silent:
            # 자동 실행 시: 팝업 없이 로그만 기록
            if hasattr(self.app, "_log_tab"):
                self.app._log_tab.append(
                    f"[스케줄 스킵] [{name}] 이미 실행 중",
                    "WARN", "스케줄러")
        else:
            self.app._set_status(f"⚠️ [{name}] 이미 실행 중입니다.")
        return

    # BUG-04 수정: _migrate_template 포함 로드
    tmpl = self._load_template_for_job(job)
    if not tmpl:
        if silent:
            if hasattr(self.app, "_log_tab"):
                self.app._log_tab.append(
                    f"[스케줄 오류] [{name}] 템플릿 \"{job.get('template_name','')}\" 없음",
                    "ERROR", "스케줄러")
        else:
            messagebox.showerror("템플릿 오류",
                f"템플릿 [{job.get('template_name','')}]"
                " 을 찾을 수 없습니다.")
        return

    # UI 콜백 정의
    def _log(msg, level="INFO"):
        self.after(0, lambda:
            self.app._log_tab.append(
                msg, level, source=name)
            if hasattr(self.app, "_log_tab") else None)
        self.after(0, lambda:
            self.app._set_status(msg[:60]))

    def _progress(cur, total, acct="", peer=""):
        """진행률 + 현재 처리 대상 UI 업데이트"""
        pct   = (cur / total * 100) if total > 0 else 0
        label = f"▶ {name}"
        self.after(0, lambda p=pct, lb=label: self.set_progress(p, lb))
        self.after(0, lambda a=acct, pe=peer, c=cur, t=total:
                   self.set_target(a, pe, c, t))

    def _done(succ, fail):
        self.after(0, lambda:
            self._on_job_done(name, succ, fail))

    # 상태: 대기 중 → 큐 추가 (engine worker가 실행 시 🟢로 전환)
    # v1.60 STEP-3: 시작 타임스탬프 기록 (ETA 정확도용)
    import time as _t_eta_stamp
    self._run_started_at = _t_eta_stamp.monotonic()
    self._update_job_status(name, "🟢 실행 중")  # [v1.61 UI-4] running 태그 적용
    self._engine.add_task(job, tmpl, _log, _progress, _done)
    # 헤더 실행 상태 업데이트
    try:
        _run_count = sum(1 for j in self._jobs if j.get("_run_status") == "running")
        self.app._queue_var.set(f"실행 중 {_run_count}개" if _run_count > 0 else "실행 없음")
    except Exception:
        pass


def _jobs_stop_all(self):
    """모든 작업 중지  [v1.54: BUG-01 수정 — CHANGE-12]

    BUG-01 수정 내역
    ----------------
    v1.53: _stop_events dict 를 clear 하지 않아 stop 후 재실행 시
    이미 종료된 Event 키가 남아 "이미 실행 중" 판단 → 영구 스킵.
    v1.54: _cancelled_jobs.clear() 로 취소 목록 완전 초기화.
    """
    self._engine.stop()             # 큐 drain + 현재 실행 중단
    self._cancelled_jobs.clear()    # BUG-01 수정: 취소 목록 초기화
    for j in self._jobs:
        name = j.get("name", "")
        self._update_job_status(name, "⏹ 중지됨")
    self.app._set_status("⏹ 전체 작업 중지")


def _jobs_stop_job(self, job: dict):
    """개별 작업 중지  [v1.54 신규 — CHANGE-13]
    대기 중이면 취소 표시, 실행 중이면 즉시 중단.
    """
    if not job:
        return
    name = job.get("name", "")
    self._engine.cancel_job(name)
    self._update_job_status(name, "⏹ 취소됨")
    self.app._set_status(f"⏹ [{name}] 작업 취소")

def _jobs_toggle_job(self):
    """선택 작업의 활성/비활성 상태 토글  [v1.55 신규 — CHANGE-A5]

    동작 흐름:
      1. Treeview 선택 작업 가져오기 (_get_selected_job)
      2. job["enabled"] 플래그 반전 (True ↔ False)
      3. JOBS_DIR 개별 JSON 파일에 즉시 저장 (재시작 후에도 유지)
      4. _refresh_tv() 로 행 색상·"활성" 컬럼 텍스트 갱신
      5. 상태바에 변경 결과 메시지 출력

    이전(v1.54): 활성/비활성 토글 기능 없음 — 모든 작업 항상 실행 대상
    변경(v1.55): enabled 플래그 도입으로 개별 작업 일시 비활성화 가능
                 JSON 파일에 저장되므로 재시작 후에도 상태 유지

    community_poster v5.20 _toggle_job 패턴 벤치마킹 적용
    """
    j = self._get_selected_job()
    if not j:
        messagebox.showwarning("선택 없음",
            "활성화 상태를 변경할 작업을 선택하세요.")
        return

    # 현재 상태 반전 (enabled 키 없으면 True 폴백 후 반전 → False)
    current      = j.get("enabled", True)
    j["enabled"] = not current

    # JSON 파일 즉시 저장 (영구 보존)
    fpath = j.get("_file")
    if fpath:
        save_json(Path(fpath), j)

    # Treeview UI 갱신
    self._refresh_tv()

    # ── v1.56 CHANGE-S6: schedule_on=False 작업 활성화 시 경고 안내 ────────────
    # 이전(v1.55): 스케줄 미설정 작업 활성화 시 단순 "활성" 메시지만 표시
    # 변경(v1.56): schedule_on=False 인 작업을 활성화하면 자동 실행 안 됨을 안내
    #              → 사용자가 스케줄을 설정해야 한다는 것을 명확히 전달
    if j["enabled"] and not j.get("schedule_on", False):
        self.app._set_status(
            f"⚠️ [{j.get('name','')}] 활성화됨 "
            f"— 스케줄 미설정, 수동 실행만 가능")
    else:
        state_txt = "✓ 활성" if j["enabled"] else "✗ 비활성"
        self.app._set_status(
            f"{'✅' if j['enabled'] else '⏸'} "
            f"[{j.get('name', '')}] → {state_txt}")




# ── v1.60 ETA 유틸리티 ─────────────────────────────────────────────────────────
def _calc_single_job_duration(job: dict) -> float:
    """단일 작업 예상 소요시간(초) 계산
    우선순위: estimated_duration(사용자 설정) > last_duration(지수평활) > 기본값
    v1.60: pre_delay 포함 계산
    """
    # 1. 사용자 직접 설정값
    est = float(job.get("estimated_duration", 0.0) or 0.0)
    if est > 0:
        return est
    # 2. 실측 기반 지수평활 (α=0.3)
    last = float(job.get("last_duration", 0.0) or 0.0)
    if last > 0:
        base_wf = WORKFLOW_BASE_DURATION.get(
            job.get("workflow", ""), WORKFLOW_BASE_DURATION_DEFAULT)
        return last * 0.3 + base_wf * 0.7
    # 3. 워크플로우 기본값 + 딜레이 + pre_delay
    wf          = job.get("workflow", "")
    base        = WORKFLOW_BASE_DURATION.get(wf, WORKFLOW_BASE_DURATION_DEFAULT)
    delay_avg   = (float(job.get("delay_min",     3)) +
                   float(job.get("delay_max",     8))) / 2
    pre_avg     = (float(job.get("pre_delay_min", 0)) +
                   float(job.get("pre_delay_max", 0))) / 2
    return base + delay_avg + pre_avg


def _calc_queue_eta(jobs: list, engine_current_name: str = "") -> list:
    """전체 큐 ETA 계산 (time 모드 + interval 모드 모두 포함)
    반환: [{"name", "start", "finish", "dur_s", "mode"}, ...]
    v1.60: interval 모드 작업도 포함, next_run 기준 정렬
    """
    from datetime import datetime as _dt_eta, timedelta as _td_eta

    now_eta = _dt_eta.now()

    active = []
    for j in jobs:
        if not (j.get("schedule_on") and j.get("enabled", True)):
            continue
        if j.get("name") == engine_current_name:
            continue
        sched = j.get("schedule", j)          # schedule 서브딕트 또는 job 자체
        mode  = sched.get("schedule_mode", j.get("schedule_mode", "time"))

        if mode == "time":
            active.append((j, now_eta))
        elif mode == "interval":
            interval_h = float(sched.get("schedule_interval",
                               j.get("schedule_interval", 24)))
            last_raw   = j.get("last_run", "")
            next_run   = now_eta
            if last_raw:
                try:
                    from datetime import datetime as _dtx
                    last_dt  = _dtx.strptime(last_raw, "%Y-%m-%d %H:%M:%S")
                    next_run = last_dt + _td_eta(hours=interval_h)
                    if next_run < now_eta:
                        next_run = now_eta
                except ValueError:
                    next_run = now_eta
            active.append((j, next_run))

    # next_run 기준 정렬
    active.sort(key=lambda x: x[1])

    eta_list = []
    cursor   = now_eta
    for j, next_run in active:
        start  = max(cursor, next_run)
        dur    = _calc_single_job_duration(j)
        finish = start + _td_eta(seconds=dur)
        eta_list.append({
            "name":   j.get("name", ""),
            "start":  start,
            "finish": finish,
            "dur_s":  dur,
            "mode":   j.get("schedule_mode", "time"),
        })
        cursor = finish

    return eta_list


def _jobs_on_job_done(self, name: str,
                       succ: int, fail: int):
    """작업 완료 콜백 — UI 갱신  [v1.78: 결과 리포트 추가]"""
    total = succ + fail
    rate  = (succ / total * 100) if total > 0 else 0.0
    if fail == 0:
        status = f"✅ {succ}/{total}"
    elif succ == 0:
        status = f"❌ {fail}/{total}"
    else:
        status = f"✅ {succ}  ❌ {fail}"
    self._update_job_status(name, status)
    self.set_counts(
        sum(1 for j in self._jobs
            if j.get("_run_status") == "success"),
        sum(1 for j in self._jobs
            if j.get("_run_status") == "failed"),
    )
    self.app._set_status(
        f"[{name}] 완료 — 성공:{succ} 실패:{fail}")

    # v1.78: 작업 완료 결과 리포트 (LogTab에 요약 기록)
    eng = _get_tg_engine()
    frozen_cnt  = len(eng._frozen_accounts)
    stopped_cnt = len(eng._flood_stopped)
    dead_cnt    = len(eng._dead_links)
    report_lines = [
        f"╔═══════════════════════════════════════",
        f"║  📊 작업 완료 리포트  [{name}]",
        f"╠═══════════════════════════════════════",
        f"║  ✅ 성공:       {succ}건",
        f"║  ❌ 실패:       {fail}건",
        f"║  📈 성공률:     {rate:.1f}%",
        f"║  🚨 FROZEN계정: {frozen_cnt}개  (당일 중단)",
        f"║  🛑 FloodStop:  {stopped_cnt}개  (임계값 초과)",
        f"║  🗑  없는채팅방: {dead_cnt}건  (블랙리스트 등록)",
        f"╚═══════════════════════════════════════",
    ]
    if hasattr(self.app, "_log_tab"):
        for line in report_lines:
            lv = "SUCCESS" if fail == 0 else ("ERROR" if succ == 0 else "WARN")
            self.app._log_tab.append(line, lv, source=name)
    # 헤더 실행 상태 업데이트
    try:
        _run_count = sum(1 for j in self._jobs if j.get("_run_status") == "running")
        self.app._queue_var.set(f"실행 중 {_run_count}개" if _run_count > 0 else "실행 없음")
    except Exception:
        pass

    # ── v1.56 CHANGE-S4: 마지막 실행 시간 갱신 + JSON 저장 ─────────────────────
    # 이전(v1.55): last_run 키 없음 → interval 스케줄 이어받기 불가
    # 변경(v1.56): 완료 시 last_run / last_run_date 를 현재 시각으로 갱신
    #              개별 JSON 파일에 저장 → 재시작 후에도 interval 이어받기
    #              저장 시 _file(_status 포함) 런타임 전용 키는 제거
    from datetime import datetime as _dt_done
    _now_done = _dt_done.now()
    for _j_done in self._jobs:
        if _j_done.get("name") == name:
            _j_done["last_run"]      = _now_done.strftime("%Y-%m-%d %H:%M:%S")
            _j_done["last_run_date"] = _now_done.strftime("%Y-%m-%d")
            # v1.60 STEP-2: last_duration 지수평활 기록 (α=0.3)
            import time as _t_done_eta
            _elapsed = _t_done_eta.monotonic() - getattr(self, "_run_started_at", 0)
            if _elapsed > 0:
                _old_dur = float(_j_done.get("last_duration", 0.0) or 0.0)
                _j_done["last_duration"] = (
                    round(_elapsed * 0.3 + _old_dur * 0.7, 1)
                    if _old_dur > 0 else round(_elapsed, 1)
                )
            _fpath_done = _j_done.get("_file")
            if _fpath_done:
                # _file / _status 는 런타임 전용 → JSON 저장 대상 아님
                _save_dict = {k: v for k, v in _j_done.items()
                              if k not in ("_file", "_status")}
                save_json(Path(_fpath_done), _save_dict)
            break

    # [CRIT-02 보완] interval 모드 fired_set 키 제거
    # → last_run 이 갱신된 이후이므로 다음 interval 사이클에 재실행 허용
    _today_done = _now_done.strftime("%Y-%m-%d")
    _iv_done_key = f"{abs(hash(name))}|{_today_done}|interval"
    if hasattr(self, "_fired_set"):
        self._fired_set.discard(_iv_done_key)

    # 통계 업데이트
    if hasattr(self.app, "_stats_tab"):
        self.after(0,
            self.app._stats_tab.add_record,
            name, succ, fail)
    # v1.60 STEP-2: ETA 패널 갱신
    self.after(0, self._refresh_time_estimate)


def _jobs_update_job_status(self,
                             name: str, status: str):
    """Treeview 상태 컬럼 갱신 + [v1.61 UI-4] 행 태그 색상 동적 변경"""
    # ── _run_status 키로 태그 결정 ───────────────────────────────
    _stat_lower = status.lower()
    if "실행" in status or "running" in _stat_lower or "🟢" in status:
        run_status = "running"
    elif "✅" in status or "완료" in status or "success" in _stat_lower:
        run_status = "success"
    elif "❌" in status or "실패" in status or "오류" in status or "fail" in _stat_lower or "error" in _stat_lower:
        run_status = "failed"
    elif "중지" in status or "취소" in status or "stop" in _stat_lower or "⏹" in status:
        run_status = ""          # 중지 후 플랫폼 색으로 복원
    else:
        run_status = ""          # "대기 중" 등 → 플랫폼 색 복원

    plat = ""
    for j in self._jobs:
        if j.get("name") == name:
            j["_status"]     = status
            j["_run_status"] = run_status
            plat             = j.get("platform", "")
            break

    # Treeview 상태 텍스트 갱신
    try:
        self._tv.set(name, "status", status)
    except Exception:
        pass

    # 행 태그 동적 변경 (v1.61 UI-4)
    try:
        enabled = True
        for j in self._jobs:
            if j.get("name") == name:
                enabled = j.get("enabled", True)
                break
        if run_status:
            new_tag = run_status
        elif not enabled:
            new_tag = "disabled"
        elif plat == "kakao":
            new_tag = "kakao"
        elif plat == "telegram":
            new_tag = "telegram"
        else:
            new_tag = "enabled"
        self._tv.item(name, tags=(new_tag,))
    except Exception:
        pass


def _jobs_load_template_for_job(self,
                                  job: dict) -> dict | None:
    """작업에 연결된 템플릿 데이터 로드  [v1.54: BUG-04 수정 — CHANGE-16]

    BUG-04 수정 내역
    ----------------
    v1.53: UI 탭의 _load_templates() 는 _migrate_template() 을 호출하지만
    실행 경로인 이 함수는 raw JSON 을 그대로 반환 → v1.52 이전 템플릿
    (action_delay, column_gap 등 구 키 사용) 실행 시 KeyError / 오동작.

    v1.54: JSON 로드 직후 TemplateTab._migrate_template(d) 호출 1줄 추가.
    · 파일을 수정하지 않음 (인메모리 변환만 수행)
    · v1.52 이전 .json 파일을 그대로 복사해서 사용 가능
    · migrate 대상 키: action_delay→oc_after_open/send, column_gap→cell_width
    """
    import logging as _log_tmpl
    tmpl_name = job.get("template_name", "")
    if not tmpl_name:
        return None
    for f in TEMPLATE_DIR.glob("*.json"):
        d = load_json(f, {})
        if d.get("name") == tmpl_name:
            return TemplateTab._migrate_template(d)  # BUG-04 fix
    # v1.58 CHANGE-X14: 템플릿 파일 미발견 시 WARNING 로그
    job_name = job.get("name", "?")
    _log_tmpl.warning(
        f"[_jobs_load_template_for_job] 템플릿 파일 미발견: "
        f"job='{job_name}', template='{tmpl_name}'"
    )
    return None




# ─────────────────────────────────────────────────────────────────────────────
# Code G: 스케줄러 제어 함수  [v1.61 SC-1 — threading.Event 기반 재작성]
# ─────────────────────────────────────────────────────────────────────────────

def _jobs_stop_scheduler(self) -> None:
    """스케줄러 데몬 스레드를 안전하게 중지.
    [v1.61 SC-1] after() 체인 완전 제거 → stop_flag.set() 방식
    """
    flag = getattr(self, "_sched_stop_flag", None)
    if flag:
        flag.set()
    self._scheduler_running = False
    self._sched_stop_flag   = None


def _jobs_start_scheduler(self) -> None:
    """독립 데몬 스레드로 스케줄러 시작.
    [v1.61 SC-1] community_poster 방식 — UI 블로킹 완전 분리
    """
    import threading as _th_sc
    self._stop_scheduler()          # 기존 스레드 정리

    stop_flag = _th_sc.Event()
    self._sched_stop_flag   = stop_flag
    self._scheduler_running = True

    def _sched_loop():
        while not stop_flag.is_set():
            try:
                _jobs_scheduler_tick(self)
            except Exception as _e:
                # [CRIT-01 fix] daemon 스레드 → UI 직접 호출 금지 → after() 래핑
                try:
                    if hasattr(self.app, "_log_tab"):
                        _msg = f"[스케줄러 오류] {_e}"
                        self.app.after(
                            0, lambda m=_msg:
                            self.app._log_tab.append(m, "ERROR", "스케줄러"))
                except Exception:
                    pass
            stop_flag.wait(30)   # 30초 대기 (UI 영향 없음)

    t = _th_sc.Thread(target=_sched_loop, daemon=True, name="scheduler-v161")
    t.start()
    self._sched_thread = t


def _jobs_restart_scheduler(self) -> None:
    """스케줄러를 중지 후 즉시 재시작 (작업 저장/수정 후 호출).
    [v1.61 SC-6] 저장 즉시 반영 — 기존 after(200) 지연 제거
    [WARN-01 fix] time.sleep(0.05) → app.after(50) 로 교체해 UI 스레드 블로킹 방지
    """
    self._stop_scheduler()
    # 스레드 종료 여유 50 ms — UI 스레드를 블로킹하지 않도록 after() 사용
    self.app.after(50, self._start_scheduler)


def _jobs_scheduler_tick(self):
    """스케줄 틱 — 스레드 루프에서 30초마다 호출.
    [v1.61 SC-1~SC-3 전면 재작성]

    변경 사항 (v1.61):
      · after() 체인 완전 제거 — 스레드 루프(_sched_loop)에서 호출됨
      · fired_set 키 구분자 | 로 변경 (SC-2: 이름에 _ 포함 시 파싱 오류 방지)
      · interval 첫 실행 즉시 트리거 제거 (SC-3: last_run_date가 오늘이면 skip)
      · 요일 필터, variance 오프셋, trigger_with_wait 유지
    """
    import datetime as _dt_fn
    import time as _t_mono
    import random as _rand_sched
    _KR_WEEKDAYS = ["월","화","수","목","금","토","일"]
    from datetime import datetime as _dt_sched

    now        = _dt_sched.now()
    today_str  = now.strftime("%Y-%m-%d")
    now_hm     = now.strftime("%H:%M")
    today_kr   = _KR_WEEKDAYS[now.weekday()]

    # ── [SC-2] _fired_set 초기화 및 당일 이전 키 정리 (구분자: |) ────────────
    if not hasattr(self, "_fired_set"):
        self._fired_set = set()
    if not hasattr(self, "_50sec_guard"):
        self._50sec_guard = {}
    # | 구분자: "{hash}|{date}|{time}" → split("|")[1] 이 항상 날짜
    self._fired_set = {k for k in self._fired_set
                       if len(k.split("|")) >= 3 and k.split("|")[1] == today_str}

    for j in self._jobs:
        try:
            if not (j.get("schedule_on", False) and j.get("enabled", True)):
                continue

            name = j.get("name", "")
            if not name:
                continue
            mode = j.get("schedule_mode", "time")

            # ── 요일 필터 ─────────────────────────────────────────────────
            _int_days = j.get("days", None)
            if _int_days is None:
                _kr_days  = j.get("schedule_days", ["월","화","수","목","금"])
                _int_days = [_KR_TO_INT[d] for d in _kr_days if d in _KR_TO_INT]
            if _int_days and now.weekday() not in _int_days:
                continue

            # ── time 모드 ─────────────────────────────────────────────────
            if mode == "time":
                sched_times = j.get("schedule_times", [])
                if not sched_times:
                    t_s = j.get("schedule_time", "")
                    if t_s:
                        sched_times = [t_s]

                _variance = int(j.get("interval_variance",
                                      DEFAULT_SCHEDULE["interval_variance"]))
                for t in sched_times:
                    if not _check_time_match(now_hm, t, _variance):
                        continue
                    # 자정 경계 처리 (BUG-N1 유지)
                    _sched_h = int(t.split(":")[0]) if ":" in t else 0
                    if _sched_h >= 23 and now.hour <= 1:
                        _key_date = (now - _dt_fn.timedelta(days=1)).strftime("%Y-%m-%d")
                    else:
                        _key_date = today_str
                    # [SC-2] 키 구분자 | 사용 — hash(name) 으로 이름 내 _ 문제 방지
                    fired_key = f"{abs(hash(name))}|{_key_date}|{t}"
                    if fired_key in self._fired_set:
                        continue
                    # 50초 중복 가드 (BENCH-3 유지)
                    _now_mono = _t_mono.monotonic()
                    if _now_mono - self._50sec_guard.get(fired_key, 0) < 50:
                        continue
                    self._50sec_guard[fired_key] = _now_mono
                    self._fired_set.add(fired_key)

                    _delay_sec = (_rand_sched.randint(-_variance * 60, _variance * 60)
                                  if _variance > 0 else 0)
                    sched_label = j.get("schedule_label", f"{today_kr} {t}")
                    _delay_info = (f" (±{_variance}분 오프셋: {_delay_sec:+d}초)"
                                   if _variance > 0 else "")
                    if hasattr(self.app, "_log_tab"):
                        self.app.after(0, lambda m=f"[스케줄] [{name}] 자동 실행 — {sched_label}{_delay_info}":
                                       self.app._log_tab.append(m, "INFO", "스케줄러"))
                    if _delay_sec > 0:
                        self.app.after(_delay_sec * 1000,
                                       lambda _j=j: self._run_job(_j, silent=True))
                    else:
                        self.app.after(0, lambda _j=j: self._run_job(_j, silent=True))

            # ── interval 모드 ─────────────────────────────────────────────
            elif mode == "interval":
                interval  = int(j.get("schedule_interval", 24))
                last_raw  = j.get("last_run", "")
                fired     = False

                if not last_raw:
                    # [SC-3] 첫 등록 시 즉시 트리거 방지 — 다음 interval 사이클 대기
                    fired = False
                else:
                    try:
                        last_dt   = _dt_sched.strptime(last_raw, "%Y-%m-%d %H:%M:%S")
                        elapsed_h = (now - last_dt).total_seconds() / 3600
                        fired     = elapsed_h >= interval
                    except ValueError:
                        fired = True   # 파싱 실패 → 재실행 허용

                if fired:
                    # [CRIT-02 fix] interval 모드도 _fired_set 으로 중복 트리거 방지
                    # last_run 이 업데이트되기 전 30초 뒤 tick 이 다시 돌 때 재실행 차단
                    _iv_key = f"{abs(hash(name))}|{today_str}|interval"
                    if _iv_key in self._fired_set:
                        continue
                    self._fired_set.add(_iv_key)
                    sched_label = j.get("schedule_label", f"매 {interval}시간")
                    if hasattr(self.app, "_log_tab"):
                        self.app.after(0, lambda m=f"[스케줄] [{name}] 자동 실행 — {sched_label}":
                                       self.app._log_tab.append(m, "INFO", "스케줄러"))
                    self.app.after(0, lambda _j=j: self._trigger_with_wait(_j))

        except Exception as _job_err:
            try:
                if hasattr(self.app, "_log_tab"):
                    self.app.after(0, lambda m=f"[스케줄러] 작업 [{j.get('name','?')}] 오류: {_job_err}":
                                   self.app._log_tab.append(m, "ERROR", "스케줄러"))
            except Exception:
                pass


def _jobs_trigger_with_wait(self, job: dict):
    """v1.60 BENCH-1: 이전 작업 완료 대기 후 실행 (_trigger_with_wait 패턴)
    engine이 바쁜 경우 별도 스레드에서 idle 이벤트를 기다린 후 실행.
    """
    import threading as _th_tww
    if not self._engine.is_busy:
        self._run_job(job, silent=True)
        return

    def _wait_and_run():
        self._engine.wait_until_idle()
        self.after(0, lambda _j=job: self._run_job(_j, silent=True))

    t = _th_tww.Thread(target=_wait_and_run, daemon=True)
    t.start()


def _jobs_log_scheduler_restore(self, job_names: list):
    """v1.60 BENCH-2: 앱 시작 시 스케줄 복원 로그
    [CRIT-05 fix] 백그라운드 스레드에서 호출될 수 있으므로 after() 로 UI 스레드 안전 보장
    """
    if not job_names:
        return
    if hasattr(self.app, "_log_tab"):
        for nm in job_names:
            self.app.after(
                0, lambda m=f"[스케줄 복원] [{nm}] 스케줄 재등록":
                self.app._log_tab.append(m, "INFO", "스케줄러"))


def _jobs_restore_scheduler_on_startup(self):
    """[v1.61 SC-4] community_poster._restore_scheduler_on_startup() 이식.

    앱 시작 시 schedule_on=True 이고 enabled=True 인 작업 목록을 수집하여
    스케줄러 데몬 스레드를 시작하고 복원 로그를 기록한다.
    """
    active_names = [
        j.get("name", "")
        for j in getattr(self, "_jobs", [])
        if j.get("schedule_on", False) and j.get("enabled", True)
    ]
    if active_names:
        self._start_scheduler()
        self._log_scheduler_restore(active_names)
        # 헤더 스케줄 상태 업데이트
        try:
            self.app._sched_var.set(f"🟢 스케줄 {len(active_names)}개")
        except Exception:
            pass
    else:
        try:
            self.app._sched_var.set("스케줄 OFF")
        except Exception:
            pass


def _jobs_sync_scheduler(self):
    """[v1.61 SC-5] community_poster._sync_scheduler() 이식.

    작업 추가/수정/삭제 후 스케줄 상태를 동기화한다.
    - schedule_on=True 인 작업이 1개 이상이면 스케줄러 시작
    - 없으면 스케줄러 중지
    - 헤더 _sched_var 업데이트
    """
    active = [
        j for j in getattr(self, "_jobs", [])
        if j.get("schedule_on", False) and j.get("enabled", True)
    ]
    if active:
        self._restart_scheduler()
        try:
            self.app._sched_var.set(f"🟢 스케줄 {len(active)}개")
        except Exception:
            pass
    else:
        self._stop_scheduler()
        try:
            self.app._sched_var.set("스케줄 OFF")
        except Exception:
            pass


# ── monkey-patch 적용  [v1.54: CHANGE-17 / v1.55: _toggle_job 추가] ───────────────────
# 변경 사항:
#   제거: _run_job_sync  (PostingEngine 단일 워커가 순차 처리 보장)
#   추가: _stop_job      (개별 작업 취소 — v1.54 신규)
#   유지: 나머지 7개 (시그니처 호환 유지)
JobsTab._run_selected          = _jobs_run_selected      # 선택 작업 큐 추가
JobsTab._run_all               = _jobs_run_all           # 전체 일괄 큐 추가
JobsTab._run_job               = _jobs_run_job           # 핵심: 큐 적재+콜백 정의
# _run_job_sync 제거됨 — PostingEngine._worker() 가 순차 처리
JobsTab._stop_all              = _jobs_stop_all          # 전체 중지 (BUG-01 수정)
JobsTab._stop_job              = _jobs_stop_job          # 개별 중지 [v1.54 신규]
JobsTab._toggle_job            = _jobs_toggle_job        # 활성 토글 [v1.55 신규 — CHANGE-A5]
JobsTab._scheduler_tick        = _jobs_scheduler_tick    # 스케줄 틱 루프 [v1.56/v1.57/v1.58 재작성]
JobsTab._stop_scheduler        = _jobs_stop_scheduler    # 스케줄러 중지 [v1.58 CHANGE-X5]
JobsTab._start_scheduler       = _jobs_start_scheduler   # 스케줄러 시작 [v1.58 CHANGE-X5]
JobsTab._restart_scheduler     = _jobs_restart_scheduler # 스케줄러 재시작 [v1.58 CHANGE-X5]
JobsTab._on_job_done           = _jobs_on_job_done       # 완료 콜백 → UI 갱신
JobsTab._update_job_status     = _jobs_update_job_status # Treeview 상태 컬럼
JobsTab._load_template_for_job = _jobs_load_template_for_job  # migrate 포함 (BUG-04)
JobsTab._trigger_with_wait          = _jobs_trigger_with_wait           # v1.60 BENCH-1
JobsTab._log_scheduler_restore      = _jobs_log_scheduler_restore       # v1.60 BENCH-2
JobsTab._restore_scheduler_on_startup = _jobs_restore_scheduler_on_startup  # v1.61 SC-4
JobsTab._sync_scheduler             = _jobs_sync_scheduler              # v1.61 SC-5
# [BUG-06 fix] lambda stub 제거 — 클래스 내부 _refresh_time_estimate 구현(line 5427)이 사용됨
# JobsTab._refresh_time_estimate      = lambda self: None  ← 실제 메서드를 덮어쓰는 버그 수정


# ── v1.60: 자동 업데이터 연동 ───────────────────────────────────────────────
try:
    import auto_updater as _au
    def _check_update_on_start(app_instance):
        import threading as _th_au
        def _safe():
            try:
                _au.check_update_async(app_instance, timeout=5)
            except Exception:
                pass
        _th_au.Thread(target=_safe, daemon=True).start()
except ImportError:
    def _check_update_on_start(app_instance):
        pass
# ────────────────────────────────────────────────────────────────────────────
# ── App 에 JobsTab 연결 ──────────────────────────────────────
def _app_build_jobs_tab(self, frame: tk.Frame):
    tab = JobsTab(frame, self)
    tab.pack(fill=tk.BOTH, expand=True)
    self._jobs_tab = tab

App._build_jobs_tab = _app_build_jobs_tab
# ============================================================
# Block 4-B : TelethonEngine — Telethon 기반 텔레그램 엔진
# ============================================================
#
# [TG-1] TelethonEngine
#   · 계정별 독립 asyncio 이벤트 루프 + daemon 스레드
#   · 최대 15계정 동시 실행
#   · 제재 탐지: FloodWaitError / PeerFloodError / UserBannedInChannel / AccountBannedError
#   · 계정별 .session 파일 영구 저장 (TelegramAccounts/ 디렉터리)
# ─────────────────────────────────────────────────────────────────────────────

try:
    from telethon import TelegramClient, events, errors as _tl_errors
    from telethon.tl.functions.channels import JoinChannelRequest
    from telethon.tl.functions.messages import ImportChatInviteRequest
    HAS_TELETHON = True
except ImportError:
    HAS_TELETHON = False
    _tl_errors = None



# 텔레그램 계정 설정 저장 경로
TG_ACCOUNTS_PATH = CONFIG_DIR / "tg_accounts.json"
TG_SESSION_DIR   = APP_DIR / "TelegramAccounts"
TG_SESSION_DIR.mkdir(exist_ok=True)


class TelethonEngine:
    """
    Telethon 기반 텔레그램 다계정 실행 엔진  [v1.61 TG-1]

    구조
    ----
    · 계정별 독립 asyncio 이벤트 루프 (daemon 스레드)
    · join_group(link)    : 그룹/채널 가입
    · send_message(peer, msg) : 메시지 전송
    · 제재 탐지 및 자동 대응:
        FloodWaitError      → n초 대기 후 재시도 (최대 3회)
        PeerFloodError      → 해당 계정 당일 중지 (status="flood")
        UserBannedInChannel → 채널 블랙리스트 등록
        AccountBannedError  → 전체 중지 + 사용자 알림 (status="banned")
    · 일일 발송 카운터 + 한도 제어
    · 워밍업 모드: 50→100→200→500 자동 조절
    """

    # ── 계정 상태 코드 ─────────────────────────────────────
    ST_IDLE    = "idle"      # 대기
    ST_RUNNING = "running"   # 실행 중
    ST_FLOOD   = "flood"     # PeerFlood — 당일 중지
    ST_BANNED  = "banned"    # 계정 밴
    ST_ERROR   = "error"     # 기타 오류

    # ── 추가 상태 코드 (v1.78) ─────────────────────────────
    ST_FROZEN  = "frozen"    # 계정 동결 (Telegram 제재)
    ST_STOPPED = "stopped"   # 당일 중단 (FloodWait 임계값 초과)

    def __init__(self, log_fn=None, alert_fn=None):
        self._accounts: list[dict]   = []   # [{name, api_id, api_hash, phone, ...}]
        self._clients:  dict         = {}   # phone → TelegramClient
        self._loops:    dict         = {}   # phone → asyncio.EventLoop
        self._threads:  dict         = {}   # phone → Thread
        self._status:   dict         = {}   # phone → ST_*
        self._daily_cnt: dict        = {}   # phone → int (오늘 발송 수)
        self._blacklist: set         = set()  # 채널 블랙리스트 (런타임)
        # ── v1.78 신규 ───────────────────────────────────────────
        self._dead_links: set        = set()  # 없는 채팅방 영구 블랙리스트
        self._frozen_accounts: set   = set()  # frozen 감지된 계정 phone 집합
        self._flood_stopped: set     = set()  # FloodWait 임계값 초과 당일 중단 계정
        self._join_cnt: dict         = {}     # phone → 오늘 가입 횟수
        self._max_flood_threshold: int = 600  # FloodWait 이 이 초 이상이면 당일 중단
        self._max_daily_join: int    = 50     # 계정당 일일 최대 가입 횟수 (기본)
        # 긴급 알림 콜백 (LogTab 긴급 패널 갱신용)
        self._alert_fn = alert_fn or (lambda phone, kind, detail="": None)
        self._log_fn    = log_fn or (lambda msg, lv="INFO": None)
        self._lock      = threading.Lock()

    # ── v1.78: 없는 채팅방 영구 블랙리스트 관리 ──────────────
    def add_dead_link(self, link: str):
        """없는 채팅방 링크를 영구 블랙리스트에 추가"""
        with self._lock:
            self._dead_links.add(link.strip().rstrip("/").lower())

    def is_dead_link(self, link: str) -> bool:
        return link.strip().rstrip("/").lower() in self._dead_links

    # ── v1.78: frozen 계정 관리 ──────────────────────────────
    def mark_frozen(self, phone: str):
        """계정을 frozen 상태로 마킹하고 당일 모든 작업 중단"""
        with self._lock:
            self._frozen_accounts.add(phone)
            self._status[phone] = self.ST_FROZEN
        self._log_fn(
            f"[TG:{phone}] 🚨 FROZEN 감지 — 당일 작업 전체 중단!", "ERROR")
        self._alert_fn(phone, "frozen")

    def is_frozen(self, phone: str) -> bool:
        return phone in self._frozen_accounts

    # ── v1.78: FloodWait 임계값 초과 당일 중단 ───────────────
    def mark_flood_stopped(self, phone: str, seconds: int):
        """FloodWait가 임계값 초과 → 당일 중단"""
        with self._lock:
            self._flood_stopped.add(phone)
            self._status[phone] = self.ST_STOPPED
        self._log_fn(
            f"[TG:{phone}] 🛑 FloodWait {seconds}초 → 임계값({self._max_flood_threshold}초) 초과 — 당일 중단", "ERROR")
        self._alert_fn(phone, "flood_stopped", f"{seconds}초")

    def is_flood_stopped(self, phone: str) -> bool:
        return phone in self._flood_stopped

    # ── 전화번호 정규화 ────────────────────────────────────
    @staticmethod
    def _normalize_phone(phone: str) -> str:
        """전화번호를 Telegram API 국제 형식(+국가코드)으로 변환.

        변환 규칙:
          - 숫자·공백·하이픈·괄호 외 문자는 제거
          - 이미 '+' 로 시작하면 그대로 반환
          - 한국 번호(010/011/016/017/018/019 로 시작) → +82로 변환
            예) 01012345678 → +821012345678
          - 그 외 '0' 으로 시작하면 '0' 제거 후 '+' 만 붙임
            (정확한 국가코드를 알 수 없으면 사용자가 직접 +XX 형식 입력 권장)
        """
        raw = re.sub(r"[\s\-\(\)]", "", str(phone).strip())  # 공백·하이픈·괄호 제거
        if not raw:
            return ""
        if raw.startswith("+"):
            return raw  # 이미 국제 형식
        # 한국 번호 패턴: 010/011/016/017/018/019
        if re.match(r"^01[016789]\d{7,8}$", raw):
            return "+82" + raw[1:]   # 맨 앞 '0' → '+82'
        # 그 외 '0'으로 시작하는 경우 → 경고 로그용 + 없이 반환 (사용자가 수정해야 함)
        return raw

    # ── 계정 설정 ──────────────────────────────────────────
    def load_accounts(self, accounts: list):
        """계정 목록을 설정. [{name, api_id, api_hash, phone, daily_limit, warmup}]"""
        with self._lock:
            self._accounts = list(accounts)

    def get_account_status(self, phone: str) -> str:
        return self._status.get(phone, self.ST_IDLE)

    def get_daily_count(self, phone: str) -> int:
        return self._daily_cnt.get(phone, 0)

    def reset_daily_counts(self):
        """자정 초기화 호출용"""
        with self._lock:
            self._daily_cnt.clear()

    # ── 클라이언트 생성/연결 ───────────────────────────────
    def _get_or_create_loop(self, phone: str):
        """계정별 asyncio 루프 (없으면 신규 생성)
        주의: 이 메서드는 self._lock 보유 중에 호출될 수 있으므로
        lock 을 획득하지 않음 (deadlock 방지). 호출자가 lock 관리 책임.
        """
        if phone not in self._loops:
            loop = asyncio.new_event_loop()
            self._loops[phone] = loop
        return self._loops[phone]

    def _ensure_client(self, acct: dict):
        """클라이언트가 없거나 연결 해제 상태면 새로 생성
        API ID / API Hash 는 계정별 값보다 전역 config(tg_api)를 우선 사용한다.
        """
        if not HAS_TELETHON:
            raise RuntimeError("telethon 패키지가 필요합니다: pip install telethon")
        phone   = self._normalize_phone(acct.get("phone", ""))  # 국제 형식 변환
        # 전역 config 에서 api_id/api_hash 읽기 (계정별 값은 fallback)
        _cfg = load_json(CONFIG_PATH, {})
        _tg  = _cfg.get("tg_api", {})
        api_id   = int(_tg.get("api_id")  or acct.get("api_id",  0) or 0)
        api_hash = str(_tg.get("api_hash") or acct.get("api_hash", "") or "")
        session = str(TG_SESSION_DIR / f"session_{phone}")

        # [NEW-BUG-04 fix] _loops/_clients dict 접근 시 lock 으로 race condition 방지
        # _get_or_create_loop 는 lock 없이 작동하므로 lock 블록 내부에서 직접 호출
        with self._lock:
            loop = self._get_or_create_loop(phone)
            if phone not in self._clients:
                # [BUG-07 fix] Telethon 1.25+에서 loop= 파라미터 제거됨 → 인자 삭제
                # loop는 _run_in_loop / asyncio.run_coroutine_threadsafe 에서 별도 전달
                client = TelegramClient(session, api_id, api_hash)
                self._clients[phone] = client
            else:
                # [WARN-04 fix] 기존 클라이언트가 연결 해제 상태면 새로 생성
                # disconnect()는 Telethon에서 코루틴이므로 동기 호출하면 실제 해제 안됨.
                # is_connected() == False 이면 해당 객체는 재사용 불가 → 즉시 교체.
                existing = self._clients[phone]
                try:
                    connected = existing.is_connected()
                except Exception:
                    connected = False
                if not connected:
                    client = TelegramClient(session, api_id, api_hash)
                    self._clients[phone] = client
        return self._clients[phone], loop

    def _run_in_loop(self, loop, coro):
        """동기 컨텍스트에서 코루틴을 루프에서 실행"""
        future = asyncio.run_coroutine_threadsafe(coro, loop)
        return future.result(timeout=60)

    def _start_loop_thread(self, phone: str, loop):
        """루프를 전용 daemon 스레드에서 실행 (이미 실행 중이면 skip)"""
        if phone in self._threads and self._threads[phone].is_alive():
            return
        def _run():
            loop.run_forever()
        t = threading.Thread(target=_run, daemon=True,
                             name=f"tg-loop-{phone}")
        t.start()
        self._threads[phone] = t

    # ── 공개 API ───────────────────────────────────────────
    # ── ② 계정 상태 실시간 조회 (get_me) ───────────────────────────────
    def _check_account_status(self, acct: dict) -> dict:
        """발송 전 계정 제재/밴/frozen 여부를 Telethon get_me() 로 확인.
        [v1.78: frozen 탐지 강화 — get_me 후 restricted_reason에서 'frozen' 검출]

        반환: {
            "ok":         bool,      # True = 정상
            "restricted": bool,      # True = 제한 계정
            "banned":     bool,      # True = 정지 계정
            "frozen":     bool,      # True = frozen 계정 (v1.78 신규)
            "scam":       bool,      # True = 스캠 마킹
            "id":         int|None,
            "username":   str,
            "name":       str,
            "reason":     str,       # 제재 이유 문자열 (없으면 "")
        }
        연결 실패 / Telethon 미설치 시 {"ok": False, ...} 반환.
        """
        empty = {"ok": False, "restricted": False, "banned": False,
                 "frozen": False, "scam": False,
                 "id": None, "username": "", "name": "", "reason": ""}
        if not HAS_TELETHON:
            return empty
        phone = self._normalize_phone(acct.get("phone", ""))

        # v1.78: 이미 frozen으로 마킹된 계정은 즉시 반환
        if self.is_frozen(phone):
            return {**empty, "frozen": True, "restricted": True,
                    "reason": "frozen (이미 감지됨)"}

        try:
            client, loop = self._ensure_client(acct)
            self._start_loop_thread(phone, loop)

            async def _get():
                if not client.is_connected():
                    await client.connect()
                if not await client.is_user_authorized():
                    return None
                return await client.get_me()

            me = self._run_in_loop(loop, _get())
            if me is None:
                return {**empty, "reason": "미인증"}

            restricted = bool(getattr(me, "restricted", False))
            banned     = bool(getattr(me, "deleted", False))  # UserDeactivated
            scam       = bool(getattr(me, "scam",   False))
            fake       = bool(getattr(me, "fake",   False))
            name       = ((getattr(me, "first_name", "") or "") + " " +
                          (getattr(me, "last_name",  "") or "")).strip()
            username   = getattr(me, "username", "") or ""
            user_id    = getattr(me, "id", None)

            # v1.78: frozen 탐지 — restriction_reason 확인
            frozen = False
            if restricted:
                rr = getattr(me, "restriction_reason", None) or []
                for r in (rr if isinstance(rr, (list, tuple)) else [rr]):
                    reason_text = str(getattr(r, "reason", "") or "").lower()
                    if "frozen" in reason_text or "spam" in reason_text:
                        frozen = True
                        break

            if frozen:
                self.mark_frozen(phone)

            reasons = []
            if frozen:      reasons.append("frozen")
            if restricted:  reasons.append("restricted")
            if banned:      reasons.append("banned/deactivated")
            if scam:        reasons.append("scam")
            if fake:        reasons.append("fake")

            info = {
                "ok":         not (restricted or banned or scam or fake or frozen),
                "restricted": restricted,
                "banned":     banned or scam or fake,
                "frozen":     frozen,
                "scam":       scam,
                "id":         user_id,
                "username":   username,
                "name":       name,
                "reason":     ", ".join(reasons),
            }
            if frozen:
                self._log_fn(
                    f"[TG:{phone}] 🚨 계정 FROZEN 감지 — 즉시 중단!", "ERROR")
            elif reasons:
                self._log_fn(
                    f"[TG:{phone}] ⚠️ 계정 상태 이상: {', '.join(reasons)}", "WARN")
            else:
                self._log_fn(
                    f"[TG:{phone}] 👤 계정 정상 — {name} (@{username}) id={user_id}", "INFO")
            return info

        except Exception as _e:
            err_str = str(_e).lower()
            # v1.78: 예외에서도 frozen 탐지
            if "frozen" in err_str:
                phone_n = self._normalize_phone(acct.get("phone", ""))
                self.mark_frozen(phone_n)
                return {**empty, "frozen": True, "restricted": True,
                        "reason": f"frozen (예외 감지: {_e})"}
            self._log_fn(f"[TG:{phone}] ⚠️ 계정 상태 조회 실패: {_e}", "WARN")
            return empty

    # ── ③ 채팅방 권한 체크 (get_permissions) ──────────────────────────
    def check_peer_permission(self, acct: dict, peer: str) -> dict:
        """발송 전 해당 채팅방에서 내 계정의 전송 권한 확인.  [v1.81: send_media 추가]

        반환: {
            "ok":           bool,   # True = 텍스트 발송 가능
            "is_member":    bool,
            "send_messages":bool,   # 텍스트 전송 가능
            "send_media":   bool,   # 이미지/파일 전송 가능
            "is_banned":    bool,
            "reason":       str,
        }
        """
        empty = {"ok": False, "is_member": False,
                 "send_messages": False, "send_media": False,
                 "is_banned": False, "reason": ""}
        if not HAS_TELETHON:
            return empty
        phone = self._normalize_phone(acct.get("phone", ""))
        try:
            client, loop = self._ensure_client(acct)
            self._start_loop_thread(phone, loop)

            async def _check():
                if not client.is_connected():
                    await client.connect()
                me    = await client.get_me()
                perms = await client.get_permissions(peer, me)
                return perms

            perms = self._run_in_loop(loop, _check())
            if perms is None:
                return {**empty, "reason": "권한 조회 실패"}

            is_banned     = bool(getattr(perms, "is_banned",      False))
            is_member     = bool(getattr(perms, "is_member",      True))
            send_messages = bool(getattr(perms, "send_messages",  True))
            # send_media: Telethon perms 에 없으면 send_messages 와 동일하게 간주
            send_media    = bool(getattr(perms, "send_media",     send_messages))

            reasons = []
            if is_banned:          reasons.append("밴")
            if not is_member:      reasons.append("비멤버")
            if not send_messages:  reasons.append("텍스트전송불가")
            if not send_media:     reasons.append("미디어전송불가")

            result = {
                "ok":           not is_banned and is_member and send_messages,
                "is_member":    is_member,
                "send_messages":send_messages,
                "send_media":   send_media,
                "is_banned":    is_banned,
                "reason":       ", ".join(reasons),
            }
            if reasons:
                self._log_fn(
                    f"[TG:{phone}] ⛔ 채팅방 권한 부족 [{peer}]: {', '.join(reasons)}", "WARN")
            return result

        except Exception:
            # get_permissions 미지원 채팅방(채널 등)은 정상 처리
            return {"ok": True, "is_member": True,
                    "send_messages": True, "send_media": True,
                    "is_banned": False, "reason": ""}

    def connect(self, acct: dict,
                otp_callback=None, password_callback=None) -> bool:
        """계정 연결.
        세션 파일이 있으면 자동 로그인.
        없으면 otp_callback(phone) → 코드 문자열 반환 필요.
        2FA 설정 계정은 password_callback(phone) → 비번 문자열 반환 필요.

        otp_callback / password_callback 이 None 이면 백그라운드 자동실행
        (배치 작업) 중에는 세션 없는 계정을 건너뜀.
        """
        phone = self._normalize_phone(acct.get("phone", ""))  # 국제 형식 변환
        try:
            client, loop = self._ensure_client(acct)
            self._start_loop_thread(phone, loop)

            async def _do_connect():
                if not client.is_connected():
                    await client.connect()
                if await client.is_user_authorized():
                    return "ok"
                # 세션 없음 — OTP 필요
                if otp_callback is None:
                    return "need_otp"
                # OTP 발송 요청
                await client.send_code_request(phone)
                code = otp_callback(phone)
                if not code:
                    return "cancelled"
                try:
                    await client.sign_in(phone, code)
                except _tl_errors.SessionPasswordNeededError:
                    # 2FA 비밀번호 필요
                    if password_callback is None:
                        return "need_2fa"
                    pw = password_callback(phone)
                    if not pw:
                        return "cancelled"
                    await client.sign_in(password=pw)
                return "ok"

            result = self._run_in_loop(loop, _do_connect())
            if result == "ok":
                self._log_fn(f"[TG:{phone}] ✅ 연결·인증 완료", "SUCCESS")
                self._status[phone] = self.ST_IDLE
                return True
            elif result == "need_otp":
                self._log_fn(f"[TG:{phone}] ⚠️ 세션 없음 — 연결 테스트 탭에서 OTP 인증 필요", "WARN")
                return False
            elif result == "need_2fa":
                self._log_fn(f"[TG:{phone}] ⚠️ 2FA 비밀번호 필요 — 연결 테스트에서 입력하세요", "WARN")
                return False
            else:  # cancelled
                self._log_fn(f"[TG:{phone}] ⚠️ 인증 취소됨", "WARN")
                return False
        except Exception as e:
            self._log_fn(f"[TG:{phone}] ❌ 연결 실패: {e}", "ERROR")
            self._status[phone] = self.ST_ERROR
            return False

    def join_group(self, acct: dict, link: str,
                   stop_event: threading.Event = None) -> bool:
        """그룹/채널 가입  [TG-1] [v1.78: frozen/dead_link/가입한도 강화]
        t.me/xxx 또는 t.me/joinchat/HASH 형식 모두 지원
        """
        if not HAS_TELETHON:
            self._log_fn("telethon 미설치", "ERROR"); return False

        phone = self._normalize_phone(acct.get("phone", ""))  # 국제 형식 변환

        # v1.78: frozen 계정 즉시 차단
        if self.is_frozen(phone):
            self._log_fn(f"[TG:{phone}] 🚨 FROZEN 계정 — 가입 차단: {link}", "ERROR")
            return False

        # v1.78: FloodWait 임계값 초과 당일 중단 계정 차단
        if self.is_flood_stopped(phone):
            self._log_fn(f"[TG:{phone}] 🛑 FloodWait 당일 중단 — 가입 차단: {link}", "ERROR")
            return False

        # v1.78: dead_link 영구 블랙리스트 확인
        if self.is_dead_link(link):
            self._log_fn(f"[TG:{phone}] 🗑 없는 채팅방(dead) — 스킵: {link}", "WARN")
            return False

        # 당일 한도 확인
        daily_limit = int(acct.get("daily_limit", 500))
        warmup      = acct.get("warmup", False)
        if warmup:
            warmup_day = int(acct.get("warmup_day", 1))
            daily_limit = min(daily_limit,
                              [50, 100, 200, 500][min(warmup_day - 1, 3)])

        if self._daily_cnt.get(phone, 0) >= daily_limit:
            self._log_fn(f"[TG:{phone}] ⚠️ 일일 한도 초과 ({daily_limit}건)", "WARN")
            return False

        # v1.78: 일일 가입 횟수 별도 제한 (frozen 예방)
        join_limit = int(acct.get("daily_join_limit", self._max_daily_join))
        if self._join_cnt.get(phone, 0) >= join_limit:
            self._log_fn(
                f"[TG:{phone}] ⚠️ 일일 가입 한도 초과 ({join_limit}건) — 가입 중단", "WARN")
            return False

        # 블랙리스트 확인
        if link in self._blacklist:
            self._log_fn(f"[TG:{phone}] ⛔ 블랙리스트 채널: {link}", "WARN")
            return False

        try:
            client, loop = self._ensure_client(acct)
            self._start_loop_thread(phone, loop)
            self._status[phone] = self.ST_RUNNING

            async def _do_join():
                if not client.is_connected():
                    await client.connect()
                # joinchat 해시 링크
                if "joinchat/" in link or "+" in link:
                    hash_part = link.split("/")[-1].lstrip("+")
                    await client(ImportChatInviteRequest(hash_part))
                else:
                    username = link.rstrip("/").split("/")[-1]
                    await client(JoinChannelRequest(username))

            # v1.79: per-account flood_threshold 반영
            _ft = int(acct.get("flood_threshold", self._max_flood_threshold))
            self._retry_run(phone, loop, _do_join, link, stop_event,
                            flood_threshold=_ft)
            with self._lock:
                self._daily_cnt[phone] = self._daily_cnt.get(phone, 0) + 1
                # v1.78: 가입 횟수 별도 카운트
                self._join_cnt[phone] = self._join_cnt.get(phone, 0) + 1

            # [v1.86] 가입 직후 FROZEN 재확인 — 가입 성공 직후 텔레그램이
            # 계정을 frozen 처리하는 경우 _retry_run은 True를 반환했지만
            # 이미 mark_frozen이 호출된 상태일 수 있음 → False 반환으로 루프 탈출
            if self.is_frozen(phone):
                self._log_fn(
                    f"[TG:{phone}] 🚨 가입 후 FROZEN 감지 — 즉시 중단!", "ERROR")
                return False

            self._status[phone] = self.ST_IDLE
            self._log_fn(f"[TG:{phone}] ✅ 가입 완료: {link}", "SUCCESS")
            return True

        except Exception as e:
            # [v1.86] _handle_error는 dict를 반환하므로 join_group은 명시적으로 False 반환
            # dict는 truthy이므로 기존 코드는 실패도 ok=True로 처리되는 버그 있었음
            self._handle_error(phone, e, link)
            return False

    def send_message(self, acct: dict, peer: str, message: str,
                     stop_event: threading.Event = None,
                     img_path: str = "",
                     pre_check_acct: bool = True,
                     pre_check_perm: bool = True) -> dict:
        """메시지 전송  [TG-1]
        img_path       : 이미지 파일 경로 (비어 있으면 텍스트만 전송)
        pre_check_acct : True 이면 발송 전 get_me() 로 계정 제재/밴 확인
        pre_check_perm : True 이면 발송 전 get_permissions() 로 채팅방 권한 확인

        반환값: {"ok": bool, "msg_id": int|None}
          · ok=True, msg_id=정수  → 전송 성공 (서버 확인된 메시지 ID)
          · ok=False, msg_id=None → 전송 실패
        """
        _FAIL = {"ok": False, "msg_id": None}
        if not HAS_TELETHON:
            self._log_fn("telethon 미설치", "ERROR"); return _FAIL

        phone = self._normalize_phone(acct.get("phone", ""))  # 국제 형식 변환

        # ── ① 발송 전 계정 상태 체크 (get_me) — UI 체크박스 연동 ───
        if pre_check_acct:
            try:
                _me_info = self._check_account_status(acct)
                if _me_info.get("restricted") or _me_info.get("banned"):
                    self._log_fn(
                        f"[TG:{phone}] ⛔ 계정 제재/밴 감지 — 발송 건너뜀 "
                        f"({_me_info.get('reason','unknown')})", "ERROR")
                    self._status[phone] = self.ST_BANNED
                    return _FAIL
            except Exception:
                pass  # 상태 체크 실패 시 계속 진행

        # ── ③ 발송 전 채팅방 권한 체크 (get_permissions) — UI 체크박스 연동 ─
        if pre_check_perm:
            try:
                _perm = self.check_peer_permission(acct, peer)
                if not _perm.get("ok", True):
                    self._log_fn(
                        f"[TG:{phone}] ⛔ 채팅방 권한 없음 [{peer}] — 건너뜀 "
                        f"({_perm.get('reason','')})", "ERROR")
                    return _FAIL
            except Exception:
                pass  # 권한 체크 실패 시 계속 진행

        daily_limit = int(acct.get("daily_limit", 500))
        warmup      = acct.get("warmup", False)
        if warmup:
            warmup_day = int(acct.get("warmup_day", 1))
            daily_limit = min(daily_limit,
                              [50, 100, 200, 500][min(warmup_day - 1, 3)])

        if self._daily_cnt.get(phone, 0) >= daily_limit:
            self._log_fn(f"[TG:{phone}] ⚠️ 일일 한도 초과 ({daily_limit}건)", "WARN")
            return _FAIL

        # 이미지 파일 유효성 확인
        _img = img_path.strip() if img_path else ""
        if _img and not __import__("os").path.isfile(_img):
            self._log_fn(f"[TG:{phone}] ⚠️ 이미지 파일 없음: {_img} — 텍스트만 전송", "WARN")
            _img = ""

        try:
            client, loop = self._ensure_client(acct)
            self._start_loop_thread(phone, loop)
            self._status[phone] = self.ST_RUNNING

            sent_holder = {}   # 코루틴 → 외부로 sent 객체 전달

            async def _do_send():
                if not client.is_connected():
                    await client.connect()
                if _img:
                    # 이미지 + 메시지 동시 전송 (Telethon send_file)
                    sent = await client.send_file(peer, _img,
                                                  caption=message if message else None)
                    self._log_fn(f"[TG:{phone}] 📎 이미지 첨부 전송 → {peer}")
                else:
                    sent = await client.send_message(peer, message)
                sent_holder["sent"] = sent  # 반환값 보존

            # v1.79: per-account flood_threshold 반영
            _ft = int(acct.get("flood_threshold", self._max_flood_threshold))
            self._retry_run(phone, loop, _do_send, peer, stop_event,
                            flood_threshold=_ft)

            # ── ② 메시지 ID 추출 ──────────────────────────────
            sent_obj = sent_holder.get("sent")
            msg_id   = getattr(sent_obj, "id", None)

            with self._lock:
                self._daily_cnt[phone] = self._daily_cnt.get(phone, 0) + 1
            self._status[phone] = self.ST_IDLE
            self._log_fn(
                f"[TG:{phone}] ✅ 발송 완료 → {peer}"
                + (f"  (msg_id={msg_id})" if msg_id else ""), "SUCCESS")
            return {"ok": True, "msg_id": msg_id}

        except Exception as e:
            return self._handle_error(phone, e, peer)

    # ── 재시도 + 제재 탐지 ───────────────────────────────────
    def _retry_run(self, phone: str, loop, coro_fn,
                   target: str, stop_event, max_retry: int = 3,
                   flood_threshold: int = None):
        """FloodWaitError 재시도 포함 실행  [v1.78: 임계값 초과 당일 중단]
        flood_threshold: per-account 임계값(초). None이면 엔진 기본값 사용.
        """
        if not HAS_TELETHON:
            raise RuntimeError("telethon 미설치")
        for attempt in range(1, max_retry + 1):
            if stop_event and stop_event.is_set():
                raise InterruptedError("중지 요청")
            # v1.78: frozen / flood_stopped 계정은 즉시 중단
            if self.is_frozen(phone):
                raise InterruptedError(f"[{phone}] FROZEN 계정 — 실행 차단")
            if self.is_flood_stopped(phone):
                raise InterruptedError(f"[{phone}] FloodWait 임계값 초과 당일 중단")
            try:
                self._run_in_loop(loop, coro_fn())
                return
            except _tl_errors.FloodWaitError as e:
                wait = e.seconds + 5
                self._log_fn(
                    f"[TG:{phone}] ⏳ FloodWait {e.seconds}s "
                    f"(시도 {attempt}/{max_retry}) — {wait}s 대기", "WARN")
                # v1.78: FloodWait 임계값 초과 시 당일 중단 (per-account 우선)
                _threshold = flood_threshold if flood_threshold is not None \
                    else self._max_flood_threshold
                if e.seconds >= _threshold:
                    self.mark_flood_stopped(phone, e.seconds)
                    raise InterruptedError(
                        f"FloodWait {e.seconds}s 임계값 초과 → 당일 중단")
                if stop_event:
                    stop_event.wait(wait)
                else:
                    time.sleep(wait)
                if attempt == max_retry:
                    raise
            # 기타 예외는 상위로 전파

    def _handle_error(self, phone: str, exc, target: str) -> dict:
        """제재 탐지 및 상태 업데이트  [TG-2] [v1.78: frozen/dead_link 탐지 추가]
        반환값: {"ok": False, "msg_id": None}
        """
        _FAIL = {"ok": False, "msg_id": None}
        if not HAS_TELETHON:
            self._status[phone] = self.ST_ERROR
            return _FAIL

        err_name  = type(exc).__name__
        err_str   = str(exc).lower()

        # v1.78: frozen 계정 탐지 (method not available for frozen accounts)
        if "frozen" in err_str or "method not available for frozen" in err_str:
            self.mark_frozen(phone)
            return _FAIL

        # v1.78: 없는 채팅방 → dead_link 영구 블랙리스트 등록
        if ("nobody is using" in err_str
                or "no user has" in err_str
                or "invalid peer" in err_str.lower()
                or "peer_id_invalid" in err_str.lower()):
            self.add_dead_link(target)
            self._log_fn(
                f"[TG:{phone}] 🗑 없는 채팅방 → 블랙리스트 등록: {target}", "WARN")
            return _FAIL

        if isinstance(exc, _tl_errors.PeerFloodError):
            self._status[phone] = self.ST_FLOOD
            self._log_fn(
                f"[TG:{phone}] 🚫 PeerFloodError — 당일 발송 중지", "ERROR")
        elif isinstance(exc, _tl_errors.UserBannedInChannelError):
            self._blacklist.add(target)
            self._status[phone] = self.ST_ERROR
            self._log_fn(
                f"[TG:{phone}] ⛔ 채널 밴 → 블랙리스트: {target}", "ERROR")
        elif "AccountBanned" in err_name or "UserDeactivated" in err_name:
            self._status[phone] = self.ST_BANNED
            self._log_fn(
                f"[TG:{phone}] ❌ 계정 밴 — 전체 중지 필요!", "ERROR")
        elif isinstance(exc, InterruptedError):
            # frozen / flood_stopped 에 의한 중단은 이미 처리됨
            if self.is_frozen(phone):
                pass  # 이미 mark_frozen에서 처리
            elif self.is_flood_stopped(phone):
                pass  # 이미 mark_flood_stopped에서 처리
            else:
                self._status[phone] = self.ST_IDLE
                self._log_fn(f"[TG:{phone}] ⏹ 사용자 중지", "WARN")
        else:
            self._status[phone] = self.ST_ERROR
            self._log_fn(f"[TG:{phone}] ❌ 오류: {exc}", "ERROR")
        return _FAIL

    # ── ④ 가입된 채팅방 목록 조회 (iter_dialogs) ──────────────────────
    def get_dialogs(self, acct: dict, limit: int = None) -> list[dict]:
        """계정이 가입된 채팅방/그룹/채널 목록 반환.  [v1.81: 전체 조회 보장]

        반환: [{"name", "id", "username", "type", "unread"}, ...]
          type: "user" | "group" | "channel" | "supergroup"
        limit: None = 전체 조회 (무제한), 숫자 지정 시 상위 N개만

        ※ iter_dialogs는 100개씩 페이지 단위로 API를 호출하므로
          timeout 없이 전용 이벤트 루프에서 완전히 끝날 때까지 대기.
        """
        if not HAS_TELETHON:
            return []
        phone = self._normalize_phone(acct.get("phone", ""))
        try:
            client, loop = self._ensure_client(acct)
            self._start_loop_thread(phone, loop)

            result: list[dict] = []

            async def _fetch_all():
                if not client.is_connected():
                    await client.connect()
                from telethon.tl.types import User, Chat, Channel
                # limit=None → Telethon이 내부적으로 100개씩 페이지 반복 → 전체 수집
                async for dialog in client.iter_dialogs(limit=limit):
                    ent  = dialog.entity
                    name = getattr(ent, "title", None) or \
                           ((getattr(ent, "first_name", "") or "") + " " +
                            (getattr(ent, "last_name",  "") or "")).strip()
                    uname  = getattr(ent, "username", "") or ""
                    eid    = getattr(ent, "id", None)
                    unread = dialog.unread_count
                    if isinstance(ent, User):
                        dtype = "user"
                    elif isinstance(ent, Channel):
                        dtype = "supergroup" if getattr(ent, "megagroup", False) \
                                else "channel"
                    else:
                        dtype = "group"
                    result.append({
                        "name":    name,
                        "id":      eid,
                        "username":uname,
                        "type":    dtype,
                        "unread":  unread,
                    })
                return result

            # timeout을 넉넉하게 (채팅방 1,000개 기준 ~60초, 5,000개 ~300초)
            future = asyncio.run_coroutine_threadsafe(_fetch_all(), loop)
            fetched = future.result(timeout=600)   # 최대 10분 대기
            self._log_fn(
                f"[TG:{phone}] 📋 대화방 목록 {len(fetched)}개 전체 조회 완료", "INFO")
            return fetched

        except Exception as _e:
            self._log_fn(f"[TG:{phone}] ⚠️ 대화방 목록 조회 실패: {_e}", "WARN")
            return []

    def get_dialogs_iter(self, acct: dict,
                        callback,          # callback(batch: list[dict], done: bool, total: int)
                        batch_size: int = 100) -> None:
        """[v1.82] 가입된 채팅방을 100개씩 수집해 callback으로 스트리밍 전달.

        callback(batch, done, total)
          · batch  : 이번에 수집된 dict 리스트
          · done   : True = 마지막 호출(수집 완료)
          · total  : 지금까지 수집된 누적 개수

        ※ 이 메서드는 즉시 반환(백그라운드 스레드에서 실행).
          UI 팝업을 먼저 열고 callback 안에서 after(0, ...) 로 행 추가.
        """
        if not HAS_TELETHON:
            callback([], True, 0)
            return
        phone = self._normalize_phone(acct.get("phone", ""))

        import threading as _thr

        def _worker():
            try:
                client, loop = self._ensure_client(acct)
                self._start_loop_thread(phone, loop)

                collected: list[dict] = []

                async def _stream():
                    if not client.is_connected():
                        await client.connect()
                    from telethon.tl.types import User, Channel
                    buf: list[dict] = []
                    async for dialog in client.iter_dialogs(limit=None):
                        ent  = dialog.entity
                        name = getattr(ent, "title", None) or (
                            (getattr(ent, "first_name", "") or "") + " " +
                            (getattr(ent, "last_name",  "") or "")).strip()
                        uname  = getattr(ent, "username", "") or ""
                        eid    = getattr(ent, "id", None)
                        unread = dialog.unread_count
                        if isinstance(ent, User):
                            dtype = "user"
                        elif isinstance(ent, Channel):
                            dtype = ("supergroup"
                                     if getattr(ent, "megagroup", False)
                                     else "channel")
                        else:
                            dtype = "group"
                        buf.append({
                            "name":    name,
                            "id":      eid,
                            "username":uname,
                            "type":    dtype,
                            "unread":  unread,
                        })
                        # batch_size 개 모이면 즉시 callback
                        if len(buf) >= batch_size:
                            collected.extend(buf)
                            callback(list(buf), False, len(collected))
                            buf.clear()
                    # 잔여분 flush
                    if buf:
                        collected.extend(buf)
                        callback(list(buf), False, len(collected))
                    # 완료 신호
                    callback([], True, len(collected))

                future = asyncio.run_coroutine_threadsafe(_stream(), loop)
                future.result(timeout=600)
                self._log_fn(
                    f"[TG:{phone}] 📋 스트리밍 조회 완료 — "
                    f"총 {len(collected)}개", "INFO")
            except Exception as _e:
                self._log_fn(
                    f"[TG:{phone}] ⚠️ 대화방 스트리밍 조회 실패: {_e}", "WARN")
                callback([], True, 0)

        _thr.Thread(target=_worker, daemon=True).start()

    def get_dialogs_page(self, acct: dict,
                         offset_id: int = 0,
                         offset_date: int = 0,
                         offset_peer=None,
                         limit: int = 100) -> dict:
        """[v1.83] 페이지 단위 수동 조회 — 100개씩 명시적으로 한 페이지만 가져옴.

        반환: {
            "dialogs": [...],       # 이번 페이지 결과
            "next_offset_id":   int,  # 다음 요청에 쓸 offset_id
            "next_offset_date": int,  # 다음 요청에 쓸 offset_date
            "next_offset_peer": obj,  # 다음 요청에 쓸 offset_peer
            "has_more": bool,         # True = 다음 페이지 있음
        }

        ※ Telegram GetDialogsRequest 직접 호출 → 한 번에 정확히 limit개만 반환.
          has_more=False 면 마지막 페이지.
        """
        if not HAS_TELETHON:
            return {"dialogs": [], "has_more": False,
                    "next_offset_id": 0, "next_offset_date": 0,
                    "next_offset_peer": None}
        phone = self._normalize_phone(acct.get("phone", ""))
        try:
            client, loop = self._ensure_client(acct)
            self._start_loop_thread(phone, loop)

            async def _fetch_page():
                if not client.is_connected():
                    await client.connect()

                from telethon.tl.functions.messages import GetDialogsRequest
                from telethon.tl.types import InputPeerEmpty, User, Channel

                peer = offset_peer if offset_peer is not None else InputPeerEmpty()

                result = await client(GetDialogsRequest(
                    offset_date=offset_date,
                    offset_id=offset_id,
                    offset_peer=peer,
                    limit=limit,
                    hash=0,
                ))

                dialogs_out = []
                for dialog in result.dialogs:
                    # entity 찾기
                    try:
                        ent = await client.get_entity(dialog.peer)
                    except Exception:
                        continue
                    name = getattr(ent, "title", None) or (
                        (getattr(ent, "first_name", "") or "") + " " +
                        (getattr(ent, "last_name",  "") or "")).strip()
                    uname  = getattr(ent, "username", "") or ""
                    eid    = getattr(ent, "id", None)
                    unread = dialog.unread_count
                    if isinstance(ent, User):
                        dtype = "user"
                    elif isinstance(ent, Channel):
                        dtype = ("supergroup"
                                 if getattr(ent, "megagroup", False)
                                 else "channel")
                    else:
                        dtype = "group"
                    dialogs_out.append({
                        "name":    name,
                        "id":      eid,
                        "username": uname,
                        "type":    dtype,
                        "unread":  unread,
                    })

                # 다음 페이지 오프셋 계산
                has_more = len(result.dialogs) >= limit
                next_peer = None
                next_id   = 0
                next_date = 0
                if has_more and result.messages:
                    last_msg = result.messages[-1]
                    next_id   = getattr(last_msg, "id",   0)
                    next_date = getattr(last_msg, "date", 0)
                    if hasattr(next_date, "timestamp"):
                        next_date = int(next_date.timestamp())
                    if result.dialogs:
                        last_dlg  = result.dialogs[-1]
                        try:
                            next_peer = await client.get_input_entity(last_dlg.peer)
                        except Exception:
                            next_peer = InputPeerEmpty()

                return {
                    "dialogs":           dialogs_out,
                    "has_more":          has_more,
                    "next_offset_id":    next_id,
                    "next_offset_date":  next_date,
                    "next_offset_peer":  next_peer,
                }

            future = asyncio.run_coroutine_threadsafe(_fetch_page(), loop)
            result = future.result(timeout=120)
            self._log_fn(
                f"[TG:{phone}] 📋 페이지 조회 {len(result['dialogs'])}개 "
                f"(has_more={result['has_more']})", "INFO")
            return result

        except Exception as _e:
            self._log_fn(f"[TG:{phone}] ⚠️ 페이지 조회 실패: {_e}", "WARN")
            return {"dialogs": [], "has_more": False,
                    "next_offset_id": 0, "next_offset_date": 0,
                    "next_offset_peer": None}

    # ── ⑤ 메시지 수정 / 삭제 ────────────────────────────────────────
    def edit_message(self, acct: dict, peer: str,
                     msg_id: int, new_text: str) -> bool:
        """발송된 메시지 내용 수정.
        msg_id: send_message() 반환 dict 의 "msg_id" 값
        반환: True = 성공, False = 실패
        """
        if not HAS_TELETHON or not msg_id:
            return False
        phone = self._normalize_phone(acct.get("phone", ""))
        try:
            client, loop = self._ensure_client(acct)
            self._start_loop_thread(phone, loop)

            async def _edit():
                if not client.is_connected():
                    await client.connect()
                await client.edit_message(peer, msg_id, new_text)

            self._run_in_loop(loop, _edit())
            self._log_fn(
                f"[TG:{phone}] ✏️ 메시지 수정 완료 (id={msg_id}) → {peer}", "SUCCESS")
            return True
        except Exception as _e:
            self._log_fn(f"[TG:{phone}] ⚠️ 메시지 수정 실패: {_e}", "WARN")
            return False

    def delete_message(self, acct: dict, peer: str,
                       msg_id: int, revoke: bool = True) -> bool:
        """발송된 메시지 삭제.
        msg_id : send_message() 반환 dict 의 "msg_id" 값
        revoke : True = 상대방 화면에서도 삭제 (양측 삭제)
        반환   : True = 성공, False = 실패
        """
        if not HAS_TELETHON or not msg_id:
            return False
        phone = self._normalize_phone(acct.get("phone", ""))
        try:
            client, loop = self._ensure_client(acct)
            self._start_loop_thread(phone, loop)

            async def _delete():
                if not client.is_connected():
                    await client.connect()
                await client.delete_messages(peer, [msg_id], revoke=revoke)

            self._run_in_loop(loop, _delete())
            self._log_fn(
                f"[TG:{phone}] 🗑️ 메시지 삭제 완료 (id={msg_id}) → {peer}", "SUCCESS")
            return True
        except Exception as _e:
            self._log_fn(f"[TG:{phone}] ⚠️ 메시지 삭제 실패: {_e}", "WARN")
            return False

    def disconnect_all(self):
        """모든 클라이언트 연결 해제"""
        # [CRIT-03 fix] 반복 중 _clients 가 다른 스레드에서 변경될 수 있으므로 list() 로 스냅샷
        for phone, client in list(self._clients.items()):
            loop = self._loops.get(phone)
            if loop and client.is_connected():
                try:
                    asyncio.run_coroutine_threadsafe(
                        client.disconnect(), loop).result(timeout=5)
                except Exception:
                    pass
        self._log_fn("[TG] 모든 계정 연결 해제", "INFO")


# 전역 TelethonEngine 인스턴스 (앱 시작 시 초기화)
_tg_engine: TelethonEngine | None = None


def _get_tg_engine(log_fn=None, alert_fn=None) -> TelethonEngine:
    """전역 TelethonEngine 싱글톤 반환  [v1.78: alert_fn 연동]"""
    global _tg_engine
    if _tg_engine is None:
        _tg_engine = TelethonEngine(log_fn=log_fn, alert_fn=alert_fn)
    else:
        if log_fn:
            _tg_engine._log_fn = log_fn
        if alert_fn:
            _tg_engine._alert_fn = alert_fn
    return _tg_engine


# ============================================================
# Block 4-C : TelegramAccountsTab — 텔레그램 계정 관리 탭
# ============================================================

class TelegramAccountsTab(tk.Frame):
    """
    텔레그램 계정 관리 탭  [v1.61 TG-4]
    · 계정 추가/수정/삭제 (API ID, API Hash, 전화번호)
    · 일일 한도 설정 + 워밍업 모드
    · 계정별 상태: 🟢실행 / 🟡대기 / 🔴중지 / ⚫밴
    · 연결 테스트 버튼
    """
    def __init__(self, master, app: "App"):
        super().__init__(master, bg=PALETTE["bg"])
        self.app      = app
        self._accounts: list[dict] = []
        self._sel_idx: int = -1
        self._status_poll_id = None
        self._build_ui()
        self._load_accounts()
        self._start_status_poll()

    # ── UI 빌드 ────────────────────────────────────────────
    def _build_ui(self):
        # ── 탭 헤더 ──────────────────────────────────────────
        hdr = tk.Frame(self, bg=PALETTE["bg"])
        hdr.pack(fill=tk.X, pady=(0, 10))

        title_f = tk.Frame(hdr, bg=PALETTE["bg"])
        title_f.pack(side=tk.LEFT)
        tk.Label(title_f, text="✈",
                 font=("Segoe UI Emoji", 15),
                 bg=PALETTE["bg"], fg="#229ED9"
                 ).pack(side=tk.LEFT)
        tk.Label(title_f, text="  텔레그램 계정 관리",
                 font=F_TITLE, bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        tk.Label(title_f,
                 text="  Telethon API 기반 · 최대 15계정 동시 실행",
                 font=F_SMALL, bg=PALETTE["bg"],
                 fg=PALETTE["muted"]).pack(side=tk.LEFT)

        # 구분선
        tk.Frame(self, bg=PALETTE["border"], height=1
                 ).pack(fill=tk.X, pady=(0, 8))

        # Telethon 없음 경고
        if not HAS_TELETHON:
            warn = tk.Frame(self,
                            bg="#FEF9C3",
                            highlightbackground="#FDE047",
                            highlightthickness=1)
            warn.pack(fill=tk.X, pady=(0, 8))
            tk.Label(warn,
                     text="⚠️  telethon 패키지가 설치되지 않았습니다.  "
                          "pip install telethon  후 재시작하세요.",
                     font=F_BODY, bg="#FEF9C3",
                     fg="#713F12", padx=14, pady=8).pack()

        # 좌우 분할
        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL,
                               bg=PALETTE["border2"], sashwidth=5,
                               sashrelief=tk.FLAT)
        paned.pack(fill=tk.BOTH, expand=True)

        # 왼쪽: 계정 목록
        left = tk.Frame(paned, bg=PALETTE["card"],
                        highlightbackground=PALETTE["border"],
                        highlightthickness=1)
        paned.add(left, minsize=200)
        self._build_list_panel(left)

        # 오른쪽: 편집 + 상태
        right = tk.Frame(paned, bg=PALETTE["bg"])
        paned.add(right, minsize=480)
        self._build_edit_panel(right)

    def _build_list_panel(self, parent: tk.Frame):
        # 컬러 헤더 바
        hdr_bar = tk.Frame(parent, bg="#229ED9")
        hdr_bar.pack(fill=tk.X)
        tk.Label(hdr_bar, text="  📱  계정 목록",
                 font=(_FF, 9, "bold"), bg="#229ED9",
                 fg="#FFFFFF").pack(side=tk.LEFT, pady=9)
        # 계정 수 뱃지
        self._acct_count_lbl = tk.Label(hdr_bar, text="0",
                 font=(_FF, 8, "bold"),
                 bg="#1A7FA8", fg="#BAE6FD",
                 padx=7, pady=2)
        self._acct_count_lbl.pack(side=tk.RIGHT, padx=8, pady=6)

        # Treeview (이름 + 상태)
        tv_frame = tk.Frame(parent, bg=PALETTE["card"])
        tv_frame.pack(fill=tk.BOTH, expand=True)

        cols = ("name", "phone", "status", "daily")
        self._tv = ttk.Treeview(tv_frame, columns=cols,
                                show="headings", height=15,
                                selectmode="browse")
        self._tv.heading("name",   text="이름")
        self._tv.heading("phone",  text="전화번호")
        self._tv.heading("status", text="상태")
        self._tv.heading("daily",  text="오늘")
        self._tv.column("name",   width=80, anchor="w")
        self._tv.column("phone",  width=90, anchor="w")
        self._tv.column("status", width=50, anchor="center")
        self._tv.column("daily",  width=40, anchor="center")

        sv = ttk.Scrollbar(tv_frame, orient=tk.VERTICAL,
                           command=self._tv.yview)
        self._tv.configure(yscrollcommand=sv.set)
        sv.pack(side=tk.RIGHT, fill=tk.Y)
        self._tv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._tv.bind("<<TreeviewSelect>>", self._on_select)

        # 색상 태그
        self._tv.tag_configure("running", foreground=PALETTE["success_text"],
                                background="#F0FDF4")
        self._tv.tag_configure("flood",   foreground=PALETTE["warning_text"],
                                background="#FFFBEB")
        self._tv.tag_configure("banned",  foreground=PALETTE["danger"],
                                background="#FEF2F2")
        self._tv.tag_configure("error",   foreground=PALETTE["danger"],
                                background="#FEF2F2")

        # 구분선
        tk.Frame(parent, bg=PALETTE["border"], height=1).pack(fill=tk.X)

        # 하단 버튼
        bf = tk.Frame(parent, bg=PALETTE["card"])
        bf.pack(fill=tk.X, padx=8, pady=8)
        btn_defs = [
            ("＋ 추가", self._add_account,  PALETTE["primary"], "#FFFFFF"),
            ("✎ 수정",  self._edit_account, "#F1F5F9",          PALETTE["text"]),
            ("✕ 삭제",  self._del_account,  "#FEF2F2",          PALETTE["danger"]),
        ]
        for txt, cmd, bg, fg in btn_defs:
            b = tk.Button(bf, text=txt, command=cmd,
                      bg=bg, fg=fg,
                      relief=tk.FLAT, font=(_FF, 8, "bold"),
                      activebackground=_lighten(bg),
                      cursor="hand2", padx=8, pady=5, bd=0)
            b.pack(side=tk.LEFT, padx=(0, 3))
            b.bind("<Enter>", lambda e, b=b, bg=bg: b.config(bg=_lighten(bg)))
            b.bind("<Leave>", lambda e, b=b, bg=bg: b.config(bg=bg))

    def _build_edit_panel(self, parent: tk.Frame):
        # 스크롤 래퍼
        canvas = tk.Canvas(parent, bg=PALETTE["bg"],
                           highlightthickness=0)
        vsb = ttk.Scrollbar(parent, orient="vertical",
                            command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._edit_frame = tk.Frame(canvas, bg=PALETTE["bg"])
        canvas.create_window((0, 0), window=self._edit_frame,
                             anchor="nw", tags="inner")
        self._edit_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")))
        canvas.bind("<MouseWheel>",
                    lambda e: canvas.yview_scroll(
                        int(-1 * (e.delta / 120)), "units"))

        f = self._edit_frame
        self._vars: dict[str, tk.StringVar] = {}

        # ════════════════════════════════════════════════════
        # [전역] API 인증 정보 — 앱 단위, 계정 공통으로 1회만 설정
        # ════════════════════════════════════════════════════
        api_card = tk.Frame(f, bg=PALETTE["hover"],
                            highlightbackground="#93C5FD",
                            highlightthickness=1)
        api_card.pack(fill=tk.X, padx=16, pady=(12, 4))
        api_inner = tk.Frame(api_card, bg=PALETTE["hover"])
        api_inner.pack(fill=tk.X, padx=12, pady=10)

        # 안내 문구
        tk.Label(api_inner,
                 text="🔑  Telegram API 앱 인증 정보  (모든 계정 공통 — 한 번만 입력)",
                 font=(_FF, 9, "bold"), bg=PALETTE["hover"],
                 fg=PALETTE["primary"]).pack(anchor="w", pady=(0, 6))

        api_grid = tk.Frame(api_inner, bg=PALETTE["hover"])
        api_grid.pack(fill=tk.X)

        # API ID
        tk.Label(api_grid, text="API ID",
                 font=F_LABEL, bg=PALETTE["hover"],
                 fg=PALETTE["text2"], anchor="e", width=9
                 ).grid(row=0, column=0, sticky="e", padx=(0, 8), pady=3)
        self._api_id_var = tk.StringVar()
        tk.Entry(api_grid, textvariable=self._api_id_var,
                 font=F_MONO,
                 bg=PALETTE["card"], fg=PALETTE["text"],
                 insertbackground=PALETTE["text"],
                 relief=tk.FLAT,
                 highlightbackground=PALETTE["border"],
                 highlightthickness=1, width=30
                 ).grid(row=0, column=1, sticky="ew", pady=3)

        # API Hash
        tk.Label(api_grid, text="API Hash",
                 font=F_LABEL, bg=PALETTE["hover"],
                 fg=PALETTE["text2"], anchor="e", width=9
                 ).grid(row=1, column=0, sticky="e", padx=(0, 8), pady=3)
        self._api_hash_var = tk.StringVar()
        tk.Entry(api_grid, textvariable=self._api_hash_var,
                 font=F_MONO, show="*",
                 bg=PALETTE["card"], fg=PALETTE["text"],
                 insertbackground=PALETTE["text"],
                 relief=tk.FLAT,
                 highlightbackground=PALETTE["border"],
                 highlightthickness=1, width=30
                 ).grid(row=1, column=1, sticky="ew", pady=3)
        api_grid.columnconfigure(1, weight=1)

        # 발급 안내 + API 저장 버튼
        api_btn_row = tk.Frame(api_inner, bg=PALETTE["hover"])
        api_btn_row.pack(fill=tk.X, pady=(6, 0))
        tk.Label(api_btn_row,
                 text="💡 my.telegram.org → API development tools 에서 발급",
                 font=F_SMALL, bg=PALETTE["hover"],
                 fg=PALETTE["muted"]).pack(side=tk.LEFT)
        tk.Button(api_btn_row, text="💾 API 저장",
                  command=self._save_global_api,
                  font=F_BTN_S, bg=PALETTE["primary"], fg="#fff",
                  activebackground=PALETTE["primary2"],
                  relief=tk.FLAT, cursor="hand2",
                  padx=12, pady=4, bd=0
                  ).pack(side=tk.RIGHT)

        # 저장된 전역 API 값 불러오기
        _cfg = load_json(CONFIG_PATH, {})
        self._api_id_var.set(_cfg.get("tg_api", {}).get("api_id", ""))
        self._api_hash_var.set(_cfg.get("tg_api", {}).get("api_hash", ""))

        # ════════════════════════════════════════════════════
        # [개별] 계정 정보 — 이름 + 전화번호만
        # ════════════════════════════════════════════════════
        self._sec_label(f, "📱 계정 정보")
        grid = tk.Frame(f, bg=PALETTE["bg"])
        grid.pack(fill=tk.X, padx=16, pady=(0, 12))

        fields = [
            ("표시 이름",  "name",  False),
            ("전화번호",   "phone", False),
        ]
        for row_i, (label, key, is_pwd) in enumerate(fields):
            tk.Label(grid, text=label,
                     font=F_LABEL, bg=PALETTE["bg"],
                     fg=PALETTE["text2"], anchor="e", width=10
                     ).grid(row=row_i, column=0,
                            sticky="e", padx=(0, 8), pady=4)
            var = tk.StringVar()
            self._vars[key] = var
            tk.Entry(grid, textvariable=var,
                     font=F_MONO,
                     bg=PALETTE["card2"],
                     fg=PALETTE["text"],
                     insertbackground=PALETTE["text"],
                     relief=tk.FLAT,
                     highlightbackground=PALETTE["border"],
                     highlightthickness=1,
                     width=34
                     ).grid(row=row_i, column=1,
                            sticky="ew", pady=4)
        grid.columnconfigure(1, weight=1)

        # ── 섹션: 발송 설정 ───────────────────────────────
        self._sec_label(f, "⚙️ 발송 설정")
        cfg_f = tk.Frame(f, bg=PALETTE["bg"])
        cfg_f.pack(fill=tk.X, padx=16, pady=(0, 12))

        # 일일 한도
        tk.Label(cfg_f, text="일일 한도",
                 font=F_LABEL, bg=PALETTE["bg"],
                 fg=PALETTE["text2"]).grid(
                     row=0, column=0, sticky="e",
                     padx=(0, 8), pady=4)
        self._vars["daily_limit"] = tk.StringVar(value="500")
        tk.Spinbox(cfg_f, from_=10, to=1000, increment=10,
                   textvariable=self._vars["daily_limit"],
                   font=F_MONO, width=8,
                   bg=PALETTE["card2"], fg=PALETTE["text"],
                   relief=tk.FLAT,
                   highlightbackground=PALETTE["border"],
                   highlightthickness=1,
                   ).grid(row=0, column=1, sticky="w", pady=4)
        tk.Label(cfg_f, text="건/일",
                 font=F_SMALL, bg=PALETTE["bg"],
                 fg=PALETTE["muted"]).grid(
                     row=0, column=2, sticky="w", padx=(4, 0))

        # 워밍업 모드
        self._warmup_var = tk.BooleanVar(value=False)
        tk.Checkbutton(cfg_f, text="워밍업 모드 (신규 계정 — 50→100→200→500 자동 조절)",
                       variable=self._warmup_var,
                       font=F_LABEL,
                       bg=PALETTE["bg"], fg=PALETTE["text"],
                       selectcolor=PALETTE["card2"],
                       activebackground=PALETTE["bg"]
                       ).grid(row=1, column=0, columnspan=3,
                              sticky="w", pady=4)

        # 워밍업 날짜
        tk.Label(cfg_f, text="워밍업 일차",
                 font=F_LABEL, bg=PALETTE["bg"],
                 fg=PALETTE["text2"]).grid(
                     row=2, column=0, sticky="e",
                     padx=(0, 8), pady=4)
        self._vars["warmup_day"] = tk.StringVar(value="1")
        tk.Spinbox(cfg_f, from_=1, to=30,
                   textvariable=self._vars["warmup_day"],
                   font=F_MONO, width=5,
                   bg=PALETTE["card2"], fg=PALETTE["text"],
                   relief=tk.FLAT,
                   highlightbackground=PALETTE["border"],
                   highlightthickness=1,
                   ).grid(row=2, column=1, sticky="w", pady=4)

        # v1.78: 일일 가입 한도 (frozen 예방)
        tk.Label(cfg_f, text="일일 가입 한도",
                 font=F_LABEL, bg=PALETTE["bg"],
                 fg=PALETTE["text2"]).grid(
                     row=3, column=0, sticky="e",
                     padx=(0, 8), pady=4)
        self._vars["daily_join_limit"] = tk.StringVar(value="50")
        tk.Spinbox(cfg_f, from_=5, to=200, increment=5,
                   textvariable=self._vars["daily_join_limit"],
                   font=F_MONO, width=8,
                   bg=PALETTE["card2"], fg=PALETTE["text"],
                   relief=tk.FLAT,
                   highlightbackground=PALETTE["border"],
                   highlightthickness=1,
                   ).grid(row=3, column=1, sticky="w", pady=4)
        tk.Label(cfg_f, text="회/일  ⚠️ 50 초과 시 frozen 위험",
                 font=F_SMALL, bg=PALETTE["bg"],
                 fg="#EF4444").grid(
                     row=3, column=2, sticky="w", padx=(4, 0))

        # v1.78: FloodWait 임계값
        tk.Label(cfg_f, text="FloodWait 중단",
                 font=F_LABEL, bg=PALETTE["bg"],
                 fg=PALETTE["text2"]).grid(
                     row=4, column=0, sticky="e",
                     padx=(0, 8), pady=4)
        self._vars["flood_threshold"] = tk.StringVar(value="600")
        tk.Spinbox(cfg_f, from_=60, to=3600, increment=60,
                   textvariable=self._vars["flood_threshold"],
                   font=F_MONO, width=8,
                   bg=PALETTE["card2"], fg=PALETTE["text"],
                   relief=tk.FLAT,
                   highlightbackground=PALETTE["border"],
                   highlightthickness=1,
                   ).grid(row=4, column=1, sticky="w", pady=4)
        tk.Label(cfg_f, text="초 초과 시 당일 중단",
                 font=F_SMALL, bg=PALETTE["bg"],
                 fg=PALETTE["muted"]).grid(
                     row=4, column=2, sticky="w", padx=(4, 0))
        cfg_f.columnconfigure(1, weight=1)

        # ── 섹션: 상태 및 통계 ───────────────────────────
        self._sec_label(f, "📊 실시간 상태")
        stat_f = tk.Frame(f, bg=PALETTE["card"],
                          highlightbackground=PALETTE["border"],
                          highlightthickness=1)
        stat_f.pack(fill=tk.X, padx=16, pady=(0, 12))
        inner_s = tk.Frame(stat_f, bg=PALETTE["card"])
        inner_s.pack(fill=tk.X, padx=12, pady=8)

        self._status_var  = tk.StringVar(value="—")
        self._daily_var   = tk.StringVar(value="0건")
        self._engine_var  = tk.StringVar(value="미연결")

        for label, var in [
            ("계정 상태",  self._status_var),
            ("오늘 발송",  self._daily_var),
            ("엔진 상태",  self._engine_var),
        ]:
            row = tk.Frame(inner_s, bg=PALETTE["card"])
            row.pack(fill=tk.X, pady=2)
            tk.Label(row, text=label, font=F_LABEL,
                     bg=PALETTE["card"], fg=PALETTE["text2"],
                     width=10, anchor="e").pack(side=tk.LEFT,
                                                padx=(0, 8))
            tk.Label(row, textvariable=var, font=F_BODY,
                     bg=PALETTE["card"],
                     fg=PALETTE["text"]).pack(side=tk.LEFT)

        # ── 버튼 행 ───────────────────────────────────────
        btn_row = tk.Frame(f, bg=PALETTE["bg"])
        btn_row.pack(fill=tk.X, padx=16, pady=(4, 16))

        save_btn = tk.Button(
            btn_row, text="💾 저장",
            command=self._save_account,
            font=F_BTN, bg=PALETTE["primary"], fg="#fff",
            activebackground=PALETTE["primary2"],
            activeforeground="#fff",
            relief=tk.FLAT, cursor="hand2",
            padx=16, pady=6, bd=0)
        save_btn.pack(side=tk.LEFT, padx=(0, 8))

        conn_btn = tk.Button(
            btn_row, text="🔗 연결 테스트",
            command=self._test_connect,
            font=F_BTN, bg=PALETTE["success"], fg="#fff",
            activebackground=_lighten(PALETTE["success"], -0.1),
            activeforeground="#fff",
            relief=tk.FLAT, cursor="hand2",
            padx=16, pady=6, bd=0)
        conn_btn.pack(side=tk.LEFT, padx=(0, 8))

        reset_btn = tk.Button(
            btn_row, text="🔄 일일 카운터 초기화",
            command=self._reset_daily,
            font=F_BTN_S, bg=PALETTE["card"],
            fg=PALETTE["text2"],
            activebackground=PALETTE["hover"],
            relief=tk.FLAT, cursor="hand2",
            padx=12, pady=6, bd=0)
        reset_btn.pack(side=tk.LEFT, padx=(0, 8))

        dialog_btn = tk.Button(
            btn_row, text="📋 대화방 목록",
            command=self._show_dialogs,
            font=F_BTN_S, bg=PALETTE.get("info", "#2196f3"), fg="#fff",
            activebackground="#1976d2",
            activeforeground="#fff",
            relief=tk.FLAT, cursor="hand2",
            padx=12, pady=6, bd=0)
        dialog_btn.pack(side=tk.LEFT, padx=(0, 8))

        acct_check_btn = tk.Button(
            btn_row, text="🔍 계정 상태 확인",
            command=self._check_acct_status_ui,
            font=F_BTN_S, bg=PALETTE.get("warning", "#f59e0b"), fg="#fff",
            activebackground="#d97706",
            activeforeground="#fff",
            relief=tk.FLAT, cursor="hand2",
            padx=12, pady=6, bd=0)
        acct_check_btn.pack(side=tk.LEFT, padx=(0, 8))

        all_check_btn = tk.Button(
            btn_row, text="🔍 전체 계정 확인",
            command=self._check_all_accts_ui,
            font=F_BTN_S, bg=PALETTE.get("warning", "#f59e0b"), fg="#fff",
            activebackground="#d97706",
            activeforeground="#fff",
            relief=tk.FLAT, cursor="hand2",
            padx=12, pady=6, bd=0)
        all_check_btn.pack(side=tk.LEFT, padx=(0, 8))

        # v1.78: t.me 링크 추출 버튼
        extract_btn = tk.Button(
            btn_row, text="🔗 링크 추출",
            command=self._extract_tme_links,
            font=F_BTN_S, bg="#7C3AED", fg="#fff",
            activebackground="#6D28D9",
            activeforeground="#fff",
            relief=tk.FLAT, cursor="hand2",
            padx=12, pady=6, bd=0)
        extract_btn.pack(side=tk.LEFT, padx=(0, 8))

        # v1.78: frozen 계정 해제 버튼
        unfreeze_btn = tk.Button(
            btn_row, text="🔓 Frozen 해제",
            command=self._unfreeze_account,
            font=F_BTN_S, bg="#DC2626", fg="#fff",
            activebackground="#B91C1C",
            activeforeground="#fff",
            relief=tk.FLAT, cursor="hand2",
            padx=12, pady=6, bd=0)
        unfreeze_btn.pack(side=tk.LEFT)

        # ── 안내 ──────────────────────────────────────────
        note_f = tk.Frame(f, bg=PALETTE["card2"],
                          highlightbackground=PALETTE["border"],
                          highlightthickness=1)
        note_f.pack(fill=tk.X, padx=16, pady=(0, 8))
        note_inner = tk.Frame(note_f, bg=PALETTE["card2"])
        note_inner.pack(fill=tk.X, padx=12, pady=8)
        tk.Label(note_inner,
                 text=(
                     "⚠️  처음 연결 시 전화번호로 OTP 인증이 필요합니다.\n"
                     "   연결 테스트 버튼을 클릭하면 콘솔에 인증 코드 입력 창이 뜹니다."
                 ),
                 font=F_SMALL, bg=PALETTE["card2"],
                 fg=PALETTE["muted"], justify=tk.LEFT,
                 anchor="nw", padx=4, pady=2
                 ).pack(fill=tk.X)

    # ── v1.78: t.me 링크 자동 추출 ────────────────────────────
    def _extract_tme_links(self):
        """계정 목록(tg_accounts.json) 및 클립보드/텍스트에서
        https://t.me/xxx 형태의 링크를 추출해 별도 창으로 표시.
        """
        import re as _re
        results = []

        # 1) 계정 목록에서 추출
        accts = load_json(TG_ACCOUNTS_PATH, [])
        if isinstance(accts, dict):
            accts = accts.get("accounts", [])
        for a in accts:
            for field in ("name", "phone", "note", "description", "link"):
                val = str(a.get(field, "") or "")
                found = _re.findall(
                    r'https?://t\.me/[\w+/\-]+|t\.me/[\w+/\-]+', val)
                results.extend(found)

        # 2) 소스 선택 다이얼로그
        src_win = tk.Toplevel(self)
        src_win.title("🔗 t.me 링크 추출")
        src_win.geometry("620x520")
        src_win.configure(bg=PALETTE["bg"])
        src_win.grab_set()

        tk.Label(src_win,
                 text="📋  t.me 링크 추출기  (v1.78)",
                 font=F_TITLE, bg=PALETTE["bg"],
                 fg=PALETTE["primary"]).pack(pady=(14, 4))
        tk.Label(src_win,
                 text="아래 텍스트 박스에 채팅방 목록을 붙여넣으세요.\n"
                      "t.me/xxx 또는 https://t.me/xxx 형식의 링크를 자동으로 추출합니다.",
                 font=F_SMALL, bg=PALETTE["bg"],
                 fg=PALETTE["muted"], justify=tk.LEFT).pack(padx=16, anchor="w")

        # 입력 텍스트박스
        input_frame = tk.Frame(src_win, bg=PALETTE["card"],
                               highlightbackground=PALETTE["border"],
                               highlightthickness=1)
        input_frame.pack(fill=tk.X, padx=16, pady=(6, 4))
        tk.Label(input_frame, text="📥 입력 (자유 형식)",
                 font=(_FF, 8, "bold"), bg=PALETTE["card"],
                 fg=PALETTE["muted"]).pack(anchor="w", padx=8, pady=(6, 2))
        in_text = tk.Text(input_frame, height=8,
                          font=F_MONO, wrap=tk.WORD,
                          bg=PALETTE["card2"], fg=PALETTE["text"],
                          insertbackground=PALETTE["text"],
                          relief=tk.FLAT,
                          highlightbackground=PALETTE["border"],
                          highlightthickness=1)
        in_text.pack(fill=tk.X, padx=8, pady=(0, 8))

        # 결과 텍스트박스
        out_frame = tk.Frame(src_win, bg=PALETTE["card"],
                             highlightbackground=PALETTE["border"],
                             highlightthickness=1)
        out_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 4))
        result_hdr = tk.Frame(out_frame, bg=PALETTE["card"])
        result_hdr.pack(fill=tk.X)
        _link_count_var = tk.StringVar(value="📤 추출 결과 — 0건")
        tk.Label(result_hdr, textvariable=_link_count_var,
                 font=(_FF, 8, "bold"), bg=PALETTE["card"],
                 fg=PALETTE["muted"]).pack(side=tk.LEFT, padx=8, pady=(6, 2))

        def _do_copy():
            txt = out_text.get("1.0", tk.END).strip()
            if txt:
                src_win.clipboard_clear()
                src_win.clipboard_append(txt)
                _link_count_var.set(
                    _link_count_var.get() + "  ✅ 복사됨")
        tk.Button(result_hdr, text="📋 복사",
                  command=_do_copy,
                  font=F_BTN_S, bg=PALETTE["primary"], fg="#fff",
                  relief=tk.FLAT, cursor="hand2", padx=8, pady=2, bd=0
                  ).pack(side=tk.RIGHT, padx=8, pady=4)

        out_sb = ttk.Scrollbar(out_frame, orient=tk.VERTICAL)
        out_text = tk.Text(out_frame, height=10,
                           font=F_MONO, wrap=tk.WORD,
                           bg=PALETTE["card2"], fg="#059669",
                           insertbackground=PALETTE["text"],
                           relief=tk.FLAT,
                           highlightbackground=PALETTE["border"],
                           highlightthickness=1,
                           yscrollcommand=out_sb.set)
        out_sb.configure(command=out_text.yview)
        out_sb.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 4))
        out_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        def _extract():
            raw = in_text.get("1.0", tk.END)
            found = _re.findall(
                r'https?://t\.me/[\w+/\-]{2,}|(?<![/\w])t\.me/[\w+/\-]{2,}',
                raw)
            # 정규화: https://t.me/ 형식으로 통일
            normalized = []
            seen = set()
            for lnk in found:
                if not lnk.startswith("http"):
                    lnk = "https://" + lnk
                lnk = lnk.rstrip("/")
                key = lnk.lower()
                if key not in seen:
                    seen.add(key)
                    normalized.append(lnk)
            out_text.delete("1.0", tk.END)
            out_text.insert(tk.END, "\n".join(normalized))
            _link_count_var.set(
                f"📤 추출 결과 — {len(normalized)}건")

        btn_row2 = tk.Frame(src_win, bg=PALETTE["bg"])
        btn_row2.pack(fill=tk.X, padx=16, pady=(0, 12))
        tk.Button(btn_row2, text="🔍 링크 추출 실행",
                  command=_extract,
                  font=F_BTN, bg="#7C3AED", fg="#fff",
                  activebackground="#6D28D9",
                  relief=tk.FLAT, cursor="hand2",
                  padx=16, pady=6, bd=0).pack(side=tk.LEFT, padx=(0, 8))
        tk.Button(btn_row2, text="닫기",
                  command=src_win.destroy,
                  font=F_BTN_S, bg=PALETTE["card"],
                  fg=PALETTE["text2"],
                  relief=tk.FLAT, cursor="hand2",
                  padx=12, pady=6, bd=0).pack(side=tk.LEFT)

        # 이미 추출된 결과가 있으면 미리 표시
        if results:
            seen2 = set()
            uniq = []
            for lnk in results:
                if not lnk.startswith("http"):
                    lnk = "https://" + lnk
                lnk = lnk.rstrip("/")
                if lnk.lower() not in seen2:
                    seen2.add(lnk.lower())
                    uniq.append(lnk)
            out_text.insert(tk.END, "\n".join(uniq))
            _link_count_var.set(
                f"📤 추출 결과 — {len(uniq)}건 (계정 메타에서)")

    # ── v1.78: Frozen 계정 해제 ────────────────────────────────
    def _unfreeze_account(self):
        """선택한 계정의 frozen/flood_stopped 상태를 수동 해제"""
        acct = self._get_selected_account()
        if not acct:
            messagebox.showwarning("선택 오류", "계정을 먼저 선택하세요.")
            return
        eng = getattr(self.app, "_tg_engine", None)
        if not eng:
            messagebox.showwarning("오류", "텔레그램 엔진이 초기화되지 않았습니다.")
            return
        phone = eng._normalize_phone(acct.get("phone", ""))
        with eng._lock:
            eng._frozen_accounts.discard(phone)
            eng._flood_stopped.discard(phone)
            eng._status[phone] = TelethonEngine.ST_IDLE
        self.app._set_status(
            f"🔓 [{phone}] frozen/flood_stopped 해제 완료 — 상태 idle로 복원")
        if hasattr(self.app, "_log_tab"):
            self.app._log_tab.append(
                f"[TG:{phone}] 🔓 Frozen 수동 해제 — 상태 초기화",
                "WARN", "계정관리")
        self._refresh_tv()

    def _save_global_api(self):
        """전역 API ID / API Hash를 config.json에 저장"""
        api_id   = self._api_id_var.get().strip()
        api_hash = self._api_hash_var.get().strip()
        if not api_id or not api_hash:
            messagebox.showwarning("입력 오류",
                                   "API ID와 API Hash를 모두 입력하세요.")
            return
        try:
            int(api_id)
        except ValueError:
            messagebox.showwarning("입력 오류", "API ID는 숫자여야 합니다.")
            return
        cfg = load_json(CONFIG_PATH, self.app._default_config())
        cfg.setdefault("tg_api", {})
        cfg["tg_api"]["api_id"]   = api_id
        cfg["tg_api"]["api_hash"] = api_hash
        save_json(CONFIG_PATH, cfg)
        self.app.config_data = cfg
        self.app._set_status("✅ API 인증 정보 저장 완료 — 계정을 추가하고 연결 테스트를 진행하세요.")

    def _sec_label(self, parent, text: str):
        """섹션 구분 레이블 (개선판)"""
        f = tk.Frame(parent, bg=PALETTE["bg"])
        f.pack(fill=tk.X, padx=16, pady=(12, 4))
        # 좌측 4px 컬러 바
        tk.Frame(f, bg="#229ED9", width=4
                 ).pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(f, text=f"  {text}", font=F_HEAD,
                 bg=PALETTE["bg"],
                 fg=PALETTE["text"]).pack(side=tk.LEFT)
        tk.Frame(f, bg=PALETTE["border"], height=1
                 ).pack(side=tk.LEFT, fill=tk.X,
                        expand=True, padx=(12, 0))

    # ── 데이터 로드/저장 ───────────────────────────────────
    def _load_accounts(self):
        self._accounts = load_json(TG_ACCOUNTS_PATH, [])
        if not isinstance(self._accounts, list):
            self._accounts = []
        self._refresh_tv()

    def _save_accounts_file(self):
        save_json(TG_ACCOUNTS_PATH, self._accounts)
        # TelethonEngine에 반영
        eng = _get_tg_engine()
        eng.load_accounts(self._accounts)

    # ── Treeview 갱신 ──────────────────────────────────────
    def _refresh_tv(self):
        self._tv.delete(*self._tv.get_children())
        eng = _get_tg_engine()
        for acct in self._accounts:
            phone  = str(acct.get("phone", ""))
            st_raw = eng.get_account_status(phone)
            cnt    = eng.get_daily_count(phone)
            # v1.78: frozen/stopped 아이콘 추가
            st_ico = {"idle": "🟡", "running": "🟢",
                      "flood": "🟠", "banned": "⚫",
                      "error": "🔴",
                      "frozen": "🚨", "stopped": "🛑"}.get(st_raw, "🟡")
            tag = st_raw if st_raw in (
                "running", "flood", "banned", "error",
                "frozen", "stopped") else ""
            self._tv.insert(
                "", "end",
                values=(acct.get("name", ""), phone, st_ico, f"{cnt}"),
                tags=(tag,) if tag else ())
        # v1.78: frozen/stopped 태그 색상
        self._tv.tag_configure("frozen",  foreground="#B91C1C",
                                background="#FEE2E2")
        self._tv.tag_configure("stopped", foreground="#92400E",
                                background="#FEF3C7")
        # 계정 수 뱃지 업데이트
        if hasattr(self, "_acct_count_lbl"):
            self._acct_count_lbl.config(text=str(len(self._accounts)))

    def _on_select(self, event=None):
        sel = self._tv.selection()
        if not sel:
            return
        idx = self._tv.index(sel[0])
        # [WARN-03 fix] 인덱스가 _accounts 범위를 벗어날 경우 IndexError 방지
        if idx < 0 or idx >= len(self._accounts):
            return
        self._sel_idx = idx
        self._fill_form(self._accounts[idx])

    def _get_selected_account(self) -> dict | None:
        """현재 선택된 계정 dict 반환, 없으면 None"""
        if self._sel_idx < 0 or self._sel_idx >= len(self._accounts):
            return None
        return self._accounts[self._sel_idx]

    def _fill_form(self, acct: dict):
        for key, var in self._vars.items():
            if key == "daily_join_limit":
                var.set(str(acct.get(key, "50")))
            elif key == "flood_threshold":
                var.set(str(acct.get(key, "600")))
            else:
                var.set(str(acct.get(key, "")))
        self._warmup_var.set(bool(acct.get("warmup", False)))

        phone  = str(acct.get("phone", ""))
        eng    = _get_tg_engine()
        st_raw = eng.get_account_status(phone)
        cnt    = eng.get_daily_count(phone)
        # v1.78: frozen/stopped 상태 표시 추가
        st_kor = {
            "idle":    "대기 🟡",
            "running": "실행 중 🟢",
            "flood":   "Flood 중지 🟠",
            "banned":  "계정 밴 ⚫",
            "error":   "오류 🔴",
            "frozen":  "FROZEN 🚨",
            "stopped": "당일 중단 🛑",
        }.get(st_raw, "대기 🟡")
        self._status_var.set(st_kor)
        self._daily_var.set(f"{cnt}건")
        self._engine_var.set("연결됨" if st_raw != "idle" or
                             phone in _get_tg_engine()._clients else "미연결")

    def _collect_form(self) -> dict:
        d = {k: v.get().strip() for k, v in self._vars.items()}
        d["warmup"]           = self._warmup_var.get()
        d["daily_limit"]      = safe_int(d.get("daily_limit", "500"), 500)
        d["warmup_day"]       = safe_int(d.get("warmup_day", "1"), 1)
        # v1.78: 새 필드
        d["daily_join_limit"] = safe_int(d.get("daily_join_limit", "50"), 50)
        d["flood_threshold"]  = safe_int(d.get("flood_threshold", "600"), 600)
        # 전화번호 자동 국제 형식 변환 (+82 등)
        raw_phone = d.get("phone", "")
        normalized = TelethonEngine._normalize_phone(raw_phone)
        if normalized and normalized != raw_phone:
            d["phone"] = normalized
            # UI 필드도 업데이트
            if "phone" in self._vars:
                self._vars["phone"].set(normalized)
        return d

    # ── 추가/수정/삭제 ─────────────────────────────────────
    def _add_account(self):
        self._sel_idx = -1
        for v in self._vars.values():
            v.set("")
        self._vars["daily_limit"].set("500")
        self._vars["warmup_day"].set("1")
        self._vars["daily_join_limit"].set("50")
        self._vars["flood_threshold"].set("600")
        self._warmup_var.set(False)

    def _edit_account(self):
        if self._sel_idx < 0:
            messagebox.showwarning("선택 없음", "수정할 계정을 선택하세요.")
            return
        self._fill_form(self._accounts[self._sel_idx])

    def _del_account(self):
        if self._sel_idx < 0:
            messagebox.showwarning("선택 없음", "삭제할 계정을 선택하세요.")
            return
        name = self._accounts[self._sel_idx].get("name", "")
        if not messagebox.askyesno("삭제 확인",
                                   f"'{name}' 계정을 삭제하시겠습니까?"):
            return
        self._accounts.pop(self._sel_idx)
        self._sel_idx = -1
        self._save_accounts_file()
        self._refresh_tv()

    def _save_account(self):
        data = self._collect_form()
        if not data.get("phone"):
            messagebox.showwarning("입력 오류", "전화번호를 입력하세요.")
            return
        # 전역 API 설정 여부 확인
        _cfg = load_json(CONFIG_PATH, {})
        _tg  = _cfg.get("tg_api", {})
        if not _tg.get("api_id") or not _tg.get("api_hash"):
            messagebox.showwarning(
                "API 미설정",
                "상단의 API 인증 정보(API ID / API Hash)를 먼저 입력하고\n"
                "💾 API 저장 버튼을 눌러 저장하세요.")
            return

        if self._sel_idx < 0:
            self._accounts.append(data)
            self._sel_idx = len(self._accounts) - 1
        else:
            self._accounts[self._sel_idx] = data

        self._save_accounts_file()
        self._refresh_tv()
        self.app._set_status(f"✅ 계정 '{data['name']}' 저장 완료.")

    def _test_connect(self):
        """연결 테스트 — OTP / 2FA 인증 다이얼로그 포함"""
        if self._sel_idx < 0:
            messagebox.showwarning("선택 없음", "테스트할 계정을 선택하세요.")
            return
        # 전역 API 설정 확인
        _cfg = load_json(CONFIG_PATH, {})
        if not _cfg.get("tg_api", {}).get("api_id"):
            messagebox.showwarning("API 미설정",
                                   "상단 API 인증 정보를 먼저 저장하세요.")
            return

        acct  = self._accounts[self._sel_idx]
        phone = TelethonEngine._normalize_phone(acct.get("phone", ""))  # 국제 형식 변환

        # ── OTP / 2FA 입력을 메인 스레드에서 받는 콜백 ────────
        # 스레드 → 메인 스레드 간 값 전달용 queue
        import queue as _q
        _otp_q = _q.Queue()
        _pw_q  = _q.Queue()

        def _ask_otp(ph: str) -> str:
            """메인 스레드에서 OTP 입력 다이얼로그 실행"""
            def _show():
                dlg = tk.Toplevel(self.app)
                dlg.title("Telegram OTP 인증")
                dlg.resizable(False, False)
                dlg.grab_set()
                dlg.focus_force()
                # 창 중앙 배치
                dlg.update_idletasks()
                w, h = 380, 220
                x = self.app.winfo_x() + (self.app.winfo_width()  - w) // 2
                y = self.app.winfo_y() + (self.app.winfo_height() - h) // 2
                dlg.geometry(f"{w}x{h}+{x}+{y}")
                dlg.configure(bg=PALETTE["card"])

                tk.Label(dlg, text="📲  텔레그램 OTP 인증",
                         font=(_FF, 12, "bold"),
                         bg=PALETTE["card"], fg=PALETTE["primary"]
                         ).pack(pady=(18, 4))
                tk.Label(dlg,
                         text=f"전화번호 {ph} 로 전송된\n인증 코드를 입력하세요.",
                         font=F_BODY, bg=PALETTE["card"],
                         fg=PALETTE["text2"]
                         ).pack(pady=(0, 12))

                code_var = tk.StringVar()
                entry = tk.Entry(dlg, textvariable=code_var,
                                 font=(_FF, 14, "bold"),
                                 justify="center", width=12,
                                 bg=PALETTE["card2"],
                                 fg=PALETTE["primary"],
                                 insertbackground=PALETTE["primary"],
                                 relief=tk.FLAT,
                                 highlightbackground=PALETTE["border"],
                                 highlightthickness=2)
                entry.pack(pady=(0, 14))
                entry.focus_set()

                def _confirm(event=None):
                    _otp_q.put(code_var.get().strip())
                    dlg.destroy()

                def _cancel():
                    _otp_q.put("")
                    dlg.destroy()

                btn_f = tk.Frame(dlg, bg=PALETTE["card"])
                btn_f.pack()
                tk.Button(btn_f, text="✅ 확인",
                          command=_confirm,
                          font=F_BTN, bg=PALETTE["primary"], fg="#fff",
                          relief=tk.FLAT, cursor="hand2",
                          padx=16, pady=6, bd=0
                          ).pack(side=tk.LEFT, padx=(0, 8))
                tk.Button(btn_f, text="취소",
                          command=_cancel,
                          font=F_BTN, bg=PALETTE["card2"],
                          fg=PALETTE["text2"],
                          relief=tk.FLAT, cursor="hand2",
                          padx=12, pady=6, bd=0
                          ).pack(side=tk.LEFT)
                entry.bind("<Return>", _confirm)
                dlg.protocol("WM_DELETE_WINDOW", _cancel)

            self.app.after(0, _show)
            return _otp_q.get()   # 스레드 블로킹 대기

        def _ask_password(ph: str) -> str:
            """메인 스레드에서 2FA 비밀번호 입력 다이얼로그 실행"""
            def _show():
                dlg = tk.Toplevel(self.app)
                dlg.title("Telegram 2FA 비밀번호")
                dlg.resizable(False, False)
                dlg.grab_set()
                dlg.focus_force()
                dlg.update_idletasks()
                w, h = 380, 210
                x = self.app.winfo_x() + (self.app.winfo_width()  - w) // 2
                y = self.app.winfo_y() + (self.app.winfo_height() - h) // 2
                dlg.geometry(f"{w}x{h}+{x}+{y}")
                dlg.configure(bg=PALETTE["card"])

                tk.Label(dlg, text="🔐  2단계 인증 비밀번호",
                         font=(_FF, 12, "bold"),
                         bg=PALETTE["card"], fg=PALETTE["warning"]
                         ).pack(pady=(18, 4))
                tk.Label(dlg,
                         text=f"{ph} 계정의 2FA 비밀번호를 입력하세요.",
                         font=F_BODY, bg=PALETTE["card"],
                         fg=PALETTE["text2"]
                         ).pack(pady=(0, 12))

                pw_var = tk.StringVar()
                entry = tk.Entry(dlg, textvariable=pw_var,
                                 show="*",
                                 font=(_FF, 13),
                                 justify="center", width=18,
                                 bg=PALETTE["card2"],
                                 fg=PALETTE["text"],
                                 insertbackground=PALETTE["text"],
                                 relief=tk.FLAT,
                                 highlightbackground=PALETTE["border"],
                                 highlightthickness=2)
                entry.pack(pady=(0, 14))
                entry.focus_set()

                def _confirm(event=None):
                    _pw_q.put(pw_var.get())
                    dlg.destroy()

                def _cancel():
                    _pw_q.put("")
                    dlg.destroy()

                btn_f = tk.Frame(dlg, bg=PALETTE["card"])
                btn_f.pack()
                tk.Button(btn_f, text="✅ 확인",
                          command=_confirm,
                          font=F_BTN, bg=PALETTE["warning"], fg="#fff",
                          relief=tk.FLAT, cursor="hand2",
                          padx=16, pady=6, bd=0
                          ).pack(side=tk.LEFT, padx=(0, 8))
                tk.Button(btn_f, text="취소",
                          command=_cancel,
                          font=F_BTN, bg=PALETTE["card2"],
                          fg=PALETTE["text2"],
                          relief=tk.FLAT, cursor="hand2",
                          padx=12, pady=6, bd=0
                          ).pack(side=tk.LEFT)
                entry.bind("<Return>", _confirm)
                dlg.protocol("WM_DELETE_WINDOW", _cancel)

            self.app.after(0, _show)
            return _pw_q.get()   # 스레드 블로킹 대기

        # ── 실제 연결 (별도 스레드) ────────────────────────────
        def _do_test():
            log_fn = None
            if hasattr(self.app, "_log_tab"):
                log_fn = lambda m, lv="INFO": self.app.after(
                    0, lambda mm=m, ll=lv:
                        self.app._log_tab.append(mm, ll, "TG계정"))
            eng = _get_tg_engine(log_fn)
            ok  = eng.connect(acct,
                              otp_callback=_ask_otp,
                              password_callback=_ask_password)
            self.app.after(0, lambda: self._fill_form(acct))
            self.app.after(0, self._refresh_tv)
            if ok:
                self.app.after(0, lambda _p=phone: self.app._set_status(
                    f"✅ [{_p}] 연결 및 인증 완료 — 세션 저장됨"))
            else:
                self.app.after(0, lambda: messagebox.showwarning(
                    "연결 실패",
                    f"❌ [{phone}] 연결 실패\n"
                    f"로그 탭에서 원인을 확인하세요."))

        threading.Thread(target=_do_test, daemon=True).start()

    def _reset_daily(self):
        """일일 발송 카운터 초기화"""
        _get_tg_engine().reset_daily_counts()
        self._refresh_tv()
        self.app._set_status("✅ 일일 발송 카운터가 초기화되었습니다.")

    # ── 계정 상태 확인 (단일 계정) ─────────────────────────
    def _check_acct_status_ui(self):
        """선택된 계정 1개의 상태를 get_me() 로 확인 → 팝업 결과 표시"""
        if self._sel_idx < 0:
            messagebox.showwarning("선택 없음", "확인할 계정을 선택하세요.")
            return
        acct = self._accounts[self._sel_idx]
        self.app._set_status(f"🔍 [{acct.get('name','')}] 계정 상태 확인 중…")

        import threading as _thr
        def _worker():
            eng  = _get_tg_engine(lambda m, lv="INFO": None)
            info = eng._check_account_status(acct)
            self.after(0, lambda: self._show_acct_status_result([acct], [info]))

        _thr.Thread(target=_worker, daemon=True).start()

    # ── 계정 상태 확인 (전체 계정) ────────────────────────
    def _check_all_accts_ui(self):
        """전체 계정 상태를 get_me() 로 확인 → 팝업 결과 표시"""
        if not self._accounts:
            messagebox.showwarning("계정 없음", "등록된 계정이 없습니다.")
            return
        self.app._set_status(f"🔍 전체 {len(self._accounts)}개 계정 상태 확인 중…")

        import threading as _thr
        def _worker():
            eng     = _get_tg_engine(lambda m, lv="INFO": None)
            results = []
            for acct in self._accounts:
                info = eng._check_account_status(acct)
                results.append(info)
            self.after(0, lambda: self._show_acct_status_result(
                self._accounts, results))

        _thr.Thread(target=_worker, daemon=True).start()

    def _show_acct_status_result(self, accounts: list, results: list):
        """계정 상태 조회 결과를 팝업 Treeview 로 표시"""
        pop = tk.Toplevel(self.app)
        pop.title("계정 상태 확인 결과")
        pop.geometry("680x400")
        pop.configure(bg=PALETTE["bg"])

        # 헤더
        hdr = tk.Frame(pop, bg=PALETTE["primary"], pady=6)
        hdr.pack(fill=tk.X)
        ok_cnt  = sum(1 for r in results if r.get("ok"))
        bad_cnt = len(results) - ok_cnt
        tk.Label(hdr,
                 text=f"🔍 계정 상태 확인 — 정상 {ok_cnt}개 / 이상 {bad_cnt}개",
                 font=(_FF, 11, "bold"), bg=PALETTE["primary"], fg="#fff"
                 ).pack(padx=12)

        # Treeview
        cols = ("name", "phone", "status", "id", "username", "reason")
        tv_f = tk.Frame(pop, bg=PALETTE["bg"])
        tv_f.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)
        tv = ttk.Treeview(tv_f, columns=cols, show="headings",
                           style="Custom.Treeview")
        headers_def = [
            ("name",     "이름",       130),
            ("phone",    "전화번호",   130),
            ("status",   "상태",        80),
            ("id",       "계정 ID",    100),
            ("username", "@링크",      110),
            ("reason",   "이상 사유",  180),
        ]
        for col, hd, w in headers_def:
            tv.heading(col, text=hd)
            tv.column(col, width=w, anchor="center" if col != "reason" else "w")
        sb = ttk.Scrollbar(tv_f, orient=tk.VERTICAL, command=tv.yview)
        tv.configure(yscrollcommand=sb.set)
        tv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        # 태그 색상
        tv.tag_configure("ok",  background="#F0FDF4")
        tv.tag_configure("bad", background="#FEF2F2")

        for acct, info in zip(accounts, results):
            ok     = info.get("ok", False)
            status = "✅ 정상" if ok else "⚠️ 이상"
            tag    = "ok" if ok else "bad"
            tv.insert("", tk.END, tags=(tag,), values=(
                acct.get("name", ""),
                acct.get("phone", ""),
                status,
                info.get("id", "") or "",
                f"@{info['username']}" if info.get("username") else "-",
                info.get("reason", "") or "없음",
            ))

        # 닫기
        tk.Button(pop, text="닫기", command=pop.destroy,
                  font=F_BTN_S, bg=PALETTE["card2"],
                  fg=PALETTE["text2"],
                  relief=tk.FLAT, cursor="hand2",
                  padx=16, pady=5, bd=0
                  ).pack(pady=(0, 10))

        self.app._set_status(f"✅ 계정 상태 확인 완료 — 정상 {ok_cnt} / 이상 {bad_cnt}")

    # ── ④ 대화방 목록 조회 ────────────────────────────────
    def _show_dialogs(self):
        """[v1.82] 대화방 목록 팝업 — 즉시 열리고 수집되는 대로 실시간 행 추가.

        기존(v1.81): 전체 수집 완료 후 팝업 오픈 → 채팅방 많으면 오랜 대기
        개선(v1.82): 팝업 즉시 오픈 → 100개씩 수집될 때마다 즉시 행 추가
        """
        if self._sel_idx < 0:
            messagebox.showwarning("선택 없음", "계정을 선택하세요.")
            return
        acct   = self._accounts[self._sel_idx]
        acct_name = acct.get("name", "")

        # ── 1. 팝업 즉시 생성 ──────────────────────────────────────
        pop = tk.Toplevel(self.app)
        pop.title(f"대화방 목록 — {acct_name}")
        pop.geometry("720x580")
        pop.configure(bg=PALETTE["bg"])

        # 상단 헤더 (조회 중 상태)
        hdr = tk.Frame(pop, bg=PALETTE["primary"], pady=6)
        hdr.pack(fill=tk.X)
        _hdr_var = tk.StringVar(value=f"📋 {acct_name} — 조회 중…")
        tk.Label(hdr, textvariable=_hdr_var,
                 font=(_FF, 11, "bold"),
                 bg=PALETTE["primary"], fg="#fff").pack(padx=12)

        # 진행 상태 바 (수집 진행 중 표시)
        prog_bar = tk.Frame(pop, bg=PALETTE["card2"], height=28)
        prog_bar.pack(fill=tk.X)
        prog_bar.pack_propagate(False)
        _prog_var = tk.StringVar(value="⏳ 연결 중… 잠시만 기다려 주세요")
        tk.Label(prog_bar, textvariable=_prog_var,
                 font=(_FF, 8), bg=PALETTE["card2"],
                 fg=PALETTE["text2"]).pack(side=tk.LEFT, padx=10)

        # 검색 바
        sf = tk.Frame(pop, bg=PALETTE["bg"], pady=4)
        sf.pack(fill=tk.X, padx=12)
        tk.Label(sf, text="🔍", bg=PALETTE["bg"],
                 fg=PALETTE["text2"]).pack(side=tk.LEFT)
        search_var = tk.StringVar()
        search_ent = tk.Entry(sf, textvariable=search_var,
                              font=F_BODY, bg=PALETTE["card2"],
                              fg=PALETTE["text"],
                              insertbackground=PALETTE["text"],
                              relief=tk.FLAT,
                              highlightbackground=PALETTE["border"],
                              highlightthickness=1)
        search_ent.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 0))

        # ── 2. Treeview ───────────────────────────────────────────
        cols = ("type", "name", "username", "unread", "msg", "media")
        tv_f = tk.Frame(pop, bg=PALETTE["bg"])
        tv_f.pack(fill=tk.BOTH, expand=True, padx=12, pady=6)
        tv = ttk.Treeview(tv_f, columns=cols, show="headings",
                           style="Custom.Treeview")
        tv.heading("type",     text="유형")
        tv.heading("name",     text="이름")
        tv.heading("username", text="@링크")
        tv.heading("unread",   text="미읽음")
        tv.heading("msg",      text="텍스트")
        tv.heading("media",    text="이미지")
        tv.column("type",     width=70,  anchor="center")
        tv.column("name",     width=190, anchor="w")
        tv.column("username", width=140, anchor="w")
        tv.column("unread",   width=55,  anchor="center")
        tv.column("msg",      width=60,  anchor="center")
        tv.column("media",    width=60,  anchor="center")
        tv.tag_configure("ok",      foreground=PALETTE["success"])
        tv.tag_configure("warn",    foreground=PALETTE["warning"])
        tv.tag_configure("error",   foreground=PALETTE["danger"])
        tv.tag_configure("private", foreground=PALETTE["muted"])  # 링크없는 비공개
        sb = ttk.Scrollbar(tv_f, orient=tk.VERTICAL, command=tv.yview)
        tv.configure(yscrollcommand=sb.set)
        tv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        TYPE_ICON = {
            "user":       "👤",
            "group":      "👥",
            "supergroup": "🏢",
            "channel":    "📢",
        }

        # 전체 dialog 목록 (페이지로 누적)
        _all_dialogs: list[dict] = []
        # 권한 캐시
        _perm_cache: dict = {}
        # 수집 완료 플래그
        _fetch_done = [False]
        # 페이지 오프셋 (수동 더 불러오기용)
        _page_state = {
            "offset_id":   0,
            "offset_date": 0,
            "offset_peer": None,
            "has_more":    True,   # 처음엔 True 가정
            "loading":     False,
        }

        # ── 3. 행 삽입 헬퍼 ──────────────────────────────────────
        def _insert_rows(batch: list[dict]):
            """검색 필터 반영해 batch 행 삽입 (전체 재그리기 없이 append)"""
            flt = search_var.get().strip().lower()
            for d in batch:
                name  = d.get("name", "")
                if flt and flt not in name.lower() and \
                   flt not in (d.get("username") or "").lower():
                    continue
                icon  = TYPE_ICON.get(d.get("type", ""), "💬")
                has_link = bool(d.get("username"))
                uname = f"@{d['username']}" if has_link else "🔒 비공개"
                key   = d.get("username") or str(d.get("id", ""))
                perm  = _perm_cache.get(key)
                if perm is None:
                    msg_icon, media_icon = "—", "—"
                    row_tag = "private" if not has_link else ""
                else:
                    msg_icon   = "✅" if perm.get("send_messages") else "❌"
                    media_icon = "✅" if perm.get("send_media")    else "❌"
                    row_tag    = "ok" if perm.get("ok") else "error"
                tv.insert("", tk.END,
                          values=(f"{icon} {d.get('type','')}",
                                  name, uname,
                                  d.get("unread", 0) or "",
                                  msg_icon, media_icon),
                          tags=(row_tag,) if row_tag else ())

        def _repopulate(*_):
            """검색어 변경 시 전체 재그리기"""
            tv.delete(*tv.get_children())
            _insert_rows(_all_dialogs)

        search_var.trace_add("write", _repopulate)

        # ── 4. 첫 페이지 자동 로딩 + 수동 페이지 로딩 ─────────
        def _load_page(is_first=False):
            """get_dialogs_page 호출 → 결과를 UI에 반영"""
            if _page_state["loading"]:
                return
            if not _page_state["has_more"] and not is_first:
                _prog_var.set("✅ 모든 채팅방 불러옴 — 더 이상 없음")
                return
            _page_state["loading"] = True
            btn_more.config(state=tk.DISABLED,
                            text="⏳ 불러오는 중…")
            _prog_var.set("⏳ 불러오는 중…")
            import threading as _thr
            def _worker():
                e = _get_tg_engine(lambda m, lv="INFO": None)
                res = e.get_dialogs_page(
                    acct,
                    offset_id=_page_state["offset_id"],
                    offset_date=_page_state["offset_date"],
                    offset_peer=_page_state["offset_peer"],
                    limit=100,
                )
                def _ui():
                    if not pop.winfo_exists():
                        return
                    batch = res["dialogs"]
                    _all_dialogs.extend(batch)
                    _insert_rows(batch)
                    # 페이지 오프셋 갱신
                    _page_state["offset_id"]   = res["next_offset_id"]
                    _page_state["offset_date"] = res["next_offset_date"]
                    _page_state["offset_peer"] = res["next_offset_peer"]
                    _page_state["has_more"]    = res["has_more"]
                    _page_state["loading"]     = False
                    n = len(_all_dialogs)
                    # 링크 카운트 업데이트
                    link_cnt = len([d for d in _all_dialogs if d.get("username")])
                    private_cnt = n - link_cnt
                    _link_count_var.set(
                        f"🔗 공개링크 {link_cnt}개  🔒 비공개 {private_cnt}개")
                    if res["has_more"]:
                        _hdr_var.set(
                            f"📋 {acct_name} — {n}개 로드됨 (더 있음)")
                        _prog_var.set(
                            f"✅ {n}개 표시 중 — 더 있을 수 있음")
                        btn_more.config(state=tk.NORMAL,
                                        text=f"➕ 100개 더 불러오기")
                        _fetch_done[0] = False
                    else:
                        _hdr_var.set(
                            f"📋 {acct_name} — 가입 채팅방 총 {n}개")
                        _prog_var.set(
                            f"✅ 전체 조회 완료 — 총 {n}개")
                        prog_bar.configure(bg="#D1FAE5")
                        btn_more.config(state=tk.DISABLED,
                                        text="✅ 전부 불러옴")
                        _fetch_done[0] = True
                        chk_btn_all.config(state=tk.NORMAL)
                        self.app._set_status(
                            f"✅ 대화방 목록 전체 조회 완료 ({n}개) — {acct_name}")
                pop.after(0, _ui)
            _thr.Thread(target=_worker, daemon=True).start()

        # ── 5. 첫 페이지 자동 시작 ───────────────────────────────
        self.app._set_status(f"📋 {acct_name} 대화방 목록 첫 100개 로딩…")

        # ── 6. 전송 권한 점검 버튼 바 ────────────────────────────
        chk_bar = tk.Frame(pop, bg=PALETTE["card"],
                           highlightbackground=PALETTE["border"],
                           highlightthickness=1)
        chk_bar.pack(fill=tk.X, padx=12, pady=(0, 4))
        chk_inner = tk.Frame(chk_bar, bg=PALETTE["card"])
        chk_inner.pack(fill=tk.X, padx=10, pady=6)

        _chk_status_var = tk.StringVar(
            value="💬 텍스트 · 📎 이미지 전송 가능 여부를 점검합니다")
        tk.Label(chk_inner, textvariable=_chk_status_var,
                 font=(_FF, 8), bg=PALETTE["card"],
                 fg=PALETTE["muted"]).pack(side=tk.LEFT, padx=(0, 10))

        def _run_check_selected():
            sel = tv.selection()
            if not sel:
                messagebox.showinfo("선택 없음",
                    "점검할 채팅방을 선택하세요.\n(Ctrl+클릭으로 다중 선택)")
                return
            targets = []
            for item in sel:
                vals  = tv.item(item, "values")
                uname = vals[2] if len(vals) > 2 else ""
                name  = vals[1] if len(vals) > 1 else ""
                peer  = uname.lstrip("@") if uname != "-" else ""
                if not peer:
                    for d in _all_dialogs:
                        if d.get("name") == name:
                            peer = str(d.get("id", ""))
                            break
                targets.append((name, peer,
                                uname.lstrip("@") if uname != "-" else None))
            _do_check(targets)

        def _run_check_all():
            if not _fetch_done[0]:
                messagebox.showinfo("조회 중",
                    "대화방 목록 수집이 진행 중입니다.\n잠시 후 다시 시도해 주세요.")
                return
            targets = []
            for d in _all_dialogs:
                peer = d.get("username") or str(d.get("id", ""))
                targets.append((d.get("name", ""), peer, d.get("username")))
            _do_check(targets)

        def _do_check(targets):
            total = len(targets)
            _chk_status_var.set(f"🔍 점검 중… 0 / {total}")
            chk_btn_sel.config(state=tk.DISABLED)
            chk_btn_all.config(state=tk.DISABLED)
            import threading as _thr
            def _worker():
                e = _get_tg_engine(lambda m, lv="INFO": None)
                for idx, (name, peer, uname_key) in enumerate(targets, 1):
                    if not peer:
                        continue
                    perm = e.check_peer_permission(acct, peer)
                    key  = uname_key or peer
                    _perm_cache[key] = perm
                    ok_cnt  = sum(1 for v in _perm_cache.values() if v.get("ok"))
                    bad_cnt = sum(1 for v in _perm_cache.values() if not v.get("ok"))
                    pop.after(0, lambda i=idx, o=ok_cnt, b=bad_cnt:
                        _chk_status_var.set(
                            f"🔍 점검 중… {i} / {total}  "
                            f"✅ {o}개 가능  ❌ {b}개 불가"))
                    pop.after(0, _repopulate)
                ok_cnt  = sum(1 for v in _perm_cache.values() if v.get("ok"))
                bad_cnt = sum(1 for v in _perm_cache.values() if not v.get("ok"))
                med_bad = sum(1 for v in _perm_cache.values()
                              if v.get("send_messages") and not v.get("send_media"))
                pop.after(0, lambda: (
                    _chk_status_var.set(
                        f"✅ 점검 완료 — 전송가능 {ok_cnt}개  "
                        f"❌ 불가 {bad_cnt}개  "
                        f"📎 이미지만불가 {med_bad}개"),
                    chk_btn_sel.config(state=tk.NORMAL),
                    chk_btn_all.config(state=tk.NORMAL),
                ))
            _thr.Thread(target=_worker, daemon=True).start()

        chk_btn_sel = tk.Button(chk_inner,
                  text="🔍 선택 항목 점검",
                  command=_run_check_selected,
                  font=F_BTN_S,
                  bg=PALETTE["warning_text"], fg="#fff",
                  activebackground=_lighten(PALETTE["warning_text"], -0.1),
                  relief=tk.FLAT, cursor="hand2",
                  padx=10, pady=3, bd=0)
        chk_btn_sel.pack(side=tk.RIGHT, padx=(4, 0))

        chk_btn_all = tk.Button(chk_inner,
                  text="🔍 전체 점검",
                  command=_run_check_all,
                  font=F_BTN_S,
                  bg="#7C3AED", fg="#fff",
                  activebackground="#6D28D9",
                  relief=tk.FLAT, cursor="hand2",
                  padx=10, pady=3, bd=0,
                  state=tk.DISABLED)   # 조회 완료 후 활성화
        chk_btn_all.pack(side=tk.RIGHT, padx=(0, 4))

        # ── 7. t.me 링크 버튼 바 ─────────────────────────────────
        link_bar = tk.Frame(pop, bg=PALETTE["card"],
                            highlightbackground=PALETTE["border"],
                            highlightthickness=1)
        link_bar.pack(fill=tk.X, padx=12, pady=(0, 6))
        link_inner = tk.Frame(link_bar, bg=PALETTE["card"])
        link_inner.pack(fill=tk.X, padx=10, pady=6)

        _link_count_var = tk.StringVar(value="🔗 t.me 링크 수집 중…")
        tk.Label(link_inner, textvariable=_link_count_var,
                 font=(_FF, 8, "bold"), bg=PALETTE["card"],
                 fg=PALETTE["primary"]).pack(side=tk.LEFT, padx=(0, 10))

        def _copy_links_selected():
            sel = tv.selection()
            if not sel:
                messagebox.showinfo("선택 없음",
                    "복사할 채팅방을 선택하세요.\n(Ctrl+클릭으로 다중 선택 가능)")
                return
            links = []
            for item in sel:
                vals = tv.item(item, "values")
                uname = vals[2] if len(vals) > 2 else ""
                if uname and uname != "-":
                    links.append(f"https://t.me/{uname.lstrip('@')}")
            if links:
                pop.clipboard_clear()
                pop.clipboard_append("\n".join(links))
                _link_count_var.set(f"✅ {len(links)}개 복사됨 — Ctrl+V로 붙여넣기")
            else:
                messagebox.showinfo("링크 없음",
                    "선택된 채팅방에 @링크가 없습니다.\n(private 그룹은 링크 없음)")

        def _copy_links_all():
            links = [f"https://t.me/{d['username']}"
                     for d in _all_dialogs if d.get("username")]
            if links:
                pop.clipboard_clear()
                pop.clipboard_append("\n".join(links))
                _link_count_var.set(
                    f"✅ 전체 {len(links)}개 복사됨 — Ctrl+V로 붙여넣기")
            else:
                messagebox.showinfo("링크 없음",
                    "공개 링크(@username)가 있는 채팅방이 없습니다.")

        tk.Button(link_inner,
                  text="📋 선택 링크 복사",
                  command=_copy_links_selected,
                  font=F_BTN_S, bg=PALETTE["primary"], fg="#fff",
                  activebackground=PALETTE["primary2"],
                  relief=tk.FLAT, cursor="hand2",
                  padx=10, pady=3, bd=0
                  ).pack(side=tk.LEFT, padx=(0, 6))

        tk.Button(link_inner,
                  text="🌐 전체 링크 복사",
                  command=_copy_links_all,
                  font=F_BTN_S, bg=PALETTE["success"], fg="#fff",
                  activebackground=_lighten(PALETTE["success"], -0.1),
                  relief=tk.FLAT, cursor="hand2",
                  padx=10, pady=3, bd=0
                  ).pack(side=tk.LEFT)

        # ── 8. 하단 버튼 바 (더 불러오기 + 닫기) ──────────────
        btn_bottom = tk.Frame(pop, bg=PALETTE["bg"])
        btn_bottom.pack(fill=tk.X, padx=12, pady=(0, 10))

        btn_more = tk.Button(btn_bottom,
                  text="➕ 100개 더 불러오기",
                  command=_load_page,
                  font=F_BTN_S,
                  bg=PALETTE["accent"] if "accent" in PALETTE else "#0EA5E9",
                  fg="#fff",
                  activebackground="#0284C7",
                  relief=tk.FLAT, cursor="hand2",
                  padx=12, pady=5, bd=0,
                  state=tk.DISABLED)  # 첫 로딩 끝나면 활성화
        btn_more.pack(side=tk.LEFT)

        tk.Button(btn_bottom, text="닫기", command=pop.destroy,
                  font=F_BTN_S, bg=PALETTE["card2"],
                  fg=PALETTE["text2"],
                  relief=tk.FLAT, cursor="hand2",
                  padx=16, pady=5, bd=0
                  ).pack(side=tk.RIGHT)

        # 첫 페이지 자동 로딩 시작
        pop.after(100, lambda: _load_page(is_first=True))

    # ── 상태 폴링 (5초마다 Treeview 갱신) ─────────────────
    def _start_status_poll(self):
        self._status_poll_id = self.after(5000, self._poll_status)

    def _poll_status(self):
        # [WARN-02 fix] 위젯이 파괴된 뒤에도 재예약되지 않도록 winfo_exists() 확인
        try:
            if not self.winfo_exists():
                return
            self._refresh_tv()
            if self._sel_idx >= 0 and self._sel_idx < len(self._accounts):
                self._fill_form(self._accounts[self._sel_idx])
        except Exception:
            pass
        # 위젯이 여전히 살아있을 때만 재예약
        try:
            if self.winfo_exists():
                self._status_poll_id = self.after(5000, self._poll_status)
        except Exception:
            pass


# ── App에 TelegramAccountsTab 연결 (monkey-patch) ────────────
def _app_build_telegram_accounts_tab(self, frame: tk.Frame):
    tab = TelegramAccountsTab(frame, self)
    tab.pack(fill=tk.BOTH, expand=True)
    self._tg_accounts_tab = tab
    # 엔진에 로그 함수 연결
    def _tg_log(msg, lv="INFO"):
        if hasattr(self, "_log_tab"):
            self.after(0, lambda m=msg, l=lv:
                       self._log_tab.append(m, l, "TG엔진"))
    _get_tg_engine(_tg_log).load_accounts(
        load_json(TG_ACCOUNTS_PATH, []))

App._build_telegram_accounts_tab = _app_build_telegram_accounts_tab

# ============================================================
# Block 5-A : LogTab — 실시간 로그
# ============================================================

class LogTab(tk.Frame):
    """
    실시간 로그 표시 + 레벨/소스 필터 + CSV 내보내기
    [v1.78] 긴급 조치 패널 추가 (Frozen/FloodWait 감지 알림 + 즉시 중단)
    """
    def __init__(self, master, app: "App"):
        super().__init__(master, bg=PALETTE["bg"])
        self.app      = app
        self._logs:   list[dict] = []   # 전체 로그 버퍼
        self._auto_scroll = tk.BooleanVar(value=True)
        # v1.78: 긴급 알림 카운터
        self._alert_frozen:  int = 0
        self._alert_flood:   int = 0
        self._alert_dead:    int = 0
        self._build()

    def _build(self):
        # ── 탭 헤더 ──────────────────────────────────────────
        hdr = tk.Frame(self, bg=PALETTE["bg"])
        hdr.pack(fill=tk.X, pady=(0, 8))

        title_f = tk.Frame(hdr, bg=PALETTE["bg"])
        title_f.pack(side=tk.LEFT)
        tk.Label(title_f, text="🗒",
                 font=("Segoe UI Emoji", 15),
                 bg=PALETTE["bg"], fg=PALETTE["primary"]
                 ).pack(side=tk.LEFT)
        tk.Label(title_f, text="  실시간 로그",
                 font=F_TITLE, bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)

        # 우측 버튼
        for txt, cmd, bg in [
            ("🗑  전체 삭제", self._clear,      "#FEF2F2"),
            ("📥  CSV 저장",  self._export_csv,  PALETTE["card"]),
        ]:
            b = tk.Button(hdr, text=txt, command=cmd,
                      bg=bg, fg=PALETTE["text2"],
                      relief=tk.FLAT,
                      font=F_BTN_S,
                      highlightbackground=PALETTE["border"],
                      highlightthickness=1,
                      activebackground=PALETTE["hover"],
                      cursor="hand2", padx=10, pady=4)
            b.pack(side=tk.RIGHT, padx=(4, 0))

        # 구분선
        tk.Frame(self, bg=PALETTE["border"], height=1
                 ).pack(fill=tk.X, pady=(0, 4))

        # ── v1.78: 긴급 조치 패널 ────────────────────────────
        self._emergency_panel = tk.Frame(
            self, bg="#FEF2F2",
            highlightbackground="#FCA5A5",
            highlightthickness=1)
        self._emergency_panel.pack(fill=tk.X, pady=(0, 4))

        emg_inner = tk.Frame(self._emergency_panel, bg="#FEF2F2")
        emg_inner.pack(fill=tk.X, padx=10, pady=6)

        # 긴급 상태 레이블
        left_emg = tk.Frame(emg_inner, bg="#FEF2F2")
        left_emg.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(left_emg, text="🚨 긴급 조치",
                 font=(_FF, 9, "bold"), bg="#FEF2F2",
                 fg="#B91C1C").pack(side=tk.LEFT, padx=(0, 10))

        self._emg_frozen_var = tk.StringVar(value="🚨 FROZEN: 0계정")
        self._emg_flood_var  = tk.StringVar(value="🛑 FloodWait중단: 0계정")
        self._emg_dead_var   = tk.StringVar(value="🗑 없는채팅방: 0건")

        tk.Label(left_emg, textvariable=self._emg_frozen_var,
                 font=(_FF, 8, "bold"), bg="#FEF2F2",
                 fg="#DC2626").pack(side=tk.LEFT, padx=(0, 12))
        tk.Label(left_emg, textvariable=self._emg_flood_var,
                 font=(_FF, 8, "bold"), bg="#FEF2F2",
                 fg="#D97706").pack(side=tk.LEFT, padx=(0, 12))
        tk.Label(left_emg, textvariable=self._emg_dead_var,
                 font=(_FF, 8, "bold"), bg="#FEF2F2",
                 fg="#6B7280").pack(side=tk.LEFT, padx=(0, 12))

        # 우측 긴급 버튼들
        right_emg = tk.Frame(emg_inner, bg="#FEF2F2")
        right_emg.pack(side=tk.RIGHT)

        tk.Button(right_emg,
                  text="⏹ 전체 즉시 중단",
                  command=self._emergency_stop_all,
                  font=(_FF, 8, "bold"),
                  bg="#DC2626", fg="#fff",
                  activebackground="#B91C1C",
                  relief=tk.FLAT, cursor="hand2",
                  padx=10, pady=4, bd=0
                  ).pack(side=tk.LEFT, padx=(0, 4))

        tk.Button(right_emg,
                  text="🔍 ERROR만 보기",
                  command=lambda: (
                      self._level_var.set("ERROR"),
                      self._apply_filter()),
                  font=(_FF, 8, "bold"),
                  bg="#B91C1C", fg="#fff",
                  activebackground="#991B1B",
                  relief=tk.FLAT, cursor="hand2",
                  padx=10, pady=4, bd=0
                  ).pack(side=tk.LEFT, padx=(0, 4))

        tk.Button(right_emg,
                  text="🗑 없는채팅방 목록",
                  command=self._show_dead_links,
                  font=(_FF, 8, "bold"),
                  bg="#6B7280", fg="#fff",
                  activebackground="#4B5563",
                  relief=tk.FLAT, cursor="hand2",
                  padx=10, pady=4, bd=0
                  ).pack(side=tk.LEFT)

        # ── 필터 바 ──────────────────────────────────────────
        flt_wrap = tk.Frame(self, bg=PALETTE["card"],
                            highlightbackground=PALETTE["border"],
                            highlightthickness=1)
        flt_wrap.pack(fill=tk.X, pady=(0, 6))
        flt = tk.Frame(flt_wrap, bg=PALETTE["card"])
        flt.pack(fill=tk.X, padx=12, pady=7)

        tk.Label(flt, text="레벨",
                 font=(_FF, 8, "bold"),
                 bg=PALETTE["card"], fg=PALETTE["muted"]
                 ).pack(side=tk.LEFT, padx=(0, 6))

        self._level_var = tk.StringVar(value="ALL")
        _lv_defs = [
            ("ALL",     PALETTE["text2"],   PALETTE["bg"]),
            ("INFO",    PALETTE["text2"],   PALETTE["bg"]),
            ("SUCCESS", "#065F46",          "#ECFDF5"),
            ("WARN",    "#92400E",          "#FFFBEB"),
            ("ERROR",   "#B91C1C",          "#FEF2F2"),
        ]
        for lv, fg, selbg in _lv_defs:
            tk.Radiobutton(
                flt, text=lv,
                variable=self._level_var, value=lv,
                bg=PALETTE["card"], fg=fg,
                selectcolor=selbg,
                activebackground=PALETTE["card"],
                font=(_FF, 8, "bold"),
                command=self._apply_filter
            ).pack(side=tk.LEFT, padx=(0, 6))

        # 구분선
        tk.Frame(flt, bg=PALETTE["border2"], width=1, height=20
                 ).pack(side=tk.LEFT, padx=(8, 8), fill=tk.Y)

        # 소스 필터
        tk.Label(flt, text="소스",
                 font=(_FF, 8, "bold"),
                 bg=PALETTE["card"], fg=PALETTE["muted"]
                 ).pack(side=tk.LEFT, padx=(0, 6))

        self._src_var = tk.StringVar(value="ALL")
        self._src_cb  = ttk.Combobox(
            flt, textvariable=self._src_var,
            values=["ALL"], width=14,
            state="readonly",
            font=F_SMALL)
        self._src_cb.pack(side=tk.LEFT)
        self._src_cb.bind("<<ComboboxSelected>>",
                          lambda e: self._apply_filter())

        # 구분선
        tk.Frame(flt, bg=PALETTE["border2"], width=1, height=20
                 ).pack(side=tk.LEFT, padx=(8, 8), fill=tk.Y)

        # 검색창
        tk.Label(flt, text="🔍",
                 font=("Segoe UI Emoji", 10),
                 bg=PALETTE["card"], fg=PALETTE["muted"]
                 ).pack(side=tk.LEFT, padx=(0, 4))
        self._search_var = tk.StringVar()
        self._search_var.trace_add(
            "write", lambda *a: self._apply_filter())
        tk.Entry(flt, textvariable=self._search_var,
                 bg=PALETTE["card2"], fg=PALETTE["text"],
                 insertbackground=PALETTE["primary"],
                 relief=tk.FLAT,
                 highlightbackground=PALETTE["border"],
                 highlightthickness=1,
                 font=F_SMALL, width=20
                 ).pack(side=tk.LEFT, ipady=2)

        # 구분선 + 자동 스크롤 체크박스
        tk.Frame(flt, bg=PALETTE["border2"], width=1, height=20
                 ).pack(side=tk.LEFT, padx=(10, 8), fill=tk.Y)
        tk.Checkbutton(flt, text="📌 자동 스크롤",
                       variable=self._auto_scroll,
                       bg=PALETTE["card"], fg=PALETTE["text2"],
                       selectcolor=PALETTE["active"],
                       activebackground=PALETTE["card"],
                       font=(_FF, 8),
                       cursor="hand2"
                       ).pack(side=tk.LEFT)

        # ── 로그 Treeview ────────────────────────────────────
        tv_frame = tk.Frame(self,
                            bg=PALETTE["card"],
                            highlightbackground=PALETTE["border"],
                            highlightthickness=1)
        tv_frame.pack(fill=tk.BOTH, expand=True)

        cols = ("time", "level", "source", "message")
        self._tv = ttk.Treeview(
            tv_frame, columns=cols,
            show="headings", height=18)

        headers = [
            ("time",    "시각",    80),
            ("level",   "레벨",    70),
            ("source",  "소스",   130),
            ("message", "내용",   700),
        ]
        for col, hd, w in headers:
            self._tv.heading(col, text=hd)
            self._tv.column(col, width=w,
                            anchor=tk.W
                            if col == "message"
                            else tk.CENTER,
                            stretch=col == "message")

        # 레벨별 태그 색상
        self._tv.tag_configure(
            "SUCCESS", foreground=PALETTE["success_text"])
        self._tv.tag_configure(
            "WARN",    foreground=PALETTE["warning_text"])
        self._tv.tag_configure(
            "ERROR",   foreground=PALETTE["danger"])
        self._tv.tag_configure(
            "INFO",    foreground=PALETTE["text"])

        style = ttk.Style()
        style.configure("Treeview",
                        background=PALETTE["card"],
                        foreground=PALETTE["text"],
                        rowheight=24,
                        fieldbackground=PALETTE["card"],
                        borderwidth=0)
        style.configure("Treeview.Heading",
                        background=PALETTE["sidebar"],
                        foreground=PALETTE["sidebar_text"],
                        relief="flat")

        tv_sb = ttk.Scrollbar(tv_frame,
                              orient=tk.VERTICAL,
                              command=self._tv.yview)
        self._tv.configure(yscrollcommand=tv_sb.set)
        tv_sb.pack(side=tk.RIGHT, fill=tk.Y)
        self._tv.pack(side=tk.LEFT,
                      fill=tk.BOTH, expand=True)

        # ── 하단 요약 바 ─────────────────────────────────────
        summ = tk.Frame(self, bg=PALETTE["card"],
                        highlightbackground=PALETTE["border"],
                        highlightthickness=1,
                        height=28)
        summ.pack(fill=tk.X, side=tk.BOTTOM, pady=(4, 0))
        summ.pack_propagate(False)

        tk.Label(summ, text="📋",
                 font=("Segoe UI Emoji", 9),
                 bg=PALETTE["card"], fg=PALETTE["muted"]
                 ).pack(side=tk.LEFT, padx=(10, 4), fill=tk.Y)
        self._summ_var = tk.StringVar(value="로그 없음")
        tk.Label(summ, textvariable=self._summ_var,
                 font=F_SMALL,
                 bg=PALETTE["card"],
                 fg=PALETTE["text2"],
                 anchor=tk.W
                 ).pack(side=tk.LEFT, fill=tk.Y)

    # ── 로그 추가 (외부에서 호출) ────────────────────────────
    def append(self, message: str,
               level: str = "INFO",
               source: str = "시스템"):
        entry = {
            "time":    now_str(),
            "level":   level.upper(),
            "source":  source,
            "message": message,
        }
        self._logs.append(entry)
        self._update_source_list()

        # 필터 통과 시만 Treeview 에 추가
        if self._match_filter(entry):
            self._insert_row(entry)
            # 자동 스크롤 (체크박스 ON 시에만)
            if self._auto_scroll.get():
                children = self._tv.get_children()
                if children:
                    self._tv.see(children[-1])

        self._update_summary()
        # v1.78: 긴급 조치 패널 업데이트
        self._update_emergency(entry)

    # ── v1.78: 긴급 조치 패널 업데이트 ────────────────────────
    def _update_emergency(self, entry: dict):
        """로그 메시지에서 frozen/FloodWait/dead 패턴 감지 → 패널 갱신"""
        msg = entry.get("message", "").lower()
        lv  = entry.get("level", "")

        if lv == "ERROR":
            if "frozen" in msg or "🚨" in entry.get("message", ""):
                self._alert_frozen += 1
                self._emg_frozen_var.set(f"🚨 FROZEN: {self._alert_frozen}계정")
                # 패널 배경 점등
                try:
                    self._emergency_panel.configure(bg="#FEE2E2",
                        highlightbackground="#EF4444")
                except Exception:
                    pass

            if "floodwait" in msg and ("임계값" in entry.get("message", "")
                                        or "당일 중단" in entry.get("message", "")):
                self._alert_flood += 1
                self._emg_flood_var.set(f"🛑 FloodWait중단: {self._alert_flood}계정")

        if lv in ("WARN", "ERROR"):
            if "없는 채팅방" in entry.get("message", "") or "dead" in msg:
                self._alert_dead += 1
                self._emg_dead_var.set(f"🗑 없는채팅방: {self._alert_dead}건")

    # ── v1.78: 긴급 중단 ────────────────────────────────────────
    def _emergency_stop_all(self):
        """모든 작업 즉시 중단"""
        try:
            if hasattr(self.app, "_jobs_tab"):
                self.app._jobs_tab._jobs_stop_all()
            self.append("🚨 긴급 전체 중단 실행 — 모든 작업 중지됨", "ERROR", "긴급조치")
        except Exception as e:
            self.append(f"⚠️ 긴급 중단 실패: {e}", "ERROR", "긴급조치")

    # ── v1.78: 없는 채팅방 목록 표시 ───────────────────────────
    def _show_dead_links(self):
        """없는 채팅방(dead_links) 목록을 팝업으로 표시"""
        eng = _get_tg_engine()
        dead = sorted(eng._dead_links)
        pop = tk.Toplevel(self)
        pop.title(f"🗑 없는 채팅방 목록 ({len(dead)}건)")
        pop.geometry("500x400")
        pop.configure(bg=PALETTE["bg"])
        pop.grab_set()

        tk.Label(pop,
                 text=f"없는 채팅방 블랙리스트  —  총 {len(dead)}건",
                 font=F_TITLE, bg=PALETTE["bg"],
                 fg=PALETTE["danger"]).pack(pady=(12, 4))
        tk.Label(pop,
                 text="이 링크들은 이번 세션에서 자동으로 스킵됩니다.",
                 font=F_SMALL, bg=PALETTE["bg"],
                 fg=PALETTE["muted"]).pack()

        txt_f = tk.Frame(pop, bg=PALETTE["card"],
                         highlightbackground=PALETTE["border"],
                         highlightthickness=1)
        txt_f.pack(fill=tk.BOTH, expand=True, padx=16, pady=8)
        sb = ttk.Scrollbar(txt_f, orient=tk.VERTICAL)
        txt = tk.Text(txt_f, font=F_MONO, wrap=tk.WORD,
                      bg=PALETTE["card2"], fg=PALETTE["danger"],
                      yscrollcommand=sb.set,
                      relief=tk.FLAT)
        sb.configure(command=txt.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        txt.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        if dead:
            txt.insert(tk.END, "\n".join(dead))
        else:
            txt.insert(tk.END, "(없는 채팅방이 감지되지 않았습니다)")

        btn_row = tk.Frame(pop, bg=PALETTE["bg"])
        btn_row.pack(fill=tk.X, padx=16, pady=(0, 12))

        def _copy():
            pop.clipboard_clear()
            pop.clipboard_append("\n".join(dead))
        def _clear_dead():
            eng._dead_links.clear()
            self._alert_dead = 0
            self._emg_dead_var.set("🗑 없는채팅방: 0건")
            txt.delete("1.0", tk.END)
            txt.insert(tk.END, "(초기화됨)")

        tk.Button(btn_row, text="📋 복사",
                  command=_copy,
                  font=F_BTN_S, bg=PALETTE["primary"], fg="#fff",
                  relief=tk.FLAT, cursor="hand2",
                  padx=10, pady=4, bd=0).pack(side=tk.LEFT, padx=(0, 8))
        tk.Button(btn_row, text="🗑 목록 초기화",
                  command=_clear_dead,
                  font=F_BTN_S, bg="#EF4444", fg="#fff",
                  relief=tk.FLAT, cursor="hand2",
                  padx=10, pady=4, bd=0).pack(side=tk.LEFT, padx=(0, 8))
        tk.Button(btn_row, text="닫기",
                  command=pop.destroy,
                  font=F_BTN_S, bg=PALETTE["card"], fg=PALETTE["text2"],
                  relief=tk.FLAT, cursor="hand2",
                  padx=10, pady=4, bd=0).pack(side=tk.LEFT)

    def _insert_row(self, entry: dict):
        tag = entry.get("level", "INFO")
        self._tv.insert("", tk.END,
            values=(entry["time"],
                    entry["level"],
                    entry["source"],
                    entry["message"]),
            tags=(tag,))

    # ── 소스 목록 갱신 ───────────────────────────────────────
    def _update_source_list(self):
        sources = ["ALL"] + sorted(set(
            e["source"] for e in self._logs))
        self._src_cb["values"] = sources

    # ── 필터 매칭 ────────────────────────────────────────────
    def _match_filter(self, entry: dict) -> bool:
        lv  = self._level_var.get()
        src = self._src_var.get()
        kw  = self._search_var.get().strip().lower()

        if lv  != "ALL" and entry["level"]  != lv:
            return False
        if src != "ALL" and entry["source"] != src:
            return False
        if kw and kw not in entry["message"].lower():
            return False
        return True

    # ── 필터 적용 (전체 재렌더) ──────────────────────────────
    def _apply_filter(self):
        self._tv.delete(*self._tv.get_children())
        for entry in self._logs:
            if self._match_filter(entry):
                self._insert_row(entry)
        children = self._tv.get_children()
        if children:
            self._tv.see(children[-1])
        self._update_summary()

    # ── 요약 바 갱신 ─────────────────────────────────────────
    def _update_summary(self):
        total   = len(self._logs)
        success = sum(1 for e in self._logs
                      if e["level"] == "SUCCESS")
        warn    = sum(1 for e in self._logs
                      if e["level"] == "WARN")
        error   = sum(1 for e in self._logs
                      if e["level"] == "ERROR")
        self._summ_var.set(
            f"전체 {total}건  |  "
            f"✅ 성공 {success}  "
            f"⚠️ 경고 {warn}  "
            f"❌ 오류 {error}")

    # ── 전체 삭제 ────────────────────────────────────────────
    def _clear(self):
        if not messagebox.askyesno("삭제 확인",
                "모든 로그를 삭제할까요?"):
            return
        self._logs.clear()
        self._tv.delete(*self._tv.get_children())
        self._update_summary()
        # v1.79: 긴급 카운터 및 패널 리셋
        self._alert_frozen = 0
        self._alert_flood  = 0
        self._alert_dead   = 0
        self._emg_frozen_var.set("🚨 FROZEN: 0계정")
        self._emg_flood_var.set("🛑 FloodWait중단: 0계정")
        self._emg_dead_var.set("🗑 없는채팅방: 0건")
        try:
            self._emergency_panel.configure(bg="#FEF2F2",
                highlightbackground="#FCA5A5")
        except Exception:
            pass

    # ── CSV 내보내기 ─────────────────────────────────────────
    def _export_csv(self):
        if not self._logs:
            self._summ_var.set("⚠️ 내보낼 로그가 없습니다.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            initialfile=f"log_{datetime.now():%Y%m%d_%H%M%S}")
        if not path:
            return
        try:
            import csv as _csv2
            with open(path, "w", newline="",
                      encoding="utf-8-sig") as f:
                w = _csv2.DictWriter(
                    f, fieldnames=[
                        "time","level",
                        "source","message"])
                w.writeheader()
                w.writerows(self._logs)
            self.app._set_status(
                f"✅ 로그 저장: {path}")
        except Exception as e:
            messagebox.showerror("저장 실패", str(e))


# ── App 에 LogTab 연결 ───────────────────────────────────────
def _app_build_log_tab(self, frame: tk.Frame):
    tab = LogTab(frame, self)
    tab.pack(fill=tk.BOTH, expand=True)
    self._log_tab = tab
    # v1.78: 엔진에 alert_fn 주입 — 긴급 조치 패널과 TelethonEngine 연동
    def _engine_alert(phone: str, kind: str, detail: str = ""):
        """TelethonEngine → LogTab 긴급 패널 콜백"""
        if kind == "frozen":
            tab._alert_frozen += 1
            try:
                tab._emg_frozen_var.set(f"🚨 FROZEN: {tab._alert_frozen}계정")
                tab._emergency_panel.configure(bg="#FEE2E2",
                    highlightbackground="#EF4444")
            except Exception:
                pass
        elif kind == "flood_stopped":
            tab._alert_flood += 1
            try:
                tab._emg_flood_var.set(f"🛑 FloodWait중단: {tab._alert_flood}계정")
            except Exception:
                pass
    _get_tg_engine(alert_fn=_engine_alert)

App._build_log_tab = _app_build_log_tab
# ============================================================
# Block 5-B : StatsTab — 통계
# ============================================================

class StatsTab(tk.Frame):
    def __init__(self, master, app: "App"):
        super().__init__(master, bg=PALETTE["bg"])
        self.app     = app
        self._records: list[dict] = []
        self._build()
        self._load_stats()

    def _build(self):
        # ── 탭 헤더 ──────────────────────────────────────────
        hdr = tk.Frame(self, bg=PALETTE["bg"])
        hdr.pack(fill=tk.X, pady=(0, 10))

        title_f = tk.Frame(hdr, bg=PALETTE["bg"])
        title_f.pack(side=tk.LEFT)
        tk.Label(title_f, text="📊",
                 font=("Segoe UI Emoji", 15),
                 bg=PALETTE["bg"], fg=PALETTE["primary"]
                 ).pack(side=tk.LEFT)
        tk.Label(title_f, text="  통계",
                 font=F_TITLE, bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)

        for txt, cmd, bg in [
            ("🔄  새로고침", self.refresh,      PALETTE["card"]),
            ("📥  CSV 저장", self._export_csv,  PALETTE["card"]),
            ("🗑  초기화",   self._reset,       "#FEF2F2"),
        ]:
            b = tk.Button(hdr, text=txt, command=cmd,
                      bg=bg, fg=PALETTE["text2"],
                      relief=tk.FLAT, font=F_BTN_S,
                      highlightbackground=PALETTE["border"],
                      highlightthickness=1,
                      activebackground=PALETTE["hover"],
                      cursor="hand2", padx=10, pady=4)
            b.pack(side=tk.RIGHT, padx=(4, 0))

        # 구분선
        tk.Frame(self, bg=PALETTE["border"], height=1
                 ).pack(fill=tk.X, pady=(0, 10))

        # ── 요약 뱃지 — 2×2 그리드 (창 축소 시 넘침 방지) ────
        self._badge_frame = tk.Frame(self, bg=PALETTE["bg"])
        self._badge_frame.pack(fill=tk.X, pady=(0, 10))
        # columnconfigure로 4칸 균등 분배
        for c in range(4):
            self._badge_frame.columnconfigure(c, weight=1)
        self._total_lbl  = self._badge("전체 실행", "0",
                                        PALETTE["primary"],  row=0, col=0)
        self._succ_lbl   = self._badge("성공",      "0",
                                        PALETTE["success"],  row=0, col=1)
        self._fail_lbl   = self._badge("실패",      "0",
                                        PALETTE["danger"],   row=0, col=2)
        self._rate_lbl   = self._badge("성공률",    "0%",
                                        PALETTE["warning"],  row=0, col=3)

        # ── Treeview ─────────────────────────────────────────
        tv_frame = tk.Frame(self,
                            bg=PALETTE["card"],
                            highlightbackground=PALETTE["border"],
                            highlightthickness=1)
        tv_frame.pack(fill=tk.BOTH, expand=True)

        cols = ("ts","job","platform","workflow",
                "succ","fail","rate")
        self._tv = ttk.Treeview(
            tv_frame, columns=cols,
            show="headings", height=16)
        headers = [
            ("ts",       "일시",       140),
            ("job",      "작업명",     160),
            ("platform", "플랫폼",      80),
            ("workflow", "작업유형",   120),
            ("succ",     "성공",        70),
            ("fail",     "실패",        70),
            ("rate",     "성공률",      80),
        ]
        for col, hd, w in headers:
            self._tv.heading(col, text=hd)
            self._tv.column(col, width=w,
                            anchor=tk.CENTER,
                            stretch=col=="job")
        style = ttk.Style()
        style.configure("Treeview",
                        background=PALETTE["card"],
                        foreground=PALETTE["text"],
                        rowheight=26,
                        fieldbackground=PALETTE["card"])
        tv_sb = ttk.Scrollbar(tv_frame,
                              orient=tk.VERTICAL,
                              command=self._tv.yview)
        self._tv.configure(yscrollcommand=tv_sb.set)
        tv_sb.pack(side=tk.RIGHT, fill=tk.Y)
        self._tv.pack(side=tk.LEFT,
                      fill=tk.BOTH, expand=True)

    def _badge(self, label: str, value: str,
               color: str, row: int = 0, col: int = 0) -> tk.Label:
        # 외곽 프레임 (그림자 효과) — grid 배치
        outer = tk.Frame(self._badge_frame,
                         bg=PALETTE["border"],
                         padx=1, pady=1)
        outer.grid(row=row, column=col, padx=(0, 8), pady=4, sticky="ew")
        f = tk.Frame(outer, bg=PALETTE["card"])
        f.pack(fill=tk.BOTH)
        # 상단 컬러 바
        tk.Frame(f, bg=color, height=3
                 ).pack(fill=tk.X)
        inner = tk.Frame(f, bg=PALETTE["card"])
        inner.pack(padx=20, pady=(8, 10))
        tk.Label(inner, text=label,
                 font=(_FF, 8),
                 bg=PALETTE["card"],
                 fg=PALETTE["muted"]
                 ).pack()
        lbl = tk.Label(inner, text=value,
                       font=(_FF, 18, "bold"),
                       bg=PALETTE["card"], fg=color)
        lbl.pack()
        return lbl

    def add_record(self, job_name: str,
                   succ: int, fail: int):
        """작업 완료 시 호출"""
        from datetime import datetime as _dt
        job_data = {}
        for f in JOBS_DIR.glob("*.json"):
            d = load_json(f, {})
            if d.get("name") == job_name:
                job_data = d
                break
        rec = {
            "ts":       _dt.now().strftime(
                            "%Y-%m-%d %H:%M"),
            "job":      job_name,
            "platform": job_data.get("platform",""),
            "workflow": job_data.get("workflow",""),
            "succ":     succ,
            "fail":     fail,
            "rate":     f"{succ/(succ+fail)*100:.1f}%"
                        if (succ+fail) > 0 else "0%",
        }
        self._records.append(rec)
        self._save_stats()
        self.refresh()

    def refresh(self):
        self._tv.delete(*self._tv.get_children())
        total = succ = fail = 0
        for r in reversed(self._records):
            total += r["succ"] + r["fail"]
            succ  += r["succ"]
            fail  += r["fail"]
            plat  = r.get("platform","")
            icon  = "🟡" if plat=="kakao" else "🔵"
            wk    = r.get("workflow","")
            wdef  = PLATFORM_WORKFLOWS.get(wk,{})
            self._tv.insert("", tk.END, values=(
                r["ts"], r["job"],
                f"{icon} {PLATFORMS.get(plat,{}).get('name',plat)}",
                wdef.get("name", wk),
                r["succ"], r["fail"], r["rate"],
            ))
        rate = f"{succ/total*100:.1f}%" \
               if total > 0 else "0%"
        self._total_lbl.config(text=str(total))
        self._succ_lbl.config( text=str(succ))
        self._fail_lbl.config( text=str(fail))
        self._rate_lbl.config( text=rate)

    def _load_stats(self):
        data = load_json(STATS_PATH, {"records":[]})
        self._records = data.get("records", [])
        self.refresh()

    def _save_stats(self):
        save_json(STATS_PATH,
                  {"records": self._records})

    def _export_csv(self):
        if not self._records:
            self.app._set_status("⚠️ 내보낼 통계 데이터가 없습니다.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV","*.csv")],
            initialfile=f"stats_"
                        f"{datetime.now():%Y%m%d}")
        if not path: return
        try:
            import csv as _c
            with open(path,"w",newline="",
                      encoding="utf-8-sig") as f:
                w = _c.DictWriter(f,
                    fieldnames=["ts","job","platform",
                                "workflow","succ",
                                "fail","rate"])
                w.writeheader()
                w.writerows(self._records)
            self.app._set_status(f"✅ 통계 저장: {path}")
        except Exception as e:
            messagebox.showerror("저장 실패", str(e))

    def _reset(self):
        if not messagebox.askyesno("초기화",
                "통계를 모두 초기화할까요?"):
            return
        self._records.clear()
        self._save_stats()
        self.refresh()


def _app_build_stats_tab(self, frame):
    tab = StatsTab(frame, self)
    tab.pack(fill=tk.BOTH, expand=True)
    self._stats_tab = tab

App._build_stats_tab = _app_build_stats_tab


# ============================================================
# Block 5-B : SettingsTab — 설정
# ============================================================

class SettingsTab(tk.Frame):
    def __init__(self, master, app: "App"):
        super().__init__(master, bg=PALETTE["bg"])
        self.app = app
        self._build()
        self._load()

    def _build(self):
        # ── 탭 헤더 ──────────────────────────────────────────
        hdr = tk.Frame(self, bg=PALETTE["bg"])
        hdr.pack(fill=tk.X, pady=(0, 10))

        title_f = tk.Frame(hdr, bg=PALETTE["bg"])
        title_f.pack(side=tk.LEFT)
        tk.Label(title_f, text="⚙",
                 font=("Segoe UI Emoji", 15),
                 bg=PALETTE["bg"], fg=PALETTE["primary"]
                 ).pack(side=tk.LEFT)
        tk.Label(title_f, text="  설정",
                 font=F_TITLE, bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)

        # 헤더 우측 고정 저장 버튼 (sticky header)
        self._hdr_save_btn = tk.Button(
            hdr, text="💾  저장",
            command=self._save,
            bg=PALETTE["primary"], fg="#FFFFFF",
            relief=tk.FLAT,
            font=F_BTN_S,
            activebackground=PALETTE["primary2"],
            cursor="hand2", padx=14, pady=5)
        self._hdr_save_btn.pack(side=tk.RIGHT)
        self._hdr_save_btn.bind("<Enter>",
            lambda e: self._hdr_save_btn.config(bg=PALETTE["primary2"]))
        self._hdr_save_btn.bind("<Leave>",
            lambda e: self._hdr_save_btn.config(bg=PALETTE["primary"]))

        # 구분선
        tk.Frame(self, bg=PALETTE["border"], height=1
                 ).pack(fill=tk.X, pady=(0, 8))

        # 스크롤 캔버스
        canvas = tk.Canvas(self, bg=PALETTE["bg"],
                           highlightthickness=0)
        vsb = tk.Scrollbar(self, orient=tk.VERTICAL,
                           command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT,
                    fill=tk.BOTH, expand=True)
        inner = tk.Frame(canvas, bg=PALETTE["bg"])
        win   = canvas.create_window(
            (0,0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e:
            canvas.configure(
                scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e:
            canvas.itemconfig(win, width=e.width))
        canvas.bind("<MouseWheel>", lambda e:
            canvas.yview_scroll(
                int(-1*(e.delta/120)), "units"))

        def card(title):
            # 섹션 제목 (좌측 4px 컬러 바)
            title_row = tk.Frame(inner, bg=PALETTE["bg"])
            title_row.pack(fill=tk.X, padx=16, pady=(16, 4))
            tk.Frame(title_row, bg=PALETTE["primary"], width=4
                     ).pack(side=tk.LEFT, fill=tk.Y)
            tk.Label(title_row, text=f"  {title}",
                     font=F_HEAD,
                     bg=PALETTE["bg"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT)
            tk.Frame(title_row, bg=PALETTE["border"], height=1
                     ).pack(side=tk.LEFT, fill=tk.X, expand=True,
                            padx=(12, 0), pady=6)
            f = tk.Frame(inner, bg=PALETTE["card"],
                         highlightbackground=PALETTE["border"],
                         highlightthickness=1)
            f.pack(fill=tk.X, padx=16, pady=(0, 4))
            return f

        def row(parent, label, widget_fn):
            r = tk.Frame(parent, bg=PALETTE["card"])
            r.pack(fill=tk.X, padx=0, pady=0)
            tk.Frame(r, bg=PALETTE["border"], height=1
                     ).pack(fill=tk.X)
            inner_r = tk.Frame(r, bg=PALETTE["card"])
            inner_r.pack(fill=tk.X, padx=12, pady=8)
            tk.Label(inner_r, text=label, width=16,
                     anchor=tk.W,
                     font=F_LABEL,
                     bg=PALETTE["card"],
                     fg=PALETTE["text2"]
                     ).pack(side=tk.LEFT)
            widget_fn(inner_r)

        # ── 경로 설정 ────────────────────────────────────
        c1 = card("📁 경로 설정")
        self._log_dir_var  = tk.StringVar()
        self._out_dir_var  = tk.StringVar()

        def _log_w(p):
            tk.Entry(p, textvariable=self._log_dir_var,
                     bg=PALETTE["card2"], fg=PALETTE["text"],
                     insertbackground=PALETTE["text"],
                     relief=tk.FLAT,
                     font=F_LABEL, width=28
                     ).pack(side=tk.LEFT, padx=(0,6))
            tk.Button(p, text="📂",
                      command=lambda:
                          self._browse_dir(self._log_dir_var),
                      bg=PALETTE["card"],
                      fg=PALETTE["text"],
                      relief=tk.FLAT, cursor="hand2",
                      padx=4).pack(side=tk.LEFT)
        row(c1, "로그 폴더", _log_w)

        def _out_w(p):
            tk.Entry(p, textvariable=self._out_dir_var,
                     bg=PALETTE["card2"], fg=PALETTE["text"],
                     insertbackground=PALETTE["text"],
                     relief=tk.FLAT,
                     font=F_LABEL, width=28
                     ).pack(side=tk.LEFT, padx=(0,6))
            tk.Button(p, text="📂",
                      command=lambda:
                          self._browse_dir(self._out_dir_var),
                      bg=PALETTE["card"],
                      fg=PALETTE["text"],
                      relief=tk.FLAT, cursor="hand2",
                      padx=4).pack(side=tk.LEFT)
        row(c1, "출력 폴더", _out_w)

        # ── 마우스 설정 ──────────────────────────────────
        c2 = card("🖱️ 마우스 설정")
        self._click_delay_var = tk.StringVar()
        self._type_delay_var  = tk.StringVar()
        self._jitter_var      = tk.StringVar()
        self._failsafe_var    = tk.BooleanVar()

        def _cd_w(p):
            tk.Entry(p, textvariable=self._click_delay_var,
                     width=8, relief=tk.FLAT,
                     bg=PALETTE["card2"], fg=PALETTE["text"],
                     insertbackground=PALETTE["text"],
                     font=F_MONO
                     ).pack(side=tk.LEFT)
            tk.Label(p, text="초",
                     font=F_SMALL,
                     bg=PALETTE["card"],
                     fg=PALETTE["text"]
                     ).pack(side=tk.LEFT, padx=(4,0))
        row(c2, "클릭 후 딜레이", _cd_w)

        def _td_w(p):
            tk.Entry(p, textvariable=self._type_delay_var,
                     width=8, relief=tk.FLAT,
                     bg=PALETTE["card2"], fg=PALETTE["text"],
                     insertbackground=PALETTE["text"],
                     font=F_MONO
                     ).pack(side=tk.LEFT)
            tk.Label(p, text="초",
                     font=F_SMALL,
                     bg=PALETTE["card"],
                     fg=PALETTE["text"]
                     ).pack(side=tk.LEFT, padx=(4,0))
        row(c2, "입력 딜레이", _td_w)

        def _jt_w(p):
            tk.Entry(p, textvariable=self._jitter_var,
                     width=8, relief=tk.FLAT,
                     bg=PALETTE["card2"], fg=PALETTE["text"],
                     insertbackground=PALETTE["text"],
                     font=F_MONO
                     ).pack(side=tk.LEFT)
            tk.Label(p, text="초 (±랜덤)",
                     font=F_SMALL,
                     bg=PALETTE["card"],
                     fg=PALETTE["text"]
                     ).pack(side=tk.LEFT, padx=(4,0))
        row(c2, "지터(Jitter)", _jt_w)

        def _fs_w(p):
            tk.Checkbutton(p, text="Failsafe 활성화",
                           variable=self._failsafe_var,
                           bg=PALETTE["card"],
                           fg=PALETTE["text"],
                           selectcolor=PALETTE["active"],
                           activebackground=PALETTE["card"],
                           font=F_LABEL
                           ).pack(side=tk.LEFT)
            tk.Label(p,
                     text="(마우스를 화면 모서리로 이동 시 긴급 중지)",
                     font=F_SMALL,
                     bg=PALETTE["card"],
                     fg=PALETTE["text"]
                     ).pack(side=tk.LEFT, padx=(8,0))
        row(c2, "안전장치", _fs_w)

        # ── 전역 딜레이 ──────────────────────────────────
        c3 = card("⏱️ 전역 딜레이")
        self._gd_min_var = tk.StringVar()
        self._gd_max_var = tk.StringVar()

        def _gd_w(p):
            for lbl, var in [
                ("최소", self._gd_min_var),
                ("최대", self._gd_max_var)
            ]:
                tk.Label(p, text=lbl,
                         font=F_LABEL,
                         bg=PALETTE["card"],
                         fg=PALETTE["text"]
                         ).pack(side=tk.LEFT,
                                padx=(0,4))
                tk.Entry(p, textvariable=var,
                         width=6, relief=tk.FLAT,
                         bg=PALETTE["card2"],
                         fg=PALETTE["text"],
                         insertbackground=PALETTE["text"],
                         font=F_MONO
                         ).pack(side=tk.LEFT,
                                padx=(0,16))
            tk.Label(p, text="초",
                     font=F_SMALL,
                     bg=PALETTE["card"],
                     fg=PALETTE["text"]
                     ).pack(side=tk.LEFT)
        row(c3, "항목 간 딜레이", _gd_w)

        # ── 스크린샷 캡처 설정 ───────────────────────────
        c4 = card("📸 스크린샷 캡처 설정")
        self._ss_enabled_var  = tk.BooleanVar(value=True)
        self._ss_interval_var = tk.StringVar(value="60")
        self._ss_on_error_var = tk.BooleanVar(value=True)

        def _ss_enabled_w(p):
            tk.Checkbutton(
                p, text="캡처 기능 활성화",
                variable=self._ss_enabled_var,
                font=F_LABEL,
                bg=PALETTE["card"], fg=PALETTE["text"],
                selectcolor=PALETTE["card2"],
                activebackground=PALETTE["card"]
            ).pack(side=tk.LEFT)
        row(c4, "활성화", _ss_enabled_w)

        def _ss_interval_w(p):
            tk.Entry(p, textvariable=self._ss_interval_var,
                     width=6, relief=tk.FLAT,
                     bg=PALETTE["card2"], fg=PALETTE["text"],
                     insertbackground=PALETTE["text"],
                     font=F_MONO
                     ).pack(side=tk.LEFT, padx=(0, 6))
            tk.Label(p, text="초마다 자동 캡처  (예: 60=1분, 3600=1시간)",
                     font=F_SMALL,
                     bg=PALETTE["card"], fg=PALETTE["muted"]
                     ).pack(side=tk.LEFT)
        row(c4, "주기적 캡처 간격", _ss_interval_w)

        def _ss_error_w(p):
            tk.Checkbutton(
                p, text="오류 발생 시 즉시 캡처",
                variable=self._ss_on_error_var,
                font=F_LABEL,
                bg=PALETTE["card"], fg=PALETTE["text"],
                selectcolor=PALETTE["card2"],
                activebackground=PALETTE["card"]
            ).pack(side=tk.LEFT)
            tk.Label(p,
                     text="(실패 항목·FailSafe 등)",
                     font=F_SMALL,
                     bg=PALETTE["card"], fg=PALETTE["muted"]
                     ).pack(side=tk.LEFT, padx=(8, 0))
        row(c4, "오류 캡처", _ss_error_w)

        # 저장 폴더 표시
        def _ss_dir_w(p):
            tk.Label(p,
                     text=str(SCREENSHOTS_DIR),
                     font=F_SMALL,
                     bg=PALETTE["card"], fg=PALETTE["muted"]
                     ).pack(side=tk.LEFT)
            tk.Button(p, text="📂 열기",
                      command=lambda: _open_folder(SCREENSHOTS_DIR),
                      bg=PALETTE["hover"], fg=PALETTE["text"],
                      relief=tk.FLAT, cursor="hand2",
                      font=F_SMALL, padx=6
                      ).pack(side=tk.LEFT, padx=(8, 0))
        row(c4, "저장 위치", _ss_dir_w)

        # ── 저장 버튼 영역 ───────────────────────────────
        save_wrap = tk.Frame(inner, bg=PALETTE["card"],
                             highlightbackground=PALETTE["border"],
                             highlightthickness=1)
        save_wrap.pack(fill=tk.X, padx=16, pady=(16, 20))
        save_inner = tk.Frame(save_wrap, bg=PALETTE["card"])
        save_inner.pack(fill=tk.X, padx=16, pady=12)

        save_btn = tk.Button(save_inner, text="💾  설정 저장",
                  command=self._save,
                  bg=PALETTE["primary"], fg="#FFFFFF",
                  relief=tk.FLAT,
                  font=(_FF, 10, "bold"),
                  activebackground=PALETTE["primary2"],
                  cursor="hand2", padx=24, pady=9)
        save_btn.pack(side=tk.LEFT)
        save_btn.bind("<Enter>",
                      lambda e: save_btn.config(bg=PALETTE["primary2"]))
        save_btn.bind("<Leave>",
                      lambda e: save_btn.config(bg=PALETTE["primary"]))
        tk.Label(save_inner,
                 text="  저장 후 즉시 반영됩니다",
                 font=F_SMALL, fg=PALETTE["muted"],
                 bg=PALETTE["card"]).pack(side=tk.LEFT, padx=(12, 0))

    def _browse_dir(self, var: tk.StringVar):
        path = filedialog.askdirectory()
        if path: var.set(path)

    def _load(self):
        cfg = self.app.config_data
        p   = cfg.get("paths", {})
        m   = cfg.get("mouse", {})
        g   = cfg.get("global_delay", {})
        ss  = cfg.get("screenshot", {})
        self._log_dir_var.set(
            p.get("logs",  str(LOGS_DIR)))
        self._out_dir_var.set(
            p.get("output",str(DATA_DIR)))
        self._click_delay_var.set(
            str(m.get("click_delay", 0.15)))
        self._type_delay_var.set(
            str(m.get("type_delay",  0.05)))
        self._jitter_var.set(
            str(m.get("jitter",      0.3)))
        self._failsafe_var.set(
            m.get("failsafe", True))
        self._gd_min_var.set(
            str(g.get("min", 2.0)))
        self._gd_max_var.set(
            str(g.get("max", 5.0)))
        # 스크린샷 설정 로드
        self._ss_enabled_var.set(ss.get("enabled",  True))
        self._ss_interval_var.set(str(ss.get("interval_min", 60)))
        self._ss_on_error_var.set(ss.get("on_error", True))


    def _save(self):
        cfg = self.app.config_data
        cfg["paths"]["logs"]   = \
            self._log_dir_var.get().strip()
        cfg["paths"]["output"] = \
            self._out_dir_var.get().strip()
        cfg["mouse"]["click_delay"] = \
            safe_float(self._click_delay_var.get(), 0.15)
        cfg["mouse"]["type_delay"]  = \
            safe_float(self._type_delay_var.get(), 0.05)
        cfg["mouse"]["jitter"]      = \
            safe_float(self._jitter_var.get(), 0.3)
        cfg["mouse"]["failsafe"]    = \
            self._failsafe_var.get()
        cfg["global_delay"]["min"]  = \
            safe_float(self._gd_min_var.get(), 2.0)
        cfg["global_delay"]["max"]  = \
            safe_float(self._gd_max_var.get(), 5.0)
        # 스크린샷 설정 저장
        cfg.setdefault("screenshot", {})
        cfg["screenshot"]["enabled"]      = self._ss_enabled_var.get()
        cfg["screenshot"]["interval_min"] = safe_float(
            self._ss_interval_var.get(), 60.0)
        cfg["screenshot"]["on_error"]     = self._ss_on_error_var.get()


        # pyautogui failsafe 적용
        if HAS_PYAUTOGUI:
            pyautogui.FAILSAFE = \
                cfg["mouse"]["failsafe"]
            pyautogui.PAUSE    = \
                cfg["mouse"]["click_delay"]

        save_json(CONFIG_PATH, cfg)
        self.app._set_status("✅ 설정이 저장되었습니다.")


def _app_build_settings_tab(self, frame):
    tab = SettingsTab(frame, self)
    tab.pack(fill=tk.BOTH, expand=True)
    self._settings_tab = tab

App._build_settings_tab = _app_build_settings_tab


# ============================================================
# LoginDialog  ―  구글 시트 CSV 인증 (v1.51 신규)
# ============================================================
# · 카카오톡_올인원_v2.6 의 LoginDialog 를 메신저 올인원 팔레트로 이식
# · PALETTE["bg"] / PALETTE["card"] / PALETTE["primary"] / PALETTE["text"] 사용
# · show() 호출 후 (authenticated:bool, username:str|None) 반환
# ============================================================

class LoginDialog:
    """구글 시트 CSV 기반 로그인 (v1.51 신규)

    사용 예::

        dlg = LoginDialog(sheet_url=SHEET_URL)
        ok, user = dlg.show()
        if not ok:
            sys.exit(0)
    """

    # ── 창 크기 상수 ──────────────────────────────────────
    _W, _H = 460, 340

    def __init__(self, sheet_url: str | None = None, debug: bool = False):
        # ── 인증 상태 ──────────────────────────────────────
        self.sheet_url     = sheet_url or SHEET_URL
        self.debug         = debug
        self.authenticated = False
        self.username: str | None = None

        # ── Tk 창 생성 ────────────────────────────────────
        self.root = tk.Tk()
        self.root.title(f"메신저 올인원 v{APP_VERSION} — 로그인")
        self.root.geometry(f"{self._W}x{self._H}")
        self.root.resizable(False, False)
        self.root.configure(bg=PALETTE["bg"])
        self._center()
        self._build()

    # ── 화면 중앙 배치 ────────────────────────────────────
    def _center(self) -> None:
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x  = (sw - self._W) // 2
        y  = (sh - self._H) // 2
        self.root.geometry(f"{self._W}x{self._H}+{x}+{y}")

    # ── UI 구성 ───────────────────────────────────────────
    def _build(self) -> None:
        P = PALETTE          # 팔레트 단축 참조
        FF = "Malgun Gothic" # 한글 폰트

        outer = tk.Frame(self.root, bg=P["bg"])
        outer.pack(expand=True, fill=tk.BOTH, padx=36, pady=28)

        # ── 제목 영역 ─────────────────────────────────────
        tk.Label(
            outer,
            text=f"🚀  {APP_TITLE}",
            font=(FF, 14, "bold"),
            bg=P["bg"], fg=P["text"],
        ).pack(pady=(0, 2))
        tk.Label(
            outer,
            text="관리자에게 발급받은 ID / PW 를 입력하세요.",
            font=(FF, 9),
            bg=P["bg"], fg=P["muted"],
        ).pack(pady=(0, 18))

        # ── requests 미설치 경고 ──────────────────────────
        if not HAS_REQUESTS:
            tk.Label(
                outer,
                text="⚠  requests 패키지가 없어 로그인을 사용할 수 없습니다.\n"
                     "pip install requests 실행 후 재시작하세요.",
                font=(FF, 9),
                bg="#FEF3C7", fg="#92400E",
                relief="solid", bd=1,
                justify="left", wraplength=360,
                padx=8, pady=6,
            ).pack(fill=tk.X, pady=(0, 14))

        # ── ID 입력 행 ────────────────────────────────────
        row_id = tk.Frame(outer, bg=P["bg"])
        row_id.pack(fill=tk.X, pady=5)
        tk.Label(
            row_id, text="ID", width=5, anchor="w",
            font=(FF, 10), bg=P["bg"], fg=P["muted"],
        ).pack(side=tk.LEFT)
        self.id_var = tk.StringVar()
        tk.Entry(
            row_id, textvariable=self.id_var,
            font=(FF, 10),
            bg=P["card"], relief="solid", bd=1, width=28,
        ).pack(side=tk.LEFT, padx=(4, 0))

        # ── PW 입력 행 ────────────────────────────────────
        row_pw = tk.Frame(outer, bg=P["bg"])
        row_pw.pack(fill=tk.X, pady=5)
        tk.Label(
            row_pw, text="PW", width=5, anchor=tk.W,
            font=(FF, 10), bg=P["bg"], fg=P["muted"],
        ).pack(side=tk.LEFT)
        self.pw_var = tk.StringVar()
        tk.Entry(
            row_pw, textvariable=self.pw_var, show="●",
            font=(FF, 10),
            bg=P["card"], relief="solid", bd=1, width=28,
        ).pack(side=tk.LEFT, padx=(4, 0))

        # ── 버튼 행 ───────────────────────────────────────
        row_btn = tk.Frame(outer, bg=P["bg"])
        row_btn.pack(pady=22)

        login_state = "normal" if HAS_REQUESTS else "disabled"
        tk.Button(
            row_btn, text="  로그인  ",
            command=self._login,
            font=(FF, 10, "bold"),
            bg=P["primary"], fg="white",
            activebackground=P["primary2"], activeforeground="white",
            relief=tk.FLAT, padx=16, pady=7,
            cursor="hand2", state=login_state,
        ).pack(side=tk.LEFT, padx=6)
        tk.Button(
            row_btn, text="  종료  ",
            command=self._exit,
            font=(FF, 10),
            bg=P["border"], fg=P["muted"],
            relief=tk.FLAT, padx=16, pady=7,
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=6)

        # ── 하단 안내 ─────────────────────────────────────
        tk.Label(
            outer,
            text="※ ID / PW 는 관리자에게 문의하세요.",
            font=(FF, 9),
            bg=P["bg"], fg=P["muted"],
        ).pack(pady=(4, 0))

        # ── 단축키 ────────────────────────────────────────
        self.root.bind("<Return>", lambda _e: self._login())
        self.root.after(100, lambda: self.root.focus_force())

    # ── 구글 시트 CSV → 사용자 딕셔너리 ─────────────────────
    def _load_users(self) -> dict | None:
        """
        구글 시트 CSV 를 fetch 하여 사용자 정보 딕셔너리를 반환한다.

        반환 형식::

            {
                "alice": {"pw": "1234", "expire": "2026-12-31", "status": "ACTIVE"},
                ...
            }

        연결 오류 시 messagebox 를 표시하고 None 을 반환한다.
        """
        try:
            resp = _requests.get(self.sheet_url, timeout=10)
            resp.raise_for_status()

            # ── CSV 파싱 ─────────────────────────────────
            reader = _csv_login.DictReader(_StringIO(resp.text))
            users: dict[str, dict] = {}
            for row in reader:
                uid  = (row.get("ID")       or row.get("id")       or "").strip()
                pw   = (row.get("PASSWORD") or row.get("password") or
                        row.get("PW")       or row.get("pw")       or "").strip()
                exp  = (row.get("EXPIRE")   or row.get("expire")   or
                        row.get("만료일")   or "").strip()
                stat = (row.get("STATUS")   or row.get("status")   or
                        row.get("활성여부") or row.get("상태")     or "").strip()
                if uid:
                    users[uid] = {"pw": pw, "expire": exp, "status": stat}
            return users

        except _requests.RequestException as exc:
            tk.messagebox.showerror(
                "연결 오류",
                f"구글 시트 연결 실패:\n{exc}\n\n"
                "인터넷 연결을 확인하거나 관리자에게 문의하세요.",
            )
            return None
        except Exception as exc:
            tk.messagebox.showerror("오류", str(exc))
            return None

    # ── 만료일 검사 ───────────────────────────────────────
    def _check_expire(self, exp_str: str) -> bool:
        """
        exp_str 이 비어 있으면 무기한(True) 처리.
        YYYY-MM-DD 형식으로 파싱하며, 파싱 실패 시도 True 반환(관대하게 처리).
        """
        if not exp_str:
            return True
        try:
            return datetime.now() <= datetime.strptime(exp_str, "%Y-%m-%d")
        except Exception:
            return True   # 날짜 형식 오류 → 관대하게 통과

    # ── 로그인 검증 ───────────────────────────────────────
    def _login(self) -> None:
        """ID / PW 입력값을 구글 시트와 대조하여 인증을 수행한다."""
        uid = self.id_var.get().strip()
        pw  = self.pw_var.get().strip()

        if not uid or not pw:
            tk.messagebox.showwarning("입력 필요", "ID와 PW를 입력하세요.")
            return

        users = self._load_users()
        if users is None:
            return   # _load_users 내부에서 이미 에러 표시

        # ── 사용자 존재 & 비밀번호 확인 ─────────────────
        info = users.get(uid)
        if not info or info["pw"] != pw:
            tk.messagebox.showerror("로그인 실패",
                                    "ID 또는 비밀번호가 올바르지 않습니다.")
            self.pw_var.set("")
            return

        # ── 계정 활성 상태 확인 ───────────────────────────
        stat = info["status"].upper()
        if stat not in ("활성", "ACTIVE", "1", "TRUE", "YES"):
            tk.messagebox.showerror("로그인 실패", "비활성화된 계정입니다.\n관리자에게 문의하세요.")
            return

        # ── 만료일 확인 ───────────────────────────────────
        if not self._check_expire(info["expire"]):
            tk.messagebox.showerror(
                "로그인 실패",
                f"계정이 만료되었습니다.\n만료일: {info['expire']}\n관리자에게 문의하세요.",
            )
            return

        # ── 인증 성공 ─────────────────────────────────────
        self.authenticated = True
        self.username = uid
        tk.messagebox.showinfo("환영합니다", f"{uid}님, 로그인 성공! 🎉")
        self.root.quit()

    # ── 종료 ──────────────────────────────────────────────
    def _exit(self) -> None:
        """로그인 창의 종료 버튼 — 미인증 상태로 루프 종료."""
        self.root.quit()

    # ── 메인루프 실행 & 결과 반환 ─────────────────────────
    def show(self) -> tuple[bool, str | None]:
        """
        로그인 창 메인루프를 실행하고 인증 결과를 반환한다.

        반환값::

            (True,  username)  → 인증 성공
            (False, None)      → 창 닫기 / 종료 클릭
        """
        self.root.mainloop()
        try:
            if self.root.winfo_exists():
                self.root.destroy()
        except Exception:
            pass
        return self.authenticated, self.username


# ============================================================
# main
# ============================================================

def main():
    # ── pyautogui 초기 설정 ───────────────────────────────
    if HAS_PYAUTOGUI:
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE    = 0.05

    # ── 로그인 인증 (v1.51 신규) ──────────────────────────
    # config.json 에 "sheet_url" 키가 있으면 우선 사용하고,
    # 없으면 코드 상단의 SHEET_URL 상수를 사용한다.
    try:
        _cfg_for_login = json.loads(CONFIG_PATH.read_text("utf-8")) \
            if CONFIG_PATH.exists() else {}
    except Exception:
        _cfg_for_login = {}

    _sheet_url = _cfg_for_login.get("sheet_url") or SHEET_URL

    login_dlg = LoginDialog(sheet_url=_sheet_url)
    _authed, _username = login_dlg.show()

    if not _authed:
        # 창 닫기 또는 종료 버튼 → 프로그램 종료
        sys.exit(0)

    app = App()

    # 시작 로그
    def _startup_log():
        time.sleep(0.5)
        deps = []
        deps.append("pyautogui ✅" if HAS_PYAUTOGUI
                    else "pyautogui ❌ (필수)")
        deps.append("pyperclip ✅" if HAS_PYPERCLIP
                    else "pyperclip ❌")
        deps.append("OCR(pytesseract+Pillow) ✅"
                    if HAS_OCR
                    else "OCR ❌ (텔레그램 이미지등 선택사항)")
        for d in deps:
            app.after(0, lambda m=d:
                app._log_tab.append(m, "INFO", "시스템")
                if hasattr(app, "_log_tab") else None)

    threading.Thread(
        target=_startup_log, daemon=True).start()

    app.mainloop()


if __name__ == "__main__":
    main()