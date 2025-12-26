# Image Editor Skill

"당신이 잠든 사이 (While You Were Sleeping)" 프로젝트의 이미지 생성 및 편집 가이드입니다.

## 기술 스택

### Image Generation & Processing
- **AI Generation**: Google Gemini API (gemini-2.0-flash-exp)
- **Image Processing**: Pillow (PIL)
- **Language**: Python 3.x
- **Output Formats**: PNG, JPEG, Base64

### Integration
- **Backend**: FastAPI endpoints for image generation
- **Storage**: `backend/output/` directory
- **Delivery**: Slack webhook integration

## 디렉토리 구조

```
backend/
├── gemini_briefing.py          # 이미지 생성 메인 모듈
├── output/                     # 생성된 이미지 저장소
├── mcp_servers/
│   └── briefing_server.py      # MCP 이미지 생성 서버
└── .env                        # GEMINI_API_KEY 설정
```

## 핵심 기능

### 1. AI 기반 이미지 생성
Google Gemini API를 사용한 브리핑 이미지 자동 생성

### 2. Pillow 기반 이미지 렌더링
텍스트를 시각적 이미지로 변환 (폰트, 레이아웃, 색상)

### 3. 템플릿 기반 브리핑 카드
주식 정보를 포함한 시각적 브리핑 카드 생성

## 이미지 생성 패턴

### 1. 기본 브리핑 이미지 생성

```python
from gemini_briefing import generate_briefing_image

# 브리핑 텍스트
briefing_text = {
    'title': '주식 브리핑 제목',
    'summary': '주요 내용 요약...',
    'details': '상세 분석 내용...'
}

# 종목 데이터
stock_data = {
    'symbol': 'AAPL',
    'name': 'Apple Inc.',
    'price': 150.25,
    'change_percent': 2.5
}

# 이미지 생성
image_path = generate_briefing_image(
    briefing_text=briefing_text,
    stock_data=stock_data,
    language='ko',
    output_path='backend/output/briefing_image.png'
)
```

### 2. Pillow를 사용한 커스텀 이미지 생성

```python
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def create_custom_briefing_card(
    title: str,
    content: str,
    stock_info: dict,
    output_path: str
) -> str:
    """
    커스텀 브리핑 카드 이미지 생성

    Args:
        title: 브리핑 제목
        content: 브리핑 내용
        stock_info: 종목 정보 딕셔너리
        output_path: 저장 경로

    Returns:
        생성된 이미지 경로
    """
    # 이미지 크기 설정 (1200x630 - 소셜 미디어 최적화)
    width, height = 1200, 630

    # 배경 생성 (다크 테마)
    background_color = (17, 24, 39)  # gray-900
    img = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(img)

    # 폰트 설정
    try:
        title_font = ImageFont.truetype("arial.ttf", 48)
        content_font = ImageFont.truetype("arial.ttf", 24)
        info_font = ImageFont.truetype("arial.ttf", 20)
    except:
        title_font = ImageFont.load_default()
        content_font = ImageFont.load_default()
        info_font = ImageFont.load_default()

    # 제목 그리기
    title_color = (255, 255, 255)  # white
    draw.text((50, 50), title, fill=title_color, font=title_font)

    # 내용 그리기
    content_color = (209, 213, 219)  # gray-300
    draw.text((50, 130), content, fill=content_color, font=content_font)

    # 종목 정보 그리기
    symbol = stock_info.get('symbol', 'N/A')
    price = stock_info.get('price', 0)
    change = stock_info.get('change_percent', 0)

    # 변동률에 따른 색상 설정
    change_color = (34, 197, 94) if change >= 0 else (239, 68, 68)  # green-500 or red-500

    info_text = f"{symbol} | ${price:.2f} ({change:+.2f}%)"
    draw.text((50, height - 80), info_text, fill=change_color, font=info_font)

    # 이미지 저장
    img.save(output_path)
    return output_path
```

### 3. 다중 종목 비교 이미지

```python
def create_stock_comparison_image(
    stocks: list,
    title: str = "TOP 5 화제 종목",
    output_path: str = "backend/output/comparison.png"
) -> str:
    """
    여러 종목을 비교하는 이미지 생성

    Args:
        stocks: 종목 리스트 (각 종목은 symbol, price, change_percent 포함)
        title: 이미지 제목
        output_path: 저장 경로

    Returns:
        생성된 이미지 경로
    """
    width, height = 1200, 800
    background_color = (17, 24, 39)
    img = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(img)

    # 제목
    try:
        title_font = ImageFont.truetype("arial.ttf", 56)
        stock_font = ImageFont.truetype("arial.ttf", 32)
    except:
        title_font = ImageFont.load_default()
        stock_font = ImageFont.load_default()

    draw.text((50, 40), title, fill=(255, 255, 255), font=title_font)

    # 종목 리스트 그리기
    y_position = 150
    for i, stock in enumerate(stocks[:5]):  # TOP 5만
        symbol = stock.get('symbol', 'N/A')
        name = stock.get('name', 'Unknown')
        price = stock.get('price', 0)
        change = stock.get('change_percent', 0)

        # 순위 배지
        rank_color = (59, 130, 246)  # blue-500
        draw.ellipse([50, y_position, 100, y_position + 50], fill=rank_color)
        draw.text((65, y_position + 10), f"{i+1}", fill=(255, 255, 255), font=stock_font)

        # 종목 정보
        stock_text = f"{symbol} - {name}"
        draw.text((120, y_position + 5), stock_text, fill=(255, 255, 255), font=stock_font)

        # 가격 및 변동률
        price_text = f"${price:.2f}"
        change_color = (34, 197, 94) if change >= 0 else (239, 68, 68)
        change_text = f"{change:+.2f}%"

        draw.text((700, y_position + 5), price_text, fill=(209, 213, 219), font=stock_font)
        draw.text((900, y_position + 5), change_text, fill=change_color, font=stock_font)

        y_position += 120

    img.save(output_path)
    return output_path
```

## 이미지 템플릿 시스템

### 템플릿 구조

```python
class BriefingImageTemplate:
    """브리핑 이미지 템플릿 클래스"""

    def __init__(self, width=1200, height=630):
        self.width = width
        self.height = height
        self.background_color = (17, 24, 39)  # gray-900
        self.primary_color = (59, 130, 246)   # blue-500
        self.text_color = (255, 255, 255)     # white
        self.secondary_text_color = (209, 213, 219)  # gray-300

    def create_header(self, img, title: str):
        """헤더 영역 생성"""
        draw = ImageDraw.Draw(img)
        # 헤더 배경
        draw.rectangle([0, 0, self.width, 100], fill=self.primary_color)
        # 제목
        try:
            font = ImageFont.truetype("arial.ttf", 48)
        except:
            font = ImageFont.load_default()
        draw.text((50, 25), title, fill=self.text_color, font=font)
        return img

    def create_content_section(self, img, content: str, y_start=120):
        """본문 영역 생성"""
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()

        # 텍스트 줄바꿈 처리
        lines = self._wrap_text(content, font, self.width - 100)
        y_position = y_start

        for line in lines:
            draw.text((50, y_position), line, fill=self.secondary_text_color, font=font)
            y_position += 40

        return img

    def create_footer(self, img, stock_info: dict):
        """푸터 영역 생성 (종목 정보)"""
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 28)
        except:
            font = ImageFont.load_default()

        symbol = stock_info.get('symbol', 'N/A')
        price = stock_info.get('price', 0)
        change = stock_info.get('change_percent', 0)

        change_color = (34, 197, 94) if change >= 0 else (239, 68, 68)
        footer_text = f"{symbol} | ${price:.2f} ({change:+.2f}%)"

        draw.text((50, self.height - 80), footer_text, fill=change_color, font=font)
        return img

    def _wrap_text(self, text: str, font, max_width: int) -> list:
        """텍스트 줄바꿈 처리"""
        lines = []
        words = text.split()
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            # 폰트의 getbbox 사용 (최신 Pillow)
            try:
                bbox = font.getbbox(test_line)
                width = bbox[2] - bbox[0]
            except:
                width = len(test_line) * 10  # 대략적인 계산

            if width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.strip())

        return lines
```

### 템플릿 사용 예제

```python
def generate_with_template(briefing_text: dict, stock_data: dict, output_path: str):
    """템플릿을 사용한 이미지 생성"""
    template = BriefingImageTemplate()

    # 빈 이미지 생성
    img = Image.new('RGB', (template.width, template.height), template.background_color)

    # 각 섹션 추가
    img = template.create_header(img, briefing_text.get('title', ''))
    img = template.create_content_section(img, briefing_text.get('summary', ''))
    img = template.create_footer(img, stock_data)

    # 저장
    img.save(output_path)
    return output_path
```

## 색상 팔레트

### 다크 테마 (기본)
```python
DARK_THEME = {
    'background': (17, 24, 39),      # gray-900
    'card': (31, 41, 55),            # gray-800
    'text_primary': (255, 255, 255), # white
    'text_secondary': (209, 213, 219), # gray-300
    'accent': (59, 130, 246),        # blue-500
    'success': (34, 197, 94),        # green-500
    'danger': (239, 68, 68),         # red-500
}
```

### 라이트 테마
```python
LIGHT_THEME = {
    'background': (255, 255, 255),   # white
    'card': (243, 244, 246),         # gray-100
    'text_primary': (17, 24, 39),    # gray-900
    'text_secondary': (75, 85, 99),  # gray-600
    'accent': (59, 130, 246),        # blue-500
    'success': (34, 197, 94),        # green-500
    'danger': (239, 68, 68),         # red-500
}
```

### 긍정적 테마 (positive-theme-design 연동)
```python
POSITIVE_THEME = {
    'background': (255, 251, 235),   # amber-50
    'card': (254, 243, 199),         # amber-100
    'text_primary': (120, 53, 15),   # amber-900
    'text_secondary': (146, 64, 14), # amber-800
    'accent': (245, 158, 11),        # amber-500
    'success': (132, 204, 22),       # lime-500
    'danger': (239, 68, 68),         # red-500
    'highlight': (253, 224, 71),     # yellow-300
}
```

## 이미지 최적화

### 1. 파일 크기 최적화

```python
def optimize_image(input_path: str, output_path: str, quality=85):
    """이미지 파일 크기 최적화"""
    img = Image.open(input_path)

    # RGB로 변환 (JPEG 호환)
    if img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = background

    # 최적화된 JPEG로 저장
    img.save(output_path, 'JPEG', quality=quality, optimize=True)
    return output_path
```

### 2. 소셜 미디어 최적화

```python
# 소셜 미디어 플랫폼별 권장 크기
SOCIAL_MEDIA_SIZES = {
    'slack': (1200, 630),      # Slack 미리보기
    'twitter': (1200, 675),    # Twitter 카드
    'facebook': (1200, 630),   # Facebook 링크
    'instagram': (1080, 1080), # Instagram 정사각형
}

def create_for_platform(content: dict, platform: str, output_path: str):
    """플랫폼별 최적화된 이미지 생성"""
    width, height = SOCIAL_MEDIA_SIZES.get(platform, (1200, 630))
    # ... 이미지 생성 로직
```

## FastAPI 엔드포인트 통합

### 이미지 생성 API

```python
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

router = APIRouter(prefix="/v1/images", tags=["images"])

class ImageGenerationRequest(BaseModel):
    title: str
    content: str
    stock_symbol: str
    stock_price: float
    stock_change: float

@router.post("/generate")
async def generate_image(request: ImageGenerationRequest):
    """브리핑 이미지 생성"""
    try:
        briefing_text = {
            'title': request.title,
            'summary': request.content
        }
        stock_data = {
            'symbol': request.stock_symbol,
            'price': request.stock_price,
            'change_percent': request.stock_change
        }

        output_path = f"backend/output/{request.stock_symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

        image_path = generate_briefing_image(
            briefing_text=briefing_text,
            stock_data=stock_data,
            output_path=output_path
        )

        return {"success": True, "image_path": image_path}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/{filename}")
async def download_image(filename: str):
    """생성된 이미지 다운로드"""
    file_path = f"backend/output/{filename}"
    if not Path(file_path).exists():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path)
```

## 개발 시 주의사항

### 1. 폰트 처리

- Windows: `C:\Windows\Fonts\` 경로의 폰트 사용
- Linux: `/usr/share/fonts/` 경로 확인
- 한글 지원: 'malgun.ttf' (맑은 고딕) 또는 'NanumGothic.ttf' 사용
- 폴백: `ImageFont.load_default()` 항상 준비

### 2. 에러 처리

```python
try:
    img = generate_briefing_image(...)
    if img is None:
        # 폴백 이미지 또는 에러 처리
        logger.error("이미지 생성 실패")
except Exception as e:
    logger.error(f"이미지 생성 중 오류: {str(e)}")
    # 기본 이미지 반환 또는 재시도
```

### 3. 메모리 관리

```python
# 대용량 이미지 처리 시 주의
img = Image.open(path)
# ... 처리 ...
img.close()  # 명시적으로 닫기
```

### 4. 텍스트 인코딩

```python
# 한글 텍스트 처리 시 UTF-8 인코딩 확인
text = "한글 텍스트"
assert isinstance(text, str), "텍스트는 문자열이어야 합니다"
```

## 테스트

### 단위 테스트

```python
# backend/test_image_generation.py
from gemini_briefing import generate_briefing_image_with_pillow

def test_image_generation():
    briefing = {
        'title': '테스트 브리핑',
        'summary': '이것은 테스트입니다.'
    }
    stock = {
        'symbol': 'TEST',
        'name': 'Test Stock',
        'price': 100.00,
        'change_percent': 5.0
    }

    result = generate_briefing_image_with_pillow(
        briefing, stock, output_path='backend/output/test.png'
    )

    assert result is not None
    assert Path(result).exists()
```

### 실행

```bash
cd backend
python test_image_generation.py
```

## 환경 변수

```bash
# backend/.env
GEMINI_API_KEY=your_gemini_api_key_here

# 이미지 설정 (선택)
IMAGE_OUTPUT_DIR=backend/output
IMAGE_DEFAULT_WIDTH=1200
IMAGE_DEFAULT_HEIGHT=630
IMAGE_QUALITY=85
```

## 개발일지 작성

이미지 생성 기능 개발 시 개발일지 작성:

**위치**: `개발일지/YYYY/MM/DD/YYYY-MM-DD_이미지기능개발.md`

**필수 섹션**:
1. 작성시각
2. 해결하고자 한 문제 (예: 새로운 템플릿 추가)
3. 해결된 것
4. 해결되지 않은 것
5. 향후 개발을 위한 컨텍스트

## 참고 문서

- **Gemini API**: `backend/README_gemini.md`
- **Pillow 문서**: https://pillow.readthedocs.io/
- **프로젝트 구조**: `프로젝트_구조.md`
- **Backend 가이드**: `backend/README.md`

## 향후 개선 아이디어

- [ ] 차트/그래프 이미지 자동 생성
- [ ] 여러 템플릿 중 선택 기능
- [ ] 애니메이션 GIF 생성
- [ ] 워터마크 자동 추가
- [ ] 배치 이미지 생성 (여러 종목 동시)
- [ ] 이미지 캐싱 시스템
- [ ] A/B 테스팅을 위한 여러 버전 생성

---

이 스킬은 프로젝트의 브리핑 이미지 생성 품질과 일관성을 유지하기 위한 가이드입니다.
