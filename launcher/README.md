# 메신저 올인원 런처

## 사용 방법

### 사용자 입장
1. `메신저올인원_런처.exe` 다운로드
2. 실행하면 자동으로 최신 버전 확인 및 다운로드
3. 이후 자동으로 `메신저올인원.exe` 실행

### 개발자 입장 (업데이트 배포 방법)

#### 1. 새 버전 exe 빌드 후 GitHub Releases에 업로드
```
GitHub → Releases → Create new release
태그: v1.61
파일: 메신저올인원.exe 첨부
```

#### 2. version.json 업데이트 (루트 폴더)
```json
{
  "version": "1.61",
  "download_url": "https://github.com/lcm67088-tech/Program/releases/download/v1.61/메신저올인원.exe",
  "md5": "",
  "release_notes": "v1.61 - 변경 내용"
}
```

#### 3. GitHub에 커밋 & 푸시
```bash
git add version.json
git commit -m "v1.61 릴리즈"
git push
```

→ 다음번 런처 실행 시 자동으로 새 버전 다운로드!

---

## 런처 빌드 방법

```bash
# build_launcher.bat 실행
# dist/메신저올인원_런처.exe 생성됨
```

## 파일 구조
```
Program/
├── version.json              ← 현재 최신 버전 정보 (항상 업데이트)
└── launcher/
    ├── launcher.py           ← 런처 소스코드
    ├── launcher.spec         ← PyInstaller 빌드 설정
    ├── build_launcher.bat    ← 빌드 실행 스크립트
    └── dist/
        └── 메신저올인원_런처.exe  ← 빌드된 런처 (사용자에게 배포)
```
