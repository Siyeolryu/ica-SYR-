# MCP 서버 설정 가이드

"당신이 잠든 사이" 프로젝트를 MCP(Model Context Protocol)를 통해 Claude Desktop이나 다른 AI 도구와 연동하는 방법을 설명합니다.

## 📚 목차
1. [MCP란?](#mcp란)
2. [설치된 MCP 서버](#설치된-mcp-서버)
3. [Claude Desktop 연동](#claude-desktop-연동)
4. [사용 방법](#사용-방법)
5. [문제 해결](#문제-해결)

---

## MCP란?

MCP(Model Context Protocol)는 AI 애플리케이션이 외부 데이터 소스와 도구를 안전하게 연결할 수 있게 하는 개방형 프로토콜입니다.

이 프로젝트에서는 MCP를 통해:
- Claude Desktop에서 직접 미국 주식 화제 종목 조회
- AI 브리핑 자동 생성
- 종목 뉴스 수집 및 분석

---

## 설치된 MCP 서버

### 1. **Stocks Server** (`stocks_server.py`)
화제 종목 조회 기능을 제공하는 MCP 서버

**제공 도구:**
- `get_trending_stocks` - 화제 종목 목록 조회
- `get_top_trending_stock` - TOP 1 화제 종목 조회
- `get_stock_info` - 특정 종목 상세 정보

**사용 예시:**
```
Claude에게: "오늘 미국 주식 화제 종목 TOP 5를 알려줘"
```

### 2. **Briefing Server** (`briefing_server.py`)
AI 브리핑 생성 기능을 제공하는 MCP 서버

**제공 도구:**
- `generate_daily_briefing` - 완전 자동화 브리핑 생성
- `analyze_stock_trending_reason` - 종목 화제 원인 분석
- `get_stock_news` - 종목 관련 뉴스 수집

**사용 예시:**
```
Claude에게: "오늘의 주식 브리핑을 생성해줘"
Claude에게: "AAPL이 왜 화제인지 분석해줘"
```

---

## Claude Desktop 연동

### 1. Claude Desktop 설정 파일 위치

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Mac:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

### 2. 설정 파일 수정

`claude_desktop_config.json` 파일을 열고 다음 내용을 추가합니다:

```json
{
  "mcpServers": {
    "while-you-were-sleeping-stocks": {
      "command": "python",
      "args": [
        "C:\\Users\\tlduf\\Downloads\\ica-project\\backend\\mcp_servers\\stocks_server.py"
      ],
      "env": {
        "PYTHONPATH": "C:\\Users\\tlduf\\Downloads\\ica-project\\backend"
      }
    },
    "while-you-were-sleeping-briefing": {
      "command": "python",
      "args": [
        "C:\\Users\\tlduf\\Downloads\\ica-project\\backend\\mcp_servers\\briefing_server.py"
      ],
      "env": {
        "PYTHONPATH": "C:\\Users\\tlduf\\Downloads\\ica-project\\backend",
        "GEMINI_API_KEY": "your_actual_gemini_api_key",
        "EXA_API_KEY": "your_actual_exa_api_key"
      }
    }
  }
}
```

**⚠️ 중요:**
- 경로를 실제 프로젝트 경로로 수정하세요
- `GEMINI_API_KEY`와 `EXA_API_KEY`를 실제 API 키로 교체하세요
- Windows에서는 `\\` (역슬래시 2개) 사용
- Mac/Linux에서는 `/` (슬래시) 사용

### 3. Claude Desktop 재시작

설정 파일을 저장한 후 Claude Desktop을 완전히 종료하고 다시 실행합니다.

---

## 사용 방법

### 1. 화제 종목 조회

Claude Desktop에서 다음과 같이 요청:

```
오늘 미국 주식 화제 종목을 알려줘
```

```
거래량이 가장 많은 종목 10개를 보여줘
```

```
AAPL 주식의 상세 정보를 알려줘
```

### 2. 브리핑 생성

```
오늘의 주식 브리핑을 생성해줘
```

```
테슬라(TSLA)가 왜 화제인지 분석해줘
```

```
애플(AAPL) 관련 최신 뉴스를 찾아줘
```

### 3. 자동화된 워크플로우

```
화제 종목을 찾고 브리핑을 만들어줘
```

Claude가 자동으로:
1. 화제 종목 조회
2. 뉴스 수집
3. AI 분석
4. 브리핑 생성

---

## MCP 서버 직접 테스트

Claude Desktop 없이 MCP 서버를 직접 테스트할 수 있습니다:

### Stocks Server 테스트
```bash
cd backend/mcp_servers
python stocks_server.py
```

### Briefing Server 테스트
```bash
cd backend/mcp_servers
python briefing_server.py
```

---

## 문제 해결

### 1. "MCP 서버를 찾을 수 없습니다"

**원인**: 경로 설정이 잘못됨

**해결:**
- `claude_desktop_config.json`의 파일 경로를 확인
- 절대 경로를 사용하는지 확인
- Windows에서는 `\\` 사용

### 2. "도구를 실행할 수 없습니다"

**원인**: Python 환경 또는 의존성 문제

**해결:**
```bash
cd backend
pip install mcp yahooquery google-generativeai exa-py
```

### 3. "API 키 오류"

**원인**: 환경 변수에 API 키가 없음

**해결:**
- `claude_desktop_config.json`의 `env` 섹션에 실제 API 키 입력
- 또는 `backend/.env` 파일에 API 키 설정

### 4. "모듈을 찾을 수 없음" 오류

**원인**: PYTHONPATH 설정 문제

**해결:**
- `claude_desktop_config.json`의 `PYTHONPATH` 확인
- backend 폴더의 절대 경로로 설정

### 5. Claude Desktop에서 도구가 보이지 않음

**체크리스트:**
1. ✅ `claude_desktop_config.json` 저장했는지 확인
2. ✅ Claude Desktop 재시작했는지 확인
3. ✅ JSON 문법 오류가 없는지 확인 (https://jsonlint.com)
4. ✅ 경로가 정확한지 확인

---

## 제공되는 도구 목록

### Stocks Server Tools
| 도구 이름 | 설명 | 파라미터 |
|---------|------|---------|
| `get_trending_stocks` | 화제 종목 목록 조회 | screener_types, count |
| `get_top_trending_stock` | TOP 1 종목 조회 | screener_types, count |
| `get_stock_info` | 종목 상세 정보 | symbol |

### Briefing Server Tools
| 도구 이름 | 설명 | 파라미터 |
|---------|------|---------|
| `generate_daily_briefing` | 자동 브리핑 생성 | include_image |
| `analyze_stock_trending_reason` | 화제 원인 분석 | symbol, include_news |
| `get_stock_news` | 뉴스 수집 | symbol, limit |

---

## 고급 설정

### 환경 변수 분리

보안을 위해 API 키를 별도 파일로 관리:

1. `backend/.env` 파일에 API 키 저장
2. `claude_desktop_config.json`에서 env 섹션 제거
3. MCP 서버가 자동으로 `.env` 파일 읽음

### 로그 확인

MCP 서버 로그 확인:
```bash
# Windows
%APPDATA%\Claude\logs\

# Mac
~/Library/Logs/Claude/

# Linux
~/.config/Claude/logs/
```

---

## 다음 단계

1. ✅ MCP 서버 설정 완료
2. ✅ Claude Desktop 연동
3. 🔜 커스텀 도구 추가
4. 🔜 다른 MCP 클라이언트 연동

---

## 참고 자료

- [MCP 공식 문서](https://modelcontextprotocol.io/)
- [Claude Desktop MCP 가이드](https://docs.anthropic.com/claude/docs/model-context-protocol)
- [프로젝트 문서](../README.md)

MCP를 통해 "당신이 잠든 사이" 기능을 Claude Desktop에서 직접 사용하세요! 🚀
