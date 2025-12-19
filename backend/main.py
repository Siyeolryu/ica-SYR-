"""
당신이 잠든 사이 - FastAPI 메인 애플리케이션
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from api import stocks, briefings, auth
from routers import news
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Lifespan 이벤트 관리
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 FastAPI 서버 시작")
    logger.info("📖 API 문서: http://localhost:8000/docs")

    # 스케줄러 시작 (선택사항 - 환경 변수로 제어)
    import os
    if os.getenv('ENABLE_SCHEDULER', 'false').lower() == 'true':
        try:
            from apscheduler.schedulers.background import BackgroundScheduler
            from apscheduler.triggers.cron import CronTrigger
            from scheduler import run_briefing_job

            scheduler = BackgroundScheduler(timezone='Asia/Seoul')
            scheduler.add_job(
                func=run_briefing_job,
                trigger=CronTrigger(hour=7, minute=0),
                id='daily_briefing_job',
                name='매일 아침 브리핑 생성'
            )
            scheduler.start()
            logger.info("📅 스케줄러 시작: 매일 오전 7시 브리핑 자동 생성")
        except Exception as e:
            logger.warning(f"스케줄러 시작 실패: {str(e)}")

    yield

    # Shutdown
    logger.info("🛑 FastAPI 서버 종료")


# FastAPI 앱 생성
app = FastAPI(
    title="당신이 잠든 사이 REST API",
    description="미국 증시 화제 종목 브리핑 서비스 API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Next.js 개발 서버
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(stocks.router, prefix="/v1")
app.include_router(briefings.router, prefix="/v1")
app.include_router(auth.router, prefix="/v1/auth")
app.include_router(news.router, prefix="/v1")  # Exa 뉴스 API

# 헬스체크 엔드포인트
@app.get("/health", tags=["Health"])
def health_check():
    """서버 상태 확인"""
    return {
        "status": "healthy",
        "version": "1.0.0"
    }

# 루트 엔드포인트
@app.get("/", tags=["Root"])
def root():
    """API 루트"""
    return {
        "message": "당신이 잠든 사이 REST API v1.0",
        "docs": "/docs",
        "health": "/health"
    }

# 실행 (개발 환경)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
