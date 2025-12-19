"""
주식 관련 비즈니스 로직
"""
from typing import List, Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class StockService:
    """주식 데이터 처리 서비스"""

    @staticmethod
    def get_trending_stocks(
        screener_types: List[str],
        count: int,
        min_volume: Optional[int] = None,
        min_change_percent: Optional[float] = None,
        sort_by: str = "score",
        order: str = "desc",
        limit: int = 10
    ) -> Dict:
        """
        화제 종목 조회

        Args:
            screener_types: 스크리너 타입 리스트
            count: 각 스크리너당 종목 수
            min_volume: 최소 거래량 필터
            min_change_percent: 최소 변동률 필터
            sort_by: 정렬 기준
            order: 정렬 순서
            limit: 최종 반환 종목 수

        Returns:
            화제 종목 데이터
        """
        from get_trending_stocks import get_trending_stocks, format_stock_data

        logger.info(f"화제 종목 조회 시작: screener_types={screener_types}, count={count}")

        # 데이터 가져오기
        stocks_data = get_trending_stocks(
            screener_types=screener_types,
            count=count
        )

        # 데이터 포맷팅
        formatted_stocks = []
        for screener_type, quotes in stocks_data.items():
            for quote in quotes:
                stock = format_stock_data(quote)
                stock['screener_types'] = [screener_type]
                stock['score'] = StockService._calculate_stock_score(stock)
                formatted_stocks.append(stock)

        # 필터링
        if min_volume:
            formatted_stocks = [s for s in formatted_stocks if s['volume'] >= min_volume]

        if min_change_percent:
            formatted_stocks = [s for s in formatted_stocks if s['change_percent'] >= min_change_percent]

        # 정렬
        reverse = (order == "desc")
        formatted_stocks.sort(key=lambda x: x.get(sort_by, 0), reverse=reverse)

        # 제한 적용
        final_stocks = formatted_stocks[:limit]

        logger.info(f"화제 종목 조회 완료: {len(final_stocks)}개 종목 반환")

        return {
            "stocks": final_stocks,
            "total": len(final_stocks),
            "generated_at": datetime.now().isoformat()
        }

    @staticmethod
    def _calculate_stock_score(stock: Dict) -> float:
        """
        종목 점수 계산

        Args:
            stock: 종목 데이터

        Returns:
            계산된 점수 (0.0 ~ 1.0)
        """
        # 간단한 점수 계산 로직
        # 실제로는 더 복잡한 알고리즘 필요
        score = 0.5

        # 변동률 가중치
        change_percent = abs(stock.get('change_percent', 0))
        if change_percent > 10:
            score += 0.3
        elif change_percent > 5:
            score += 0.2
        elif change_percent > 2:
            score += 0.1

        # 거래량 가중치
        volume = stock.get('volume', 0)
        if volume > 100_000_000:
            score += 0.2
        elif volume > 50_000_000:
            score += 0.1

        return min(score, 1.0)

    @staticmethod
    def get_stock_detail(
        symbol: str,
        include_news: bool = True,
        news_limit: int = 5,
        include_financials: bool = False
    ) -> Dict:
        """
        종목 상세 정보 조회

        Args:
            symbol: 종목 심볼
            include_news: 뉴스 포함 여부
            news_limit: 뉴스 개수
            include_financials: 재무 정보 포함 여부

        Returns:
            종목 상세 정보
        """
        from yahooquery import Ticker

        logger.info(f"종목 상세 정보 조회: {symbol}")

        ticker = Ticker(symbol)

        # 기본 정보
        quotes = ticker.quotes
        if symbol not in quotes or not quotes[symbol]:
            raise ValueError(f"종목을 찾을 수 없습니다: {symbol}")

        quote = quotes[symbol]
        summary = ticker.summary_detail.get(symbol, {})
        profile = ticker.summary_profile.get(symbol, {})

        result = {
            "symbol": symbol,
            "name": quote.get("shortName", ""),
            "description": profile.get("longBusinessSummary", ""),
            "current_price": quote.get("regularMarketPrice", 0),
            "previous_close": quote.get("regularMarketPreviousClose", 0),
            "change": quote.get("regularMarketChange", 0),
            "change_percent": quote.get("regularMarketChangePercent", 0),
            "volume": quote.get("regularMarketVolume", 0),
            "average_volume": summary.get("averageVolume", 0),
            "market_cap": quote.get("marketCap", 0),
            "pe_ratio": summary.get("trailingPE"),
            "dividend_yield": summary.get("dividendYield"),
            "52_week_high": summary.get("fiftyTwoWeekHigh"),
            "52_week_low": summary.get("fiftyTwoWeekLow"),
            "sector": profile.get("sector", ""),
            "industry": profile.get("industry", ""),
            "news": [],
            "updated_at": datetime.now().isoformat()
        }

        # 뉴스 추가 (선택적)
        if include_news:
            try:
                from exa_news import search_stock_news
                news_articles = search_stock_news(
                    symbol,
                    stock_name=result['name'],
                    limit=news_limit,
                    days_back=7
                )
                result['news'] = news_articles
                logger.info(f"{symbol} 뉴스 {len(news_articles)}개 수집 완료")
            except Exception as e:
                logger.warning(f"뉴스 조회 실패: {str(e)}")
                result['news'] = []

        logger.info(f"종목 상세 정보 조회 완료: {symbol}")
        return result

    @staticmethod
    def validate_symbol(symbol: str) -> bool:
        """
        종목 심볼 유효성 검증

        Args:
            symbol: 종목 심볼

        Returns:
            유효 여부
        """
        return symbol.isalpha() and symbol.isupper()
