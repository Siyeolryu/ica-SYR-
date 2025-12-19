"""
브리핑 관련 API 라우터
"""
from fastapi import APIRouter, Query, HTTPException, Path
from datetime import datetime
import logging

from models.schemas import (
    BriefingCreateRequest,
    BriefingResponse,
    BriefingListResponse,
    SendBriefingRequest,
    SendBriefingResponse,
    ErrorResponse
)
from services.briefing_service import BriefingService

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Briefings"]
)


@router.post(
    "/briefings",
    response_model=BriefingResponse,
    status_code=200,
    responses={
        400: {"model": ErrorResponse, "description": "잘못된 요청"},
        422: {"model": ErrorResponse, "description": "충분한 종목 데이터 없음"},
        500: {"model": ErrorResponse, "description": "브리핑 생성 실패"}
    },
    summary="브리핑 생성",
    description="화제 종목 정보를 기반으로 AI 브리핑(이미지 + 텍스트)을 생성합니다."
)
def create_briefing(request: BriefingCreateRequest):
    """
    ## 브리핑 생성 API

    화제 종목을 분석하여 AI 브리핑을 생성합니다.

    **예시 요청:**
    ```json
    {
      "stock_symbols": ["AAPL", "TSLA", "MSFT"],
      "format": "both",
      "language": "ko",
      "count": 5
    }
    ```
    """
    try:
        logger.info(f"브리핑 생성 시작: {request.dict()}")

        # BriefingService를 통해 브리핑 생성
        result = BriefingService.create_briefing(
            stock_symbols=request.stock_symbols,
            format_type=request.format,
            language=request.language,
            count=request.count
        )

        briefing_data = result['briefing_data']
        top_stock = result['stock_data']
        briefing_id = result['briefing_id']
        image_url = result['image_url']

        response = {
            "success": True,
            "data": {
                "briefing_id": briefing_id,
                "generated_at": datetime.now().isoformat(),
                "status": "completed",
                "stocks_included": [
                    {
                        "symbol": top_stock.get('symbol', ''),
                        "name": top_stock.get('name', ''),
                        "price": top_stock.get('price', 0),
                        "change_percent": top_stock.get('change_percent', 0),
                        "volume": top_stock.get('volume', 0)
                    }
                ],
                "content": {
                    "text": {
                        "title": briefing_data.get('title', '오늘의 화제 종목 브리핑'),
                        "summary": briefing_data.get('summary', ''),
                        "sections": briefing_data.get('sections', [])
                    },
                    "image": {
                        "url": image_url,
                        "thumbnail_url": image_url,
                        "width": 1200,
                        "height": 1600,
                        "format": "png"
                    } if image_url else None
                },
                "metadata": {
                    "template_used": request.template_id or "default_v1",
                    "generation_time_ms": result.get('generation_time_ms', 0),
                    "ai_model": "gemini-pro",
                    "language": request.language
                }
            }
        }

        logger.info(f"브리핑 생성 완료: {briefing_id}")
        return response

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": {
                    "code": "GENERATION_ERROR",
                    "message": str(e),
                    "timestamp": datetime.now().isoformat()
                }
            }
        )
    except Exception as e:
        logger.error(f"브리핑 생성 실패: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": {
                    "code": "GENERATION_ERROR",
                    "message": "브리핑 생성 중 오류 발생",
                    "details": {"error": str(e)},
                    "timestamp": datetime.now().isoformat()
                }
            }
        )


@router.get(
    "/briefings",
    response_model=BriefingListResponse,
    responses={
        400: {"model": ErrorResponse, "description": "잘못된 파라미터"},
        401: {"model": ErrorResponse, "description": "인증 실패"}
    },
    summary="브리핑 목록 조회",
    description="생성된 브리핑 목록을 조회합니다."
)
def get_briefings(
    page: int = Query(1, ge=1, description="페이지 번호 (1부터 시작)"),
    limit: int = Query(20, ge=1, le=100, description="페이지당 항목 수"),
    start_date: str = Query(None, description="시작 날짜 (ISO 8601)"),
    end_date: str = Query(None, description="종료 날짜 (ISO 8601)"),
    stock_symbol: str = Query(None, description="특정 종목 필터"),
    status: str = Query(None, description="브리핑 상태 필터 (completed, processing, failed)")
):
    """
    ## 브리핑 목록 조회 API

    생성된 브리핑 히스토리를 조회합니다.

    **예시 요청:**
    ```
    GET /v1/briefings?page=1&limit=10&start_date=2024-01-01T00:00:00Z
    ```
    """
    try:
        # BriefingService를 통해 목록 조회
        data = BriefingService.get_briefings(
            page=page,
            limit=limit,
            start_date=start_date,
            end_date=end_date,
            stock_symbol=stock_symbol,
            status=status
        )

        return {
            "success": True,
            "data": data
        }

    except Exception as e:
        logger.error(f"브리핑 목록 조회 실패: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "브리핑 목록 조회 실패",
                    "details": {"error": str(e)},
                    "timestamp": datetime.now().isoformat()
                }
            }
        )


@router.get(
    "/briefings/{briefing_id}",
    response_model=BriefingResponse,
    responses={
        404: {"model": ErrorResponse, "description": "브리핑을 찾을 수 없음"},
        401: {"model": ErrorResponse, "description": "인증 실패"}
    },
    summary="브리핑 상세 조회",
    description="특정 브리핑의 상세 정보를 조회합니다."
)
def get_briefing(
    briefing_id: str = Path(..., description="브리핑 ID")
):
    """
    ## 브리핑 상세 조회 API

    특정 브리핑의 전체 내용을 조회합니다.

    **예시 요청:**
    ```
    GET /v1/briefings/brf_20240115_060000_abc123
    ```
    """
    try:
        # BriefingService를 통해 상세 조회
        data = BriefingService.get_briefing_by_id(briefing_id)

        return {
            "success": True,
            "data": data
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "error": {
                    "code": "BRIEFING_NOT_FOUND",
                    "message": str(e),
                    "timestamp": datetime.now().isoformat()
                }
            }
        )
    except Exception as e:
        logger.error(f"브리핑 상세 조회 실패: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "브리핑 조회 실패",
                    "details": {"error": str(e)},
                    "timestamp": datetime.now().isoformat()
                }
            }
        )


@router.post(
    "/briefings/{briefing_id}/send",
    response_model=SendBriefingResponse,
    responses={
        404: {"model": ErrorResponse, "description": "브리핑을 찾을 수 없음"},
        422: {"model": ErrorResponse, "description": "잘못된 이메일 또는 Slack Webhook"},
        500: {"model": ErrorResponse, "description": "발송 실패"}
    },
    summary="브리핑 발송",
    description="생성된 브리핑을 이메일 또는 Slack으로 발송합니다."
)
def send_briefing(
    briefing_id: str = Path(..., description="발송할 브리핑 ID"),
    request: SendBriefingRequest = None
):
    """
    ## 브리핑 발송 API

    브리핑을 이메일 또는 Slack으로 발송합니다.

    **예시 요청:**
    ```json
    {
      "channels": [
        {
          "type": "email",
          "email": "user@example.com"
        },
        {
          "type": "slack",
          "slack_webhook_url": "https://hooks.slack.com/services/XXX/YYY/ZZZ",
          "slack_channel": "#stock-briefing"
        }
      ],
      "send_immediately": true
    }
    ```
    """
    try:
        logger.info(f"브리핑 발송: {briefing_id}")

        # BriefingService를 통해 발송
        result = BriefingService.send_briefing(
            briefing_id=briefing_id,
            channels=[ch.dict() for ch in request.channels],
            send_immediately=request.send_immediately
        )

        # 채널별 결과 구성
        channel_results = []
        for channel in request.channels:
            channel_result = {
                "type": channel.type,
                "status": "sent",
                "sent_at": datetime.now().isoformat()
            }

            if channel.type == "email":
                channel_result["email"] = channel.email
                channel_result["message_id"] = f"msg_email_{datetime.now().timestamp()}"
            elif channel.type == "slack":
                channel_result["slack_channel"] = channel.slack_channel
                channel_result["message_id"] = f"msg_slack_{datetime.now().timestamp()}"

            channel_results.append(channel_result)

        return {
            "success": True,
            "data": {
                "briefing_id": briefing_id,
                "send_job_id": result['send_job_id'],
                "status": result['status'],
                "channels": channel_results,
                "total_sent": result['total_sent'],
                "total_failed": result['total_failed']
            }
        }

    except Exception as e:
        logger.error(f"브리핑 발송 실패: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": {
                    "code": "SEND_ERROR",
                    "message": "브리핑 발송 실패",
                    "details": {"error": str(e)},
                    "timestamp": datetime.now().isoformat()
                }
            }
        )
