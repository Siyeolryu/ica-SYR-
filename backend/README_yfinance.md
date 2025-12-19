# yfinance를 사용한 주식 데이터 수집

yfinance 라이브러리를 사용하여 Yahoo Finance에서 주식 데이터를 가져오는 모듈입니다.

## 설치

```bash
pip install -r requirements.txt
```

## 주요 기능

### 1. 거래량 상위 종목 조회
```python
from yfinance_stocks import get_trending_stocks_by_volume

# 거래량 상위 10개 종목 가져오기
stocks = get_trending_stocks_by_volume(limit=10)

for stock in stocks:
    print(f"{stock['symbol']}: {stock['name']}")
    print(f"  가격: ${stock['price']:.2f}")
    print(f"  변동률: {stock['change_percent']:+.2f}%")
    print(f"  거래량: {stock['volume']:,}")
```

### 2. 상승률 상위 종목 조회
```python
from yfinance_stocks import get_top_gainers

# 상승률 상위 10개 종목 가져오기
gainers = get_top_gainers(limit=10)

for stock in gainers:
    print(f"{stock['symbol']}: {stock['name']} - {stock['change_percent']:+.2f}%")
```

### 3. 특정 종목 상세 정보 조회
```python
from yfinance_stocks import get_stock_data

# 애플(AAPL) 종목 정보 가져오기
apple = get_stock_data('AAPL')

if apple:
    print(f"종목명: {apple['name']}")
    print(f"현재가: ${apple['current_price']:.2f}")
    print(f"변동률: {apple['change_percent']:+.2f}%")
    print(f"시가총액: ${apple['market_cap']:,}")
    print(f"섹터: {apple['sector']}")
    print(f"최근 5일 주가:")
    for day in apple['price_history']:
        print(f"  {day['date']}: ${day['price']:.2f}")
```

### 4. 오늘의 화제 종목 TOP 1
```python
from yfinance_stocks import get_top_trending_stock

# 거래량과 상승률을 종합한 TOP 1 종목
top_stock = get_top_trending_stock()

if top_stock:
    print(f"오늘의 화제 종목: {top_stock['symbol']} ({top_stock['name']})")
    print(f"가격: ${top_stock['price']:.2f}")
    print(f"변동률: {top_stock['change_percent']:+.2f}%")
    print(f"거래량: {top_stock['volume']:,}")
    print(f"화제도 점수: {top_stock.get('score', 0):.4f}")
```

## 실행 방법

```bash
# 테스트 실행
python backend/yfinance_stocks.py
```

## yfinance vs yahooquery 비교

### yfinance 장점
- 더 많은 종목 정보 제공 (재무 정보, 뉴스 등)
- 주가 히스토리 데이터를 쉽게 가져올 수 있음
- 더 안정적인 API

### yfinance 단점
- 스크리너 기능이 제한적 (거래량/상승률 상위를 직접 구현해야 함)
- 주요 종목 리스트를 직접 관리해야 함

### yahooquery 장점
- 스크리너 기능 내장 (most_actives, day_gainers 등)
- 더 간단한 API

### yahooquery 단점
- 종목 상세 정보가 제한적
- 주가 히스토리 가져오기가 복잡할 수 있음

## 권장 사용법

- **스크리너 결과가 필요할 때**: `yahooquery` 사용 (기존 `get_trending_stocks.py`)
- **종목 상세 정보가 필요할 때**: `yfinance` 사용 (이 모듈)
- **주가 히스토리가 필요할 때**: `yfinance` 사용

## 주의사항

1. **API 호출 제한**: Yahoo Finance는 과도한 요청 시 IP 차단할 수 있습니다.
2. **시장 운영 시간**: 미국 증시 운영 시간(한국 시간 새벽)에만 실시간 데이터가 업데이트됩니다.
3. **데이터 지연**: 일부 데이터는 15-20분 지연될 수 있습니다.
4. **주요 종목 리스트**: 현재는 하드코딩된 주요 종목 리스트를 사용합니다. 실제 스크리너 결과를 가져오려면 Yahoo Finance API를 직접 호출해야 합니다.

## 향후 개선 사항

1. Yahoo Finance API를 통한 동적 스크리너 결과 가져오기
2. 캐싱 기능 추가 (같은 데이터를 여러 번 요청하지 않도록)
3. 에러 재시도 로직 추가
4. 더 많은 종목 정보 제공 (뉴스, 재무제표 등)












