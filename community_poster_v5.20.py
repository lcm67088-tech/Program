#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Community Auto Poster v5.20
완전 로컬 기반 | ttkbootstrap 현대적 UI
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import json, os, threading, time, random, re, csv, copy
from datetime import datetime, timedelta
from pathlib import Path
import queue

# ── ttkbootstrap 시도 ──────────────────────────────────────────────
try:
    import ttkbootstrap as tb
    from ttkbootstrap.constants import *
    try:
        from ttkbootstrap.widgets import ToolTip
    except ImportError:
        from ttkbootstrap.tooltip import ToolTip
    HAS_BOOTSTRAP = True
except ImportError:
    HAS_BOOTSTRAP = False
    tb = ttk

# ── Selenium ────────────────────────────────────────────────────────
try:
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait, Select
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
    HAS_SELENIUM = True
except ImportError:
    HAS_SELENIUM = False

def _get_chrome_major_version() -> int | None:
    """PC에 설치된 Chrome의 메이저 버전을 반환 (Windows/Mac/Linux 지원)"""
    import re, subprocess, sys
    try:
        if sys.platform == "win32":
            import winreg
            for hive in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
                for path in (
                    r"Software\Google\Chrome\BLBeacon",
                    r"Software\Chromium\BLBeacon",
                    r"Software\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome",
                ):
                    try:
                        k = winreg.OpenKey(hive, path)
                        ver, _ = winreg.QueryValueEx(k, "version" if "BLBeacon" in path else "DisplayVersion")
                        return int(ver.split(".")[0])
                    except Exception:
                        continue
            # registry 실패 시 shell 명령으로 재시도
            try:
                out = subprocess.check_output(
                    r'reg query "HKLM\SOFTWARE\Google\Chrome\BLBeacon" /v version',
                    shell=True, stderr=subprocess.DEVNULL
                ).decode()
                m = re.search(r"(\d+)\.\d+\.\d+\.\d+", out)
                if m:
                    return int(m.group(1))
            except Exception:
                pass
        elif sys.platform == "darwin":
            out = subprocess.check_output(
                ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"],
                stderr=subprocess.DEVNULL
            ).decode()
            m = re.search(r"(\d+)", out)
            if m:
                return int(m.group(1))
        else:  # Linux
            for cmd in ("google-chrome", "google-chrome-stable", "chromium-browser", "chromium"):
                try:
                    out = subprocess.check_output([cmd, "--version"], stderr=subprocess.DEVNULL).decode()
                    m = re.search(r"(\d+)", out)
                    if m:
                        return int(m.group(1))
                except Exception:
                    continue
    except Exception:
        pass
    return None

# ═══════════════════════════════════════════════════════════════════
#  색상/스타일 상수
# ═══════════════════════════════════════════════════════════════════
PALETTE = {
    "bg":        "#F8F9FA",
    "sidebar":   "#1E293B",
    "sidebar_h": "#334155",
    "card":      "#FFFFFF",
    "border":    "#E2E8F0",
    "primary":   "#3B82F6",
    "success":   "#22C55E",
    "warning":   "#F59E0B",
    "danger":    "#EF4444",
    "muted":     "#94A3B8",
    "text":      "#1E293B",
    "text2":     "#64748B",
    "accent":    "#8B5CF6",
}

SITE_COLORS = {
    "마멘토":    "#3B82F6",
    "투잡커넥트": "#22C55E",
    "비즈모아":  "#F59E0B",
    "셀프모아":  "#8B5CF6",
    "아이보스":  "#EF4444",
}

FONT_FAMILY = "Malgun Gothic" if os.name == "nt" else "NanumGothic"

# ═══════════════════════════════════════════════════════════════════
#  경로 설정
# ═══════════════════════════════════════════════════════════════════
# EXE(frozen) 실행 시 sys.executable 기준, .py 실행 시 __file__ 기준
import sys as _sys
if getattr(_sys, 'frozen', False):
    BASE_DIR = Path(_sys.executable).parent   # EXE 옆 폴더
else:
    BASE_DIR = Path(__file__).parent           # .py 옆 폴더
CONFIG_DIR  = BASE_DIR / "config"
LOG_DIR     = BASE_DIR / "logs"
for d in (CONFIG_DIR, LOG_DIR):
    d.mkdir(exist_ok=True)

CFG_ACCOUNTS = CONFIG_DIR / "accounts.json"
CFG_CONTENTS = CONFIG_DIR / "contents.json"
CFG_SITES    = CONFIG_DIR / "sites.json"
CFG_SCHEDULE = CONFIG_DIR / "schedule.json"
CFG_OPTIONS  = CONFIG_DIR / "options.json"
CFG_JOBS     = CONFIG_DIR / "jobs.json"

# ═══════════════════════════════════════════════════════════════════
#  기본 사이트 설정
# ═══════════════════════════════════════════════════════════════════
# ─────────────────────────────────────────────────────────────────
#  마멘토 게시판 목록 (bo_table → 한글 이름)
# ─────────────────────────────────────────────────────────────────
MAMENTOR_BOARDS = {
    "smartstore":      "스마트스토어",
    "coupang":         "쿠팡",
    "s_reware":        "쇼핑리워드",
    "autocomplete":    "자완",
    "openmarcket":     "기타오픈마켓",
    "closemarcket":    "기타폐쇄몰",
    "program":         "프로그램판매",
    "programbuy":      "프로그램구매",
    "coin":            "플레이스배포",
    "place_ad":        "플레이스리워드",
    "keyword_ad":      "키워드광고",
    "blog_mkt":        "블로그 마케팅",
    "app_mkt":         "앱 마케팅",
    "cafe_mkt":        "카페 마케팅",
    "etc_search_mkt":  "기타 검색마케팅",
    "facebook":        "페이스북",
    "instagram":       "인스타그램",
    "youtube":         "유튜브",
    "etc_sns":         "기타 SNS",
    "media_mkt":       "언론 마케팅",
    "CPA_CPS":         "CPA/CPS",
    "etc_online_mkt":  "기타 온라인마케팅",
    "offline_mkt":     "오프라인 마케팅",
    "mkt_story":       "마케팅 이야기",
    "aietc":           "AI마케팅",
    "class":           "마케팅 강좌",
    "chinaetc":        "중국마케팅기타",
    "xiaohongshu":     "왕홍,샤오홍슈",
    "mkt_beginner":    "마케팅 왕초보",
    "etc_mkt":         "기타",
}
# bo_table 역방향 (한글 → bo_table)
MAMENTOR_BOARDS_R = {v: k for k, v in MAMENTOR_BOARDS.items()}

# ─────────────────────────────────────────────────────────────────
#  셀프모아 게시판 목록 (bo_table → 한글 이름)
#  URL 패턴: http://m.selfmoa.com/bbs/write.php?bo_table={bo_table}
# ─────────────────────────────────────────────────────────────────
SELFMOA_BOARDS = {
    "blog": "블로그",
    "SNS":  "SNS",
    "gita": "기타",
}
# bo_table 역방향 (한글 → bo_table)
SELFMOA_BOARDS_R = {v: k for k, v in SELFMOA_BOARDS.items()}

DEFAULT_SITES = {
    # ──────────────────────────────────────────────────────────────
    # 로그인 방식 설명
    #   main_url     : 항상 여기서 시작 (세션/쿠키 초기화)
    #   login_btn_sel: 메인 페이지에서 클릭할 '로그인' 버튼/링크
    #                  비워두면 메인에 ID/PW 폼이 바로 있다고 가정
    #   id_sel       : 아이디 입력 필드 셀렉터
    #   pw_sel       : 비밀번호 입력 필드 셀렉터
    #   btn_sel      : 로그인 제출 버튼 셀렉터
    # ──────────────────────────────────────────────────────────────
    "마멘토": {
        # HTML 확인: https://mamentor.co.kr/bbs/write.php?bo_table=place_ad
        # 로그인: 메인 사이드바에 로그인 폼 직접 노출 (login_btn_sel 불필요)
        "main_url":      "https://www.mamentor.co.kr",
        "login_btn_sel": "",
        # write_url: 계정별로 bo_table 지정 (MAMENTOR_BOARDS 참고)
        "write_url":     "https://www.mamentor.co.kr/bbs/write.php?bo_table=place_ad",
        "popup_sel":     ".hd_pops_reject, .btn_pops_close",
        # ── 로그인 폼 셀렉터 (메인 페이지 사이드바)
        "id_sel":        "#ol_id, input[name='mb_id'], input[placeholder*='아이디']",
        "pw_sel":        "#ol_pw, input[name='mb_password'], input[type='password']",
        "btn_sel":       ".btn_login, input[type='submit'][value*='로그인'], button[type='submit']",
        # ── 글쓰기 폼 셀렉터 (HTML 확인)
        "title_sel":     "#wr_subject",              # <input id="wr_subject" name="wr_subject">
        "editor_type":   "ckeditor4",               # ★ CKEditor4 (마멘토 도메인 ckeditor4_eyoom 사용)
        "editor_sel":    "#wr_content",              # <textarea id="wr_content" class="ckeditor">
        "submit_sel":    "#btn_submit",              # <input id="btn_submit" type="submit" value="작성완료">
        "success_pat":   "wr_id=",
        # ── 분류 셀렉터 (HTML 확인: select[name='ca_name'])
        "cat_sel":       "select[name='ca_name']",
        # ── 링크 필드 (HTML 확인: id=wr_link1, id=wr_link2)
        "link1_sel":     "#wr_link1",                # <input id="wr_link1" name="wr_link1">
        "link2_sel":     "#wr_link2",                # <input id="wr_link2" name="wr_link2">
        # ── 파일 첨부 (HTML 확인: name="bf_file[]" id="bf_file_1", id="bf_file_2")
        # 코드에서 #bf_file_1, #bf_file_2 ID 셀렉터로 접근
        "color":         "#3B82F6",
        "enabled":       True
    },
    "투잡커넥트": {
        # ── 메인 URL (팝업 쿠키 셋팅용, 실제 로그인은 login_url 로 이동)
        # HTML 확인: https://www.tojobcn.com/bbs/write.php?bo_table=order
        "main_url":      "https://www.tojobcn.com",
        # ── 로그인 전용 URL (그누보드 표준 로그인 페이지)
        "login_url":     "https://www.tojobcn.com/bbs/login.php",
        "login_btn_sel": "",
        # ── 글쓰기 URL  (분류: 작업의뢰 or 업체홍보)
        "write_url":     "https://www.tojobcn.com/bbs/write.php?bo_table=order",
        "popup_sel":     "",
        # ── 로그인 폼 셀렉터 (HTML 확인: name=mb_id, name=mb_password)
        "id_sel":        "input[name='mb_id']",
        "pw_sel":        "input[name='mb_password']",
        "btn_sel":       "button[type='submit'], input[type='submit'][value*='로그인']",
        # ── 글쓰기 폼 셀렉터 (SmartEditor2 / oEditors.getById['wr_content'] 방식)
        "title_sel":     "#wr_subject",              # <input id="wr_subject">
        "editor_type":   "smarteditor2",             # ★ SmartEditor2 (HuskyEZCreator.js 사용)
        "editor_sel":    "#wr_content",              # textarea (SmartEditor2가 감싸는 원본 textarea)
        "submit_sel":    "#btn_submit",              # <button id="btn_submit" type="submit">
        "success_pat":   "wr_id=",
        # ── 분류(카테고리) 드롭다운 (HTML 확인: select[name='ca_name'])
        # options: 작업의뢰, 업체홍보
        "cat_sel":       "select[name='ca_name']",
        "cat_default":   "업체홍보",          # 계정에 category 없을 때 기본값
        # ── 링크 필드 (HTML 확인: id=wr_link1, id=wr_link2)
        "link1_sel":     "#wr_link1",
        "link2_sel":     "#wr_link2",
        "color":         "#22C55E",
        "enabled":       True
    },
    "비즈모아": {
        "main_url":      "https://www.bizmoa.co.kr",
        "login_btn_sel": "",
        "write_url":     "",
        # 구글 애드센스 vignette 팡업 닫기 (selfmoa와 동일)
        "popup_sel":     "#dismiss-button",
        "id_sel":        "#id",
        "pw_sel":        "#pw",
        "btn_sel":       ".btn_login",
        "title_sel":     "#wr_subject",
        "editor_type":   "smarteditor2",
        "editor_sel":    "",
        "submit_sel":    "#btn_submit",
        "success_pat":   "wr_id=",
        "cat_sel":       "",
        "link1_sel":     "",
        "link2_sel":     "",
        "color":         "#F59E0B",
        "enabled":       True
    },
    "셀프모아": {
        # HTML 확인: http://m.selfmoa.com/bbs/write.php?bo_table=blog
        # 로그인: 모바일 메인(m.selfmoa.com) 오른쪽 사이드바 로그인 폼 직접 노이지
        # ※ m.selfmoa.com (http) 사용 – www.selfmoa.co.kr 유효하지 않음
        "main_url":      "http://m.selfmoa.com",
        "login_url":     "",
        "login_btn_sel": "",
        # write_url: 계정의 [카테고리] 필드로 자동 결정 (SELFMOA_BOARDS 참고)
        #   블로그 → http://m.selfmoa.com/bbs/write.php?bo_table=blog
        #   SNS    → http://m.selfmoa.com/bbs/write.php?bo_table=SNS
        #   기타   → http://m.selfmoa.com/bbs/write.php?bo_table=gita
        # 계정에 직접 write_url 입력 시 해당 URL 우선 사용
        "write_url":     "",
        # 구글 애드센스 vignette 팡업 (#google_vignette URL 단편)
        # 화면에 “광고 닫기” X 버튼: div#dismiss-button
        "popup_sel":     "#dismiss-button",
        # ── 로그인 폼 셀렉터 (HTML 확인: form#basic_outlogin)
        "id_sel":        "input[name='mb_id'], #outlogin_mb_id",
        "pw_sel":        "input[name='mb_password'], #outlogin_mb_password",
        "btn_sel":       "button[type='submit'].btn-navy, button[type='submit']",
        # ── 글쓰기 폼 셀렉터 (HTML 확인)
        "title_sel":     "#wr_subject",              # <input id="wr_subject" name="wr_subject">
        "editor_type":   "smarteditor2",             # ★ SmartEditor2 (HuskyEZCreator.js 사용)
        "editor_sel":    "",                         # SmartEditor2는 oEditors.getById 로 주입
        "submit_sel":    "#btn_submit",              # <button id="btn_submit" type="submit">
        "success_pat":   "wr_id=",
        # ── 분류(커테고리) 드롭다운 (HTML 확인: select[name='ca_name'])
        # options: 기자단, 체험단, 기타  → 기타로 고정
        "cat_sel":       "select[name='ca_name']",
        "cat_default":   "기타",
        # ── 게시글 작성 버튼 (game_board 목록페이지에서 클릭용)
        # <a href="./write.php?bo_table=blog" class="btn btn-color btn-sm">
        "write_btn_sel": "a.btn-color[href*='write.php'], a[href*='write.php?bo_table']",
        "link1_sel":     "",
        "link2_sel":     "",
        "color":         "#8B5CF6",
        "enabled":       True
    },
    "아이보스": {
        # ── 로그인: ab-login 페이지 직접 이동
        # HTML 확인: form name="TCBOARD_BD2986_WRITE_index471"
        "main_url":      "https://www.i-boss.co.kr/ab-login",
        "login_btn_sel": "",
        "write_url":     "https://www.i-boss.co.kr/ab-2988",  # 서비스 홍보 글쓰기
        "popup_sel":     "",
        # ── 로그인 폼 셀렉터
        "id_sel":        "input[name='member_id'], input[placeholder*='아이디'], input[placeholder*='이메일']",
        "pw_sel":        "input[name='member_pw'], input[type='password']",
        "btn_sel":       "button[type='submit'], .btn-login, .btn-submit",
        # ── 글쓰기 폼 셀렉터 (HTML 확인: Summernote 사용 확인)
        # 아이보스는 ./tools/editor/SummerEditor/summernote.js 로드 → Summernote 에디터
        "title_sel":     "#subject",                 # <input id="subject" name="subject">
        "editor_type":   "summernote",              # ★ Summernote (./tools/editor/SummerEditor/summernote.js)
        "editor_sel":    ".note-editable",          # Summernote 편집 영역
        # 이미지 버튼: Summernote 툴바 사진 버튼 → .note-misc .note-btn:first-child
        # ── 구분(카테고리): 커스텀 드롭다운 (일반 <select> 아님)
        # HTML: <div class="custom-select-display"> → options: data-value=B/C/A/D/S 등
        "cat_sel":       ".custom-select-display",
        "cat_type":      "custom_select",
        # 구분 옵션 매핑 (data-value → 표시이름)
        # 계정의 category 에 data-value(영문) 또는 한글명 입력 가능
        "cat_options": {
            "B": "블로그",    "C": "카페",       "A": "인스타그램",
            "D": "유튜브",    "S": "SNS",        "J": "스토어",
            "U": "언론홍보",  "W": "SEO",        "F": "지도",
            "G": "포스팅",    "E": "체험단",     "H": "인플루언서",
            "O": "숏폼",      "N": "PPL",        "Z": "기타",
        },
        # ── 등록 버튼 (HTML 확인: input[name='submit_OK'])
        "submit_sel":    "input[name='submit_OK']",
        "success_pat":   "ab-",
        "link1_sel":     "",
        "link2_sel":     "",
        # ── 계정 키 → 글쓰기 폼 input name 매핑 (HTML 확인)
        # 아이보스 글쓰기 폼: etc_1(회사명), etc_4(담당자명), phone_2(연락처),
        #                      etc_5(이메일), etc_2(네이트온), etc_3(카카오톡)
        # 연락처(phone_2)/이메일/네이트온/카카오톡은 class="oneOfvalue" → 1개 이상 필수
        "field_map": {
            "company": "etc_1",    # 회사명 (필수)
            "manager": "etc_4",    # 담당자명 (필수)
            "contact": "phone_2",  # 연락처 (oneOfvalue)
            "email":   "etc_5",    # 이메일 (oneOfvalue)
            "nate":    "etc_2",    # 네이트온 (oneOfvalue)
            "kakao":   "etc_3",    # 카카오톡 (oneOfvalue)
        },
        "color":         "#EF4444",
        "enabled":       True
    },
}

DEFAULT_OPTIONS = {
    "order":         "sequential",
    "delay_min":     3,
    "delay_max":     8,
    "retry_count":   2,
    "on_error":      "skip",
    "headless":      False,
    "random_content":False,
}

DEFAULT_SCHEDULE = {
    "enabled":  False,
    "mode":     "interval",
    "interval_hours":   3,
    "interval_variance":30,
    "times":    ["09:00","14:00","19:00"],
    "days":     [0,1,2,3,4],
}

# ═══════════════════════════════════════════════════════════════════
#  유틸리티
# ═══════════════════════════════════════════════════════════════════
def load_json(path, default):
    try:
        if Path(path).exists():
            with open(path, encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return copy.deepcopy(default)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def _merge_site_cfg(saved: dict, default: dict) -> dict:
    """저장된 사이트 설정에 DEFAULT 키를 채우고 오타 URL을 자동 수정.
    v5.3: 저장값이 빈 문자열("")이면 DEFAULT 값으로 복구 (초기화 방지).
    단, 의도적으로 비워도 되는 키(popup_sel, login_btn_sel,
    link1_sel, link2_sel)는 빈값 허용.
    """
    merged = copy.deepcopy(default)
    # 빈값이 아닌 저장값만 덮어쓰기 (선택적 필드는 예외)
    _allow_empty = {"popup_sel", "login_btn_sel",
                    "link1_sel", "link2_sel", "cat_sel",
                    "cat_default", "cat_type"}
    # login_url 은 투잡커넥트에 필수이므로 빈값이면 DEFAULT 사용 (not in _allow_empty)
    for k, v in saved.items():
        if k in _allow_empty:
            merged[k] = v  # 빈값 허용
        elif isinstance(v, str) and v.strip() == "":
            pass  # 빈 문자열 → DEFAULT 유지
        else:
            merged[k] = v  # 유효한 값 → 덮어쓰기
    # ── URL 자동 마이그레이션 ───────────────────────────────────
    _url_migrations = [
        ("mamento.co.kr",   "mamentor.co.kr"),      # 마멘토 오타
        ("www.toojob.co.kr","www.tojobcn.com"),      # 투잡커넥트 구 URL
        ("toojob.co.kr",    "tojobcn.com"),          # 투잡커넥트 구 URL (www 없는 경우)
    ]
    for key in ("main_url", "write_url", "login_url", "login_btn_sel"):
        val = merged.get(key, "")
        if not isinstance(val, str):
            continue
        for old_s, new_s in _url_migrations:
            if old_s in val:
                merged[key] = val.replace(old_s, new_s)
                break
    return merged

def load_sites_merged() -> dict:
    """sites.json 을 읽되 DEFAULT_SITES 기준으로 누락 키·오타를 보정한다."""
    saved = load_json(CFG_SITES, {})
    result = {}
    # DEFAULT 사이트 목록 기준으로 merge
    for site_name, default_cfg in DEFAULT_SITES.items():
        saved_cfg = saved.get(site_name, {})
        result[site_name] = _merge_site_cfg(saved_cfg, default_cfg)
    # saved 에만 있는 사용자 추가 사이트 보존
    for site_name, cfg in saved.items():
        if site_name not in result:
            result[site_name] = cfg
    return result

def log_entry(level, site, account, message):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [ts, level, site, account, message]
    log_file = LOG_DIR / f"log_{datetime.now().strftime('%Y-%m-%d')}.csv"
    with open(log_file, "a", newline="", encoding="utf-8-sig") as f:
        csv.writer(f).writerow(row)
    return f"[{ts}] [{level}] {site} | {account} → {message}"

# ═══════════════════════════════════════════════════════════════════
#  포스팅 엔진
# ═══════════════════════════════════════════════════════════════════
class PostingEngine:
    def __init__(self, app):
        self.app = app
        self.q = queue.Queue()
        self.running = False
        self._thread = None
        self._busy = threading.Event()   # 작업 실행 중 플래그 (set=실행중)
        self._idle = threading.Event()   # 유휴 상태 플래그 (set=idle)
        self._idle.set()                 # 초기 상태: idle

    def start(self):
        self.running = True
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()

    def stop(self):
        self.running = False

    def add_task(self, task):
        self.q.put(task)

    def wait_until_idle(self, timeout=300):
        """이전 작업 완료까지 대기 (기본 최대 5분)
        _idle Event가 set(=유휴 상태)이 될 때까지 블록.
        이전 코드의 _busy.wait()는 busy=set일 때 즉시 반환하는 버그가 있었음.
        """
        self._idle.wait(timeout)

    @property
    def is_busy(self):
        return self._busy.is_set()

    def _worker(self):
        while self.running:
            try:
                task = self.q.get(timeout=1)
                self._busy.set()         # 작업 시작 → busy ON
                self._idle.clear()       # idle OFF (대기 스레드 블록)
                try:
                    self._run_task(task)
                finally:
                    self.q.task_done()
                    if self.q.empty():
                        self._busy.clear()   # 큐 완전히 비면 → busy OFF
                        self._idle.set()     # idle ON → 대기 스레드 해제
            except queue.Empty:
                pass

    def _run_task(self, task):
        site_name   = task.get("site")
        account     = task.get("account")
        content     = task.get("content")
        site_cfg    = task.get("site_cfg")
        opts        = task.get("options")
        callback    = task.get("callback")

        acc_id = account.get("id", "")
        acc_pw = account.get("password", "")

        # ── 디버그 로그 콜백 ──────────────────────────────────────────
        def cb(status, msg):
            entry = log_entry(status, site_name, acc_id, msg)
            if callback:
                self.app.after(0, callback, status, entry)

        def dbg(msg):
            """DEBUG 레벨: 상세 진행 상황 로그"""
            cb("DEBUG", msg)

        # ── 작업 실행 전 앞 대기 (pre_delay) ──────────────────────────
        _pre_min = opts.get("pre_delay_min", 0) or 0
        _pre_max = opts.get("pre_delay_max", 0) or 0
        if _pre_min or _pre_max:
            _pre_wait = random.randint(int(_pre_min),
                                       max(int(_pre_min), int(_pre_max)))
            if _pre_wait > 0:
                dbg(f"[앞 대기] 실행 전 {_pre_wait}초 대기 중...")
                time.sleep(_pre_wait)

        if not HAS_SELENIUM:
            cb("ERROR", "selenium 미설치 – pip install selenium undetected-chromedriver")
            return

        driver = None
        for attempt in range(opts.get("retry_count", 2) + 1):
            try:
                dbg(f"[드라이버] Chrome 시작 (시도 {attempt+1})")
                options = uc.ChromeOptions()
                if opts.get("headless"):
                    options.add_argument("--headless=new")
                # ── 크래시 방지 & 탐지 회피 옵션 ──
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--disable-software-rasterizer")
                options.add_argument("--disable-extensions")
                options.add_argument("--disable-popup-blocking")
                options.add_argument("--disable-infobars")
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_argument("--no-first-run")
                options.add_argument("--no-service-autorun")
                options.add_argument("--password-store=basic")
                options.add_argument("--window-size=1280,900")
                options.add_argument("--lang=ko-KR")
                options.add_argument(
                    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                )
                _chrome_ver = _get_chrome_major_version()
                dbg(f"[드라이버] 감지된 Chrome 버전: {_chrome_ver}")
                try:
                    if _chrome_ver:
                        driver = uc.Chrome(options=options, version_main=_chrome_ver)
                    else:
                        driver = uc.Chrome(options=options)
                except Exception as _drv_e:
                    import traceback as _tb
                    dbg(f"[드라이버] Chrome 시작 실패: {type(_drv_e).__name__}: {_drv_e}")
                    dbg(f"[드라이버] 트레이스백:\n{_tb.format_exc()}")
                    raise
                driver.set_window_size(1280, 900)
                dbg("[드라이버] Chrome 실행 완료")

                # ════════════════════════════════════════════════════════
                #  공용 헬퍼 함수들
                # ════════════════════════════════════════════════════════

                def dismiss_alert(d, timeout=3):
                    import time as _t
                    deadline = _t.time() + timeout
                    while _t.time() < deadline:
                        try:
                            alert_text = d.switch_to.alert.text
                            d.switch_to.alert.accept()
                            dbg(f"[팝업] JS Alert 닫음: \"{alert_text}\"")
                            _t.sleep(0.3)
                        except Exception:
                            break

                def close_all_popups(d):
                    dismiss_alert(d)
                    try:
                        from selenium.webdriver.common.keys import Keys as _Keys
                        d.find_element(By.TAG_NAME, "body").send_keys(_Keys.ESCAPE)
                        time.sleep(0.3)
                    except Exception:
                        pass
                    dismiss_alert(d)

                    popup_sel = site_cfg.get("popup_sel", "")
                    if popup_sel:
                        try:
                            el = WebDriverWait(d, 2).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, popup_sel))
                            )
                            d.execute_script("arguments[0].click();", el)
                            dbg(f"[팝업] popup_sel 클릭: {popup_sel}")
                            time.sleep(0.3)
                        except Exception:
                            pass

                    CSS_CLOSE = [
                        ".popup-close", ".popup_close", ".modal-close", ".modal_close",
                        ".btn-close", ".btn_close", ".layer-close", ".layer_close",
                        ".close-btn", ".close_btn", ".close-button", ".dialog-close",
                        "#closeBtn", "#btnClose", "#popupClose", "#layerClose", "#modalClose",
                        "[aria-label='close']", "[aria-label='닫기']", "[aria-label='Close']",
                        "[aria-label='광고 닫기']",   # ← Google Vignette 광고 닫기
                        "#dismiss-button", "div#dismiss-button",  # ← Google Vignette (selfmoa/bizmoa)
                        ".hd_pops_reject", ".ab-close", "button.close", "a.close",
                        "[class*='PopupClose']", "[class*='popupClose']",
                        "[class*='ModalClose']", "[id*='Close']:not(input):not(select)",
                    ]
                    # ── Google Vignette (#google_vignette) URL hash 별도 처리 ──
                    try:
                        if "#google_vignette" in d.current_url:
                            d.execute_script(
                                "var el = document.getElementById('dismiss-button');"
                                "if (el) { el.click(); }"
                                "else { history.replaceState(null,'',"
                                "location.pathname+location.search); }"
                            )
                            dbg("[팡업] Google Vignette 해제")
                            time.sleep(0.3)
                    except Exception:
                        pass
                    for sel in CSS_CLOSE:
                        try:
                            for el in d.find_elements(By.CSS_SELECTOR, sel):
                                if el.is_displayed():
                                    d.execute_script("arguments[0].click();", el)
                                    time.sleep(0.2)
                        except Exception:
                            pass

                    XPATH_CLOSE = [
                        "//*[self::button or self::a or self::span or self::label or self::div or self::p]"
                        "[contains(normalize-space(text()),'오늘') and contains(normalize-space(text()),'그만')]",
                        "//*[self::button or self::a or self::span or self::label or self::div or self::p]"
                        "[contains(normalize-space(text()),'오늘') and contains(normalize-space(text()),'보지')]",
                        "//*[self::button or self::a or self::span or self::label or self::div or self::p]"
                        "[contains(normalize-space(text()),'하루') and contains(normalize-space(text()),'보지')]",
                        "//*[self::button or self::a or self::span or self::label or self::div or self::p]"
                        "[contains(normalize-space(text()),'24시간')]",
                        "//*[self::button or self::a or self::span or self::label or self::div or self::p]"
                        "[contains(normalize-space(text()),'일주일') and contains(normalize-space(text()),'보지')]",
                        "//*[self::button or self::a or self::span or self::label or self::div or self::p]"
                        "[normalize-space(text())='닫기' or normalize-space(text())='X'"
                        " or normalize-space(text())='×' or normalize-space(text())='✕'"
                        " or normalize-space(text())='Close' or normalize-space(text())='close']",
                    ]
                    for xp in XPATH_CLOSE:
                        try:
                            for el in d.find_elements(By.XPATH, xp):
                                if el.is_displayed():
                                    d.execute_script("arguments[0].click();", el)
                                    time.sleep(0.2)
                        except Exception:
                            pass

                    try:
                        d.execute_script("""
                            var DISMISS_TODAY=['오늘 그만보기','오늘그만보기','오늘 하루 보지 않기',
                                '오늘 하루 안보기','하루 동안 보지 않기','하루동안 보지않기',
                                '24시간 보지 않기','24시간보지않기','일주일 보지않기','오늘 그만 보기'];
                            var DISMISS_CLOSE=['닫기','닫 기','X','x','×','✕','✖','Close','close'];
                            function tryClick(el){try{el.click();}catch(e){}}
                            var all=document.querySelectorAll('*');
                            for(var i=0;i<all.length;i++){
                                var el=all[i],st=window.getComputedStyle(el);
                                var zi=parseInt(st.zIndex)||0;
                                var disp=st.display!=='none'&&st.visibility!=='hidden'&&el.offsetWidth>0&&el.offsetHeight>0;
                                if(zi>50&&disp){
                                    var btns=el.querySelectorAll('button,a,span,label,p,div[role="button"],[role="button"]');
                                    for(var j=0;j<btns.length;j++){
                                        var t=(btns[j].innerText||'').trim();
                                        for(var k=0;k<DISMISS_TODAY.length;k++){if(t.indexOf(DISMISS_TODAY[k])!==-1)tryClick(btns[j]);}
                                    }
                                    for(var j=0;j<btns.length;j++){
                                        var t=(btns[j].innerText||'').trim();
                                        for(var k=0;k<DISMISS_CLOSE.length;k++){if(t===DISMISS_CLOSE[k])tryClick(btns[j]);}
                                    }
                                }
                            }
                        """)
                        time.sleep(0.3)
                    except Exception:
                        pass
                    dismiss_alert(d)

                def find_visible(d, selector, timeout=10):
                    sels = [s.strip() for s in selector.split(",") if s.strip()]
                    per = max(1, timeout // max(len(sels), 1))
                    for sel in sels:
                        try:
                            WebDriverWait(d, per).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, sel))
                            )
                        except Exception:
                            pass
                        try:
                            for el in d.find_elements(By.CSS_SELECTOR, sel):
                                if el.is_displayed():
                                    return el
                        except Exception:
                            pass
                    raise Exception(f"요소를 찾을 수 없음: {selector}")

                def text_to_html(text):
                    """순수 텍스트를 HTML로 변환
                    - 이미 HTML 태그가 있으면 그대로 반환
                    - \\n 한 줄 = 각각 <p>단락 (SmartEditor2/CKEditor/Summernote 공통 안정)
                    - 빈 줄(\\n\\n) = <p>&nbsp;</p> 공백 단락 (단락 간격 유지)
                    - 연속 빈 줄 3개 이상 → 2개로 정규화
                    """
                    import html as _hm, re as _re
                    if bool(_re.search(r'<(br|p|div|span|img|b|i|u|h[1-6]|ul|ol|li)[\s/>]', text, _re.I)):
                        return text  # 이미 HTML → 그대로
                    norm = text.replace('\r\n', '\n').replace('\r', '\n')
                    norm = _re.sub(r'\n{3,}', '\n\n', norm)  # 연속 빈줄 정규화
                    parts = []
                    for line in norm.split('\n'):
                        stripped = line.strip()
                        if stripped:
                            parts.append(f'<p>{_hm.escape(stripped)}</p>')
                        else:
                            parts.append('<p>&nbsp;</p>')  # 빈줄 = 공백 단락(간격)
                    # 맨 앞뒤 공백 단락 제거
                    while parts and parts[0] == '<p>&nbsp;</p>':
                        parts.pop(0)
                    while parts and parts[-1] == '<p>&nbsp;</p>':
                        parts.pop()
                    return ''.join(parts) if parts else '<p>&nbsp;</p>'

                # ════════════════════════════════════════════════════════
                #  사이트별 분리 실행 라우터
                # ════════════════════════════════════════════════════════
                if site_name == "아이보스":
                    self._post_iboss(
                        driver, site_cfg, account, content,
                        cb, dbg, dismiss_alert, close_all_popups,
                        find_visible, text_to_html, acc_id, acc_pw
                    )
                elif site_name in ("마멘토",):
                    self._post_gnuboard(
                        driver, site_cfg, account, content,
                        cb, dbg, dismiss_alert, close_all_popups,
                        find_visible, text_to_html, acc_id, acc_pw
                    )
                elif site_name == "투잡커넥트":
                    # ★ 투잡커넥트는 SmartEditor2 사용 (oEditors.getById 방식)
                    self._post_smarteditor(
                        driver, site_cfg, account, content,
                        cb, dbg, dismiss_alert, close_all_popups,
                        find_visible, text_to_html, acc_id, acc_pw
                    )
                else:
                    # 비즈모아, 셀프모아 등 SmartEditor2 계열
                    self._post_smarteditor(
                        driver, site_cfg, account, content,
                        cb, dbg, dismiss_alert, close_all_popups,
                        find_visible, text_to_html, acc_id, acc_pw
                    )

                d_min = opts.get("delay_min", 3)
                d_rnd = random.randint(0, max(0, opts.get("delay_max", 8) - d_min))
                # ── 게시 완료 즉시 Chrome 창 닫기 (delay 전에 먼저 종료) ──
                if driver:
                    try: driver.quit()
                    except: pass
                    driver = None
                time.sleep(d_min + d_rnd)
                break

            except Exception as e:
                import traceback as _tbm
                tb = _tbm.format_exc()
                _etype = type(e).__name__
                # 에러 발생 시 현재 URL·페이지 제목 기록
                _err_url = ""
                _err_title = ""
                if driver:
                    try: _err_url = driver.current_url
                    except: pass
                    try: _err_title = driver.title
                    except: pass
                _detail = (
                    f"[{_etype}] {e}"
                    + (f"\n  └ 현재 URL : {_err_url}" if _err_url else "")
                    + (f"\n  └ 페이지 제목: {_err_title}" if _err_title else "")
                )
                if attempt < opts.get("retry_count", 2):
                    cb("WARN", f"재시도 {attempt+1}/{opts.get('retry_count',2)} – {_detail}")
                    dbg(f"[스택트레이스 (시도 {attempt+1})]\n{tb}")
                    time.sleep(3)
                else:
                    cb("ERROR", f"최종 실패 – {_detail}")
                    dbg(f"[스택트레이스 (최종)]\n{tb}")
            finally:
                if driver:
                    try: driver.quit()
                    except: pass
                    driver = None

    # ════════════════════════════════════════════════════════════════
    #  사이트별 포스팅 로직 분리
    # ════════════════════════════════════════════════════════════════

    def _login_common(self, driver, site_cfg, acc_id, acc_pw,
                      cb, dbg, dismiss_alert, close_all_popups, find_visible):
        """공용 로그인: 메인 진입 → 팝업 닫기 → ID/PW 입력 → 검증"""

        main_url = site_cfg.get("main_url", "").rstrip("/")
        if not main_url:
            raise Exception("main_url 이 설정되지 않았습니다")
        dbg(f"[로그인 STEP1] 메인 URL 진입: {main_url}")
        driver.get(main_url)
        time.sleep(2.5)

        dbg("[로그인 STEP2] 팝업 닫기 1차")
        close_all_popups(driver)
        time.sleep(0.5)
        dbg("[로그인 STEP2] 팝업 닫기 2차 (지연 팝업 대응)")
        close_all_popups(driver)

        # ── login_url 이 별도로 지정된 경우 해당 페이지로 직접 이동 ──
        login_url = site_cfg.get("login_url", "").strip()
        if login_url:
            dbg(f"[로그인 STEP2.5] 로그인 전용 URL 이동: {login_url}")
            driver.get(login_url)
            time.sleep(1.5)
            close_all_popups(driver)

        login_btn_sel = site_cfg.get("login_btn_sel", "").strip()
        if login_btn_sel:
            dbg(f"[로그인 STEP3] 로그인 버튼 클릭 시도: {login_btn_sel}")
            _clicked = False
            for sel in [s.strip() for s in login_btn_sel.split(",") if s.strip()]:
                try:
                    el = WebDriverWait(driver, 4).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, sel))
                    )
                    if el.is_displayed():
                        driver.execute_script("arguments[0].click();", el)
                        _clicked = True
                        dbg(f"[로그인 STEP3] 클릭 성공: {sel}")
                        break
                except Exception as _e:
                    dbg(f"[로그인 STEP3] 셀렉터 실패: {sel} → {_e}")
            if not _clicked:
                for tag in ("button", "a", "span"):
                    try:
                        for el in driver.find_elements(By.TAG_NAME, tag):
                            if el.is_displayed() and el.text.strip() in ("로그인", "Login"):
                                driver.execute_script("arguments[0].click();", el)
                                _clicked = True
                                dbg(f"[로그인 STEP3] 텍스트 폴백 클릭: {el.text.strip()}")
                                break
                    except Exception:
                        pass
                    if _clicked:
                        break
            if _clicked:
                time.sleep(1.5)
                close_all_popups(driver)
        else:
            dbg("[로그인 STEP3] login_btn_sel 없음 – 페이지에 바로 폼 있음")

        id_sel  = site_cfg.get("id_sel",  "input[name='id'], input[type='email']")
        pw_sel  = site_cfg.get("pw_sel",  "input[name='pw'], input[type='password']")
        btn_sel = site_cfg.get("btn_sel", "button[type='submit'], input[type='submit']")

        dbg(f"[로그인 STEP4] ID 입력 (셀렉터: {id_sel})")
        id_el = find_visible(driver, id_sel)
        id_el.click(); id_el.clear(); id_el.send_keys(acc_id)
        dbg(f"[로그인 STEP4] ID 입력 완료: {acc_id}")

        dbg(f"[로그인 STEP4] PW 입력 (셀렉터: {pw_sel})")
        pw_el = find_visible(driver, pw_sel)
        pw_el.click(); pw_el.clear(); pw_el.send_keys(acc_pw)

        dbg(f"[로그인 STEP4] 로그인 버튼 클릭 (셀렉터: {btn_sel})")
        btn_el = find_visible(driver, btn_sel)
        btn_el.click()
        time.sleep(2.5)

        dbg("[로그인 STEP5] 로그인 후 팝업 처리")
        close_all_popups(driver)

        dbg(f"[로그인 STEP6] 로그인 성공 확인 (현재 URL: {driver.current_url})")
        try:
            still = driver.find_elements(By.CSS_SELECTOR, pw_sel.split(",")[0].strip())
            if still and still[0].is_displayed():
                raise Exception("로그인 실패 – ID/PW를 확인하세요 (비밀번호 필드가 여전히 보임)")
        except Exception as _ce:
            if "로그인 실패" in str(_ce):
                raise

    # ──────────────────────────────────────────────────────────────
    #  아이보스 전용 포스팅 로직  (다른 사이트와 통합하지 않음)
    # ──────────────────────────────────────────────────────────────
    def _post_iboss(self, driver, site_cfg, account, content,
                    cb, dbg, dismiss_alert, close_all_popups,
                    find_visible, text_to_html, acc_id, acc_pw):

        def _scroll_and_fill(driver, css, value, label):
            """요소를 찾아 스크롤 후 값 입력, 성공/실패 DEBUG 출력"""
            try:
                el = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, css))
                )
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                time.sleep(0.2)
                el.click(); el.clear(); el.send_keys(value)
                dbg(f"[아이보스] {label} 입력 완료: {value}")
            except Exception as _e:
                dbg(f"[아이보스] {label} 입력 실패 "
                    f"(셀렉터: {css}) → [{type(_e).__name__}] {_e}  ← 필드가 없으면 무시해도 됩니다")

        # ── STEP1  로그인 ─────────────────────────────────────────
        self._login_common(driver, site_cfg, acc_id, acc_pw,
                           cb, dbg, dismiss_alert, close_all_popups, find_visible)

        # ── STEP2  글쓰기 페이지 이동 ────────────────────────────
        write_url = site_cfg.get("write_url", "").strip()
        if not write_url:
            raise Exception("write_url 이 설정되지 않았습니다")
        dbg(f"[아이보스 STEP2] 글쓰기 페이지 이동: {write_url}")
        driver.get(write_url)
        time.sleep(2.5)
        dismiss_alert(driver)
        dbg(f"[아이보스 STEP2] 글쓰기 페이지 로드 완료 (URL: {driver.current_url})")

        # ── STEP3  제목 ───────────────────────────────────────────
        title_sel = site_cfg.get("title_sel", "#subject")
        title_val = content.get("title", "")
        if title_sel and title_val:
            dbg(f"[아이보스 STEP3] 제목 입력: \"{title_val[:40]}\"")
            try:
                WebDriverWait(driver, 8).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, title_sel))
                )
                t_el = driver.find_element(By.CSS_SELECTOR, title_sel)
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", t_el)
                t_el.click(); t_el.clear(); t_el.send_keys(title_val)
                dbg("[아이보스 STEP3] 제목 입력 완료")
            except Exception as e:
                raise Exception(f"제목 입력 실패 (셀렉터: {title_sel}) "
                                f"[{type(e).__name__}] → {e}")

        # ── STEP4  구분 드롭다운 (custom-select) ─────────────────
        # HTML 확인: data-value=B(블로그)/C(카페)/A(인스타그램)/D(유튜브)/S(SNS)/J(스토어)
        #            /U(언론홍보)/W(SEO)/F(지도)/G(포스팅)/E(체험단)/H(인플루언서)/O(숏폼)/N(PPL)/Z(기타)
        # ※ 계정의 category에 data-value(영문) 또는 한글명 입력 가능
        cat_val = account.get("category", "").strip()
        if not cat_val:
            dbg("[\uc544\uc774\ubcf4\uc2a4 STEP4] \uce74\ud14c\uace0\ub9ac \ubbf8\uc124\uc815 \u2013 \uccab \ubc88\uc9f8 \uc635\uc158 \uc790\ub3d9 \uc120\ud0dd")
            try:
                _toggle0 = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".custom-select-display"))
                )
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", _toggle0)
                time.sleep(0.2)
                driver.execute_script("arguments[0].click();", _toggle0)
                time.sleep(0.6)
                _opts0 = driver.find_elements(By.CSS_SELECTOR, ".custom-options .option")
                if _opts0:
                    driver.execute_script("arguments[0].click();", _opts0[0])
                    _auto_val = _opts0[0].get_attribute("data-value") or _opts0[0].text.strip()
                    dbg(f"[\uc544\uc774\ubcf4\uc2a4 STEP4] \uccab \ubc88\uc9f8 \uc635\uc158 \uc790\ub3d9 \uc120\ud0dd: {_auto_val}")
                else:
                    dbg("[\uc544\uc774\ubcf4\uc2a4 STEP4] \u26a0 \ub4dc\ub86d\ub2e4\uc6b4 \uc635\uc158 \uc5c6\uc74c")
                time.sleep(0.3)
            except Exception as _e0:
                dbg(f"[\uc544\uc774\ubcf4\uc2a4 STEP4] \uc790\ub3d9 \uc120\ud0dd \uc2e4\ud328: {_e0}")
        if cat_val:
            # cat_options 역방향: 한글이름 → data-value 변환
            _cat_opts = site_cfg.get("cat_options", {})
            _cat_rev  = {v: k for k, v in _cat_opts.items()}
            if cat_val in _cat_rev:
                _orig_cat = cat_val
                cat_val = _cat_rev[cat_val]
                dbg(f"[아이보스 STEP4] 카테고리 한글→code 변환: {_orig_cat} → {cat_val}")
            dbg(f"[아이보스 STEP4] 구분 드롭다운 선택: \"{cat_val}\"")
            try:
                toggle = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".custom-select-display"))
                )
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", toggle)
                time.sleep(0.2)
                driver.execute_script("arguments[0].click();", toggle)
                time.sleep(0.6)
                _clicked = False
                opts_els = driver.find_elements(By.CSS_SELECTOR, ".custom-options .option")
                dbg(f"[아이보스 STEP4] 드롭다운 옵션 {len(opts_els)}개 발견")
                # data-value 완전 일치 우선 (B, C, A, D, S, J, U, W, F, G, E, H, O, N, Z)
                for opt in opts_els:
                    if (opt.get_attribute("data-value") or "").strip() == cat_val:
                        driver.execute_script("arguments[0].click();", opt)
                        _clicked = True
                        dbg(f"[아이보스 STEP4] data-value 일치: {cat_val}")
                        break
                # 텍스트 완전 일치
                if not _clicked:
                    for opt in opts_els:
                        if opt.text.strip() == cat_val:
                            driver.execute_script("arguments[0].click();", opt)
                            _clicked = True
                            dbg(f"[아이보스 STEP4] 텍스트 일치: {opt.text.strip()}")
                            break
                # 부분 포함
                if not _clicked:
                    for opt in opts_els:
                        if cat_val in opt.text:
                            driver.execute_script("arguments[0].click();", opt)
                            _clicked = True
                            dbg(f"[아이보스 STEP4] 부분 일치: {opt.text.strip()}")
                            break
                if not _clicked:
                    all_opts = [f"{o.get_attribute('data-value')}={o.text.strip()}" for o in opts_els]
                    dbg(f"[아이보스 STEP4] ⚠ 구분 옵션 \"{cat_val}\" 없음 – 가용 옵션: {all_opts}")
                time.sleep(0.3)
            except Exception as e:
                dbg(f"[아이보스 STEP4] 구분 드롭다운 실패 [{type(e).__name__}]: {e}  ← 비워두면 생략")

        # ── STEP5  회사명 (etc_1) – 필수 ─────────────────────────
        company_val = account.get("company", "").strip()
        if company_val:
            _scroll_and_fill(driver, "input[name='etc_1']", company_val, "회사명(etc_1)")
        else:
            dbg("[아이보스 STEP5] 회사명 비어있음 – 생략")

        # ── STEP6  담당자명 (etc_4) – 필수 ──────────────────────
        manager_val = account.get("manager", "").strip()
        if manager_val:
            _scroll_and_fill(driver, "input[name='etc_4']", manager_val, "담당자명(etc_4)")
        else:
            dbg("[아이보스 STEP6] 담당자명 비어있음 – 생략")

        # ── STEP7  연락처 (phone_2) – 선택 ──────────────────────
        # HTML 확인: phone_2는 일반 텍스트 input (라디오버튼 없음, disabled 아님)
        # <input type="text" name="phone_2" class="AB-text oneOfvalue">
        contact_val = account.get("contact", "").strip()
        if contact_val:
            try:
                # 가시성 확보 (혹시 disabled 상태일 경우 대비)
                driver.execute_script(
                    "var f=document.querySelector(\"input[name='phone_2']\");"
                    "if(f){"
                    "  f.removeAttribute('disabled');"
                    "  f.removeAttribute('readonly');"
                    "  f.style.display='';"
                    "  f.style.visibility='';"
                    "  f.scrollIntoView({block:'center'});"
                    "}"
                )
                time.sleep(0.3)
                el = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='phone_2']"))
                )
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                time.sleep(0.2)
                driver.execute_script("arguments[0].value = arguments[1];", el, contact_val)
                el.send_keys("")   # change 이벤트 트리거
                dbg(f"[아이보스 STEP7] 연락처(phone_2) 입력 완료: {contact_val}")
            except Exception as _e:
                dbg(f"[아이보스 STEP7] 연락처(phone_2) 입력 실패 → {_e}  (선택 필드, 무시)")
        else:
            dbg("[아이보스 STEP7] 연락처 비어있음 – 생략 (선택 필드)")

        # ── STEP8  이메일 (etc_5) – 선택 ────────────────────────
        email_val = account.get("email", "").strip()
        if email_val:
            _scroll_and_fill(driver, "input[name='etc_5']", email_val, "이메일(etc_5)")
        else:
            dbg("[아이보스 STEP8] 이메일 비어있음 – 생략 (선택 필드)")

        # ── STEP9  네이트온 (etc_2) – 선택 ──────────────────────
        nate_val = account.get("nate", "").strip()
        if nate_val:
            _scroll_and_fill(driver, "input[name='etc_2']", nate_val, "네이트온(etc_2)")
        else:
            dbg("[아이보스 STEP9] 네이트온 비어있음 – 생략 (선택 필드)")

        # ── STEP10 카카오톡 (etc_3) – 선택 ─────────────────────
        kakao_val = account.get("kakao", "").strip()
        if kakao_val:
            _scroll_and_fill(driver, "input[name='etc_3']", kakao_val, "카카오톡(etc_3)")
        else:
            dbg("[아이보스 STEP10] 카카오톡 비어있음 – 생략 (선택 필드)")

        # ── STEP11 본문 에디터 (Summernote) v5.20 ─────────────────
        import re as _re2  # noqa: F811
        body     = text_to_html(content.get("body", ""))

        # ① 에디터 대기
        WebDriverWait(driver, 12).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".note-editable"))
        )
        time.sleep(1.0)
        dbg("[STEP11] 에디터 준비")


        # ④ summernote('code', html) 단 한 번 주입
        _result = driver.execute_script(
            "var h=arguments[0];"
            "var jq=(typeof jQuery!=='undefined')?jQuery:(typeof $!=='undefined'?$:null);"
            "if(jq){"
            "  var sn=document.querySelector('[id^=\"smNote-\"]');"
            "  if(sn){try{jq(sn).summernote('code',h);return 'api-ok';}catch(e){}}"
            "  var ta=document.querySelector('textarea[name=\"comment_1\"]')"
            "        ||document.querySelector('textarea[data-editor]');"
            "  if(ta){var id=ta.getAttribute('data-editor');"
            "    if(id&&jq('#'+id).length){"
            "      try{jq('#'+id).summernote('code',h);return 'api-ok(id)';}catch(e){}}}"
            "}"
            "var ed=document.querySelector('.note-editable');"
            "if(ed){"
            "  ed.innerHTML=h;"
            "  var t2=document.querySelector('textarea[name=\"comment_1\"]')"
            "         ||document.querySelector('textarea[id^=\"oEdit-\"]')"
            "         ||document.querySelector('textarea[data-editor]');"
            "  if(t2)t2.value=h;"
            "  return 'inner-ok';"
            "}"
            "return 'failed';",
            body
        )
        dbg(f"[STEP11] 주입 결과: {_result}")
        if _result == 'failed':
            raise Exception("에디터 주입 실패")
        time.sleep(0.3)

        # ── STEP12 등록 버튼 ──────────────────────────────────────
        dismiss_alert(driver)
        try:
            _btn = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='submit_OK']"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", _btn)
            time.sleep(0.3)
            _btn.click()
            dbg("[STEP12] 등록 버튼 클릭")
        except Exception:
            try:
                _btn2 = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(.,'등록')]|//input[@type='submit']"))
                )
                driver.execute_script("arguments[0].click();", _btn2)
                dbg("[STEP12] 등록 버튼 클릭 (XPATH 폴백)")
            except Exception as _e:
                raise Exception(f"등록 버튼 실패: {_e}")

        # 성공 판정 (7초)
        import re as _re, time as _t
        _write_url = site_cfg.get("write_url", "")
        _ok = False
        _t0 = _t.time()
        while _t.time() - _t0 < 7:
            _cur = driver.current_url
            if _re.search(r"ab-\d+-\d+", _cur): _ok = True; break
            if _write_url and _write_url not in _cur and "ab-" in _cur: _ok = True; break
            _t.sleep(0.4)
        dismiss_alert(driver)
        _url = driver.current_url
        dbg(f"[STEP12] 최종 URL: {_url}")
        if _ok or _re.search(r"ab-\d+-\d+", _url):
            cb("SUCCESS", f"게시 완료 → {_url}")
        else:
            cb("SUCCESS", f"게시 완료(URL 확인 권장) → {_url}")

    #  마멘토(그누보드) 전용 포스팅 로직  ← 다른 사이트와 통합 금지
    # ──────────────────────────────────────────────────────────────
    def _post_gnuboard(self, driver, site_cfg, account, content,
                       cb, dbg, dismiss_alert, close_all_popups,
                       find_visible, text_to_html, acc_id, acc_pw):

        # ── STEP1  게시판(bo_table) 결정 ────────────────────────
        # 우선순위: 계정의 write_url > 계정의 category(한글·bo_table) > site_cfg default
        # ※ 항상 www.mamentor.co.kr 로 통일 (non-www와 쿠키가 분리되므로)
        def _norm_mam(url: str) -> str:
            if not url:
                return url
            url = url.replace("http://", "https://")
            if "://mamentor.co.kr" in url:
                url = url.replace("://mamentor.co.kr", "://www.mamentor.co.kr")
            return url

        raw_write_url = (account.get("write_url") or "").strip()
        if not raw_write_url:
            cat_raw = account.get("category", "").strip()
            if cat_raw:
                bo = MAMENTOR_BOARDS_R.get(cat_raw, cat_raw)
                raw_write_url = f"https://www.mamentor.co.kr/bbs/write.php?bo_table={bo}"
                dbg(f"[마멘토 STEP1] 카테고리 '{cat_raw}' → bo_table={bo}")
            else:
                raw_write_url = site_cfg.get("write_url", "").strip()
        if not raw_write_url:
            raise Exception("write_url 이 없습니다 – 계정의 [글쓰기 URL] 또는 [카테고리]를 지정하세요")

        write_url = _norm_mam(raw_write_url)

        # bo_table 추출 (board 목록 URL 생성용)
        import re as _re
        _bo_m = _re.search(r"bo_table=([\w]+)", write_url)
        bo_table = _bo_m.group(1) if _bo_m else ""
        board_url = (f"https://www.mamentor.co.kr/bbs/board.php?bo_table={bo_table}"
                     if bo_table else "")
        dbg(f"[마멘토 STEP1] bo_table={bo_table}")
        dbg(f"[마멘토 STEP1] board_url={board_url}")
        dbg(f"[마멘토 STEP1] write_url={write_url}")

        # ── STEP2  로그인 (항상 www 도메인으로 강제) ─────────────────
        # ※ sites.json에 non-www가 저장되어 있어도 여기서 무조건 www로 오버라이드
        # ※ mamentor.co.kr 쿠키 도메인이 www와 분리되므로 처음부터 www에서 로그인해야 함
        _www_site_cfg = dict(site_cfg)
        _www_site_cfg["main_url"] = "https://www.mamentor.co.kr"
        dbg("[마멘토 STEP2] www 도메인으로 강제 로그인 시도")
        self._login_common(driver, _www_site_cfg, acc_id, acc_pw,
                           cb, dbg, dismiss_alert, close_all_popups, find_visible)

        # ── STEP2.5  로그인 쿠키 안정화 + non-www 쿠키 브릿지 ──────
        # non-www에서 발급된 쿠키가 있을 경우 www 도메인에도 복사
        dbg("[마멘토 STEP2.5] 쿠키 브릿지 처리 시작")
        time.sleep(0.5)
        try:
            _all_cookies = driver.get_cookies()
            _bridged = 0
            for _ck in _all_cookies:
                _dom = _ck.get("domain", "")
                # non-www 도메인 쿠키를 www 도메인에도 복사
                if "mamentor.co.kr" in _dom and not _dom.startswith("www") and not _dom.startswith("."):
                    _new_ck = dict(_ck)
                    _new_ck["domain"] = "www.mamentor.co.kr"
                    try:
                        # www 페이지에서 쿠키 주입 (현재 www에 있어야 함)
                        driver.add_cookie(_new_ck)
                        _bridged += 1
                    except Exception as _ce:
                        dbg(f"[마멘토 STEP2.5] 쿠키 브릿지 실패: {_ck.get('name')} → {_ce}")
            dbg(f"[마멘토 STEP2.5] 쿠키 브릿지 완료 ({_bridged}개 복사)")
        except Exception as _be:
            dbg(f"[마멘토 STEP2.5] 쿠키 브릿지 오류 (무시): {_be}")

        # www 메인으로 이동해 쿠키 적용 확인
        dbg("[마멘토 STEP2.5] www 메인 재진입으로 세션 확인")
        driver.get("https://www.mamentor.co.kr")
        time.sleep(2)
        dismiss_alert(driver)
        close_all_popups(driver)
        dbg(f"[마멘토 STEP2.5] 완료 (URL: {driver.current_url})")

        # ── STEP3  게시판 목록 → 글쓰기 버튼 클릭 ───────────────
        # 다이렉트 write.php 이동 대신 board 목록에서 버튼 클릭 방식 사용
        if board_url:
            dbg(f"[마멘토 STEP3] 게시판 목록 이동: {board_url}")
            driver.get(board_url)
            time.sleep(2)
            dismiss_alert(driver)
            dbg(f"[마멘토 STEP3] 목록 로드 (URL: {driver.current_url})")

            # 글쓰기 버튼 순서대로 시도
            _write_btn_sels = [
                "a.btn_write",
                ".btn_write",
                f"a[href*='write.php?bo_table={bo_table}']",
                "a[href*='write.php']",
            ]
            _btn_clicked = False
            for _sel in _write_btn_sels:
                try:
                    _wbtn = WebDriverWait(driver, 4).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, _sel))
                    )
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", _wbtn)
                    time.sleep(0.3)
                    driver.execute_script("arguments[0].click();", _wbtn)
                    dbg(f"[마멘토 STEP3] 글쓰기 버튼 클릭 완료 (셀렉터: {_sel})")
                    _btn_clicked = True
                    time.sleep(2)
                    dismiss_alert(driver)
                    break
                except Exception:
                    continue

            if not _btn_clicked:
                dbg(f"[마멘토 STEP3] 글쓰기 버튼 미발견 – write_url 직접 이동(fallback): {write_url}")
                driver.get(write_url)
                time.sleep(2.5)
                dismiss_alert(driver)
        else:
            dbg(f"[마멘토 STEP3] bo_table 없음 – write_url 직접 이동: {write_url}")
            driver.get(write_url)
            time.sleep(2.5)
            dismiss_alert(driver)

        # STEP3 완료: 로그인 페이지로 튕겼는지 확인
        _cur3 = driver.current_url
        dbg(f"[마멘토 STEP3] 도달 URL: {_cur3}")
        if "login" in _cur3.lower() and "write" not in _cur3.lower():
            # ── 방어 로직: www 도메인 쿠키 미적용 시 재로그인 후 글쓰기 URL 직접 이동
            dbg("[마멘토 STEP3] 로그인 리다이렉트 감지 → www 도메인 재로그인 시도")
            try:
                _www_site_cfg = dict(site_cfg)
                _www_site_cfg["main_url"] = "https://www.mamentor.co.kr"
                self._login_common(driver, _www_site_cfg, acc_id, acc_pw,
                                   cb, dbg, dismiss_alert, close_all_popups, find_visible)
                time.sleep(1)
                dbg(f"[마멘토 STEP3-재시도] write_url 직접 이동: {write_url}")
                driver.get(write_url)
                time.sleep(2.5)
                dismiss_alert(driver)
                _cur3 = driver.current_url
                dbg(f"[마멘토 STEP3-재시도] 도달 URL: {_cur3}")
            except Exception as _re:
                dbg(f"[마멘토 STEP3-재시도] 재로그인 실패: {_re}")
            # 재시도 후에도 로그인 리다이렉트면 최종 예외
            if "login" in _cur3.lower() and "write" not in _cur3.lower():
                raise Exception(
                    f"글쓰기 페이지 도달 실패 – 로그인 페이지로 리다이렉트: {_cur3}\n"
                    "계정 아이디/비밀번호를 확인하세요. (www/non-www 도메인 세션 문제일 수 있음)")


        # ── STEP4  제목 입력 ──────────────────────────────────────
        title_sel = site_cfg.get("title_sel", "#wr_subject")
        title_val = content.get("title", "")
        if title_sel and title_val:
            dbg(f"[마멘토 STEP4] 제목 입력: \"{title_val[:40]}\"")
            try:
                WebDriverWait(driver, 8).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, title_sel))
                )
                t_el = driver.find_element(By.CSS_SELECTOR, title_sel)
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", t_el)
                t_el.click(); t_el.clear(); t_el.send_keys(title_val)
                dbg("[마멘토 STEP4] 제목 입력 완료")
            except Exception as e:
                raise Exception(f"제목 입력 실패 (셀렉터: {title_sel}) [{type(e).__name__}] → {e}")

        # ── STEP4.5  게시판 카테고리 (ca_name <select>) ──────────
        cat_sel = site_cfg.get("cat_sel", "").strip()
        if cat_sel:
            try:
                from selenium.webdriver.support.ui import Select as _Sel
                cat_el = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, cat_sel))
                )
                sel_obj = _Sel(cat_el)
                # 첫 번째 유효 옵션(value가 빈 문자열이 아닌) 자동 선택
                opts = [o for o in sel_obj.options if o.get_attribute("value").strip()]
                if opts:
                    sel_obj.select_by_value(opts[0].get_attribute("value"))
                    dbg(f"[마멘토 STEP4.5] 카테고리 선택: {opts[0].text} (value={opts[0].get_attribute('value')})")
                else:
                    dbg("[마멘토 STEP4.5] 카테고리 옵션 없음 – 건너뜀")
            except Exception as e:
                dbg(f"[마멘토 STEP4.5] 카테고리 처리 실패 [{type(e).__name__}]: {e} – 계속 진행")

        # ── STEP5  본문 (CKEditor4) ───────────────────
        body_raw = content.get("body", "")
        body = text_to_html(body_raw)

        dbg(f"[마멘토 STEP5] 본문 길이: {len(body)} bytes (textarea maxlength=65536)")

        dbg("[마멘토 STEP5] CKEditor4 본문 삽입 시도...")
        try:
            # ① textarea maxlength 제거 (65536 제한 해제)
            driver.execute_script(
                "var ta=document.getElementById('wr_content');"
                "if(ta){ta.removeAttribute('maxlength');"
                "Object.defineProperty(ta,'maxLength',{value:999999999,writable:true,configurable:true});}")
            dbg("[마멘토 STEP5] textarea maxlength 제거 완료")

            # ② CKEditor4 준비 대기 (최대 8초)
            for _ck_wait in range(16):
                _ck_ready = driver.execute_script(
                    "try{return typeof CKEDITOR!=='undefined'&&"
                    "Object.keys(CKEDITOR.instances).length>0;}catch(e){return false;}")
                if _ck_ready:
                    break
                time.sleep(0.5)
            dbg(f"[마멘토 STEP5] CKEditor4 준비 완료 (대기: {_ck_wait * 0.5:.1f}초)")

            # ③ setData + textarea 동기화
            _js_set = (
                "try{"
                "var inst=CKEDITOR.instances['wr_content']"
                "||CKEDITOR.instances[Object.keys(CKEDITOR.instances)[0]];"
                "if(!inst)return 'failed:no-instance';"
                "inst.setData(arguments[0]);"
                "var ta=document.getElementById('wr_content');"
                "if(ta){ta.removeAttribute('maxlength');ta.value=arguments[0];}"
                "return 'cke-ok:'+inst.name+':len='+arguments[0].length;"
                "}catch(e){return 'failed:'+String(e);}"
            )
            result = driver.execute_script(_js_set, body)
            dbg(f"[마멘토 STEP5] CKEditor4 결과: {result}")

            if str(result).startswith("failed"):
                # ④ 폴백: textarea 직접 입력
                dbg("[마멘토 STEP5] CKEditor4 실패 – textarea 폴백 시도")
                ta_sel = site_cfg.get("editor_sel", "#wr_content")
                try:
                    ta = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ta_sel))
                    )
                    driver.execute_script(
                        "arguments[0].removeAttribute('maxlength');arguments[0].value=arguments[1];",
                        ta, body)
                    dbg(f"[마멘토 STEP5] textarea 폴백 완료: {ta_sel}")
                except Exception as te:
                    raise Exception(f"CKEditor4·textarea 모두 실패: cke={result}, ta={te}")
        except Exception as e:
            raise Exception(f"본문 삽입 실패 [{type(e).__name__}]: {e}")

        # ── STEP6  부가 필드 (field_map 있으면 사용) ──────────────
        for acc_key, input_name in site_cfg.get("field_map", {}).items():
            val = (account.get(acc_key) or "").strip()
            if val:
                try:
                    el = WebDriverWait(driver, 4).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, f"input[name='{input_name}']"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                    el.clear(); el.send_keys(val)
                    dbg(f"[마멘토 STEP6] 부가필드 {input_name}: {val}")
                except Exception as e:
                    dbg(f"[마멘토 STEP6] 부가필드 {input_name} 실패 [{type(e).__name__}]: {e}")

        # ── STEP6.5  링크1 / 링크2 (wr_link1, wr_link2) ─────────
        link1_sel = site_cfg.get("link1_sel", "").strip()
        link2_sel = site_cfg.get("link2_sel", "").strip()
        link1_val = (account.get("link1") or content.get("link1") or "").strip()
        link2_val = (account.get("link2") or content.get("link2") or "").strip()
        for _lsel, _lval, _lname in [
            (link1_sel, link1_val, "링크1(wr_link1)"),
            (link2_sel, link2_val, "링크2(wr_link2)"),
        ]:
            if _lsel and _lval:
                try:
                    _lel = WebDriverWait(driver, 4).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, _lsel))
                    )
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", _lel)
                    _lel.clear(); _lel.send_keys(_lval)
                    dbg(f"[마멘토 STEP6.5] {_lname} 입력: {_lval}")
                except Exception as e:
                    dbg(f"[마멘토 STEP6.5] {_lname} 입력 실패 [{type(e).__name__}]: {e} – 건너뜀")
            elif _lsel:
                dbg(f"[마멘토 STEP6.5] {_lname} 값 없음 – 건너뜀")

        # ── STEP7  게시 버튼 ──────────────────────────────────────
        dismiss_alert(driver)
        submit_sel = site_cfg.get("submit_sel", "#btn_submit")
        dbg(f"[마멘토 STEP7] 등록 버튼 클릭 ({submit_sel})")
        try:
            btn = find_visible(driver, submit_sel, timeout=8)
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
            time.sleep(0.3)
            driver.execute_script("arguments[0].click();", btn)
            dbg("[마멘토 STEP7] 클릭 완료 – 응답 대기 중...")
            time.sleep(3)
            dismiss_alert(driver)
        except Exception as e:
            raise Exception(f"등록 버튼 클릭 실패 ({submit_sel}) [{type(e).__name__}] → {e}")

        success_pat = site_cfg.get("success_pat", "wr_id=")
        cur_url = driver.current_url
        dbg(f"[마멘토 STEP7] 게시 후 URL: {cur_url}")
        if success_pat and success_pat in cur_url:
            cb("SUCCESS", f"게시 완료 → {cur_url}")
        else:
            cb("SUCCESS", f"게시 완료(URL 패턴 미일치, 수동 확인 권장) → {cur_url}")

    # ──────────────────────────────────────────────────────────────
    #  투잡커넥트 전용 포스팅 로직 (Summernote 에디터)
    #  ★ 실제 HTML 확인: $('#summernote').summernote({...}) 사용
    # ──────────────────────────────────────────────────────────────
    def _post_summernote(self, driver, site_cfg, account, content,
                         cb, dbg, dismiss_alert, close_all_popups,
                         find_visible, text_to_html, acc_id, acc_pw):

        # ── STEP1  로그인 ─────────────────────────────────────────
        self._login_common(driver, site_cfg, acc_id, acc_pw,
                           cb, dbg, dismiss_alert, close_all_popups, find_visible)

        # ── STEP2  글쓰기 페이지 이동 ────────────────────────────
        write_url = site_cfg.get("write_url", "").strip()
        if not write_url:
            raise Exception("write_url 이 설정되지 않았습니다")
        dbg(f"[투잡 STEP2] 글쓰기 페이지 이동: {write_url}")
        driver.get(write_url)
        time.sleep(2.5)
        dismiss_alert(driver)
        dbg(f"[투잡 STEP2] 글쓰기 페이지 로드 완료 (URL: {driver.current_url})")

        # ── STEP3  분류(카테고리) 드롭다운 선택 ──────────────────
        cat_sel = site_cfg.get("cat_sel", "").strip()
        if cat_sel:
            cat_val = (account.get("category") or
                       site_cfg.get("cat_default", "") or "").strip()
            dbg(f"[투잡 STEP3] 분류 선택 시도: '{cat_val}' (셀렉터: {cat_sel})")
            try:
                from selenium.webdriver.support.ui import Select as _Select
                WebDriverWait(driver, 6).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, cat_sel))
                )
                cat_el = driver.find_element(By.CSS_SELECTOR, cat_sel)
                sel_obj = _Select(cat_el)
                if cat_val:
                    try:
                        sel_obj.select_by_value(cat_val)
                        dbg(f"[투잡 STEP3] 분류 선택 완료 (value): {cat_val}")
                    except Exception:
                        try:
                            sel_obj.select_by_visible_text(cat_val)
                            dbg(f"[투잡 STEP3] 분류 선택 완료 (text): {cat_val}")
                        except Exception as _ce:
                            dbg(f"[투잡 STEP3] 분류 선택 실패 (무시): {_ce}")
                else:
                    opts = sel_obj.options
                    if len(opts) > 1:
                        sel_obj.select_by_index(1)
                        dbg(f"[투잡 STEP3] 분류 기본 선택: {opts[1].text}")
                time.sleep(0.3)
            except Exception as e:
                dbg(f"[투잡 STEP3] 분류 셀렉터 오류 (무시): {e}")

        # ── STEP4  제목 입력 ──────────────────────────────────────
        title_sel = site_cfg.get("title_sel", "#wr_subject")
        title_val = content.get("title", "")
        if title_sel and title_val:
            dbg(f"[투잡 STEP4] 제목 입력: \"{title_val[:40]}\"")
            try:
                WebDriverWait(driver, 8).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, title_sel))
                )
                t_el = driver.find_element(By.CSS_SELECTOR, title_sel)
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", t_el)
                t_el.click(); t_el.clear(); t_el.send_keys(title_val)
                dbg("[투잡 STEP4] 제목 입력 완료")
            except Exception as e:
                raise Exception(f"제목 입력 실패 (셀렉터: {title_sel}) [{type(e).__name__}] → {e}")

        # ── STEP5  본문 (Summernote) ────────────────────
        body = text_to_html(content.get("body", ""))
        dbg("[투잡 STEP5] Summernote 에디터 대기 중 (최대 12초)...")
        try:
            # .note-editable 대기 – 없어도 continue (fallback으로 처리)
            _has_note_editable = False
            try:
                WebDriverWait(driver, 12).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".note-editable"))
                )
                _has_note_editable = True
                time.sleep(1.2)
                dbg("[투잡 STEP5] Summernote 에디터 발견 – 본문 삽입 시작")
            except Exception:
                dbg("[투잡 STEP5] .note-editable 없음 – textarea/직접삽입 fallback 시도...")

            injected = driver.execute_script("""
                var html = arguments[0];
                // 1) jQuery summernote API: #summernote (투잡커넥트 기본 ID)
                if (typeof $ !== 'undefined') {
                    var snEl = document.getElementById('summernote');
                    if (snEl) {
                        try { $('#summernote').summernote('code', html); return 'summernote-id-ok'; }
                        catch(e) { /* fall through */ }
                    }
                    // 2) [id^="smNote-"] 동적 ID
                    var snDiv = document.querySelector('[id^="smNote-"]');
                    if (snDiv) {
                        try { $(snDiv).summernote('code', html); return 'smNote-api-ok'; }
                        catch(e) { /* fall through */ }
                    }
                    // 3) .note-editable 직접 참조
                    var edEl = document.querySelector('.note-editable');
                    if (edEl) {
                        try { $(edEl).summernote('code', html); return 'edSel-api-ok'; }
                        catch(e) { /* fall through */ }
                    }
                }
                // 4) .note-editable innerHTML 직접 삽입 + textarea 동기화
                var editable = document.querySelector('.note-editable');
                if (editable) {
                    editable.focus();
                    editable.innerHTML = html;
                }
                // 5) textarea 직접 입력 (Summernote 없을 때 fallback)
                var ta = document.getElementById('wr_content')
                      || document.querySelector('textarea[name="wr_content"]')
                      || document.querySelector('textarea[id^="oEdit-"]')
                      || document.querySelector('textarea.summernote')
                      || document.querySelector('textarea[name*="content"]');
                if (ta) {
                    ta.value = html;
                    try { ta.dispatchEvent(new Event('input',{bubbles:true})); } catch(e){}
                    try { ta.dispatchEvent(new Event('change',{bubbles:true})); } catch(e){}
                    if (editable) {
                        try { editable.dispatchEvent(new Event('input',{bubbles:true})); } catch(e){}
                        try { editable.dispatchEvent(new Event('change',{bubbles:true})); } catch(e){}
                    }
                    return editable ? 'innerHTML+ta-ok' : 'ta-only-ok';
                }
                if (editable) {
                    try { editable.dispatchEvent(new Event('input',{bubbles:true})); } catch(e){}
                    try { editable.dispatchEvent(new Event('change',{bubbles:true})); } catch(e){}
                    return 'innerHTML-ok(no-ta)';
                }
                return 'failed:no-editor-found';
            """, body)
            dbg(f"[투잡 STEP5] 본문 삽입 결과: {injected}")
            if str(injected).startswith("failed"):
                raise Exception(f"본문 삽입 실패 – 에디터를 찾을 수 없음: {injected}")
            time.sleep(0.5)
        except Exception as e:
            raise Exception(f"본문 에디터 처리 실패 [{type(e).__name__}]: {e}")

        # ── STEP6  부가 필드 (field_map) ─────────────────────────
        for acc_key, input_name in site_cfg.get("field_map", {}).items():
            val = (account.get(acc_key) or "").strip()
            if val:
                try:
                    el = WebDriverWait(driver, 4).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, f"input[name='{input_name}']"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                    el.clear(); el.send_keys(val)
                    dbg(f"[투잡 STEP6] 부가필드 {input_name}: {val}")
                except Exception as e:
                    dbg(f"[투잡 STEP6] 부가필드 {input_name} 실패: {e}")

        # ── STEP6.5  링크1 / 링크2 ────────────────────────────────
        link1_sel = site_cfg.get("link1_sel", "").strip()
        link2_sel = site_cfg.get("link2_sel", "").strip()
        link1_val = (account.get("link1") or content.get("link1") or "").strip()
        link2_val = (account.get("link2") or content.get("link2") or "").strip()
        for _lsel, _lval, _lname in [
            (link1_sel, link1_val, "링크1(wr_link1)"),
            (link2_sel, link2_val, "링크2(wr_link2)"),
        ]:
            if _lsel and _lval:
                try:
                    _lel = WebDriverWait(driver, 4).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, _lsel))
                    )
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", _lel)
                    _lel.clear(); _lel.send_keys(_lval)
                    dbg(f"[투잡 STEP6.5] {_lname} 입력: {_lval}")
                except Exception as e:
                    dbg(f"[투잡 STEP6.5] {_lname} 입력 실패 [{type(e).__name__}]: {e} – 건너뜀")
            elif _lsel:
                dbg(f"[투잡 STEP6.5] {_lname} 값 없음 – 건너뜀")

        # ── STEP7  게시 버튼 ──────────────────────────────────────
        dismiss_alert(driver)
        submit_sel = site_cfg.get("submit_sel", "#btn_submit")
        dbg(f"[투잡 STEP7] 등록 버튼 클릭 ({submit_sel})")
        try:
            btn = find_visible(driver, submit_sel, timeout=8)
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
            time.sleep(0.3)
            driver.execute_script("arguments[0].click();", btn)
            dbg("[투잡 STEP7] 클릭 완료 – 응답 대기 중...")
            time.sleep(3)
            dismiss_alert(driver)
        except Exception as e:
            raise Exception(f"등록 버튼 클릭 실패 ({submit_sel}) [{type(e).__name__}] → {e}")

        success_pat = site_cfg.get("success_pat", "wr_id=")
        cur_url = driver.current_url
        dbg(f"[투잡 STEP7] 게시 후 URL: {cur_url}")
        if success_pat and success_pat in cur_url:
            cb("SUCCESS", f"게시 완료 → {cur_url}")
        else:
            cb("SUCCESS", f"게시 완료(URL 패턴 미일치, 수동 확인 권장) → {cur_url}")

    # ──────────────────────────────────────────────────────────────
    #  투잡커넥트·비즈모아·셀프모아 (SmartEditor2) 공용 로직
    # ──────────────────────────────────────────────────────────────
    def _post_smarteditor(self, driver, site_cfg, account, content,
                          cb, dbg, dismiss_alert, close_all_popups,
                          find_visible, text_to_html, acc_id, acc_pw):

        # ── write_url 도메인 정규화 (계정에 non-www 저장되어도 www로 보정) ──
        _raw_wu = (account.get("write_url") or site_cfg.get("write_url", "")).strip()
        _main_dom = re.sub(r"https?://", "", site_cfg.get("main_url", "").rstrip("/"))
        if _raw_wu and _main_dom:
            _raw_wu = re.sub(
                r"https?://" + re.escape(_main_dom.lstrip("www.").lstrip(".")),
                "http://" + _main_dom if _main_dom.startswith("m.") else "https://" + _main_dom,
                _raw_wu, flags=re.IGNORECASE
            )
        site_cfg = dict(site_cfg)
        if _raw_wu:
            site_cfg["write_url"] = _raw_wu

        self._login_common(driver, site_cfg, acc_id, acc_pw,
                           cb, dbg, dismiss_alert, close_all_popups, find_visible)

        # ── 셀프모아: write_url 없을 때 category 로 bo_table 자동 결정 ──────────
        # 마멘토의 MAMENTOR_BOARDS_R 로직과 동일한 패턴
        # ※ site_cfg에 site_name 키가 없을 수 있으므로 main_url로도 보조 식별
        _site_name = (site_cfg.get("site_name") or
                      account.get("site") or
                      ("셀프모아" if "selfmoa" in site_cfg.get("main_url", "").lower() else ""))
        dbg(f"[셀프모아 분기] _site_name={_site_name!r}  main_url={site_cfg.get('main_url','')}")
        if not site_cfg.get("write_url", "").strip() and _site_name == "셀프모아":
            _cat_raw = account.get("category", "").strip()
            if _cat_raw:
                # 한글 → bo_table 변환 (예: "블로그" → "blog")
                _bo = SELFMOA_BOARDS_R.get(_cat_raw, _cat_raw)
                _auto_wu = f"http://m.selfmoa.com/bbs/write.php?bo_table={_bo}"
                site_cfg = dict(site_cfg)
                site_cfg["write_url"] = _auto_wu
                dbg(f"[셀프모아] 카테고리 '{_cat_raw}' → bo_table={_bo} → write_url={_auto_wu}")
            else:
                dbg("[셀프모아] category 미지정 – write_url 자동 결정 불가")

        write_url = site_cfg.get("write_url", "").strip()
        if not write_url:
            raise Exception(
                "write_url 이 설정되지 않았습니다\n"
                "셀프모아: 계정 [카테고리] 필드에 블로그 / SNS / 기타 중 하나를 입력하세요"
            )
        dbg(f"[SmartEditor STEP7] 글쓰기 페이지 이동: {write_url}")
        driver.get(write_url)
        time.sleep(2)
        dismiss_alert(driver)

        # ── 분류(카테고리) 드롭다운 선택 ────────────────────────────
        cat_sel = site_cfg.get("cat_sel", "").strip()
        if cat_sel:
            # 셀프모아: category 필드는 board(게시판) 결정용이므로 ca_name에 쓰지 않음
            # → cat_default("기타") 고정 사용. 다른 사이트는 기존 방식 유지.
            _is_selfmoa_ca = "selfmoa" in site_cfg.get("main_url", "").lower()
            if _is_selfmoa_ca:
                cat_val = site_cfg.get("cat_default", "기타")
            else:
                cat_val = (account.get("category") or
                           site_cfg.get("cat_default", "") or "").strip()
            dbg(f"[SmartEditor STEP7.5] 분류 선택 시도: '{cat_val}' (셀렉터: {cat_sel})")
            try:
                from selenium.webdriver.support.ui import Select as _Select
                WebDriverWait(driver, 6).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, cat_sel))
                )
                cat_el = driver.find_element(By.CSS_SELECTOR, cat_sel)
                sel_obj = _Select(cat_el)
                if cat_val:
                    try:
                        sel_obj.select_by_value(cat_val)
                        dbg(f"[SmartEditor STEP7.5] 분류 선택 완료 (value): {cat_val}")
                    except Exception:
                        try:
                            sel_obj.select_by_visible_text(cat_val)
                            dbg(f"[SmartEditor STEP7.5] 분류 선택 완료 (text): {cat_val}")
                        except Exception as _ce:
                            dbg(f"[SmartEditor STEP7.5] 분류 선택 실패 (무시): {_ce}")
                else:
                    # 값이 없으면 두 번째 옵션(인덱스 1) 선택 (첫 번째는 보통 "선택하세요")
                    opts = sel_obj.options
                    if len(opts) > 1:
                        sel_obj.select_by_index(1)
                        dbg(f"[SmartEditor STEP7.5] 분류 기본 선택: {opts[1].text}")
                time.sleep(0.3)
            except Exception as e:
                dbg(f"[SmartEditor STEP7.5] 분류 셀렉터 오류 (무시): {e}")

        # ── 제목 입력 ────────────────────────────────────────────
        title_sel = site_cfg.get("title_sel", "#wr_subject")
        title_val = content.get("title", "")
        if title_sel and title_val:
            dbg(f"[SmartEditor STEP8] 제목 입력: {title_val[:30]}")
            try:
                WebDriverWait(driver, 8).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, title_sel))
                )
                t_el = driver.find_element(By.CSS_SELECTOR, title_sel)
                t_el.click(); t_el.clear(); t_el.send_keys(title_val)
            except Exception as e:
                raise Exception(f"제목 입력 실패: {e}")

        # 본문 (SmartEditor2)
        body = text_to_html(content.get("body", ""))
        dbg("[SmartEditor STEP9] SmartEditor2 에디터 로드 대기")
        # 에디터 iframe 이 렌더링될 때까지 최대 10초 대기
        try:
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script(
                    "return (typeof oEditors !== 'undefined' && oEditors.getById && "
                    "oEditors.getById['wr_content']) || "
                    "(typeof nhn !== 'undefined' && nhn.husky && "
                    "nhn.husky.EZCreator && nhn.husky.EZCreator.getSmartEditorList && "
                    "nhn.husky.EZCreator.getSmartEditorList().length > 0);"
                )
            )
            dbg("[SmartEditor STEP9] 에디터 로드 확인")
        except Exception:
            dbg("[SmartEditor STEP9] 에디터 로드 대기 타임아웃 – 직접 삽입 시도")

        dbg("[SmartEditor STEP9] SmartEditor2 본문 삽입")
        try:
            driver.execute_script("""
                // 방법1: oEditors.getById 방식 (투잡커넥트, 셀프모아, 비즈모아)
                if (typeof oEditors !== 'undefined' && oEditors.getById
                        && oEditors.getById['wr_content']) {
                    oEditors.getById['wr_content'].setIR(arguments[0]);
                    oEditors.getById['wr_content'].exec('UPDATE_CONTENTS_FIELD', []);
                    return;
                }
                // 방법2: EZCreator 방식 (그 외 SmartEditor2)
                try {
                    var eds = nhn.husky.EZCreator.getSmartEditorList();
                    if (eds && eds.length > 0) {
                        eds[0].setIR(arguments[0]);
                        return;
                    }
                } catch(e2) {}
                // 방법3: textarea 직접 값 삽입 (최후 fallback)
                var ta = document.querySelector('textarea[id="wr_content"], '
                        + 'textarea[name="wr_content"], '
                        + 'textarea[id*="content"], textarea[name*="content"]');
                if (ta) { ta.value = arguments[0]; }
            """, body)
            dbg("[SmartEditor STEP9] 본문 삽입 완료")
        except Exception as e:
            raise Exception(f"SmartEditor2 본문 삽입 실패: {e}")

        # 부가 필드
        for acc_key, input_name in site_cfg.get("field_map", {}).items():
            val = account.get(acc_key, "")
            if val:
                try:
                    el = driver.find_element(By.CSS_SELECTOR, f"input[name='{input_name}']")
                    el.clear(); el.send_keys(val)
                    dbg(f"[SmartEditor] 부가필드 {input_name}: {val}")
                except Exception as e:
                    dbg(f"[SmartEditor] 부가필드 {input_name} 실패: {e}")

        # 링크 #1/#2: 계정의 link1/link2 → 직접 입력 (없으면 company/contact 폴백)
        for acc_key_primary, acc_key_fallback, sel_key in [
            ("link1", "company",  "link1_sel"),
            ("link2", "contact",  "link2_sel"),
        ]:
            sel = site_cfg.get(sel_key, "")
            val = account.get(acc_key_primary, "") or account.get(acc_key_fallback, "")
            if sel and val:
                try:
                    el = driver.find_element(By.CSS_SELECTOR, sel)
                    el.clear(); el.send_keys(val)
                    dbg(f"[SmartEditor] {sel_key} 입력: {val[:40]}")
                except Exception as e:
                    dbg(f"[SmartEditor] {sel_key} 실패 (무시): {e}")

        dismiss_alert(driver)
        submit_sel = site_cfg.get("submit_sel", "#btn_submit, input[name='submit_OK'], input[type='submit']")
        dbg(f"[SmartEditor STEP10] 게시 버튼 클릭: {submit_sel}")
        try:
            btn = find_visible(driver, submit_sel, timeout=8)
            driver.execute_script("arguments[0].click();", btn)
            time.sleep(3)
        except Exception as e:
            raise Exception(f"게시 버튼 클릭 실패: {e}")

        success_pat = site_cfg.get("success_pat", "wr_id=")
        cur_url = driver.current_url
        dbg(f"[SmartEditor STEP10] 게시 후 URL: {cur_url}")
        if success_pat and success_pat in cur_url:
            cb("SUCCESS", f"게시 완료 → {cur_url}")
        else:
            cb("SUCCESS", f"게시 완료(URL 패턴 미일치) → {cur_url}")


# ═══════════════════════════════════════════════════════════════════
#  메인 애플리케이션
# ═══════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Community Auto Poster v5.20")
        self.geometry("1280x820")
        self.minsize(1024, 680)
        self.configure(bg=PALETTE["bg"])

        # 데이터 로드
        self.accounts  = load_json(CFG_ACCOUNTS, [])
        self.contents  = load_json(CFG_CONTENTS, [])
        self.sites     = load_sites_merged()  # DEFAULT + 저장값 merge + 오타 자동 수정
        self.schedule  = load_json(CFG_SCHEDULE, DEFAULT_SCHEDULE)
        self.options   = load_json(CFG_OPTIONS,  DEFAULT_OPTIONS)
        self.jobs      = load_json(CFG_JOBS,     [])

        self.engine    = PostingEngine(self)
        self.engine.start()
        self._posting_results = []   # 실시간 결과 내역

        self._scheduler_running = False
        self._scheduler_thread  = None
        self._job_sched_threads = {}     # {job_name: stop_flag(Event)} 개별 스케줄 스레드

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # ── 프로그램 시작 시: 전역 or 개별 스케줄 자동 복원 ──────────
        self.after(500, self._restore_scheduler_on_startup)

    # ──────────────────────────────────────────────────────────────
    #  공통 스타일 헬퍼
    # ──────────────────────────────────────────────────────────────
    def _styled_frame(self, parent, bg=None, padx=0, pady=0, relief="flat", border=0):
        f = tk.Frame(parent, bg=bg or PALETTE["card"], relief=relief,
                     bd=border, padx=padx, pady=pady)
        return f

    def _card(self, parent, padx=16, pady=12):
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
                        font=(FONT_FAMILY, size, weight),
                        fg=color or PALETTE["text"],
                        bg=parent.cget("bg"), **kw)

    def _button(self, parent, text, command, color=None, text_color="#FFFFFF",
                size=9, width=None, **kw):
        cfg = dict(text=text, command=command,
                   font=(FONT_FAMILY, size, "bold"),
                   bg=color or PALETTE["primary"],
                   fg=text_color,
                   activebackground=color or PALETTE["primary"],
                   activeforeground=text_color,
                   relief="flat", cursor="hand2",
                   padx=12, pady=5, bd=0)
        if width: cfg["width"] = width
        cfg.update(kw)
        b = tk.Button(parent, **cfg)
        # hover
        orig = color or PALETTE["primary"]
        def on_enter(e): b.config(bg=self._darken(orig))
        def on_leave(e): b.config(bg=orig)
        b.bind("<Enter>", on_enter)
        b.bind("<Leave>", on_leave)
        return b

    def _darken(self, hex_color, factor=0.85):
        hex_color = hex_color.lstrip("#")
        r,g,b = int(hex_color[0:2],16), int(hex_color[2:4],16), int(hex_color[4:6],16)
        return "#{:02x}{:02x}{:02x}".format(int(r*factor),int(g*factor),int(b*factor))

    def _separator(self, parent, orient="horizontal", color=None):
        c = color or PALETTE["border"]
        if orient == "horizontal":
            return tk.Frame(parent, bg=c, height=1)
        return tk.Frame(parent, bg=c, width=1)

    def _badge(self, parent, text, color):
        f = tk.Frame(parent, bg=color, padx=6, pady=2)
        tk.Label(f, text=text, font=(FONT_FAMILY,8,"bold"),
                 fg="#fff", bg=color).pack()
        return f

    # ──────────────────────────────────────────────────────────────
    #  UI 구성
    # ──────────────────────────────────────────────────────────────
    def _build_ui(self):
        self._build_header()
        container = tk.Frame(self, bg=PALETTE["bg"])
        container.pack(fill="both", expand=True)
        self._build_sidebar(container)
        self._build_content(container)
        self._build_statusbar()
        # 첫 탭
        self._show_tab("jobs")

    # ── 헤더 ──────────────────────────────────────────────────────
    def _build_header(self):
        hdr = tk.Frame(self, bg=PALETTE["sidebar"], height=56)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        # 로고 + 제목
        logo_frame = tk.Frame(hdr, bg=PALETTE["sidebar"])
        logo_frame.pack(side="left", padx=20)
        tk.Label(logo_frame, text="⚡", font=(FONT_FAMILY,18),
                 fg=PALETTE["primary"], bg=PALETTE["sidebar"]).pack(side="left")
        tk.Label(logo_frame, text=" Community Auto Poster",
                 font=(FONT_FAMILY,13,"bold"),
                 fg="#F1F5F9", bg=PALETTE["sidebar"]).pack(side="left")
        tk.Label(logo_frame, text=" v5.20",
                 font=(FONT_FAMILY,9),
                 fg=PALETTE["muted"], bg=PALETTE["sidebar"]).pack(side="left")

        # 상태 배지
        right = tk.Frame(hdr, bg=PALETTE["sidebar"])
        right.pack(side="right", padx=20)

        self._queue_var = tk.StringVar(value="대기 0")
        self._sched_var = tk.StringVar(value="스케줄 OFF")

        tk.Label(right, textvariable=self._queue_var,
                 font=(FONT_FAMILY,9), fg=PALETTE["muted"],
                 bg=PALETTE["sidebar"]).pack(side="right", padx=8)
        tk.Label(right, textvariable=self._sched_var,
                 font=(FONT_FAMILY,9), fg=PALETTE["muted"],
                 bg=PALETTE["sidebar"]).pack(side="right", padx=8)

    # ── 사이드바 ──────────────────────────────────────────────────
    def _build_sidebar(self, parent):
        sb = tk.Frame(parent, bg=PALETTE["sidebar"], width=200)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        tk.Frame(sb, bg=PALETTE["sidebar"], height=16).pack()

        self._nav_buttons = {}
        nav_items = [

            ("jobs",     "📋  작업 관리",  "계정×콘텐츠 조합"),
            ("accounts", "👤  계정 관리",  "계정 추가/수정"),
            ("contents", "📝  콘텐츠",     "글 템플릿 관리"),
            ("sites",    "⚙  사이트 설정","URL·셀렉터 편집"),
            ("options",  "🔧  옵션",       "실행 옵션"),
            ("logs",     "🗒  로그",       "결과 로그"),
            ("stats",    "📊  결과 통계",   "성공/실패 내역"),
        ]
        for key, label, tip in nav_items:
            btn = tk.Button(sb, text=f"  {label}",
                            font=(FONT_FAMILY, 10),
                            fg="#94A3B8", bg=PALETTE["sidebar"],
                            activeforeground="#FFFFFF",
                            activebackground=PALETTE["sidebar_h"],
                            relief="flat", anchor="w", cursor="hand2",
                            padx=16, pady=10,
                            command=lambda k=key: self._show_tab(k))
            btn.pack(fill="x")
            self._nav_buttons[key] = btn

        # 하단 버전
        tk.Frame(sb, bg=PALETTE["sidebar"]).pack(fill="y", expand=True)
        tk.Label(sb, text="© 2025 Auto Poster  v5.20",
                 font=(FONT_FAMILY,8), fg="#334155",
                 bg=PALETTE["sidebar"]).pack(pady=10)

    def _show_tab(self, key):
        for k, btn in self._nav_buttons.items():
            if k == key:
                btn.config(fg="#FFFFFF", bg=PALETTE["sidebar_h"],
                           font=(FONT_FAMILY,10,"bold"))
            else:
                btn.config(fg="#94A3B8", bg=PALETTE["sidebar"],
                           font=(FONT_FAMILY,10))
        self._content_area.pack_forget()
        for w in self._tab_frames.values():
            w.pack_forget()
        frame = self._tab_frames.get(key)
        if frame:
            frame.pack(fill="both", expand=True)
        self._content_area.pack(fill="both", expand=True)
        # refresh
        refresh = getattr(self, f"_refresh_{key}", None)
        if refresh: refresh()

    # ── 콘텐츠 영역 ───────────────────────────────────────────────
    def _build_content(self, parent):
        self._content_area = tk.Frame(parent, bg=PALETTE["bg"])
        self._content_area.pack(fill="both", expand=True)
        self._tab_frames = {}

        builders = {

            "jobs":     self._build_jobs_tab,
            "accounts": self._build_accounts_tab,
            "contents": self._build_contents_tab,
            "sites":    self._build_sites_tab,
            "options":  self._build_options_tab,
            "logs":     self._build_logs_tab,
            "stats":    self._build_stats_tab,
        }
        for key, builder in builders.items():
            f = tk.Frame(self._content_area, bg=PALETTE["bg"])
            self._tab_frames[key] = f
            builder(f)


    # ══════════════════════════════════════════════════════════════
    #  도움말 팝업
    # ══════════════════════════════════════════════════════════════
    _HELP_DATA = {
        "jobs": {
            "title": "📋  작업 관리 – 사용 방법",
            "steps": [
                ("작업이란?",
                 "작업 = 계정 1개 + 콘텐츠 1개의 조합입니다.\n"
                 "미리 설정해두면 버튼 한 번으로 바로 실행하거나 개별 스케줄로 자동 반복할 수 있어요."),
                ("① 작업 추가",
                 "+ 작업 추가 버튼을 클릭하면 설정 창이 열립니다.\n"
                 "계정, 사용할 글을 선택 후 저장하세요.\n"
                 "작업 설정 창에서 [개별 스케줄 활성화]를 체크하면\n"
                 "이 작업만의 독립 스케줄을 지정할 수 있습니다."),
                ("② 작업 실행",
                 "목록에서 원하는 작업을 선택 후\n"
                 "▶ 선택 즉시 실행 또는 ▶▶ 전체 실행 버튼을 누르세요.\n"
                 "동시에 트리거된 작업들은 순서대로 큐에 쌓여 순차 실행됩니다."),
                ("③ 활성/비활성",
                 "⊙ 활성 토글 버튼으로 특정 작업만 끄거나 켤 수 있습니다.\n"
                 "비활성 작업은 전체 실행 및 스케줄 실행 시 건너뜁니다."),
                ("④ 스케줄 상태 아이콘",
                 "작업 목록의 스케줄 컬럼에서 상태를 확인하세요:\n"
                 "🟢 실행 중 (개별 스케줄 활성, 스레드 동작 중)\n"
                 "🟡 설정됨 (스케줄 저장됨, 현재 일시정지)\n"
                 "⚫ OFF (개별 스케줄 없음)\n"
                 "⚪ 전역 (전역 스케줄 탭 설정 따름)"),
            ],
            "tips": [
                "💡 동일 계정으로 다른 글을 쓰려면 작업을 복제(⧉)하세요.",
                "💡 3h 작업과 6h 작업이 동시에 트리거되면 큐에 순서대로 쌓여 순차 실행됩니다.",
                                "💡 작업 이름을 직관적으로 지으면 관리가 편합니다.",
            ]
        },
        "accounts": {
            "title": "👤  계정 관리 – 사용 방법",
            "steps": [
                ("계정이란?",
                 "글을 올릴 커뮤니티 사이트의 아이디/비밀번호 정보입니다.\n"
                 "사이트마다 별도로 등록해야 합니다."),
                ("① 계정 추가",
                 "+ 계정 추가 버튼을 클릭하세요.\n"
                 "사이트 선택 → 아이디 → 비밀번호 입력 후 저장합니다."),
                ("② 계정 수정/삭제",
                 "목록에서 계정을 클릭하여 선택한 뒤\n"
                 "✎ 수정 또는 ✕ 삭제 버튼을 누르세요."),
                ("③ CSV 일괄 등록",
                 "계정이 많다면 📥 CSV 가져오기로 한 번에 등록할 수 있습니다.\n"
                 "먼저 📤 CSV 내보내기로 양식을 다운받아 작성하세요."),
                ("④ 지원 사이트",
                 "현재 지원 사이트 (v5.20 기준):\n"
                 "• 마멘토 (CKEditor4)\n"
                 "• 투잡커넥트 (SmartEditor2) ← v5.20 에디터 변경\n"
                 "• 비즈모아 (SmartEditor2)\n"
                 "• 셀프모아 (SmartEditor2)\n"
                 "• 아이보스 (SmartEditor2)"),
            ],
            "tips": [
                "💡 ⊙ 활성화 토글로 특정 계정만 일시 비활성화할 수 있습니다.",
                "💡 비밀번호는 암호화 없이 저장되므로 공유 PC 주의!",
                "💡 같은 사이트에 계정 여러 개를 등록할 수 있습니다.",
            ]
        },
        "contents": {
            "title": "📝  콘텐츠 템플릿 – 사용 방법",
            "steps": [
                ("템플릿이란?",
                 "여러 계정에 공통으로 쓸 글(제목+본문)을 미리 저장한 것입니다.\n"
                 "한 번 만들어두면 반복 사용할 수 있어요."),
                ("① 새 템플릿 만들기",
                 "왼쪽 목록 상단의 + 버튼을 누르면 새 템플릿이 생성됩니다.\n"
                 "제목·태그·본문을 작성한 뒤 💾 저장 버튼을 누르세요."),
                ("② HTML 본문",
                 "본문은 HTML 형식도 지원합니다.\n"
                 "빠른삽입 버튼(<br>, <b>, <a> 등)으로 쉽게 입력하세요."),
            ],
            "tips": [
                "💡 템플릿은 여러 개 만들어 목적별로 사용할 수 있습니다.",
                "💡 복사 버튼으로 기존 템플릿을 빠르게 복제하세요.",
            ]
        },
        "sites": {
            "title": "⚙  사이트 설정 – 사용 방법",
            "steps": [
                ("⚠ 주의",
                 "이 탭은 고급 설정 항목입니다.\n"
                 "잘못 변경하면 포스팅이 작동하지 않을 수 있습니다.\n"
                 "변경 전 반드시 백업(↺ 기본값 복원)을 확인하세요."),
                ("사이트 설정이란?",
                 "각 커뮤니티 사이트의 로그인 URL, 글쓰기 URL,\n"
                 "입력 셀렉터(CSS), 에디터 타입, 성공 패턴 등을 관리합니다."),
                ("에디터 타입 안내 (v5.20)",
                 "• smarteditor2: 투잡커넥트·비즈모아·셀프모아·아이보스\n"
                 "  → oEditors API로 본문 주입\n"
                 "• ckeditor4: 마멘토\n"
                 "  → CKEDITOR.instances API로 본문 주입\n"
                 "• summernote: 기타 사이트\n"
                 "  → jQuery .summernote('code', html) 주입"),
                ("기본값 복원",
                 "설정이 꼬였을 경우 ↺ 기본값 복원 버튼을 누르면\n"
                 "초기 상태로 되돌아갑니다."),
            ],
            "tips": [
                "💡 사이트가 업데이트되면 URL이나 셀렉터가 바뀔 수 있습니다.",
                "💡 처음에는 변경하지 말고 기본값을 그대로 사용하세요.",
                "💡 투잡커넥트는 v5.20부터 SmartEditor2로 변경되었습니다.",
            ]
        },
        "schedule": {
            "title": "🕐  자동 스케줄 – 사용 방법",
            "steps": [
                ("스케줄 구조 (v5.18 개편)",
                 "두 가지 스케줄이 독립적으로 동작합니다:\n"
                 "① 전역 스케줄: 스케줄 탭에서 설정 – 활성 작업 전체를 주기적으로 실행\n"
                 "② 개별 스케줄: 각 작업 설정 창에서 설정 – 해당 작업만 독립 실행\n"
                 "전역 OFF여도 개별 스케줄은 계속 동작합니다."),
                ("① 개별 스케줄 설정 (권장)",
                 "작업 추가/수정 창 → [개별 스케줄 활성화] 체크\n"
                 "→ 실행 모드·간격·요일 설정 후 저장\n"
                 "저장 즉시 해당 작업 전용 스레드가 시작됩니다.\n"
                 "다른 작업 스케줄에는 영향을 주지 않습니다."),
                ("② 실행 모드",
                 "간격 실행: N시간(±분 랜덤 편차)마다 실행\n"
                 "  예) 3시간 ±30분 → 2.5~3.5시간마다 실행\n"
                 "시간대 지정: 매일 특정 시각에 실행\n"
                 "  예) 09:00, 18:00 → 하루 2회 자동 실행"),
                ("③ 요일 설정",
                 "원하는 요일만 선택 가능 (월·화·수·목·금·토·일)\n"
                 "선택한 요일에만 스케줄이 트리거됩니다."),
                ("④ 겹치는 작업 처리",
                 "여러 작업이 동시에 트리거되더라도\n"
                 "PostingEngine 내부 큐에 순서대로 쌓이고\n"
                 "앞 작업이 완료된 후 다음 작업이 자동 시작됩니다.\n"
                 "병렬 실행 없이 항상 순차 처리됩니다."),
                ("⑤ 앱 재시작 후 자동 복원",
                 "개별 스케줄이 활성화된 작업은\n"
                 "프로그램을 껐다 켜도 자동으로 스케줄이 복원됩니다."),
            ],
            "tips": [
                "💡 작업A(3h)·작업B(6h)처럼 겹쳐도 큐 순서로 안전하게 처리됩니다.",
                "💡 전역 스케줄을 끄더라도 개별 스케줄 작업은 계속 실행됩니다.",
                "💡 작업 삭제 시 해당 스케줄 스레드도 자동으로 정리됩니다.",
                "💡 결과는 로그 탭에서 [SCHED:작업명] 태그로 확인할 수 있습니다.",
                "💡 PC 절전 모드나 화면보호기 상태에도 실행됩니다.",
            ]
        },
        "options": {
            "title": "🔧  실행 옵션 – 사용 방법",
            "steps": [
                ("딜레이(지연 시간)",
                 "각 포스팅 사이에 기다리는 시간(초)입니다.\n"
                 "너무 짧으면 스팸으로 인식될 수 있어 최소 3초를 권장합니다."),
                ("실행 순서",
                 "순서대로: 작업 목록 순서대로 실행\n"
                 "랜덤: 작업 순서를 무작위로 섞어 실행"),
                ("변경 후 저장",
                 "옵션 변경 후 💾 저장 버튼을 눌러야 적용됩니다."),
            ],
            "tips": [
                "💡 딜레이를 너무 짧게 설정하면 사이트에서 차단될 수 있습니다.",
                "💡 랜덤 순서는 패턴을 숨겨 더 자연스럽게 보입니다.",
            ]
        },
        "logs": {
            "title": "🗒  실행 로그 – 사용 방법",
            "steps": [
                ("로그란?",
                 "포스팅 실행 결과가 시간순으로 기록되는 공간입니다.\n"
                 "성공/실패 여부와 상세 메시지를 확인할 수 있습니다."),
                ("색상 구분",
                 "🟢 초록(SUCCESS): 포스팅 성공\n"
                 "🔴 빨강(ERROR): 오류 발생\n"
                 "🟡 노랑(WARN): 경고 (성공했지만 확인 필요)\n"
                 "🔵 파랑(DEBUG): 상세 진행 정보\n"
                 "⚪ INFO: 스케줄 트리거 등 시스템 메시지"),
                ("스케줄 로그 확인",
                 "[SCHED:작업명] 태그가 붙은 항목이 스케줄 자동 실행 기록입니다.\n"
                 "예) [SCHED:홍보글A] 스케줄 트리거 → 큐에 투입"),
                ("필터 사용",
                 "상단 필터 버튼으로 SUCCESS, ERROR 만 골라 볼 수 있습니다."),
                ("로그 파일",
                 "📁 로그 폴더 열기 버튼으로 날짜별 CSV 파일을 확인할 수 있습니다."),
            ],
            "tips": [
                "💡 오류가 발생하면 ERROR 필터로 원인 메시지를 확인하세요.",
                "💡 로그는 자동으로 날짜별 CSV 파일로도 저장됩니다.",
                "💡 투잡커넥트 오류 시 [투잡 STEP5] 이후 메시지를 확인하세요.",
            ]
        },
        "stats": {
            "title": "📊  결과 통계 – 사용 방법",
            "steps": [
                ("통계란?",
                 "포스팅 결과(성공/실패)를 한눈에 볼 수 있는 대시보드입니다.\n"
                 "실행 탭이나 작업 탭에서 포스팅하면 자동으로 기록됩니다."),
                ("① 오늘 실시간 확인",
                 "날짜 선택에서 '오늘 (실시간)'을 선택하면\n"
                 "현재 세션에서 실행한 결과가 바로 보입니다."),
                ("② 날짜별 과거 조회",
                 "드롭다운에서 날짜를 선택하면\n"
                 "그 날의 포스팅 기록을 불러옵니다."),
                ("③ CSV 내보내기",
                 "📤 CSV 내보내기 버튼으로 표 내용을 엑셀로 저장할 수 있습니다."),
            ],
            "tips": [
                "💡 성공률이 낮으면 계정 상태나 사이트 설정을 확인하세요.",
                "💡 표를 클릭하면 상세 결과 메시지를 볼 수 있습니다.",
            ]
        },
    }

    def _show_help(self, tab_key):
        """각 탭 전용 도움말 팝업"""
        data = self._HELP_DATA.get(tab_key)
        if not data:
            return

        win = tk.Toplevel(self)
        win.title(data["title"])
        win.geometry("560x520")
        win.resizable(False, False)
        win.configure(bg=PALETTE["bg"])
        win.grab_set()   # 모달

        # ── 헤더 ──
        hdr = tk.Frame(win, bg=PALETTE["primary"], padx=20, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text=data["title"],
                 font=(FONT_FAMILY, 13, "bold"),
                 fg="#FFFFFF", bg=PALETTE["primary"]).pack(anchor="w")

        # ── 스크롤 본문 ──
        body_outer = tk.Frame(win, bg=PALETTE["bg"])
        body_outer.pack(fill="both", expand=True, padx=0, pady=0)

        canvas = tk.Canvas(body_outer, bg=PALETTE["bg"],
                           highlightthickness=0)
        vsb = ttk.Scrollbar(body_outer, orient="vertical",
                            command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        scroll_frame = tk.Frame(canvas, bg=PALETTE["bg"])
        canvas_win = canvas.create_window((0, 0), window=scroll_frame,
                                          anchor="nw")

        def on_resize(e):
            canvas.itemconfig(canvas_win, width=e.width)
        canvas.bind("<Configure>", on_resize)

        def on_frame_configure(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
        scroll_frame.bind("<Configure>", on_frame_configure)

        # 마우스 휠
        def _on_mousewheel(e):
            canvas.yview_scroll(int(-1*(e.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        win.bind("<Destroy>", lambda e: canvas.unbind_all("<MouseWheel>"))

        # ── 단계별 내용 ──
        pad = tk.Frame(scroll_frame, bg=PALETTE["bg"])
        pad.pack(fill="both", expand=True, padx=20, pady=16)

        # 순서 단계 카드
        tk.Label(pad, text="📖  사용 순서",
                 font=(FONT_FAMILY, 10, "bold"),
                 fg=PALETTE["primary"], bg=PALETTE["bg"]).pack(anchor="w", pady=(0,8))

        for idx, (step_title, step_body) in enumerate(data["steps"], 1):
            step_card = tk.Frame(pad, bg=PALETTE["card"],
                                 highlightbackground=PALETTE["border"],
                                 highlightthickness=1)
            step_card.pack(fill="x", pady=4)
            inner = tk.Frame(step_card, bg=PALETTE["card"])
            inner.pack(fill="x", padx=14, pady=10)

            # 번호 원형
            num_bg = PALETTE["primary"] if idx > 0 else PALETTE["warning"]
            num_f = tk.Frame(inner, bg=num_bg, width=28, height=28)
            num_f.pack(side="left", anchor="nw")
            num_f.pack_propagate(False)
            tk.Label(num_f, text=str(idx),
                     font=(FONT_FAMILY, 9, "bold"),
                     fg="#fff", bg=num_bg).place(relx=.5, rely=.5, anchor="center")

            text_f = tk.Frame(inner, bg=PALETTE["card"])
            text_f.pack(side="left", fill="x", expand=True, padx=10)
            tk.Label(text_f, text=step_title,
                     font=(FONT_FAMILY, 10, "bold"),
                     fg=PALETTE["text"], bg=PALETTE["card"],
                     anchor="w").pack(anchor="w")
            tk.Label(text_f, text=step_body,
                     font=(FONT_FAMILY, 9),
                     fg=PALETTE["text2"], bg=PALETTE["card"],
                     justify="left", anchor="w",
                     wraplength=420).pack(anchor="w", pady=(2,0))

        # 팁
        if data.get("tips"):
            tk.Frame(pad, bg=PALETTE["border"], height=1).pack(fill="x", pady=12)
            tip_card = tk.Frame(pad, bg="#FFFBEB",
                                highlightbackground="#FDE68A",
                                highlightthickness=1)
            tip_card.pack(fill="x", pady=4)
            tip_inner = tk.Frame(tip_card, bg="#FFFBEB")
            tip_inner.pack(fill="x", padx=14, pady=10)
            tk.Label(tip_inner, text="✨  알아두면 좋아요!",
                     font=(FONT_FAMILY, 9, "bold"),
                     fg="#92400E", bg="#FFFBEB").pack(anchor="w", pady=(0,4))
            for tip in data["tips"]:
                tk.Label(tip_inner, text=tip,
                         font=(FONT_FAMILY, 9),
                         fg="#78350F", bg="#FFFBEB",
                         justify="left", anchor="w",
                         wraplength=460).pack(anchor="w", pady=1)

        # 여백
        tk.Frame(pad, bg=PALETTE["bg"], height=12).pack()

        # ── 닫기 버튼 ──
        btn_row = tk.Frame(win, bg=PALETTE["bg"])
        btn_row.pack(fill="x", padx=20, pady=(0,14))
        self._button(btn_row, "✕  닫기", win.destroy,
                     color="#64748B").pack(side="right")

    # ──────────────────────────────────────────────────────────────
    #  상태바
    # ──────────────────────────────────────────────────────────────
    def _build_statusbar(self):
        bar = tk.Frame(self, bg=PALETTE["border"], height=28)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)
        self._status_var = tk.StringVar(value="준비")
        tk.Label(bar, textvariable=self._status_var,
                 font=(FONT_FAMILY, 9), fg=PALETTE["text2"],
                 bg=PALETTE["border"]).pack(side="left", padx=12)
        self._log_count_var = tk.StringVar(value="로그 0건")
        tk.Label(bar, textvariable=self._log_count_var,
                 font=(FONT_FAMILY,9), fg=PALETTE["text2"],
                 bg=PALETTE["border"]).pack(side="right", padx=12)

    def _set_status(self, msg):
        self.after(0, self._status_var.set, msg)

    # ══════════════════════════════════════════════════════════════
    #  탭 2: 계정 관리
    # ══════════════════════════════════════════════════════════════
    def _build_accounts_tab(self, parent):
        top = tk.Frame(parent, bg=PALETTE["bg"])
        top.pack(fill="x", padx=24, pady=(20,0))
        self._label(top, "계정 관리", 16, "bold").pack(side="left")
        self._button(top, "❓ 도움말", lambda: self._show_help("accounts"),
                     color="#8B5CF6", size=8).pack(side="right")

        toolbar = tk.Frame(parent, bg=PALETTE["bg"])
        toolbar.pack(fill="x", padx=24, pady=10)
        self._button(toolbar, "+ 계정 추가", self._add_account,
                     color=PALETTE["primary"]).pack(side="left", padx=(0,6))
        self._button(toolbar, "✎ 수정", self._edit_account,
                     color=PALETTE["warning"], text_color="#fff").pack(side="left", padx=3)
        self._button(toolbar, "✕ 삭제", self._del_account,
                     color=PALETTE["danger"]).pack(side="left", padx=3)
        self._button(toolbar, "⊙ 활성화 토글", self._toggle_account,
                     color="#64748B").pack(side="left", padx=3)
        self._button(toolbar, "📥 CSV 가져오기", self._import_accounts_csv,
                     color="#64748B").pack(side="right", padx=3)
        self._button(toolbar, "📤 CSV 내보내기", self._export_accounts_csv,
                     color="#64748B").pack(side="right", padx=3)

        card = tk.Frame(parent, bg=PALETTE["card"],
                        highlightbackground=PALETTE["border"],
                        highlightthickness=1)
        card.pack(fill="both", expand=True, padx=24, pady=(0,16))

        cols = ("사이트","아이디","카테고리","회사명","게시판 URL","상태")
        self._acc_tree = ttk.Treeview(card, columns=cols, show="headings",
                                       selectmode="browse")
        widths = [90, 120, 90, 120, 240, 60]
        for col, w in zip(cols, widths):
            self._acc_tree.heading(col, text=col)
            self._acc_tree.column(col, width=w, minwidth=50)

        # 색상 태그
        for site, color in SITE_COLORS.items():
            self._acc_tree.tag_configure(f"site_{site}", foreground=color)
        self._acc_tree.tag_configure("disabled", foreground=PALETTE["muted"])

        vsb = ttk.Scrollbar(card, orient="vertical", command=self._acc_tree.yview)
        hsb = ttk.Scrollbar(card, orient="horizontal", command=self._acc_tree.xview)
        self._acc_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        self._acc_tree.pack(fill="both", expand=True)
        self._acc_tree.bind("<Double-1>", lambda e: self._edit_account())

    def _resolve_display_url(self, acc: dict, site: str) -> str:
        """계정 목록 '게시판 URL' 컬럼에 표시할 URL을 계산.
        우선순위: account.write_url > category 자동 생성 > sites.json write_url
        """
        # ① 계정에 직접 write_url 있으면 우선 사용
        wu = acc.get("write_url", "").strip()
        if wu:
            return wu
        # ② category 값으로 URL 자동 생성
        cat = acc.get("category", "").strip()
        if cat:
            if site == "마멘토":
                # 한글명 또는 bo_table 직접 입력 모두 수용
                bo = MAMENTOR_BOARDS_R.get(cat, cat)
                return f"https://www.mamentor.co.kr/bbs/write.php?bo_table={bo}"
            elif site == "셀프모아":
                bo = SELFMOA_BOARDS_R.get(cat, cat)
                return f"http://m.selfmoa.com/bbs/write.php?bo_table={bo}"
        # ③ sites.json 기본 write_url (fallback)
        return self.sites.get(site, {}).get("write_url", "")

    def _refresh_accounts(self):
        self._acc_tree.delete(*self._acc_tree.get_children())
        for acc in self.accounts:
            site = acc.get("site","")
            tag = f"site_{site}" if acc.get("enabled",True) else "disabled"
            self._acc_tree.insert("", "end",
                values=(
                    site,
                    acc.get("id",""),
                    acc.get("category",""),
                    acc.get("company",""),
                    self._resolve_display_url(acc, site),
                    "✓ 활성" if acc.get("enabled",True) else "✗ 비활성"
                ), tags=(tag,))

    def _get_selected_acc_idx(self):
        sel = self._acc_tree.selection()
        if not sel: return None
        return self._acc_tree.index(sel[0])

    def _add_account(self):
        dlg = AccountDialog(self, "계정 추가", {}, list(self.sites.keys()))
        if dlg.result:
            self.accounts.append(dlg.result)
            save_json(CFG_ACCOUNTS, self.accounts)
            self._refresh_accounts()

    def _edit_account(self):
        idx = self._get_selected_acc_idx()
        if idx is None:
            messagebox.showinfo("알림","계정을 선택하세요."); return
        dlg = AccountDialog(self, "계정 수정", self.accounts[idx], list(self.sites.keys()))
        if dlg.result:
            self.accounts[idx] = dlg.result
            save_json(CFG_ACCOUNTS, self.accounts)
            self._refresh_accounts()

    def _del_account(self):
        idx = self._get_selected_acc_idx()
        if idx is None: return
        if messagebox.askyesno("삭제", f"'{self.accounts[idx].get('id','')}' 계정을 삭제하시겠습니까?"):
            self.accounts.pop(idx)
            save_json(CFG_ACCOUNTS, self.accounts)
            self._refresh_accounts()

    def _toggle_account(self):
        idx = self._get_selected_acc_idx()
        if idx is None: return
        self.accounts[idx]["enabled"] = not self.accounts[idx].get("enabled",True)
        save_json(CFG_ACCOUNTS, self.accounts)
        self._refresh_accounts()

    def _import_accounts_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV","*.csv")])
        if not path: return
        try:
            with open(path, encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    acc = {k.strip(): v.strip() for k,v in row.items()}
                    acc["enabled"] = True
                    self.accounts.append(acc)
            save_json(CFG_ACCOUNTS, self.accounts)
            self._refresh_accounts()
            messagebox.showinfo("완료","CSV 가져오기 완료")
        except Exception as e:
            messagebox.showerror("오류", str(e))

    def _export_accounts_csv(self):
        if not self.accounts: return
        path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV","*.csv")])
        if not path: return
        keys = list(self.accounts[0].keys())
        with open(path,"w",newline="",encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader(); w.writerows(self.accounts)
        messagebox.showinfo("완료","CSV 내보내기 완료")

    # ══════════════════════════════════════════════════════════════
    #  탭 3: 콘텐츠
    # ══════════════════════════════════════════════════════════════
    def _build_contents_tab(self, parent):
        top = tk.Frame(parent, bg=PALETTE["bg"])
        top.pack(fill="x", padx=24, pady=(20,0))
        self._label(top, "콘텐츠 템플릿", 16, "bold").pack(side="left")
        self._button(top, "❓ 도움말", lambda: self._show_help("contents"),
                     color="#8B5CF6", size=8).pack(side="right")

        paned = tk.PanedWindow(parent, orient="horizontal",
                                bg=PALETTE["bg"], sashwidth=6,
                                sashrelief="flat")
        paned.pack(fill="both", expand=True, padx=24, pady=10)

        # 왼쪽: 목록
        left = tk.Frame(paned, bg=PALETTE["card"],
                        highlightbackground=PALETTE["border"],
                        highlightthickness=1)
        paned.add(left, minsize=220)

        lh2 = tk.Frame(left, bg=PALETTE["card"])
        lh2.pack(fill="x", padx=12, pady=10)
        self._label(lh2, "템플릿 목록", 10, "bold").pack(side="left")
        self._button(lh2, "+", self._add_content,
                     color=PALETTE["primary"], size=9).pack(side="right")

        self._separator(left).pack(fill="x")

        self._cont_listbox = tk.Listbox(left, font=(FONT_FAMILY,9),
                                         selectbackground=PALETTE["primary"],
                                         selectforeground="#fff",
                                         bg=PALETTE["card"],
                                         relief="flat", bd=0,
                                         highlightthickness=0,
                                         activestyle="none")
        self._cont_listbox.pack(fill="both", expand=True, padx=8, pady=8)
        self._cont_listbox.bind("<<ListboxSelect>>", self._on_cont_select)

        # 오른쪽: 편집
        right = tk.Frame(paned, bg=PALETTE["card"],
                         highlightbackground=PALETTE["border"],
                         highlightthickness=1)
        paned.add(right, minsize=400)

        rh2 = tk.Frame(right, bg=PALETTE["card"])
        rh2.pack(fill="x", padx=16, pady=10)
        self._label(rh2, "템플릿 편집", 10, "bold").pack(side="left")

        btn_row = tk.Frame(rh2, bg=PALETTE["card"])
        btn_row.pack(side="right")
        self._button(btn_row, "저장", self._save_content,
                     color=PALETTE["success"]).pack(side="left", padx=2)
        self._button(btn_row, "삭제", self._del_content,
                     color=PALETTE["danger"]).pack(side="left", padx=2)
        self._button(btn_row, "복사", self._copy_content,
                     color="#64748B").pack(side="left", padx=2)

        self._separator(right).pack(fill="x")

        edit_inner = tk.Frame(right, bg=PALETTE["card"])
        edit_inner.pack(fill="both", expand=True, padx=16, pady=12)

        # 제목
        self._label(edit_inner, "제목", 9, color=PALETTE["text2"]).pack(anchor="w")
        self._cont_title = tk.Entry(edit_inner, font=(FONT_FAMILY,10),
                                     bg=PALETTE["bg"],
                                     relief="flat", bd=0,
                                     highlightbackground=PALETTE["border"],
                                     highlightthickness=1)
        self._cont_title.pack(fill="x", pady=(2,8), ipady=5, padx=1)

        # 카테고리 태그
        tag_row = tk.Frame(edit_inner, bg=PALETTE["card"])
        tag_row.pack(fill="x", pady=(0,8))
        self._label(tag_row, "태그/카테고리", 9, color=PALETTE["text2"]).pack(side="left")
        self._cont_tags = tk.Entry(tag_row, font=(FONT_FAMILY,9),
                                    bg=PALETTE["bg"], relief="flat", bd=0,
                                    highlightbackground=PALETTE["border"],
                                    highlightthickness=1, width=20)
        self._cont_tags.pack(side="left", padx=8, ipady=3)

        # 본문
        self._label(edit_inner, "본문 (HTML 형식 지원)",
                    9, color=PALETTE["text2"]).pack(anchor="w")
        body_frame = tk.Frame(edit_inner, bg=PALETTE["bg"],
                               highlightbackground=PALETTE["border"],
                               highlightthickness=1)
        body_frame.pack(fill="both", expand=True, pady=(2,0), padx=1)
        self._cont_body = tk.Text(body_frame, font=(FONT_FAMILY,9),
                                   bg=PALETTE["bg"], relief="flat",
                                   wrap="word", undo=True)
        body_sb = ttk.Scrollbar(body_frame, command=self._cont_body.yview)
        self._cont_body.configure(yscrollcommand=body_sb.set)
        body_sb.pack(side="right", fill="y")
        self._cont_body.pack(fill="both", expand=True, padx=4, pady=4)

        # 빠른 삽입 버튼
        quick = tk.Frame(edit_inner, bg=PALETTE["card"])
        quick.pack(fill="x", pady=(4,2))
        self._label(quick, "빠른삽입: ", 8, color=PALETTE["text2"]).pack(side="left")
        # HTML 태그
        for _txt, _snip in [("<br>","<br/>"),("<b>","<b></b>"),("<i>","<i></i>"),
                             ("<a>","<a href=''>링크</a>"),("<p>","<p></p>")]:
            tk.Button(quick, text=_txt,
                      font=(FONT_FAMILY, 7),
                      bg="#F1F5F9", fg=PALETTE["text2"], relief="flat",
                      cursor="hand2", padx=5, pady=2,
                      command=lambda s=_snip: self._insert_snippet(s)
                      ).pack(side="left", padx=1)

        self._current_cont_idx = None

    def _refresh_contents(self):
        self._cont_listbox.delete(0,"end")
        for c in self.contents:
            self._cont_listbox.insert("end",
                c.get("title","(제목없음)"))

    def _on_cont_select(self, event):
        sel = self._cont_listbox.curselection()
        if not sel: return
        idx = sel[0]
        self._current_cont_idx = idx
        c = self.contents[idx]
        self._cont_title.delete(0,"end")
        self._cont_title.insert(0, c.get("title",""))
        self._cont_tags.delete(0,"end")
        self._cont_tags.insert(0, c.get("tags",""))
        self._cont_body.delete("1.0","end")
        self._cont_body.insert("end", c.get("body",""))


    def _add_content(self):
        new = {"title": f"새 템플릿 {len(self.contents)+1}",
               "tags": "", "body": ""}
        self.contents.append(new)
        save_json(CFG_CONTENTS, self.contents)
        self._refresh_contents()
        self._cont_listbox.selection_set(len(self.contents)-1)
        self._on_cont_select(None)

    def _save_content(self):
        if self._current_cont_idx is None: return
        idx = self._current_cont_idx
        self.contents[idx] = {
            "title": self._cont_title.get(),
            "tags":  self._cont_tags.get(),
            "body":  self._cont_body.get("1.0","end").strip(),
        }
        save_json(CFG_CONTENTS, self.contents)
        self._refresh_contents()
        self._cont_listbox.selection_set(idx)
        messagebox.showinfo("저장","저장되었습니다.")

    def _del_content(self):
        if self._current_cont_idx is None: return
        if messagebox.askyesno("삭제","삭제하시겠습니까?"):
            self.contents.pop(self._current_cont_idx)
            save_json(CFG_CONTENTS, self.contents)
            self._current_cont_idx = None
            self._refresh_contents()
            self._cont_title.delete(0,"end")
            self._cont_body.delete("1.0","end")


    def _copy_content(self):
        if self._current_cont_idx is None: return
        # 저장되지 않은 편집 내용도 복사에 반영
        c = copy.deepcopy(self.contents[self._current_cont_idx])
        c["title"] = c["title"] + " (복사)"
        self.contents.append(c)
        save_json(CFG_CONTENTS, self.contents)
        self._refresh_contents()

    def _insert_snippet(self, snippet):
        self._cont_body.insert("insert", snippet)

    # ══════════════════════════════════════════════════════════════
    #  탭 4: 작업 관리
    # ══════════════════════════════════════════════════════════════

    def _build_jobs_tab(self, parent):
        top = tk.Frame(parent, bg=PALETTE["bg"])
        top.pack(fill="x", padx=24, pady=(20,0))
        self._label(top, "작업 관리", 16, "bold").pack(side="left")
        self._label(top, "  계정 × 콘텐츠 조합을 자유롭게 설정하세요",
                    10, color=PALETTE["text2"]).pack(side="left")
        self._button(top, "❓ 도움말", lambda: self._show_help("jobs"),
                     color="#8B5CF6", size=8).pack(side="right")

        toolbar = tk.Frame(parent, bg=PALETTE["bg"])
        toolbar.pack(fill="x", padx=24, pady=10)
        self._button(toolbar, "+ 작업 추가", self._add_job,
                     color=PALETTE["primary"]).pack(side="left", padx=(0,6))
        self._button(toolbar, "✎ 수정", self._edit_job,
                     color=PALETTE["warning"], text_color="#fff").pack(side="left", padx=3)
        self._button(toolbar, "⧉ 복제", self._dup_job,
                     color="#64748B").pack(side="left", padx=3)
        self._button(toolbar, "✕ 삭제", self._del_job,
                     color=PALETTE["danger"]).pack(side="left", padx=3)
        self._button(toolbar, "⊙ 활성 토글", self._toggle_job,
                     color="#64748B").pack(side="left", padx=3)
        self._button(toolbar, "▶ 선택 즉시 실행", self._run_selected_jobs,
                     color=PALETTE["success"]).pack(side="right", padx=3)
        self._button(toolbar, "▶▶ 전체 실행", self._run_all_jobs,
                     color=PALETTE["primary"]).pack(side="right", padx=3)

        # ── 실행 진행 상태 바 ──────────────────────────────────────
        self._jobs_prog_frame = tk.Frame(parent, bg=PALETTE["bg"],
                                         highlightbackground=PALETTE["border"],
                                         highlightthickness=1)
        pf = self._jobs_prog_frame
        self._jobs_progress = ttk.Progressbar(pf, mode="determinate")
        self._jobs_progress.pack(fill="x", side="left", expand=True,
                                 padx=(10,6), pady=5)
        self._jobs_prog_lbl = tk.Label(pf,
            text="준비 중", font=(FONT_FAMILY, 8),
            fg=PALETTE["text2"], bg=PALETTE["bg"])
        self._jobs_prog_lbl.pack(side="left", padx=(0,6))
        self._jobs_stop_btn = self._button(pf, "⏹ 중지",
            self._stop_jobs, color=PALETTE["danger"], size=8)
        self._jobs_stop_btn.pack(side="left", padx=(0,8), pady=4)
        self._jobs_stop_btn.config(state="disabled")
        self._jobs_prog_frame.pack(fill="x", padx=24, pady=(0,4))

        # 안내 카드
        guide = tk.Frame(parent, bg="#EFF6FF",
                         highlightbackground="#BFDBFE",
                         highlightthickness=1)
        guide.pack(fill="x", padx=24, pady=(0,8))
        gi = tk.Frame(guide, bg="#EFF6FF")
        gi.pack(fill="x", padx=16, pady=8)
        self._label(gi, "💡 작업이란?", 9, "bold", color="#1D4ED8").pack(anchor="w")
        self._label(gi,
            "각 작업 = 계정 1개 + 콘텐츠 1개의 조합입니다.  "
            "A계정→B콘텐츠, B계정→A콘텐츠 등 자유 조합 가능.",
            8, color="#1E40AF").pack(anchor="w")

        # ── 상하 PanedWindow ──────────────────────────────────────
        vpane = tk.PanedWindow(parent, orient="vertical",
                               bg=PALETTE["bg"], sashwidth=6,
                               sashrelief="flat")
        vpane.pack(fill="both", expand=True, padx=24, pady=(0,8))

        # ── 상단: 작업 목록 Treeview ──────────────────────────────
        card = tk.Frame(vpane, bg=PALETTE["card"],
                        highlightbackground=PALETTE["border"],
                        highlightthickness=1)
        vpane.add(card, minsize=200)

        cols = ("#","작업명","계정","커뮤니티","게시판","콘텐츠","딜레이","스케줄","상태")
        self._jobs_tree = ttk.Treeview(card, columns=cols, show="headings",
                                        selectmode="extended")
        widths = [30, 110, 110, 80, 100, 130, 55, 90, 72, 60]
        for col, w in zip(cols, widths):
            self._jobs_tree.heading(col, text=col)
            self._jobs_tree.column(col, width=w, minwidth=30)

        for site, color in SITE_COLORS.items():
            self._jobs_tree.tag_configure(f"site_{site}", foreground=color)
        self._jobs_tree.tag_configure("disabled", foreground=PALETTE["muted"])

        vsb = ttk.Scrollbar(card, orient="vertical", command=self._jobs_tree.yview)
        hsb = ttk.Scrollbar(card, orient="horizontal", command=self._jobs_tree.xview)
        self._jobs_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        self._jobs_tree.pack(fill="both", expand=True)
        self._jobs_tree.bind("<Double-1>", lambda e: self._edit_job())

        # ── 하단: 스케줄 + 딜레이 설정 패널 ─────────────────────
        bottom = tk.Frame(vpane, bg=PALETTE["bg"])
        vpane.add(bottom, minsize=180)

        bottom.columnconfigure(0, weight=1)
        bottom.columnconfigure(1, weight=1)
        bottom.rowconfigure(0, weight=1)

        # ── 왼쪽 카드: 실행 딜레이 & 순서 ────────────────────────
        delay_card = tk.Frame(bottom, bg=PALETTE["card"],
                              highlightbackground=PALETTE["border"],
                              highlightthickness=1)
        delay_card.grid(row=0, column=0, sticky="nsew", padx=(0,6), pady=4)
        dh = tk.Frame(delay_card, bg=PALETTE["primary"])
        dh.pack(fill="x")
        tk.Label(dh, text="⚙  실행 딜레이 & 순서",
                 font=(FONT_FAMILY, 9, "bold"),
                 fg="#fff", bg=PALETTE["primary"],
                 padx=12, pady=6).pack(side="left")
        di = tk.Frame(delay_card, bg=PALETTE["card"])
        di.pack(fill="both", expand=True, padx=14, pady=10)

        # 처리 순서
        ord_row = tk.Frame(di, bg=PALETTE["card"]); ord_row.pack(fill="x", pady=4)
        tk.Label(ord_row, text="처리 순서",
                 font=(FONT_FAMILY,9), fg=PALETTE["text2"],
                 bg=PALETTE["card"], width=12, anchor="e").pack(side="left")
        tk.Frame(ord_row, bg=PALETTE["card"], width=8).pack(side="left")
        self._opt_order_var = tk.StringVar(value=self.options.get("order","sequential"))
        for val, lab in [("sequential","순서대로"),("random","랜덤")]:
            tk.Radiobutton(ord_row, text=lab,
                           variable=self._opt_order_var, value=val,
                           font=(FONT_FAMILY,9),
                           bg=PALETTE["card"], fg=PALETTE["text"],
                           activebackground=PALETTE["card"],
                           selectcolor=PALETTE["card"]).pack(side="left", padx=5)

        # 전역 딜레이
        gl_row = tk.Frame(di, bg=PALETTE["card"]); gl_row.pack(fill="x", pady=4)
        tk.Label(gl_row, text="전역 딜레이",
                 font=(FONT_FAMILY,9), fg=PALETTE["text2"],
                 bg=PALETTE["card"], width=12, anchor="e").pack(side="left")
        tk.Frame(gl_row, bg=PALETTE["card"], width=8).pack(side="left")
        self._opt_delay_min_var = tk.IntVar(value=self.options.get("delay_min",3))
        self._opt_delay_max_var = tk.IntVar(value=self.options.get("delay_max",8))
        tk.Spinbox(gl_row, from_=0, to=300,
                   textvariable=self._opt_delay_min_var,
                   font=(FONT_FAMILY,9), width=5,
                   bg=PALETTE["bg"]).pack(side="left")
        tk.Label(gl_row, text=" ~ ", font=(FONT_FAMILY,9),
                 bg=PALETTE["card"]).pack(side="left")
        tk.Spinbox(gl_row, from_=0, to=300,
                   textvariable=self._opt_delay_max_var,
                   font=(FONT_FAMILY,9), width=5,
                   bg=PALETTE["bg"]).pack(side="left")
        tk.Label(gl_row, text=" 초  (작업별 딜레이 없을 때 적용)",
                 font=(FONT_FAMILY,8), fg=PALETTE["text2"],
                 bg=PALETTE["card"]).pack(side="left", padx=4)

        # 딜레이 저장 버튼
        ds_row = tk.Frame(di, bg=PALETTE["card"]); ds_row.pack(fill="x", pady=(6,0))
        self._button(ds_row, "💾 딜레이 저장", self._save_delay_opts,
                     color=PALETTE["success"], size=8).pack(side="left")

        # ── 오른쪽 카드: 자동 스케줄 ──────────────────────────────
        sched_card = tk.Frame(bottom, bg=PALETTE["card"],
                              highlightbackground=PALETTE["border"],
                              highlightthickness=1)
        sched_card.grid(row=0, column=1, sticky="nsew", padx=(6,0), pady=4)
        sh = tk.Frame(sched_card, bg="#0EA5E9")
        sh.pack(fill="x")
        tk.Label(sh, text="🕐  자동 스케줄",
                 font=(FONT_FAMILY, 9, "bold"),
                 fg="#fff", bg="#0EA5E9",
                 padx=12, pady=6).pack(side="left")
        si = tk.Frame(sched_card, bg=PALETTE["card"])
        si.pack(fill="both", expand=True, padx=14, pady=8)

        # 활성화
        r0 = tk.Frame(si, bg=PALETTE["card"]); r0.pack(fill="x", pady=2)
        self._sched_enabled_var = tk.BooleanVar(value=self.schedule.get("enabled",False))
        tk.Checkbutton(r0, text="자동 스케줄 활성화",
                       variable=self._sched_enabled_var,
                       font=(FONT_FAMILY,9,"bold"),
                       fg=PALETTE["text"], bg=PALETTE["card"],
                       activebackground=PALETTE["card"],
                       selectcolor=PALETTE["card"],
                       command=self._toggle_schedule).pack(side="left")
        self._sched_status_lbl = tk.Label(r0,
            text="활성화됨" if self.schedule.get("enabled") else "꺼짐",
            font=(FONT_FAMILY,8),
            fg=PALETTE["success"] if self.schedule.get("enabled") else PALETTE["muted"],
            bg=PALETTE["card"])
        self._sched_status_lbl.pack(side="left", padx=8)

        # 모드
        r1 = tk.Frame(si, bg=PALETTE["card"]); r1.pack(fill="x", pady=2)
        tk.Label(r1, text="실행 모드",
                 font=(FONT_FAMILY,9), fg=PALETTE["text2"],
                 bg=PALETTE["card"], width=9, anchor="e").pack(side="left")
        tk.Frame(r1, bg=PALETTE["card"], width=6).pack(side="left")
        self._sched_mode_var = tk.StringVar(value=self.schedule.get("mode","interval"))
        for val, lab in [("interval","반복 간격"),("times","지정 시각")]:
            tk.Radiobutton(r1, text=lab,
                           variable=self._sched_mode_var, value=val,
                           font=(FONT_FAMILY,9),
                           bg=PALETTE["card"], fg=PALETTE["text"],
                           activebackground=PALETTE["card"],
                           selectcolor=PALETTE["card"],
                           command=self._update_sched_ui).pack(side="left", padx=5)

        # 반복 간격 프레임
        self._sched_interval_frame = tk.Frame(si, bg=PALETTE["card"])
        self._sched_interval_frame.pack(fill="x", pady=2)
        tk.Label(self._sched_interval_frame, text="간격",
                 font=(FONT_FAMILY,9), fg=PALETTE["text2"],
                 bg=PALETTE["card"], width=9, anchor="e").grid(row=0,column=0,sticky="w")
        self._sched_interval_var = tk.IntVar(value=self.schedule.get("interval_hours",3))
        tk.Spinbox(self._sched_interval_frame, from_=1, to=72,
                   textvariable=self._sched_interval_var,
                   font=(FONT_FAMILY,9), width=5,
                   bg=PALETTE["bg"]).grid(row=0,column=1,padx=4)
        tk.Label(self._sched_interval_frame, text="시간  ±",
                 font=(FONT_FAMILY,9), bg=PALETTE["card"]).grid(row=0,column=2)
        self._sched_variance_var = tk.IntVar(value=self.schedule.get("interval_variance",30))
        tk.Spinbox(self._sched_interval_frame, from_=0, to=120,
                   textvariable=self._sched_variance_var,
                   font=(FONT_FAMILY,9), width=4,
                   bg=PALETTE["bg"]).grid(row=0,column=3,padx=4)
        tk.Label(self._sched_interval_frame, text="분",
                 font=(FONT_FAMILY,9), bg=PALETTE["card"]).grid(row=0,column=4)

        # 지정 시각 프레임
        self._sched_times_frame = tk.Frame(si, bg=PALETTE["card"])
        self._sched_times_frame.pack(fill="x", pady=2)
        tk.Label(self._sched_times_frame, text="시각 (HH:MM, 쉼표 구분)",
                 font=(FONT_FAMILY,8), fg=PALETTE["text2"],
                 bg=PALETTE["card"]).pack(anchor="w")
        times_str = ",".join(self.schedule.get("times",["09:00","14:00","19:00"]))
        self._sched_times_entry = tk.Entry(self._sched_times_frame,
                                            font=(FONT_FAMILY,9),
                                            bg=PALETTE["bg"], relief="flat",
                                            highlightbackground=PALETTE["border"],
                                            highlightthickness=1)
        self._sched_times_entry.insert(0, times_str)
        self._sched_times_entry.pack(fill="x", ipady=4)

        # 요일
        r3 = tk.Frame(si, bg=PALETTE["card"]); r3.pack(fill="x", pady=2)
        tk.Label(r3, text="실행 요일",
                 font=(FONT_FAMILY,9), fg=PALETTE["text2"],
                 bg=PALETTE["card"], width=9, anchor="e").pack(side="left")
        days = self.schedule.get("days",[0,1,2,3,4])
        self._sched_day_vars = []
        for i, dl in enumerate(["월","화","수","목","금","토","일"]):
            var = tk.BooleanVar(value=i in days)
            self._sched_day_vars.append(var)
            tk.Checkbutton(r3, text=dl, variable=var,
                           font=(FONT_FAMILY,8),
                           bg=PALETTE["card"], fg=PALETTE["text"],
                           activebackground=PALETTE["card"],
                           selectcolor=PALETTE["card"]).pack(side="left", padx=2)

        # 스케줄 저장
        ss_row = tk.Frame(si, bg=PALETTE["card"]); ss_row.pack(fill="x", pady=(4,0))
        self._button(ss_row, "💾 스케줄 저장", self._save_schedule,
                     color="#0EA5E9", size=8).pack(side="left")

        self._update_sched_ui()

    def _refresh_jobs(self):
        self._jobs_tree.delete(*self._jobs_tree.get_children())
        for i, job in enumerate(self.jobs):
            acc  = self._resolve_job_account(job)
            cont = self._resolve_job_content(job)
            community = job.get("community", "") or (acc.get("site","") if acc else "")
            acc_id     = acc.get("id","") if acc else "(없음)"
            cont_title = cont.get("title","") if cont else "(없음)"
            enabled    = job.get("enabled", True)
            # 게시판 표시: 한글명 우선, 없으면 bo_table
            board_raw  = job.get("board", "")
            board_disp = MAMENTOR_BOARDS.get(board_raw, board_raw) if board_raw else ""
            tag = f"site_{community}" if enabled and community in SITE_COLORS else ("disabled" if not enabled else "")
            # 딜레이 표시 (전역=기본, 개별 설정 시 표시)
            d_min = job.get("delay_min", None)
            d_max = job.get("delay_max", None)
            if d_min is not None and d_max is not None:
                delay_disp = f"{d_min}~{d_max}초"
            else:
                delay_disp = "전역 설정"
            # 스케줄 표시 (🟢=실행중, 🟡=설정됨/중지, ⚫=OFF, ⚪=전역)
            jsched = job.get("schedule", {})
            jname  = job.get("name", "")
            if not jsched or jsched.get("use_global", True):
                sched_disp = "⚪ 전역"
            elif not jsched.get("enabled", False):
                sched_disp = "⚫ OFF"
            else:
                running = jname in self._job_sched_threads
                icon    = "🟢" if running else "🟡"
                jmode   = jsched.get("mode", "interval")
                days    = jsched.get("days", list(range(7)))
                day_chars = ["월","화","수","목","금","토","일"]
                day_str   = "".join(day_chars[d] for d in sorted(days) if 0<=d<7)
                day_suffix = f"/{day_str}" if day_str and day_str != "월화수목금토일" else ""
                if jmode == "interval":
                    jh = jsched.get("interval_hours", 3)
                    jv = jsched.get("interval_variance", 0)
                    vs = f"±{jv}m" if jv > 0 else ""
                    sched_disp = f"{icon} {jh}h{vs}{day_suffix}"
                else:
                    times = jsched.get("times", [])
                    t_str = ",".join(times) if times else "시각미설정"
                    sched_disp = f"{icon} {t_str}{day_suffix}"

            self._jobs_tree.insert("", "end",
                values=(i+1,
                        job.get("name", f"작업{i+1}"),
                        acc_id, community, board_disp, cont_title,
                        delay_disp, sched_disp,
                        "✓ 활성" if enabled else "✗ 비활성"),
                tags=(tag,))

    def _save_delay_opts(self):
        """작업관리 탭에서 딜레이/순서 저장"""
        self.options["order"]     = self._opt_order_var.get()
        self.options["delay_min"] = self._opt_delay_min_var.get()
        self.options["delay_max"] = self._opt_delay_max_var.get()
        save_json(CFG_OPTIONS, self.options)
        messagebox.showinfo("저장", "딜레이 설정이 저장되었습니다.")

    def _resolve_job_account(self, job):
        idx = job.get("account_idx", -1)
        if 0 <= idx < len(self.accounts):
            return self.accounts[idx]
        # fallback: match by id
        aid = job.get("account_id", "")
        for a in self.accounts:
            if a.get("id") == aid:
                return a
        return None

    def _resolve_job_content(self, job):
        idx = job.get("content_idx", -1)
        if 0 <= idx < len(self.contents):
            return self.contents[idx]
        return None

    def _get_selected_job_idxs(self):
        sel = self._jobs_tree.selection()
        return [self._jobs_tree.index(s) for s in sel]

    # ── 개별 작업 스케줄러 (작업별 독립 스레드) ──────────────────────

    def _start_job_scheduler(self, job):
        """개별 작업 전용 스케줄 스레드 시작.
        이미 실행 중인 경우 먼저 중지 후 재시작."""
        jname = job.get("name", "")
        if not jname:
            return
        self._stop_job_scheduler(jname)   # 기존 스레드 정리

        jsched = job.get("schedule", {})
        if not jsched.get("enabled", False):
            return                        # 개별 스케줄 비활성이면 시작 안함

        stop_flag = threading.Event()
        self._job_sched_threads[jname] = stop_flag

        def _job_loop():
            last_run = 0.0          # 마지막 실행 시각 (timestamp)
            # interval 모드용 대기시간을 1회 계산 (루프마다 재계산 X)
            def _calc_wait():
                jh = jsched.get("interval_hours", 3)
                jv = jsched.get("interval_variance", 0)
                return jh * 3600 + random.randint(-jv * 60, jv * 60)

            next_wait = _calc_wait()

            while not stop_flag.is_set():
                now  = datetime.now()
                days = jsched.get("days", [0,1,2,3,4,5,6])
                mode = jsched.get("mode", "interval")
                fired = False

                if now.weekday() not in days:
                    stop_flag.wait(30)
                    continue

                if mode == "interval":
                    if (now.timestamp() - last_run) >= next_wait:
                        fired = True
                else:  # times 모드
                    for t in jsched.get("times", []):
                        try:
                            h2, m2 = map(int, t.split(":"))
                            target = now.replace(hour=h2, minute=m2,
                                                 second=0, microsecond=0)
                            if 0 <= (target - now).total_seconds() < 60:
                                # 1분 내 중복 방지
                                if (now.timestamp() - last_run) >= 50:
                                    fired = True
                        except Exception:
                            pass

                if fired:
                    last_run  = now.timestamp()
                    next_wait = _calc_wait()   # 다음 대기시간 새로 계산
                    self._log_append(
                        f"[SCHED:{jname}] 스케줄 트리거 → 큐에 투입", "INFO")
                    # 메인 스레드에서 _execute_jobs 호출 (큐에 투입)
                    self.after(0, lambda j=job: self._execute_jobs([j]))

                stop_flag.wait(30)   # 30초 대기 후 재확인

        t = threading.Thread(target=_job_loop, daemon=True, name=f"sched-{jname}")
        t.start()
        self._log_append(f"[SCHED:{jname}] 개별 스케줄러 시작", "INFO")

    def _stop_job_scheduler(self, job_name):
        """특정 작업의 스케줄 스레드 중지"""
        flag = self._job_sched_threads.pop(job_name, None)
        if flag:
            flag.set()   # stop_flag.wait() 에서 즉시 깨어나 루프 종료
            self._log_append(f"[SCHED:{job_name}] 개별 스케줄러 중지", "INFO")

    def _stop_all_job_schedulers(self):
        """모든 개별 작업 스케줄러 중지"""
        for name, flag in list(self._job_sched_threads.items()):
            flag.set()
        self._job_sched_threads.clear()

    def _restore_scheduler_on_startup(self):
        """프로그램 시작 시 저장된 스케줄 상태 자동 복원"""
        # 전역 스케줄 복원
        if self.schedule.get("enabled", False):
            self._start_scheduler()
            self._log_append("[SCHED] 전역 스케줄 자동 복원", "INFO")
        # 개별 스케줄 복원 (각 작업 독립 스레드)
        restored = []
        for job in self.jobs:
            jsched = job.get("schedule", {})
            if (job.get("enabled", True) and
                jsched.get("enabled", False) and
                not jsched.get("use_global", True)):
                self._start_job_scheduler(job)
                restored.append(job.get("name", ""))
        if restored:
            self._log_append(
                f"[SCHED] 개별 스케줄 복원: {', '.join(restored)}", "INFO")

    def _sync_scheduler(self):
        """작업 추가/수정/삭제 후 개별 스케줄 동기화"""
        active_names = set()
        for job in self.jobs:
            jsched = job.get("schedule", {})
            if (job.get("enabled", True) and
                jsched.get("enabled", False) and
                not jsched.get("use_global", True)):
                active_names.add(job.get("name", ""))
                if job.get("name", "") not in self._job_sched_threads:
                    self._start_job_scheduler(job)
        # 삭제된 작업 스케줄러 중지
        for name in list(self._job_sched_threads.keys()):
            if name not in active_names:
                self._stop_job_scheduler(name)

    def _add_job(self):
        dlg = JobDialog(self, "작업 추가", {}, self.accounts, self.contents, self.sites)
        if dlg.result:
            self.jobs.append(dlg.result)
            save_json(CFG_JOBS, self.jobs)
            self._refresh_jobs()
            # 개별 스케줄 활성화된 경우 해당 작업 스케줄러 즉시 시작
            self._start_job_scheduler(dlg.result)
            self._sync_scheduler()

    def _edit_job(self):
        idxs = self._get_selected_job_idxs()
        if not idxs:
            messagebox.showinfo("알림", "작업을 선택하세요."); return
        idx = idxs[0]
        dlg = JobDialog(self, "작업 수정", self.jobs[idx], self.accounts, self.contents, self.sites)
        if dlg.result:
            old_name = self.jobs[idx].get("name", "")
            self.jobs[idx] = dlg.result
            save_json(CFG_JOBS, self.jobs)
            self._refresh_jobs()
            # 이름 바뀐 경우 기존 스케줄러 중지
            new_name = dlg.result.get("name", "")
            if old_name != new_name:
                self._stop_job_scheduler(old_name)
            # 수정된 작업 스케줄러 재시작 (비활성이면 _start_job_scheduler 내부에서 무시)
            self._start_job_scheduler(dlg.result)
            self._sync_scheduler()

    def _dup_job(self):
        idxs = self._get_selected_job_idxs()
        if not idxs: return
        for idx in idxs:
            j = copy.deepcopy(self.jobs[idx])
            j["name"] = j.get("name", "") + " (복사)"
            self.jobs.append(j)
        save_json(CFG_JOBS, self.jobs)
        self._refresh_jobs()

    def _del_job(self):
        idxs = self._get_selected_job_idxs()
        if not idxs: return
        if messagebox.askyesno("삭제", f"{len(idxs)}개 작업을 삭제하시겠습니까?"):
            for idx in sorted(idxs, reverse=True):
                jname = self.jobs[idx].get("name", "")
                self._stop_job_scheduler(jname)   # 해당 작업 스케줄러 중지
                self.jobs.pop(idx)
            save_json(CFG_JOBS, self.jobs)
            self._refresh_jobs()

    def _toggle_job(self):
        idxs = self._get_selected_job_idxs()
        if not idxs: return
        for idx in idxs:
            self.jobs[idx]["enabled"] = not self.jobs[idx].get("enabled", True)
            job = self.jobs[idx]
            if job.get("enabled", True):
                self._start_job_scheduler(job)   # 활성화 → 스케줄러 재시작
            else:
                self._stop_job_scheduler(job.get("name", ""))  # 비활성화 → 중지
        save_json(CFG_JOBS, self.jobs)
        self._refresh_jobs()

    def _stop_jobs(self):
        """작업 관리 탭 중지 버튼 핸들러"""
        self.engine.stop()
        self.engine.start()
        self._jobs_stop_btn.config(state="disabled")
        self._jobs_prog_lbl.config(text="중지됨", fg=PALETTE["muted"])
        self._set_status("중지됨")

    def _run_all_jobs(self):
        active = [j for j in self.jobs if j.get("enabled", True)]
        if not active:
            messagebox.showinfo("알림", "활성화된 작업이 없습니다."); return
        self._execute_jobs(active)

    def _run_selected_jobs(self):
        idxs = self._get_selected_job_idxs()
        if not idxs:
            messagebox.showinfo("알림", "작업을 선택하세요."); return
        jobs = [self.jobs[i] for i in idxs]
        self._execute_jobs(jobs)

    def _execute_jobs(self, job_list):
        """작업 목록을 포스팅 엔진에 투입"""
        total = len(job_list)
        if total == 0: return
        done_count = [0]
        success_count = [0]
        fail_count = [0]

        # 진행 UI 초기화
        self._jobs_progress["maximum"] = total
        self._jobs_progress["value"]   = 0
        self._jobs_prog_lbl.config(text=f"0 / {total}  ✓ 0  ✗ 0",
                                   fg=PALETTE["text2"])
        self._jobs_stop_btn.config(state="normal")

        def on_done(status, entry):
            # DEBUG 는 카운터 증가 없이 로그만 기록
            if status == "DEBUG":
                self._log_append(entry, "DEBUG")
                return
            done_count[0] += 1
            if status == "SUCCESS":
                success_count[0] += 1
            else:
                fail_count[0] += 1
            self._log_append(entry, status)
            # 결과 내역 저장
            self._record_result(status, entry)
            # 진행 UI 업데이트
            self._jobs_progress["value"] = done_count[0]
            ok_c = success_count[0]; fail_c = fail_count[0]
            self._jobs_prog_lbl.config(
                text=f"{done_count[0]} / {total}  ✓ {ok_c}  ✗ {fail_c}",
                fg=PALETTE["success"] if fail_c == 0 else PALETTE["warning"])
            self._set_status(f"작업 진행 {done_count[0]}/{total}")
            if done_count[0] >= total:
                self._set_status(
                    f"작업 완료 ✓  성공 {success_count[0]} / 실패 {fail_count[0]}")
                self._jobs_stop_btn.config(state="disabled")
                self._jobs_prog_lbl.config(
                    text=f"완료  ✓ {success_count[0]}  ✗ {fail_count[0]}",
                    fg=PALETTE["success"] if fail_count[0]==0 else PALETTE["danger"])

        opts = self.options.copy()
        order = opts.get("order", "sequential")
        tasks = list(job_list)
        if order == "random":
            random.shuffle(tasks)

        for job in tasks:
            acc  = self._resolve_job_account(job)
            cont = self._resolve_job_content(job)
            if not acc or not cont:
                self._log_append(
                    f"[SKIP] '{job.get('name','')}' – 계정 또는 콘텐츠 없음", "WARN")
                done_count[0] += 1
                continue

            # 커뮤니티가 명시적으로 지정된 경우 그것을, 없으면 계정 기본 사이트 사용
            site_name = job.get("community") or acc.get("site", "")
            site_cfg  = self.sites.get(site_name, {})

            # ── 게시판(board) 오버라이드: 작업에 board 지정 시 계정 복사본에 반영
            acc_for_task = dict(acc)   # 원본 계정 보호
            _job_board = job.get("board", "").strip()
            if _job_board and site_name == "마멘토":
                _bo_key = MAMENTOR_BOARDS_R.get(_job_board, _job_board)
                acc_for_task["write_url"] = (
                    f"https://mamentor.co.kr/bbs/write.php?bo_table={_bo_key}"
                )
                acc_for_task["category"] = _bo_key
            elif _job_board and site_name == "셀프모아":
                # 셀프모아: 한글명 → bo_table 변환 후 write_url 자동 생성
                _bo_key = SELFMOA_BOARDS_R.get(_job_board, _job_board)
                acc_for_task["write_url"] = (
                    f"http://m.selfmoa.com/bbs/write.php?bo_table={_bo_key}"
                )
                acc_for_task["category"] = _bo_key

            # 작업별 딜레이가 지정된 경우 opts 오버라이드
            task_opts = opts.copy()
            if job.get("delay_min") is not None:
                task_opts["delay_min"] = job["delay_min"]
            if job.get("delay_max") is not None:
                task_opts["delay_max"] = job["delay_max"]
            # pre_delay: 작업 실행 전 앞 대기
            if job.get("pre_delay_min") is not None:
                task_opts["pre_delay_min"] = job["pre_delay_min"]
            if job.get("pre_delay_max") is not None:
                task_opts["pre_delay_max"] = job["pre_delay_max"]

            self.engine.add_task({
                "site":        site_name,
                "account":     acc_for_task,
                "content":     cont,
                "site_cfg":    site_cfg,
                "options":     task_opts,
                "callback":    on_done,
            })

        self._set_status(f"작업 {total}건 대기열 투입 완료")

    # ══════════════════════════════════════════════════════════════
    #  탭 5: 사이트 설정
    # ══════════════════════════════════════════════════════════════
    def _build_sites_tab(self, parent):
        top = tk.Frame(parent, bg=PALETTE["bg"])
        top.pack(fill="x", padx=24, pady=(20,0))
        self._label(top, "사이트 설정", 16, "bold").pack(side="left")
        self._label(top, "  URL·셀렉터·편집기 타입을 자유롭게 수정하세요",
                    10, color=PALETTE["text2"]).pack(side="left")
        self._button(top, "❓ 도움말", lambda: self._show_help("sites"),
                     color="#8B5CF6", size=8).pack(side="right")

        toolbar = tk.Frame(parent, bg=PALETTE["bg"])
        toolbar.pack(fill="x", padx=24, pady=8)
        self._button(toolbar, "+ 사이트 추가", self._add_site,
                     color=PALETTE["primary"]).pack(side="left", padx=(0,6))
        self._button(toolbar, "✕ 삭제", self._del_site,
                     color=PALETTE["danger"]).pack(side="left", padx=3)
        self._button(toolbar, "💾 저장", self._save_sites,
                     color=PALETTE["success"]).pack(side="right")
        self._button(toolbar, "↺ 기본값 복원", self._reset_sites,
                     color="#64748B").pack(side="right", padx=6)

        paned = tk.PanedWindow(parent, orient="horizontal",
                                bg=PALETTE["bg"], sashwidth=6)
        paned.pack(fill="both", expand=True, padx=24, pady=(0,16))

        # 사이트 목록
        left = tk.Frame(paned, bg=PALETTE["card"],
                        highlightbackground=PALETTE["border"],
                        highlightthickness=1)
        paned.add(left, minsize=180)
        self._site_listbox = tk.Listbox(left, font=(FONT_FAMILY,10),
                                         selectbackground=PALETTE["primary"],
                                         selectforeground="#fff",
                                         bg=PALETTE["card"],
                                         relief="flat", bd=0,
                                         highlightthickness=0,
                                         activestyle="none")
        self._site_listbox.pack(fill="both", expand=True, padx=8, pady=8)
        self._site_listbox.bind("<<ListboxSelect>>", self._on_site_select)

        # 설정 편집
        right = tk.Frame(paned, bg=PALETTE["card"],
                         highlightbackground=PALETTE["border"],
                         highlightthickness=1)
        paned.add(right, minsize=500)

        canvas = tk.Canvas(right, bg=PALETTE["card"], highlightthickness=0)
        vsb = ttk.Scrollbar(right, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)

        self._site_edit_inner = tk.Frame(canvas, bg=PALETTE["card"])
        canvas.create_window((0,0), window=self._site_edit_inner, anchor="nw")
        self._site_edit_inner.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self._site_fields = {}
        self._current_site = None

        fields_def = [
            ("main_url",      "메인 URL (항상 여기서 시작)",             "entry"),
            ("login_btn_sel", "로그인 버튼 셀렉터 (메인→로그인폼 이동용)", "entry"),
            ("write_url",   "글쓰기 URL",        "entry"),
            ("popup_sel",   "팝업 닫기 셀렉터",  "entry"),
            ("id_sel",      "아이디 필드 셀렉터","entry"),
            ("pw_sel",      "비밀번호 필드 셀렉터","entry"),
            ("btn_sel",     "로그인 버튼 셀렉터","entry"),
            ("title_sel",   "제목 필드 셀렉터",  "entry"),
            ("editor_type", "에디터 타입",        "combo"),
            ("editor_sel",  "에디터 셀렉터",     "entry"),
            ("cat_sel",     "카테고리 셀렉터",   "entry"),
            ("submit_sel",  "제출 버튼 셀렉터",  "entry"),
            ("success_pat", "성공 URL 패턴",     "entry"),
            ("link1_sel",   "부가필드1 셀렉터",  "entry"),
            ("link2_sel",   "부가필드2 셀렉터",  "entry"),
            ("enabled",     "활성화",            "check"),
        ]
        self._site_fields_def = fields_def

        for field_key, label, ftype in fields_def:
            row = tk.Frame(self._site_edit_inner, bg=PALETTE["card"])
            row.pack(fill="x", padx=16, pady=3)

            tk.Label(row, text=label, font=(FONT_FAMILY,9),
                     fg=PALETTE["text2"], bg=PALETTE["card"],
                     width=18, anchor="e").pack(side="left")
            tk.Frame(row, bg=PALETTE["card"], width=8).pack(side="left")

            if ftype == "entry":
                w = tk.Entry(row, font=(FONT_FAMILY,9),
                             bg=PALETTE["bg"], relief="flat",
                             highlightbackground=PALETTE["border"],
                             highlightthickness=1, width=50)
                w.pack(side="left", ipady=4, fill="x", expand=True, padx=(0,16))
                self._site_fields[field_key] = w
            elif ftype == "combo":
                var = tk.StringVar()
                w = ttk.Combobox(row, textvariable=var, width=20,
                                 values=["ckeditor4","smarteditor2","summernote","textarea"])
                w.pack(side="left")
                self._site_fields[field_key] = var
            elif ftype == "check":
                var = tk.BooleanVar()
                w = tk.Checkbutton(row, variable=var,
                                   bg=PALETTE["card"],
                                   activebackground=PALETTE["card"])
                w.pack(side="left")
                self._site_fields[field_key] = var

    def _refresh_sites(self):
        self._site_listbox.delete(0,"end")
        for name in self.sites:
            self._site_listbox.insert("end", name)

    def _on_site_select(self, event):
        sel = self._site_listbox.curselection()
        if not sel: return
        name = self._site_listbox.get(sel[0])
        self._current_site = name
        cfg = self.sites.get(name, {})
        for field_key, label, ftype in self._site_fields_def:
            val = cfg.get(field_key, "")
            w = self._site_fields[field_key]
            if ftype == "entry":
                w.delete(0,"end"); w.insert(0, str(val))
            elif ftype == "combo":
                w.set(str(val))
            elif ftype == "check":
                w.set(bool(val))

    def _save_sites(self):
        if self._current_site:
            data = {}
            for field_key, label, ftype in self._site_fields_def:
                w = self._site_fields[field_key]
                if ftype == "entry":
                    data[field_key] = w.get()
                elif ftype == "combo":
                    data[field_key] = w.get()
                elif ftype == "check":
                    data[field_key] = w.get()
            self.sites[self._current_site] = data
        save_json(CFG_SITES, self.sites)
        messagebox.showinfo("저장","사이트 설정이 저장되었습니다.")

    def _add_site(self):
        name = simpledialog.askstring("사이트 추가","새 사이트 이름:")
        if name and name not in self.sites:
            self.sites[name] = copy.deepcopy(list(DEFAULT_SITES.values())[0])
            self.sites[name]["color"] = "#64748B"
            save_json(CFG_SITES, self.sites)
            self._refresh_sites()

    def _del_site(self):
        sel = self._site_listbox.curselection()
        if not sel: return
        name = self._site_listbox.get(sel[0])
        if messagebox.askyesno("삭제",f"'{name}' 사이트를 삭제하시겠습니까?"):
            del self.sites[name]
            save_json(CFG_SITES, self.sites)
            self._refresh_sites()

    def _reset_sites(self):
        if messagebox.askyesno("복원","모든 사이트 설정을 기본값으로 복원하시겠습니까?"):
            self.sites = copy.deepcopy(DEFAULT_SITES)
            save_json(CFG_SITES, self.sites)
            self._refresh_sites()

    # ══════════════════════════════════════════════════════════════
    #  탭 6: 스케줄
    # ══════════════════════════════════════════════════════════════
    def _build_schedule_tab(self, parent):
        top = tk.Frame(parent, bg=PALETTE["bg"])
        top.pack(fill="x", padx=24, pady=(20,0))
        self._label(top, "자동 스케줄", 16, "bold").pack(side="left")
        self._button(top, "❓ 도움말", lambda: self._show_help("schedule"),
                     color="#8B5CF6", size=8).pack(side="right")

        card = tk.Frame(parent, bg=PALETTE["card"],
                        highlightbackground=PALETTE["border"],
                        highlightthickness=1)
        card.pack(fill="x", padx=24, pady=16)
        inner = tk.Frame(card, bg=PALETTE["card"])
        inner.pack(fill="x", padx=24, pady=20)

        # 활성화
        row0 = tk.Frame(inner, bg=PALETTE["card"])
        row0.pack(fill="x", pady=6)
        self._sched_enabled_var = tk.BooleanVar(value=self.schedule.get("enabled",False))
        tk.Checkbutton(row0, text="자동 스케줄 활성화",
                       variable=self._sched_enabled_var,
                       font=(FONT_FAMILY,11,"bold"),
                       fg=PALETTE["text"], bg=PALETTE["card"],
                       activebackground=PALETTE["card"],
                       selectcolor=PALETTE["card"],
                       command=self._toggle_schedule).pack(side="left")

        self._separator(inner).pack(fill="x", pady=10)

        # 모드
        row1 = tk.Frame(inner, bg=PALETTE["card"])
        row1.pack(fill="x", pady=6)
        self._label(row1, "실행 모드", 10, "bold").pack(side="left", padx=(0,16))
        self._sched_mode_var = tk.StringVar(value=self.schedule.get("mode","interval"))
        for val, lab in [("interval","반복 간격"),("times","지정 시각")]:
            tk.Radiobutton(row1, text=lab,
                           variable=self._sched_mode_var, value=val,
                           font=(FONT_FAMILY,10),
                           bg=PALETTE["card"], fg=PALETTE["text"],
                           activebackground=PALETTE["card"],
                           selectcolor=PALETTE["card"],
                           command=self._update_sched_ui).pack(side="left", padx=8)

        # 반복 간격 설정
        self._sched_interval_frame = tk.Frame(inner, bg=PALETTE["card"])
        self._sched_interval_frame.pack(fill="x", pady=8)
        self._label(self._sched_interval_frame, "반복 간격", 9, color=PALETTE["text2"]
                    ).grid(row=0, column=0, sticky="w", padx=(0,12))
        self._sched_interval_var = tk.IntVar(value=self.schedule.get("interval_hours",3))
        tk.Spinbox(self._sched_interval_frame, from_=1, to=72,
                   textvariable=self._sched_interval_var,
                   font=(FONT_FAMILY,10), width=6,
                   bg=PALETTE["bg"]).grid(row=0, column=1)
        self._label(self._sched_interval_frame, "시간", 9).grid(row=0, column=2, padx=4)
        self._label(self._sched_interval_frame, "± 랜덤", 9, color=PALETTE["text2"]
                    ).grid(row=0, column=3, padx=(12,4))
        self._sched_variance_var = tk.IntVar(value=self.schedule.get("interval_variance",30))
        tk.Spinbox(self._sched_interval_frame, from_=0, to=120,
                   textvariable=self._sched_variance_var,
                   font=(FONT_FAMILY,10), width=6,
                   bg=PALETTE["bg"]).grid(row=0, column=4)
        self._label(self._sched_interval_frame, "분", 9).grid(row=0, column=5, padx=4)

        # 지정 시각
        self._sched_times_frame = tk.Frame(inner, bg=PALETTE["card"])
        self._sched_times_frame.pack(fill="x", pady=8)
        self._label(self._sched_times_frame, "실행 시각 (쉼표 구분, HH:MM)",
                    9, color=PALETTE["text2"]).pack(anchor="w")
        times_str = ",".join(self.schedule.get("times",["09:00","14:00","19:00"]))
        self._sched_times_entry = tk.Entry(self._sched_times_frame,
                                            font=(FONT_FAMILY,10),
                                            bg=PALETTE["bg"], relief="flat",
                                            highlightbackground=PALETTE["border"],
                                            highlightthickness=1)
        self._sched_times_entry.insert(0, times_str)
        self._sched_times_entry.pack(fill="x", pady=4, ipady=5)

        # 요일 선택
        self._separator(inner).pack(fill="x", pady=10)
        days_frame = tk.Frame(inner, bg=PALETTE["card"])
        days_frame.pack(fill="x", pady=6)
        self._label(days_frame, "실행 요일", 10, "bold").pack(anchor="w", pady=(0,6))
        days_row = tk.Frame(days_frame, bg=PALETTE["card"])
        days_row.pack(fill="x")
        days = self.schedule.get("days",[0,1,2,3,4])
        day_labels = ["월","화","수","목","금","토","일"]
        self._sched_day_vars = []
        for i, dl in enumerate(day_labels):
            var = tk.BooleanVar(value=i in days)
            self._sched_day_vars.append(var)
            cb = tk.Checkbutton(days_row, text=dl, variable=var,
                                font=(FONT_FAMILY,10),
                                bg=PALETTE["card"], fg=PALETTE["text"],
                                activebackground=PALETTE["card"],
                                selectcolor=PALETTE["card"])
            cb.pack(side="left", padx=6)

        self._separator(inner).pack(fill="x", pady=10)

        btn_row = tk.Frame(inner, bg=PALETTE["card"])
        btn_row.pack(fill="x")
        self._button(btn_row, "💾 저장", self._save_schedule,
                     color=PALETTE["success"]).pack(side="left")
        self._sched_status_lbl = self._label(btn_row, "스케줄 꺼짐",
                                              9, color=PALETTE["muted"])
        self._sched_status_lbl.pack(side="left", padx=12)

        self._update_sched_ui()

    def _refresh_schedule(self):
        pass

    def _update_sched_ui(self):
        mode = self._sched_mode_var.get()
        if mode == "interval":
            self._sched_interval_frame.pack(fill="x", pady=8)
            self._sched_times_frame.pack_forget()
        else:
            self._sched_interval_frame.pack_forget()
            self._sched_times_frame.pack(fill="x", pady=8)

    def _save_schedule(self):
        days = [i for i, v in enumerate(self._sched_day_vars) if v.get()]
        times_raw = self._sched_times_entry.get()
        times = [t.strip() for t in times_raw.split(",") if t.strip()]
        self.schedule = {
            "enabled":           self._sched_enabled_var.get(),
            "mode":              self._sched_mode_var.get(),
            "interval_hours":    self._sched_interval_var.get(),
            "interval_variance": self._sched_variance_var.get(),
            "times":             times,
            "days":              days,
        }
        save_json(CFG_SCHEDULE, self.schedule)
        messagebox.showinfo("저장","스케줄이 저장되었습니다.")
        if self.schedule["enabled"]:
            self._start_scheduler()
        else:
            self._stop_scheduler()
        self._stop_all_job_schedulers()   # 모든 개별 작업 스케줄러 중지

    def _toggle_schedule(self):
        if self._sched_enabled_var.get():
            self._sched_status_lbl.config(text="스케줄 활성화됨", fg=PALETTE["success"])
        else:
            self._sched_status_lbl.config(text="스케줄 꺼짐", fg=PALETTE["muted"])

    def _start_scheduler(self):
        self._stop_scheduler()
        self._scheduler_running = True
        self._sched_var.set("스케줄 ON")

        def _check_sched_match(sched, now):
            """전역/개별 스케줄 공통 트리거 판별. True이면 지금 실행할 시각."""
            if now.weekday() not in sched.get("days", [0,1,2,3,4,5,6]):
                return False
            if sched.get("mode", "interval") == "times":
                for t in sched.get("times", []):
                    try:
                        h2, m2 = map(int, t.split(":"))
                        target = now.replace(hour=h2, minute=m2, second=0, microsecond=0)
                        if 0 <= (target - now).total_seconds() < 60:
                            return True
                    except: pass
                return False
            return True   # interval 모드: 대기 후 항상 실행

        def _trigger_jobs(jobs_to_run, label=""):
            """이전 작업 완료 대기 후 jobs_to_run 실행 (별도 스레드)"""
            def _do():
                if self.engine.is_busy:
                    self._log_append(
                        f"[SCHED{label}] 이전 작업 실행 중 – 완료 대기...", "WARN")
                    self.engine.wait_until_idle()
                self.after(0, lambda: self._execute_jobs(jobs_to_run))
            threading.Thread(target=_do, daemon=True).start()

        def _run():
            # ── 전역 스케줄 루프 ──────────────────────────────────────
            global_last = [0.0]          # 마지막 interval 트리거 시각

            while self._scheduler_running:
                now    = datetime.now()
                gsched = self.schedule

                # ── 전역 스케줄 트리거 판별 ──
                global_trigger = False
                if gsched.get("mode", "interval") == "interval":
                    h = gsched.get("interval_hours", 3)
                    v = gsched.get("interval_variance", 30)
                    wait_sec = h * 3600 + random.randint(-v * 60, v * 60)
                    if (now.timestamp() - global_last[0]) >= wait_sec:
                        if now.weekday() in gsched.get("days", [0,1,2,3,4,5,6]):
                            global_trigger = True
                            global_last[0] = now.timestamp()
                else:
                    if _check_sched_match(gsched, now):
                        global_trigger = True

                if global_trigger:
                    # 전역 스케줄 따르는 활성 작업
                    # (개별 스케줄이 활성화된 작업은 제외)
                    global_jobs = [
                        j for j in self.jobs
                        if j.get("enabled", True)
                        and (
                            j.get("schedule", {}).get("use_global", True) or
                            not j.get("schedule", {}).get("enabled", False)
                        )
                    ]
                    if global_jobs:
                        self._log_append(
                            f"[SCHED] 전역 스케줄 실행: {len(global_jobs)}개 작업", "INFO")
                        _trigger_jobs(global_jobs, "")

                # 개별 스케줄은 각 작업의 독립 스레드(_start_job_scheduler)에서 처리
                # 전역 스케줄러는 전역 스케줄 설정이 활성화된 작업만 담당

                time.sleep(30)   # 30초마다 체크

        self._scheduler_thread = threading.Thread(target=_run, daemon=True)
        self._scheduler_thread.start()

    def _stop_scheduler(self):
        self._scheduler_running = False
        self._sched_var.set("스케줄 OFF")

    def _auto_post(self):
        """수동 실행 버튼 또는 레거시 호출용"""
        self._show_tab("jobs")
        active = [j for j in self.jobs if j.get("enabled", True)]
        if active:
            self._execute_jobs(active)
        else:
            self._log_append("[AUTO] 활성 작업 없음, 스케줄 실행 건너뜀", "WARN")

    # ══════════════════════════════════════════════════════════════
    #  탭 7: 옵션
    # ══════════════════════════════════════════════════════════════
    def _build_options_tab(self, parent):
        top = tk.Frame(parent, bg=PALETTE["bg"])
        top.pack(fill="x", padx=24, pady=(20,0))
        self._label(top, "실행 옵션", 16, "bold").pack(side="left")
        self._button(top, "❓ 도움말", lambda: self._show_help("options"),
                     color="#8B5CF6", size=8).pack(side="right")

        card = tk.Frame(parent, bg=PALETTE["card"],
                        highlightbackground=PALETTE["border"],
                        highlightthickness=1)
        card.pack(fill="x", padx=24, pady=16)
        inner = tk.Frame(card, bg=PALETTE["card"])
        inner.pack(fill="x", padx=32, pady=24)

        def section(title):
            f = tk.Frame(inner, bg=PALETTE["card"])
            f.pack(fill="x", pady=(12,4))
            self._label(f, title, 10, "bold", color=PALETTE["primary"]).pack(anchor="w")
            self._separator(f, color=PALETTE["primary"]).pack(fill="x", pady=4)
            return tk.Frame(inner, bg=PALETTE["card"])

        def field_row(parent, label, widget_factory):
            row = tk.Frame(parent, bg=PALETTE["card"])
            row.pack(fill="x", pady=5)
            tk.Label(row, text=label, font=(FONT_FAMILY,9),
                     fg=PALETTE["text2"], bg=PALETTE["card"],
                     width=18, anchor="e").pack(side="left")
            tk.Frame(row, bg=PALETTE["card"], width=12).pack(side="left")
            w = widget_factory(row)
            w.pack(side="left")
            return w

        # 딜레이/순서 설정은 작업 관리 탭으로 통합됨
        # (작업 관리 탭 하단 "실행 딜레이 & 순서" 카드 참고)

        # ── 오류 처리 ──
        sec2 = section("오류 처리")
        sec2.pack(fill="x")

        self._opt_retry_var = tk.IntVar(value=self.options.get("retry_count",2))
        field_row(sec2, "재시도 횟수",
                  lambda p: tk.Spinbox(p, from_=0, to=10,
                                        textvariable=self._opt_retry_var,
                                        font=(FONT_FAMILY,9), width=5,
                                        bg=PALETTE["bg"]))

        self._opt_error_var = tk.StringVar(value=self.options.get("on_error","skip"))
        err_row = tk.Frame(sec2, bg=PALETTE["card"])
        err_row.pack(fill="x", pady=5)
        tk.Label(err_row, text="오류 시", font=(FONT_FAMILY,9),
                 fg=PALETTE["text2"], bg=PALETTE["card"],
                 width=18, anchor="e").pack(side="left")
        tk.Frame(err_row, bg=PALETTE["card"], width=12).pack(side="left")
        for val, lab in [("skip","건너뜀"),("stop","중지"),("retry","재시도")]:
            tk.Radiobutton(err_row, text=lab,
                           variable=self._opt_error_var, value=val,
                           font=(FONT_FAMILY,9),
                           bg=PALETTE["card"], fg=PALETTE["text"],
                           activebackground=PALETTE["card"],
                           selectcolor=PALETTE["card"]).pack(side="left", padx=6)

        # ── 브라우저 ──
        sec3 = section("브라우저 설정")
        sec3.pack(fill="x")

        self._opt_headless_var = tk.BooleanVar(value=self.options.get("headless",False))
        hl_row = tk.Frame(sec3, bg=PALETTE["card"])
        hl_row.pack(fill="x", pady=5)
        tk.Label(hl_row, text="헤드리스 모드", font=(FONT_FAMILY,9),
                 fg=PALETTE["text2"], bg=PALETTE["card"],
                 width=18, anchor="e").pack(side="left")
        tk.Frame(hl_row, bg=PALETTE["card"], width=12).pack(side="left")
        tk.Checkbutton(hl_row, variable=self._opt_headless_var,
                       text="브라우저 창 숨김",
                       font=(FONT_FAMILY,9),
                       bg=PALETTE["card"], fg=PALETTE["text"],
                       activebackground=PALETTE["card"],
                       selectcolor=PALETTE["card"]).pack(side="left")

        self._separator(inner).pack(fill="x", pady=16)

        self._button(inner, "💾 옵션 저장", self._save_options,
                     color=PALETTE["success"]).pack(anchor="w")

    def _refresh_options(self):
        pass

    def _save_options(self):
        self.options = {
            "order":       self.options.get("order","sequential"),
            "delay_min":   self.options.get("delay_min",3),
            "delay_max":   self.options.get("delay_max",8),
            "retry_count": self._opt_retry_var.get(),
            "on_error":    self._opt_error_var.get(),
            "headless":    self._opt_headless_var.get(),
        }
        save_json(CFG_OPTIONS, self.options)
        messagebox.showinfo("저장","옵션이 저장되었습니다.")

    # ══════════════════════════════════════════════════════════════
    #  탭 8: 로그
    # ══════════════════════════════════════════════════════════════
    def _build_logs_tab(self, parent):
        top = tk.Frame(parent, bg=PALETTE["bg"])
        top.pack(fill="x", padx=24, pady=(20,0))
        self._label(top, "실행 로그", 16, "bold").pack(side="left")
        self._button(top, "❓ 도움말", lambda: self._show_help("logs"),
                     color="#8B5CF6", size=8).pack(side="right")

        toolbar = tk.Frame(parent, bg=PALETTE["bg"])
        toolbar.pack(fill="x", padx=24, pady=10)
        self._button(toolbar, "🗑 로그 지우기", self._clear_logs,
                     color="#64748B").pack(side="left")
        self._button(toolbar, "📁 로그 폴더 열기", self._open_log_folder,
                     color="#64748B").pack(side="left", padx=6)

        # 필터
        filter_row = tk.Frame(toolbar, bg=PALETTE["bg"])
        filter_row.pack(side="right")
        self._label(filter_row, "필터: ", 9, color=PALETTE["text2"]).pack(side="left")
        self._log_filter_var = tk.StringVar(value="ALL")
        for val in ["ALL","SUCCESS","ERROR","WARN","DEBUG"]:
            color = {"ALL":PALETTE["text"],"SUCCESS":PALETTE["success"],
                     "ERROR":PALETTE["danger"],"WARN":PALETTE["warning"],
                     "DEBUG":"#60A5FA"}[val]
            tk.Radiobutton(filter_row, text=val,
                           variable=self._log_filter_var, value=val,
                           font=(FONT_FAMILY,8), fg=color,
                           bg=PALETTE["bg"],
                           activebackground=PALETTE["bg"],
                           selectcolor=PALETTE["bg"],
                           command=self._apply_log_filter).pack(side="left", padx=3)

        # 통계 배지
        stat_row = tk.Frame(parent, bg=PALETTE["bg"])
        stat_row.pack(fill="x", padx=24, pady=(0,6))
        self._log_stats = {}
        for key, label, color in [
            ("total","전체",PALETTE["text"]),
            ("success","성공",PALETTE["success"]),
            ("error","오류",PALETTE["danger"]),
            ("warn","경고",PALETTE["warning"])
        ]:
            f = tk.Frame(stat_row, bg=color, padx=10, pady=4)
            f.pack(side="left", padx=3)
            var = tk.StringVar(value=f"{label} 0")
            tk.Label(f, textvariable=var, font=(FONT_FAMILY,8,"bold"),
                     fg="#fff", bg=color).pack()
            self._log_stats[key] = var

        card = tk.Frame(parent, bg=PALETTE["card"],
                        highlightbackground=PALETTE["border"],
                        highlightthickness=1)
        card.pack(fill="both", expand=True, padx=24, pady=(0,16))

        self._log_text = tk.Text(card, font=("Consolas" if os.name=="nt" else "monospace", 9),
                                  bg="#0F172A", fg="#E2E8F0",
                                  relief="flat", wrap="word",
                                  state="disabled")
        log_sb = ttk.Scrollbar(card, command=self._log_text.yview)
        self._log_text.configure(yscrollcommand=log_sb.set)
        log_sb.pack(side="right", fill="y")
        self._log_text.pack(fill="both", expand=True, padx=4, pady=4)

        self._log_text.tag_configure("SUCCESS", foreground="#4ADE80")
        self._log_text.tag_configure("ERROR",   foreground="#F87171")
        self._log_text.tag_configure("WARN",    foreground="#FBBF24")
        self._log_text.tag_configure("INFO",    foreground="#94A3B8")
        self._log_text.tag_configure("DEBUG",   foreground="#60A5FA")

        self._log_entries = []

    def _log_append(self, entry, level="INFO"):
        self._log_entries.append((level, entry))
        self._apply_log_filter()
        # 통계
        total   = len(self._log_entries)
        success = sum(1 for l,_ in self._log_entries if l=="SUCCESS")
        error   = sum(1 for l,_ in self._log_entries if l=="ERROR")
        warn    = sum(1 for l,_ in self._log_entries if l=="WARN")
        self._log_stats["total"].set(f"전체 {total}")
        self._log_stats["success"].set(f"성공 {success}")
        self._log_stats["error"].set(f"오류 {error}")
        self._log_stats["warn"].set(f"경고 {warn}")
        self._log_count_var.set(f"로그 {total}건")

    def _apply_log_filter(self):
        filt = self._log_filter_var.get()
        self._log_text.config(state="normal")
        self._log_text.delete("1.0","end")
        for level, entry in self._log_entries:
            if filt == "ALL" or filt == level:
                self._log_text.insert("end", entry + "\n", level)
        self._log_text.config(state="disabled")
        self._log_text.see("end")

    def _refresh_logs(self):
        pass

    # ── 결과 내역 기록 ────────────────────────────────────────────
    def _record_result(self, status, entry):
        """포스팅 결과를 _posting_results 에 저장 후 stats 탭 갱신"""
        from datetime import datetime as _dt
        ts = _dt.now().strftime("%Y-%m-%d %H:%M:%S")
        # entry 파싱: [YYYY-MM-DD HH:MM:SS] [LEVEL] SITE | ACCOUNT → MSG
        site    = ""
        account = ""
        msg     = entry
        try:
            # 예: [2025-01-01 12:00:00] [SUCCESS] 마멘토 | user@id → 게시 완료 → ...
            m = re.search(r'\]\s+(.+?)\s+\|\s+(.+?)\s+→\s+(.+)$', entry)
            if m:
                site    = m.group(1).strip()
                account = m.group(2).strip()
                msg     = m.group(3).strip()
        except Exception:
            pass
        self._posting_results.append({
            "ts":      ts,
            "status":  status,
            "site":    site,
            "account": account,
            "msg":     msg,
        })
        # stats 탭 실시간 갱신
        if hasattr(self, "_stats_tree"):
            self.after(0, self._stats_insert_row,
                       ts, status, site, account, msg)
            self.after(0, self._stats_update_badges)

    def _stats_insert_row(self, ts, status, site, account, msg):
        """Treeview에 결과 행 삽입"""
        filt = self._stats_filter_var.get() if hasattr(self,"_stats_filter_var") else "ALL"
        if filt != "ALL" and filt != status:
            return
        tag = "success" if status == "SUCCESS" else "error"
        icon = "✅" if status == "SUCCESS" else "❌"
        self._stats_tree.insert("", 0,
            values=(ts, icon + " " + status, site, account, msg[:80]),
            tags=(tag,))

    def _stats_update_badges(self):
        """통계 배지 숫자 갱신"""
        if not hasattr(self, "_stats_badge_vars"):
            return
        total   = len(self._posting_results)
        success = sum(1 for r in self._posting_results if r["status"] == "SUCCESS")
        fail    = total - success
        rate    = int(success / total * 100) if total else 0
        self._stats_badge_vars["total"].set(str(total))
        self._stats_badge_vars["success"].set(str(success))
        self._stats_badge_vars["fail"].set(str(fail))
        self._stats_badge_vars["rate"].set(f"{rate}%")

    # ── 통계 탭 빌드 ──────────────────────────────────────────────
    def _build_stats_tab(self, parent):
        # 가이드 카드
        # stats 헤더
        stats_top = tk.Frame(parent, bg=PALETTE["bg"])
        stats_top.pack(fill="x", padx=24, pady=(20,0))
        self._label(stats_top, "결과 통계", 16, "bold").pack(side="left")
        self._button(stats_top, "❓ 도움말", lambda: self._show_help("stats"),
                     color="#8B5CF6", size=8).pack(side="right")

        guide = tk.Frame(parent, bg="#EFF6FF", padx=16, pady=10)
        guide.pack(fill="x", padx=24, pady=(14,0))
        tk.Label(guide, text="📊 결과 통계 & 포스팅 내역",
                 font=(FONT_FAMILY,10,"bold"), fg="#1E40AF", bg="#EFF6FF").pack(anchor="w")
        tk.Label(guide,
                 text="포스팅 실행 후 성공/실패 내역을 확인할 수 있습니다.\n날짜를 선택하면 과거 기록도 조회할 수 있어요. (로그 폴더의 CSV 파일 기반)",
                 font=(FONT_FAMILY,9), fg="#3B82F6", bg="#EFF6FF", justify="left").pack(anchor="w")

        # ── 통계 배지 카드 ────────────────────────────────────────
        badge_outer = tk.Frame(parent, bg=PALETTE["bg"])
        badge_outer.pack(fill="x", padx=24, pady=(12,4))
        self._stats_badge_vars = {}
        badge_defs = [
            ("total",   "전체",   PALETTE["text"],    "#F1F5F9"),
            ("success", "성공",   PALETTE["success"], "#DCFCE7"),
            ("fail",    "실패",   PALETTE["danger"],  "#FEE2E2"),
            ("rate",    "성공률", PALETTE["primary"], "#DBEAFE"),
        ]
        for key, label, fg_c, bg_c in badge_defs:
            cell = tk.Frame(badge_outer, bg=bg_c,
                            highlightbackground=PALETTE["border"],
                            highlightthickness=1,
                            padx=20, pady=14)
            cell.pack(side="left", padx=6, pady=2)
            var = tk.StringVar(value="0" if key != "rate" else "0%")
            tk.Label(cell, textvariable=var,
                     font=(FONT_FAMILY, 20, "bold"),
                     fg=fg_c, bg=bg_c).pack()
            tk.Label(cell, text=label,
                     font=(FONT_FAMILY, 9),
                     fg=PALETTE["text2"], bg=bg_c).pack()
            self._stats_badge_vars[key] = var

        # ── 날짜 선택 & 조회 도구모음 ─────────────────────────────
        ctrl_row = tk.Frame(parent, bg=PALETTE["bg"])
        ctrl_row.pack(fill="x", padx=24, pady=(8,4))

        tk.Label(ctrl_row, text="📅 날짜 선택:",
                 font=(FONT_FAMILY,9,"bold"), fg=PALETTE["text2"],
                 bg=PALETTE["bg"]).pack(side="left")

        # 날짜 목록 생성
        import glob as _glob
        log_files = sorted(_glob.glob(str(LOG_DIR / "log_*.csv")), reverse=True)
        date_opts = ["오늘 (실시간)"]
        for lf in log_files:
            fname = os.path.basename(lf)
            date_part = fname.replace("log_","").replace(".csv","")
            if date_part not in date_opts:
                date_opts.append(date_part)
        if len(date_opts) == 1:
            date_opts.append("기록 없음")

        self._stats_date_var = tk.StringVar(value=date_opts[0])
        date_combo = ttk.Combobox(ctrl_row, textvariable=self._stats_date_var,
                                  values=date_opts, width=18,
                                  font=(FONT_FAMILY,9), state="readonly")
        date_combo.pack(side="left", padx=8)

        # 필터
        tk.Label(ctrl_row, text="  필터:",
                 font=(FONT_FAMILY,9), fg=PALETTE["text2"],
                 bg=PALETTE["bg"]).pack(side="left")
        self._stats_filter_var = tk.StringVar(value="ALL")
        for val, fg_c in [("ALL","#1E293B"),("SUCCESS","#22C55E"),("FAIL","#EF4444")]:
            tk.Radiobutton(ctrl_row, text=val,
                           variable=self._stats_filter_var, value=val,
                           font=(FONT_FAMILY,8), fg=fg_c,
                           bg=PALETTE["bg"], activebackground=PALETTE["bg"],
                           selectcolor=PALETTE["bg"],
                           command=self._refresh_stats).pack(side="left", padx=3)

        self._button(ctrl_row, "🔄 새로고침", self._refresh_stats,
                     color=PALETTE["primary"]).pack(side="left", padx=10)
        self._button(ctrl_row, "📤 CSV 내보내기", self._export_stats_csv,
                     color="#64748B").pack(side="left")
        self._button(ctrl_row, "🗑 내역 지우기", self._clear_stats,
                     color=PALETTE["danger"]).pack(side="left", padx=4)

        # ── 결과 Treeview ─────────────────────────────────────────
        tree_frame = tk.Frame(parent, bg=PALETTE["card"],
                              highlightbackground=PALETTE["border"],
                              highlightthickness=1)
        tree_frame.pack(fill="both", expand=True, padx=24, pady=(4,16))

        cols = ("time", "status", "site", "account", "message")
        col_labels = {"time":"시간", "status":"상태",
                      "site":"사이트", "account":"계정", "message":"결과 메시지"}
        col_widths = {"time":148, "status":80, "site":100,
                      "account":130, "message":400}

        style = ttk.Style()
        style.configure("Stats.Treeview",
                        font=(FONT_FAMILY,9),
                        rowheight=26,
                        background="#FFFFFF",
                        fieldbackground="#FFFFFF")
        style.configure("Stats.Treeview.Heading",
                        font=(FONT_FAMILY,9,"bold"))

        self._stats_tree = ttk.Treeview(tree_frame,
                                         columns=cols,
                                         show="headings",
                                         style="Stats.Treeview",
                                         selectmode="browse")
        for c in cols:
            self._stats_tree.heading(c, text=col_labels[c])
            self._stats_tree.column(c, width=col_widths[c], minwidth=60)

        self._stats_tree.tag_configure("success", foreground="#166534", background="#DCFCE7")
        self._stats_tree.tag_configure("error",   foreground="#991B1B", background="#FEE2E2")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical",
                            command=self._stats_tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal",
                            command=self._stats_tree.xview)
        self._stats_tree.configure(yscrollcommand=vsb.set,
                                   xscrollcommand=hsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        self._stats_tree.pack(fill="both", expand=True, padx=2, pady=2)

        # 초기 데이터 로드
        self.after(100, self._refresh_stats)

    def _refresh_stats(self):
        """날짜 선택에 따라 결과 Treeview 갱신"""
        if not hasattr(self, "_stats_tree"):
            return
        # 트리 초기화
        for row in self._stats_tree.get_children():
            self._stats_tree.delete(row)

        date_sel = self._stats_date_var.get() if hasattr(self,"_stats_date_var") else "오늘 (실시간)"
        filt = self._stats_filter_var.get() if hasattr(self,"_stats_filter_var") else "ALL"

        rows = []
        if date_sel == "오늘 (실시간)":
            # 메모리의 실시간 결과
            rows = [(r["ts"], r["status"], r["site"], r["account"], r["msg"])
                    for r in self._posting_results]
        else:
            # CSV 파일에서 읽기
            csv_file = LOG_DIR / f"log_{date_sel}.csv"
            if csv_file.exists():
                try:
                    import csv as _csv
                    with open(csv_file, "r", encoding="utf-8-sig") as f:
                        reader = _csv.reader(f)
                        for row in reader:
                            if len(row) >= 5:
                                ts, level, site, account, msg = row[0],row[1],row[2],row[3],row[4]
                                rows.append((ts, level, site, account, msg))
                except Exception as e:
                    rows = []

        # 필터 적용 후 삽입 (최신순)
        total = success = fail = 0
        for ts, status, site, account, msg in reversed(rows):
            if filt != "ALL" and filt != status:
                continue
            if status not in ("SUCCESS","ERROR","WARN","FAIL"):
                continue
            total += 1
            if status == "SUCCESS":
                success += 1
                tag = "success"
                icon = "✅"
            else:
                fail += 1
                tag = "error"
                icon = "❌"
            self._stats_tree.insert("", "end",
                values=(ts, icon+" "+status, site, account, msg[:100]),
                tags=(tag,))

        # 배지 갱신
        rate = int(success/total*100) if total else 0
        if hasattr(self,"_stats_badge_vars"):
            self._stats_badge_vars["total"].set(str(total))
            self._stats_badge_vars["success"].set(str(success))
            self._stats_badge_vars["fail"].set(str(fail))
            self._stats_badge_vars["rate"].set(f"{rate}%")

    def _export_stats_csv(self):
        """현재 테이블 내용을 CSV로 내보내기"""
        from tkinter import filedialog as _fd
        path = _fd.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV","*.csv")],
            initialfile="포스팅결과.csv")
        if not path:
            return
        import csv as _csv
        from datetime import datetime as _dt
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            w = _csv.writer(f)
            w.writerow(["시간","상태","사이트","계정","결과메시지"])
            for child in self._stats_tree.get_children():
                vals = self._stats_tree.item(child, "values")
                w.writerow(vals)
        messagebox.showinfo("완료", f"CSV 저장 완료:\n{path}")

    def _clear_stats(self):
        """실시간 결과 내역 초기화"""
        if not messagebox.askyesno("확인", "결과 내역을 지우시겠습니까?\n(로그 파일은 삭제되지 않습니다)"):
            return
        self._posting_results.clear()
        for row in self._stats_tree.get_children():
            self._stats_tree.delete(row)
        self._stats_update_badges()

    def _clear_logs(self):
        self._log_entries.clear()
        self._log_text.config(state="normal")
        self._log_text.delete("1.0","end")
        self._log_text.config(state="disabled")

    def _open_log_folder(self):
        if os.name == "nt":
            os.startfile(str(LOG_DIR))
        else:
            import subprocess
            subprocess.Popen(["xdg-open", str(LOG_DIR)])

    # ──────────────────────────────────────────────────────────────
    #  종료
    # ──────────────────────────────────────────────────────────────
    def _on_close(self):
        self.engine.stop()
        self._stop_scheduler()
        self.destroy()


# ═══════════════════════════════════════════════════════════════════
#  계정 편집 다이얼로그
# ═══════════════════════════════════════════════════════════════════
class AccountDialog(tk.Toplevel):
    """
    계정 추가/수정 다이얼로그.
    사이트를 선택하면 해당 커뮤니티 전용 입력 항목이 자동으로 표시됩니다.

    공통 항목  : 사이트, 아이디, 비밀번호, 글쓰기URL, 메모, 활성화
    아이보스   : 회사명, 담당자명, 연락처, 이메일, 네이트온ID, 카카오톡ID
    마멘토     : 게시판(드롭다운 30종), 부가링크1, 부가링크2
    투잡커넥트 : 카테고리(업체홍보/작업의뢰), 부가링크1, 부가링크2
    비즈모아   : 카테고리, 부가링크1, 부가링크2
    셀프모아   : 카테고리, 부가링크1, 부가링크2
    """

    # 사이트별 추가 표시 필드 키 목록
    _SITE_FIELDS = {
        "아이보스":   ["category", "company", "manager", "contact", "email", "nate", "kakao"],
        "마멘토":     ["category", "link1", "link2"],
        "투잡커넥트": ["category", "link1", "link2"],
        "비즈모아":   ["category", "link1", "link2"],
        "셀프모아":   ["category", "link1", "link2"],
    }

    # 사이트별 카테고리 선택지 (None → MAMENTOR_BOARDS 사용)
    _SITE_CAT_VALUES = {
        "마멘토":     None,  # 마멘토는 별도 게시판 드롭다운 (MAMENTOR_BOARDS)
        "투잡커넥트": ["", "업체홍보", "작업의뢰"],
        "비즈모아":   [""],
        "셀프모아":   ["", "블로그", "SNS", "기타"],  # SELFMOA_BOARDS 한글명
        # 아이보스 구분(카테고리): 한글명 표시 (_post_iboss에서 한글→code 역변환 지원)
        # 매체별: 블로그(B) 카페(C) 인스타그램(A) 유튜브(D) SNS(S) 스토어(J) 언론홍보(U) SEO(W) 지도(F)
        # 유형별: 포스팅(G) 체험단(E) 인플루언서(H) 숏폼(O) PPL(N)
        # 기타:   기타(Z)
        "아이보스":   [
            "",
            "블로그",
            "카페",
            "인스타그램",
            "유튜브",
            "SNS",
            "스토어",
            "언론홍보",
            "SEO",
            "지도",
            "포스팅",
            "체험단",
            "인플루언서",
            "숏폼",
            "PPL",
            "기타",
        ],
    }

    def __init__(self, parent, title, data, site_names):
        super().__init__(parent)
        self.title(title)
        self.geometry("520x460")
        self.configure(bg=PALETTE["card"])
        self.resizable(False, True)
        self.grab_set()
        self.result    = None
        self._site_names = site_names
        self._data     = dict(data)
        self._vars     = {}
        self._rows     = []   # (key, tags, frame) 목록
        self._cat_cbs  = []   # 카테고리 콤보박스 참조 목록
        self._iboss_cat_cb = None  # 아이보스 구분 콤보박스 참조
        # ── category 필드는 사이트마다 다른 위젯 → 각각 별도 var 유지
        # _refresh() 에서 현재 사이트에 맞는 var를 _vars["category"]에 연결
        self._cat_iboss_var    = None  # 아이보스 전용
        self._cat_mamentor_var = None  # 마멘토 전용
        self._cat_combo_var    = None  # 투잡/비즈모아/셀프모아 전용
        self._build(title)
        self.transient(parent)
        self.wait_window()

    # ── UI 구성 ──────────────────────────────────────────────────
    def _build(self, title):
        # ── 헤더 ────────────────────────────────────────────────
        hdr = tk.Frame(self, bg=PALETTE["sidebar"], padx=20, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text=title, font=(FONT_FAMILY, 12, "bold"),
                 fg="#F1F5F9", bg=PALETTE["sidebar"]).pack(side="left")

        # ── 스크롤 캔버스 ───────────────────────────────────────
        self._canvas = tk.Canvas(self, bg=PALETTE["card"],
                                  highlightthickness=0)
        vsb = ttk.Scrollbar(self, orient="vertical",
                             command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self._canvas.pack(fill="both", expand=True)

        self._inner = tk.Frame(self._canvas, bg=PALETTE["card"])
        self._win_id = self._canvas.create_window(
            (0, 0), window=self._inner, anchor="nw")
        self._inner.bind("<Configure>",
            lambda e: self._canvas.configure(
                scrollregion=self._canvas.bbox("all")))
        self._canvas.bind("<Configure>",
            lambda e: self._canvas.itemconfig(self._win_id, width=e.width))

        # ── 공통 필드 ───────────────────────────────────────────
        self._mk_field("site",     "사이트",              "combo",    tags=None)
        self._mk_field("id",       "아이디",              "entry",    tags=None)
        self._mk_field("password", "비밀번호",            "password", tags=None)
        self._mk_field("write_url","글쓰기 URL\n(비워두면 기본값)", "entry", tags=None)

        # ── 구분선 · 섹션 헤더 (사이트 전용 필드가 있을 때만 표시) ──
        self._sep = tk.Frame(self._inner, bg=PALETTE["border"], height=1)
        self._sep.pack(fill="x", padx=24, pady=(8, 0))
        self._sec_lbl = tk.Label(
            self._inner,
            text="── 커뮤니티 추가 정보 ──",
            font=(FONT_FAMILY, 8), fg=PALETTE["muted"],
            bg=PALETTE["card"])
        self._sec_lbl.pack(pady=(2, 4))

        # ── 아이보스 전용 ────────────────────────────────────────
        # ↳ 구분(카테고리) 가장 먼저 표시 (글쓰기 폼 순서와 동일)
        self._mk_field("category", "구분 (카테고리)", "cat_iboss",
                       tags={"아이보스"})
        self._mk_field("company", "회사명",       "entry", tags={"아이보스"})
        self._mk_field("manager", "담당자명",      "entry", tags={"아이보스"})
        self._mk_field("contact", "연락처",        "entry", tags={"아이보스"})
        self._mk_field("email",   "이메일",        "entry", tags={"아이보스"})
        self._mk_field("nate",    "네이트온 ID",   "entry", tags={"아이보스"})
        self._mk_field("kakao",   "카카오톡 ID",   "entry", tags={"아이보스"})

        # ── 마멘토 전용 (게시판 드롭다운) ───────────────────────
        self._mk_field("category", "게시판",      "cat_mamentor",
                       tags={"마멘토"})

        # ── 투잡커넥트/비즈모아/셀프모아 전용 (카테고리) ─────────
        self._mk_field("category", "카테고리",    "cat_combo",
                       tags={"투잡커넥트", "비즈모아", "셀프모아"})

        # ── 링크 (마멘토·투잡커넥트·비즈모아·셀프모아 공통) ─────
        self._mk_field("link1", "부가링크1 (link1)", "entry",
                       tags={"마멘토", "투잡커넥트", "비즈모아", "셀프모아"})
        self._mk_field("link2", "부가링크2 (link2)", "entry",
                       tags={"마멘토", "투잡커넥트", "비즈모아", "셀프모아"})

        # ── 공통 하단 필드 ───────────────────────────────────────
        bot_sep = tk.Frame(self._inner, bg=PALETTE["border"], height=1)
        bot_sep.pack(fill="x", padx=24, pady=(8, 0))
        self._mk_field("memo",    "메모",    "text",  tags=None)
        self._mk_field("enabled", "활성화",  "check", tags=None)

        # ── 저장/취소 버튼 ───────────────────────────────────────
        btn_frame = tk.Frame(self, bg=PALETTE["card"])
        btn_frame.pack(fill="x", padx=24, pady=16)
        tk.Button(btn_frame, text="저장",
                  font=(FONT_FAMILY, 10, "bold"),
                  bg=PALETTE["primary"], fg="#fff",
                  relief="flat", padx=20, pady=6, cursor="hand2",
                  command=self._save).pack(side="right", padx=4)
        tk.Button(btn_frame, text="취소",
                  font=(FONT_FAMILY, 10),
                  bg="#E2E8F0", fg=PALETTE["text"],
                  relief="flat", padx=20, pady=6, cursor="hand2",
                  command=self.destroy).pack(side="right", padx=4)

        # ── 초기 사이트에 맞게 필드 갱신 ────────────────────────
        init_site = self._data.get("site", "")
        self._refresh(init_site)

        # 사이트 변경 감지
        self._vars["site"].trace_add(
            "write", lambda *_: self._refresh(self._vars["site"].get()))

    # ── 필드 생성 헬퍼 ────────────────────────────────────────────
    def _mk_field(self, key, label, ftype, tags=None):
        """
        key   : 데이터 키
        label : 라벨 텍스트 (줄바꿈 가능)
        ftype : entry / password / combo / cat_mamentor / cat_iboss / cat_combo / text / check
        tags  : None이면 항상 표시, set이면 해당 사이트에서만 표시
        """
        row = tk.Frame(self._inner, bg=PALETTE["card"])
        row.pack(fill="x", padx=24, pady=4)
        self._rows.append((key, tags, row))

        val = self._data.get(key, "" if ftype != "check" else True)

        tk.Label(row, text=label,
                 font=(FONT_FAMILY, 9), fg=PALETTE["text2"],
                 bg=PALETTE["card"], width=16, anchor="e",
                 justify="right").pack(side="left")
        tk.Frame(row, bg=PALETTE["card"], width=8).pack(side="left")

        if ftype == "entry":
            var = tk.StringVar(value=str(val))
            tk.Entry(row, textvariable=var, font=(FONT_FAMILY, 9),
                     bg=PALETTE["bg"], relief="flat",
                     highlightbackground=PALETTE["border"],
                     highlightthickness=1, width=30
                     ).pack(side="left", ipady=4, fill="x", expand=True)
            self._vars.setdefault(key, var)

        elif ftype == "password":
            var = tk.StringVar(value=str(val))
            e = tk.Entry(row, textvariable=var, font=(FONT_FAMILY, 9),
                         bg=PALETTE["bg"], relief="flat",
                         highlightbackground=PALETTE["border"],
                         highlightthickness=1, show="●", width=30)
            e.pack(side="left", ipady=4, fill="x", expand=True)
            sv = tk.BooleanVar(value=False)
            def _tog(s=sv, ew=e): ew.config(show="" if s.get() else "●")
            tk.Checkbutton(row, text="보기", variable=sv, command=_tog,
                           font=(FONT_FAMILY, 8), bg=PALETTE["card"],
                           activebackground=PALETTE["card"],
                           selectcolor=PALETTE["card"]
                           ).pack(side="left", padx=4)
            self._vars.setdefault(key, var)

        elif ftype == "combo":
            var = tk.StringVar(value=str(val))
            ttk.Combobox(row, textvariable=var,
                         values=self._site_names, width=18
                         ).pack(side="left")
            self._vars.setdefault(key, var)

        elif ftype == "cat_mamentor":
            # 마멘토: MAMENTOR_BOARDS 드롭다운
            var = tk.StringVar(value=str(val))
            mam_vals = [""] + list(MAMENTOR_BOARDS.values())
            cb = ttk.Combobox(row, textvariable=var,
                              values=mam_vals, width=24)
            cb.pack(side="left")
            tk.Label(row, text="bo_table 직접 입력 가능",
                     font=(FONT_FAMILY, 8), fg=PALETTE["muted"],
                     bg=PALETTE["card"]).pack(side="left", padx=6)
            self._cat_mamentor_var = var  # ★ 마멘토 category var 보관
            self._vars.setdefault(key, var)

        elif ftype == "cat_iboss":
            # 아이보스 전용: 구분(카테고리) 콤보박스 (한글 레이블, _post_iboss 역변환 지원)
            iboss_vals = self._SITE_CAT_VALUES.get("아이보스", [""])
            var = tk.StringVar(value=str(val))
            cb = ttk.Combobox(row, textvariable=var,
                              values=iboss_vals, width=18)
            cb.pack(side="left")
            tk.Label(row, text="블로그/카페/인스타그램/… 직접 입력도 가능",
                     font=(FONT_FAMILY, 8), fg=PALETTE["muted"],
                     bg=PALETTE["card"]).pack(side="left", padx=6)
            self._iboss_cat_cb = cb   # _refresh 에서 직접 참조
            self._cat_iboss_var = var  # ★ 아이보스 category var 보관
            self._vars.setdefault(key, var)

        elif ftype == "cat_combo":
            # 투잡커넥트/비즈모아/셀프모아: 선택지 드롭다운
            var = tk.StringVar(value=str(val))
            cb = ttk.Combobox(row, textvariable=var, values=[""], width=18)
            cb.pack(side="left")
            self._cat_cbs.append(cb)   # 사이트 변경 시 값 교체용
            self._cat_combo_var = var   # ★ 투잡/비즈모아/셀프모아 category var 보관
            self._vars.setdefault(key, var)

        elif ftype == "text":
            var = tk.StringVar(value=str(val))
            tk.Entry(row, textvariable=var, font=(FONT_FAMILY, 9),
                     bg=PALETTE["bg"], relief="flat",
                     highlightbackground=PALETTE["border"],
                     highlightthickness=1, width=30
                     ).pack(side="left", ipady=4, fill="x", expand=True)
            self._vars.setdefault(key, var)

        elif ftype == "check":
            var = tk.BooleanVar(value=bool(val))
            tk.Checkbutton(row, variable=var, bg=PALETTE["card"],
                           activebackground=PALETTE["card"],
                           selectcolor=PALETTE["card"]).pack(side="left")
            self._vars.setdefault(key, var)

    # ── 사이트 변경 시 필드 show/hide ────────────────────────────
    def _refresh(self, site: str):
        for key, tags, row in self._rows:
            if tags is None or site in tags:
                row.pack(fill="x", padx=24, pady=4)
            else:
                row.pack_forget()

        # cat_combo 선택지 업데이트 (투잡커넥트 등)
        cat_vals = self._SITE_CAT_VALUES.get(site, [""])
        if cat_vals:
            for cb in self._cat_cbs:
                cb.configure(values=cat_vals)

        # ★ 핵심 수정: 사이트에 맞는 category var를 _vars["category"]에 동적 연결
        # setdefault 로 첫 번째(아이보스) var만 등록됐던 설계 오류를 여기서 보정
        if site == "아이보스" and self._cat_iboss_var is not None:
            self._vars["category"] = self._cat_iboss_var
        elif site == "마멘토" and self._cat_mamentor_var is not None:
            self._vars["category"] = self._cat_mamentor_var
        elif site in ("투잡커넥트", "비즈모아", "셀프모아") and self._cat_combo_var is not None:
            self._vars["category"] = self._cat_combo_var

        # 구분선/헤더 표시 여부
        if self._SITE_FIELDS.get(site):
            self._sep.pack(fill="x", padx=24, pady=(8, 0))
            self._sec_lbl.pack(pady=(2, 4))
        else:
            self._sep.pack_forget()
            self._sec_lbl.pack_forget()

        # 높이 자동 조정
        self._inner.update_idletasks()
        needed = self._inner.winfo_reqheight() + 120
        h = max(380, min(needed, 700))
        self.geometry(f"520x{h}")
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    # ── 저장 ─────────────────────────────────────────────────────
    def _save(self):
        result = {k: v.get() for k, v in self._vars.items()}
        if not result.get("site"):
            messagebox.showwarning("경고", "사이트를 선택하세요.", parent=self)
            return
        if not result.get("id"):
            messagebox.showwarning("경고", "아이디를 입력하세요.", parent=self)
            return
        self.result = result
        self.destroy()
# ═══════════════════════════════════════════════════════════════════
#  작업 편집 다이얼로그 (JobDialog)
# ═══════════════════════════════════════════════════════════════════
class JobDialog(tk.Toplevel):
    def __init__(self, parent, title, data, accounts, contents, sites=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("720x760")
        self.configure(bg=PALETTE["card"])
        self.resizable(True, True)
        self.grab_set()
        self.result      = None
        self._accounts      = accounts
        self._contents      = contents
        self._sites         = sites or {}
        self._data          = dict(data)
        self._build(title)
        self.transient(parent)
        self.wait_window()

    def _build(self, title):
        hdr = tk.Frame(self, bg=PALETTE["sidebar"], padx=20, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text=title, font=(FONT_FAMILY, 12, "bold"),
                 fg="#F1F5F9", bg=PALETTE["sidebar"]).pack(side="left")

        body = tk.Frame(self, bg=PALETTE["card"])
        body.pack(fill="both", expand=True, padx=20, pady=16)

        # ── 작업명
        rn = tk.Frame(body, bg=PALETTE["card"]); rn.pack(fill="x", pady=4)
        tk.Label(rn, text="작업명", font=(FONT_FAMILY,9), fg=PALETTE["text2"],
                 bg=PALETTE["card"], width=10, anchor="e").pack(side="left")
        tk.Frame(rn, bg=PALETTE["card"], width=8).pack(side="left")
        self._name_var = tk.StringVar(value=self._data.get("name",""))
        tk.Entry(rn, textvariable=self._name_var, font=(FONT_FAMILY,10),
                 bg=PALETTE["bg"], relief="flat",
                 highlightbackground=PALETTE["border"],
                 highlightthickness=1).pack(side="left", fill="x", expand=True, ipady=4)

        # ── 계정 선택
        ra = tk.Frame(body, bg=PALETTE["card"]); ra.pack(fill="x", pady=4)
        tk.Label(ra, text="계정", font=(FONT_FAMILY,9), fg=PALETTE["text2"],
                 bg=PALETTE["card"], width=10, anchor="e").pack(side="left")
        tk.Frame(ra, bg=PALETTE["card"], width=8).pack(side="left")
        # 드롭다운 항목: "사이트 | 아이디 | 메모(있으면)"
        def _acc_label(a):
            base = f"{a.get('site','')} | {a.get('id','')}"
            memo = (a.get("memo") or "").strip()
            return f"{base}  [{memo}]" if memo else base
        acc_labels     = [_acc_label(a)         for a in self._accounts]
        acc_labels_key = [f"{a.get('site','')} | {a.get('id','')}" for a in self._accounts]
        self._acc_var = tk.StringVar()
        saved_ai = self._data.get("account_idx", -1)
        if 0 <= saved_ai < len(acc_labels):
            self._acc_var.set(acc_labels[saved_ai])
        _acc_combo = ttk.Combobox(ra, textvariable=self._acc_var,
                     values=acc_labels, width=44, state="readonly")
        _acc_combo.pack(side="left")

        # ── 계정 상세 정보 카드 (선택 시 업데이트) ──────────────
        _acc_info_frame = tk.Frame(body,
                                    bg="#F0F9FF",
                                    highlightbackground="#BAE6FD",
                                    highlightthickness=1)
        _acc_info_frame.pack(fill="x", pady=(0, 4), padx=0)

        _acc_detail_lbl = tk.Label(_acc_info_frame,
            text="",
            font=(FONT_FAMILY, 8),
            fg="#0369A1", bg="#F0F9FF",
            anchor="w", justify="left",
            padx=10, pady=5)
        _acc_detail_lbl.pack(fill="x")

        def _update_acc_info(*_):
            sel = self._acc_var.get()
            # acc_labels 에서 인덱스 찾기
            idx = -1
            for i, lbl in enumerate(acc_labels):
                if lbl == sel:
                    idx = i; break
            if idx < 0:
                _acc_info_frame.pack_forget()
                return
            a = self._accounts[idx]
            site_val = a.get("site",  "")
            id_val   = a.get("id",    "")
            memo_val = (a.get("memo") or "").strip()
            pw_val   = a.get("password", "")
            pw_mask  = ("●" * min(len(pw_val), 8)) if pw_val else "(없음)"
            parts = [
                f"🌐 커뮤니티: {site_val}",
                f"👤 아이디:   {id_val}",
                f"🔒 비밀번호: {pw_mask}",
            ]
            if memo_val:
                parts.append(f"📝 메모:     {memo_val}")
            _acc_detail_lbl.config(text="   ".join(parts))
            _acc_info_frame.pack(fill="x", pady=(0, 4), after=ra)
        _acc_combo.bind("<<ComboboxSelected>>", _update_acc_info)
        _update_acc_info()  # 초기 표시

        # ── 커뮤니티 선택  (계정과 독립적으로 선택 가능)
        rsite = tk.Frame(body, bg=PALETTE["card"]); rsite.pack(fill="x", pady=4)
        tk.Label(rsite, text="커뮤니티", font=(FONT_FAMILY,9), fg=PALETTE["text2"],
                 bg=PALETTE["card"], width=10, anchor="e").pack(side="left")
        tk.Frame(rsite, bg=PALETTE["card"], width=8).pack(side="left")
        # 사이트 목록을 부모에서 가져온다
        site_names = list(self._sites.keys())
        # "자동(계정 기본사이트)" 옵션 제일 앞에 삽입
        site_choices = ["[자동] 계정 기본 사이트"] + site_names
        self._site_var = tk.StringVar()
        saved_community = self._data.get("community", "")
        if saved_community and saved_community in site_names:
            self._site_var.set(saved_community)
        else:
            self._site_var.set(site_choices[0])
        site_combo = ttk.Combobox(rsite, textvariable=self._site_var,
                                   values=site_choices, width=26, state="readonly")
        site_combo.pack(side="left")
        # 커뮤니티 색상 도트 표시
        self._site_dot = tk.Label(rsite, text="  ●",
                                   font=(FONT_FAMILY,14), fg=PALETTE["muted"],
                                   bg=PALETTE["card"])
        self._site_dot.pack(side="left")
        self._site_name_lbl = tk.Label(rsite, text="",
                                        font=(FONT_FAMILY,8), fg=PALETTE["muted"],
                                        bg=PALETTE["card"])
        self._site_name_lbl.pack(side="left")

        def on_site_change(*_):
            sel = self._site_var.get()
            color = SITE_COLORS.get(sel, PALETTE["muted"])
            self._site_dot.config(fg=color)
            self._site_name_lbl.config(
                text="(계정 사이트 사용)" if sel.startswith("[") else sel,
                fg=color)
            # 마멘토/셀프모아 선택 시 게시판 콤보박스 활성화 + 목록 전환
            # _board_combo 가 아직 생성되지 않았을 수 있으므로 hasattr 으로 방어
            if hasattr(self, "_board_combo") and self._board_combo is not None:
                if sel == "마멘토":
                    _bvals = [""] + list(MAMENTOR_BOARDS.values())
                    self._board_combo.config(state="normal", values=_bvals)
                    self._board_hint_lbl.config(
                        text="마멘토 게시판 선택 · 비워두면 계정 게시판 사용")
                elif sel == "셀프모아":
                    _bvals = [""] + list(SELFMOA_BOARDS.values())
                    self._board_combo.config(state="normal", values=_bvals)
                    self._board_hint_lbl.config(
                        text="셀프모아 게시판 선택 · 비워두면 계정 카테고리 사용")
                else:
                    self._board_combo.config(state="disabled", values=[""])
                    self._board_var.set("")
                    self._board_hint_lbl.config(
                        text="마멘토/셀프모아 선택 시 활성 · 비워두면 계정 게시판 사용")
        site_combo.bind("<<ComboboxSelected>>", on_site_change)

        # ── 게시판 선택 (마멘토/셀프모아 활성, 다른 사이트 선택 시 비활성)
        rb = tk.Frame(body, bg=PALETTE["card"]); rb.pack(fill="x", pady=4)
        tk.Label(rb, text="게시판", font=(FONT_FAMILY,9), fg=PALETTE["text2"],
                 bg=PALETTE["card"], width=10, anchor="e").pack(side="left")
        tk.Frame(rb, bg=PALETTE["card"], width=8).pack(side="left")
        self._board_var = tk.StringVar(value="")
        saved_board = self._data.get("board", "")
        _init_site   = self._data.get("community", "")
        if saved_board:
            # 저장된 bo_table → 한글명 변환 (마멘토/셀프모아 각각)
            if _init_site == "마멘토":
                disp = MAMENTOR_BOARDS.get(saved_board, saved_board)
            elif _init_site == "셀프모아":
                disp = SELFMOA_BOARDS.get(saved_board, saved_board)
            else:
                disp = saved_board
            self._board_var.set(disp)
        # 초기 목록은 사이트에 맞게 설정
        if _init_site == "마멘토":
            _init_board_vals = [""] + list(MAMENTOR_BOARDS.values())
        elif _init_site == "셀프모아":
            _init_board_vals = [""] + list(SELFMOA_BOARDS.values())
        else:
            _init_board_vals = [""]
        self._board_combo = ttk.Combobox(rb, textvariable=self._board_var,
                                          values=_init_board_vals, width=22)
        self._board_combo.pack(side="left")
        self._board_hint_lbl = tk.Label(rb,
            text="마멘토/셀프모아 선택 시 활성 · 비워두면 계정 게시판 사용",
            font=(FONT_FAMILY,8), fg=PALETTE["muted"], bg=PALETTE["card"])
        self._board_hint_lbl.pack(side="left", padx=8)
        # _board_combo 생성 완료 후 on_site_change() 호출 (순서 보장)
        on_site_change()
        # 초기 상태 (on_site_change 가 처리하지만 명시적 보강)
        _active_sites = ("마멘토", "셀프모아")
        self._board_combo.config(state="normal" if _init_site in _active_sites else "disabled")

        # ── 콘텐츠 선택
        rc = tk.Frame(body, bg=PALETTE["card"]); rc.pack(fill="x", pady=4)
        tk.Label(rc, text="콘텐츠", font=(FONT_FAMILY,9), fg=PALETTE["text2"],
                 bg=PALETTE["card"], width=10, anchor="e").pack(side="left")
        tk.Frame(rc, bg=PALETTE["card"], width=8).pack(side="left")
        cont_labels = [c.get("title", f"템플릿{i+1}") for i,c in enumerate(self._contents)]
        self._cont_var = tk.StringVar()
        saved_ci = self._data.get("content_idx", -1)
        if 0 <= saved_ci < len(cont_labels):
            self._cont_var.set(cont_labels[saved_ci])
        _cont_combo = ttk.Combobox(rc, textvariable=self._cont_var,
                     values=cont_labels, width=36, state="readonly")
        _cont_combo.pack(side="left")


        # ══════════════════════════════════════════════════════
        # ── 작업별 스케줄 설정 ─────────────────────────────────
        # ══════════════════════════════════════════════════════
        tk.Frame(body, bg=PALETTE["border"], height=1).pack(fill="x", pady=6)
        sched_lbl_row = tk.Frame(body, bg=PALETTE["card"])
        sched_lbl_row.pack(fill="x", pady=(2,0))
        tk.Label(sched_lbl_row, text="🕐  작업별 스케줄",
                 font=(FONT_FAMILY, 9, "bold"),
                 fg=PALETTE["primary"], bg=PALETTE["card"]).pack(side="left")
        tk.Label(sched_lbl_row,
                 text="  (체크 해제 시 전역 스케줄 따름)",
                 font=(FONT_FAMILY, 8), fg=PALETTE["text2"],
                 bg=PALETTE["card"]).pack(side="left")

        # 개별 스케줄 활성화 여부
        _js = self._data.get("schedule", {})
        _use_ind   = not _js.get("use_global", True) if _js else False
        _sched_ena = _js.get("enabled", False) if _js else False
        self._jsched_use_var = tk.BooleanVar(value=_use_ind)
        self._jsched_ena_var = tk.BooleanVar(value=_sched_ena)

        sched_toggle_row = tk.Frame(body, bg=PALETTE["card"])
        sched_toggle_row.pack(fill="x", pady=2)
        tk.Checkbutton(sched_toggle_row, text="개별 스케줄 활성화",
                       variable=self._jsched_use_var,
                       font=(FONT_FAMILY, 9, "bold"),
                       fg=PALETTE["success"], bg=PALETTE["card"],
                       activebackground=PALETTE["card"],
                       selectcolor=PALETTE["card"]).pack(side="left", padx=2)
        tk.Label(sched_toggle_row,
                 text="  ← 체크 시 저장 즉시 이 작업만 자동 반복 실행",
                 font=(FONT_FAMILY, 8), fg=PALETTE["text2"],
                 bg=PALETTE["card"]).pack(side="left")

        # 스케줄 세부 프레임 (토글)
        sched_detail_frame = tk.Frame(body, bg=PALETTE["card"])
        sched_detail_frame.pack(fill="x")

        # 실행 모드
        sched_mode_row = tk.Frame(sched_detail_frame, bg=PALETTE["card"])
        sched_mode_row.pack(fill="x", pady=3)
        tk.Label(sched_mode_row, text="실행 모드",
                 font=(FONT_FAMILY,9), fg=PALETTE["text2"],
                 bg=PALETTE["card"], width=10, anchor="e").pack(side="left")
        tk.Frame(sched_mode_row, bg=PALETTE["card"], width=8).pack(side="left")
        _jmode_init = _js.get("mode", "interval") if _js else "interval"
        self._jsched_mode_var = tk.StringVar(value=_jmode_init)
        for val, lab in [("interval","반복 간격"), ("times","지정 시각")]:
            tk.Radiobutton(sched_mode_row, text=lab,
                           variable=self._jsched_mode_var, value=val,
                           font=(FONT_FAMILY,9),
                           bg=PALETTE["card"], fg=PALETTE["text"],
                           activebackground=PALETTE["card"],
                           selectcolor=PALETTE["card"]).pack(side="left", padx=6)

        # 반복 간격 행
        sched_interval_row = tk.Frame(sched_detail_frame, bg=PALETTE["card"])
        sched_interval_row.pack(fill="x", pady=2)
        tk.Label(sched_interval_row, text="반복 간격",
                 font=(FONT_FAMILY,9), fg=PALETTE["text2"],
                 bg=PALETTE["card"], width=10, anchor="e").pack(side="left")
        tk.Frame(sched_interval_row, bg=PALETTE["card"], width=8).pack(side="left")
        self._jsched_h_var = tk.IntVar(value=_js.get("interval_hours", 3) if _js else 3)
        tk.Spinbox(sched_interval_row, from_=1, to=72,
                   textvariable=self._jsched_h_var,
                   font=(FONT_FAMILY,9), width=5,
                   bg=PALETTE["bg"]).pack(side="left")
        tk.Label(sched_interval_row, text=" 시간 ±",
                 font=(FONT_FAMILY,9), bg=PALETTE["card"]).pack(side="left", padx=2)
        self._jsched_v_var = tk.IntVar(value=_js.get("interval_variance", 30) if _js else 30)
        tk.Spinbox(sched_interval_row, from_=0, to=120,
                   textvariable=self._jsched_v_var,
                   font=(FONT_FAMILY,9), width=5,
                   bg=PALETTE["bg"]).pack(side="left")
        tk.Label(sched_interval_row, text=" 분",
                 font=(FONT_FAMILY,9), bg=PALETTE["card"]).pack(side="left", padx=2)

        # 지정 시각 행
        sched_times_row = tk.Frame(sched_detail_frame, bg=PALETTE["card"])
        sched_times_row.pack(fill="x", pady=2)
        tk.Label(sched_times_row, text="지정 시각",
                 font=(FONT_FAMILY,9), fg=PALETTE["text2"],
                 bg=PALETTE["card"], width=10, anchor="e").pack(side="left")
        tk.Frame(sched_times_row, bg=PALETTE["card"], width=8).pack(side="left")
        _times_init = ",".join(_js.get("times", ["09:00"])) if _js else "09:00"
        self._jsched_times_var = tk.StringVar(value=_times_init)
        tk.Entry(sched_times_row, textvariable=self._jsched_times_var,
                 font=(FONT_FAMILY,9), width=22,
                 bg=PALETTE["bg"], relief="flat",
                 highlightbackground=PALETTE["border"],
                 highlightthickness=1).pack(side="left")
        tk.Label(sched_times_row, text=" HH:MM (쉼표 구분)",
                 font=(FONT_FAMILY,8), fg=PALETTE["text2"],
                 bg=PALETTE["card"]).pack(side="left", padx=4)

        # 요일 선택 행
        sched_days_row = tk.Frame(sched_detail_frame, bg=PALETTE["card"])
        sched_days_row.pack(fill="x", pady=2)
        tk.Label(sched_days_row, text="실행 요일",
                 font=(FONT_FAMILY,9), fg=PALETTE["text2"],
                 bg=PALETTE["card"], width=10, anchor="e").pack(side="left")
        tk.Frame(sched_days_row, bg=PALETTE["card"], width=8).pack(side="left")
        _days_init = _js.get("days", [0,1,2,3,4]) if _js else [0,1,2,3,4]
        self._jsched_day_vars = []
        for di, dlabel in enumerate(["월","화","수","목","금","토","일"]):
            dv = tk.BooleanVar(value=di in _days_init)
            self._jsched_day_vars.append(dv)
            tk.Checkbutton(sched_days_row, text=dlabel, variable=dv,
                           font=(FONT_FAMILY,9),
                           bg=PALETTE["card"], fg=PALETTE["text"],
                           activebackground=PALETTE["card"],
                           selectcolor=PALETTE["card"]).pack(side="left", padx=2)

        def _toggle_sched_detail(*_):
            if self._jsched_use_var.get():
                sched_detail_frame.pack(fill="x")
            else:
                sched_detail_frame.pack_forget()
        self._jsched_use_var.trace_add("write", _toggle_sched_detail)
        _toggle_sched_detail()  # 초기 상태 반영

        # ══════════════════════════════════════════════════════
        # ── 작업별 딜레이 설정 ─────────────────────────────────
        # ══════════════════════════════════════════════════════
        tk.Frame(body, bg=PALETTE["border"], height=1).pack(fill="x", pady=6)
        delay_lbl_row = tk.Frame(body, bg=PALETTE["card"])
        delay_lbl_row.pack(fill="x", pady=(2,0))
        tk.Label(delay_lbl_row, text="⏱  작업별 딜레이",
                 font=(FONT_FAMILY, 9, "bold"),
                 fg=PALETTE["primary"], bg=PALETTE["card"]).pack(side="left")
        tk.Label(delay_lbl_row,
                 text="  (비워두면 전역 설정 사용)",
                 font=(FONT_FAMILY, 8), fg=PALETTE["text2"],
                 bg=PALETTE["card"]).pack(side="left")

        # 앞 대기 (pre_delay)
        pre_row = tk.Frame(body, bg=PALETTE["card"])
        pre_row.pack(fill="x", pady=3)
        tk.Label(pre_row, text="앞 대기",
                 font=(FONT_FAMILY,9), fg=PALETTE["text2"],
                 bg=PALETTE["card"], width=10, anchor="e").pack(side="left")
        tk.Frame(pre_row, bg=PALETTE["card"], width=8).pack(side="left")
        pre_min_init = str(self._data.get("pre_delay_min","")) if self._data.get("pre_delay_min") is not None else ""
        pre_max_init = str(self._data.get("pre_delay_max","")) if self._data.get("pre_delay_max") is not None else ""
        self._pre_delay_min_var = tk.StringVar(value=pre_min_init)
        self._pre_delay_max_var = tk.StringVar(value=pre_max_init)
        tk.Entry(pre_row, textvariable=self._pre_delay_min_var,
                 font=(FONT_FAMILY,9), width=6,
                 bg=PALETTE["bg"], relief="flat",
                 highlightbackground=PALETTE["border"],
                 highlightthickness=1).pack(side="left")
        tk.Label(pre_row, text=" ~ ", font=(FONT_FAMILY,9),
                 bg=PALETTE["card"]).pack(side="left")
        tk.Entry(pre_row, textvariable=self._pre_delay_max_var,
                 font=(FONT_FAMILY,9), width=6,
                 bg=PALETTE["bg"], relief="flat",
                 highlightbackground=PALETTE["border"],
                 highlightthickness=1).pack(side="left")
        tk.Label(pre_row, text=" 초  (실행 시작 전 대기)",
                 font=(FONT_FAMILY,8), fg=PALETTE["text2"],
                 bg=PALETTE["card"]).pack(side="left", padx=4)

        # 뒤 대기 (post_delay / 기존 delay_min/max)
        delay_row = tk.Frame(body, bg=PALETTE["card"])
        delay_row.pack(fill="x", pady=3)
        tk.Label(delay_row, text="뒤 대기",
                 font=(FONT_FAMILY,9), fg=PALETTE["text2"],
                 bg=PALETTE["card"], width=10, anchor="e").pack(side="left")
        tk.Frame(delay_row, bg=PALETTE["card"], width=8).pack(side="left")

        # None이면 빈칸으로 표시
        d_min_init = str(self._data.get("delay_min", "")) if self._data.get("delay_min") is not None else ""
        d_max_init = str(self._data.get("delay_max", "")) if self._data.get("delay_max") is not None else ""
        self._delay_min_var = tk.StringVar(value=d_min_init)
        self._delay_max_var = tk.StringVar(value=d_max_init)

        tk.Entry(delay_row, textvariable=self._delay_min_var,
                 font=(FONT_FAMILY,9), width=6,
                 bg=PALETTE["bg"], relief="flat",
                 highlightbackground=PALETTE["border"],
                 highlightthickness=1).pack(side="left")
        tk.Label(delay_row, text=" ~ ", font=(FONT_FAMILY,9),
                 bg=PALETTE["card"]).pack(side="left")
        tk.Entry(delay_row, textvariable=self._delay_max_var,
                 font=(FONT_FAMILY,9), width=6,
                 bg=PALETTE["bg"], relief="flat",
                 highlightbackground=PALETTE["border"],
                 highlightthickness=1).pack(side="left")
        tk.Label(delay_row, text=" 초  (게시 완료 후 대기)",
                 font=(FONT_FAMILY,8), fg=PALETTE["text2"],
                 bg=PALETTE["card"]).pack(side="left", padx=4)

        # ── 저장 / 취소
        tk.Frame(body, bg=PALETTE["border"], height=1).pack(fill="x", pady=8)
        save_row = tk.Frame(body, bg=PALETTE["card"]); save_row.pack(fill="x")

        def save():
            name = self._name_var.get().strip()
            if not name:
                messagebox.showwarning("경고","작업명을 입력하세요.", parent=self); return
            if not self._acc_var.get():
                messagebox.showwarning("경고","계정을 선택하세요.", parent=self); return
            if not self._cont_var.get():
                messagebox.showwarning("경고","콘텐츠를 선택하세요.", parent=self); return
            acc_sel  = self._acc_var.get()
            cont_sel = self._cont_var.get()
            ai = acc_labels.index(acc_sel)  if acc_sel  in acc_labels  else -1
            ci = cont_labels.index(cont_sel) if cont_sel in cont_labels else -1
            site_sel = self._site_var.get()
            community = "" if site_sel.startswith("[") else site_sel
            # 게시판: 한글명 → bo_table 역변환 저장 (마멘토/셀프모아 각각)
            board_disp = self._board_var.get().strip()
            _comm_sel  = "" if site_sel.startswith("[") else site_sel
            if _comm_sel == "마멘토":
                board_val = MAMENTOR_BOARDS_R.get(board_disp, board_disp)
            elif _comm_sel == "셀프모아":
                board_val = SELFMOA_BOARDS_R.get(board_disp, board_disp)
            else:
                board_val = board_disp
            # 딜레이 파싱 (빈칸이면 None → 전역 사용)
            try:
                d_min = int(self._delay_min_var.get().strip()) if self._delay_min_var.get().strip() else None
                d_max = int(self._delay_max_var.get().strip()) if self._delay_max_var.get().strip() else None
            except ValueError:
                d_min = d_max = None
            try:
                pre_min = int(self._pre_delay_min_var.get().strip()) if self._pre_delay_min_var.get().strip() else None
                pre_max = int(self._pre_delay_max_var.get().strip()) if self._pre_delay_max_var.get().strip() else None
            except ValueError:
                pre_min = pre_max = None
            # 개별 스케줄 저장
            if self._jsched_use_var.get():
                days_sel = [i for i,v in enumerate(self._jsched_day_vars) if v.get()]
                times_raw = self._jsched_times_var.get()
                times_list = [t.strip() for t in times_raw.split(",") if t.strip()]
                job_sched = {
                    "use_global":        False,
                    "enabled":           True,   # 체크 = 활성화
                    "mode":              self._jsched_mode_var.get(),
                    "interval_hours":    self._jsched_h_var.get(),
                    "interval_variance": self._jsched_v_var.get(),
                    "times":             times_list,
                    "days":              days_sel,
                }
            else:
                job_sched = {"use_global": True, "enabled": False}
            self.result = {
                "name":          name,
                "account_idx":   ai,
                "account_id":    self._accounts[ai].get("id","") if ai>=0 else "",
                "community":     community,
                "board":         board_val,
                "content_idx":   ci,
                "schedule":      job_sched,
                "pre_delay_min": pre_min,
                "pre_delay_max": pre_max,
                "delay_min":     d_min,
                "delay_max":     d_max,
                "enabled":       self._data.get("enabled", True),
                "memo":          self._data.get("memo",""),
            }
            self.destroy()

        tk.Button(save_row, text="저장",
                  font=(FONT_FAMILY,10,"bold"),
                  bg=PALETTE["primary"], fg="#fff",
                  relief="flat", padx=20, pady=6,
                  cursor="hand2", command=save).pack(side="right", padx=4)
        tk.Button(save_row, text="취소",
                  font=(FONT_FAMILY,10),
                  bg="#E2E8F0", fg=PALETTE["text"],
                  relief="flat", padx=20, pady=6,
                  cursor="hand2", command=self.destroy).pack(side="right", padx=4)


# ═══════════════════════════════════════════════════════════════════
#  진입점
# ═══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()
