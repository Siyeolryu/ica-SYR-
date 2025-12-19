"""
FRMI 종목 상세 정보 테스트
"""
from yahooquery import Ticker

symbol = "FRMI"
print(f"=" * 60)
print(f"{symbol} 상세 정보 테스트")
print(f"=" * 60)

try:
    ticker = Ticker(symbol)

    print(f"\n1. quotes 타입: {type(ticker.quotes)}")
    print(f"   quotes 키: {list(ticker.quotes.keys()) if isinstance(ticker.quotes, dict) else 'N/A'}")

    print(f"\n2. summary_detail 타입: {type(ticker.summary_detail)}")
    print(f"   summary_detail 내용: {ticker.summary_detail}")

    print(f"\n3. summary_profile 타입: {type(ticker.summary_profile)}")
    print(f"   summary_profile 내용: {ticker.summary_profile}")

    print(f"\n4. financial_data 타입: {type(ticker.financial_data)}")
    print(f"   financial_data 내용: {ticker.financial_data}")

except Exception as e:
    print(f"\n[ERROR] 오류 발생: {str(e)}")
    import traceback
    traceback.print_exc()
