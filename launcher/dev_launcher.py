# -*- coding: utf-8 -*-
"""
메신저 올인원 - 개발용 런처
GitHub에서 최신 py 파일을 받아서 바로 실행합니다. (즉시 반영)
자기 자신(dev_launcher.py)도 자동 업데이트합니다.
"""

import os
import sys
import json
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import urllib.request
import urllib.error

# ── 설정 ──────────────────────────────────────────────────────────────────────
GITHUB_USER   = "lcm67088-tech"
GITHUB_REPO   = "Program"
GITHUB_BRANCH = "main"

PY_FILE_NAME      = "messenger_allInOne_v1.60.py"
PY_RAW_URL        = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/{PY_FILE_NAME}"

DEV_LAUNCHER_URL  = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/launcher/dev_launcher.py"

LAUNCHER_VERSION  = "1.0.2"
LAUNCHER_VER_URL  = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/launcher/dev_launcher_version.json"

BASE_DIR          = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
PY_SAVE_PATH      = os.path.join(BASE_DIR, PY_FILE_NAME)
SELF_PY_PATH      = os.path.join(BASE_DIR, "dev_launcher.py")
# ─────────────────────────────────────────────────────────────────────────────


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "DevLauncher"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8")


def fetch_binary(url: str, dest: str, progress_callback=None):
    req = urllib.request.Request(url, headers={"User-Agent": "DevLauncher"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        total = int(resp.headers.get("Content-Length", 0))
        downloaded = 0
        content = b""
        while True:
            chunk = resp.read(65536)
            if not chunk:
                break
            content += chunk
            downloaded += len(chunk)
            if progress_callback:
                progress_callback(downloaded, total)
    with open(dest, "wb") as f:
        f.write(content)


def get_python_path() -> str:
    for cmd in ["python", "python3"]:
        try:
            result = subprocess.run(
                [cmd, "--version"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                return cmd
        except Exception:
            continue
    return ""


class DevLauncherApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("메신저 올인원 - 개발용 런처")
        self.root.geometry("480x280")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 480) // 2
        y = (self.root.winfo_screenheight() - 280) // 2
        self.root.geometry(f"480x280+{x}+{y}")

        self._build_ui()
        self.root.after(300, self._start)

    def _build_ui(self):
        bg     = "#1e1e2e"
        fg     = "#cdd6f4"
        accent = "#a6e3a1"

        tk.Label(
            self.root, text="메신저 올인원", font=("맑은 고딕", 18, "bold"),
            bg=bg, fg=accent
        ).pack(pady=(24, 2))

        tk.Label(
            self.root, text="개발용 런처 (DEV)",
            font=("맑은 고딕", 10, "bold"), bg=bg, fg="#f38ba8"
        ).pack()

        tk.Label(
            self.root, text=f"v{LAUNCHER_VERSION}  |  항상 최신 py 파일로 실행",
            font=("맑은 고딕", 8), bg=bg, fg="#6c7086"
        ).pack(pady=(2, 0))

        self.status_var = tk.StringVar(value="준비 중...")
        tk.Label(
            self.root, textvariable=self.status_var,
            font=("맑은 고딕", 10), bg=bg, fg=fg
        ).pack(pady=(18, 6))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "dev.Horizontal.TProgressbar",
            troughcolor="#313244", background=accent,
            thickness=14
        )
        self.progress = ttk.Progressbar(
            self.root, style="dev.Horizontal.TProgressbar",
            orient="horizontal", length=380, mode="indeterminate"
        )
        self.progress.pack(pady=4)

        self.info_var = tk.StringVar(value="")
        tk.Label(
            self.root, textvariable=self.info_var,
            font=("맑은 고딕", 9), bg=bg, fg="#6c7086"
        ).pack(pady=(8, 0))

    def set_status(self, msg: str):
        self.status_var.set(msg)
        self.root.update_idletasks()

    def set_info(self, msg: str):
        self.info_var.set(msg)
        self.root.update_idletasks()

    def set_progress_determinate(self, value: float):
        self.progress.stop()
        self.progress.config(mode="determinate")
        self.progress["value"] = value
        self.root.update_idletasks()

    def set_progress_indeterminate(self):
        self.progress.config(mode="indeterminate")
        self.progress.start(12)
        self.root.update_idletasks()

    def _start(self):
        self.set_progress_indeterminate()
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        # Python 확인
        self.root.after(0, self.set_status, "Python 확인 중...")
        python_path = get_python_path()
        if not python_path:
            self.root.after(0, messagebox.showerror,
                "오류", "Python이 설치되어 있지 않습니다.\nhttps://python.org 에서 설치해주세요.")
            self.root.after(0, self.root.destroy)
            return

        try:
            # 1. 런처 자체 업데이트 체크
            self.root.after(0, self.set_status, "런처 업데이트 확인 중...")
            try:
                ver_json = json.loads(fetch_text(LAUNCHER_VER_URL))
                remote_ver = ver_json.get("version", LAUNCHER_VERSION)
                if remote_ver != LAUNCHER_VERSION:
                    self.root.after(0, self.set_status, f"런처 업데이트 중... v{remote_ver}")
                    new_code = fetch_text(DEV_LAUNCHER_URL)
                    with open(SELF_PY_PATH, "w", encoding="utf-8") as f:
                        f.write(new_code)
                    # 업데이트된 런처로 재시작
                    self.root.after(0, self.set_status, "런처 업데이트 완료! 재시작 중...")
                    self.root.after(500, lambda: self._restart(python_path))
                    return
            except Exception:
                pass  # 런처 업데이트 실패해도 그냥 진행

            # 2. 최신 py 파일 다운로드
            self.root.after(0, self.set_status, "최신 파일 받는 중...")

            def on_progress(downloaded, total):
                if total > 0:
                    pct = downloaded / total * 100
                    self.root.after(0, self.set_progress_determinate, pct)
                kb = downloaded / 1024
                self.root.after(0, self.set_info, f"{kb:.0f} KB 다운로드 중...")

            fetch_binary(PY_RAW_URL, PY_SAVE_PATH, on_progress)
            self.root.after(0, self.set_status, "완료! 실행 중...")
            self.root.after(0, self.set_info, PY_FILE_NAME)

        except Exception as e:
            if os.path.exists(PY_SAVE_PATH):
                self.root.after(0, self.set_status, "네트워크 오류 - 로컬 파일로 실행 중...")
                self.root.after(0, self.set_info, f"오류: {e}")
            else:
                self.root.after(0, messagebox.showerror,
                    "오류", f"네트워크 오류이고 로컬 파일도 없습니다.\n\n{e}")
                self.root.after(0, self.root.destroy)
                return

        self.root.after(1000, lambda: self._launch(python_path))

    def _restart(self, python_path):
        """업데이트된 런처로 재시작"""
        try:
            subprocess.Popen(
                f'"{python_path}" "{SELF_PY_PATH}"',
                cwd=BASE_DIR, shell=True
            )
        except Exception:
            pass
        self.root.destroy()

    def _launch(self, python_path):
        try:
            subprocess.Popen(
                f'"{python_path}" "{PY_SAVE_PATH}"',
                cwd=BASE_DIR, shell=True
            )
        except Exception as e:
            messagebox.showerror("실행 오류", f"실행할 수 없습니다.\n{e}")
        finally:
            self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = DevLauncherApp()
    app.run()
