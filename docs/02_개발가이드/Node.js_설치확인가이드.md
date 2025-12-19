# Node.js 설치 확인 가이드

## Node.js 설치 확인

Node.js가 설치되어 있는지 확인하려면 다음 명령어를 실행하세요:

```bash
node --version
npm --version
```

## 설치되어 있지 않은 경우

### Windows

1. [Node.js 공식 웹사이트](https://nodejs.org/)에서 LTS 버전 다운로드
2. 설치 프로그램 실행 및 설치
3. **중요**: 설치 후 터미널을 완전히 종료하고 다시 시작해야 환경 변수가 적용됩니다.

### 설치 후 확인

터미널을 다시 시작한 후:
```bash
node --version
npm --version
```

## 환경 변수 문제 해결

만약 설치했는데도 인식되지 않는다면:

1. **시스템 환경 변수 확인**
   - Windows 검색에서 "환경 변수" 검색
   - 시스템 변수에서 `Path` 확인
   - Node.js 설치 경로가 포함되어 있는지 확인 (예: `C:\Program Files\nodejs\`)

2. **터미널 재시작**
   - PowerShell 또는 명령 프롬프트를 완전히 종료하고 다시 시작

3. **설치 경로 확인**
   - 일반적으로 `C:\Program Files\nodejs\` 또는 `C:\Users\[사용자명]\AppData\Roaming\npm`에 설치됩니다.

## 프로젝트 실행

Node.js가 정상적으로 인식되면:

```bash
# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

브라우저에서 [http://localhost:3000](http://localhost:3000)을 열어 확인하세요.
