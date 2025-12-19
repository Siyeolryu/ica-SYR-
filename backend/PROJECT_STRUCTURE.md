ㄴ# FastAPI 프로젝트 구조

## 📁 디렉토리 구조

```
backend/
├── main.py              # FastAPI 애플리케이션 진입점
├── requirements.txt     # Python 패키지 의존성
├── .env                 # 환경 변수 설정
│
├── api/                 # API 라우터 (엔드포인트 정의)
│   ├── __init__.py
│   ├── stocks.py       # 주식 관련 API 엔드포인트
│   ├── briefings.py    # 브리핑 관련 API 엔드포인트
│   └── auth.py         # 인증 관련 API 엔드포인트
│
├── services/           # 비즈니스 로직
│   ├── __init__.py
│   ├── stock_service.py      # 주식 데이터 처리 서비스
│   ├── briefing_service.py   # 브리핑 생성 서비스
│   └── auth_service.py       # 인증 처리 서비스
│
└── models/             # Pydantic 모델 (데이터 스키마)
    ├── __init__.py
    └── schemas.py      # API 요청/응답 스키마
```

## 🏗️ 아키텍처 패턴

### 계층 분리 (Layered Architecture)

1. **API Layer** (`api/`)
   - HTTP 요청/응답 처리
   - 입력 유효성 검증
   - 에러 핸들링
   - Services 호출

2. **Service Layer** (`services/`)
   - 비즈니스 로직 구현
   - 외부 API 호출
   - 데이터 가공 및 변환
   - 트랜잭션 관리

3. **Model Layer** (`models/`)
   - 데이터 스키마 정의
   - 요청/응답 모델
   - 데이터 유효성 검증

## 📝 주요 파일 설명

### main.py
- FastAPI 애플리케이션 생성
- CORS 미들웨어 설정
- 라우터 등록
- 애플리케이션 라이프사이클 관리

### api/ (라우터)
각 라우터는 관련된 엔드포인트를 그룹화합니다:
- `stocks.py`: `/v1/trending-stocks`, `/v1/stocks/{symbol}`
- `briefings.py`: `/v1/briefings`, `/v1/briefings/{id}`
- `auth.py`: `/v1/auth/login`, `/v1/auth/refresh`

### services/ (비즈니스 로직)
API 라우터에서 호출되는 실제 비즈니스 로직:
- `stock_service.py`: 주식 데이터 수집, 필터링, 점수 계산
- `briefing_service.py`: AI 브리핑 생성, 발송
- `auth_service.py`: 사용자 인증, 토큰 관리

### models/ (데이터 모델)
Pydantic 모델로 API 입출력 스키마 정의:
- Request 모델: API 요청 데이터 검증
- Response 모델: API 응답 데이터 형식
- Error 모델: 에러 응답 형식

## 🔧 설정 파일

### requirements.txt
필요한 Python 패키지:
- `fastapi`: 웹 프레임워크
- `uvicorn`: ASGI 서버
- `yahooquery`: Yahoo Finance API
- `pydantic`: 데이터 검증
- 기타 의존성

### .env
환경 변수 설정:
```
GEMINI_API_KEY=your_key
EXA_API_KEY=your_key
EMAIL_USERNAME=your_email
SLACK_WEBHOOK_URL=your_webhook
```

## 🚀 서버 실행

### 개발 모드
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

### 프로덕션 모드
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📚 API 문서

서버 실행 후 다음 URL에서 API 문서 확인:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔒 CORS 설정

프론트엔드 접근 허용:
- `http://localhost:3000` (Next.js 기본 포트)
- `http://localhost:3001` (대체 포트)

## 🧪 API 테스트 예시

### 헬스체크
```bash
curl http://localhost:8000/health
```

### 화제 종목 조회
```bash
curl "http://localhost:8000/v1/trending-stocks?limit=5"
```

### 종목 상세 조회
```bash
curl "http://localhost:8000/v1/stocks/AAPL?include_news=true"
```

## 📦 패키지 설치

```bash
cd backend
pip install -r requirements.txt
```

## 🔄 데이터 흐름

```
Client Request
    ↓
FastAPI Router (api/)
    ↓
Service Layer (services/)
    ↓
External APIs (Yahoo Finance, Gemini, etc.)
    ↓
Service Layer (데이터 가공)
    ↓
FastAPI Router (응답 생성)
    ↓
Client Response
```

## 💡 개발 가이드

### 새로운 엔드포인트 추가
1. `models/schemas.py`에 Request/Response 모델 정의
2. `services/`에 비즈니스 로직 구현
3. `api/`에 라우터 엔드포인트 추가
4. `main.py`에 라우터 등록 (필요시)

### 코드 스타일
- 함수/변수명: snake_case
- 클래스명: PascalCase
- 상수: UPPER_CASE
- Docstring: Google Style

## 🛠️ 문제 해결

### 포트 충돌
다른 포트 사용:
```bash
uvicorn main:app --port 8001
```

### 패키지 오류
의존성 재설치:
```bash
pip install -r requirements.txt --upgrade
```

## 📞 지원

문제가 발생하면 다음을 확인하세요:
1. Python 버전 (3.9 이상 권장)
2. 가상 환경 활성화
3. 환경 변수 설정 (.env 파일)
4. 로그 확인 (콘솔 출력)
