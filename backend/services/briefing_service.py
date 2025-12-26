"""
브리핑 관련 비즈니스 로직
"""
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
import json
import logging
import os

logger = logging.getLogger(__name__)

# 출력 디렉토리 설정
OUTPUT_DIR = Path(__file__).parent.parent / 'output'
OUTPUT_DIR.mkdir(exist_ok=True)


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
        브리핑 목록 조회 - output 폴더의 파일들을 스캔

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

        try:
            # output 폴더에서 JSON 파일 찾기
            json_files = list(OUTPUT_DIR.glob("briefing_*.json"))
            
            briefings = []
            
            for json_file in sorted(json_files, key=lambda x: x.stat().st_mtime, reverse=True):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    briefing_data = data.get('briefing', {})
                    stock_data = data.get('stock_data', {})
                    
                    # 브리핑 ID 생성 (파일명 기반)
                    briefing_id = json_file.stem
                    
                    # 생성 시간
                    generated_at = briefing_data.get('generated_at') or data.get('created_at', '')
                    
                    # 날짜 필터링
                    if start_date and generated_at < start_date:
                        continue
                    if end_date and generated_at > end_date:
                        continue
                    
                    # 종목 필터링
                    if stock_symbol:
                        stock_sym = stock_data.get('symbol', '') or briefing_data.get('stock_symbol', '')
                        if stock_sym.upper() != stock_symbol.upper():
                            continue
                    
                    # 이미지 경로 찾기
                    image_url = None
                    image_path = briefing_data.get('image_path', '')
                    
                    # 절대 경로인 경우 처리
                    if image_path and os.path.exists(image_path):
                        try:
                            # 상대 경로로 변환
                            rel_path = os.path.relpath(image_path, OUTPUT_DIR)
                            image_url = f"http://localhost:8000/api/briefings/files/{rel_path.replace(os.sep, '/')}"
                        except ValueError:
                            # OUTPUT_DIR 밖에 있는 경우 절대 경로 사용 불가
                            pass
                    
                    # 이미지 파일 찾기 (여러 패턴 시도)
                    if not image_url:
                        # 패턴 1: briefing_ID.png
                        image_file = json_file.parent / f"{briefing_id}.png"
                        if not image_file.exists():
                            # 패턴 2: briefing_card_ID.png
                            pattern = briefing_id.replace('briefing_', 'briefing_card_')
                            image_file = json_file.parent / f"{pattern}.png"
                        if not image_file.exists():
                            # 패턴 3: JSON 파일명과 유사한 PNG 파일 찾기
                            base_name = json_file.stem
                            # briefing_NVDA_20251226_194439 -> briefing_NVDA_20251226_194438
                            if '_' in base_name:
                                parts = base_name.split('_')
                                if len(parts) >= 3:
                                    # 마지막 숫자 부분을 하나 줄여서 찾기
                                    try:
                                        last_num = int(parts[-1])
                                        new_parts = parts[:-1] + [str(last_num - 1).zfill(len(parts[-1]))]
                                        alt_name = '_'.join(new_parts)
                                        image_file = json_file.parent / f"{alt_name}.png"
                                    except ValueError:
                                        pass
                        if image_file.exists():
                            rel_path = os.path.relpath(image_file, OUTPUT_DIR)
                            image_url = f"http://localhost:8000/api/briefings/files/{rel_path.replace(os.sep, '/')}"
                    
                    # DOCX 파일 찾기
                    docx_file = json_file.parent / 'reports' / f"briefing_report_{briefing_id}.docx"
                    if not docx_file.exists():
                        docx_file = json_file.parent / f"{briefing_id.replace('briefing_', 'briefing_')}.docx"
                    docx_url = None
                    if docx_file.exists():
                        rel_path = os.path.relpath(docx_file, OUTPUT_DIR)
                        docx_url = f"/api/briefings/files/{rel_path.replace(os.sep, '/')}"
                    
                    # 종목 정보 추출
                    stocks_included = []
                    if stock_data:
                        stocks_included.append({
                            "symbol": stock_data.get('symbol', ''),
                            "name": stock_data.get('name', ''),
                            "price": stock_data.get('price', 0),
                            "change_percent": stock_data.get('change_percent', 0),
                            "volume": stock_data.get('volume', 0)
                        })
                    
                    # 브리핑 항목 구성
                    briefing_item = {
                        "briefing_id": briefing_id,
                        "generated_at": generated_at,
                        "status": "completed",
                        "stocks_count": len(stocks_included),
                        "stocks": stocks_included,
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
                            "template_used": "default_v1",
                            "ai_model": "gemini-pro",
                            "language": "ko",
                            "docx_url": docx_url
                        },
                        "sent_channels": [],
                        "view_count": 0
                    }
                    
                    briefings.append(briefing_item)
                    
                except Exception as e:
                    logger.warning(f"브리핑 파일 읽기 실패: {json_file.name}, 오류: {str(e)}")
                    continue
            
            # 페이지네이션
            total = len(briefings)
            start_idx = (page - 1) * limit
            end_idx = start_idx + limit
            paginated_briefings = briefings[start_idx:end_idx]
            
            return {
                "briefings": paginated_briefings,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": total,
                    "total_pages": (total + limit - 1) // limit if total > 0 else 0,
                    "has_next": end_idx < total,
                    "has_prev": page > 1
                }
            }
            
        except Exception as e:
            logger.error(f"브리핑 목록 조회 중 오류: {str(e)}")
            return {
                "briefings": [],
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": 0,
                    "total_pages": 0,
                    "has_next": False,
                    "has_prev": False
                }
            }

    @staticmethod
    def get_briefing_by_id(briefing_id: str) -> Dict:
        """
        브리핑 상세 조회 - output 폴더에서 JSON 파일 읽기

        Args:
            briefing_id: 브리핑 ID

        Returns:
            브리핑 상세 정보
        """
        logger.info(f"브리핑 상세 조회: {briefing_id}")

        try:
            # JSON 파일 찾기
            json_file = OUTPUT_DIR / f"{briefing_id}.json"
            
            if not json_file.exists():
                raise ValueError(f"브리핑을 찾을 수 없습니다: {briefing_id}")
            
            # JSON 파일 읽기
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            briefing_data = data.get('briefing', {})
            stock_data = data.get('stock_data', {})
            
            # 이미지 경로 찾기
            image_url = None
            image_path = briefing_data.get('image_path', '')
            
            # 절대 경로인 경우 처리
            if image_path and os.path.exists(image_path):
                try:
                    rel_path = os.path.relpath(image_path, OUTPUT_DIR)
                    image_url = f"http://localhost:8000/api/briefings/files/{rel_path.replace(os.sep, '/')}"
                except ValueError:
                    pass
            
            # 이미지 파일 찾기 (여러 패턴 시도)
            if not image_url:
                json_file = OUTPUT_DIR / f"{briefing_id}.json"
                # 패턴 1: briefing_ID.png
                image_file = OUTPUT_DIR / f"{briefing_id}.png"
                if not image_file.exists():
                    # 패턴 2: briefing_card_ID.png
                    pattern = briefing_id.replace('briefing_', 'briefing_card_')
                    image_file = OUTPUT_DIR / f"{pattern}.png"
                if not image_file.exists() and json_file.exists():
                    # 패턴 3: JSON 파일명과 유사한 PNG 파일 찾기
                    base_name = json_file.stem
                    if '_' in base_name:
                        parts = base_name.split('_')
                        if len(parts) >= 3:
                            try:
                                last_num = int(parts[-1])
                                new_parts = parts[:-1] + [str(last_num - 1).zfill(len(parts[-1]))]
                                alt_name = '_'.join(new_parts)
                                image_file = OUTPUT_DIR / f"{alt_name}.png"
                            except ValueError:
                                pass
                if image_file.exists():
                    rel_path = os.path.relpath(image_file, OUTPUT_DIR)
                    image_url = f"http://localhost:8000/api/briefings/files/{rel_path.replace(os.sep, '/')}"
            
            # DOCX 파일 찾기
            docx_file = OUTPUT_DIR / 'reports' / f"briefing_report_{briefing_id}.docx"
            if not docx_file.exists():
                docx_file = OUTPUT_DIR / f"{briefing_id.replace('briefing_', 'briefing_')}.docx"
            docx_url = None
            if docx_file.exists():
                rel_path = os.path.relpath(docx_file, OUTPUT_DIR)
                docx_url = f"/api/briefings/files/{rel_path.replace(os.sep, '/')}"
            
            # 종목 정보 추출
            stocks_included = []
            if stock_data:
                stocks_included.append({
                    "symbol": stock_data.get('symbol', ''),
                    "name": stock_data.get('name', ''),
                    "price": stock_data.get('price', 0),
                    "change_percent": stock_data.get('change_percent', 0),
                    "volume": stock_data.get('volume', 0)
                })
            
            return {
                "briefing_id": briefing_id,
                "generated_at": briefing_data.get('generated_at') or data.get('created_at', ''),
                "status": "completed",
                "stocks_included": stocks_included,
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
                    "template_used": "default_v1",
                    "generation_time_ms": 0,
                    "ai_model": "gemini-pro",
                    "language": "ko",
                    "docx_url": docx_url
                }
            }
            
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"브리핑 상세 조회 중 오류: {str(e)}")
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
