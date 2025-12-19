# 개발일지: Google Gemini API 통합

## 작성시각
2024년 1월 15일

## 해결하고자 한 문제
서비스 기획서에 "AI 이미지 브리핑 생성"과 "뉴스 요약" 기능이 필요한데, 사용자가 제공한 Google Gemini API 코드를 프로젝트에 통합하고 싶었어요. AI를 사용해서 주식 브리핑 텍스트를 자동으로 생성하고, 뉴스 기사도 요약할 수 있게 만들었어요.

## 해결된 것

### 1. Gemini API 모듈 생성
- `backend/gemini_briefing.py` 파일을 만들었어요
- 사용자가 제공한 코드를 개선해서 프로젝트에 맞게 만들었어요
- 에러 처리와 로깅을 추가했어요

### 2. 주요 기능 3개 만들기
- **`generate_briefing_text()`**: 주식 데이터를 기반으로 브리핑 텍스트를 생성하는 함수
  - 여러 종목 정보를 받아서 제목, 요약, 각 종목별 섹션을 만들어요
  - 한국어와 영어를 지원해요
- **`summarize_news()`**: 뉴스 기사들을 요약하는 함수
  - 여러 뉴스 기사를 받아서 3-5문장으로 요약해요
- **`generate_stock_analysis()`**: 특정 종목에 대한 분석을 생성하는 함수
  - 종목 데이터를 받아서 2-3문장으로 간단한 분석을 만들어요

### 3. 환경 변수 지원
- API 키를 환경 변수에서 가져올 수 있어요
- `GEMINI_API_KEY` 환경 변수를 설정하면 자동으로 사용해요
- 코드에서 직접 API 키를 제공할 수도 있어요

### 4. 에러 처리 개선
- API 키가 없으면 친절한 에러 메시지를 보여줘요
- API 호출이 실패하면 기본 템플릿을 반환해서 서비스가 중단되지 않아요
- 모든 에러를 로그에 기록해요

### 5. requirements.txt 업데이트
- `google-genai>=0.2.0` 패키지를 추가했어요

### 6. 사용 방법 문서 작성
- `backend/README_gemini.md` 파일을 만들었어요
- 각 함수의 사용 방법과 예시를 설명했어요
- API 키 발급 방법도 안내했어요

### 7. 테스트 코드 포함
- 파일을 직접 실행하면 테스트가 실행돼요
- API 키가 없으면 안내 메시지를 보여줘요

## 해결되지 않은 것

### 1. JSON 파싱 개선
- 지금은 기본적인 파싱만 해요
- Gemini API가 반환하는 JSON을 더 정교하게 파싱해야 해요
- 실제로는 JSON 형식으로 반환되지 않을 수 있어요

### 2. 이미지 생성 기능
- 지금은 텍스트만 생성해요
- 서비스 기획서에 "AI 이미지 브리핑 생성"이 있는데, 이미지 생성 기능이 없어요
- 나중에 Gemini의 이미지 생성 기능을 활용해야 해요

### 3. 캐싱 기능
- 같은 입력에 대해 매번 API를 호출해요
- 비용을 절감하기 위해 캐싱 기능이 필요해요

### 4. Rate Limiting
- API 호출 제한을 관리하는 기능이 없어요
- 너무 많이 호출하면 차단될 수 있어요

### 5. 스트리밍 응답
- 긴 텍스트를 생성할 때 스트리밍으로 처리하는 기능이 없어요
- 사용자가 기다리는 시간이 길 수 있어요

## 향후 개발을 위한 컨텍스트

### 사용한 모델
- **gemini-2.0-flash-exp**: 빠르고 효율적인 모델
- 다른 모델도 사용 가능 (gemini-1.5-pro, gemini-1.5-flash 등)

### API 키 관리
```python
# 환경 변수에서 가져오기 (권장)
export GEMINI_API_KEY=your_api_key

# 코드에서 직접 설정
briefing = generate_briefing_text(stocks, api_key='your_key')
```

### 파일 구조
```
backend/
├── gemini_briefing.py      # Gemini API 모듈 (새로 만듦)
├── yfinance_stocks.py      # 주식 데이터 수집
├── get_trending_stocks.py  # yahooquery 사용
├── requirements.txt        # 필요한 라이브러리
└── README_gemini.md        # Gemini 사용법 (새로 만듦)
```

### 통합 워크플로우
```python
# 1. 주식 데이터 가져오기
from yfinance_stocks import get_trending_stocks_by_volume
stocks = get_trending_stocks_by_volume(limit=5)

# 2. 브리핑 텍스트 생성
from gemini_briefing import generate_briefing_text
briefing = generate_briefing_text(stocks, language='ko')

# 3. 결과 사용
print(briefing['title'])
print(briefing['summary'])
```

### 다음 단계
1. **JSON 파싱 개선** (최우선)
   - Gemini API 응답을 더 정확하게 파싱
   - JSON 형식이 아닌 경우 처리

2. **이미지 생성 기능**
   - Gemini의 이미지 생성 기능 활용
   - 브리핑 이미지 자동 생성

3. **캐싱 기능 추가**
   - 같은 입력에 대한 결과 캐싱
   - 비용 절감

4. **Rate Limiting**
   - API 호출 제한 관리
   - 재시도 로직

5. **템플릿 시스템**
   - 다양한 브리핑 템플릿 지원
   - 사용자 맞춤 형식

### 참고사항
- Gemini API는 무료 티어가 있지만 제한이 있어요
- 대량 사용 시 비용이 발생할 수 있어요
- API 호출은 네트워크 요청이므로 시간이 걸릴 수 있어요
- 에러 발생 시 기본 템플릿을 반환해서 서비스가 중단되지 않도록 했어요

### 쉽게 설명하면
Google Gemini API를 추가한 것은 마치 "똑똑한 비서를 고용한 것"과 같아요.
- **기존**: 주식 데이터만 가져와서 보여줘요
- **새로운**: 주식 데이터를 분석해서 "오늘은 애플이 2% 올랐고, 거래량이 많았어요" 같은 설명을 자동으로 만들어줘요

이제 AI가 자동으로 브리핑 텍스트를 만들어주니까, 사람이 직접 작성할 필요가 없어요!










