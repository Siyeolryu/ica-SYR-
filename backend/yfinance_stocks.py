"""
yfinance를 사용하여 Yahoo Finance에서 주식 데이터를 가져오는 모듈
"""
import yfinance as yf
from typing import List, Dict, Optional
import logging
from datetime import datetime, timedelta
import pandas as pd

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_trending_stocks_by_volume(limit: int = 10) -> List[Dict]:
    """
    거래량 상위 종목을 가져옵니다.
    
    Args:
        limit: 가져올 종목 수
    
    Returns:
        종목 정보 리스트
    """
    try:
        # Yahoo Finance의 거래량 상위 종목 티커 리스트 (주요 종목들)
        # 실제로는 Yahoo Finance API를 통해 동적으로 가져와야 하지만,
        # yfinance는 스크리너 기능이 제한적이므로 주요 종목들을 직접 조회합니다.
        
        # 주요 미국 주식 티커 리스트
        major_tickers = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'BRK-B',
            'V', 'UNH', 'XOM', 'JNJ', 'JPM', 'WMT', 'PG', 'MA', 'HD', 'CVX',
            'ABBV', 'PFE', 'AVGO', 'COST', 'MRK', 'PEP', 'TMO', 'CSCO', 'ABT',
            'ACN', 'ADBE', 'NFLX', 'CMCSA', 'NKE', 'DIS', 'VZ', 'INTC', 'TXN',
            'QCOM', 'AMD', 'CRM', 'HON', 'LIN', 'AMAT', 'INTU', 'AMGN', 'BKNG'
        ]
        
        stocks_data = []
        
        # 각 티커의 정보를 가져옴
        for ticker_symbol in major_tickers[:limit * 2]:  # 여유있게 가져와서 필터링
            try:
                ticker = yf.Ticker(ticker_symbol)
                info = ticker.info
                
                # 현재 시장 데이터 가져오기
                hist = ticker.history(period='1d', interval='1m')
                
                if hist.empty:
                    continue
                
                current_price = hist['Close'].iloc[-1]
                previous_close = info.get('previousClose', current_price)
                volume = hist['Volume'].iloc[-1] if 'Volume' in hist.columns else info.get('volume', 0)
                
                change = current_price - previous_close
                change_percent = (change / previous_close * 100) if previous_close > 0 else 0
                
                stock_data = {
                    'symbol': ticker_symbol,
                    'name': info.get('longName', info.get('shortName', ticker_symbol)),
                    'price': round(current_price, 2),
                    'change': round(change, 2),
                    'change_percent': round(change_percent, 2),
                    'volume': int(volume),
                    'market_cap': info.get('marketCap', 0),
                    'sector': info.get('sector', 'N/A'),
                    'industry': info.get('industry', 'N/A'),
                }
                
                stocks_data.append(stock_data)
                
            except Exception as e:
                logger.warning(f"{ticker_symbol} 데이터 가져오기 실패: {str(e)}")
                continue
        
        # 거래량 기준으로 정렬
        stocks_data.sort(key=lambda x: x['volume'], reverse=True)
        
        return stocks_data[:limit]
    
    except Exception as e:
        logger.error(f"거래량 상위 종목 가져오기 실패: {str(e)}")
        return []


def get_top_gainers(limit: int = 10) -> List[Dict]:
    """
    상승률 상위 종목을 가져옵니다.
    
    Args:
        limit: 가져올 종목 수
    
    Returns:
        종목 정보 리스트
    """
    try:
        major_tickers = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'BRK-B',
            'V', 'UNH', 'XOM', 'JNJ', 'JPM', 'WMT', 'PG', 'MA', 'HD', 'CVX',
            'ABBV', 'PFE', 'AVGO', 'COST', 'MRK', 'PEP', 'TMO', 'CSCO', 'ABT',
            'ACN', 'ADBE', 'NFLX', 'CMCSA', 'NKE', 'DIS', 'VZ', 'INTC', 'TXN',
            'QCOM', 'AMD', 'CRM', 'HON', 'LIN', 'AMAT', 'INTU', 'AMGN', 'BKNG'
        ]
        
        stocks_data = []
        
        for ticker_symbol in major_tickers[:limit * 2]:
            try:
                ticker = yf.Ticker(ticker_symbol)
                info = ticker.info
                hist = ticker.history(period='1d', interval='1m')
                
                if hist.empty:
                    continue
                
                current_price = hist['Close'].iloc[-1]
                previous_close = info.get('previousClose', current_price)
                volume = hist['Volume'].iloc[-1] if 'Volume' in hist.columns else info.get('volume', 0)
                
                change = current_price - previous_close
                change_percent = (change / previous_close * 100) if previous_close > 0 else 0
                
                # 상승 종목만 필터링
                if change_percent <= 0:
                    continue
                
                stock_data = {
                    'symbol': ticker_symbol,
                    'name': info.get('longName', info.get('shortName', ticker_symbol)),
                    'price': round(current_price, 2),
                    'change': round(change, 2),
                    'change_percent': round(change_percent, 2),
                    'volume': int(volume),
                    'market_cap': info.get('marketCap', 0),
                }
                
                stocks_data.append(stock_data)
                
            except Exception as e:
                logger.warning(f"{ticker_symbol} 데이터 가져오기 실패: {str(e)}")
                continue
        
        # 상승률 기준으로 정렬
        stocks_data.sort(key=lambda x: x['change_percent'], reverse=True)
        
        return stocks_data[:limit]
    
    except Exception as e:
        logger.error(f"상승률 상위 종목 가져오기 실패: {str(e)}")
        return []


def get_stock_data(symbol: str) -> Optional[Dict]:
    """
    특정 종목의 상세 정보를 가져옵니다.
    
    Args:
        symbol: 종목 심볼 (예: 'AAPL')
    
    Returns:
        종목 상세 정보 딕셔너리 또는 None
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # 최근 5일간의 주가 데이터
        hist = ticker.history(period='5d')
        
        if hist.empty:
            logger.warning(f"{symbol}: 주가 데이터가 없습니다.")
            return None
        
        current_price = hist['Close'].iloc[-1]
        previous_close = info.get('previousClose', hist['Close'].iloc[-2] if len(hist) > 1 else current_price)
        
        change = current_price - previous_close
        change_percent = (change / previous_close * 100) if previous_close > 0 else 0
        
        # 5일간 주가 히스토리
        price_history = []
        for idx, row in hist.iterrows():
            price_history.append({
                'date': idx.strftime('%Y-%m-%d'),
                'price': round(row['Close'], 2),
                'volume': int(row['Volume']) if 'Volume' in row else 0,
            })
        
        stock_data = {
            'symbol': symbol,
            'name': info.get('longName', info.get('shortName', symbol)),
            'description': info.get('longBusinessSummary', ''),
            'current_price': round(current_price, 2),
            'previous_close': round(previous_close, 2),
            'change': round(change, 2),
            'change_percent': round(change_percent, 2),
            'volume': int(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else info.get('volume', 0),
            'average_volume': info.get('averageVolume', 0),
            'market_cap': info.get('marketCap', 0),
            'pe_ratio': info.get('trailingPE', 0),
            'dividend_yield': info.get('dividendYield', 0),
            '52_week_high': info.get('fiftyTwoWeekHigh', 0),
            '52_week_low': info.get('fiftyTwoWeekLow', 0),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'price_history': price_history,
            'updated_at': datetime.now().isoformat(),
        }
        
        logger.info(f"{symbol} 데이터 수집 완료")
        return stock_data
    
    except Exception as e:
        logger.error(f"{symbol} 데이터 가져오기 실패: {str(e)}")
        return None


def get_top_trending_stock() -> Optional[Dict]:
    """
    오늘의 화제 종목 TOP 1을 가져옵니다.
    거래량과 상승률을 종합하여 선정합니다.
    
    Returns:
        TOP 1 종목 정보 또는 None
    """
    try:
        # 거래량 상위 종목 가져오기
        volume_stocks = get_trending_stocks_by_volume(limit=5)
        
        if not volume_stocks:
            # 거래량 데이터가 없으면 상승률 상위에서 가져오기
            gainer_stocks = get_top_gainers(limit=1)
            return gainer_stocks[0] if gainer_stocks else None
        
        # 거래량과 상승률을 종합한 점수 계산
        for stock in volume_stocks:
            # 점수 = 거래량 정규화 (0-1) * 0.6 + 상승률 정규화 (0-1) * 0.4
            max_volume = max(s['volume'] for s in volume_stocks)
            max_change = max(abs(s['change_percent']) for s in volume_stocks)
            
            volume_score = (stock['volume'] / max_volume) if max_volume > 0 else 0
            change_score = (abs(stock['change_percent']) / max_change) if max_change > 0 else 0
            
            stock['score'] = volume_score * 0.6 + change_score * 0.4
        
        # 점수 기준으로 정렬
        volume_stocks.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        top_stock = volume_stocks[0]
        logger.info(f"TOP 1 종목 선정: {top_stock['symbol']} (점수: {top_stock.get('score', 0):.4f})")
        
        return top_stock
    
    except Exception as e:
        logger.error(f"화제 종목 선정 실패: {str(e)}")
        return None


if __name__ == "__main__":
    # 사용 예시
    print("=" * 60)
    print("Yahoo Finance 데이터 가져오기 테스트")
    print("=" * 60)
    
    # 1. 거래량 상위 종목
    print("\n1. 거래량 상위 5개 종목:")
    volume_stocks = get_trending_stocks_by_volume(limit=5)
    for i, stock in enumerate(volume_stocks, 1):
        print(f"  {i}. {stock['symbol']} ({stock['name']})")
        print(f"     가격: ${stock['price']:.2f}, 변동: {stock['change_percent']:+.2f}%, 거래량: {stock['volume']:,}")
    
    # 2. 상승률 상위 종목
    print("\n2. 상승률 상위 5개 종목:")
    gainer_stocks = get_top_gainers(limit=5)
    for i, stock in enumerate(gainer_stocks, 1):
        print(f"  {i}. {stock['symbol']} ({stock['name']})")
        print(f"     가격: ${stock['price']:.2f}, 변동: {stock['change_percent']:+.2f}%")
    
    # 3. TOP 1 종목
    print("\n3. 오늘의 화제 종목 TOP 1:")
    top_stock = get_top_trending_stock()
    if top_stock:
        print(f"   {top_stock['symbol']} ({top_stock['name']})")
        print(f"   가격: ${top_stock['price']:.2f}")
        print(f"   변동: {top_stock['change_percent']:+.2f}%")
        print(f"   거래량: {top_stock['volume']:,}")
        print(f"   점수: {top_stock.get('score', 0):.4f}")
    
    # 4. 특정 종목 상세 정보
    print("\n4. 특정 종목 상세 정보 (AAPL):")
    apple_data = get_stock_data('AAPL')
    if apple_data:
        print(f"   종목명: {apple_data['name']}")
        print(f"   현재가: ${apple_data['current_price']:.2f}")
        print(f"   변동률: {apple_data['change_percent']:+.2f}%")
        print(f"   시가총액: ${apple_data['market_cap']:,}")
        print(f"   섹터: {apple_data['sector']}")
        print(f"   최근 5일 주가:")
        for day in apple_data['price_history']:
            print(f"     {day['date']}: ${day['price']:.2f}")












