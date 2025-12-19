#!/usr/bin/env python3
"""
MCP 서버 테스트 스크립트
"""
import asyncio
import sys
import os

# 상위 디렉토리를 path에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


async def test_stocks_server():
    """Stocks MCP 서버 테스트"""
    print("=" * 50)
    print("Stocks MCP 서버 테스트")
    print("=" * 50)

    try:
        from get_trending_stocks import get_top_trending_stock, format_stock_data

        print("\n[1/3] TOP 1 화제 종목 조회 중...")
        top_stock = get_top_trending_stock(count=5)

        if top_stock:
            stock = format_stock_data(top_stock)
            print(f"\n✅ 성공!")
            print(f"  종목: {stock['symbol']} - {stock['name']}")
            print(f"  현재가: ${stock['price']:.2f}")
            print(f"  변동률: {stock['change_percent']:.2f}%")
            print(f"  거래량: {stock['volume']:,}")
        else:
            print("\n❌ 화제 종목을 찾을 수 없습니다")

        print("\n[2/3] 여러 화제 종목 조회 중...")
        from get_trending_stocks import get_trending_stocks
        stocks_data = get_trending_stocks(
            screener_types=['most_actives'],
            count=3
        )

        if stocks_data and 'most_actives' in stocks_data:
            print(f"\n✅ 성공! {len(stocks_data['most_actives'])}개 종목 조회")
            for quote in stocks_data['most_actives'][:3]:
                stock = format_stock_data(quote)
                print(f"  - {stock['symbol']}: ${stock['price']:.2f} ({stock['change_percent']:.2f}%)")

        print("\n[3/3] 특정 종목 정보 조회 중...")
        from yahooquery import Ticker
        ticker = Ticker("AAPL")
        quotes = ticker.quotes

        if "AAPL" in quotes:
            quote = quotes["AAPL"]
            print(f"\n✅ 성공!")
            print(f"  종목: AAPL - {quote.get('shortName', '')}")
            print(f"  현재가: ${quote.get('regularMarketPrice', 0):.2f}")

        print("\n" + "=" * 50)
        print("✅ Stocks MCP 서버 모든 테스트 통과!")
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()


async def test_briefing_server():
    """Briefing MCP 서버 테스트"""
    print("\n\n" + "=" * 50)
    print("Briefing MCP 서버 테스트")
    print("=" * 50)

    try:
        print("\n[1/2] 뉴스 수집 테스트 중...")
        print("  (Exa API 키가 필요합니다)")

        # Exa API 키 확인
        from dotenv import load_dotenv
        load_dotenv()

        exa_key = os.getenv('EXA_API_KEY')
        if not exa_key or exa_key == 'your_exa_api_key_here':
            print("  ⚠️ Exa API 키가 설정되지 않았습니다")
            print("  .env 파일에 EXA_API_KEY를 설정하세요")
        else:
            try:
                from exa_news import search_and_summarize_news
                news_result = search_and_summarize_news(
                    company_name="Apple",
                    num_results=2
                )
                if news_result:
                    print("  ✅ 뉴스 수집 성공!")
                    if news_result.get('summary'):
                        print(f"  요약: {news_result['summary'][:100]}...")
            except Exception as e:
                print(f"  ❌ 뉴스 수집 실패: {str(e)}")

        print("\n[2/2] Gemini API 테스트 중...")
        print("  (Gemini API 키가 필요합니다)")

        gemini_key = os.getenv('GEMINI_API_KEY')
        if not gemini_key or gemini_key == 'your_gemini_api_key_here':
            print("  ⚠️ Gemini API 키가 설정되지 않았습니다")
            print("  .env 파일에 GEMINI_API_KEY를 설정하세요")
        else:
            try:
                from gemini_briefing import analyze_why_trending
                stock_data = {
                    'symbol': 'AAPL',
                    'shortName': 'Apple Inc.',
                    'regularMarketChangePercent': 2.5
                }
                news = "Apple announces new product line..."
                analysis = analyze_why_trending(stock_data, news)
                if analysis:
                    print("  ✅ AI 분석 성공!")
                    print(f"  분석: {analysis[:100]}...")
            except Exception as e:
                print(f"  ❌ AI 분석 실패: {str(e)}")

        print("\n" + "=" * 50)
        print("✅ Briefing MCP 서버 테스트 완료!")
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()


async def main():
    """메인 테스트 실행"""
    print("\n" + "=" * 50)
    print("당신이 잠든 사이 - MCP 서버 테스트")
    print("=" * 50)

    # Stocks 서버 테스트
    await test_stocks_server()

    # Briefing 서버 테스트
    await test_briefing_server()

    print("\n\n" + "=" * 50)
    print("모든 테스트 완료!")
    print("=" * 50)
    print("\n다음 단계:")
    print("1. Claude Desktop에 MCP 서버 설정")
    print("2. claude_desktop_config.json 파일 수정")
    print("3. Claude Desktop 재시작")
    print("\n자세한 내용은 README_MCP.md를 참고하세요")


if __name__ == "__main__":
    asyncio.run(main())
