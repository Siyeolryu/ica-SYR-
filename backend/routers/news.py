"""
Exa API를 사용한 뉴스 검색 라우터
"""
from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from datetime import datetime
import logging

from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["News"]
)


# Response Models
class NewsArticle(BaseModel):
    """뉴스 기사 모델"""
    title: str
    url: str
    published_date: str
    source: str
    summary: Optional[str] = ""
    author: Optional[str] = ""


class NewsResponse(BaseModel):
    """뉴스 응답 모델"""
    success: bool
    data: dict


class ErrorResponse(BaseModel):
    """에러 응답 모델"""
    success: bool
    error: dict


@router.get(
    "/news/stock/{ticker}",
    response_model=NewsResponse,
    responses={
        400: {"model": ErrorResponse, "description": "잘못된 파라미터"},
        401: {"model": ErrorResponse, "description": "API 키 없음"},
        500: {"model": ErrorResponse, "description": "뉴스 수집 실패"}
    },
    summary="종목 뉴스 검색",
    description="Exa API를 사용하여 특정 종목의 뉴스를 검색합니다."
)
def get_stock_news(
    ticker: str,
    days_back: int = Query(
        7,
        ge=1,
        le=30,
        description="며칠 전까지의 뉴스 검색 (1-30일)"
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="가져올 뉴스 개수 (최대 100)"
    ),
    translate: bool = Query(
        True,
        description="한국어로 번역 여부 (기본값: True)"
    )
):
    """
    ## 종목 뉴스 검색 API

    Exa API를 사용하여 특정 종목의 뉴스를 검색합니다.

    **예시 요청:**
    ```
    GET /v1/news/stock/AAPL?days_back=7&limit=10
    ```

    **검색 범위:**
    - 최근 1~30일 내 뉴스
    - 검색 쿼리: "{ticker} stock news"

    **반환 데이터:**
    - 제목, URL, 발행일, 출처, 요약
    """
    try:
        from exa_news import search_stock_news

        # 심볼 유효성 검증
        if not ticker or len(ticker) > 10:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "error": {
                        "code": "INVALID_TICKER",
                        "message": "잘못된 종목 심볼",
                        "details": {"ticker": ticker},
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )

        logger.info(f"뉴스 검색 시작: {ticker} (최근 {days_back}일, {limit}개)")

        # 뉴스 검색
        news_articles = search_stock_news(
            stock_symbol=ticker,
            limit=limit,
            days_back=days_back
        )

        logger.info(f"뉴스 검색 완료: {ticker} - {len(news_articles)}개")

        # 한국어 번역
        if translate and news_articles:
            try:
                from gemini_briefing import translate_news_to_korean
                logger.info(f"뉴스 번역 시작: {len(news_articles)}개")
                news_articles = translate_news_to_korean(news_articles)
                logger.info("뉴스 번역 완료")
            except Exception as e:
                logger.warning(f"번역 실패, 원본 반환: {str(e)}")

        return {
            "success": True,
            "data": {
                "ticker": ticker,
                "news": news_articles,
                "total": len(news_articles),
                "days_back": days_back,
                "translated": translate,
                "generated_at": datetime.now().isoformat()
            }
        }

    except ValueError as e:
        logger.error(f"API 키 오류: {str(e)}")
        raise HTTPException(
            status_code=401,
            detail={
                "success": False,
                "error": {
                    "code": "API_KEY_ERROR",
                    "message": "Exa API 키가 설정되지 않았습니다",
                    "details": {"error": str(e)},
                    "timestamp": datetime.now().isoformat()
                }
            }
        )
    except Exception as e:
        logger.error(f"뉴스 검색 실패: {ticker}, {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": {
                    "code": "NEWS_FETCH_ERROR",
                    "message": "뉴스 검색 실패",
                    "details": {"error": str(e)},
                    "timestamp": datetime.now().isoformat()
                }
            }
        )


@router.get(
    "/news/stock/{ticker}/24h",
    response_model=NewsResponse,
    responses={
        400: {"model": ErrorResponse, "description": "잘못된 파라미터"},
        401: {"model": ErrorResponse, "description": "API 키 없음"},
        500: {"model": ErrorResponse, "description": "뉴스 수집 실패"}
    },
    summary="24시간 종목 뉴스 검색",
    description="최근 24시간 내 특정 종목의 뉴스를 검색합니다."
)
def get_stock_news_24h(
    ticker: str,
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="가져올 뉴스 개수 (최대 100)"
    ),
    translate: bool = Query(
        True,
        description="한국어로 번역 여부 (기본값: True)"
    )
):
    """
    ## 24시간 종목 뉴스 검색 API

    최근 24시간 내 특정 종목의 뉴스를 검색합니다.

    **예시 요청:**
    ```
    GET /v1/news/stock/AAPL/24h?limit=5
    ```

    **검색 조건:**
    - 검색 키워드: "{ticker} stock news"
    - 검색 범위: 최근 24시간
    - 결과: 제목, URL, 발행일 포함
    """
    try:
        from exa_news import search_stock_news_24h

        # 심볼 유효성 검증
        if not ticker or len(ticker) > 10:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "error": {
                        "code": "INVALID_TICKER",
                        "message": "잘못된 종목 심볼",
                        "details": {"ticker": ticker},
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )

        logger.info(f"24시간 뉴스 검색 시작: {ticker} ({limit}개)")

        # 24시간 뉴스 검색
        news_articles = search_stock_news_24h(ticker, limit=limit)

        logger.info(f"24시간 뉴스 검색 완료: {ticker} - {len(news_articles)}개")

        # 한국어 번역
        if translate and news_articles:
            try:
                from gemini_briefing import translate_news_to_korean
                logger.info(f"뉴스 번역 시작: {len(news_articles)}개")
                news_articles = translate_news_to_korean(news_articles)
                logger.info("뉴스 번역 완료")
            except Exception as e:
                logger.warning(f"번역 실패, 원본 반환: {str(e)}")

        return {
            "success": True,
            "data": {
                "ticker": ticker,
                "news": news_articles,
                "total": len(news_articles),
                "period": "24h",
                "translated": translate,
                "generated_at": datetime.now().isoformat()
            }
        }

    except ValueError as e:
        logger.error(f"API 키 오류: {str(e)}")
        raise HTTPException(
            status_code=401,
            detail={
                "success": False,
                "error": {
                    "code": "API_KEY_ERROR",
                    "message": "Exa API 키가 설정되지 않았습니다",
                    "details": {"error": str(e)},
                    "timestamp": datetime.now().isoformat()
                }
            }
        )
    except Exception as e:
        logger.error(f"24시간 뉴스 검색 실패: {ticker}, {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": {
                    "code": "NEWS_FETCH_ERROR",
                    "message": "뉴스 검색 실패",
                    "details": {"error": str(e)},
                    "timestamp": datetime.now().isoformat()
                }
            }
        )


@router.post(
    "/news/stocks/batch",
    response_model=NewsResponse,
    responses={
        400: {"model": ErrorResponse, "description": "잘못된 파라미터"},
        401: {"model": ErrorResponse, "description": "API 키 없음"},
        500: {"model": ErrorResponse, "description": "뉴스 수집 실패"}
    },
    summary="여러 종목 뉴스 일괄 검색",
    description="여러 종목의 뉴스를 한 번에 검색합니다."
)
def get_multiple_stocks_news(
    tickers: List[str],
    limit_per_stock: int = Query(
        3,
        ge=1,
        le=20,
        description="종목당 뉴스 개수"
    ),
    days_back: int = Query(
        7,
        ge=1,
        le=30,
        description="며칠 전까지의 뉴스 검색"
    ),
    translate: bool = Query(
        True,
        description="한국어로 번역 여부 (기본값: True)"
    )
):
    """
    ## 여러 종목 뉴스 일괄 검색 API

    여러 종목의 뉴스를 한 번에 검색합니다.

    **예시 요청:**
    ```json
    POST /v1/news/stocks/batch
    {
        "tickers": ["AAPL", "TSLA", "NVDA"],
        "limit_per_stock": 3,
        "days_back": 7
    }
    ```
    """
    try:
        from exa_news import search_trending_stocks_news

        # 검증
        if not tickers or len(tickers) == 0:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "error": {
                        "code": "INVALID_PARAMETER",
                        "message": "종목 리스트가 비어있습니다",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )

        if len(tickers) > 20:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "error": {
                        "code": "TOO_MANY_TICKERS",
                        "message": "최대 20개 종목까지 조회 가능합니다",
                        "details": {"requested": len(tickers), "max": 20},
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )

        logger.info(f"일괄 뉴스 검색 시작: {len(tickers)}개 종목")

        # 여러 종목 뉴스 검색
        all_news = search_trending_stocks_news(
            stock_symbols=tickers,
            limit_per_stock=limit_per_stock,
            days_back=days_back
        )

        total_articles = sum(len(articles) for articles in all_news.values())
        logger.info(f"일괄 뉴스 검색 완료: 총 {total_articles}개")

        # 한국어 번역
        if translate and total_articles > 0:
            try:
                from gemini_briefing import translate_news_to_korean
                logger.info(f"뉴스 번역 시작: {total_articles}개")
                for ticker, articles in all_news.items():
                    if articles:
                        all_news[ticker] = translate_news_to_korean(articles)
                logger.info("뉴스 번역 완료")
            except Exception as e:
                logger.warning(f"번역 실패, 원본 반환: {str(e)}")

        return {
            "success": True,
            "data": {
                "news_by_ticker": all_news,
                "total_tickers": len(tickers),
                "total_articles": total_articles,
                "days_back": days_back,
                "translated": translate,
                "generated_at": datetime.now().isoformat()
            }
        }

    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"API 키 오류: {str(e)}")
        raise HTTPException(
            status_code=401,
            detail={
                "success": False,
                "error": {
                    "code": "API_KEY_ERROR",
                    "message": "Exa API 키가 설정되지 않았습니다",
                    "details": {"error": str(e)},
                    "timestamp": datetime.now().isoformat()
                }
            }
        )
    except Exception as e:
        logger.error(f"일괄 뉴스 검색 실패: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": {
                    "code": "NEWS_FETCH_ERROR",
                    "message": "뉴스 검색 실패",
                    "details": {"error": str(e)},
                    "timestamp": datetime.now().isoformat()
                }
            }
        )
