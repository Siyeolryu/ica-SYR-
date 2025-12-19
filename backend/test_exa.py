"""
Exa API 연결 테스트 스크립트
"""
from exa_news import search_stock_news, search_trending_stocks_news, initialize_exa_client
import os

def test_exa_connection():
    """Exa API 연결을 테스트합니다."""
    print("=" * 60)
    print("Exa API 연결 테스트")
    print("=" * 60)
    
    # API 키 확인
    api_key = os.getenv('EXA_API_KEY', '')
    
    if not api_key:
        print("\n❌ EXA_API_KEY 환경 변수가 설정되지 않았습니다.")
        print("다음 중 하나의 방법으로 설정하세요:")
        print("  1. backend/.env 파일에 EXA_API_KEY=your_key 추가")
        print("  2. 환경 변수로 설정: set EXA_API_KEY=your_key (Windows)")
        print("  3. 환경 변수로 설정: export EXA_API_KEY=your_key (Linux/Mac)")
        return False
    
    print(f"\n✅ API 키가 설정되었습니다. (길이: {len(api_key)} 문자)")
    
    try:
        # 클라이언트 초기화 테스트
        print("\n1. 클라이언트 초기화 중...")
        client_config = initialize_exa_client(api_key)
        print("   ✅ 클라이언트 초기화 성공")
        
        # 특정 종목 뉴스 검색 테스트
        print("\n2. 뉴스 검색 테스트 (AAPL)...")
        news = search_stock_news(
            'AAPL',
            'Apple Inc.',
            limit=3,
            api_key=api_key
        )
        
        if news:
            print(f"   ✅ 뉴스 {len(news)}개 검색 성공")
            for i, article in enumerate(news, 1):
                print(f"\n   {i}. {article['title']}")
                print(f"      출처: {article.get('source', 'N/A')}")
                print(f"      날짜: {article.get('published_date', 'N/A')}")
        else:
            print("   ⚠️  뉴스를 찾을 수 없습니다.")
        
        # 여러 종목 뉴스 검색 테스트
        print("\n3. 여러 종목 뉴스 검색 테스트 (AAPL, TSLA)...")
        all_news = search_trending_stocks_news(
            ['AAPL', 'TSLA'],
            limit_per_stock=2,
            api_key=api_key
        )
        
        total_news = sum(len(articles) for articles in all_news.values())
        print(f"   ✅ 총 {total_news}개 뉴스 검색 성공")
        for symbol, articles in all_news.items():
            print(f"      {symbol}: {len(articles)}개")
        
        print("\n" + "=" * 60)
        print("✅ 모든 테스트 통과!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        print("\n문제 해결 방법:")
        print("  1. API 키가 올바른지 확인하세요")
        print("  2. 인터넷 연결을 확인하세요")
        print("  3. Exa API 서비스 상태를 확인하세요")
        return False

if __name__ == "__main__":
    test_exa_connection()












