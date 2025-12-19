"""
화제 종목 관련 API 라우터
"""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from datetime import datetime
import logging

from models.schemas import (
    TrendingStocksResponse,
    StockDetailResponse,
    ErrorResponse
)
from get_trending_stocks import get_trending_stocks, format_stock_data

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Stocks"]
)


@router.get(
    "/trending-stocks",
    response_model=TrendingStocksResponse,
    responses={
        400: {"model": ErrorResponse, "description": "잘못된 파라미터"},
        429: {"model": ErrorResponse, "description": "API 호출 제한 초과"},
        500: {"model": ErrorResponse, "description": "데이터 수집 실패"}
    },
    summary="화제 종목 조회",
    description="Yahoo Finance Screener를 활용하여 화제 종목 목록을 조회합니다."
)
def get_trending_stocks_api(
    screener_types: str = Query(
        "most_actives,day_gainers",
        description="스크리너 타입 (콤마로 구분). most_actives: 거래량 상위, day_gainers: 상승률 상위, day_losers: 하락률 상위",
        example="most_actives,day_gainers"
    ),
    count: int = Query(
        10,
        ge=1,
        le=50,
        description="각 스크리너당 종목 수"
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="최종 반환 종목 수"
    ),
    min_volume: Optional[int] = Query(
        None,
        description="최소 거래량 필터"
    ),
    min_change_percent: Optional[float] = Query(
        None,
        description="최소 변동률 필터 (%)"
    ),
    sort_by: str = Query(
        "score",
        description="정렬 기준 (score, volume, change_percent)",
        pattern="^(score|volume|change_percent)$"
    ),
    order: str = Query(
        "desc",
        description="정렬 순서 (asc, desc)",
        pattern="^(asc|desc)$"
    )
):
    """
    ## 화제 종목 조회 API

    Yahoo Finance Screener에서 화제 종목을 수집하여 반환합니다.

    **예시 요청:**
    ```
    GET /v1/trending-stocks?screener_types=most_actives,day_gainers&count=10&limit=5
    ```

    **스크리너 타입:**
    - `most_actives`: 거래량 상위 종목
    - `day_gainers`: 당일 상승률 상위 종목
    - `day_losers`: 당일 하락률 상위 종목
    """
    try:
        # 스크리너 타입 파싱
        screener_list = [s.strip() for s in screener_types.split(",")]

        # 유효한 스크리너 타입 확인
        valid_screeners = ["most_actives", "day_gainers", "day_losers"]
        for screener in screener_list:
            if screener not in valid_screeners:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "success": False,
                        "error": {
                            "code": "INVALID_PARAMETER",
                            "message": f"Invalid screener type: {screener}",
                            "details": {
                                "parameter": "screener_types",
                                "provided": screener,
                                "valid_values": valid_screeners
                            },
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                )

        logger.info(f"화제 종목 조회 시작: screener_types={screener_list}, count={count}")

        # 데이터 가져오기
        stocks_data = get_trending_stocks(
            screener_types=screener_list,
            count=count
        )

        # 데이터 포맷팅
        formatted_stocks = []
        for screener_type, quotes in stocks_data.items():
            for quote in quotes:
                stock = format_stock_data(quote)
                stock['screener_types'] = [screener_type]
                # 임시 점수 계산 (실제로는 더 복잡한 로직 필요)
                stock['score'] = 0.8
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
            "success": True,
            "data": {
                "stocks": final_stocks,
                "total": len(final_stocks),
                "generated_at": datetime.now().isoformat()
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"화제 종목 조회 실패: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": {
                    "code": "DATA_FETCH_ERROR",
                    "message": "외부 데이터 수집 실패",
                    "details": {"error": str(e)},
                    "timestamp": datetime.now().isoformat()
                }
            }
        )


@router.get(
    "/stocks/{symbol}",
    response_model=StockDetailResponse,
    responses={
        400: {"model": ErrorResponse, "description": "잘못된 종목 심볼"},
        404: {"model": ErrorResponse, "description": "종목을 찾을 수 없음"},
        500: {"model": ErrorResponse, "description": "데이터 수집 실패"}
    },
    summary="종목 상세 정보 조회",
    description="특정 종목의 상세 정보와 관련 뉴스를 조회합니다."
)
def get_stock_detail(
    symbol: str,
    include_news: bool = Query(
        True,
        description="관련 뉴스 포함 여부"
    ),
    news_limit: int = Query(
        5,
        ge=1,
        le=20,
        description="뉴스 개수"
    ),
    include_financials: bool = Query(
        False,
        description="재무 정보 포함 여부"
    )
):
    """
    ## 종목 상세 정보 조회 API

    특정 종목의 상세 정보를 조회합니다.

    **예시 요청:**
    ```
    GET /v1/stocks/AAPL?include_news=true&news_limit=5
    ```
    """
    try:
        from yahooquery import Ticker

        logger.info(f"종목 상세 정보 조회: {symbol}")

        # 심볼 유효성 검증 (대문자, 알파벳만)
        if not symbol.isalpha() or not symbol.isupper():
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "error": {
                        "code": "INVALID_SYMBOL",
                        "message": "잘못된 종목 심볼 형식",
                        "details": {
                            "symbol": symbol,
                            "format": "대문자 알파벳만 허용 (예: AAPL)"
                        },
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )

        ticker = Ticker(symbol)

        # 기본 정보
        quotes = ticker.quotes
        if symbol not in quotes or not quotes[symbol]:
            raise HTTPException(
                status_code=404,
                detail={
                    "success": False,
                    "error": {
                        "code": "STOCK_NOT_FOUND",
                        "message": f"종목을 찾을 수 없습니다: {symbol}",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )

        quote = quotes[symbol]
        summary = ticker.summary_detail.get(symbol, {})
        profile = ticker.summary_profile.get(symbol, {})

        result = {
            "success": True,
            "data": {
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
        }

        # 뉴스 추가 (선택적)
        if include_news:
            try:
                from exa_news import search_stock_news
                news_articles = search_stock_news(
                    symbol,
                    stock_name=result['data']['name'],
                    limit=news_limit,
                    days_back=7
                )
                result['data']['news'] = news_articles
                logger.info(f"{symbol} 뉴스 {len(news_articles)}개 수집 완료")
            except Exception as e:
                logger.warning(f"뉴스 조회 실패: {str(e)}")
                result['data']['news'] = []

        logger.info(f"종목 상세 정보 조회 완료: {symbol}")
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"종목 상세 정보 조회 실패: {symbol}, {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": {
                    "code": "DATA_FETCH_ERROR",
                    "message": "종목 정보 수집 실패",
                    "details": {"error": str(e)},
                    "timestamp": datetime.now().isoformat()
                }
            }
        )
