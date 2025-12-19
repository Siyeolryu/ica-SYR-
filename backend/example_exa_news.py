"""
Exa API를 사용한 뉴스 수집 예제

요구사항:
1. Exa API를 사용해서 주식 관련 뉴스 검색
2. 검색 키워드: "{ticker} stock news"
3. 최근 24시간 뉴스만 검색
4. 결과에서 제목, URL, 발행일 추출
5. 에러 처리 포함
"""

from exa_news import search_stock_news_24h
import os


def main():
    """Exa API를 사용한 24시간 뉴스 검색 예제"""

    print("=" * 70)
    print("Exa API 24시간 뉴스 수집 서비스")
    print("=" * 70)

    # API 키 확인
    api_key = os.getenv('EXA_API_KEY', '')

    if not api_key:
        print("\n⚠️  EXA_API_KEY 환경 변수가 설정되지 않았습니다.")
        print("\n환경 변수 설정 방법:")
        print("  Windows:   set EXA_API_KEY=your_api_key")
        print("  Linux/Mac: export EXA_API_KEY=your_api_key")
        print("\n또는 backend/.env 파일에 다음 내용 추가:")
        print("  EXA_API_KEY=your_api_key")
        return

    # 테스트할 종목들
    tickers = ['AAPL', 'TSLA', 'NVDA']

    print(f"\n검색할 종목: {', '.join(tickers)}")
    print("검색 범위: 최근 24시간\n")

    # 각 종목별 뉴스 검색
    for ticker in tickers:
        print(f"\n{'='*70}")
        print(f"[{ticker}] 최근 24시간 뉴스 검색 중...")
        print('='*70)

        try:
            # 최근 24시간 뉴스 검색
            news = search_stock_news_24h(ticker, limit=5, api_key=api_key)

            if news:
                print(f"\n✅ {len(news)}개의 뉴스를 찾았습니다.\n")

                for i, article in enumerate(news, 1):
                    print(f"{i}. 제목: {article['title']}")
                    print(f"   URL: {article['url']}")
                    print(f"   발행일: {article['published_date']}")
                    print(f"   출처: {article.get('source', 'N/A')}")
                    print()
            else:
                print(f"\n⚠️  {ticker}의 최근 24시간 내 뉴스가 없습니다.")

        except ValueError as e:
            print(f"\n❌ API 키 오류: {e}")
            break
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")

    print("\n" + "="*70)
    print("검색 완료!")
    print("="*70)


if __name__ == "__main__":
    main()
