# FastAPI 프로젝트 세팅 가이드

## ✅ 완료된 세팅

FastAPI 프로젝트가 성공적으로 세팅되었습니다!

### 설치된 항목
- ✅ FastAPI 0.124.4
- ✅ Uvicorn 0.38.0 (ASGI 서버)
- ✅ Pydantic 2.12.5 (데이터 검증)
- ✅ Python-multipart (파일 업로드 지원)

### 생성된 파일
- ✅ `backend/main.py` - FastAPI 메인 애플리케이션
- ✅ `backend/routers/` - API 라우터 모듈
  - `stocks.py` - 화제 종목 API
  - `briefings.py` - 브리핑 API
  - `auth.py` - 인증 API
- ✅ `backend/models/schemas.py` - Pydantic 스키마
- ✅ `backend/.env` - 환경 변수 파일 (템플릿)
- ✅ `backend/start_server.bat` - Windows 실행 스크립트
- ✅ `backend/start_server.sh` - Linux/Mac 실행 스크립트

---

## 🚀 서버 실행 방법

### 방법 1: 간편 실행 (권장)

#### Windows
```bash
cd backend
start_server.bat
```

#### Linux/Mac
```bash
cd backend
chmod +x start_server.sh
./start_server.sh
```

### 방법 2: 직접 실행

```bash
cd backend
python main.py
```

### 방법 3: uvicorn 명령어

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📖 서버 접속

서버가 실행되면 다음 URL에 접속할 수 있습니다:

- **API 루트**: http://localhost:8000
- **Swagger UI (대화형 문서)**: http://localhost:8000/docs
- **ReDoc (읽기 전용 문서)**: http://localhost:8000/redoc
- **헬스체크**: http://localhost:8000/health

---

## 🔧 환경 변수 설정

`backend/.env` 파일을 열고 실제 API 키로 수정하세요:

```env
# Gemini API (필수)
GEMINI_API_KEY=실제_gemini_api_키

# Exa API (필수)
EXA_API_KEY=실제_exa_api_키

# Email 발송 (선택)
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_password

# Slack 발송 (선택)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXX/YYY/ZZZ
```

### API 키 발급 방법

#### Gemini API
1. https://makersuite.google.com/app/apikey 접속
2. "Create API Key" 클릭
3. 생성된 키를 `.env`에 입력

#### Exa API
1. https://exa.ai 접속
2. 회원가입 후 대시보드에서 API 키 발급
3. 생성된 키를 `.env`에 입력

---

## 🧪 API 테스트

### 1. 헬스체크
```bash
curl http://localhost:8000/health
```

**응답:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### 2. 화제 종목 조회
```bash
curl "http://localhost:8000/v1/trending-stocks?count=5&limit=3"
```

### 3. Swagger UI로 테스트
1. 브라우저에서 http://localhost:8000/docs 접속
2. 각 API 엔드포인트를 클릭하여 "Try it out" 버튼으로 테스트
3. 파라미터를 입력하고 "Execute" 실행

---

## 📂 프로젝트 구조

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
├── get_trending_stocks.py       # 화제 종목 수집 모듈
├── daily_briefing_workflow.py   # 브리핑 워크플로우
├── .env                         # 환경 변수 (API 키)
├── requirements.txt             # Python 의존성
├── requirements_fastapi.txt     # FastAPI 의존성
├── start_server.bat             # Windows 실행 스크립트
├── start_server.sh              # Linux/Mac 실행 스크립트
└── SETUP_GUIDE.md               # 이 파일
```

---

## 🎯 주요 API 엔드포인트

### 화제 종목 API
- `GET /v1/trending-stocks` - 화제 종목 목록 조회
- `GET /v1/stocks/{symbol}` - 종목 상세 정보

### 브리핑 API
- `POST /v1/briefings` - 브리핑 생성
- `GET /v1/briefings` - 브리핑 목록 조회
- `GET /v1/briefings/{id}` - 브리핑 상세 조회
- `POST /v1/briefings/{id}/send` - 브리핑 발송

### 인증 API
- `POST /v1/auth/login` - 로그인

자세한 API 명세는 다음 문서를 참고하세요:
- [REST API 명세서](../REST_API_명세서.md)
- [FastAPI Router 가이드](./FASTAPI_ROUTER_가이드.md)
- [FastAPI README](./README_FASTAPI.md)

---

## 🔍 문제 해결

### 1. "ModuleNotFoundError: No module named 'fastapi'"
```bash
cd backend
pip install -r requirements_fastapi.txt
```

### 2. 포트 충돌 (8000번 포트가 이미 사용 중)
```bash
# 다른 포트로 실행
uvicorn main:app --reload --port 8080
```

### 3. CORS 에러
- `main.py`의 `allow_origins`에 프론트엔드 URL 추가
- Next.js 기본 포트 3000, 3001은 이미 허용됨

### 4. API 키 오류
- `.env` 파일에 실제 API 키가 입력되었는지 확인
- 키 앞뒤에 따옴표나 공백이 없는지 확인

---

## 📝 Next.js와 연동

FastAPI 서버가 실행된 상태에서 Next.js 프론트엔드를 실행하세요:

```bash
# 터미널 1: FastAPI 서버 (백엔드)
cd backend
python main.py

# 터미널 2: Next.js 서버 (프론트엔드)
npm run dev
```

- FastAPI: http://localhost:8000
- Next.js: http://localhost:3000

---

## 🎉 완료!

FastAPI 서버가 성공적으로 세팅되었습니다!

다음 단계:
1. ✅ FastAPI 서버 실행
2. ✅ Swagger UI에서 API 테스트
3. ✅ Next.js 프론트엔드와 연동
4. 🔜 데이터베이스 연동 (향후)
5. 🔜 JWT 인증 구현 (향후)

문제가 있으면 `backend/README_FASTAPI.md` 또는 `backend/FASTAPI_ROUTER_가이드.md`를 참고하세요!
