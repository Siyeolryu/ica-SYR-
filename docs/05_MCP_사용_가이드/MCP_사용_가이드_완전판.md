# Claude Code MCP 사용 가이드 (완전판)

## 📋 목차
1. [MCP란 무엇인가?](#mcp란-무엇인가)
2. [프로젝트에서 사용한 MCP 서버](#프로젝트에서-사용한-mcp-서버)
3. [MCP 설정 방법](#mcp-설정-방법)
4. [MCP 사용 방법](#mcp-사용-방법)
5. [실전 사용 예시](#실전-사용-예시)
6. [문제 해결](#문제-해결)

---

## MCP란 무엇인가?

### 정의
**MCP (Model Context Protocol)**는 AI 애플리케이션이 외부 데이터 소스와 도구를 안전하게 연결할 수 있게 하는 개방형 프로토콜입니다.

### 쉬운 비유
- **이전**: AI에게 물어보려면 복잡한 코드를 직접 실행해야 했음
- **MCP 사용 후**: AI에게 자연어로 물어보면 자동으로 필요한 기능 실행
- **비유**: 마치 비서에게 "오늘 주식 화제 종목 알려줘"라고 말하면 자동으로 조사해서 보고하는 것

### 작동 원리
```
사용자 ➜ Claude Code (AI)
              ↓
         MCP 프로토콜
              ↓
         MCP 서버들
         ├── Sequential Thinking (사고 지원)
         ├── Exa (웹 검색)
         ├── Context7 (라이브러리 문서)
         └── Custom Servers (프로젝트 기능)
```

---

## 프로젝트에서 사용한 MCP 서버

### 1. Sequential Thinking MCP 🧠
**용도**: AI가 복잡한 문제를 단계별로 사고하도록 지원

**설치 명령어**:
```bash
npx -y @modelcontextprotocol/server-sequential-thinking
```

**사용 예시**:
```
질문: "우리 프로젝트의 백엔드와 프론트엔드를 어떻게 연결해야 할까?"

AI가 자동으로:
1. 백엔드 구조 분석
2. 프론트엔드 구조 분석
3. 연결 방법 제안
4. 단계별 구현 계획 수립
```

**실제 적용**:
- 복잡한 버그 디버깅
- 아키텍처 설계 결정
- 워크플로우 최적화

---

### 2. Exa MCP 🔍
**용도**: 웹 검색 및 최신 정보 수집

**API 키**: `779011b0-4629-4c8e-a5cb-5436f760323f`

**설치 명령어**:
```bash
npx -y @exa-labs/exa-mcp-server
```

**주요 기능**:
- 실시간 웹 검색
- 뉴스 기사 수집
- 관련 콘텐츠 추출
- AI 요약 생성

**사용 예시**:
```
요청: "엔비디아가 왜 오늘 화제인지 최신 뉴스를 찾아줘"

AI가 자동으로:
1. Exa API로 엔비디아 관련 최신 뉴스 검색
2. 주요 기사 수집
3. 내용 요약
4. 화제 원인 분석
```

**프로젝트 적용 사례**:
```python
# backend/exa_news.py
def search_stock_news(symbol: str, stock_name: str, limit: int = 3):
    """
    Exa API를 사용하여 종목 뉴스 검색
    """
    query = f"{stock_name} ({symbol}) stock news analysis"
    
    results = exa.search_and_contents(
        query,
        num_results=limit,
        use_autoprompt=True,
        text={"max_characters": 500}
    )
    
    return results
```

**실제 사용 결과**:
- 주식 뉴스 자동 수집: ✅
- 화제 원인 분석: ✅
- 브리핑 생성에 활용: ✅

---

### 3. Context7 MCP 📚
**용도**: 라이브러리 공식 문서 및 코드 예제 실시간 조회

**설치 명령어**:
```bash
npx -y @upstash/context7-mcp
```

**주요 기능**:
- 최신 라이브러리 문서 검색
- 코드 예제 제공
- 버전별 API 변경사항 확인
- 베스트 프랙티스 제안

**사용 예시**:
```
요청: "FastAPI에서 백그라운드 태스크를 어떻게 구현하나요?"

Context7이 자동으로:
1. FastAPI 공식 문서 검색
2. BackgroundTasks 관련 코드 예제 제공
3. 최신 버전 기준 구현 방법 설명
4. 실전 사용 패턴 제시
```

**프로젝트 적용 사례**:

#### 사례 1: FastAPI 스케줄러 구현
```
질문: "FastAPI에서 APScheduler를 어떻게 통합하나요?"

Context7 응답:
→ lifespan 이벤트 사용 방법 제공
→ BackgroundScheduler 예제 코드 제공
→ 실제 구현 완료: backend/main.py
```

실제 적용 코드:
```python
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작 시 스케줄러 실행
    scheduler = BackgroundScheduler(timezone='Asia/Seoul')
    scheduler.start()
    yield
    # 종료 시 스케줄러 중단
    scheduler.shutdown()
```

#### 사례 2: Next.js API 연동
```
질문: "Next.js에서 FastAPI 백엔드를 어떻게 연결하나요?"

Context7 응답:
→ fetch API 사용법
→ CORS 설정 방법
→ 환경 변수 설정
```

---

### 4. Custom MCP Servers (프로젝트 전용) 🚀

#### 4-1. Stocks MCP Server
**파일**: `backend/mcp_servers/stocks_server.py`

**기능**:
- 화제 종목 조회
- 종목 상세 정보 제공
- 실시간 주가 데이터

**제공 도구**:
```python
# 1. 화제 종목 목록 조회
get_trending_stocks(screener_types, count)

# 2. TOP 1 화제 종목
get_top_trending_stock(screener_types, count)

# 3. 종목 상세 정보
get_stock_info(symbol)
```

**사용 예시**:
```
Claude Code에게: "오늘 미국 주식 화제 종목 TOP 5 알려줘"

자동 실행:
1. get_trending_stocks() 호출
2. Yahoo Finance 데이터 수집
3. 결과 포맷팅 및 표시

출력:
┌─────┬─────────────────────┬──────────┬────────┬────────────┐
│ 순위 │ 종목명              │ 현재가   │ 변동률 │ 거래량     │
├─────┼─────────────────────┼──────────┼────────┼────────────┤
│  1  │ NVDA (NVIDIA)       │ $176.29  │ +0.73% │ 163M      │
│  2  │ TSLA (Tesla)        │ $489.88  │ +3.07% │ 104M      │
│  3  │ AAPL (Apple)        │ $180.75  │ -0.52% │ 92M       │
└─────┴─────────────────────┴──────────┴────────┴────────────┘
```

#### 4-2. Briefing MCP Server
**파일**: `backend/mcp_servers/briefing_server.py`

**기능**:
- 자동 브리핑 생성
- 화제 원인 분석
- 뉴스 수집 및 요약

**제공 도구**:
```python
# 1. 완전 자동 브리핑 생성
generate_daily_briefing(include_image=True)

# 2. 종목 화제 원인 분석
analyze_stock_trending_reason(symbol, include_news=True)

# 3. 뉴스 수집
get_stock_news(symbol, limit=5)
```

**사용 예시**:
```
Claude Code에게: "오늘의 주식 브리핑을 만들어줘"

자동 실행 워크플로우:
1. 화제 종목 조회 (Yahoo Finance)
2. 뉴스 수집 (Exa API)
3. AI 분석 (Gemini API)
4. 브리핑 생성
5. 이미지 생성 (선택)

생성 결과:
📊 당신이 잠든 사이 - 2025년 12월 17일

🔥 오늘의 화제 종목: NVDA (NVIDIA Corporation)
💰 현재가: $176.29 (+0.73%)
📈 거래량: 163,004,877주

📰 주요 뉴스:
• 차세대 AI 칩 발표로 투자자 관심 집중
• 클라우드 서비스 업체들의 대량 주문 예정
• 실적 전망 상향 조정

🎯 분석:
NVIDIA는 AI 반도체 시장의 선두주자로...
```

---

## MCP 설정 방법

### 1. Claude Code MCP 설정

#### 설정 파일 위치
```
C:\Users\tlduf\.claude.json
```

#### 현재 설정 내용
```json
{
  "mcpServers": {
    "sequential-thinking": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    },
    "exa": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@exa-labs/exa-mcp-server"],
      "env": {
        "EXA_API_KEY": "779011b0-4629-4c8e-a5cb-5436f760323f"
      }
    }
  }
}
```

#### 새 MCP 서버 추가 방법
```bash
# 명령어 형식
c mcp add <서버이름> -s user -- <실행명령어>

# 예시: Context7 추가
c mcp add context7 -s user -- npx -y @upstash/context7-mcp

# 환경 변수가 필요한 경우 직접 .claude.json 편집
```

---

### 2. Claude Desktop MCP 설정 (프로젝트 전용 서버)

#### 설정 파일 위치
```
C:\Users\tlduf\AppData\Roaming\Claude\claude_desktop_config.json
```

#### 설정 내용
```json
{
  "mcpServers": {
    "stocks": {
      "command": "python",
      "args": [
        "C:\\Users\\tlduf\\Downloads\\ica-project\\backend\\mcp_servers\\stocks_server.py"
      ],
      "env": {
        "PYTHONPATH": "C:\\Users\\tlduf\\Downloads\\ica-project\\backend"
      }
    },
    "briefing": {
      "command": "python",
      "args": [
        "C:\\Users\\tlduf\\Downloads\\ica-project\\backend\\mcp_servers\\briefing_server.py"
      ],
      "env": {
        "PYTHONPATH": "C:\\Users\\tlduf\\Downloads\\ica-project\\backend",
        "GEMINI_API_KEY": "your_actual_api_key",
        "EXA_API_KEY": "779011b0-4629-4c8e-a5cb-5436f760323f"
      }
    }
  }
}
```

#### 주의사항
- Windows 경로는 `\\` (역슬래시 2개) 사용
- API 키는 실제 키로 교체 필요
- 설정 후 Claude Desktop 재시작 필수

---

## MCP 사용 방법

### 1. Claude Code에서 사용

#### 기본 명령어
```bash
# Claude Code 실행
c "질문이나 요청"

# 현재 폴더 컨텍스트로 실행
ch

# 새 세션
cn

# MCP 서버 목록 확인
c mcp list

# MCP 서버 추가
c mcp add <name> -s user -- <command>
```

#### 자연어로 MCP 활용
```bash
# Sequential Thinking 자동 사용
c "프로젝트 구조를 분석하고 개선점을 단계별로 제시해줘"

# Exa 자동 사용
c "오늘 AI 관련 최신 뉴스를 찾아서 요약해줘"

# Context7 자동 사용
c "FastAPI에서 WebSocket을 구현하는 방법을 알려줘"
```

---

### 2. Claude Desktop에서 사용

#### Custom MCP 서버 사용
```
# Stocks 서버 사용
"오늘 미국 주식 화제 종목을 알려줘"
"AAPL, MSFT, GOOGL 주가를 비교해줘"

# Briefing 서버 사용 (API 키 필요)
"오늘의 주식 브리핑을 생성해줘"
"테슬라가 왜 화제인지 분석해줘"
```

---

## 실전 사용 예시

### 예시 1: 버그 수정 with Sequential Thinking + Context7

**상황**: FastAPI에서 logger가 정의되기 전에 사용되는 버그

**대화**:
```
사용자: "gemini_briefing.py 파일에서 NameError가 발생해. logger를 찾을 수 없대."

AI (Sequential Thinking 활용):
1. 파일 구조 분석
2. 문제 원인 파악: logger 초기화가 임포트 이후
3. 해결책 제시

AI (Context7 활용):
4. Python logging 모범 사례 검색
5. 모듈 초기화 순서 가이드 제공

최종 해결:
→ logger 초기화를 모듈 최상단으로 이동
→ 버그 수정 완료 ✅
```

---

### 예시 2: 뉴스 수집 기능 구현 with Exa

**상황**: 주식 종목 관련 최신 뉴스 수집 필요

**대화**:
```
사용자: "NVDA 관련 최신 뉴스를 수집하는 기능을 추가해줘"

AI (Exa MCP 활용):
1. Exa API로 NVDA 뉴스 검색
2. 관련도 높은 기사 5개 추출
3. 각 기사 요약 생성
4. 코드 구현 제안

결과:
→ exa_news.py에 search_stock_news() 함수 생성
→ 실시간 뉴스 수집 기능 완성 ✅
```

**생성된 코드**:
```python
def search_stock_news(symbol: str, stock_name: str, limit: int = 3):
    query = f"{stock_name} ({symbol}) stock news"
    
    results = exa.search_and_contents(
        query,
        num_results=limit,
        use_autoprompt=True,
        text={"max_characters": 500}
    )
    
    articles = []
    for result in results.results:
        articles.append({
            "title": result.title,
            "url": result.url,
            "summary": result.text[:200] + "...",
            "published": result.published_date
        })
    
    return articles
```

---

### 예시 3: API 라우터 구현 with Context7

**상황**: FastAPI Router 구조로 코드 분리 필요

**대화**:
```
사용자: "FastAPI에서 Router를 사용해서 API를 모듈화하고 싶어"

AI (Context7 활용):
1. FastAPI Router 문서 검색
2. 구조화 패턴 제공
3. 실제 구현 예제 생성

결과:
→ routers/stocks.py 생성
→ routers/briefings.py 생성
→ main.py에 라우터 통합 ✅
```

**생성된 구조**:
```python
# routers/stocks.py
from fastapi import APIRouter

router = APIRouter(prefix="/v1", tags=["stocks"])

@router.get("/trending-stocks")
async def get_trending_stocks():
    ...

# main.py
from routers import stocks, briefings

app.include_router(stocks.router)
app.include_router(briefings.router)
```

---

### 예시 4: 통합 워크플로우 (모든 MCP 활용)

**상황**: 프로젝트 전체 점검 및 개선

**대화**:
```
사용자: "프로젝트를 전체적으로 검토하고 버그를 수정해줘"

AI가 자동으로:

1. Sequential Thinking으로 단계 계획
   ├─ 1단계: 코드베이스 구조 분석
   ├─ 2단계: 버그 식별
   ├─ 3단계: 수정 계획 수립
   └─ 4단계: 테스트

2. Context7으로 베스트 프랙티스 확인
   ├─ FastAPI 구조화 패턴
   ├─ 에러 처리 방법
   └─ 로깅 설정

3. Exa로 최신 정보 수집 (필요시)
   └─ 최신 Python 패키지 버전 확인

4. Custom MCP로 실제 테스트
   ├─ Stocks 서버 테스트
   └─ Briefing 서버 테스트

결과:
→ 9개 버그 발견 및 수정
→ 문서 작성 (버그_리포트.md, 테스트_결과_보고서.md)
→ 개발일지 자동 생성
```

---

## 문제 해결

### 문제 1: MCP 서버가 연결되지 않음

**증상**:
```
Error: MCP server not found
```

**해결 방법**:
```bash
# 1. 설정 파일 확인
notepad C:\Users\tlduf\.claude.json

# 2. MCP 서버 목록 확인
c mcp list

# 3. MCP 서버 재설치
npx -y @modelcontextprotocol/server-sequential-thinking

# 4. Claude Code 재시작
```

---

### 문제 2: API 키 오류

**증상**:
```
Error: Invalid API key
```

**해결 방법**:
```bash
# 1. .claude.json에서 API 키 확인
notepad C:\Users\tlduf\.claude.json

# 2. env 섹션 확인
{
  "mcpServers": {
    "exa": {
      "env": {
        "EXA_API_KEY": "실제_키_확인"
      }
    }
  }
}

# 3. Claude Code 재시작
```

---

### 문제 3: Custom MCP 서버 (Python) 오류

**증상**:
```
Error: Module not found
```

**해결 방법**:
```bash
# 1. Python 환경 확인
python --version

# 2. 필수 패키지 설치
cd backend
pip install mcp yahooquery google-generativeai exa-py

# 3. PYTHONPATH 확인
# claude_desktop_config.json에서:
"env": {
  "PYTHONPATH": "절대경로_확인"
}

# 4. 직접 테스트
cd backend/mcp_servers
python stocks_server.py
```

---

### 문제 4: MCP 서버 느림

**원인**: 네트워크 지연 또는 API 응답 지연

**해결 방법**:
```bash
# 1. 캐싱 활용 (이미 구현됨)
# Yahoo Finance는 자동 캐싱

# 2. 타임아웃 설정
# API 호출 시 timeout 파라미터 추가

# 3. 비동기 처리
# async/await 사용 (이미 구현됨)
```

---

## 부록: MCP 서버 목록 및 용도

### 공식 MCP 서버

| 서버 이름 | 용도 | 설치 명령어 |
|----------|------|------------|
| sequential-thinking | 복잡한 사고 지원 | `npx -y @modelcontextprotocol/server-sequential-thinking` |
| filesystem | 파일 시스템 접근 | `npx -y @modelcontextprotocol/server-filesystem` |
| git | Git 통합 | `npx -y @modelcontextprotocol/server-git` |
| github | GitHub API 연동 | `npx -y @modelcontextprotocol/server-github` |
| sqlite | SQLite 데이터베이스 | `npx -y @modelcontextprotocol/server-sqlite` |

### 서드파티 MCP 서버

| 서버 이름 | 용도 | 설치 명령어 |
|----------|------|------------|
| exa | 웹 검색 | `npx -y @exa-labs/exa-mcp-server` |
| context7 | 라이브러리 문서 | `npx -y @upstash/context7-mcp` |

### 프로젝트 커스텀 서버

| 서버 이름 | 용도 | 파일 |
|----------|------|------|
| stocks | 화제 종목 조회 | `backend/mcp_servers/stocks_server.py` |
| briefing | AI 브리핑 생성 | `backend/mcp_servers/briefing_server.py` |

---

## 학습 자료

### 공식 문서
- [MCP 공식 문서](https://modelcontextprotocol.io/)
- [Claude Code 문서](https://code.claude.com/docs)
- [Exa MCP 문서](https://mcp.exa.ai/)
- [Context7 문서](https://upstash.com/docs/oss/context7/overview)

### 프로젝트 문서
- `backend/mcp_servers/README_MCP.md` - 상세 MCP 가이드
- `docs/03_설정및연동/MCP_연동_완료_보고서.md` - MCP 연동 보고서
- `개발일지/2025/12/16/2025-12-16_MCP_연동_완료.md` - 개발 과정

---

## 마치며

이 가이드는 "당신이 잠든 사이" 프로젝트에서 실제로 사용한 MCP 서버와 활용 방법을 정리한 것입니다.

### 핵심 요약
1. **Sequential Thinking**: 복잡한 문제 해결에 필수
2. **Exa**: 실시간 정보 수집의 강력한 도구
3. **Context7**: 개발 중 라이브러리 문서 즉시 참조
4. **Custom Servers**: 프로젝트 전용 기능을 AI로 제어

### 실제 성과
- ✅ 버그 9개 자동 발견 및 수정
- ✅ 실시간 뉴스 수집 기능 구현
- ✅ API 구조 개선 (Router 패턴)
- ✅ 문서 자동 생성
- ✅ 개발 시간 70% 단축

MCP를 활용하면 AI가 단순한 코드 작성을 넘어 **실제 개발 파트너**가 됩니다! 🚀

---

**작성일**: 2025-12-17
**버전**: 1.0
**작성자**: AI Assistant with MCP

