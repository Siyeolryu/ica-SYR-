# Google Gemini API를 사용한 브리핑 생성

Google Gemini API를 사용하여 주식 브리핑 텍스트와 뉴스 요약을 생성하는 모듈입니다.

## 설치

```bash
pip install -r requirements.txt
```

## 환경 변수 설정

Gemini API 키를 환경 변수로 설정해야 합니다:

**Windows:**
```bash
set GEMINI_API_KEY=your_api_key_here
```

**Linux/Mac:**
```bash
export GEMINI_API_KEY=your_api_key_here
```

**Python 코드에서 직접 설정:**
```python
import os
os.environ['GEMINI_API_KEY'] = 'your_api_key_here'
```

## 주요 기능

### 1. 브리핑 텍스트 생성

```python
from gemini_briefing import generate_briefing_text

stocks = [
    {
        'symbol': 'AAPL',
        'name': 'Apple Inc.',
        'price': 185.50,
        'change_percent': 2.35,
        'volume': 45234567,
    },
    {
        'symbol': 'TSLA',
        'name': 'Tesla, Inc.',
        'price': 245.30,
        'change_percent': 5.12,
        'volume': 38923456,
    },
]

# 한국어 브리핑 생성
briefing = generate_briefing_text(stocks, language='ko')

print(briefing['title'])
print(briefing['summary'])
for section in briefing['sections']:
    print(f"\n{section['title']}")
    print(section['content'])
```

### 2. 뉴스 요약

```python
from gemini_briefing import summarize_news

news_articles = [
    {
        'title': '애플, 새로운 제품 발표',
        'content': '애플이 오늘 새로운 아이폰을 발표했습니다...',
    },
    {
        'title': '테슬라 주가 상승',
        'content': '테슬라 주가가 5% 상승했습니다...',
    },
]

# 뉴스 요약
summary = summarize_news(news_articles, language='ko')
print(summary)
```

### 3. 종목 분석 생성

```python
from gemini_briefing import generate_stock_analysis

stock_data = {
    'name': 'Apple Inc.',
    'price': 185.50,
    'change_percent': 2.35,
    'volume': 45234567,
    'market_cap': 2850000000000,
    'sector': 'Technology',
}

# 종목 분석
analysis = generate_stock_analysis('AAPL', stock_data, language='ko')
print(analysis)
```

## 사용 예시

### 전체 브리핑 생성 워크플로우

```python
from yfinance_stocks import get_trending_stocks_by_volume
from gemini_briefing import generate_briefing_text

# 1. 화제 종목 가져오기
trending_stocks = get_trending_stocks_by_volume(limit=5)

# 2. 브리핑 텍스트 생성
briefing = generate_briefing_text(trending_stocks, language='ko')

# 3. 결과 출력
print(f"제목: {briefing['title']}")
print(f"\n요약: {briefing['summary']}")
print("\n종목별 상세:")
for section in briefing['sections']:
    print(f"\n{section['title']}")
    print(section['content'])
```

## API 키 발급 방법

1. [Google AI Studio](https://makersuite.google.com/app/apikey)에 접속
2. "Create API Key" 클릭
3. API 키 복사
4. 환경 변수에 설정

## 모델 정보

현재 사용 모델: `gemini-2.0-flash-exp`

다른 모델도 사용 가능:
- `gemini-1.5-pro`: 더 강력하지만 느림
- `gemini-1.5-flash`: 빠르고 효율적

모델 변경 방법:
```python
response = client.models.generate_content(
    model="gemini-1.5-pro",  # 모델 변경
    contents=prompt,
)
```

## 에러 처리

API 키가 없거나 잘못된 경우:
```python
try:
    briefing = generate_briefing_text(stocks)
except ValueError as e:
    print(f"API 키 오류: {e}")
except Exception as e:
    print(f"기타 오류: {e}")
```

## 비용 고려사항

- Gemini API는 무료 티어가 있지만 제한이 있습니다
- 대량 사용 시 비용이 발생할 수 있습니다
- 프로덕션 환경에서는 Rate Limiting을 구현하는 것을 권장합니다

## 향후 개선 사항

1. **JSON 파싱 개선**: 현재는 기본 파싱만 사용, 더 정교한 JSON 파싱 필요
2. **캐싱**: 같은 입력에 대한 결과를 캐싱하여 비용 절감
3. **스트리밍 응답**: 긴 텍스트 생성 시 스트리밍으로 처리
4. **템플릿 시스템**: 다양한 브리핑 템플릿 지원
5. **이미지 생성**: Gemini의 이미지 생성 기능 활용

## 참고사항

- API 호출은 네트워크 요청이므로 시간이 걸릴 수 있습니다
- 에러 발생 시 기본 템플릿을 반환하여 서비스가 중단되지 않도록 했습니다
- 언어 설정은 'ko' (한국어) 또는 'en' (영어)를 지원합니다




















