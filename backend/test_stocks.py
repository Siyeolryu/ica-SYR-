"""
화제 종목 가져오기 테스트 스크립트
사용자가 제공한 코드를 개선한 버전
"""
from get_trending_stocks import get_top_trending_stock, format_stock_data
import sys

def main():
    print("=" * 50)
    print("오늘의 화제 종목 조회")
    print("=" * 50)
    
    try:
        # 사용자가 제공한 코드의 개선 버전
        top_stock = get_top_trending_stock(count=5)
        
        if top_stock:
            formatted_stock = format_stock_data(top_stock)
            
            print(f"\n✅ 오늘의 화제 종목: {formatted_stock['symbol']}")
            print(f"   회사명: {formatted_stock['name']}")
            print(f"   현재가: ${formatted_stock['price']:.2f}")
            
            change_percent = formatted_stock['change_percent']
            change_sign = "+" if change_percent >= 0 else ""
            color = "🟢" if change_percent >= 0 else "🔴"
            
            print(f"   변동률: {color} {change_sign}{change_percent:.2f}%")
            print(f"   거래량: {formatted_stock['volume']:,}")
            
            if formatted_stock['market_cap'] > 0:
                market_cap_b = formatted_stock['market_cap'] / 1e9
                print(f"   시가총액: ${market_cap_b:.2f}B")
        else:
            print("\n❌ 화제 종목을 찾을 수 없습니다.")
            sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()












