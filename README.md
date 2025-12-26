# 당신이 잠든 사이 (While You Were Sleeping)

미국주식 투자하는 한국인 직장인을 위한 완전 자동화된 데일리 브리핑 서비스입니다.

## 서비스 개요

"당신이 잠든 사이"는 한국 시간 기준 매일 아침 7시, Yahoo Finance의 거래량과 상승률 데이터를 분석하여 가장 활발하게 움직인 상위 5개 화제 종목을 자동으로 선정하고, 각 종목의 핵심 정보와 관련 뉴스를 수집하여 AI가 생성한 이미지 브리핑으로 제공하는 완전 자동화 서비스입니다.

**핵심 차별점**:
- 복잡한 분석 없이 "가장 활발한 종목" 자동 선정
- Chatless (입력 없이 자동) - 사용자의 개입 없이 완전 자동으로 작동
- 슬랙으로 자동 발송되는 이미지 브리핑

자세한 내용은 [서비스 기획서](./docs/01_기획/서비스기획서_당신이잠든사이.md)를 참고하세요.

## 📚 문서 구조

프로젝트 문서가 체계적으로 정리되어 있습니다:

- **📁 [docs/](./docs/)** - 모든 프로젝트 문서
  - **[01_기획/](./docs/01_기획/)** - 서비스 기획 및 설계
  - **[02_개발가이드/](./docs/02_개발가이드/)** - 개발 및 실행 가이드
  - **[03_설정및연동/](./docs/03_설정및연동/)** - 환경 설정 및 외부 연동
  - **[04_보고서/](./docs/04_보고서/)** - 테스트 및 점검 보고서

- **📁 [개발일지/](./개발일지/)** - 시간순 개발 기록 (YYYY/MM/DD 구조)

자세한 내용은 **[프로젝트_구조.md](./프로젝트_구조.md)**를 참고하세요.

## 기술 스택

### 프론트엔드
- **Framework**: Next.js 14
- **Styling**: TailwindCSS
- **Language**: TypeScript

### 백엔드
- **Language**: Python 3.x
- **스케줄러**: APScheduler
- **API**: 
  - Yahoo Finance (yahooquery) - 종목 데이터 수집
  - Exa API - 뉴스 수집
  - Google Gemini API - 브리핑 생성 및 이미지 생성
- **이미지 처리**: Pillow

## 🚀 빠른 시작

### ⚡ 서버 시작 (가장 빠른 방법)

**Windows에서 한 번에 시작:**
```powershell
.\start_dev_servers.bat
```

또는 PowerShell에서:
```powershell
.\start_dev_servers.ps1
```

이 스크립트가 프론트엔드와 백엔드 서버를 자동으로 시작합니다!

**수동으로 시작하려면:**
- 프론트엔드: `npm run dev` (http://localhost:3000)
- 백엔드: `cd backend && python main.py` (http://localhost:8000)

자세한 내용은 👉 **[서버_시작_가이드.md](./서버_시작_가이드.md)**

처음 시작하시나요? 👉 **[QUICK_START.md](./docs/02_개발가이드/QUICK_START.md)** (5분 안에 시작!)

더 자세한 내용은 👉 **[실행가이드.md](./docs/02_개발가이드/실행가이드.md)**

## 📖 주요 문서

| 문서 | 설명 |
|------|------|
| [QUICK_START](./docs/02_개발가이드/QUICK_START.md) | 5분 안에 시작하기 |
| [실행가이드](./docs/02_개발가이드/실행가이드.md) | 상세한 실행 방법 |
| [REST_API_명세서](./docs/02_개발가이드/REST_API_명세서.md) | 전체 API 엔드포인트 |
| [프로젝트_구조](./프로젝트_구조.md) | 프로젝트 디렉토리 구조 |
| [MCP_연동_완료_보고서](./docs/03_설정및연동/MCP_연동_완료_보고서.md) | Claude Desktop MCP 연동 |
| [Claude_Pro_인증_완료_보고서](./docs/03_설정및연동/Claude_Pro_인증_완료_보고서.md) | Claude Code 설정 |

## 시작하기

### 설치

```bash
npm install
```

### 개발 서버 실행

```bash
npm run dev
```

브라우저에서 [http://localhost:3000](http://localhost:3000)을 열어 확인하세요.

### 빌드

```bash
npm run build
npm start
```

## 프로젝트 구조

```
├── backend/                    # 백엔드 (Python)
│   ├── get_trending_stocks.py  # 화제 종목 수집
│   ├── exa_news.py            # 뉴스 수집 및 요약
│   ├── gemini_briefing.py     # 브리핑 생성 (텍스트 + 이미지)
│   ├── send_briefing.py       # 슬랙 발송
│   ├── daily_briefing_workflow.py  # 통합 워크플로우
│   ├── scheduler.py           # 스케줄러 (매일 7시 실행)
│   ├── requirements.txt       # Python 의존성
│   └── output/                # 생성된 브리핑 저장
├── components/                # 프론트엔드 컴포넌트
│   ├── Layout.tsx
│   ├── StockCard.tsx
│   ├── BriefingCard.tsx
│   └── Button.tsx
├── pages/                     # Next.js 페이지
│   ├── _app.tsx
│   ├── index.tsx              # 메인 대시보드
│   └── briefings/[id].tsx     # 브리핑 상세
├── 서비스기획서_당신이잠든사이.md  # 서비스 기획서
└── 개발일지/                   # 개발 일지
```

## 백엔드 실행 방법

### 1. Python 환경 설정
```bash
cd backend
pip install -r requirements.txt
```

### 2. 환경 변수 설정
`backend/.env` 파일 생성:
```env
GEMINI_API_KEY=your_gemini_api_key
EXA_API_KEY=your_exa_api_key
SLACK_WEBHOOK_URL=your_slack_webhook_url
```

### 3. 스케줄러 실행
```bash
# 매일 아침 7시 자동 실행
python backend/scheduler.py

# 즉시 실행 (테스트용)
python backend/scheduler.py --run-once
```

## 주요 기능

### 백엔드 (자동화 워크플로우)
1. **자동 화제 종목 선정** - Yahoo Finance API를 통한 거래량/상승률 기반 상위 5개 종목 선정
2. **종목 정보 수집 및 정리** - 선정된 종목의 기본 정보 수집
3. **뉴스 수집 및 요약** - Exa API로 뉴스 수집, Gemini API로 요약
4. **AI 이미지 브리핑 생성** - Gemini API로 브리핑 텍스트 및 이미지 생성
5. **자동 실행 및 슬랙 발송** - 한국 시간 기준 매일 아침 7시 자동 실행 및 슬랙 발송

### 프론트엔드 (대시보드)
- 📊 오늘의 화제 종목 조회
- 📝 브리핑 생성 및 관리
- 📱 반응형 디자인 (모바일 지원)
- 🌙 다크 모드 기본 적용

## 디자인 특징

- 다크 테마 기본 적용
- 주식 상승/하락 색상 (녹색/빨간색)
- 카드 기반 레이아웃
- 모바일 반응형 디자인

