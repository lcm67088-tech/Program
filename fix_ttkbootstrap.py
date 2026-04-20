"""
ttkbootstrap Python 3.14 호환 패치 스크립트
=============================================
실행 방법:
    python fix_ttkbootstrap.py

문제: Python 3.14 + ttkbootstrap 에서 Combobox 생성 시
     "Duplicate element Combobox.downarrow" TclError 발생

원인: ttkbootstrap/style.py 의 element_create() 호출 시
     이미 존재하는 element를 중복 생성하려 할 때 오류 발생
     (Python 3.14의 Tk 버전이 더 엄격하게 체크함)

패치: element_create() 호출부를 try/except TclError 로 감싸서
      중복 오류를 무시하도록 수정
"""

import sys
import os
import re
import shutil
from pathlib import Path

def find_ttkbootstrap_style():
    """ttkbootstrap style.py 경로 찾기"""
    for path in sys.path:
        candidate = Path(path) / "ttkbootstrap" / "style.py"
        if candidate.exists():
            return candidate

    # site-packages에서 직접 검색
    import site
    for sp in site.getsitepackages():
        candidate = Path(sp) / "ttkbootstrap" / "style.py"
        if candidate.exists():
            return candidate

    return None


def patch_style(style_path: Path):
    print(f"[INFO] 패치 대상: {style_path}")

    # 백업 생성
    backup_path = style_path.with_suffix(".py.bak")
    if not backup_path.exists():
        shutil.copy2(style_path, backup_path)
        print(f"[INFO] 백업 생성: {backup_path}")
    else:
        print(f"[INFO] 백업 이미 존재: {backup_path}")

    content = style_path.read_text(encoding="utf-8")

    # 이미 패치됐는지 확인
    if "# [PATCHED-3.14]" in content:
        print("[OK] 이미 패치가 적용되어 있습니다.")
        return True

    # 패치 대상 패턴: self.style.element_create( 로 시작하는 호출 블록
    # try/except TclError 로 감싸기
    old_pattern = r'(\s+)(self\.style\.element_create\()'
    
    # 모든 element_create 호출을 try/except로 감싸는 방식으로 패치
    # 단순하고 확실한 방법: element_create 메서드 자체를 monkey-patch
    
    monkey_patch = '''
# [PATCHED-3.14] Python 3.14 Tk 중복 element 오류 방지 패치
def _safe_element_create(self, elementname, etype, *args, **kw):
    try:
        self.tk.call(self._name, "element", "create", elementname, etype,
                     *args, *kw)
    except Exception as e:
        if "Duplicate element" in str(e):
            pass  # 이미 존재하는 element 무시
        else:
            raise

import tkinter.ttk as _ttk_mod
_ttk_mod.Style.element_create = _safe_element_create
# [/PATCHED-3.14]

'''

    # 파일 맨 앞의 import 블록 이후에 삽입
    # "import tkinter" 또는 첫 번째 class 정의 전에 삽입
    insert_after = "from tkinter import ttk"
    
    if insert_after in content:
        content = content.replace(
            insert_after,
            insert_after + "\n" + monkey_patch,
            1  # 첫 번째 발생만 교체
        )
        style_path.write_text(content, encoding="utf-8")
        print("[OK] 패치 적용 완료!")
        return True
    
    # 대안: 파일 시작 부분에 추가
    # import 구문들 이후 첫 번째 빈 줄 찾기
    lines = content.splitlines(keepends=True)
    insert_idx = 0
    for i, line in enumerate(lines):
        if line.startswith("import ") or line.startswith("from "):
            insert_idx = i + 1
    
    if insert_idx > 0:
        lines.insert(insert_idx, monkey_patch)
        style_path.write_text("".join(lines), encoding="utf-8")
        print("[OK] 패치 적용 완료! (대안 방법)")
        return True

    print("[오류] 패치 삽입 위치를 찾지 못했습니다.")
    return False


def main():
    print("=" * 50)
    print(" ttkbootstrap Python 3.14 호환 패치")
    print("=" * 50)
    print()

    style_path = find_ttkbootstrap_style()
    if not style_path:
        print("[오류] ttkbootstrap이 설치되어 있지 않습니다.")
        print("       먼저 install.bat 을 실행하세요.")
        input("\n아무 키나 누르면 종료...")
        sys.exit(1)

    success = patch_style(style_path)

    print()
    if success:
        print("패치 완료! 이제 프로그램을 실행하세요:")
        print("  python messenger_allInOne_v1.61.py")
    else:
        print("패치 실패. 개발자에게 문의하세요.")

    input("\n아무 키나 누르면 종료...")


if __name__ == "__main__":
    main()
