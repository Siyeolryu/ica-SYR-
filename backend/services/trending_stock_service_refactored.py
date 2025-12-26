"""
화제 종목 수집 서비스 (리팩토링 완료)
yahooquery Screener를 사용하여 화제 종목을 수집하고 Top1 종목의 상세 정보를 조회

리팩토링 내용:
1. 중복 코드 제거 - 데이터 타입 처리 로직 통합
2. 함수 분리 - 긴 함수를 작은 함수로 분할
3. 상수 정의 - 매직 넘버 제거
4. 타입 힌트 추가 - 가독성 향상
"""
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import logging
import pandas as pd

logger = logging.getLogger(__name__)


class TrendingStockService:
    """yahooquery Screener를 사용한 화제 종목 수집 서비스"""

    # ========================================================================
    # 상수 정의
    # ========================================================================
    AVAILABLE_SCREENERS = ['most_actives', 'day_gainers', 'day_losers']
    DEFAULT_STOCK_COUNT = 10
    DEFAULT_COUNT_PER_SCREENER = 5

    # 에러 메시지
    ERROR_INVALID_SCREENER = "Invalid screener type: {}. Available types: {}"
    ERROR_NO_DATA_RETURNED = "No data returned from screener: {}"
    ERROR_NO_SYMBOL_FOUND = "No symbol found in screener results"
    ERROR_YAHOOQUERY_NOT_INSTALLED = "yahooquery package is not installed. Please run: pip install yahooquery"

    # ========================================================================
    # Public Methods
    # ========================================================================

    @staticmethod
    def get_top_trending_stock(
        screener_type: str = 'most_actives',
        count: int = DEFAULT_STOCK_COUNT
    ) -> Dict:
        """
        화제 종목 중 Top1 종목 조회

        Args:
            screener_type: 스크리너 타입 (most_actives, day_gainers, day_losers)
            count: 조회할 종목 수 (기본 10개)

        Returns:
            Top1 종목의 상세 정보

        Raises:
            ValueError: 잘못된 스크리너 타입
            Exception: API 호출 실패
        """
        try:
            from yahooquery import Screener

            # 스크리너 타입 검증
            TrendingStockService._validate_screener_type(screener_type)

            logger.info(f"화제 종목 조회 시작: screener_type={screener_type}, count={count}")

            # Screener 데이터 조회
            screener = Screener()
            data = screener.get_screeners([screener_type], count=count)

            # Top1 종목 추출
            symbol, top_stock = TrendingStockService._extract_top_stock(data, screener_type)

            logger.info(f"Top1 종목 선정: {symbol}")

            # 종목 상세 정보 조회
            detail = TrendingStockService.get_stock_detail(symbol)

            # 결과 구성
            result = TrendingStockService._build_top_stock_result(
                screener_type=screener_type,
                symbol=symbol,
                top_stock=top_stock,
                detail=detail
            )

            logger.info(f"화제 종목 조회 완료: {symbol}")
            return result

        except ValueError:
            raise
        except ImportError as e:
            logger.error(f"yahooquery 모듈 import 실패: {str(e)}")
            raise Exception(TrendingStockService.ERROR_YAHOOQUERY_NOT_INSTALLED)
        except Exception as e:
            logger.error(f"화제 종목 조회 실패: {str(e)}")
            raise Exception(f"Failed to get trending stock: {str(e)}")

    @staticmethod
    def get_stock_detail(symbol: str) -> Dict:
        """
        종목 상세 정보 조회

        Args:
            symbol: 종목 심볼

        Returns:
            종목 상세 정보

        Raises:
            Exception: API 호출 실패
        """
        try:
            from yahooquery import Ticker

            logger.info(f"종목 상세 정보 조회: {symbol}")

            # Ticker 인스턴스 생성 및 데이터 조회
            ticker = Ticker(symbol)
            quote = TrendingStockService._get_ticker_quotes(ticker, symbol)
            summary = TrendingStockService._get_ticker_summary(ticker, symbol)
            profile = TrendingStockService._get_ticker_profile(ticker, symbol)
            financial = TrendingStockService._get_ticker_financial(ticker, symbol)

            # 상세 정보 구성
            detail = TrendingStockService._build_stock_detail(
                symbol=symbol,
                quote=quote,
                summary=summary,
                profile=profile,
                financial=financial
            )

            logger.info(f"종목 상세 정보 조회 완료: {symbol}")
            return detail

        except ImportError as e:
            logger.error(f"yahooquery 모듈 import 실패: {str(e)}")
            raise Exception(TrendingStockService.ERROR_YAHOOQUERY_NOT_INSTALLED)
        except Exception as e:
            logger.error(f"종목 상세 정보 조회 실패: {symbol}, {str(e)}")
            raise Exception(f"Failed to get stock detail: {str(e)}")

    @staticmethod
    def get_multiple_trending_stocks(
        screener_types: Optional[List[str]] = None,
        count_per_screener: int = DEFAULT_COUNT_PER_SCREENER
    ) -> Dict:
        """
        여러 스크리너에서 화제 종목 조회

        Args:
            screener_types: 스크리너 타입 리스트 (기본: 모든 타입)
            count_per_screener: 각 스크리너당 조회할 종목 수

        Returns:
            스크리너별 화제 종목 목록
        """
        try:
            from yahooquery import Screener

            # 기본값 설정 및 검증
            screener_types = screener_types or TrendingStockService.AVAILABLE_SCREENERS
            TrendingStockService._validate_screener_types(screener_types)

            logger.info(f"여러 화제 종목 조회 시작: types={screener_types}, count={count_per_screener}")

            # Screener 데이터 조회
            screener = Screener()
            data = screener.get_screeners(screener_types, count=count_per_screener)

            if data is None:
                raise Exception("No data returned from screeners")

            # 데이터 처리
            results = TrendingStockService._process_multiple_screeners_data(data, screener_types)

            logger.info(f"여러 화제 종목 조회 완료: {len(results)}개 스크리너")

            return {
                "screener_types": screener_types,
                "results": results,
                "collected_at": datetime.now().isoformat()
            }

        except ValueError:
            raise
        except ImportError as e:
            logger.error(f"yahooquery 모듈 import 실패: {str(e)}")
            raise Exception(TrendingStockService.ERROR_YAHOOQUERY_NOT_INSTALLED)
        except Exception as e:
            logger.error(f"여러 화제 종목 조회 실패: {str(e)}")
            raise Exception(f"Failed to get multiple trending stocks: {str(e)}")

    @staticmethod
    def get_available_screeners() -> List[str]:
        """사용 가능한 스크리너 타입 목록 반환"""
        return TrendingStockService.AVAILABLE_SCREENERS.copy()

    # ========================================================================
    # Private Helper Methods - Validation
    # ========================================================================

    @staticmethod
    def _validate_screener_type(screener_type: str) -> None:
        """단일 스크리너 타입 유효성 검증"""
        if screener_type not in TrendingStockService.AVAILABLE_SCREENERS:
            raise ValueError(
                TrendingStockService.ERROR_INVALID_SCREENER.format(
                    screener_type,
                    ', '.join(TrendingStockService.AVAILABLE_SCREENERS)
                )
            )

    @staticmethod
    def _validate_screener_types(screener_types: List[str]) -> None:
        """여러 스크리너 타입 유효성 검증"""
        for screener_type in screener_types:
            TrendingStockService._validate_screener_type(screener_type)

    # ========================================================================
    # Private Helper Methods - Data Extraction
    # ========================================================================

    @staticmethod
    def _extract_top_stock(data: Any, screener_type: str) -> tuple[str, Dict]:
        """
        Screener 데이터에서 Top1 종목 추출

        Returns:
            (symbol, stock_data) 튜플
        """
        # DataFrame 처리
        if isinstance(data, pd.DataFrame):
            return TrendingStockService._extract_from_dataframe(data, screener_type)

        # Dict 처리
        if isinstance(data, dict):
            return TrendingStockService._extract_from_dict(data, screener_type)

        raise Exception(f"Unexpected data type: {type(data)}")

    @staticmethod
    def _extract_from_dataframe(data: pd.DataFrame, screener_type: str) -> tuple[str, Dict]:
        """DataFrame에서 Top1 종목 추출"""
        if data.empty:
            raise Exception(TrendingStockService.ERROR_NO_DATA_RETURNED.format(screener_type))

        top_stock = data.iloc[0].to_dict()
        symbol = top_stock.get('symbol')

        if not symbol:
            raise Exception(TrendingStockService.ERROR_NO_SYMBOL_FOUND)

        return symbol, top_stock

    @staticmethod
    def _extract_from_dict(data: Dict, screener_type: str) -> tuple[str, Dict]:
        """Dict에서 Top1 종목 추출"""
        if screener_type not in data or not data[screener_type]:
            raise Exception(TrendingStockService.ERROR_NO_DATA_RETURNED.format(screener_type))

        screener_data = data[screener_type]

        if 'quotes' not in screener_data or not screener_data['quotes']:
            raise Exception(f"No quotes found for screener: {screener_type}")

        top_stock = screener_data['quotes'][0]
        symbol = top_stock.get('symbol')

        if not symbol:
            raise Exception(TrendingStockService.ERROR_NO_SYMBOL_FOUND)

        return symbol, top_stock

    @staticmethod
    def _extract_stock_data(stock_raw: Dict) -> Dict:
        """원시 종목 데이터를 표준 포맷으로 변환"""
        return {
            "symbol": stock_raw.get('symbol'),
            "name": stock_raw.get('shortName', stock_raw.get('longName', '')),
            "price": stock_raw.get('regularMarketPrice', 0),
            "change": stock_raw.get('regularMarketChange', 0),
            "change_percent": stock_raw.get('regularMarketChangePercent', 0),
            "volume": stock_raw.get('regularMarketVolume', 0),
            "market_cap": stock_raw.get('marketCap', 0),
        }

    # ========================================================================
    # Private Helper Methods - Ticker Data
    # ========================================================================

    @staticmethod
    def _get_ticker_quotes(ticker: Any, symbol: str) -> Dict:
        """Ticker에서 quotes 데이터 추출"""
        quotes = ticker.quotes

        if not isinstance(quotes, dict):
            raise Exception(f"Invalid quotes data type: {type(quotes)}")

        if symbol not in quotes:
            raise Exception(f"Symbol not found: {symbol}")

        quote = quotes.get(symbol, {})

        if not isinstance(quote, dict):
            raise Exception(f"Invalid quote data: {quote}")

        return quote

    @staticmethod
    def _get_ticker_summary(ticker: Any, symbol: str) -> Dict:
        """Ticker에서 summary_detail 데이터 추출"""
        if isinstance(ticker.summary_detail, dict) and symbol in ticker.summary_detail:
            summary_data = ticker.summary_detail[symbol]
            return summary_data if isinstance(summary_data, dict) else {}
        return {}

    @staticmethod
    def _get_ticker_profile(ticker: Any, symbol: str) -> Dict:
        """Ticker에서 summary_profile 데이터 추출"""
        if isinstance(ticker.summary_profile, dict) and symbol in ticker.summary_profile:
            profile_data = ticker.summary_profile[symbol]
            return profile_data if isinstance(profile_data, dict) else {}
        return {}

    @staticmethod
    def _get_ticker_financial(ticker: Any, symbol: str) -> Dict:
        """Ticker에서 financial_data 추출"""
        if isinstance(ticker.financial_data, dict) and symbol in ticker.financial_data:
            financial_data = ticker.financial_data[symbol]
            return financial_data if isinstance(financial_data, dict) else {}
        return {}

    # ========================================================================
    # Private Helper Methods - Result Building
    # ========================================================================

    @staticmethod
    def _build_top_stock_result(
        screener_type: str,
        symbol: str,
        top_stock: Dict,
        detail: Dict
    ) -> Dict:
        """Top1 종목 결과 구성"""
        return {
            "screener_type": screener_type,
            "rank": 1,
            "screener_data": TrendingStockService._extract_stock_data(top_stock),
            "detail": detail,
            "collected_at": datetime.now().isoformat()
        }

    @staticmethod
    def _build_stock_detail(
        symbol: str,
        quote: Dict,
        summary: Dict,
        profile: Dict,
        financial: Dict
    ) -> Dict:
        """종목 상세 정보 구성"""
        return {
            "basic_info": {
                "symbol": symbol,
                "name": quote.get("shortName", ""),
                "long_name": quote.get("longName", ""),
                "description": profile.get("longBusinessSummary", ""),
                "sector": profile.get("sector", ""),
                "industry": profile.get("industry", ""),
                "website": profile.get("website", ""),
                "country": profile.get("country", ""),
            },
            "market_data": {
                "current_price": quote.get("regularMarketPrice", 0),
                "previous_close": quote.get("regularMarketPreviousClose", 0),
                "open": quote.get("regularMarketOpen", 0),
                "day_high": quote.get("regularMarketDayHigh", 0),
                "day_low": quote.get("regularMarketDayLow", 0),
                "volume": quote.get("regularMarketVolume", 0),
                "average_volume": summary.get("averageVolume", 0),
                "market_cap": quote.get("marketCap", 0),
            },
            "valuation": {
                "pe_ratio": summary.get("trailingPE"),
                "forward_pe": summary.get("forwardPE"),
                "peg_ratio": summary.get("pegRatio"),
                "price_to_book": summary.get("priceToBook"),
                "enterprise_value": summary.get("enterpriseValue"),
            },
            "dividends": {
                "dividend_rate": summary.get("dividendRate"),
                "dividend_yield": summary.get("dividendYield"),
                "ex_dividend_date": summary.get("exDividendDate"),
                "payout_ratio": summary.get("payoutRatio"),
            },
            "52_week": {
                "high": summary.get("fiftyTwoWeekHigh"),
                "low": summary.get("fiftyTwoWeekLow"),
                "change": summary.get("fiftyTwoWeekChange"),
            },
            "financial_highlights": {
                "revenue": financial.get("totalRevenue"),
                "revenue_per_share": financial.get("revenuePerShare"),
                "profit_margin": financial.get("profitMargins"),
                "operating_margin": financial.get("operatingMargins"),
                "return_on_equity": financial.get("returnOnEquity"),
                "return_on_assets": financial.get("returnOnAssets"),
                "debt_to_equity": financial.get("debtToEquity"),
                "current_ratio": financial.get("currentRatio"),
                "free_cash_flow": financial.get("freeCashflow"),
            }
        }

    # ========================================================================
    # Private Helper Methods - Multiple Screeners
    # ========================================================================

    @staticmethod
    def _process_multiple_screeners_data(data: Any, screener_types: List[str]) -> Dict:
        """여러 스크리너 데이터 처리"""
        # DataFrame 처리
        if isinstance(data, pd.DataFrame):
            return TrendingStockService._process_dataframe_screeners(data, screener_types)

        # Dict 처리
        if isinstance(data, dict):
            return TrendingStockService._process_dict_screeners(data, screener_types)

        raise Exception(f"Unexpected data type: {type(data)}")

    @staticmethod
    def _process_dataframe_screeners(data: pd.DataFrame, screener_types: List[str]) -> Dict:
        """DataFrame 형식의 여러 스크리너 데이터 처리"""
        if data.empty:
            raise Exception("No data returned from screeners")

        results = {}
        for screener_type in screener_types:
            # 해당 스크리너의 데이터만 필터링
            screener_data = data[data.index.get_level_values(0) == screener_type]

            stocks = [
                TrendingStockService._extract_stock_data(row.to_dict())
                for _, row in screener_data.iterrows()
            ]

            results[screener_type] = {
                "count": len(stocks),
                "stocks": stocks
            }

        return results

    @staticmethod
    def _process_dict_screeners(data: Dict, screener_types: List[str]) -> Dict:
        """Dict 형식의 여러 스크리너 데이터 처리"""
        results = {}

        for screener_type in screener_types:
            if screener_type not in data:
                continue

            screener_data = data[screener_type]
            stocks = []

            if 'quotes' in screener_data:
                stocks = [
                    TrendingStockService._extract_stock_data(quote)
                    for quote in screener_data['quotes']
                ]

            results[screener_type] = {
                "count": len(stocks),
                "stocks": stocks
            }

        return results
