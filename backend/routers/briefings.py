"""
브리핑 관련 API 라우터
"""
from fastapi import APIRouter, Query, HTTPException, Path
from datetime import datetime
import logging
import os

from models.schemas import (
    BriefingCreateRequest,
    BriefingResponse,
    BriefingListResponse,
    SendBriefingRequest,
    SendBriefingResponse,
    ErrorResponse
)

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
        from daily_briefing_workflow import run_daily_briefing_workflow

        logger.info(f"브리핑 생성 시작: {request.dict()}")

        # 브리핑 생성 워크플로우 실행
        result = run_daily_briefing_workflow()

        if not result or not result.get('briefing_data'):
            raise HTTPException(
                status_code=500,
                detail={
                    "success": False,
                    "error": {
                        "code": "GENERATION_ERROR",
                        "message": "브리핑 생성에 실패했습니다",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )

        briefing_data = result['briefing_data']
        top_stock = result.get('stock_data', {})

        # 브리핑 ID 생성
        briefing_id = f"brf_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # 이미지 URL 생성 (실제로는 CDN에 업로드 후 URL 반환)
        image_path = briefing_data.get('image_path', '')
        image_url = f"http://localhost:8000/briefings/images/{briefing_id}.png" if image_path else ""

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
        logger.info(f"브리핑 목록 조회: page={page}, limit={limit}")

        # TODO: 실제로는 데이터베이스에서 조회
        # 현재는 샘플 데이터 반환
        briefings = []
        total = 0

        return {
            "success": True,
            "data": {
                "briefings": briefings,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": total,
                    "total_pages": (total + limit - 1) // limit if total > 0 else 0,
                    "has_next": page * limit < total,
                    "has_prev": page > 1
                }
            }
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
        logger.info(f"브리핑 상세 조회: {briefing_id}")

        # TODO: 실제로는 데이터베이스에서 조회
        raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "error": {
                    "code": "BRIEFING_NOT_FOUND",
                    "message": f"브리핑을 찾을 수 없습니다: {briefing_id}",
                    "timestamp": datetime.now().isoformat()
                }
            }
        )

    except HTTPException:
        raise
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

        # TODO: 실제 발송 로직 구현
        send_job_id = f"job_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        channel_results = []
        for channel in request.channels:
            result = {
                "type": channel.type,
                "status": "sent",
                "sent_at": datetime.now().isoformat()
            }

            if channel.type == "email":
                result["email"] = channel.email
                result["message_id"] = f"msg_email_{datetime.now().timestamp()}"
            elif channel.type == "slack":
                result["slack_channel"] = channel.slack_channel
                result["message_id"] = f"msg_slack_{datetime.now().timestamp()}"

            channel_results.append(result)

        return {
            "success": True,
            "data": {
                "briefing_id": briefing_id,
                "send_job_id": send_job_id,
                "status": "sent" if request.send_immediately else "scheduled",
                "channels": channel_results,
                "total_sent": len(channel_results),
                "total_failed": 0
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
