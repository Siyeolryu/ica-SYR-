"""
매일 아침 7시에 브리핑 워크플로우를 자동 실행하는 스케줄러
"""
import logging
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import sys
from pathlib import Path

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 워크플로우 모듈 임포트
from daily_briefing_workflow import run_daily_briefing_workflow


def job_listener(event):
    """
    스케줄러 작업 실행 이벤트 리스너
    """
    if event.exception:
        logger.error(f"작업 실행 중 오류 발생: {event.exception}")
    else:
        logger.info(f"작업 실행 완료: {event.job_id}")


def run_briefing_job():
    """
    매일 실행될 브리핑 워크플로우 작업
    """
    logger.info("=" * 80)
    logger.info("스케줄된 브리핑 워크플로우 시작")
    logger.info(f"실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 80)
    
    try:
        # 설정 로드 (실제 사용 시 환경 변수나 설정 파일에서 로드)
        config = {
            'email_recipients': [],  # 실제 이메일 주소 리스트
            'slack_channels': []  # 실제 슬랙 채널 리스트
        }
        
        # 워크플로우 실행
        result = run_daily_briefing_workflow(config)
        
        if result['success']:
            logger.info("브리핑 워크플로우 성공적으로 완료")
        else:
            logger.error(f"브리핑 워크플로우 실패: {result.get('error', 'Unknown error')}")
        
        return result
    
    except Exception as e:
        logger.error(f"작업 실행 중 예외 발생: {str(e)}")
        raise


def start_scheduler(hour: int = 7, minute: int = 0):
    """
    스케줄러 시작
    
    Args:
        hour: 실행 시간 (기본값: 7)
        minute: 실행 분 (기본값: 0)
    """
    logger.info("=" * 80)
    logger.info("브리핑 스케줄러 시작")
    logger.info(f"실행 시간: 매일 {hour:02d}:{minute:02d}")
    logger.info("=" * 80)
    
    # BlockingScheduler 생성
    scheduler = BlockingScheduler(timezone='Asia/Seoul')
    
    # 이벤트 리스너 등록
    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    
    # 매일 지정된 시간에 작업 등록
    scheduler.add_job(
        func=run_briefing_job,
        trigger=CronTrigger(hour=hour, minute=minute),
        id='daily_briefing_job',
        name='매일 아침 브리핑 생성',
        replace_existing=True
    )
    
    logger.info("스케줄러가 시작되었습니다. 종료하려면 Ctrl+C를 누르세요.")
    
    try:
        # 스케줄러 실행 (무한 루프)
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("스케줄러 종료 중...")
        scheduler.shutdown()
        logger.info("스케줄러가 종료되었습니다.")


def run_once_now():
    """
    즉시 한 번 실행 (테스트용)
    """
    logger.info("즉시 실행 모드: 브리핑 워크플로우를 지금 실행합니다.")
    return run_briefing_job()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='브리핑 자동 생성 스케줄러')
    parser.add_argument(
        '--run-once',
        action='store_true',
        help='즉시 한 번 실행 (테스트용)'
    )
    parser.add_argument(
        '--hour',
        type=int,
        default=7,
        help='실행 시간 (기본값: 7)'
    )
    parser.add_argument(
        '--minute',
        type=int,
        default=0,
        help='실행 분 (기본값: 0)'
    )
    
    args = parser.parse_args()
    
    if args.run_once:
        # 즉시 실행 모드
        run_once_now()
    else:
        # 스케줄러 모드
        start_scheduler(hour=args.hour, minute=args.minute)

