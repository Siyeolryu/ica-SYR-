"""
브리핑 관련 비즈니스 로직 (리팩토링 완료)

리팩토링 내용:
1. 상수 정의 - URL, 기본값 하드코딩 제거
2. 함수 분리 - 채널 처리 로직 별도 메서드로 추출
3. 타입 힌트 개선
4. 페이지네이션 로직 메서드 분리
"""
from typing import Dict, List, Optional
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)


class BriefingService:
    """브리핑 생성 및 관리 서비스"""

    # ========================================================================
    # 상수 정의
    # ========================================================================

    # 서버 설정
    BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
    IMAGE_URL_PATTERN = "{base_url}/briefings/images/{briefing_id}.png"

    # 브리핑 설정
    DEFAULT_BRIEFING_FORMAT = "both"  # text, image, both
    DEFAULT_LANGUAGE = "ko"  # ko, en
    DEFAULT_STOCK_COUNT = 5

    # 페이지네이션 기본값
    DEFAULT_PAGE = 1
    DEFAULT_LIMIT = 20
    MAX_LIMIT = 100

    # 채널 타입
    CHANNEL_TYPE_EMAIL = 'email'
    CHANNEL_TYPE_SLACK = 'slack'
    SLACK_DEFAULT_CHANNEL = '#general'

    # ========================================================================
    # Public Methods - Briefing Creation
    # ========================================================================

    @staticmethod
    def create_briefing(
        stock_symbols: Optional[List[str]] = None,
        format_type: str = DEFAULT_BRIEFING_FORMAT,
        language: str = DEFAULT_LANGUAGE,
        count: int = DEFAULT_STOCK_COUNT
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

        Raises:
            ValueError: 브리핑 생성 실패
        """
        from daily_briefing_workflow import run_daily_briefing_workflow

        logger.info(f"브리핑 생성 시작: symbols={stock_symbols}, format={format_type}")

        # 브리핑 생성 워크플로우 실행
        result = run_daily_briefing_workflow()

        if not result or not result.get('briefing_data'):
            raise ValueError("브리핑 생성에 실패했습니다")

        # 결과 파싱
        briefing_data = result['briefing_data']
        top_stock = result.get('stock_data', {})

        # 브리핑 ID 생성
        briefing_id = BriefingService._generate_briefing_id()

        # 이미지 URL 생성
        image_path = briefing_data.get('image_path', '')
        image_url = BriefingService._generate_image_url(briefing_id) if image_path else ""

        logger.info(f"브리핑 생성 완료: {briefing_id}")

        return {
            "briefing_id": briefing_id,
            "briefing_data": briefing_data,
            "stock_data": top_stock,
            "image_url": image_url,
            "generation_time_ms": result.get('generation_time_ms', 0)
        }

    # ========================================================================
    # Public Methods - Briefing Retrieval
    # ========================================================================

    @staticmethod
    def get_briefings(
        page: int = DEFAULT_PAGE,
        limit: int = DEFAULT_LIMIT,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        stock_symbol: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict:
        """
        브리핑 목록 조회

        Args:
            page: 페이지 번호
            limit: 페이지당 항목 수 (최대 100)
            start_date: 시작 날짜 (YYYY-MM-DD)
            end_date: 종료 날짜 (YYYY-MM-DD)
            stock_symbol: 종목 필터
            status: 상태 필터 (draft, published, archived)

        Returns:
            브리핑 목록 및 페이지네이션 정보
        """
        logger.info(f"브리핑 목록 조회: page={page}, limit={limit}")

        # Limit 검증
        limit = min(limit, BriefingService.MAX_LIMIT)

        # TODO: 실제로는 데이터베이스에서 조회
        # briefings = db.query(Briefing).filter(...).offset((page-1)*limit).limit(limit).all()
        briefings = []
        total = 0

        # 페이지네이션 정보 구성
        pagination = BriefingService._build_pagination(page, limit, total)

        return {
            "briefings": briefings,
            "pagination": pagination
        }

    @staticmethod
    def get_briefing_by_id(briefing_id: str) -> Dict:
        """
        브리핑 상세 조회

        Args:
            briefing_id: 브리핑 ID

        Returns:
            브리핑 상세 정보

        Raises:
            ValueError: 브리핑을 찾을 수 없음
        """
        logger.info(f"브리핑 상세 조회: {briefing_id}")

        # TODO: 실제로는 데이터베이스에서 조회
        # briefing = db.query(Briefing).filter(Briefing.id == briefing_id).first()
        # if not briefing:
        #     raise ValueError(f"브리핑을 찾을 수 없습니다: {briefing_id}")

        raise ValueError(f"브리핑을 찾을 수 없습니다: {briefing_id}")

    # ========================================================================
    # Public Methods - Briefing Sending
    # ========================================================================

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
            channels: 발송 채널 목록 [{"type": "email", "email": "..."}, ...]
            send_immediately: 즉시 발송 여부

        Returns:
            발송 결과

        Channel Format:
            Email: {"type": "email", "email": "user@example.com"}
            Slack: {"type": "slack", "slack_webhook_url": "...", "slack_channel": "#general"}
        """
        from send_briefing import send_briefing_to_channels

        logger.info(f"브리핑 발송: {briefing_id}, channels={len(channels)}")

        # TODO: 실제 브리핑 데이터 조회
        briefing_data = BriefingService._get_test_briefing_data()

        # 채널별 수신자 추출
        email_recipients, slack_channels = BriefingService._extract_channel_recipients(channels)

        # 발송 실행
        results = send_briefing_to_channels(
            briefing_data=briefing_data,
            image_path=None,
            email_recipients=email_recipients,
            slack_channels=slack_channels
        )

        # 발송 Job ID 생성
        send_job_id = BriefingService._generate_send_job_id()

        logger.info(f"브리핑 발송 완료: {results['total_sent']}개 성공, {results['total_failed']}개 실패")

        return {
            "send_job_id": send_job_id,
            "status": "sent" if send_immediately else "scheduled",
            "total_sent": results['total_sent'],
            "total_failed": results['total_failed'],
            "results": results
        }

    # ========================================================================
    # Private Helper Methods - ID Generation
    # ========================================================================

    @staticmethod
    def _generate_briefing_id() -> str:
        """브리핑 ID 생성 (타임스탬프 기반)"""
        return f"brf_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    @staticmethod
    def _generate_send_job_id() -> str:
        """발송 Job ID 생성 (타임스탬프 기반)"""
        return f"job_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    @staticmethod
    def _generate_image_url(briefing_id: str) -> str:
        """브리핑 이미지 URL 생성"""
        return BriefingService.IMAGE_URL_PATTERN.format(
            base_url=BriefingService.BASE_URL,
            briefing_id=briefing_id
        )

    # ========================================================================
    # Private Helper Methods - Pagination
    # ========================================================================

    @staticmethod
    def _build_pagination(page: int, limit: int, total: int) -> Dict:
        """페이지네이션 정보 구성"""
        total_pages = (total + limit - 1) // limit if total > 0 else 0

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
            "has_next": page * limit < total,
            "has_prev": page > 1
        }

    # ========================================================================
    # Private Helper Methods - Channel Processing
    # ========================================================================

    @staticmethod
    def _extract_channel_recipients(channels: List[Dict]) -> tuple[List[str], List[Dict]]:
        """
        채널 목록에서 수신자 추출

        Args:
            channels: 채널 정보 목록

        Returns:
            (email_recipients, slack_channels) 튜플
        """
        email_recipients = []
        slack_channels = []

        for channel in channels:
            channel_type = channel.get('type')

            if channel_type == BriefingService.CHANNEL_TYPE_EMAIL:
                email = channel.get('email')
                if email:
                    email_recipients.append(email)

            elif channel_type == BriefingService.CHANNEL_TYPE_SLACK:
                webhook_url = channel.get('slack_webhook_url')
                if webhook_url:
                    slack_channels.append({
                        'webhook_url': webhook_url,
                        'channel': channel.get('slack_channel', BriefingService.SLACK_DEFAULT_CHANNEL)
                    })

        return email_recipients, slack_channels

    @staticmethod
    def _get_test_briefing_data() -> Dict:
        """테스트용 브리핑 데이터 반환"""
        return {
            "title": "오늘의 화제 종목 브리핑",
            "summary": "테스트 브리핑입니다.",
            "sections": []
        }
