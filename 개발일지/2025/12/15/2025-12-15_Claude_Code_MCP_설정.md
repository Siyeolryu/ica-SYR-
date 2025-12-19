# Claude Code MCP 설정 및 테스트

## 작성시각
2025년 12월 15일

## 해결하고자 한 문제
- 터미널에서 `/claude` 명령어를 사용할 수 없는 문제
- Claude Code MCP 설치 및 설정 확인
- MCP 서버 설정 및 연결 테스트

## 해결된 것

### 1. Claude Code 설치 확인
- **버전**: 2.0.69 (Claude Code)
- 시스템에 정상적으로 설치되어 있음을 확인
- 별칭 자동 로드 기능 활성화됨

### 2. 사용 가능한 별칭 확인
PowerShell에서 다음 별칭들이 사용 가능함을 확인:
- `c` / `cc` - claude 실행
- `cn` - claude --new (새 세션)
- `ch` - claude . (현재 폴더)
- `cv` - claude --version (버전 확인)

### 3. MCP 서버 설정
- **sequential-thinking** MCP 서버 추가 완료
- 명령어: `npx -y @modelcontextprotocol/server-sequential-thinking`
- 연결 상태: ✓ Connected
- 설정 파일: `C:\Users\tlduf\.claude.json`

### 4. 기능 테스트
- Claude Code 정상 작동 확인
- 간단한 질의 응답 테스트 성공
- MCP 서버 연결 상태 정상

## 해결되지 않은 것

### 1. `/claude` 명령어 사용 불가
- Windows PowerShell에서 `/`로 시작하는 명령어는 표준이 아님
- `/`는 경로 구분자나 명령줄 플래그로 사용됨
- PowerShell 함수로 만들려는 시도도 실패

## 향후 개발을 위한 컨텍스트

### 권장 사용 방법
1. **기본 사용**: `c "질문 또는 명령"`
2. **현재 폴더**: `ch` (현재 프로젝트 컨텍스트로 실행)
3. **새 세션**: `cn`
4. **버전 확인**: `cv`

### MCP 서버 관리
```powershell
# MCP 서버 목록 확인
c mcp list

# MCP 서버 추가
c mcp add <server-name> -s user -- <command>

# 설정 파일 위치
C:\Users\tlduf\.claude.json
```

### 추가 MCP 서버 설치 옵션
필요시 다음과 같은 MCP 서버들을 추가할 수 있음:
- `@upstash/context7-mcp` - 컨텍스트 관리
- `@modelcontextprotocol/server-filesystem` - 파일시스템 접근
- `@modelcontextprotocol/server-git` - Git 통합

### 기술적 참고사항
- Claude Code는 Node.js 기반으로 실행됨
- MCP 서버는 npx를 통해 on-demand로 실행됨
- 사용자 레벨 설정(`-s user`)으로 구성됨
- PowerShell 별칭은 자동으로 로드됨

### Windows PowerShell 명령어 제약
- `/`로 시작하는 명령어는 PowerShell에서 비표준
- 대신 짧은 별칭 사용 권장 (`c`, `cc`)
- Unix 스타일 명령어가 아닌 Windows 스타일 사용 필요

