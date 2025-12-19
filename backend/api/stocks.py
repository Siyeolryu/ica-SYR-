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
from services.stock_service import StockService
from services.trending_stock_service import TrendingStockService

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

        # StockService를 통해 데이터 조회
        data = StockService.get_trending_stocks(
            screener_types=screener_list,
            count=count,
            min_volume=min_volume,
            min_change_percent=min_change_percent,
            sort_by=sort_by,
            order=order,
            limit=limit
        )

        return {
            "success": True,
            "data": data
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
        # 심볼 유효성 검증
        if not StockService.validate_symbol(symbol):
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

        # StockService를 통해 데이터 조회
        stock_data = StockService.get_stock_detail(
            symbol=symbol,
            include_news=include_news,
            news_limit=news_limit,
            include_financials=include_financials
        )

        return {
            "success": True,
            "data": stock_data
        }

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "error": {
                    "code": "STOCK_NOT_FOUND",
                    "message": str(e),
                    "timestamp": datetime.now().isoformat()
                }
            }
        )
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


@router.get(
    "/top-trending-stock",
    responses={
        400: {"model": ErrorResponse, "description": "잘못된 파라미터"},
        500: {"model": ErrorResponse, "description": "데이터 수집 실패"}
    },
    summary="Top1 화제 종목 조회",
    description="yahooquery Screener를 사용하여 Top1 화제 종목과 상세 정보를 조회합니다."
)
def get_top_trending_stock_api(
    screener_type: str = Query(
        "most_actives",
        description="스크리너 타입 (most_actives, day_gainers, day_losers)",
        pattern="^(most_actives|day_gainers|day_losers)$"
    ),
    count: int = Query(
        10,
        ge=1,
        le=25,
        description="스크리너에서 조회할 종목 수"
    )
):
    """
    ## Top1 화제 종목 조회 API

    yahooquery Screener를 사용하여 화제 종목 중 Top1 종목의 상세 정보를 조회합니다.

    **예시 요청:**
    ```
    GET /v1/top-trending-stock?screener_type=most_actives&count=10
    ```

    **스크리너 타입:**
    - `most_actives`: 거래량 상위 종목
    - `day_gainers`: 당일 상승률 상위 종목
    - `day_losers`: 당일 하락률 상위 종목

    **응답 데이터:**
    - Top1 종목의 기본 정보 (symbol, name, price, volume 등)
    - 상세 정보 (재무 데이터, 밸류에이션, 배당 정보 등)
    """
    try:
        logger.info(f"Top1 화제 종목 조회: screener_type={screener_type}")

        # TrendingStockService를 통해 데이터 조회
        result = TrendingStockService.get_top_trending_stock(
            screener_type=screener_type,
            count=count
        )

        return {
            "success": True,
            "data": result
        }

    except ValueError as e:
        logger.error(f"유효성 검증 실패: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "error": {
                    "code": "INVALID_PARAMETER",
                    "message": str(e),
                    "timestamp": datetime.now().isoformat()
                }
            }
        )
    except Exception as e:
        logger.error(f"Top1 화제 종목 조회 실패: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": {
                    "code": "DATA_FETCH_ERROR",
                    "message": "화제 종목 조회 실패",
                    "details": {"error": str(e)},
                    "timestamp": datetime.now().isoformat()
                }
            }
        )


@router.get(
    "/multiple-trending-stocks",
    responses={
        400: {"model": ErrorResponse, "description": "잘못된 파라미터"},
        500: {"model": ErrorResponse, "description": "데이터 수집 실패"}
    },
    summary="여러 스크리너에서 화제 종목 조회",
    description="여러 스크리너 타입을 동시에 조회하여 화제 종목 목록을 반환합니다."
)
def get_multiple_trending_stocks_api(
    screener_types: str = Query(
        "most_actives,day_gainers",
        description="스크리너 타입 (콤마로 구분)",
        example="most_actives,day_gainers,day_losers"
    ),
    count: int = Query(
        5,
        ge=1,
        le=25,
        description="각 스크리너당 종목 수"
    )
):
    """
    ## 여러 스크리너에서 화제 종목 조회 API

    여러 스크리너를 동시에 조회하여 스크리너별 화제 종목 목록을 반환합니다.

    **예시 요청:**
    ```
    GET /v1/multiple-trending-stocks?screener_types=most_actives,day_gainers&count=5
    ```

    **응답 데이터:**
    - 각 스크리너별 종목 목록
    - 종목별 기본 정보 (symbol, name, price, volume 등)
    """
    try:
        # 스크리너 타입 파싱
        screener_list = [s.strip() for s in screener_types.split(",")]

        logger.info(f"여러 화제 종목 조회: screener_types={screener_list}")

        # TrendingStockService를 통해 데이터 조회
        result = TrendingStockService.get_multiple_trending_stocks(
            screener_types=screener_list,
            count_per_screener=count
        )

        return {
            "success": True,
            "data": result
        }

    except ValueError as e:
        logger.error(f"유효성 검증 실패: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "error": {
                    "code": "INVALID_PARAMETER",
                    "message": str(e),
                    "timestamp": datetime.now().isoformat()
                }
            }
        )
    except Exception as e:
        logger.error(f"여러 화제 종목 조회 실패: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": {
                    "code": "DATA_FETCH_ERROR",
                    "message": "화제 종목 조회 실패",
                    "details": {"error": str(e)},
                    "timestamp": datetime.now().isoformat()
                }
            }
        )


@router.get(
    "/available-screeners",
    summary="사용 가능한 스크리너 목록",
    description="사용 가능한 스크리너 타입 목록을 반환합니다."
)
def get_available_screeners_api():
    """
    ## 사용 가능한 스크리너 목록 API

    사용 가능한 스크리너 타입 목록을 반환합니다.

    **응답 데이터:**
    - 스크리너 타입 리스트
    """
    try:
        screeners = TrendingStockService.get_available_screeners()

        return {
            "success": True,
            "data": {
                "screeners": screeners,
                "count": len(screeners)
            }
        }

    except Exception as e:
        logger.error(f"스크리너 목록 조회 실패: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "스크리너 목록 조회 실패",
                    "details": {"error": str(e)},
                    "timestamp": datetime.now().isoformat()
                }
            }
        )
