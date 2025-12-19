# Exa API를 사용한 뉴스 검색

Exa API를 사용하여 주식 관련 뉴스를 검색하는 모듈입니다.

## 설치

```bash
pip install -r requirements.txt
```

## 환경 변수 설정

Exa API 키를 환경 변수로 설정해야 합니다:

**Windows:**
```bash
set EXA_API_KEY=your_api_key_here
```

**Linux/Mac:**
```bash
export EXA_API_KEY=your_api_key_here
```

**또는 backend/.env 파일에 추가:**
```
EXA_API_KEY=your_api_key_here
```

## 주요 기능

### 1. 최근 24시간 뉴스 검색 (신규 기능)

```python
from exa_news import search_stock_news_24h

# 애플(AAPL) 관련 최근 24시간 뉴스 검색
news = search_stock_news_24h('AAPL', limit=10)

for article in news:
    print(f"제목: {article['title']}")
    print(f"URL: {article['url']}")
    print(f"발행일: {article['published_date']}")
    print()
```

### 2. 특정 기간 뉴스 검색

```python
from exa_news import search_stock_news

# 애플(AAPL) 관련 뉴스 검색 (최근 7일)
news = search_stock_news(
    stock_symbol='AAPL',
    stock_name='Apple Inc.',
    limit=5,
    days_back=7
)

for article in news:
    print(f"제목: {article['title']}")
    print(f"출처: {article['source']}")
    print(f"날짜: {article['published_date']}")
    print(f"요약: {article['summary']}")
    print(f"URL: {article['url']}")
    print()
```

### 3. 여러 종목 뉴스 일괄 검색

```python
from exa_news import search_trending_stocks_news

# 여러 종목의 뉴스를 한 번에 검색
all_news = search_trending_stocks_news(
    stock_symbols=['AAPL', 'TSLA', 'MSFT'],
    limit_per_stock=3,
    days_back=7
)

for symbol, articles in all_news.items():
    print(f"\n{symbol} 관련 뉴스:")
    for article in articles:
        print(f"  - {article['title']}")
```

### 4. 뉴스 요약 (Gemini API 사용)

```python
from exa_news import search_stock_news, get_news_summary

# 뉴스 검색
news = search_stock_news('AAPL', limit=5)

# 뉴스 요약
summary = get_news_summary(news, language='ko')
print(summary)
```

## 통합 워크플로우

```python
from yfinance_stocks import get_trending_stocks_by_volume
from exa_news import search_trending_stocks_news
from gemini_briefing import generate_briefing_text

# 1. 화제 종목 가져오기
trending_stocks = get_trending_stocks_by_volume(limit=5)
symbols = [stock['symbol'] for stock in trending_stocks]

# 2. 각 종목의 뉴스 검색
all_news = search_trending_stocks_news(symbols, limit_per_stock=3)

# 3. 뉴스를 종목 데이터에 추가
for stock in trending_stocks:
    stock['news'] = all_news.get(stock['symbol'], [])

# 4. 브리핑 텍스트 생성 (뉴스 포함)
briefing = generate_briefing_text(trending_stocks, language='ko')
```

## API 키 발급 방법

1. [Exa AI](https://exa.ai/) 웹사이트에 접속
2. 회원가입 및 로그인
3. API 키 발급
4. 환경 변수에 설정

## 파라미터 설명

### search_stock_news_24h() - 신규 함수

- `ticker`: 종목 심볼 (필수, 예: 'AAPL', 'TSLA')
- `limit`: 가져올 뉴스 개수 (기본값: 10, 최대: 100)
- `api_key`: Exa API 키 (선택, 환경 변수에서 가져옴)

**반환값:**
```python
[
    {
        'title': '뉴스 제목',
        'url': '뉴스 URL',
        'published_date': '2025-12-19T10:30:00.000Z',
        'source': 'example.com',
        'summary': '뉴스 요약...'
    }
]
```

### search_stock_news()

- `stock_symbol`: 종목 심볼 (필수)
- `stock_name`: 종목명 (선택, 검색 정확도 향상)
- `limit`: 가져올 뉴스 개수 (기본값: 5, 최대: 100)
- `days_back`: 며칠 전까지의 뉴스 검색 (기본값: 7)
- `api_key`: Exa API 키 (선택, 환경 변수에서 가져옴)

### search_trending_stocks_news()

- `stock_symbols`: 종목 심볼 리스트 (필수)
- `limit_per_stock`: 종목당 가져올 뉴스 개수 (기본값: 3)
- `days_back`: 며칠 전까지의 뉴스 검색 (기본값: 7)
- `api_key`: Exa API 키 (선택)

## 에러 처리

API 키가 없거나 잘못된 경우:
```python
try:
    news = search_stock_news('AAPL')
except ValueError as e:
    print(f"API 키 오류: {e}")
except Exception as e:
    print(f"기타 오류: {e}")
```

## 비용 고려사항

- Exa API는 무료 티어가 있지만 제한이 있습니다
- 대량 사용 시 비용이 발생할 수 있습니다
- 프로덕션 환경에서는 Rate Limiting을 구현하는 것을 권장합니다

## 향후 개선 사항

1. **캐싱**: 같은 종목의 뉴스를 여러 번 검색하지 않도록 캐싱
2. **에러 재시도**: API 호출 실패 시 자동 재시도
3. **뉴스 필터링**: 관련성 높은 뉴스만 필터링
4. **뉴스 클러스터링**: 비슷한 뉴스를 그룹화
5. **감성 분석**: 뉴스의 긍정/부정 감성 분석

## 참고사항

- Exa API는 neural search를 사용하여 관련성 높은 뉴스를 찾습니다
- `use_autoprompt=True` 옵션으로 검색 쿼리를 자동으로 개선합니다
- 날짜 범위를 설정하여 최신 뉴스만 가져올 수 있습니다
- 뉴스 요약은 Gemini API를 사용합니다 (선택적)












