# 백엔드 모듈

Yahoo Finance를 사용하여 화제 종목을 가져오는 Python 모듈입니다.

## 설치

```bash
pip install -r requirements.txt
```

## 사용 방법

### 기본 사용 (사용자가 제공한 코드 개선 버전)

```python
from get_trending_stocks import get_top_trending_stock, format_stock_data

# TOP 1 종목 가져오기
top_stock = get_top_trending_stock(count=5)

if top_stock:
    formatted = format_stock_data(top_stock)
    print(f"오늘의 화제 종목: {formatted['symbol']}")
```

### 여러 종목 가져오기

```python
from get_trending_stocks import get_trending_stocks

# 거래량 상위와 상승률 상위 종목 가져오기
data = get_trending_stocks(
    screener_types=['most_actives', 'day_gainers'],
    count=10
)

for screener_type, quotes in data.items():
    print(f"\n{screener_type}:")
    for quote in quotes:
        print(f"  - {quote['symbol']}: {quote.get('shortName', 'N/A')}")
```

## 함수 설명

### `get_top_trending_stock()`
오늘의 화제 종목 TOP 1을 가져옵니다.

**파라미터:**
- `screener_types`: 사용할 스크리너 타입 리스트 (기본값: ['most_actives', 'day_gainers'])
- `count`: 각 스크리너에서 가져올 종목 수 (기본값: 5)

**반환값:**
- 종목 정보 딕셔너리 또는 None

### `get_trending_stocks()`
여러 스크리너에서 종목 데이터를 수집합니다.

**파라미터:**
- `screener_types`: 수집할 스크리너 타입 리스트
- `count`: 각 스크리너에서 가져올 종목 수

**반환값:**
- 스크리너 타입별 종목 리스트를 담은 딕셔너리

### `format_stock_data()`
Yahoo Finance 데이터를 표준 형식으로 변환합니다.

**파라미터:**
- `quote`: Yahoo Finance에서 가져온 종목 데이터

**반환값:**
- 표준화된 종목 정보 딕셔너리

## 에러 처리

모든 함수는 예외가 발생할 수 있으므로 try-except로 감싸서 사용하는 것을 권장합니다.

```python
try:
    top_stock = get_top_trending_stock()
    if top_stock:
        print(f"종목: {top_stock['symbol']}")
except Exception as e:
    print(f"오류 발생: {str(e)}")
```




















