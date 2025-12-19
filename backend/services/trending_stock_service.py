"""
화제 종목 수집 서비스
yahooquery Screener를 사용하여 화제 종목을 수집하고 Top1 종목의 상세 정보를 조회
"""
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class TrendingStockService:
    """yahooquery Screener를 사용한 화제 종목 수집 서비스"""

    # 사용 가능한 스크리너 타입
    AVAILABLE_SCREENERS = ['most_actives', 'day_gainers', 'day_losers']

    @staticmethod
    def get_top_trending_stock(
        screener_type: str = 'most_actives',
        count: int = 10
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
            from yahooquery import Screener, Ticker

            # 스크리너 타입 유효성 검증
            if screener_type not in TrendingStockService.AVAILABLE_SCREENERS:
                raise ValueError(
                    f"Invalid screener type: {screener_type}. "
                    f"Available types: {', '.join(TrendingStockService.AVAILABLE_SCREENERS)}"
                )

            logger.info(f"화제 종목 조회 시작: screener_type={screener_type}, count={count}")

            # Screener 인스턴스 생성
            screener = Screener()

            # 스크리너 데이터 조회
            data = screener.get_screeners([screener_type], count=count)

            # 결과 확인 (DataFrame 또는 dict 처리)
            if data is None:
                raise Exception(f"No data returned from screener: {screener_type}")

            # DataFrame인 경우
            if hasattr(data, 'empty'):
                if data.empty:
                    raise Exception(f"No data returned from screener: {screener_type}")

                # 첫 번째 종목 추출 (Top1)
                top_stock = data.iloc[0].to_dict()
                symbol = top_stock.get('symbol')
            # dict인 경우
            elif isinstance(data, dict):
                # screener_type 키로 접근
                if screener_type not in data or not data[screener_type]:
                    raise Exception(f"No data for screener: {screener_type}")

                screener_data = data[screener_type]

                # quotes 키에서 종목 리스트 추출
                if 'quotes' in screener_data and screener_data['quotes']:
                    top_stock = screener_data['quotes'][0]
                    symbol = top_stock.get('symbol')
                else:
                    raise Exception(f"No quotes found for screener: {screener_type}")
            else:
                raise Exception(f"Unexpected data type: {type(data)}")

            if not symbol:
                raise Exception("No symbol found in screener results")

            logger.info(f"Top1 종목 선정: {symbol}")

            # 종목 상세 정보 조회
            detail = TrendingStockService.get_stock_detail(symbol)

            # 결과 구성
            result = {
                "screener_type": screener_type,
                "rank": 1,
                "screener_data": {
                    "symbol": symbol,
                    "name": top_stock.get('shortName', top_stock.get('longName', '')),
                    "price": top_stock.get('regularMarketPrice', 0),
                    "change": top_stock.get('regularMarketChange', 0),
                    "change_percent": top_stock.get('regularMarketChangePercent', 0),
                    "volume": top_stock.get('regularMarketVolume', 0),
                    "market_cap": top_stock.get('marketCap', 0),
                },
                "detail": detail,
                "collected_at": datetime.now().isoformat()
            }

            logger.info(f"화제 종목 조회 완료: {symbol}")
            return result

        except ValueError as e:
            logger.error(f"유효성 검증 실패: {str(e)}")
            raise
        except ImportError as e:
            logger.error(f"yahooquery 모듈 import 실패: {str(e)}")
            raise Exception("yahooquery package is not installed. Please run: pip install yahooquery")
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

            # Ticker 인스턴스 생성
            ticker = Ticker(symbol)

            # 기본 정보
            quotes = ticker.quotes

            # 에러 체크 - quotes가 dict가 아닌 경우 (에러 메시지일 수 있음)
            if not isinstance(quotes, dict):
                raise Exception(f"Invalid quotes data type: {type(quotes)}")

            # 심볼이 quotes에 없는 경우
            if symbol not in quotes:
                raise Exception(f"Symbol not found: {symbol}")

            quote = quotes.get(symbol, {})

            # quote가 dict가 아닌 경우 (에러일 수 있음)
            if not isinstance(quote, dict):
                raise Exception(f"Invalid quote data: {quote}")

            # summary_detail 처리
            summary = {}
            if isinstance(ticker.summary_detail, dict) and symbol in ticker.summary_detail:
                summary_data = ticker.summary_detail[symbol]
                summary = summary_data if isinstance(summary_data, dict) else {}

            # summary_profile 처리
            profile = {}
            if isinstance(ticker.summary_profile, dict) and symbol in ticker.summary_profile:
                profile_data = ticker.summary_profile[symbol]
                profile = profile_data if isinstance(profile_data, dict) else {}

            # financial_data 처리
            financial = {}
            if isinstance(ticker.financial_data, dict) and symbol in ticker.financial_data:
                financial_data = ticker.financial_data[symbol]
                financial = financial_data if isinstance(financial_data, dict) else {}

            # 상세 정보 구성
            detail = {
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

            logger.info(f"종목 상세 정보 조회 완료: {symbol}")
            return detail

        except ImportError as e:
            logger.error(f"yahooquery 모듈 import 실패: {str(e)}")
            raise Exception("yahooquery package is not installed")
        except Exception as e:
            logger.error(f"종목 상세 정보 조회 실패: {symbol}, {str(e)}")
            raise Exception(f"Failed to get stock detail: {str(e)}")

    @staticmethod
    def get_multiple_trending_stocks(
        screener_types: List[str] = None,
        count_per_screener: int = 5
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

            if screener_types is None:
                screener_types = TrendingStockService.AVAILABLE_SCREENERS

            # 유효성 검증
            for screener_type in screener_types:
                if screener_type not in TrendingStockService.AVAILABLE_SCREENERS:
                    raise ValueError(f"Invalid screener type: {screener_type}")

            logger.info(f"여러 화제 종목 조회 시작: types={screener_types}, count={count_per_screener}")

            # Screener 인스턴스 생성
            screener = Screener()

            # 스크리너 데이터 조회
            data = screener.get_screeners(screener_types, count=count_per_screener)

            if data is None:
                raise Exception("No data returned from screeners")

            results = {}

            # DataFrame인 경우
            if hasattr(data, 'empty'):
                if data.empty:
                    raise Exception("No data returned from screeners")

                # 스크리너별로 데이터 그룹화
                for screener_type in screener_types:
                    # 해당 스크리너의 데이터만 필터링
                    screener_data = data[data.index.get_level_values(0) == screener_type]

                    stocks = []
                    for idx, row in screener_data.iterrows():
                        stock = {
                            "symbol": row.get('symbol'),
                            "name": row.get('shortName', row.get('longName', '')),
                            "price": row.get('regularMarketPrice', 0),
                            "change": row.get('regularMarketChange', 0),
                            "change_percent": row.get('regularMarketChangePercent', 0),
                            "volume": row.get('regularMarketVolume', 0),
                            "market_cap": row.get('marketCap', 0),
                        }
                        stocks.append(stock)

                    results[screener_type] = {
                        "count": len(stocks),
                        "stocks": stocks
                    }
            # dict인 경우
            elif isinstance(data, dict):
                for screener_type in screener_types:
                    if screener_type in data:
                        screener_data = data[screener_type]

                        stocks = []
                        if 'quotes' in screener_data:
                            for quote in screener_data['quotes']:
                                stock = {
                                    "symbol": quote.get('symbol'),
                                    "name": quote.get('shortName', quote.get('longName', '')),
                                    "price": quote.get('regularMarketPrice', 0),
                                    "change": quote.get('regularMarketChange', 0),
                                    "change_percent": quote.get('regularMarketChangePercent', 0),
                                    "volume": quote.get('regularMarketVolume', 0),
                                    "market_cap": quote.get('marketCap', 0),
                                }
                                stocks.append(stock)

                        results[screener_type] = {
                            "count": len(stocks),
                            "stocks": stocks
                        }
            else:
                raise Exception(f"Unexpected data type: {type(data)}")

            logger.info(f"여러 화제 종목 조회 완료: {len(results)}개 스크리너")

            return {
                "screener_types": screener_types,
                "results": results,
                "collected_at": datetime.now().isoformat()
            }

        except ValueError as e:
            logger.error(f"유효성 검증 실패: {str(e)}")
            raise
        except ImportError as e:
            logger.error(f"yahooquery 모듈 import 실패: {str(e)}")
            raise Exception("yahooquery package is not installed")
        except Exception as e:
            logger.error(f"여러 화제 종목 조회 실패: {str(e)}")
            raise Exception(f"Failed to get multiple trending stocks: {str(e)}")

    @staticmethod
    def get_available_screeners() -> List[str]:
        """
        사용 가능한 스크리너 타입 목록 반환

        Returns:
            스크리너 타입 리스트
        """
        return TrendingStockService.AVAILABLE_SCREENERS
