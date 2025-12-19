"""
브리핑 관련 비즈니스 로직
"""
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BriefingService:
    """브리핑 생성 및 관리 서비스"""

    @staticmethod
    def create_briefing(
        stock_symbols: Optional[List[str]] = None,
        format_type: str = "both",
        language: str = "ko",
        count: int = 5
    ) -> Dict:
        """
        브리핑 생성

        Args:
            stock_symbols: 분석할 종목 심볼 리스트
            format_type: 브리핑 포맷 (text, image, both)
            language: 언어 (ko, en)
            count: 포함할 종목 수

        Returns:
            생성된 브리핑 데이터
        """
        from daily_briefing_workflow import run_daily_briefing_workflow

        logger.info(f"브리핑 생성 시작: symbols={stock_symbols}, format={format_type}")

        # 브리핑 생성 워크플로우 실행
        result = run_daily_briefing_workflow()

        if not result or not result.get('briefing_data'):
            raise ValueError("브리핑 생성에 실패했습니다")

        briefing_data = result['briefing_data']
        top_stock = result.get('stock_data', {})

        # 브리핑 ID 생성
        briefing_id = f"brf_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # 이미지 처리
        image_path = briefing_data.get('image_path', '')
        image_url = f"http://localhost:8000/briefings/images/{briefing_id}.png" if image_path else ""

        logger.info(f"브리핑 생성 완료: {briefing_id}")

        return {
            "briefing_id": briefing_id,
            "briefing_data": briefing_data,
            "stock_data": top_stock,
            "image_url": image_url,
            "generation_time_ms": result.get('generation_time_ms', 0)
        }

    @staticmethod
    def get_briefings(
        page: int = 1,
        limit: int = 20,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        stock_symbol: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict:
        """
        브리핑 목록 조회

        Args:
            page: 페이지 번호
            limit: 페이지당 항목 수
            start_date: 시작 날짜
            end_date: 종료 날짜
            stock_symbol: 종목 필터
            status: 상태 필터

        Returns:
            브리핑 목록 및 페이지네이션 정보
        """
        logger.info(f"브리핑 목록 조회: page={page}, limit={limit}")

        # TODO: 실제로는 데이터베이스에서 조회
        briefings = []
        total = 0

        return {
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

    @staticmethod
    def get_briefing_by_id(briefing_id: str) -> Dict:
        """
        브리핑 상세 조회

        Args:
            briefing_id: 브리핑 ID

        Returns:
            브리핑 상세 정보
        """
        logger.info(f"브리핑 상세 조회: {briefing_id}")

        # TODO: 실제로는 데이터베이스에서 조회
        raise ValueError(f"브리핑을 찾을 수 없습니다: {briefing_id}")

    @staticmethod
    def send_briefing(
        briefing_id: str,
        channels: List[Dict],
        send_immediately: bool = True
    ) -> Dict:
        """
        브리핑 발송

        Args:
            briefing_id: 브리핑 ID
            channels: 발송 채널 목록
            send_immediately: 즉시 발송 여부

        Returns:
            발송 결과
        """
        from send_briefing import send_briefing_to_channels

        logger.info(f"브리핑 발송: {briefing_id}, channels={len(channels)}")

        # TODO: 실제 브리핑 데이터 조회
        briefing_data = {
            "title": "오늘의 화제 종목 브리핑",
            "summary": "테스트 브리핑입니다.",
            "sections": []
        }

        # 채널별 발송
        email_recipients = []
        slack_channels = []

        for channel in channels:
            if channel.get('type') == 'email':
                email_recipients.append(channel.get('email'))
            elif channel.get('type') == 'slack':
                slack_channels.append({
                    'webhook_url': channel.get('slack_webhook_url'),
                    'channel': channel.get('slack_channel', '#general')
                })

        # 발송 실행
        results = send_briefing_to_channels(
            briefing_data=briefing_data,
            image_path=None,
            email_recipients=email_recipients,
            slack_channels=slack_channels
        )

        send_job_id = f"job_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        logger.info(f"브리핑 발송 완료: {results['total_sent']}개 성공, {results['total_failed']}개 실패")

        return {
            "send_job_id": send_job_id,
            "status": "sent" if send_immediately else "scheduled",
            "total_sent": results['total_sent'],
            "total_failed": results['total_failed'],
            "results": results
        }
