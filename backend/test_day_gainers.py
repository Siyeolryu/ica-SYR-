"""
day_gainers Top1 종목 테스트
"""
from yahooquery import Screener, Ticker

print("=" * 60)
print("day_gainers Top1 종목 테스트")
print("=" * 60)

try:
    # Screener에서 day_gainers 조회
    screener = Screener()
    data = screener.get_screeners(['day_gainers'], count=1)

    if isinstance(data, dict) and 'day_gainers' in data:
        quotes = data['day_gainers']['quotes']
        if quotes:
            top_stock = quotes[0]
            symbol = top_stock.get('symbol')
            print(f"\nTop1 Symbol: {symbol}")
            print(f"Name: {top_stock.get('shortName')}")
            print(f"Price: {top_stock.get('regularMarketPrice')}")

            # Ticker로 상세 정보 조회
            print(f"\n{symbol} 상세 정보 조회 중...")
            ticker = Ticker(symbol)

            print(f"\nquotes 타입: {type(ticker.quotes)}")
            print(f"quotes 내용: {ticker.quotes}")

            if isinstance(ticker.quotes, dict):
                if symbol in ticker.quotes:
                    quote = ticker.quotes[symbol]
                    print(f"\nquote 타입: {type(quote)}")
                    print(f"quote 내용 (일부): {str(quote)[:500]}")
                else:
                    print(f"\n[ERROR] Symbol {symbol} not found in quotes")
            else:
                print(f"\n[ERROR] quotes is not a dict: {ticker.quotes}")

except Exception as e:
    print(f"\n[ERROR] 오류 발생: {str(e)}")
    import traceback
    traceback.print_exc()
