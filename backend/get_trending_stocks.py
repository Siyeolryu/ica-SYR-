"""
Yahoo Finance를 사용하여 화제 종목을 가져오는 모듈
"""
from yahooquery import Screener
from typing import List, Dict, Optional
import logging
from datetime import datetime

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_trending_stocks(
    screener_types: List[str] = ['most_actives', 'day_gainers'],
    count: int = 10
) -> Dict[str, List[Dict]]:
    """
    Yahoo Finance Screener에서 화제 종목 데이터를 수집합니다.
    
    Args:
        screener_types: 수집할 스크리너 타입 리스트
        count: 각 스크리너에서 가져올 종목 수
    
    Returns:
        스크리너 타입별 종목 리스트를 담은 딕셔너리
    """
    try:
        screener = Screener()
        screeners = screener.get_screeners(screener_types, count=count)
        
        result = {}
        for screener_type, data in screeners.items():
            if 'quotes' in data and len(data['quotes']) > 0:
                result[screener_type] = data['quotes']
                logger.info(f"{screener_type}: {len(data['quotes'])}개 종목 수집 완료")
            else:
                logger.warning(f"{screener_type}: 데이터 없음")
                result[screener_type] = []
        
        return result
    
    except Exception as e:
        logger.error(f"스크리너 데이터 수집 실패: {str(e)}")
        raise


def get_top_trending_stock(
    screener_types: List[str] = ['most_actives', 'day_gainers'],
    count: int = 5
) -> Optional[Dict]:
    """
    오늘의 화제 종목 TOP 1을 가져옵니다.
    
    Args:
        screener_types: 사용할 스크리너 타입 리스트
        count: 각 스크리너에서 가져올 종목 수
    
    Returns:
        TOP 1 종목 정보 딕셔너리 또는 None
    """
    try:
        # most_actives를 우선적으로 사용
        screener = Screener()
        
        # most_actives에서 상위 종목 가져오기
        if 'most_actives' in screener_types:
            data = screener.get_screeners('most_actives', count=count)
            if 'most_actives' in data and 'quotes' in data['most_actives']:
                quotes = data['most_actives']['quotes']
                if len(quotes) > 0:
                    top_stock = quotes[0]
                    logger.info(f"TOP 1 종목 선정: {top_stock.get('symbol')}")
                    return top_stock
        
        # most_actives가 없으면 day_gainers 사용
        if 'day_gainers' in screener_types:
            data = screener.get_screeners('day_gainers', count=count)
            if 'day_gainers' in data and 'quotes' in data['day_gainers']:
                quotes = data['day_gainers']['quotes']
                if len(quotes) > 0:
                    top_stock = quotes[0]
                    logger.info(f"TOP 1 종목 선정: {top_stock.get('symbol')}")
                    return top_stock
        
        logger.warning("화제 종목을 찾을 수 없습니다.")
        return None
    
    except Exception as e:
        logger.error(f"화제 종목 선정 실패: {str(e)}")
        return None


def format_stock_data(quote: Dict) -> Dict:
    """
    Yahoo Finance quote 데이터를 표준 형식으로 변환합니다.
    
    Args:
        quote: Yahoo Finance에서 가져온 종목 데이터
    
    Returns:
        표준화된 종목 정보 딕셔너리
    """
    return {
        'symbol': quote.get('symbol', ''),
        'name': quote.get('shortName', quote.get('longName', '')),
        'price': quote.get('regularMarketPrice', 0),
        'change': quote.get('regularMarketChange', 0),
        'change_percent': quote.get('regularMarketChangePercent', 0),
        'volume': quote.get('regularMarketVolume', 0),
        'market_cap': quote.get('marketCap', 0),
        'timestamp': datetime.now().isoformat()
    }


if __name__ == "__main__":
    # 간단한 사용 예시 (사용자가 제공한 코드 개선 버전)
    try:
        top_stock = get_top_trending_stock(count=5)
        
        if top_stock:
            formatted_stock = format_stock_data(top_stock)
            print(f"오늘의 화제 종목: {formatted_stock['symbol']} ({formatted_stock['name']})")
            print(f"현재가: ${formatted_stock['price']:.2f}")
            print(f"변동률: {formatted_stock['change_percent']:.2f}%")
            print(f"거래량: {formatted_stock['volume']:,}")
        else:
            print("화제 종목을 찾을 수 없습니다.")
    
    except Exception as e:
        logger.error(f"오류 발생: {str(e)}")












