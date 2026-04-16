# -*- coding: utf-8 -*-
"""
메신저 올인원 - 런처
GitHub Releases에서 최신 버전을 확인하고 자동으로 다운로드 후 실행합니다.
"""

import os
import sys
import json
import shutil
import hashlib
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import urllib.request
import urllib.error

# ── 설정 ──────────────────────────────────────────────────────────────────────
GITHUB_USER     = "lcm67088-tech"
GITHUB_REPO     = "Program"
VERSION_URL     = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/version.json"
LAUNCHER_VERSION = "1.0.0"

# 실행 파일 저장 경로 (런처와 같은 폴더)
BASE_DIR     = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
APP_EXE_NAME = "메신저올인원.exe"
APP_EXE_PATH = os.path.join(BASE_DIR, APP_EXE_NAME)
VERSION_FILE = os.path.join(BASE_DIR, "local_version.json")
# ─────────────────────────────────────────────────────────────────────────────


def get_local_version() -> str:
    """로컬에 저장된 버전 정보를 읽어옵니다."""
    try:
        if os.path.exists(VERSION_FILE):
            with open(VERSION_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("version", "0.0.0")
    except Exception:
        pass
    return "0.0.0"


def save_local_version(version: str):
    """로컬 버전 정보를 저장합니다."""
    with open(VERSION_FILE, "w", encoding="utf-8") as f:
        json.dump({"version": version}, f, ensure_ascii=False)


def fetch_remote_version() -> dict:
    """GitHub에서 최신 버전 정보를 가져옵니다."""
    req = urllib.request.Request(
        VERSION_URL,
        headers={"User-Agent": "MessengerAllInOne-Launcher"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def download_file(url: str, dest: str, progress_callback=None):
    """파일을 다운로드합니다. progress_callback(downloaded, total) 형태."""
    req = urllib.request.Request(url, headers={"User-Agent": "MessengerAllInOne-Launcher"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        total = int(resp.headers.get("Content-Length", 0))
        downloaded = 0
        chunk_size = 65536  # 64KB
        tmp_path = dest + ".tmp"
        with open(tmp_path, "wb") as f:
            while True:
                chunk = resp.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
                downloaded += len(chunk)
                if progress_callback:
                    progress_callback(downloaded, total)
    # 다운로드 완료 후 교체
    if os.path.exists(dest):
        os.remove(dest)
    os.rename(tmp_path, dest)


def verify_md5(filepath: str, expected_md5: str) -> bool:
    """MD5 체크섬을 검증합니다."""
    if not expected_md5:
        return True
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest().lower() == expected_md5.lower()


class LauncherApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("메신저 올인원 런처")
        self.root.geometry("480x260")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        # 화면 중앙 배치
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 480) // 2
        y = (self.root.winfo_screenheight() - 260) // 2
        self.root.geometry(f"480x260+{x}+{y}")

        self._build_ui()
        self.root.after(300, self._start_check)

    def _build_ui(self):
        bg = "#1e1e2e"
        fg = "#cdd6f4"
        accent = "#89b4fa"

        # 타이틀
        tk.Label(
            self.root, text="메신저 올인원", font=("맑은 고딕", 18, "bold"),
            bg=bg, fg=accent
        ).pack(pady=(28, 4))

        tk.Label(
            self.root, text=f"런처 v{LAUNCHER_VERSION}",
            font=("맑은 고딕", 9), bg=bg, fg="#6c7086"
        ).pack()

        # 상태 메시지
        self.status_var = tk.StringVar(value="버전 확인 중...")
        tk.Label(
            self.root, textvariable=self.status_var,
            font=("맑은 고딕", 10), bg=bg, fg=fg
        ).pack(pady=(20, 6))

        # 진행 바
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "custom.Horizontal.TProgressbar",
            troughcolor="#313244", background=accent,
            thickness=14
        )
        self.progress = ttk.Progressbar(
            self.root, style="custom.Horizontal.TProgressbar",
            orient="horizontal", length=380, mode="indeterminate"
        )
        self.progress.pack(pady=4)

        # 버전 정보
        self.version_var = tk.StringVar(value="")
        tk.Label(
            self.root, textvariable=self.version_var,
            font=("맑은 고딕", 9), bg=bg, fg="#6c7086"
        ).pack(pady=(8, 0))

    def set_status(self, msg: str):
        self.status_var.set(msg)
        self.root.update_idletasks()

    def set_version_info(self, local: str, remote: str = ""):
        if remote:
            self.version_var.set(f"로컬: v{local}  →  최신: v{remote}")
        else:
            self.version_var.set(f"현재 버전: v{local}")
        self.root.update_idletasks()

    def set_progress_determinate(self, value: float):
        """0~100 사이 값으로 진행 바 설정"""
        self.progress.stop()
        self.progress.config(mode="determinate")
        self.progress["value"] = value
        self.root.update_idletasks()

    def set_progress_indeterminate(self):
        self.progress.config(mode="indeterminate")
        self.progress.start(12)
        self.root.update_idletasks()

    def _start_check(self):
        self.set_progress_indeterminate()
        threading.Thread(target=self._check_and_launch, daemon=True).start()

    def _check_and_launch(self):
        local_ver = get_local_version()

        # 앱이 없으면 무조건 다운로드
        if not os.path.exists(APP_EXE_PATH):
            local_ver = "0.0.0"

        try:
            self.set_status("GitHub에서 버전 확인 중...")
            remote_info = fetch_remote_version()
            remote_ver  = remote_info.get("version", "0.0.0")
            download_url = remote_info.get("download_url", "")
            expected_md5 = remote_info.get("md5", "")

            self.set_version_info(local_ver, remote_ver)

            need_update = (
                local_ver != remote_ver or
                not os.path.exists(APP_EXE_PATH)
            )

            if need_update:
                self.set_status(f"새 버전 발견! v{remote_ver} 다운로드 중...")

                def on_progress(downloaded, total):
                    if total > 0:
                        pct = downloaded / total * 100
                        self.root.after(0, self.set_progress_determinate, pct)
                        mb_d = downloaded / 1024 / 1024
                        mb_t = total / 1024 / 1024
                        self.root.after(0, self.set_status,
                            f"다운로드 중... {mb_d:.1f} / {mb_t:.1f} MB")

                download_file(download_url, APP_EXE_PATH, on_progress)

                # MD5 검증
                if expected_md5 and not verify_md5(APP_EXE_PATH, expected_md5):
                    self.root.after(0, messagebox.showerror,
                        "오류", "다운로드된 파일이 손상되었습니다.\n다시 시도해주세요.")
                    self.root.after(0, self.root.destroy)
                    return

                save_local_version(remote_ver)
                self.root.after(0, self.set_status, f"v{remote_ver} 업데이트 완료! 실행 중...")
            else:
                self.root.after(0, self.set_status, f"최신 버전입니다 (v{local_ver}). 실행 중...")

        except (urllib.error.URLError, urllib.error.HTTPError, Exception) as e:
            # 네트워크 오류 시 로컬 버전으로 실행
            if os.path.exists(APP_EXE_PATH):
                self.root.after(0, self.set_status,
                    f"네트워크 오류 - 로컬 버전(v{local_ver}) 실행 중...")
            else:
                self.root.after(0, messagebox.showerror,
                    "오류",
                    f"네트워크 연결 실패 및 로컬 파일 없음.\n\n{e}\n\n인터넷 연결 후 다시 시도해주세요.")
                self.root.after(0, self.root.destroy)
                return

        # 1초 뒤 실행
        self.root.after(1000, self._launch_app)

    def _launch_app(self):
        try:
            subprocess.Popen([APP_EXE_PATH], cwd=BASE_DIR)
        except Exception as e:
            messagebox.showerror("실행 오류", f"프로그램을 실행할 수 없습니다.\n{e}")
        finally:
            self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = LauncherApp()
    app.run()
