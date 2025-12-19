# FastAPI 서버 실행 가이드

## 📚 목차
1. [설치](#설치)
2. [실행](#실행)
3. [API 문서](#api-문서)
4. [프로젝트 구조](#프로젝트-구조)
5. [API 엔드포인트](#api-엔드포인트)
6. [예제 요청](#예제-요청)

---

## 설치

### 1. 의존성 설치

```bash
# 기존 requirements.txt 설치
pip install -r requirements.txt

# FastAPI 추가 의존성 설치
pip install -r requirements_fastapi.txt
```

또는 한 번에 설치:

```bash
pip install fastapi uvicorn pydantic python-multipart
```

### 2. 환경 변수 설정

`.env` 파일 생성 (backend 폴더 내):

```env
# Gemini API
GEMINI_API_KEY=your_gemini_api_key

# Exa API
EXA_API_KEY=your_exa_api_key

# 이메일 발송 (선택)
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_password

# Slack 발송 (선택)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXX/YYY/ZZZ
```

---

## 실행

### 개발 모드 실행

```bash
# 방법 1: Python으로 직접 실행
python main.py

# 방법 2: uvicorn으로 실행 (권장)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 방법 3: uvicorn으로 특정 포트 실행
uvicorn main:app --reload --port 8080
```

### 프로덕션 모드 실행

```bash
# workers를 사용하여 성능 향상
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## API 문서

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:

- **Swagger UI (대화형)**: http://localhost:8000/docs
- **ReDoc (읽기 전용)**: http://localhost:8000/redoc
- **헬스체크**: http://localhost:8000/health

---

## 프로젝트 구조

```
backend/
├── main.py                       # FastAPI 앱 진입점
├── routers/                      # API 라우터
│   ├── __init__.py
│   ├── stocks.py                # 화제 종목 API
│   ├── briefings.py             # 브리핑 API
│   └── auth.py                  # 인증 API
├── models/                       # 데이터 모델
│   ├── __init__.py
│   └── schemas.py               # Pydantic 스키마
├── get_trending_stocks.py       # 화제 종목 수집
├── daily_briefing_workflow.py   # 브리핑 워크플로우
├── requirements_fastapi.txt     # FastAPI 의존성
├── FASTAPI_ROUTER_가이드.md     # FastAPI 가이드
└── README_FASTAPI.md            # 이 파일
```

---

## API 엔드포인트

### 1. 화제 종목 API

#### GET `/v1/trending-stocks` - 화제 종목 조회
- **설명**: Yahoo Finance Screener에서 화제 종목 목록 조회
- **인증**: 선택적
- **파라미터**:
  - `screener_types`: 스크리너 타입 (기본: "most_actives,day_gainers")
  - `count`: 각 스크리너당 종목 수 (1-50, 기본: 10)
  - `limit`: 최종 반환 종목 수 (1-100, 기본: 10)
  - `min_volume`: 최소 거래량 필터
  - `sort_by`: 정렬 기준 (score, volume, change_percent)
  - `order`: 정렬 순서 (asc, desc)

#### GET `/v1/stocks/{symbol}` - 종목 상세 정보
- **설명**: 특정 종목의 상세 정보와 뉴스 조회
- **인증**: 선택적
- **Path 파라미터**:
  - `symbol`: 종목 심볼 (예: AAPL, TSLA)
- **Query 파라미터**:
  - `include_news`: 뉴스 포함 여부 (기본: true)
  - `news_limit`: 뉴스 개수 (1-20, 기본: 5)
  - `include_financials`: 재무 정보 포함 여부 (기본: false)

### 2. 브리핑 API

#### POST `/v1/briefings` - 브리핑 생성
- **설명**: AI 브리핑 생성
- **인증**: 필수
- **Request Body**:
  ```json
  {
    "stock_symbols": ["AAPL", "TSLA"],
    "format": "both",
    "language": "ko",
    "count": 5
  }
  ```

#### GET `/v1/briefings` - 브리핑 목록 조회
- **설명**: 생성된 브리핑 목록 조회
- **인증**: 필수
- **파라미터**:
  - `page`: 페이지 번호 (기본: 1)
  - `limit`: 페이지당 항목 수 (기본: 20)
  - `start_date`: 시작 날짜
  - `end_date`: 종료 날짜

#### GET `/v1/briefings/{briefing_id}` - 브리핑 상세 조회
- **설명**: 특정 브리핑 상세 정보 조회
- **인증**: 필수

#### POST `/v1/briefings/{briefing_id}/send` - 브리핑 발송
- **설명**: 브리핑을 이메일/Slack으로 발송
- **인증**: 필수
- **Request Body**:
  ```json
  {
    "channels": [
      {
        "type": "email",
        "email": "user@example.com"
      }
    ],
    "send_immediately": true
  }
  ```

### 3. 인증 API

#### POST `/v1/auth/login` - 로그인
- **설명**: 사용자 로그인 및 JWT 토큰 발급
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "your_password"
  }
  ```

#### POST `/v1/auth/refresh` - 토큰 갱신
- **설명**: Refresh token으로 새 토큰 발급

---

## 예제 요청

### 1. 화제 종목 조회

```bash
# curl 요청
curl -X GET "http://localhost:8000/v1/trending-stocks?screener_types=most_actives,day_gainers&count=10&limit=5"

# Python requests
import requests

response = requests.get(
    "http://localhost:8000/v1/trending-stocks",
    params={
        "screener_types": "most_actives,day_gainers",
        "count": 10,
        "limit": 5
    }
)
print(response.json())
```

### 2. 종목 상세 정보 조회

```bash
# curl 요청
curl -X GET "http://localhost:8000/v1/stocks/AAPL?include_news=true&news_limit=5"

# Python requests
import requests

response = requests.get(
    "http://localhost:8000/v1/stocks/AAPL",
    params={
        "include_news": True,
        "news_limit": 5
    }
)
print(response.json())
```

### 3. 브리핑 생성

```bash
# curl 요청
curl -X POST "http://localhost:8000/v1/briefings" \
  -H "Content-Type: application/json" \
  -d '{
    "stock_symbols": ["AAPL", "TSLA", "MSFT"],
    "format": "both",
    "language": "ko",
    "count": 5
  }'

# Python requests
import requests

response = requests.post(
    "http://localhost:8000/v1/briefings",
    json={
        "stock_symbols": ["AAPL", "TSLA", "MSFT"],
        "format": "both",
        "language": "ko",
        "count": 5
    }
)
print(response.json())
```

### 4. 로그인

```bash
# curl 요청
curl -X POST "http://localhost:8000/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password"
  }'

# Python requests
import requests

response = requests.post(
    "http://localhost:8000/v1/auth/login",
    json={
        "email": "test@example.com",
        "password": "password"
    }
)
token = response.json()["data"]["token"]
print(f"Token: {token}")
```

---

## CORS 설정

Next.js 프론트엔드와 연동하기 위해 CORS가 설정되어 있습니다:

```python
# main.py에서 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

프로덕션 환경에서는 `allow_origins`를 실제 도메인으로 변경하세요.

---

## Next.js에서 API 호출하기

### 예제: 화제 종목 조회

```typescript
// pages/api/trending-stocks.ts 또는 클라이언트 컴포넌트
async function getTrendingStocks() {
  const response = await fetch(
    'http://localhost:8000/v1/trending-stocks?screener_types=most_actives&count=10&limit=5'
  );

  if (!response.ok) {
    throw new Error('Failed to fetch trending stocks');
  }

  const data = await response.json();
  return data.data.stocks;
}

// 사용 예시
const stocks = await getTrendingStocks();
console.log(stocks);
```

---

## 문제 해결

### 1. 포트 충돌
```bash
# 다른 포트로 실행
uvicorn main:app --reload --port 8001
```

### 2. 모듈을 찾을 수 없음
```bash
# backend 폴더에서 실행하는지 확인
cd backend
python main.py
```

### 3. CORS 에러
- `main.py`의 CORS 설정에서 프론트엔드 URL 확인
- 브라우저 개발자 도구에서 네트워크 탭 확인

---

## 다음 단계

1. **데이터베이스 연동**: PostgreSQL 또는 MongoDB 연동
2. **JWT 인증 구현**: 실제 토큰 생성 및 검증
3. **Rate Limiting**: API 호출 제한 추가
4. **로깅**: 구조화된 로깅 시스템
5. **테스트**: pytest로 API 테스트 작성
6. **배포**: Docker 컨테이너화 및 배포

---

## 참고 자료

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [Pydantic 문서](https://docs.pydantic.dev/)
- [Uvicorn 문서](https://www.uvicorn.org/)
- [REST API 명세서](../REST_API_명세서.md)
- [FastAPI Router 가이드](./FASTAPI_ROUTER_가이드.md)
