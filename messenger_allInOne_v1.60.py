# ============================================================
# messenger_allInOne_v1.60  변경 이력
# ============================================================
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

import json, os, sys, threading, time, random, string, re, queue
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
APP_VERSION = "1.60"
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
        used_enc = "utf-8"
        for enc in ("utf-8-sig", "utf-8", "cp949", "latin-1"):
            try:
                raw = fpath.read_text(encoding=enc)
                used_enc = enc
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
LOGS_DIR     = APP_DIR  / "logs"
DATA_DIR     = APP_DIR  / "data"

for _d in (CONFIG_DIR, TEMPLATE_DIR, JOBS_DIR, LOGS_DIR, DATA_DIR):
    _d.mkdir(parents=True, exist_ok=True)

CONFIG_PATH = CONFIG_DIR / "config.json"
STATS_PATH  = CONFIG_DIR / "stats.json"

# ── UI 팔레트 (v1.10 라이트 테마 — community_poster 벤치마킹) ─
PALETTE = {
    # ── 배경 계층 (라이트 테마 — community_poster v5.20 벤치마킹) ──
    "bg":       "#F8F9FA",   # 메인 배경 (Tailwind gray-50)
    "sidebar":  "#1E293B",   # 사이드바 다크 슬레이트 (유지)
    "card":     "#FFFFFF",   # 카드/패널 흰색
    "card2":    "#F1F5F9",   # 입력창 배경 (slate-100)
    # ── 테두리/구분선 ─────────────────────────────────────────
    "border":   "#E2E8F0",   # 일반 테두리 (slate-200)
    "border2":  "#CBD5E1",   # 강조 테두리 (slate-300)
    # ── 인터랙션 ─────────────────────────────────────────────
    "hover":    "#F1F5F9",   # hover 배경 (slate-100)
    "active":   "#E2E8F0",   # 활성 배경 (slate-200)
    "selected": "#DBEAFE",   # 트리뷰 선택 행 (blue-100)
    # ── 포인트 컬러 (Tailwind CSS 체계) ──────────────────────
    "primary":  "#2563EB",   # 블루 포인트 (blue-600, 흰글 5.2:1)
    "primary2": "#1D4ED8",   # 블루 호버  (blue-700, 흰글 6.7:1)
    "success":  "#22C55E",   # 성공 초록  배경/뱃지용 (green-500)
    "success_text": "#15803D", # 성공 텍스트용 (green-700, 대비 7.4:1)
    "warning_text": "#B45309",   # 경고 텍스트용 (amber-700, white 대비 5.02:1 ✅)
    "warning":  "#F59E0B",   # 경고 앰버  (amber-500)
    "danger":   "#DC2626",   # 위험 레드  (red-600, 흰글 4.8:1)
    "accent":   "#8B5CF6",   # 강조 바이올렛 (violet-500)
    # ── 텍스트 계층 ───────────────────────────────────────────
    "text":     "#1E293B",   # 기본 텍스트 (slate-800)
    "text2":    "#64748B",   # 보조 텍스트 (slate-500)
    "muted":    "#475569",   # 힌트 텍스트 (slate-600, card 대비 7.58:1 ✅)
    # ── 사이드바 전용 (다크 bg 위 텍스트) ────────────────────
    "sidebar_text": "#F1F5F9",  # 사이드바 기본 텍스트 (밝은 slate)
    # ── 플랫폼 원색 (유지) ────────────────────────────────────
    "kakao":    "#FEE500",
    "telegram": "#229ED9",
}

# ── 폰트 상수 (v1.08 통일) ───────────────────────────────
_FF  = "Malgun Gothic"         # 기본 한글 폰트
_FFM = "Consolas"              # 모노스페이스
F_TITLE  = (_FF,  13, "bold")  # 탭 제목 (13pt bold)
F_HEAD   = (_FF,  10, "bold")  # 섹션 헤더 (10pt bold)
F_BODY   = (_FF,  10)          # 본문 (10pt)
F_LABEL  = (_FF,   9)          # 라벨 (9pt)
F_SMALL  = (_FF,   9)          # 보조/힌트 (9pt, 8pt→9pt 가독성 개선)
F_BTN    = (_FF,   9, "bold")  # 버튼 (9pt bold)
F_BTN_S  = (_FF,   9)          # 소형 버튼 (9pt, 8pt→9pt 통일)
F_MONO   = (_FFM,  9)          # 입력창/좌표 값 (9pt)
F_MONO_S = (_FFM,  9)          # 소형 모노 (9pt, 8pt→9pt 통일)
F_MONO_B = (_FFM, 10, "bold")  # 굵은 모노 (미리보기 등)
F_ICON   = ("Segoe UI Emoji", 18)  # 이모지/아이콘

# ── 사이드바 탭 ─────────────────────────────────────────────
SIDEBAR_TABS = [
    ("templates", "🗂️  작업 템플릿"),
    ("jobs",      "📋  작업 관리"),
    ("log",       "🗒️  로그"),
    ("stats",     "📊  통계"),
    ("settings",  "⚙️   설정"),
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
        "coord_keys":   ["chrome_addr", "join_btn", "close_tab"],
        "coord_labels": ["🌐 크롬 주소창", "✅ 가입 버튼", "❌ 탭 닫기"],
        "coord_types":  ["point", "point", "point"],
    },
    "telegram_message": {
        "name":         "메시지 발송",
        "platform":     "telegram",
        "needs_ocr":    False,
        "needs_message":True,
        "needs_image":  True,   # 이미지 첨부 지원
        "coord_keys":   ["chrome_addr", "message_input", "send_btn"],
        "coord_labels": ["🌐 크롬 주소창", "✏️ 메시지 입력창", "📤 전송 버튼"],
        "coord_types":  ["point", "point", "point"],
    },
}


# ── v1.60: 워크플로우별 기본 예상 소요시간(초) ────────────────────────
WORKFLOW_BASE_DURATION: dict = {
    "kakao_friend":    90,
    "kakao_openchat": 120,
    "telegram_join":   60,
    "telegram_message": 75,
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
    except Exception:
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
    h = hex_color.lstrip("#")
    r,g,b = tuple(int(h[i:i+2],16) for i in (0,2,4))
    r = min(255, int(r+(255-r)*factor))
    g = min(255, int(g+(255-g)*factor))
    b = min(255, int(b+(255-b)*factor))
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

        # ── 데이터 로드 ────────────────────────────────────
        self.config_data = load_json(CONFIG_PATH, self._default_config())
        self.stats_data  = load_json(STATS_PATH,  {"stats": [], "total": {}})

        # ── 상태 변수 ──────────────────────────────────────
        self._active_tab: str = "templates"
        self._tab_btns:   dict[str, tk.Label] = {}
        self._tab_frames: dict[str, tk.Frame] = {}
        self._status_var  = tk.StringVar(value="준비")

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
        }

    # ── 전체 UI ─────────────────────────────────────────────
    def _build_ui(self):
        self._build_header()
        body = tk.Frame(self, bg=PALETTE["bg"])
        body.pack(fill=tk.BOTH, expand=True)
        self._build_sidebar(body)
        self._build_content(body)
        self._build_statusbar()

    # ── 헤더 ────────────────────────────────────────────────
    def _build_header(self):
        hdr = tk.Frame(self, bg=PALETTE["sidebar"], height=58)
        hdr.pack(fill=tk.X, side=tk.TOP)
        hdr.pack_propagate(False)
        # 하단 구분선
        tk.Frame(hdr, bg=PALETTE["border"], height=1
                 ).place(relx=0, rely=1.0, relwidth=1.0, anchor="sw")

        tk.Label(hdr, text="💬", font=F_ICON,
                 bg=PALETTE["sidebar"], fg=PALETTE["sidebar_text"]
                 ).pack(side=tk.LEFT, padx=(18, 8), pady=14)

        tk.Label(hdr, text="메신저 올인원",
                 font=F_TITLE,
                 bg=PALETTE["sidebar"], fg=PALETTE["sidebar_text"]
                 ).pack(side=tk.LEFT, pady=14)

        tk.Label(hdr, text=f" v{APP_VERSION}",
                 font=F_MONO_S,
                 bg=PALETTE["sidebar"], fg=PALETTE["sidebar_text"]
                 ).pack(side=tk.LEFT, pady=14)

        # 우측 의존성 뱃지
        dep = []
        dep.append("PyAG ✅" if HAS_PYAUTOGUI else "PyAG ❌")
        dep.append("OCR ✅"  if HAS_OCR       else "OCR ❌")
        dep.append("CB ✅"   if HAS_PYPERCLIP else "CB ❌")
        tk.Label(hdr, text="  ".join(dep),
                 font=F_MONO_S,
                 bg=PALETTE["sidebar"], fg=PALETTE["sidebar_text"]
                 ).pack(side=tk.RIGHT, padx=18)

    # ── 사이드바 ────────────────────────────────────────────
    def _build_sidebar(self, parent: tk.Frame):
        sb = tk.Frame(parent, bg=PALETTE["sidebar"], width=200)
        sb.pack(fill=tk.Y, side=tk.LEFT)
        sb.pack_propagate(False)
        # 우측 세로 구분선
        tk.Frame(parent, bg=PALETTE["border"], width=1
                 ).pack(fill=tk.Y, side=tk.LEFT)

        # 앱명 소형 레이블
        tk.Label(sb, text="MENU",
                 font=F_MONO_S,
                 bg=PALETTE["sidebar"], fg=PALETTE["sidebar_text"]
                 ).pack(anchor=tk.W, padx=18, pady=(14, 4))
        tk.Frame(sb, bg=PALETTE["border"], height=1
                 ).pack(fill=tk.X, padx=14, pady=(0, 6))

        for tab_id, label in SIDEBAR_TABS:
            self._make_tab_btn(sb, tab_id, label)

        # 하단 버전 표시
        tk.Frame(sb, bg=PALETTE["border"], height=1
                 ).pack(fill=tk.X, padx=14, side=tk.BOTTOM, pady=(0, 4))
        tk.Label(sb, text=f"v{APP_VERSION}",
                 font=F_MONO_S,
                 bg=PALETTE["sidebar"], fg=PALETTE["sidebar_text"]
                 ).pack(side=tk.BOTTOM, pady=6)

    def _make_tab_btn(self, parent, tab_id: str, label: str):
        btn = tk.Label(
            parent, text=f"  {label}",
            font=F_BODY,
            bg=PALETTE["sidebar"], fg=PALETTE["sidebar_text"],
            anchor=tk.W, cursor="hand2", padx=12, pady=11,
        )
        btn.pack(fill=tk.X, padx=8, pady=1)
        btn.bind("<Button-1>", lambda e, t=tab_id: self._switch_tab(t))
        btn.bind("<Enter>",    lambda e, b=btn: b.config(bg=PALETTE["hover"]))
        btn.bind("<Leave>",    lambda e, b=btn, t=tab_id: b.config(
            bg=PALETTE["selected"] if self._active_tab==t else PALETTE["sidebar"]))
        self._tab_btns[tab_id] = btn

    # ── 콘텐츠 영역 ─────────────────────────────────────────
    def _build_content(self, parent: tk.Frame):
        content = tk.Frame(parent, bg=PALETTE["bg"])
        content.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self._content_frame = tk.Frame(content, bg=PALETTE["bg"])
        self._content_frame.pack(fill=tk.BOTH, expand=True,
                                  padx=16, pady=(12,0))

        # 탭별 Frame 생성 (각 탭 클래스에서 채움)
        builders = {
            "templates": self._build_templates_tab,
            "jobs":      self._build_jobs_tab,
            "log":       self._build_log_tab,
            "stats":     self._build_stats_tab,
            "settings":  self._build_settings_tab,
        }
        for tab_id, builder in builders.items():
            frame = tk.Frame(self._content_frame, bg=PALETTE["bg"])
            self._tab_frames[tab_id] = frame
            builder(frame)
            frame.place(relwidth=1, relheight=1)
            frame.lower()

        self._switch_tab("templates")

    # ── 탭 전환 ─────────────────────────────────────────────
    def _switch_tab(self, tab_id: str):
        if self._active_tab in self._tab_btns:
            ob = self._tab_btns[self._active_tab]
            ob.config(bg=PALETTE["sidebar"], fg=PALETTE["sidebar_text"],
                      font=F_BODY)
        self._active_tab = tab_id
        if tab_id in self._tab_btns:
            nb = self._tab_btns[tab_id]
            nb.config(bg=PALETTE["selected"], fg=PALETTE["text"],
                      font=F_BTN)
        for tid, frame in self._tab_frames.items():
            frame.lift() if tid == tab_id else frame.lower()

    # ── 상태바 ──────────────────────────────────────────────
    def _build_statusbar(self):
        bar = tk.Frame(self, bg=PALETTE["sidebar"], height=28)
        bar.pack(fill=tk.X, side=tk.BOTTOM)
        bar.pack_propagate(False)
        tk.Frame(bar, bg=PALETTE["border"], height=1
                 ).place(relx=0, rely=0, relwidth=1.0)
        tk.Label(bar, textvariable=self._status_var,
                 font=F_SMALL,
                 bg=PALETTE["sidebar"], fg=PALETTE["sidebar_text"],
                 anchor=tk.W, padx=12).pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(bar, text=datetime.now().strftime("%Y-%m-%d"),
                 font=F_MONO_S,
                 bg=PALETTE["sidebar"], fg=PALETTE["sidebar_text"],
                 padx=12).pack(side=tk.RIGHT, fill=tk.Y)

    def _set_status(self, msg: str):
        self._status_var.set(msg)

    # ── Placeholder (이후 Block에서 채워짐) ─────────────────
    def _build_templates_tab(self, f): pass
    def _build_jobs_tab(self,      f): pass
    def _build_log_tab(self,       f): pass
    def _build_stats_tab(self,     f): pass
    def _build_settings_tab(self,  f): pass

    # ── 종료 ────────────────────────────────────────────────
    def _on_close(self):
        save_json(CONFIG_PATH, self.config_data)
        save_json(STATS_PATH,  self.stats_data)
        self.destroy()
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
        # 타이틀 행
        hdr = tk.Frame(self, bg=PALETTE["bg"])
        hdr.pack(fill=tk.X, pady=(0, 10))
        tk.Label(hdr, text="🗂️  작업 템플릿 관리",
                 font=F_TITLE,
                 bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        tk.Label(hdr,
                 text="템플릿을 먼저 만들고 → 작업 관리에서 선택하세요",
                 font=F_LABEL,
                 bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT, padx=(16, 0))

        # 도움말 버튼
        tk.Button(hdr, text="❓ 도움말",
                  command=self._show_help,
                  bg=PALETTE["card"], fg=PALETTE["text"],
                  relief=tk.FLAT, font=F_SMALL,
                  activebackground=PALETTE["hover"],
                  cursor="hand2", padx=8, pady=3
                  ).pack(side=tk.RIGHT)

        # 좌우 분할
        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL,
                               bg=PALETTE["border"], sashwidth=4,
                               sashrelief=tk.FLAT)
        paned.pack(fill=tk.BOTH, expand=True)

        # 왼쪽: 템플릿 목록
        left = tk.Frame(paned, bg=PALETTE["sidebar"], width=210)
        paned.add(left, minsize=180)
        self._build_list_panel(left)

        # 오른쪽: 편집 패널 (스크롤 가능)
        right = tk.Frame(paned, bg=PALETTE["bg"])
        paned.add(right, minsize=560)
        self._build_edit_panel(right)

    # ── 왼쪽: 템플릿 목록 패널 ──────────────────────────────
    def _build_list_panel(self, parent: tk.Frame):
        # 헤더
        lhdr = tk.Frame(parent, bg=PALETTE["sidebar"])
        lhdr.pack(fill=tk.X, padx=10, pady=(12, 6))
        tk.Label(lhdr, text="📄 템플릿 목록",
                 font=F_BTN,
                 bg=PALETTE["sidebar"], fg=PALETTE["sidebar_text"]
                 ).pack(side=tk.LEFT)

        # 리스트박스 + 스크롤
        lf = tk.Frame(parent, bg=PALETTE["sidebar"],
                      highlightbackground=PALETTE["border"],
                      highlightthickness=1)
        lf.pack(fill=tk.BOTH, expand=True, padx=8)

        sb = tk.Scrollbar(lf, orient=tk.VERTICAL)
        self._tmpl_lb = tk.Listbox(
            lf, yscrollcommand=sb.set,
            bg=PALETTE["card"], fg=PALETTE["text"],
            selectbackground=PALETTE["selected"],
            selectforeground=PALETTE["text"],
            font=F_LABEL,
            relief=tk.FLAT, bd=0, activestyle="none",
            highlightthickness=0,
        )
        sb.config(command=self._tmpl_lb.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self._tmpl_lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._tmpl_lb.bind("<<ListboxSelect>>", self._on_select)

        # 버튼 행
        bf = tk.Frame(parent, bg=PALETTE["sidebar"])
        bf.pack(fill=tk.X, padx=8, pady=8)
        btn_defs = [
            ("＋ 새 템플릿", self._add_template, PALETTE["primary"],  PALETTE["bg"]),
            ("⧉ 복제",       self._dup_template, PALETTE["hover"],    PALETTE["text2"]),
            ("✕ 삭제",       self._del_template, PALETTE["danger"],   PALETTE["text"]),
        ]
        for txt, cmd, bg, fg in btn_defs:
            tk.Button(bf, text=txt, command=cmd,
                      bg=bg, fg=fg,
                      relief=tk.FLAT, font=F_SMALL,
                      activebackground=_lighten(bg, 0.08),
                      activeforeground=fg,
                      cursor="hand2", padx=8, pady=4, bd=0,
                      ).pack(side=tk.LEFT, padx=2)

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

        pad = {"padx": 16, "pady": (0, 12)}

        # ── 섹션 헬퍼 ───────────────────────────────────────
        def section(title: str) -> tk.Frame:
            wrap = tk.Frame(self._edit_inner, bg=PALETTE["bg"])
            wrap.pack(fill=tk.X, **pad)
            # 섹션 제목 행
            title_row = tk.Frame(wrap, bg=PALETTE["bg"])
            title_row.pack(fill=tk.X, pady=(0, 5))
            tk.Label(title_row, text=title,
                     font=F_HEAD,
                     bg=PALETTE["bg"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT)
            # 제목 옆 구분선
            tk.Frame(title_row, bg=PALETTE["border"], height=1
                     ).pack(side=tk.LEFT, fill=tk.X, expand=True,
                            padx=(10, 0), pady=6)
            card = tk.Frame(wrap, bg=PALETTE["card"],
                            highlightbackground=PALETTE["border2"],
                            highlightthickness=1)
            card.pack(fill=tk.X)
            return card

        def row(parent, label: str, widget_fn):
            r = tk.Frame(parent, bg=PALETTE["card"])
            r.pack(fill=tk.X, padx=14, pady=6)
            tk.Label(r, text=label, width=15, anchor=tk.W,
                     font=F_LABEL,
                     bg=PALETTE["card"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT)
            widget_fn(r)
            return r

        # ════════════════════════════════════════════════════
        # 섹션 1 : 기본 정보
        # ════════════════════════════════════════════════════
        s1 = section("📌 기본 정보")

        # 템플릿명
        self._name_var = tk.StringVar(
            value=self._cur("name", "새 템플릿"))
        def _name_w(p):
            tk.Entry(p, textvariable=self._name_var,
                     bg=PALETTE["bg"], fg=PALETTE["text"],
                     insertbackground=PALETTE["text"],
                     relief=tk.FLAT, font=F_BODY,
                     width=28).pack(side=tk.LEFT)
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
        # 저장 버튼
        # ════════════════════════════════════════════════════
        save_row = tk.Frame(self._edit_inner, bg=PALETTE["bg"])
        save_row.pack(fill=tk.X, padx=16, pady=(4, 20))
        tk.Button(save_row, text="💾  템플릿 저장",
                  command=self._save_template,
                  bg=PALETTE["primary"], fg="#FFFFFF",
                  relief=tk.FLAT,
                  font=F_BTN,
                  activebackground=_lighten(PALETTE["primary"]),
                  cursor="hand2", padx=20, pady=8
                  ).pack(side=tk.LEFT)

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
                     width=14, anchor=tk.W,
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
        tk.Label(r, text="CSV 파일", width=14, anchor=tk.W,
                 font=F_LABEL,
                 bg=PALETTE["card"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        self._tgt_path_var = tk.StringVar(
            value=self._cur("target_file", ""))
        tk.Entry(r, textvariable=self._tgt_path_var,
                 bg=PALETTE["bg"], fg=PALETTE["text"],
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
                 width=14, anchor=tk.W,
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
        except Exception as e:
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
            messagebox.showinfo(
                "예시 파일 저장 완료",
                f"저장 위치:\n{save_path}\n\n{data['hint']}"
            )
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
        tk.Label(wrap, text="💬 메시지",
                 font=F_HEAD,
                 bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(anchor=tk.W, pady=(0, 6))
        card = tk.Frame(wrap, bg=PALETTE["card"],
                        highlightbackground=PALETTE["border"],
                        highlightthickness=1)
        card.pack(fill=tk.X)

        msg_frame = tk.Frame(card, bg=PALETTE["card"])
        msg_frame.pack(fill=tk.X, padx=12, pady=8)
        tk.Label(msg_frame, text="메시지 내용",
                 width=14, anchor=tk.W,
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

        tk.Label(self._img_section_wrap,
                 text="🖼️ 이미지 첨부 설정",
                 font=F_HEAD,
                 bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(anchor=tk.W, pady=(0, 6))

        card = tk.Frame(self._img_section_wrap,
                        bg=PALETTE["card"],
                        highlightbackground=PALETTE["border"],
                        highlightthickness=1)
        card.pack(fill=tk.X)

        # ── 이미지 사용 여부 토글 ──────────────────────────
        img_row = tk.Frame(card, bg=PALETTE["card"])
        img_row.pack(fill=tk.X, padx=12, pady=8)
        tk.Label(img_row, text="이미지 첨부",
                 width=14, anchor=tk.W,
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
                 width=14, anchor=tk.W,
                 font=F_LABEL,
                 bg=PALETTE["card"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        # 텔레그램: none/clipboard/file
        # 카카오:   file/dragdrop
        _wk_now = self._wtype_var.get()
        _is_tg  = _wk_now == "telegram_message"
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
                              ("dragdrop","🖱️ 드래그앤드롭")]
        for val, lbl in _img_mode_opts:
            tk.Radiobutton(
                self._img_mode_row, text=lbl,
                variable=self._img_mode_var,
                value=val,
                bg=PALETTE["card"], fg=PALETTE["text"],
                selectcolor=PALETTE["active"],
                activebackground=PALETTE["card"],
                font=F_LABEL,
                command=self._toggle_image_path,
            ).pack(side=tk.LEFT, padx=(0, 20))

        # ── 텔레그램 전용: 파일첨부 버튼 좌표 ──────────────────
        # 파일경로 모드일 때만 표시 (_toggle_image_path 에서 제어)
        if _is_tg:
            self._tg_attach_row = tk.Frame(card, bg=PALETTE["card"])
            # 초기에는 숨김 (pack 안 함) — _toggle_image_path 에서 표시
            tk.Label(self._tg_attach_row, text="첨부버튼 좌표",
                     width=14, anchor=tk.W,
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
                         width=6, bg=PALETTE["bg"], fg=PALETTE["text"],
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
                     text=" ← 파일경로 모드 시 필수",
                     font=F_SMALL, bg=PALETTE["card"],
                     fg=PALETTE["warning_text"]
                     ).pack(side=tk.LEFT, padx=(4, 0))

            # ── 텔레그램 전용: 파일명 입력란 좌표 ──────────────
            self._tg_filename_row = tk.Frame(card, bg=PALETTE["card"])
            # 초기에는 숨김 (_toggle_image_path 에서 표시)
            tk.Label(self._tg_filename_row, text="파일명입력 좌표",
                     width=14, anchor=tk.W,
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
                         width=6, bg=PALETTE["bg"], fg=PALETTE["text"],
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
                     text=" ← 파일명 입력란 클릭 좌표",
                     font=F_SMALL, bg=PALETTE["card"],
                     fg=PALETTE["warning_text"]
                     ).pack(side=tk.LEFT, padx=(4, 0))

        # ── 이미지 파일 경로 (파일경로 방식) ──────────────────
        self._img_path_row = tk.Frame(card, bg=PALETTE["card"])
        # pack 여부는 _toggle_image_path 가 결정 (초기 pack 제거)
        tk.Label(self._img_path_row, text="이미지 경로",
                 width=14, anchor=tk.W,
                 font=F_LABEL,
                 bg=PALETTE["card"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        self._img_path_var = tk.StringVar(
            value=self._cur("image_path", ""))
        tk.Entry(self._img_path_row,
                 textvariable=self._img_path_var,
                 bg=PALETTE["bg"], fg=PALETTE["text"],
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
                 width=14, anchor=tk.W,
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
                 width=14, anchor=tk.W,
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
                     width=6, bg=PALETTE["bg"], fg=PALETTE["text"],
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
                 width=14, anchor=tk.W,
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
                     width=6, bg=PALETTE["bg"], fg=PALETTE["text"],
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
                     width=5, bg=PALETTE["bg"], fg=PALETTE["text"],
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
                     width=5, bg=PALETTE["bg"], fg=PALETTE["text"],
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
                     width=5, bg=PALETTE["bg"], fg=PALETTE["text"],
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
        show_tg_file = use and mode == "file"
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

        tk.Label(self._coord_section_wrap,
                 text="🖱️ 좌표 설정",
                 font=F_HEAD,
                 bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(anchor=tk.W, pady=(0, 6))
        tk.Label(self._coord_section_wrap,
                 text="📸 캡처 버튼 클릭 → 3초 후 마우스 위치 저장  "
                      "/ 영역은 드래그로 지정",
                 font=F_SMALL,
                 bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(anchor=tk.W, pady=(0, 6))

        card = tk.Frame(self._coord_section_wrap,
                        bg=PALETTE["card"],
                        highlightbackground=PALETTE["border"],
                        highlightthickness=1)
        card.pack(fill=tk.X)

        for i, (key, label, ctype) in enumerate(
                zip(keys, labels, types)):
            sv = saved.get(key, {})
            self._build_coord_row(card, i, key, label, ctype, sv)

    def _build_coord_row(self, parent, idx, key, label, ctype, saved):
        r = tk.Frame(parent, bg=PALETTE["card"])
        r.pack(fill=tk.X, padx=12, pady=5)

        # 라벨
        tk.Label(r, text=label, width=18, anchor=tk.W,
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
                         bg=PALETTE["bg"], fg=PALETTE["text"],
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
                         bg=PALETTE["bg"], fg=PALETTE["text"],
                         insertbackground=PALETTE["text"],
                         relief=tk.FLAT,
                         font=F_MONO
                         ).pack(side=tk.LEFT)
            # 현재 좌표 표시 라벨
            disp = tk.Label(r, text="",
                            font=F_MONO_S,
                            bg=PALETTE["card"],
                            fg=PALETTE["success_text"])
            disp.pack(side=tk.LEFT, padx=(6, 0))
            tk.Button(r, text="📸 캡처",
                      command=lambda k=key, x=xv, y=yv, d=disp:
                          self._capture_point(k, x, y, d),
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
                tk.Label(r, text=label, width=14, anchor=tk.W,
                         font=F_LABEL,
                         bg=PALETTE["card"], fg=PALETTE["text"]
                         ).pack(side=tk.LEFT)
                widget_fn(r)

            # 키워드
            def _kw_w(p):
                self._id_keyword_var = tk.StringVar(
                    value=self._cur("id_keyword", "가망"))
                e = tk.Entry(p, textvariable=self._id_keyword_var,
                             bg=PALETTE["bg"], fg=PALETTE["text"],
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
                         bg=PALETTE["bg"], fg=PALETTE["text"],
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
                           bg=PALETTE["bg"], fg=PALETTE["text"],
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
            tk.Label(prev_row, text="미리보기", width=14, anchor=tk.W,
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

        # ─ 섹션 제목 & 카드 헬퍼 ─────────────────────────
        def _make_card():
            tk.Label(self._timing_section_wrap,
                     text="⏱️ 딜레이 설정",
                     font=F_HEAD,
                     bg=PALETTE["bg"], fg=PALETTE["text"]
                     ).pack(anchor=tk.W, pady=(0, 6))
            card = tk.Frame(self._timing_section_wrap,
                            bg=PALETTE["card"],
                            highlightbackground=PALETTE["border"],
                            highlightthickness=1)
            card.pack(fill=tk.X)
            return card

        def _row(parent):
            r = tk.Frame(parent, bg=PALETTE["card"])
            r.pack(fill=tk.X, padx=12, pady=(8, 4))
            return r

        def _field(row, label, var, width=6):
            tk.Label(row, text=label, font=F_SMALL,
                     bg=PALETTE["card"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT, padx=(10, 2))
            tk.Entry(row, textvariable=var, width=width,
                     bg=PALETTE["bg"], fg=PALETTE["text"],
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
                         bg=PALETTE["bg"], fg=PALETTE["text"],
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
                     bg=PALETTE["bg"], fg=PALETTE["text"],
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
            tk.Label(r1, text="단계 타이밍", width=14, anchor=tk.W,
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
            tk.Label(r2, text="", width=14, anchor=tk.W,
                     font=F_LABEL, bg=PALETTE["card"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT)
            for lbl_t, var in [
                ("색판별대기(s)", self._kf_after_color_wait),
                ("Tab 후(s)",     self._kf_after_tab),
            ]:
                _field(r2, lbl_t, var)
            # 행3: 간격/지터 (kakao_friend 전용 변수명 사용)
            r3 = _row(card)
            tk.Label(r3, text="ID 간격", width=14, anchor=tk.W,
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
        # 텔레그램 : 원본 v2 딜레이 8개
        # ════════════════════════════════════════════════
        elif wk in ("telegram_join", "telegram_message"):
            card = _make_card()
            # 행1: 로딩/전환
            r1 = _row(card)
            tk.Label(r1, text="로딩 대기", width=14, anchor=tk.W,
                     font=F_LABEL, bg=PALETTE["card"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT)
            self._tg_chrome_load   = tk.StringVar(value=str(self._cur("tg_chrome_load",    2.0)))
            self._tg_tg_open       = tk.StringVar(value=str(self._cur("tg_telegram_open",  1.5)))
            self._tg_join_click    = tk.StringVar(value=str(self._cur("tg_join_click",     2.0)))
            for lbl_t, var in [
                ("Chrome(s)",   self._tg_chrome_load),
                ("앱전환(s)",   self._tg_tg_open),
                ("가입클릭(s)", self._tg_join_click),
            ]:
                _field(r1, lbl_t, var)
            # 행2: 메시지 관련
            r2 = _row(card)
            tk.Label(r2, text="메시지 딜레이", width=14, anchor=tk.W,
                     font=F_LABEL, bg=PALETTE["card"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT)
            self._tg_after_type  = tk.StringVar(value=str(self._cur("tg_after_type",  0.5)))
            self._tg_after_send  = tk.StringVar(value=str(self._cur("tg_after_send",  1.0)))
            self._tg_after_back  = tk.StringVar(value=str(self._cur("tg_after_back",  0.8)))
            for lbl_t, var in [
                ("타이핑 후(s)", self._tg_after_type),
                ("전송 후(s)",   self._tg_after_send),
                ("뒤로가기(s)",  self._tg_after_back),
            ]:
                _field(r2, lbl_t, var)
            # 행3: 링크 간격
            r3 = _row(card)
            tk.Label(r3, text="링크 간격", width=14, anchor=tk.W,
                     font=F_LABEL, bg=PALETTE["card"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT)
            self._tg_between_min = tk.StringVar(value=str(self._cur("tg_between_min", 3.0)))
            self._tg_between_max = tk.StringVar(value=str(self._cur("tg_between_max", 7.0)))
            for lbl_t, var in [
                ("최소(s)", self._tg_between_min),
                ("최대(s)", self._tg_between_max),
            ]:
                _field(r3, lbl_t, var)
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
        tk.Label(r0, text="시작 좌표", width=14, anchor=tk.W,
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
                     bg=PALETTE["bg"], fg=PALETTE["text"],
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
        tk.Label(r1, text="1칸 크기", width=14, anchor=tk.W,
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
                     bg=PALETTE["bg"], fg=PALETTE["text"],
                     insertbackground=PALETTE["text"],
                     relief=tk.FLAT, font=F_MONO
                     ).pack(side=tk.LEFT)
        tk.Label(r1, text="px", font=F_SMALL,
                 bg=PALETTE["card"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT, padx=(4, 0))

        # ── 구성 (열·행) ──────────────────────────────────── v1.52
        r2 = tk.Frame(card, bg=PALETTE["card"])
        r2.pack(fill=tk.X, padx=12, pady=4)
        tk.Label(r2, text="구성", width=14, anchor=tk.W,
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
                     bg=PALETTE["bg"], fg=PALETTE["text"],
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
        tk.Label(r3, text="방향", width=14, anchor=tk.W,
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
        tk.Label(r4, text="미리보기", width=14, anchor=tk.W,
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
            tk.Label(r, text=label, width=14, anchor=tk.W,
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
        _is_tg_sc = wk == "telegram_message"

        if not _is_tg_sc:
            # ── 카카오 전용: 바로입력 / 좌표클릭 ──────────────
            self._input_method_var = tk.StringVar(
                value=self._cur("input_method", "direct"))

            self._sc_mi_x = tk.StringVar(
                value=str(self._cur("message_input_coord", {}).get("x", 0)))
            self._sc_mi_y = tk.StringVar(
                value=str(self._cur("message_input_coord", {}).get("y", 0)))

            r_mi_coord = tk.Frame(card, bg=PALETTE["card"])
            tk.Label(r_mi_coord, text="입력창 좌표", width=14, anchor=tk.W,
                     font=F_LABEL, bg=PALETTE["card"],
                     fg=PALETTE["accent"]).pack(side=tk.LEFT)
            for lbl_t, var in [("X:", self._sc_mi_x), ("Y:", self._sc_mi_y)]:
                tk.Label(r_mi_coord, text=lbl_t, font=F_MONO_S,
                         bg=PALETTE["card"], fg=PALETTE["text"]
                         ).pack(side=tk.LEFT, padx=(4, 0))
                tk.Entry(r_mi_coord, textvariable=var, width=6,
                         bg=PALETTE["bg"], fg=PALETTE["text"],
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
            tk.Label(r_tg_mi, text="입력창 좌표", width=14, anchor=tk.W,
                     font=F_LABEL, bg=PALETTE["card"],
                     fg=PALETTE["accent"]).pack(side=tk.LEFT)
            for lbl_t, var in [("X:", self._tg_mi_x), ("Y:", self._tg_mi_y)]:
                tk.Label(r_tg_mi, text=lbl_t, font=F_MONO_S,
                         bg=PALETTE["card"], fg=PALETTE["text"]
                         ).pack(side=tk.LEFT, padx=(4, 0))
                tk.Entry(r_tg_mi, textvariable=var, width=6,
                         bg=PALETTE["bg"], fg=PALETTE["text"],
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
        tk.Label(r_sbtn, text="전송버튼 좌표", width=14, anchor=tk.W,
                 font=F_LABEL, bg=PALETTE["card"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        for lbl_t, var in [("X:", self._sc_send_btn_x),
                            ("Y:", self._sc_send_btn_y)]:
            tk.Label(r_sbtn, text=lbl_t, font=F_MONO_S,
                     bg=PALETTE["card"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT, padx=(4, 0))
            tk.Entry(r_sbtn, textvariable=var, width=6,
                     bg=PALETTE["bg"], fg=PALETTE["text"],
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
        tk.Label(r_cbtn, text="닫기버튼 좌표", width=14, anchor=tk.W,
                 font=F_LABEL, bg=PALETTE["card"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        for lbl_t, var in [("X:", self._sc_close_btn_x),
                            ("Y:", self._sc_close_btn_y)]:
            tk.Label(r_cbtn, text=lbl_t, font=F_MONO_S,
                     bg=PALETTE["card"], fg=PALETTE["text"]
                     ).pack(side=tk.LEFT, padx=(4, 0))
            tk.Entry(r_cbtn, textvariable=var, width=6,
                     bg=PALETTE["bg"], fg=PALETTE["text"],
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
        if wk == "telegram_message":
            sep()

            # join_first 체크박스
            self._join_first_var = tk.BooleanVar(
                value=self._cur("join_first", False))

            # join_btn 좌표 행 (join_first=True 시만 표시)
            self._tg_jb_x = tk.StringVar(
                value=str(self._cur("join_btn_coord", {}).get("x", 0)))
            self._tg_jb_y = tk.StringVar(
                value=str(self._cur("join_btn_coord", {}).get("y", 0)))

            r_jb = tk.Frame(card, bg=PALETTE["card"])
            tk.Label(r_jb, text="가입버튼 좌표", width=14, anchor=tk.W,
                     font=F_LABEL, bg=PALETTE["card"],
                     fg=PALETTE["accent"]).pack(side=tk.LEFT)
            for lbl_t, var in [("X:", self._tg_jb_x), ("Y:", self._tg_jb_y)]:
                tk.Label(r_jb, text=lbl_t, font=F_MONO_S,
                         bg=PALETTE["card"], fg=PALETTE["text"]
                         ).pack(side=tk.LEFT, padx=(4, 0))
                tk.Entry(r_jb, textvariable=var, width=6,
                         bg=PALETTE["bg"], fg=PALETTE["text"],
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

            def _join_first_w(p):
                tk.Checkbutton(p, text="✅ 가입 후 발송",
                               variable=self._join_first_var,
                               command=_toggle_jb_coord,
                               bg=PALETTE["card"], fg=PALETTE["text"],
                               selectcolor=PALETTE["active"],
                               activebackground=PALETTE["card"],
                               font=F_LABEL,
                               ).pack(side=tk.LEFT)
                tk.Label(p, text="(그룹 링크 열고 가입 버튼 클릭 후 메시지 발송)",
                         font=F_SMALL, bg=PALETTE["card"],
                         fg=PALETTE["muted"]
                         ).pack(side=tk.LEFT, padx=(6, 0))
            row("가입 옵션", _join_first_w)
            _toggle_jb_coord()  # 초기 상태 반영

    # ── 좌표 캡처 — 포인트 ──────────────────────────────────
    def _capture_point(self, key, xv, yv, disp_lbl):
        """3초 카운트다운 후 마우스 좌표 캡처 (오버레이 없음)"""
        if not HAS_PYAUTOGUI:
            messagebox.showwarning("패키지 없음",
                "pyautogui 가 설치되지 않았습니다.")
            return

        def _do_capture():
            for i in range(3, 0, -1):
                self.app._set_status(f"⏳ [{key}] {i}초 후 캡처…")
                import time as _t; _t.sleep(1)
            try:
                x, y = pyautogui.position()
                xv.set(str(x)); yv.set(str(y))
                if disp_lbl:
                    disp_lbl.config(text=f"({x}, {y})")
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
            # ▶ 텔레그램 계열 딜레이 저장
            if hasattr(self, "_tg_chrome_load"):
                data["tg_chrome_load"]   = safe_float(self._tg_chrome_load.get(),   2.0)
                data["tg_telegram_open"] = safe_float(self._tg_tg_open.get(),       1.5)
                data["tg_join_click"]    = safe_float(self._tg_join_click.get(),    2.0)
                data["tg_after_type"]    = safe_float(self._tg_after_type.get(),    0.5)
                data["tg_after_send"]    = safe_float(self._tg_after_send.get(),    1.0)
                data["tg_after_back"]    = safe_float(self._tg_after_back.get(),    0.8)
                data["tg_between_min"]   = safe_float(self._tg_between_min.get(),   3.0)
                data["tg_between_max"]   = safe_float(self._tg_between_max.get(),   7.0)
            # ▶ 텔레그램 전송/닫기 방식 저장 (메시지 계열)
            if wk == "telegram_message":
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
            wk   = t.get("workflow", "")
            wdef = PLATFORM_WORKFLOWS.get(wk, {})
            icon = "🟡" if plat == "kakao" else "🔵"
            self._tmpl_lb.insert(
                tk.END,
                f"{icon} {t.get('name','?')}  [{wdef.get('name','')}]")

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
        self.after(3000, lambda: _check_update_on_start(self))  # v1.60 자동업데이터
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
        # 타이틀 행
        hdr = tk.Frame(self, bg=PALETTE["bg"])
        hdr.pack(fill=tk.X, pady=(0, 10))
        tk.Label(hdr, text="📋  작업 관리",
                 font=F_TITLE,
                 bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        tk.Label(hdr,
                 text="템플릿을 선택하고 스케줄을 설정해 작업을 실행합니다",
                 font=F_LABEL,
                 bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT, padx=(16, 0))
        tk.Button(hdr, text="❓ 도움말",
                  command=self._show_help,
                  bg=PALETTE["hover"], fg=PALETTE["text"],
                  relief=tk.FLAT, font=F_SMALL,
                  cursor="hand2", padx=10, pady=4, bd=0,
                  activebackground=PALETTE["active"],
                  activeforeground=PALETTE["text"],
                  ).pack(side=tk.RIGHT)

        # 툴바
        tb = tk.Frame(self, bg=PALETTE["bg"])
        tb.pack(fill=tk.X, pady=(0, 8))
        btns = [
            ("＋ 작업 추가",  self._add_job,    PALETTE["primary"], PALETTE["bg"]),
            ("✎ 수정",        self._edit_job,   PALETTE["hover"],   PALETTE["text"]),
            ("⧉ 복제",        self._dup_job,    PALETTE["hover"],   PALETTE["text2"]),
            ("✕ 삭제",        self._del_job,    PALETTE["danger"],  PALETTE["text"]),
        ]
        for txt, cmd, bg, fg in btns:
            tk.Button(tb, text=txt, command=cmd,
                      bg=bg, fg=fg,
                      relief=tk.FLAT,
                      font=F_BTN_S,
                      activebackground=_lighten(bg, 0.1),
                      activeforeground=fg,
                      cursor="hand2", padx=14, pady=6, bd=0,
                      ).pack(side=tk.LEFT, padx=(0, 4))

        # 실행 버튼 (우측)
        tk.Button(tb, text="▶▶ 전체 실행",
                  command=self._run_all,
                  bg=PALETTE["success"], fg=PALETTE["text"],
                  relief=tk.FLAT, font=F_BTN,
                  cursor="hand2", padx=16, pady=6, bd=0,
                  activebackground=_lighten(PALETTE["success"], 0.1),
                  activeforeground=PALETTE["bg"],
                  ).pack(side=tk.RIGHT, padx=(4, 0))
        tk.Button(tb, text="▶ 선택 실행",
                  command=self._run_selected,
                  bg=PALETTE["primary"], fg="#FFFFFF",
                  relief=tk.FLAT, font=F_BTN,
                  cursor="hand2", padx=16, pady=6, bd=0,
                  activebackground=PALETTE["primary2"],
                  activeforeground=PALETTE["bg"],
                  ).pack(side=tk.RIGHT, padx=(4, 0))
        tk.Button(tb, text="⏹ 중지",
                  command=lambda: (  # v1.54 CHANGE-18: 선택 시 개별 중지
                      self._stop_job(self._get_selected_job())
                      if self._get_selected_job()
                      else self._stop_all()),
                  bg=PALETTE["danger"], fg="#FFFFFF",
                  relief=tk.FLAT, font=F_BTN_S,
                  cursor="hand2", padx=12, pady=6, bd=0,
                  ).pack(side=tk.RIGHT, padx=(4, 0))

        # ── v1.55 CHANGE-A1: 활성 토글 버튼 ─────────────────────────────
        # 이전(v1.54): 활성/비활성 토글 기능 없음 (모든 작업 항상 실행 대상)
        # 변경(v1.55): 선택 작업의 enabled 플래그를 즉시 전환 후 JSON 저장
        tk.Frame(tb, bg=PALETTE["border2"], width=1, height=28
                 ).pack(side=tk.LEFT, padx=(6, 6), fill=tk.Y)
        tk.Button(tb, text="⊙ 활성 토글",
                  command=self._toggle_job,
                  bg="#64748B", fg="#FFFFFF",
                  relief=tk.FLAT, font=F_BTN_S,
                  cursor="hand2", padx=12, pady=6, bd=0,
                  activebackground="#475569",
                  activeforeground="#FFFFFF",
                  ).pack(side=tk.LEFT, padx=(0, 4))

        # ── v1.55 CHANGE-B: 인라인 안내 카드 ────────────────────────────
        # 이전(v1.54): ❓ 도움말 버튼 클릭 시만 안내 확인 가능
        # 변경(v1.55): Treeview 위에 항상 노출되는 파란 안내 카드 삽입
        #   배색: bg #EFF6FF / border #BFDBFE / text #1D4ED8
        #   (community_poster v5.20 팁 카드 배색 벤치마킹)
        tip_frame = tk.Frame(self,
                             bg="#EFF6FF",
                             highlightbackground="#BFDBFE",
                             highlightthickness=1)
        tip_frame.pack(fill=tk.X, pady=(0, 6))
        tk.Label(tip_frame,
                 text=("💡  작업 관리란?  "
                       "각 작업 = 템플릿 1개 + 대상 목록 조합입니다.  "
                       "⊙ 활성 토글로 특정 작업만 일시 비활성화할 수 있습니다."),
                 font=F_SMALL,
                 bg="#EFF6FF", fg="#1D4ED8",
                 anchor=tk.W, padx=12, pady=6,
                 ).pack(fill=tk.X)

        # ── 작업 목록 Treeview ──────────────────────────────
        tv_frame = tk.Frame(self, bg=PALETTE["bg"])
        tv_frame.pack(fill=tk.BOTH, expand=True)

        # ── v1.55 CHANGE-A2: "active" 컬럼 추가 ────────────────────────
        # 이전(v1.54): 6개 컬럼 (name/template/platform/workflow/schedule/status)
        # 변경(v1.55): 7번째 "active" 컬럼 추가 → ✓ 활성 / ✗ 비활성 표시
        cols = ("name", "template", "platform", "workflow",
                "schedule", "status", "active")
        self._tv = ttk.Treeview(
            tv_frame, columns=cols,
            show="headings", height=14)

        headers = [
            ("name",     "작업명",   160),
            ("template", "템플릿명", 160),
            ("platform", "플랫폼",    80),
            ("workflow", "작업유형", 150),
            ("schedule", "스케줄",   130),
            ("status",   "상태",      90),
            ("active",   "활성",      60),   # v1.55 신규
        ]
        for col, hd, w in headers:
            self._tv.heading(col, text=hd)
            self._tv.column(col, width=w,
                            anchor=tk.CENTER, stretch=False)

        # Treeview 스타일
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background=PALETTE["card"],
                        foreground=PALETTE["text"],
                        rowheight=32,
                        fieldbackground=PALETTE["card"],
                        borderwidth=0,
                        font=F_LABEL)
        style.configure("Treeview.Heading",
                        background=PALETTE["sidebar"],
                        foreground=PALETTE["sidebar_text"],
                        relief="flat",
                        font=F_SMALL,
                        padding=(6, 6))
        style.map("Treeview",
                  background=[("selected", PALETTE["selected"])],
                  foreground=[("selected", PALETTE["text"])])
        style.layout("Treeview", [
            ("Treeview.treearea", {"sticky": "nswe"})])

        # ── v1.55 CHANGE-A3: 비활성 행 태그 색상 등록 ───────────────────
        # 이전(v1.54): 태그 없음 (모든 행 동일 색상)
        # 변경(v1.55): disabled 태그 → foreground muted(#475569) + bg #F8F9FA
        #              enabled  태그 → 기본 색상 (명시적 정의)
        self._tv.tag_configure("disabled",
                               foreground=PALETTE["muted"],
                               background="#F8F9FA")
        self._tv.tag_configure("enabled",
                               foreground=PALETTE["text"],
                               background=PALETTE["card"])

        tv_sb = ttk.Scrollbar(tv_frame, orient=tk.VERTICAL,
                              command=self._tv.yview)
        self._tv.configure(yscrollcommand=tv_sb.set)
        tv_sb.pack(side=tk.RIGHT, fill=tk.Y)
        self._tv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._tv.bind("<Double-1>", lambda e: self._edit_job())

        # ── 진행 상태 바 ────────────────────────────────────
        prog_outer = tk.Frame(self, bg=PALETTE["sidebar"],
                              highlightbackground=PALETTE["border"],
                              highlightthickness=1)
        prog_outer.pack(fill=tk.X, pady=(10, 0))
        prog_frame = tk.Frame(prog_outer, bg=PALETTE["sidebar"])
        prog_frame.pack(fill=tk.X, padx=10, pady=6)

        self._prog_var   = tk.DoubleVar(value=0)
        self._prog_label = tk.StringVar(value="⏳ 대기 중")

        tk.Label(prog_frame, textvariable=self._prog_label,
                 font=F_SMALL,
                 bg=PALETTE["sidebar"], fg=PALETTE["sidebar_text"],
                 width=16, anchor=tk.W,
                 ).pack(side=tk.LEFT, padx=(0, 8))

        style2 = ttk.Style()
        style2.configure("Green.Horizontal.TProgressbar",
                         troughcolor=PALETTE["card"],
                         background=PALETTE["success"],
                         bordercolor=PALETTE["border"],
                         lightcolor=PALETTE["success"],
                         darkcolor=PALETTE["success"])
        prog_bar = ttk.Progressbar(
            prog_frame, variable=self._prog_var,
            maximum=100, mode="determinate",
            style="Green.Horizontal.TProgressbar")
        prog_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 성공/실패 카운터
        self._succ_var = tk.StringVar(value="✅ 0")
        self._fail_var = tk.StringVar(value="❌ 0")
        tk.Label(prog_frame, textvariable=self._succ_var,
                 font=F_BTN,
                 bg=PALETTE["sidebar"],
                 fg=PALETTE["success"]
                 ).pack(side=tk.LEFT, padx=(14, 4))
        tk.Label(prog_frame, textvariable=self._fail_var,
                 font=F_BTN,
                 bg=PALETTE["sidebar"],
                 fg=PALETTE["danger"]
                 ).pack(side=tk.LEFT)

        # ── v1.60 STEP-5: ETA 패널 (예상 소요시간 / 예상 완료시각) ─────────────
        eta_outer = tk.Frame(self, bg=PALETTE["sidebar"],
                             highlightbackground=PALETTE["border"],
                             highlightthickness=1)
        eta_outer.pack(fill=tk.X, pady=(4, 0))
        eta_frame = tk.Frame(eta_outer, bg=PALETTE["sidebar"])
        eta_frame.pack(fill=tk.X, padx=10, pady=4)

        self._eta_total_var  = tk.StringVar(value="⏱ 예상 소요: -")
        self._eta_finish_var = tk.StringVar(value="🏁 예상 완료: -")

        tk.Label(eta_frame, textvariable=self._eta_total_var,
                 font=F_SMALL, bg=PALETTE["sidebar"],
                 fg=PALETTE["sidebar_text"], anchor=tk.W
                 ).pack(side=tk.LEFT, padx=(0, 16))
        tk.Label(eta_frame, textvariable=self._eta_finish_var,
                 font=F_SMALL, bg=PALETTE["sidebar"],
                 fg=PALETTE["sidebar_text"], anchor=tk.W
                 ).pack(side=tk.LEFT)
        self._eta_refresh_btn = tk.Button(
            eta_frame, text="↻",
            font=F_SMALL, bg=PALETTE["sidebar"],
            fg=PALETTE["accent"],
            bd=0, cursor="hand2",
            command=self._refresh_time_estimate)
        self._eta_refresh_btn.pack(side=tk.RIGHT, padx=(0, 4))
        # ────────────────────────────────────────────────────────

    # ── 작업 로드/저장 ───────────────────────────────────────
    def _refresh_time_estimate(self):
        """v1.60 STEP-6: ETA 패널 갱신 — 전체 소요시간 / 예상 완료시각 계산"""
        from datetime import datetime as _dt_ref
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

    def _refresh_tv(self):
        self._tv.delete(*self._tv.get_children())
        for j in self._jobs:
            wk    = j.get("workflow", "")
            wdef  = PLATFORM_WORKFLOWS.get(wk, {})
            plat  = j.get("platform", "")
            icon  = "🟡 카카오" if plat == "kakao" else "🔵 텔레그램"
            sched = j.get("schedule_label", "없음")
            stat  = j.get("_status", "대기")
            # ── v1.55 CHANGE-A4: enabled 상태 반영 ──────────────────────
            # 이전(v1.54): values 6개, 태그 없음
            # 변경(v1.55): values 7번째 act_txt 추가 + row_tag 적용
            #   enabled=True  → "✓ 활성"  + tag "enabled"  (기본색)
            #   enabled=False → "✗ 비활성" + tag "disabled" (muted 회색)
            #   기존 JSON에 enabled 키 없으면 True 폴백 (하위 호환)
            enabled  = j.get("enabled", True)
            act_txt  = "✓ 활성" if enabled else "✗ 비활성"
            row_tag  = "enabled" if enabled else "disabled"
            self._tv.insert("", tk.END, iid=j.get("name"),
                values=(j.get("name", ""),
                        j.get("template_name", ""),
                        icon,
                        wdef.get("name", ""),
                        sched, stat,
                        act_txt),       # ← 7번째 값 (v1.55 신규)
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
        if save_json(JOBS_DIR / fname, data):
            self.app._set_status(
                f"✅ 작업 [{data['name']}] 저장")
            self._load_jobs()
            # v1.58 CHANGE-X9: 저장 후 스케줄러 재시작
            if hasattr(self, "_restart_scheduler"):
                self._restart_scheduler()
            self.after(0, self._refresh_time_estimate)  # v1.60 P-17
        else:
            messagebox.showerror("저장 실패",
                "작업 저장 중 오류가 발생했습니다.")

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
    def set_progress(self, val, label=""):
        self._prog_var.set(val)
        if label: self._prog_label.set(label)
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
        self._build()
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

        p = {"padx": 20, "pady": 6}

        def section(title):
            title_fr = tk.Frame(inner, bg=PALETTE["bg"])
            title_fr.pack(fill=tk.X, padx=20, pady=(16, 5))
            tk.Label(title_fr, text=title,
                     font=F_HEAD,
                     bg=PALETTE["bg"],
                     fg=PALETTE["text"]
                     ).pack(side=tk.LEFT)
            tk.Frame(title_fr, bg=PALETTE["border"], height=1
                     ).pack(side=tk.LEFT, fill=tk.X, expand=True,
                            padx=(10, 0), pady=7)
            f = tk.Frame(inner, bg=PALETTE["card"],
                         highlightbackground=PALETTE["border2"],
                         highlightthickness=1)
            f.pack(fill=tk.X, padx=20, pady=(0, 4))
            return f

        def row(parent, label, widget_fn):
            r = tk.Frame(parent, bg=PALETTE["card"])
            r.pack(fill=tk.X, padx=14, pady=7)
            tk.Label(r, text=label, width=14, anchor=tk.W,
                     font=F_LABEL,
                     bg=PALETTE["card"],
                     fg=PALETTE["text"]
                     ).pack(side=tk.LEFT)
            widget_fn(r)

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

        self._build_schedule_section(inner, row, section)

        # ── 저장 버튼 ───────────────────────────────────────
        tk.Button(inner, text="💾  저장",
                  command=self._ok,
                  bg=PALETTE["primary"], fg="#FFFFFF",
                  relief=tk.FLAT,
                  font=F_BTN,
                  cursor="hand2", padx=32, pady=10, bd=0,
                  activebackground=PALETTE["primary2"],
                  activeforeground=PALETTE["bg"],
                  ).pack(pady=(18, 24))
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
                 width=14, anchor=tk.W,
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
        name = self._jname_var.get().strip()
        if not name:
            messagebox.showwarning("입력 오류",
                "작업명을 입력하세요.")
            return
        tmpl_name = self._tmpl_var.get().strip()
        if not tmpl_name:
            messagebox.showwarning("입력 오류",
                "작업 템플릿을 선택하세요.")
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
            days = [i for i, v in enumerate(self._sched_day_vars) if v.get()]
        elif hasattr(self, "_sched_days"):
            days = [_KR_TO_INT[d] for d, var in self._sched_days.items()
                    if var.get() and d in _KR_TO_INT]
        else:
            days = list(DEFAULT_SCHEDULE["days"])
        # 하위호환 KR 리스트
        sched_days = [_DAY_LABELS_OK[i] for i in days]

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

        # ── 스케줄 ON 시 입력 유효성 검사 (BUG-03, BUG-04, EDGE-04) ─────────────
        if sched_on:
            if invalid_times:
                messagebox.showwarning("시각 형식 오류",
                    f"올바르지 않은 시각 형식이 있습니다:\n"
                    f"{', '.join(invalid_times)}\n\n"
                    f"HH:MM 형식으로 입력하세요. (예: 09:00, 14:00)")
                return
            if sched_mode == "time" and not sched_times:
                messagebox.showwarning("시각 미입력",
                    "실행 시각을 1개 이상 입력하세요.\n"
                    "예: 09:00  또는  09:00, 14:00, 19:00")
                return
            if not days:
                messagebox.showwarning("요일 미선택",
                    "실행 요일을 1개 이상 선택하세요.")
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
        self.wk         = job.get("workflow",
                          template.get("workflow", ""))
        self.coords     = template.get("coords", {})
        self._log       = log_fn      or (lambda m, l="INFO": None)
        self._progress  = progress_fn or (lambda c, t: None)
        self._done      = done_fn     or (lambda s, f: None)
        self._stop      = stop_event  or threading.Event()
        self._succ      = 0
        self._fail      = 0
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
        elif wk in ("telegram_join", "telegram_message"):
            for line in lines:
                rows.append({"이름": "", "텔레그램링크": line})
        else:
            # 기타: 첫 컬럼에 그대로 넣기
            for line in lines:
                rows.append({"값": line})
        self._log(f"직접 입력 목록 {len(rows)}개 로드", "INFO")
        return rows

    # ── 메인 실행 진입점 ─────────────────────────────────────
    def run(self):
        dispatch = {
            "kakao_friend":    self._run_kakao_friend,
            "kakao_openchat":  self._run_kakao_openchat,
            "telegram_join":   self._run_telegram_join,
            "telegram_message":self._run_telegram_message,
        }
        fn = dispatch.get(self.wk)
        if not fn:
            self._log(f"알 수 없는 작업유형: {self.wk}", "ERROR")
            self._done(0, 1)
            return
        try:
            fn()
        except Exception as e:
            self._log(f"실행 중 오류: {e}", "ERROR")
        finally:
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
                        "[실행불가] 드래그앤드롭 소스 좌표가 설정되지 않았습니다.",
                        "ERROR")
                    return
                if not (drp_c.get("x") and drp_c.get("y")):
                    self._log(
                        "[실행불가] 드래그앤드롭 드롭 좌표가 설정되지 않았습니다.",
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
                    self._log(f"  ② 이미지 첨부 (before) 시작")
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
                    self._log(f"  ④ 전송 — Enter")
                    self._hotkey("return")
                elif send_method == "ctrl_enter":
                    self._log(f"  ④ 전송 — Ctrl+Enter")
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
                    self._log(f"  ⑤ 이미지 첨부 (after) 시작")
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
                        self._log(f"  ⑥ 창 닫기 — ESC")
                        pyautogui.press("escape")
                    elif close_method == "altf4":
                        self._log(f"  ⑥ 창 닫기 — Alt+F4")
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
                break
            except Exception as e:
                self._fail += 1
                self._log(f"  ❌ 실패: {e}", "ERROR")
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
        if not HAS_PYAUTOGUI:
            self._log("pyautogui 가 필요합니다.", "ERROR")
            return

        rows  = self._read_targets()
        total = len(rows)

        if not rows:
            self._log("대상 목록이 비어 있습니다.", "WARN")
            return

        if not rows:
            return

        self._log(f"텔레그램 그룹 가입 시작 — "
                  f"총 {total}개", "INFO")

        for idx, row in enumerate(rows):
            if self._is_stopped():
                self._log("사용자 중지", "WARN")
                break

            self._progress(idx+1, total)
            link = str(row.get("텔레그램링크",
                       row.get("link", ""))).strip()

            if not link:
                self._log(f"  ⚠️ 링크 없음 스킵", "WARN")
                self._fail += 1
                continue

            self._log(f"[{idx+1}/{total}] 가입: {link}")

            try:
                result = self._telegram_join_once(link)
                if result == "success":
                    self._succ += 1
                    self._log(f"  ✅ 가입 완료", "SUCCESS")
                elif result == "already":
                    self._succ += 1
                    self._log(f"  ℹ️ 이미 가입됨", "INFO")
                else:
                    self._fail += 1
                    self._log(f"  ❌ 가입 실패", "ERROR")

            except Exception as e:
                self._fail += 1
                self._log(f"  ❌ 오류: {e}", "ERROR")

            tg_min = safe_float(self.tmpl.get("tg_between_min", 3.0))
            tg_max = safe_float(self.tmpl.get("tg_between_max", 7.0))
            if self._sleep_or_stop(random.uniform(tg_min, tg_max)): return  # BUG-03 fix

        self._log(
            f"완료 — 성공:{self._succ} / 실패:{self._fail}",
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
    # ════════════════════════════════════════════════════════
    # def _run_telegram_join_msg(self):  ← 제거됨; join_first 옵션으로 대체

        # ── 이미지 설정 읽기 ────────────────────────────────
        use_img  = self.tmpl.get("use_image", False)
        img_mode = self.tmpl.get("image_mode", "none")   # none/clipboard/file
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
        tg_join   = safe_float(self.tmpl.get("tg_join_click",  2.0))
        tg_type   = safe_float(self.tmpl.get("tg_after_type",  0.5))
        tg_send   = safe_float(self.tmpl.get("tg_after_send",  1.0))
        tg_back   = safe_float(self.tmpl.get("tg_after_back",  0.8))
        tg_min    = safe_float(self.tmpl.get("tg_between_min", 3.0))
        tg_max    = safe_float(self.tmpl.get("tg_between_max", 7.0))

        self._log(f"텔레그램 그룹가입+메시지 시작 — 총 {total}개  "
                  f"[이미지:{img_mode if use_img else 'none'} / "
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

                # ② 가입 버튼
                self._click("join_btn")
                time.sleep(tg_join)

                # ③ 이미지 첨부 (클립보드)
                if use_img and img_mode == "clipboard":
                    _cb_d = self.tmpl.get("image_delays", {})
                    _cb_paste = safe_float(_cb_d.get("cb_after_paste", 0), 0) or tg_type
                    pyautogui.hotkey("ctrl", "v")
                    time.sleep(_cb_paste)

                # ④ 이미지 첨부 (파일경로)
                elif use_img and img_mode == "file":
                    try:
                        self._tg_attach_file(img_path, tg_type)
                    except WorkflowExecutor._DialogSkipError as _dse:
                        self._fail += 1
                        self._log(f"  ⚠️ {_dse} → 다음 항목으로 건너뜀", "WARN")
                        continue

                # ⑤ 텍스트 입력 + 전송
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
                    # 바로입력: 링크/가입 후 입력창 자동 포커스
                    time.sleep(0.2)
                self._type(msg)
                time.sleep(tg_type)
                self._tg_send(send_method, tg_send)

                # ⑥ 닫기
                if close_after:
                    self._tg_close(close_method, tg_back)

                self._succ += 1
                self._log("  ✅ 완료", "SUCCESS")

            except Exception as e:
                self._fail += 1
                self._log(f"  ❌ 오류: {e}", "ERROR")
                try: pyautogui.press("escape")
                except: pass

            if self._sleep_or_stop(random.uniform(tg_min, tg_max)): return  # BUG-03 fix

        self._log(f"완료 — 성공:{self._succ} / 실패:{self._fail}", "SUCCESS")

    # ════════════════════════════════════════════════════════
    # 텔레그램 메시지 발송
    # ════════════════════════════════════════════════════════
    def _run_telegram_message(self):
        if not HAS_PYAUTOGUI:
            self._log("pyautogui 가 필요합니다.", "ERROR")
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

                # ② 이미지 첨부 (클립보드)
                if use_img and img_mode == "clipboard":
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
                try: pyautogui.press("escape")
                except: pass

            if self._sleep_or_stop(random.uniform(tg_min, tg_max)): return  # BUG-03 fix

        self._log(f"완료 — 성공:{self._succ} / 실패:{self._fail}", "SUCCESS")

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
        import time as _t

        # ── 포그라운드 창 타이틀 읽기 함수 구성 ──────────────
        _get_title = None
        try:
            import win32gui as _wg
            def _get_title():
                try:
                    return _wg.GetWindowText(_wg.GetForegroundWindow())
                except Exception:
                    return ""
        except ImportError:
            pass

        if _get_title is None:
            try:
                import pygetwindow as _pgw
                def _get_title():
                    try:
                        return _pgw.getActiveWindowTitle() or ""
                    except Exception:
                        return ""
            except ImportError:
                pass

        # ── 감지 불가 환경: 단순 대기 후 성공 간주 ───────────
        if _get_title is None:
            self._log("  ⚠️ [첨부버튼] 창 감지 라이브러리 없음 → 단순 대기", "WARN")
            pyautogui.click(ab_x, ab_y)
            _t.sleep(d_dialog)
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
                _t.sleep(poll)
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
            _t.sleep(0.5)

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
        """이미지 드래그앤드롭 (kakao_drag_drop 방식)
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
        self._log(f"[이미지] 드래그앤드롭 시작  소스({sx},{sy}) → 드롭({tx},{ty})")

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

        self._log("[이미지] ✅ 드래그앤드롭 완료")
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
        self.drain()
        if self._current_stop:
            self._current_stop.set()

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
        self._idle.wait(timeout)

    def _worker(self):
        while self.running:
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

            if self.q.empty():
                self._busy.clear()
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

    이전(v1.53): done_event.wait() 로 _run_job_sync() 를 순차 호출하는
    별도 daemon thread (_seq) 를 생성해서 처리.
    변경(v1.54): PostingEngine 이 큐 기반 직렬 처리를 보장하므로
    _run_job() 반복 호출만으로 충분 (별도 _seq 스레드 불필요, CHANGE-11 삭제).
    변경(v1.55): enabled=False 작업을 active_jobs 리스트로 필터링 후 실행.
    활성 작업이 0개이면 경고 다이얼로그 표시 후 즉시 반환.
    """
    if not self._jobs:
        messagebox.showwarning("작업 없음",
            "등록된 작업이 없습니다.")
        return

    # ── v1.55 CHANGE-A6: 비활성 작업 필터링 ─────────────────────────
    # 이전(v1.54): 모든 작업(self._jobs) 순차 실행 — enabled 무관
    # 변경(v1.55): enabled=True 작업만 실행 (False 작업 자동 스킵)
    #   활성 작업 0개이면 경고 다이얼로그 후 실행 중단
    active_jobs = [j for j in self._jobs if j.get("enabled", True)]
    if not active_jobs:
        messagebox.showwarning("활성 작업 없음",
            "활성화된 작업이 없습니다.\n"
            "⊙ 활성 토글 버튼으로 작업을 활성화하세요.")
        return

    for j in active_jobs:
        self._run_job(j)


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
            messagebox.showinfo("실행 중",
                f"[{name}] 이미 실행 중입니다.")
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

    def _progress(cur, total):
        pct = (cur / total * 100) if total > 0 else 0
        label = f"{name}  {cur}/{total}"
        self.after(0, lambda:
            self.set_progress(pct, label))

    def _done(succ, fail):
        self.after(0, lambda:
            self._on_job_done(name, succ, fail))

    # 상태: 대기 중 → 큐 추가 (engine worker가 실행 시 🟢로 전환)
    # v1.60 STEP-3: 시작 타임스탬프 기록 (ETA 정확도용)
    import time as _t_eta_stamp
    self._run_started_at = _t_eta_stamp.monotonic()
    self._update_job_status(name, "⏳ 대기 중")
    self._engine.add_task(job, tmpl, _log, _progress, _done)


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
    import math as _math_eta

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
    """작업 완료 콜백 — UI 갱신"""
    total = succ + fail
    status = f"✅ {succ}/{total}"
    self._update_job_status(name, status)
    self.set_counts(
        sum(1 for j in self._jobs
            if "✅" in j.get("_status","")),
        sum(1 for j in self._jobs
            if "❌" in j.get("_status","")),
    )
    self.app._set_status(
        f"[{name}] 완료 — 성공:{succ} 실패:{fail}")

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

    # 통계 업데이트
    if hasattr(self.app, "_stats_tab"):
        self.after(0,
            self.app._stats_tab.add_record,
            name, succ, fail)
    # v1.60 STEP-2: ETA 패널 갱신
    self.after(0, self._refresh_time_estimate)


def _jobs_update_job_status(self,
                             name: str, status: str):
    """Treeview 상태 컬럼 갱신"""
    for j in self._jobs:
        if j.get("name") == name:
            j["_status"] = status
            break
    try:
        self._tv.set(name, "status", status)
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
# Code G: 스케줄러 제어 함수  [v1.58 CHANGE-X5]
# ─────────────────────────────────────────────────────────────────────────────

def _jobs_stop_scheduler(self) -> None:
    """실행 중인 스케줄러 after-callback을 안전하게 취소."""
    if getattr(self, "_scheduler_after_id", None):
        try:
            self.after_cancel(self._scheduler_after_id)
        except Exception:
            pass
    self._scheduler_after_id = None
    self._scheduler_running  = False


def _jobs_start_scheduler(self) -> None:
    """스케줄러 틱을 즉시 한 번 호출 (이후 30초 반복)."""
    self._stop_scheduler()          # 중복 방지
    self._scheduler_running = True
    self._scheduler_tick()          # 첫 틱 즉시 실행


def _jobs_restart_scheduler(self) -> None:
    """스케줄러를 중지 후 즉시 재시작 (작업 저장/수정 후 호출)."""
    self._stop_scheduler()
    self.after(200, self._start_scheduler)  # 200ms 뒤 재시작


def _jobs_scheduler_tick(self):
    """스케줄 틱 — 30초마다 호출, 조건 충족 작업 자동 큐 투입
    [v1.56: CHANGE-S1 / v1.57: CHANGE-W9 / v1.58: CHANGE-X6]

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    v1.58 변경 사항:
      · _check_time_match() 활용: ±interval_variance 분 허용
      · 요일 필터: days(int list) 우선, schedule_days(KR) 폴백
      · 예외 격리: 작업 단위 try/except (한 작업 오류가 루프 중단 방지)

    실행 모드:
      ┌──────────────┬──────────────────────────────────────────────┐
      │ time 모드    │ _check_time_match(now_hm, t, variance)       │
      │              │ AND fired_key not in _fired_set              │
      │              │ AND 요일 필터 통과                            │
      ├──────────────┼──────────────────────────────────────────────┤
      │ interval 모드│ (now - last_run) >= schedule_interval 시간   │
      │              │ last_run="" → 첫 실행 즉시                    │
      │              │ AND 요일 필터 통과                            │
      └──────────────┴──────────────────────────────────────────────┘
    """
    # BUG-F3: _scheduler_running 체크 — stop 후 잔존 after가 재진입하는 것 방지
    if not getattr(self, "_scheduler_running", True):
        return   # stop_scheduler()가 호출된 상태 → 조용히 종료
    _KR_WEEKDAYS = ["월","화","수","목","금","토","일"]
    from datetime import datetime as _dt_sched
    try:
        now        = _dt_sched.now()
        today_str  = now.strftime("%Y-%m-%d")
        now_hm     = now.strftime("%H:%M")
        today_kr   = _KR_WEEKDAYS[now.weekday()]

        # ── BUG-05: _fired_set 당일 이전 키 자동 정리 ────────────────────────
        if hasattr(self, "_fired_set"):
            self._fired_set = {k for k in self._fired_set
                               if k.split("_")[-2] == today_str
                               or len(k.split("_")) < 3}
        else:
            self._fired_set = set()

        for j in self._jobs:
            # ── v1.58 CHANGE-X6: 작업 단위 예외 격리 ────────────────────────
            try:
                # ── 대상 필터: schedule_on=True AND enabled=True ────────────
                if not (j.get("schedule_on", False) and j.get("enabled", True)):
                    continue

                name = j.get("name", "")
                # BUG-F6/벤치마킹⑩: 이름 빈 문자열 방어 — _fired_set 키 오염 방지
                if not name:
                    continue
                mode = j.get("schedule_mode", "time")

                # ── v1.58: 요일 필터 — days(int) 우선, schedule_days(KR) 폴백 ─
                _int_days = j.get("days", None)
                if _int_days is None:
                    _kr_days = j.get("schedule_days", ["월","화","수","목","금"])
                    _int_days = [_KR_TO_INT[d] for d in _kr_days if d in _KR_TO_INT]
                if _int_days and now.weekday() not in _int_days:
                    continue   # 오늘 요일이 실행 대상 아님

                # ── time 모드: 복수 시각 루프 ──────────────────────────────
                if mode == "time":
                    sched_times = j.get("schedule_times", [])
                    if not sched_times:
                        t_single = j.get("schedule_time", "")
                        if t_single:
                            sched_times = [t_single]

                    # v1.58 CHANGE-X16: interval_variance ±분 허용
                    _variance = int(j.get("interval_variance",
                                          DEFAULT_SCHEDULE["interval_variance"]))
                    for t in sched_times:
                        if not _check_time_match(now_hm, t, _variance):
                            continue
                        # v1.60 BUG-N1: 자정 경계 — fired_key 날짜를 스케줄 기준 날짜로 고정
                        import datetime as _dt_fn
                        _sched_h = int(t.split(":")[0]) if ":" in t else 0
                        _now_h   = now.hour
                        # 스케줄이 23:xx인데 현재 00:xx → 전날 날짜 사용
                        if _sched_h >= 23 and _now_h <= 1:
                            _key_date = (now - _dt_fn.timedelta(days=1)).strftime("%Y-%m-%d")
                        else:
                            _key_date = today_str
                        fired_key = f"{name}_{_key_date}_{t}"
                        if fired_key in self._fired_set:
                            continue   # 이 분(minute)에 이미 트리거됨
                        # v1.60 BENCH-3: 50초 중복 가드 (monotonic 기반)
                        import time as _t_mono60
                        _guard_map = getattr(self, "_50sec_guard", {})
                        _now_mono  = _t_mono60.monotonic()
                        if _now_mono - _guard_map.get(fired_key, 0) < 50:
                            continue
                        _guard_map[fired_key] = _now_mono
                        self._50sec_guard = _guard_map
                        self._fired_set.add(fired_key)
                        # BUG-F7/벤치마킹④: interval_variance 랜덤 오프셋 적용
                        # variance>0이면 ±variance 범위 내 랜덤 딜레이 후 실행
                        # variance=0이면 즉시 실행 (기존 동작 유지)
                        import random as _rand_sched
                        _delay_sec = (
                            _rand_sched.randint(-_variance * 60, _variance * 60)
                            if _variance > 0 else 0
                        )
                        sched_label = j.get("schedule_label", f"{today_kr} {t}")
                        if hasattr(self.app, "_log_tab"):
                            _delay_info = (f" (±{_variance}분 오프셋: {_delay_sec:+d}초)"
                                           if _variance > 0 else "")
                            self.app._log_tab.append(
                                f"[스케줄] [{name}] 자동 실행 — {sched_label}{_delay_info}",
                                "INFO", "스케줄러")
                        if _delay_sec > 0:
                            self.after(_delay_sec * 1000,
                                       lambda _j=j: self._run_job(_j, silent=True))
                        elif _delay_sec < 0:
                            # 음수 오프셋: 이미 지나갔으므로 즉시 실행
                            self._run_job(j, silent=True)
                        else:
                            self._run_job(j, silent=True)

                # ── interval 모드: N시간마다 실행 ──────────────────────────
                elif mode == "interval":
                    interval = int(j.get("schedule_interval", 24))
                    last_raw = j.get("last_run", "")
                    fired    = False
                    if not last_raw:
                        fired = True   # 첫 실행 — 즉시
                    else:
                        try:
                            last_dt   = _dt_sched.strptime(
                                            last_raw, "%Y-%m-%d %H:%M:%S")
                            elapsed_h = (now - last_dt).total_seconds() / 3600
                            if elapsed_h >= interval:
                                fired = True
                        except ValueError:
                            fired = True   # 파싱 실패 → 재실행 허용
                    if fired:
                        sched_label = j.get("schedule_label",
                                            f"매 {interval}시간")
                        if hasattr(self.app, "_log_tab"):
                            self.app._log_tab.append(
                                f"[스케줄] [{name}] 자동 실행 — {sched_label}",
                                "INFO", "스케줄러")
                        # v1.60 BENCH-1: trigger_with_wait 패턴 적용
                        self._trigger_with_wait(j)
                        # v1.60 BUG-N3: last_run은 완료 콜백에서만 갱신 (tick에서 설정 금지)

            except Exception as _job_err:
                # 작업 단위 예외 격리 — 한 작업 오류가 전체 루프 중단 방지
                try:
                    if hasattr(self.app, "_log_tab"):
                        self.app._log_tab.append(
                            f"[스케줄러] 작업 [{j.get('name','?')}] 오류: {_job_err}",
                            "ERROR", "스케줄러")
                except Exception:
                    pass

    except Exception as _sched_err:
        try:
            if hasattr(self.app, "_log_tab"):
                self.app._log_tab.append(
                    f"[스케줄러 오류] {_sched_err}",
                    "ERROR", "스케줄러")
        except Exception:
            pass

    # 30초 후 재예약 — 예외 발생 시에도 루프 유지
    # BUG-F1 수정: after() 반환 ID를 저장해야 after_cancel이 실제로 작동
    self._scheduler_after_id = self.after(30_000, self._scheduler_tick)


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
    """v1.60 BENCH-2: 앱 시작 시 스케줄 복원 로그"""
    if not job_names:
        return
    if hasattr(self.app, "_log_tab"):
        for nm in job_names:
            self.app._log_tab.append(
                f"[스케줄 복원] [{nm}] 스케줄 재등록",
                "INFO", "스케줄러")


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
JobsTab._trigger_with_wait     = _jobs_trigger_with_wait      # v1.60 BENCH-1
JobsTab._log_scheduler_restore = _jobs_log_scheduler_restore  # v1.60 BENCH-2
JobsTab._refresh_time_estimate = lambda self: None            # stub (실제: 클래스 내부 정의)


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
# Block 5-A : LogTab — 실시간 로그
# ============================================================

class LogTab(tk.Frame):
    """
    실시간 로그 표시 + 레벨/소스 필터 + CSV 내보내기
    """
    def __init__(self, master, app: "App"):
        super().__init__(master, bg=PALETTE["bg"])
        self.app     = app
        self._logs:  list[dict] = []   # 전체 로그 버퍼
        self._build()

    def _build(self):
        # ── 타이틀 행 ───────────────────────────────────────
        hdr = tk.Frame(self, bg=PALETTE["bg"])
        hdr.pack(fill=tk.X, pady=(0, 8))
        tk.Label(hdr, text="🗒️  로그",
                 font=F_TITLE,
                 bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)

        # 우측 버튼
        for txt, cmd in [
            ("🗑 전체 삭제", self._clear),
            ("📥 CSV 저장",  self._export_csv),
        ]:
            tk.Button(hdr, text=txt, command=cmd,
                      bg=PALETTE["card"], fg=PALETTE["text"],
                      relief=tk.FLAT,
                      font=F_SMALL,
                      activebackground=PALETTE["hover"],
                      cursor="hand2", padx=8, pady=3
                      ).pack(side=tk.RIGHT, padx=(4, 0))

        # ── 필터 행 ─────────────────────────────────────────
        flt = tk.Frame(self, bg=PALETTE["bg"])
        flt.pack(fill=tk.X, pady=(0, 6))

        tk.Label(flt, text="레벨:",
                 font=F_LABEL,
                 bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT, padx=(0, 4))

        self._level_var = tk.StringVar(value="ALL")
        levels = ["ALL", "INFO", "SUCCESS", "WARN", "ERROR"]
        level_colors = {
            "ALL":     PALETTE["text2"],
            "INFO":    PALETTE["muted"],
            "SUCCESS": PALETTE["success"],
            "WARN":    PALETTE["warning"],
            "ERROR":   PALETTE["danger"],
        }
        for lv in levels:
            tk.Radiobutton(
                flt, text=lv,
                variable=self._level_var,
                value=lv,
                bg=PALETTE["bg"],
                fg=level_colors.get(lv, PALETTE["text"]),
                selectcolor=PALETTE["active"],
                activebackground=PALETTE["bg"],
                font=F_SMALL,
                command=self._apply_filter
            ).pack(side=tk.LEFT, padx=(0, 8))

        # 소스 필터
        tk.Label(flt, text="소스:",
                 font=F_LABEL,
                 bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT, padx=(12, 4))

        self._src_var = tk.StringVar(value="ALL")
        self._src_cb  = ttk.Combobox(
            flt, textvariable=self._src_var,
            values=["ALL"], width=16,
            state="readonly",
            font=F_SMALL)
        self._src_cb.pack(side=tk.LEFT)
        self._src_cb.bind("<<ComboboxSelected>>",
                          lambda e: self._apply_filter())

        # 검색창
        tk.Label(flt, text="검색:",
                 font=F_LABEL,
                 bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT, padx=(12, 4))
        self._search_var = tk.StringVar()
        self._search_var.trace_add(
            "write", lambda *a: self._apply_filter())
        tk.Entry(flt, textvariable=self._search_var,
                 bg=PALETTE["card2"], fg=PALETTE["text"],
                 insertbackground=PALETTE["text"],
                 relief=tk.FLAT,
                 font=F_SMALL, width=18
                 ).pack(side=tk.LEFT)

        # ── 로그 Treeview ────────────────────────────────────
        tv_frame = tk.Frame(self, bg=PALETTE["bg"])
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
        summ = tk.Frame(self, bg=PALETTE["sidebar"],
                        height=28)
        summ.pack(fill=tk.X, side=tk.BOTTOM)
        summ.pack_propagate(False)

        self._summ_var = tk.StringVar(value="로그 없음")
        tk.Label(summ, textvariable=self._summ_var,
                 font=F_SMALL,
                 bg=PALETTE["sidebar"],
                 fg=PALETTE["sidebar_text"],
                 anchor=tk.W, padx=12
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
            # 자동 스크롤
            children = self._tv.get_children()
            if children:
                self._tv.see(children[-1])

        self._update_summary()

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

    # ── CSV 내보내기 ─────────────────────────────────────────
    def _export_csv(self):
        if not self._logs:
            messagebox.showinfo("없음", "로그가 없습니다.")
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
        # 타이틀
        hdr = tk.Frame(self, bg=PALETTE["bg"])
        hdr.pack(fill=tk.X, pady=(0, 10))
        tk.Label(hdr, text="📊  통계",
                 font=F_TITLE,
                 bg=PALETTE["bg"], fg=PALETTE["text"]
                 ).pack(side=tk.LEFT)
        for txt, cmd in [
            ("🔄 새로고침", self.refresh),
            ("📥 CSV 저장", self._export_csv),
            ("🗑 초기화",   self._reset),
        ]:
            tk.Button(hdr, text=txt, command=cmd,
                      bg=PALETTE["card"], fg=PALETTE["text"],
                      relief=tk.FLAT,
                      font=F_SMALL,
                      activebackground=PALETTE["hover"],
                      cursor="hand2", padx=8, pady=3
                      ).pack(side=tk.RIGHT, padx=(4,0))

        # 요약 뱃지 행
        self._badge_frame = tk.Frame(self, bg=PALETTE["bg"])
        self._badge_frame.pack(fill=tk.X, pady=(0, 10))
        self._total_lbl  = self._badge("전체 실행", "0",
                                        PALETTE["primary"])
        self._succ_lbl   = self._badge("성공",      "0",
                                        PALETTE["success"])
        self._fail_lbl   = self._badge("실패",      "0",
                                        PALETTE["danger"])
        self._rate_lbl   = self._badge("성공률",    "0%",
                                        PALETTE["warning"])

        # Treeview
        tv_frame = tk.Frame(self, bg=PALETTE["bg"])
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
               color: str) -> tk.Label:
        f = tk.Frame(self._badge_frame,
                     bg=PALETTE["card"],
                     highlightbackground=color,
                     highlightthickness=2)
        f.pack(side=tk.LEFT, padx=(0,10), pady=4,
               ipadx=16, ipady=8)
        tk.Label(f, text=label,
                 font=F_SMALL,
                 bg=PALETTE["card"],
                 fg=PALETTE["text"]
                 ).pack()
        lbl = tk.Label(f, text=value,
                       font=F_TITLE,
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
            messagebox.showinfo("없음","통계 데이터 없음")
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
        hdr = tk.Frame(self, bg=PALETTE["bg"])
        hdr.pack(fill=tk.X, pady=(0,10))
        tk.Label(hdr, text="⚙️  설정",
                 font=F_TITLE,
                 bg=PALETTE["bg"],
                 fg=PALETTE["text"]).pack(side=tk.LEFT)

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
            tk.Label(inner, text=title,
                     font=F_HEAD,
                     bg=PALETTE["bg"],
                     fg=PALETTE["text"]
                     ).pack(anchor=tk.W,
                            padx=16, pady=(14,4))
            f = tk.Frame(inner, bg=PALETTE["card"],
                         highlightbackground=PALETTE["border"],
                         highlightthickness=1)
            f.pack(fill=tk.X, padx=16, pady=(0,4))
            return f

        def row(parent, label, widget_fn):
            r = tk.Frame(parent, bg=PALETTE["card"])
            r.pack(fill=tk.X, padx=12, pady=7)
            tk.Label(r, text=label, width=16,
                     anchor=tk.W,
                     font=F_LABEL,
                     bg=PALETTE["card"],
                     fg=PALETTE["text"]
                     ).pack(side=tk.LEFT)
            widget_fn(r)

        # ── 경로 설정 ────────────────────────────────────
        c1 = card("📁 경로 설정")
        self._log_dir_var  = tk.StringVar()
        self._out_dir_var  = tk.StringVar()

        def _log_w(p):
            tk.Entry(p, textvariable=self._log_dir_var,
                     bg=PALETTE["bg"], fg=PALETTE["text"],
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
                     bg=PALETTE["bg"], fg=PALETTE["text"],
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
                     bg=PALETTE["bg"], fg=PALETTE["text"],
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
                     bg=PALETTE["bg"], fg=PALETTE["text"],
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
                     bg=PALETTE["bg"], fg=PALETTE["text"],
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
                         bg=PALETTE["bg"],
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

        # ── 저장 버튼 ────────────────────────────────────
        tk.Button(inner, text="💾  설정 저장",
                  command=self._save,
                  bg=PALETTE["primary"],
                  fg=PALETTE["text"],
                  relief=tk.FLAT,
                  font=F_HEAD,
                  activebackground=_lighten(
                      PALETTE["primary"]),
                  cursor="hand2",
                  padx=20, pady=8
                  ).pack(anchor=tk.W,
                         padx=16, pady=(16,20))

    def _browse_dir(self, var: tk.StringVar):
        path = filedialog.askdirectory()
        if path: var.set(path)

    def _load(self):
        cfg = self.app.config_data
        p   = cfg.get("paths", {})
        m   = cfg.get("mouse", {})
        g   = cfg.get("global_delay", {})
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

        # pyautogui failsafe 적용
        if HAS_PYAUTOGUI:
            pyautogui.FAILSAFE = \
                cfg["mouse"]["failsafe"]
            pyautogui.PAUSE    = \
                cfg["mouse"]["click_delay"]

        save_json(CONFIG_PATH, cfg)
        self.app._set_status("✅ 설정 저장 완료")
        messagebox.showinfo("저장 완료",
            "설정이 저장되었습니다.")


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
        outer.pack(expand=True, fill="both", padx=36, pady=28)

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
            ).pack(fill="x", pady=(0, 14))

        # ── ID 입력 행 ────────────────────────────────────
        row_id = tk.Frame(outer, bg=P["bg"])
        row_id.pack(fill="x", pady=5)
        tk.Label(
            row_id, text="ID", width=5, anchor="w",
            font=(FF, 10), bg=P["bg"], fg=P["muted"],
        ).pack(side="left")
        self.id_var = tk.StringVar()
        tk.Entry(
            row_id, textvariable=self.id_var,
            font=(FF, 10),
            bg=P["card"], relief="solid", bd=1, width=28,
        ).pack(side="left", padx=(4, 0))

        # ── PW 입력 행 ────────────────────────────────────
        row_pw = tk.Frame(outer, bg=P["bg"])
        row_pw.pack(fill="x", pady=5)
        tk.Label(
            row_pw, text="PW", width=5, anchor="w",
            font=(FF, 10), bg=P["bg"], fg=P["muted"],
        ).pack(side="left")
        self.pw_var = tk.StringVar()
        tk.Entry(
            row_pw, textvariable=self.pw_var, show="●",
            font=(FF, 10),
            bg=P["card"], relief="solid", bd=1, width=28,
        ).pack(side="left", padx=(4, 0))

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
            relief="flat", padx=16, pady=7,
            cursor="hand2", state=login_state,
        ).pack(side="left", padx=6)
        tk.Button(
            row_btn, text="  종료  ",
            command=self._exit,
            font=(FF, 10),
            bg=P["border"], fg=P["muted"],
            relief="flat", padx=16, pady=7,
            cursor="hand2",
        ).pack(side="left", padx=6)

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