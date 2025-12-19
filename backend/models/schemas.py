"""
Pydantic 스키마 정의
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# ============= 공통 응답 스키마 =============

class ErrorDetail(BaseModel):
    """에러 상세 정보"""
    code: str
    message: str
    details: Optional[dict] = None
    request_id: Optional[str] = None
    timestamp: str


class ErrorResponse(BaseModel):
    """에러 응답"""
    success: bool = False
    error: ErrorDetail


# ============= 주식 관련 스키마 =============

class StockData(BaseModel):
    """주식 기본 정보"""
    symbol: str
    name: str
    price: float
    change_percent: float
    volume: int
    market_cap: int
    score: float = 0.0
    screener_types: List[str] = []
    timestamp: str


class TrendingStocksData(BaseModel):
    """화제 종목 데이터"""
    stocks: List[StockData]
    total: int
    generated_at: str


class TrendingStocksResponse(BaseModel):
    """화제 종목 응답"""
    success: bool = True
    data: TrendingStocksData


class NewsItem(BaseModel):
    """뉴스 항목"""
    title: str
    source: str
    published_at: str
    url: str
    summary: str


class StockDetailData(BaseModel):
    """주식 상세 정보"""
    symbol: str
    name: str
    description: str
    current_price: float
    previous_close: float
    change: float
    change_percent: float
    volume: int
    average_volume: int
    market_cap: int
    pe_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    week_52_high: Optional[float] = Field(None, alias="52_week_high")
    week_52_low: Optional[float] = Field(None, alias="52_week_low")
    sector: str
    industry: str
    news: List[NewsItem] = []
    updated_at: str

    class Config:
        populate_by_name = True


class StockDetailResponse(BaseModel):
    """주식 상세 정보 응답"""
    success: bool = True
    data: StockDetailData


# ============= 브리핑 관련 스키마 =============

class BriefingCreateRequest(BaseModel):
    """브리핑 생성 요청"""
    stock_symbols: Optional[List[str]] = None
    screener_types: List[str] = ["most_actives", "day_gainers"]
    count: int = Field(5, ge=1, le=10)
    format: str = Field("both", pattern="^(image|text|both)$")
    language: str = Field("ko", pattern="^(ko|en)$")
    template_id: Optional[str] = None


class BriefingStockInfo(BaseModel):
    """브리핑에 포함된 주식 정보"""
    symbol: str
    name: str
    price: float
    change_percent: float
    volume: int


class BriefingTextContent(BaseModel):
    """브리핑 텍스트 내용"""
    title: str
    summary: str
    sections: List[dict] = []


class BriefingImageContent(BaseModel):
    """브리핑 이미지 내용"""
    url: str
    thumbnail_url: Optional[str] = None
    width: int = 1200
    height: int = 1600
    format: str = "png"


class BriefingContent(BaseModel):
    """브리핑 콘텐츠"""
    text: Optional[BriefingTextContent] = None
    image: Optional[BriefingImageContent] = None


class BriefingMetadata(BaseModel):
    """브리핑 메타데이터"""
    template_used: str
    generation_time_ms: Optional[int] = None
    ai_model: str = "gemini-pro"
    language: str = "ko"


class BriefingData(BaseModel):
    """브리핑 데이터"""
    briefing_id: str
    generated_at: str
    status: str
    stocks_included: List[BriefingStockInfo]
    content: BriefingContent
    metadata: BriefingMetadata


class BriefingResponse(BaseModel):
    """브리핑 생성 응답"""
    success: bool = True
    data: BriefingData


class BriefingAsyncData(BaseModel):
    """브리핑 비동기 처리 데이터"""
    briefing_id: str
    status: str = "processing"
    estimated_completion_time: str
    check_status_url: str


class BriefingAsyncResponse(BaseModel):
    """브리핑 비동기 응답"""
    success: bool = True
    data: BriefingAsyncData


# ============= 발송 관련 스키마 =============

class SendChannel(BaseModel):
    """발송 채널"""
    type: str = Field(..., pattern="^(email|slack)$")
    email: Optional[str] = None
    slack_webhook_url: Optional[str] = None
    slack_channel: Optional[str] = "#general"


class SendBriefingRequest(BaseModel):
    """브리핑 발송 요청"""
    channels: List[SendChannel]
    send_immediately: bool = True
    scheduled_at: Optional[str] = None


class SendChannelResult(BaseModel):
    """발송 채널 결과"""
    type: str
    email: Optional[str] = None
    slack_channel: Optional[str] = None
    status: str
    sent_at: Optional[str] = None
    message_id: Optional[str] = None


class SendBriefingData(BaseModel):
    """브리핑 발송 데이터"""
    briefing_id: str
    send_job_id: str
    status: str
    channels: List[SendChannelResult]
    total_sent: int = 0
    total_failed: int = 0


class SendBriefingResponse(BaseModel):
    """브리핑 발송 응답"""
    success: bool = True
    data: SendBriefingData


# ============= 브리핑 히스토리 스키마 =============

class BriefingListItem(BaseModel):
    """브리핑 목록 항목"""
    briefing_id: str
    generated_at: str
    status: str
    stocks_count: int
    stocks: List[dict]
    content: dict
    sent_channels: List[str] = []
    view_count: int = 0


class PaginationInfo(BaseModel):
    """페이지네이션 정보"""
    page: int
    limit: int
    total: int
    total_pages: int
    has_next: bool
    has_prev: bool


class BriefingListData(BaseModel):
    """브리핑 목록 데이터"""
    briefings: List[BriefingListItem]
    pagination: PaginationInfo


class BriefingListResponse(BaseModel):
    """브리핑 목록 응답"""
    success: bool = True
    data: BriefingListData


# ============= 인증 관련 스키마 =============

class LoginRequest(BaseModel):
    """로그인 요청"""
    email: str
    password: str


class UserInfo(BaseModel):
    """사용자 정보"""
    id: str
    email: str
    name: str
    plan: str = "free"


class LoginData(BaseModel):
    """로그인 데이터"""
    token: str
    token_type: str = "Bearer"
    expires_at: str
    expires_in: int = 86400
    user: UserInfo


class LoginResponse(BaseModel):
    """로그인 응답"""
    success: bool = True
    data: LoginData
