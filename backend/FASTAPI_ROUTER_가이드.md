# FastAPI APIRouter 사용법 가이드

## 목차
1. [기본 개념](#기본-개념)
2. [프로젝트 구조](#프로젝트-구조)
3. [기본 사용법](#기본-사용법)
4. [실전 예제](#실전-예제)
5. [프로젝트 적용 예제](#프로젝트-적용-예제)

---

## 기본 개념

### APIRouter란?
- FastAPI의 라우팅을 모듈화하는 도구
- 여러 엔드포인트를 그룹화하여 관리
- 코드 구조를 깔끔하게 유지

### 왜 APIRouter를 사용하나?
```python
# ❌ 나쁜 예: 모든 라우트를 main.py에 작성
@app.get("/stocks")
@app.get("/briefings")
@app.get("/users")
# ... 수백 개의 엔드포인트

# ✅ 좋은 예: 기능별로 분리
# routers/stocks.py
# routers/briefings.py
# routers/users.py
```

---

## 프로젝트 구조

```
backend/
├── main.py                    # FastAPI 앱 진입점
├── routers/                   # 라우터 모듈들
│   ├── __init__.py
│   ├── stocks.py             # 주식 관련 엔드포인트
│   ├── briefings.py          # 브리핑 관련 엔드포인트
│   └── auth.py               # 인증 관련 엔드포인트
├── models/                    # 데이터 모델
│   ├── __init__.py
│   └── schemas.py
├── services/                  # 비즈니스 로직
│   ├── __init__.py
│   ├── stock_service.py
│   └── briefing_service.py
└── dependencies.py            # 공통 의존성
```

---

## 기본 사용법

### 1. 간단한 예제

**routers/example.py**
```python
from fastapi import APIRouter

# APIRouter 생성
router = APIRouter()

# 라우트 정의
@router.get("/hello")
def hello():
    return {"message": "Hello World"}

@router.get("/hello/{name}")
def hello_name(name: str):
    return {"message": f"Hello {name}"}
```

**main.py**
```python
from fastapi import FastAPI
from routers import example

# FastAPI 앱 생성
app = FastAPI()

# 라우터 등록
app.include_router(example.router)

# 이제 /hello, /hello/{name} 엔드포인트가 생성됨
```

---

### 2. Prefix와 Tags 사용

```python
from fastapi import APIRouter

# prefix: 모든 라우트에 /api/v1 접두사 추가
# tags: Swagger 문서에서 그룹화
router = APIRouter(
    prefix="/api/v1",
    tags=["stocks"]
)

@router.get("/trending")  # 실제 경로: /api/v1/trending
def get_trending():
    return {"stocks": []}

@router.get("/{symbol}")  # 실제 경로: /api/v1/{symbol}
def get_stock(symbol: str):
    return {"symbol": symbol}
```

**main.py에서 등록**
```python
from fastapi import FastAPI
from routers import stocks

app = FastAPI()

# 라우터 등록 (prefix는 이미 라우터에 정의됨)
app.include_router(stocks.router)
```

---

### 3. 의존성(Dependencies) 사용

```python
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()

# 의존성 함수
def verify_token(token: str):
    if token != "secret":
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

# 특정 라우트에 의존성 적용
@router.get("/protected")
def protected_route(token: str = Depends(verify_token)):
    return {"message": "You have access"}

# 또는 라우터 전체에 의존성 적용
router = APIRouter(
    dependencies=[Depends(verify_token)]
)

@router.get("/all-protected")
def another_protected():
    return {"message": "This is also protected"}
```

---

## 실전 예제

### 예제 1: CRUD API

**routers/items.py**
```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

# 요청/응답 모델
class Item(BaseModel):
    id: int
    name: str
    price: float

class ItemCreate(BaseModel):
    name: str
    price: float

# 가짜 데이터베이스
items_db = []

# CREATE
@router.post("", response_model=Item)
def create_item(item: ItemCreate):
    new_item = Item(
        id=len(items_db) + 1,
        name=item.name,
        price=item.price
    )
    items_db.append(new_item)
    return new_item

# READ (전체 목록)
@router.get("", response_model=List[Item])
def get_items():
    return items_db

# READ (단일 항목)
@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# UPDATE
@router.put("/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: ItemCreate):
    for idx, item in enumerate(items_db):
        if item.id == item_id:
            items_db[idx] = Item(
                id=item_id,
                name=updated_item.name,
                price=updated_item.price
            )
            return items_db[idx]
    raise HTTPException(status_code=404, detail="Item not found")

# DELETE
@router.delete("/{item_id}")
def delete_item(item_id: int):
    for idx, item in enumerate(items_db):
        if item.id == item_id:
            items_db.pop(idx)
            return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")
```

---

## 프로젝트 적용 예제

### 1. 화제 종목 API 라우터

**routers/stocks.py**
```python
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# 기존 모듈 임포트
import sys
sys.path.append('..')
from get_trending_stocks import get_trending_stocks, format_stock_data

router = APIRouter(
    prefix="/v1/trending-stocks",
    tags=["stocks"]
)

# 응답 모델 정의
class StockResponse(BaseModel):
    symbol: str
    name: str
    price: float
    change_percent: float
    volume: int
    market_cap: int
    score: float = 0.0
    screener_types: List[str] = []
    timestamp: str

class TrendingStocksResponse(BaseModel):
    success: bool
    data: dict

# GET /v1/trending-stocks
@router.get("", response_model=TrendingStocksResponse)
def get_trending_stocks_api(
    screener_types: str = Query("most_actives,day_gainers", description="스크리너 타입 (콤마로 구분)"),
    count: int = Query(10, ge=1, le=50, description="각 스크리너당 종목 수"),
    limit: int = Query(10, ge=1, le=100, description="최종 반환 종목 수"),
    min_volume: Optional[int] = Query(None, description="최소 거래량 필터"),
    sort_by: str = Query("score", description="정렬 기준"),
    order: str = Query("desc", description="정렬 순서")
):
    """
    Yahoo Finance Screener를 활용하여 화제 종목 목록을 조회합니다.
    """
    try:
        # 스크리너 타입 파싱
        screener_list = [s.strip() for s in screener_types.split(",")]

        # 데이터 가져오기
        stocks_data = get_trending_stocks(
            screener_types=screener_list,
            count=count
        )

        # 데이터 포맷팅
        formatted_stocks = []
        for screener_type, quotes in stocks_data.items():
            for quote in quotes[:limit]:
                stock = format_stock_data(quote)
                stock['screener_types'] = [screener_type]
                stock['score'] = 0.8  # 임시 점수
                formatted_stocks.append(stock)

        # 필터링
        if min_volume:
            formatted_stocks = [s for s in formatted_stocks if s['volume'] >= min_volume]

        # 정렬
        reverse = (order == "desc")
        formatted_stocks.sort(key=lambda x: x.get(sort_by, 0), reverse=reverse)

        return {
            "success": True,
            "data": {
                "stocks": formatted_stocks[:limit],
                "total": len(formatted_stocks),
                "generated_at": datetime.now().isoformat()
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

### 2. 종목 상세 정보 API

**routers/stocks.py (계속)**
```python
from yahooquery import Ticker

@router.get("/{symbol}")
def get_stock_detail(
    symbol: str,
    include_news: bool = Query(True, description="관련 뉴스 포함 여부"),
    news_limit: int = Query(5, ge=1, le=20, description="뉴스 개수")
):
    """
    특정 종목의 상세 정보와 관련 뉴스를 조회합니다.
    """
    try:
        ticker = Ticker(symbol)

        # 기본 정보
        quote = ticker.quotes[symbol]
        summary = ticker.summary_detail[symbol]
        profile = ticker.summary_profile.get(symbol, {})

        result = {
            "success": True,
            "data": {
                "symbol": symbol,
                "name": quote.get("shortName", ""),
                "description": profile.get("longBusinessSummary", ""),
                "current_price": quote.get("regularMarketPrice", 0),
                "previous_close": quote.get("regularMarketPreviousClose", 0),
                "change": quote.get("regularMarketChange", 0),
                "change_percent": quote.get("regularMarketChangePercent", 0),
                "volume": quote.get("regularMarketVolume", 0),
                "market_cap": quote.get("marketCap", 0),
                "sector": profile.get("sector", ""),
                "industry": profile.get("industry", ""),
                "updated_at": datetime.now().isoformat()
            }
        }

        # 뉴스 추가 (선택적)
        if include_news:
            # 실제로는 Exa API나 다른 뉴스 소스 사용
            result["data"]["news"] = []

        return result

    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Stock {symbol} not found or error occurred: {str(e)}"
        )
```

---

### 3. 브리핑 생성 API

**routers/briefings.py**
```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import sys
sys.path.append('..')
from daily_briefing_workflow import run_daily_briefing_workflow

router = APIRouter(
    prefix="/v1/briefings",
    tags=["briefings"]
)

# 요청 모델
class BriefingCreateRequest(BaseModel):
    stock_symbols: Optional[List[str]] = None
    screener_types: List[str] = ["most_actives", "day_gainers"]
    count: int = 5
    format: str = "both"  # image, text, both
    language: str = "ko"  # ko, en
    template_id: Optional[str] = None

# 응답 모델
class BriefingResponse(BaseModel):
    success: bool
    data: dict

# POST /v1/briefings
@router.post("", response_model=BriefingResponse, status_code=200)
def create_briefing(request: BriefingCreateRequest):
    """
    화제 종목 정보를 기반으로 AI 브리핑(이미지 + 텍스트)을 생성합니다.
    """
    try:
        # 브리핑 생성 워크플로우 실행
        result = run_daily_briefing_workflow()

        if not result or not result.get('briefing_data'):
            raise HTTPException(
                status_code=500,
                detail="브리핑 생성에 실패했습니다."
            )

        briefing_data = result['briefing_data']

        return {
            "success": True,
            "data": {
                "briefing_id": f"brf_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "generated_at": datetime.now().isoformat(),
                "status": "completed",
                "stocks_included": result.get('top_stock', {}),
                "content": {
                    "text": briefing_data.get('text_content'),
                    "image": {
                        "url": briefing_data.get('image_path', '')
                    }
                },
                "metadata": {
                    "template_used": request.template_id or "default_v1",
                    "ai_model": "gemini-pro",
                    "language": request.language
                }
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# GET /v1/briefings (목록 조회)
@router.get("", response_model=BriefingResponse)
def get_briefings(
    page: int = Query(1, ge=1, description="페이지 번호"),
    limit: int = Query(20, ge=1, le=100, description="페이지당 항목 수")
):
    """
    생성된 브리핑 목록을 조회합니다.
    """
    # TODO: 데이터베이스에서 조회
    return {
        "success": True,
        "data": {
            "briefings": [],
            "pagination": {
                "page": page,
                "limit": limit,
                "total": 0,
                "total_pages": 0
            }
        }
    }

# GET /v1/briefings/{briefing_id}
@router.get("/{briefing_id}", response_model=BriefingResponse)
def get_briefing(briefing_id: str):
    """
    특정 브리핑의 상세 정보를 조회합니다.
    """
    # TODO: 데이터베이스에서 조회
    raise HTTPException(status_code=404, detail="Briefing not found")
```

---

### 4. 메인 앱 구성

**main.py**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import stocks, briefings

# FastAPI 앱 생성
app = FastAPI(
    title="당신이 잠든 사이 API",
    description="미국 증시 화제 종목 브리핑 서비스",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(stocks.router)
app.include_router(briefings.router)

# 헬스체크 엔드포인트
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# 루트 엔드포인트
@app.get("/")
def root():
    return {
        "message": "당신이 잠든 사이 API",
        "version": "1.0.0",
        "docs": "/docs"
    }

# 실행 (개발 환경)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

### 5. 실행 방법

```bash
# 1. FastAPI 설치
pip install fastapi uvicorn pydantic

# 2. 서버 실행
python main.py

# 또는
uvicorn main:app --reload

# 3. API 문서 확인
# http://localhost:8000/docs (Swagger UI)
# http://localhost:8000/redoc (ReDoc)

# 4. API 테스트
curl http://localhost:8000/v1/trending-stocks
```

---

## 핵심 포인트

### 1. APIRouter 생성
```python
router = APIRouter(
    prefix="/api/v1",     # URL 접두사
    tags=["stocks"],      # Swagger 그룹
    dependencies=[...]    # 공통 의존성
)
```

### 2. 라우트 정의
```python
@router.get("/path")
@router.post("/path")
@router.put("/path")
@router.delete("/path")
```

### 3. 라우터 등록
```python
app.include_router(router)
```

### 4. 모듈화 장점
- 코드 구조가 명확
- 유지보수 용이
- 팀 협업에 유리
- 테스트 작성 쉬움

---

## 다음 단계

1. **데이터베이스 연동**: SQLAlchemy 또는 MongoDB 연동
2. **인증 구현**: JWT 토큰 기반 인증
3. **에러 처리**: 전역 예외 핸들러
4. **로깅**: 요청/응답 로깅
5. **테스트**: pytest로 API 테스트 작성
6. **배포**: Docker, Nginx 설정

이 가이드를 참고하여 프로젝트에 FastAPI를 적용할 수 있습니다!
