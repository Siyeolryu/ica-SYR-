"""
Exa API를 사용하여 주식 관련 뉴스를 검색하는 모듈
"""
import requests
from typing import List, Dict, Optional
import logging
import os
from pathlib import Path
from datetime import datetime, timedelta

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# .env 파일에서 API 키 로드
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        logger.info(".env 파일에서 API 키를 로드했습니다.")
except ImportError:
    logger.warning("python-dotenv가 설치되지 않았습니다. 환경 변수에서만 API 키를 가져옵니다.")

# 환경 변수에서 API 키 가져오기
EXA_API_KEY = os.getenv('EXA_API_KEY', '')
EXA_API_BASE_URL = 'https://api.exa.ai'


def initialize_exa_client(api_key: Optional[str] = None) -> Dict[str, str]:
    """
    Exa API 클라이언트 설정을 반환합니다.
    
    Args:
        api_key: Exa API 키 (없으면 환경 변수에서 가져옴)
    
    Returns:
        API 설정 딕셔너리
    """
    api_key = api_key or EXA_API_KEY
    
    if not api_key:
        raise ValueError(
            "Exa API 키가 필요합니다. "
            "환경 변수 EXA_API_KEY를 설정하거나 api_key 파라미터를 제공하세요."
        )
    
    return {
        'api_key': api_key,
        'base_url': EXA_API_BASE_URL,
        'headers': {
            'x-api-key': api_key,
            'Content-Type': 'application/json',
        }
    }


def search_stock_news(
    stock_symbol: str,
    stock_name: Optional[str] = None,
    limit: int = 5,
    days_back: int = 7,
    api_key: Optional[str] = None
) -> List[Dict]:
    """
    특정 종목에 대한 뉴스를 검색합니다.

    Args:
        stock_symbol: 종목 심볼 (예: 'AAPL')
        stock_name: 종목명 (선택, 검색 정확도 향상)
        limit: 가져올 뉴스 개수 (기본값: 5)
        days_back: 며칠 전까지의 뉴스 검색 (기본값: 7)
        api_key: Exa API 키 (선택)

    Returns:
        뉴스 기사 리스트 (title, url, published_date 포함)
    """
    try:
        client_config = initialize_exa_client(api_key)

        # 검색 쿼리 생성
        query = f"{stock_symbol} stock news"

        # 날짜 범위 설정 (ISO 8601 형식)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)

        # Exa API 요청
        url = f"{client_config['base_url']}/search"

        payload = {
            'query': query,
            'num_results': min(limit, 100),  # API 제한: 최대 100
            'start_published_date': start_date.strftime('%Y-%m-%d'),
            'end_published_date': end_date.strftime('%Y-%m-%d'),
            'type': 'auto',  # auto, neural, keyword 중 선택
            'use_autoprompt': True,  # 자동 프롬프트 개선
        }

        logger.info(f"Exa API 요청: {query} (최근 {days_back}일)")

        response = requests.post(
            url,
            headers=client_config['headers'],
            json=payload,
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

        # 결과 파싱
        news_articles = []
        if 'results' in data:
            for result in data['results']:
                article = {
                    'title': result.get('title', '제목 없음'),
                    'url': result.get('url', ''),
                    'published_date': result.get('publishedDate', ''),
                    'author': result.get('author', ''),
                    'summary': result.get('text', '')[:500] if 'text' in result else '',
                    'source': result.get('url', '').split('/')[2] if result.get('url') else '',
                }
                news_articles.append(article)

        logger.info(f"{stock_symbol} 관련 뉴스 {len(news_articles)}개 수집 완료")
        return news_articles

    except requests.exceptions.HTTPError as e:
        logger.error(f"Exa API HTTP 오류 ({e.response.status_code}): {e.response.text if e.response else str(e)}")
        return []
    except requests.exceptions.Timeout:
        logger.error("Exa API 요청 시간 초과 (30초)")
        return []
    except requests.exceptions.RequestException as e:
        logger.error(f"Exa API 네트워크 오류: {str(e)}")
        return []
    except ValueError as e:
        logger.error(f"API 키 오류: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"뉴스 검색 중 예상치 못한 오류: {str(e)}", exc_info=True)
        return []


def search_stock_news_24h(
    ticker: str,
    limit: int = 10,
    api_key: Optional[str] = None
) -> List[Dict]:
    """
    특정 종목의 최근 24시간 뉴스를 검색합니다.

    Args:
        ticker: 종목 심볼 (예: 'AAPL', 'TSLA')
        limit: 가져올 뉴스 개수 (기본값: 10, 최대: 100)
        api_key: Exa API 키 (선택)

    Returns:
        뉴스 기사 리스트 [{'title': str, 'url': str, 'published_date': str}, ...]

    Raises:
        ValueError: API 키가 없을 경우

    Example:
        >>> news = search_stock_news_24h('AAPL', limit=5)
        >>> for article in news:
        ...     print(f"{article['title']} - {article['url']}")
    """
    return search_stock_news(
        stock_symbol=ticker,
        limit=limit,
        days_back=1,  # 최근 24시간
        api_key=api_key
    )


def search_trending_stocks_news(
    stock_symbols: List[str],
    limit_per_stock: int = 3,
    days_back: int = 7,
    api_key: Optional[str] = None
) -> Dict[str, List[Dict]]:
    """
    여러 종목에 대한 뉴스를 한 번에 검색합니다.

    Args:
        stock_symbols: 종목 심볼 리스트
        limit_per_stock: 종목당 가져올 뉴스 개수 (기본값: 3)
        days_back: 며칠 전까지의 뉴스 검색 (기본값: 7)
        api_key: Exa API 키 (선택)

    Returns:
        종목별 뉴스 딕셔너리 {symbol: [news_articles]}
    """
    try:
        client_config = initialize_exa_client(api_key)

        all_news = {}

        for symbol in stock_symbols:
            news = search_stock_news(
                symbol,
                limit=limit_per_stock,
                days_back=days_back,
                api_key=api_key
            )
            all_news[symbol] = news

        logger.info(f"총 {len(stock_symbols)}개 종목의 뉴스 수집 완료")
        return all_news

    except Exception as e:
        logger.error(f"뉴스 일괄 검색 실패: {str(e)}")
        return {symbol: [] for symbol in stock_symbols}


def get_news_summary(
    news_articles: List[Dict],
    language: str = 'ko'
) -> str:
    """
    뉴스 기사들을 요약합니다.
    (Gemini API를 사용하여 요약)
    
    Args:
        news_articles: 뉴스 기사 리스트
        language: 언어 ('ko' 또는 'en')
    
    Returns:
        요약된 텍스트
    """
    try:
        from gemini_briefing import summarize_news
        return summarize_news(news_articles, language=language)
    except ImportError:
        logger.warning("Gemini API가 없어서 기본 요약을 반환합니다.")
        # 기본 요약
        if not news_articles:
            return "뉴스가 없습니다."
        
        titles = [article.get('title', '') for article in news_articles[:3]]
        return f"주요 뉴스: {', '.join(titles)}"


if __name__ == "__main__":
    # 테스트용
    print("=" * 60)
    print("Exa API 뉴스 검색 테스트")
    print("=" * 60)

    # API 키 확인
    api_key = os.getenv('EXA_API_KEY', '')

    if not api_key:
        print("\n⚠️  EXA_API_KEY 환경 변수가 설정되지 않았습니다.")
        print("다음 명령어로 설정하세요:")
        print("  Windows: set EXA_API_KEY=your_api_key")
        print("  Linux/Mac: export EXA_API_KEY=your_api_key")
        print("\n또는 backend/.env 파일에 EXA_API_KEY=your_api_key 추가")
    else:
        try:
            # 24시간 뉴스 검색 테스트 (요구사항)
            print("\n1. 최근 24시간 뉴스 검색 (AAPL):")
            news_24h = search_stock_news_24h('AAPL', limit=5, api_key=api_key)

            if news_24h:
                for i, article in enumerate(news_24h, 1):
                    print(f"\n  {i}. 제목: {article['title']}")
                    print(f"     URL: {article['url']}")
                    print(f"     발행일: {article['published_date']}")
                    print(f"     출처: {article.get('source', 'N/A')}")
            else:
                print("  최근 24시간 내 뉴스가 없습니다.")

            # 7일 뉴스 검색 테스트
            print("\n2. 최근 7일 뉴스 검색 (TSLA):")
            news_7d = search_stock_news('TSLA', limit=3, days_back=7, api_key=api_key)

            if news_7d:
                for i, article in enumerate(news_7d, 1):
                    print(f"\n  {i}. {article['title']}")
                    print(f"     출처: {article.get('source', 'N/A')}")
                    print(f"     날짜: {article.get('published_date', 'N/A')}")
                    print(f"     URL: {article.get('url', 'N/A')}")
            else:
                print("  뉴스를 찾을 수 없습니다.")

            # 여러 종목 뉴스 검색 테스트
            print("\n3. 여러 종목 뉴스 검색 (AAPL, TSLA, NVDA):")
            all_news = search_trending_stocks_news(
                ['AAPL', 'TSLA', 'NVDA'],
                limit_per_stock=2,
                days_back=3,
                api_key=api_key
            )

            for symbol, articles in all_news.items():
                print(f"\n  {symbol}: {len(articles)}개 뉴스")
                for article in articles:
                    print(f"    - {article['title']}")

        except Exception as e:
            print(f"\n❌ 오류 발생: {str(e)}")
            import traceback
            traceback.print_exc()
            print("\nAPI 키를 확인하고 다시 시도하세요.")












