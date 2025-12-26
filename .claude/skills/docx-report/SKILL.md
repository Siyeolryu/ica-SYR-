# DOCX Report Skill

"당신이 잠든 사이 (While You Were Sleeping)" 프로젝트의 Word 문서 생성 가이드입니다.

## 기술 스택

### Document Generation
- **Library**: python-docx
- **Language**: Python 3.x
- **Output Format**: .docx (Microsoft Word)
- **Integration**: FastAPI endpoints for report generation

### Features
- 브리핑 리포트 자동 생성
- 종목 정보 표 자동 삽입
- 뉴스 요약 포맷팅
- 차트 이미지 삽입
- 커스텀 스타일링

## 디렉토리 구조

```
backend/
├── docx_generator.py           # Word 문서 생성 메인 모듈
├── output/                     # 생성된 문서 저장소
│   └── reports/                # 브리핑 리포트 저장
├── api/
│   └── reports.py              # 리포트 생성 API 엔드포인트
└── .env                        # 환경 변수
```

## 핵심 기능

### 1. 브리핑 리포트 생성
종목 정보와 뉴스를 포함한 일일 브리핑 Word 문서 자동 생성

### 2. 표 및 서식 자동화
종목 데이터를 표 형식으로 자동 변환 및 스타일 적용

### 3. 이미지 삽입
차트, 그래프, 브리핑 이미지를 Word 문서에 삽입

### 4. 템플릿 기반 생성
사전 정의된 템플릿을 사용한 일관된 문서 생성

## 설치

```bash
pip install python-docx
```

## 기본 사용법

### 1. 간단한 브리핑 리포트 생성

```python
from docx_generator import create_briefing_report

# 브리핑 데이터
briefing_data = {
    'date': '2025-12-24',
    'title': '오늘의 화제 종목 TOP 5',
    'stocks': [
        {
            'symbol': 'AAPL',
            'name': 'Apple Inc.',
            'price': 150.25,
            'change_percent': 2.5,
            'volume': 50000000,
            'news_summary': 'Apple announces new product...'
        },
        # ... more stocks
    ],
    'summary': '오늘 미국 증시는 기술주 중심으로 상승세를 보였습니다...'
}

# 문서 생성
output_path = create_briefing_report(
    briefing_data=briefing_data,
    output_path='backend/output/reports/briefing_2025-12-24.docx'
)

print(f"Report generated: {output_path}")
```

### 2. 커스텀 스타일로 리포트 생성

```python
from docx_generator import BriefingReportGenerator

# 리포트 생성기 초기화
generator = BriefingReportGenerator(
    title_font='Arial',
    body_font='Calibri',
    title_size=24,
    body_size=11
)

# 커스텀 스타일로 생성
generator.create_report(
    briefing_data=briefing_data,
    output_path='backend/output/reports/custom_briefing.docx',
    include_images=True,
    include_charts=True
)
```

## 문서 구조 패턴

### 1. 표준 브리핑 리포트 구조

```python
def create_briefing_report(briefing_data: dict, output_path: str) -> str:
    """
    표준 브리핑 리포트 생성

    문서 구조:
    1. 헤더 (날짜, 제목)
    2. 전체 요약
    3. 종목별 상세 정보
       - 종목명, 티커
       - 현재가, 등락률
       - 뉴스 요약
       - 차트 이미지 (선택)
    4. 푸터 (생성 시간, 출처)

    Args:
        briefing_data: 브리핑 데이터 딕셔너리
        output_path: 저장 경로

    Returns:
        생성된 문서 경로
    """
    from docx import Document
    from docx.shared import Pt, RGBColor, Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from datetime import datetime

    # 새 문서 생성
    doc = Document()

    # === 헤더 섹션 ===
    # 제목
    title = doc.add_heading(briefing_data.get('title', '일일 주식 브리핑'), level=1)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # 날짜
    date_paragraph = doc.add_paragraph()
    date_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    date_run = date_paragraph.add_run(f"날짜: {briefing_data.get('date', datetime.now().strftime('%Y-%m-%d'))}")
    date_run.font.size = Pt(12)
    date_run.font.color.rgb = RGBColor(100, 100, 100)

    # 구분선
    doc.add_paragraph('_' * 50)

    # === 전체 요약 ===
    doc.add_heading('📊 시장 요약', level=2)
    summary = doc.add_paragraph(briefing_data.get('summary', ''))
    summary.style = 'Body Text'

    doc.add_paragraph()  # 공백

    # === 종목별 상세 정보 ===
    doc.add_heading('🔥 화제 종목 TOP 5', level=2)

    for i, stock in enumerate(briefing_data.get('stocks', [])[:5], 1):
        # 종목 헤더
        stock_heading = doc.add_heading(f"{i}. {stock.get('symbol')} - {stock.get('name')}", level=3)

        # 종목 정보 표
        table = doc.add_table(rows=4, cols=2)
        table.style = 'Light Grid Accent 1'

        # 표 데이터 입력
        cells = table.rows[0].cells
        cells[0].text = '현재가'
        cells[1].text = f"${stock.get('price', 0):.2f}"

        cells = table.rows[1].cells
        cells[0].text = '등락률'
        change = stock.get('change_percent', 0)
        cells[1].text = f"{change:+.2f}%"
        # 등락에 따른 색상 설정
        change_run = cells[1].paragraphs[0].runs[0]
        if change >= 0:
            change_run.font.color.rgb = RGBColor(0, 128, 0)  # 녹색
        else:
            change_run.font.color.rgb = RGBColor(255, 0, 0)  # 빨간색

        cells = table.rows[2].cells
        cells[0].text = '거래량'
        cells[1].text = f"{stock.get('volume', 0):,}"

        cells = table.rows[3].cells
        cells[0].text = '뉴스 요약'
        cells[1].text = stock.get('news_summary', 'N/A')

        # 차트 이미지 삽입 (있는 경우)
        chart_path = stock.get('chart_image_path')
        if chart_path and Path(chart_path).exists():
            doc.add_paragraph()
            doc.add_picture(chart_path, width=Inches(5))

        doc.add_paragraph()  # 종목 간 간격

    # === 푸터 ===
    doc.add_paragraph('_' * 50)
    footer = doc.add_paragraph()
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer_run = footer.add_run(
        f"생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"출처: Yahoo Finance, Exa News API\n"
        f"🤖 Generated with Claude Code"
    )
    footer_run.font.size = Pt(9)
    footer_run.font.color.rgb = RGBColor(150, 150, 150)

    # 문서 저장
    doc.save(output_path)
    return output_path
```

### 2. 종목 비교 리포트

```python
def create_stock_comparison_report(stocks: list, output_path: str) -> str:
    """
    여러 종목을 비교하는 리포트 생성

    Args:
        stocks: 종목 리스트
        output_path: 저장 경로

    Returns:
        생성된 문서 경로
    """
    from docx import Document
    from docx.shared import Pt, RGBColor

    doc = Document()

    # 제목
    doc.add_heading('종목 비교 분석', level=1)

    # 비교 표 생성
    table = doc.add_table(rows=len(stocks) + 1, cols=6)
    table.style = 'Medium Grid 1 Accent 1'

    # 헤더
    headers = ['순위', '티커', '종목명', '현재가', '등락률', '거래량']
    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = header
        # 헤더 스타일
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.size = Pt(11)

    # 데이터 입력
    for i, stock in enumerate(stocks, 1):
        row = table.rows[i]
        row.cells[0].text = str(i)
        row.cells[1].text = stock.get('symbol', 'N/A')
        row.cells[2].text = stock.get('name', 'N/A')
        row.cells[3].text = f"${stock.get('price', 0):.2f}"

        # 등락률 (색상 적용)
        change = stock.get('change_percent', 0)
        change_cell = row.cells[4]
        change_cell.text = f"{change:+.2f}%"
        for paragraph in change_cell.paragraphs:
            for run in paragraph.runs:
                if change >= 0:
                    run.font.color.rgb = RGBColor(0, 128, 0)
                else:
                    run.font.color.rgb = RGBColor(255, 0, 0)

        row.cells[5].text = f"{stock.get('volume', 0):,}"

    doc.save(output_path)
    return output_path
```

### 3. 뉴스 요약 리포트

```python
def create_news_summary_report(news_items: list, output_path: str) -> str:
    """
    뉴스 요약 리포트 생성

    Args:
        news_items: 뉴스 아이템 리스트
        output_path: 저장 경로

    Returns:
        생성된 문서 경로
    """
    from docx import Document
    from docx.shared import Pt, RGBColor

    doc = Document()

    # 제목
    doc.add_heading('📰 주요 뉴스 요약', level=1)

    for i, news in enumerate(news_items, 1):
        # 뉴스 번호 및 제목
        heading = doc.add_heading(f"{i}. {news.get('title', 'No Title')}", level=2)

        # 메타 정보 (날짜, 출처)
        meta = doc.add_paragraph()
        meta_run = meta.add_run(
            f"📅 {news.get('date', 'N/A')} | 🔗 {news.get('source', 'N/A')}"
        )
        meta_run.font.size = Pt(10)
        meta_run.font.color.rgb = RGBColor(100, 100, 100)

        # 뉴스 요약
        summary = doc.add_paragraph(news.get('summary', ''))
        summary.style = 'Body Text'

        # 관련 종목
        if 'related_stocks' in news:
            related = doc.add_paragraph()
            related_run = related.add_run(
                f"관련 종목: {', '.join(news.get('related_stocks', []))}"
            )
            related_run.font.italic = True
            related_run.font.size = Pt(10)

        # URL
        if 'url' in news:
            url_para = doc.add_paragraph()
            url_para.add_run('링크: ')
            url_run = url_para.add_run(news.get('url', ''))
            url_run.font.color.rgb = RGBColor(0, 0, 255)
            url_run.font.underline = True

        doc.add_paragraph()  # 뉴스 간 간격

    doc.save(output_path)
    return output_path
```

## 고급 기능

### 1. 템플릿 기반 리포트 생성

```python
class BriefingReportTemplate:
    """브리핑 리포트 템플릿 클래스"""

    def __init__(self, template_path: str = None):
        """
        Args:
            template_path: 기존 템플릿 문서 경로 (선택)
        """
        from docx import Document

        if template_path and Path(template_path).exists():
            self.doc = Document(template_path)
        else:
            self.doc = Document()
            self._setup_default_styles()

    def _setup_default_styles(self):
        """기본 스타일 설정"""
        from docx.shared import Pt, RGBColor

        # 제목 스타일
        style = self.doc.styles['Heading 1']
        font = style.font
        font.name = 'Arial'
        font.size = Pt(24)
        font.bold = True
        font.color.rgb = RGBColor(0, 51, 102)  # 다크 블루

        # 부제목 스타일
        style = self.doc.styles['Heading 2']
        font = style.font
        font.name = 'Arial'
        font.size = Pt(18)
        font.bold = True
        font.color.rgb = RGBColor(37, 99, 235)  # 블루

        # 본문 스타일
        style = self.doc.styles['Normal']
        font = style.font
        font.name = 'Calibri'
        font.size = Pt(11)

    def add_title_section(self, title: str, date: str):
        """제목 섹션 추가"""
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.shared import Pt, RGBColor

        title_para = self.doc.add_heading(title, level=1)
        title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        date_para = self.doc.add_paragraph()
        date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        date_run = date_para.add_run(f"📅 {date}")
        date_run.font.size = Pt(12)
        date_run.font.color.rgb = RGBColor(100, 100, 100)

        self.doc.add_paragraph('=' * 60)

    def add_summary_section(self, summary: str):
        """요약 섹션 추가"""
        self.doc.add_heading('📊 시장 요약', level=2)
        para = self.doc.add_paragraph(summary)
        para.style = 'Body Text'
        self.doc.add_paragraph()

    def add_stock_section(self, stock_data: dict, rank: int):
        """종목 섹션 추가"""
        from docx.shared import RGBColor, Inches

        # 종목 헤더
        self.doc.add_heading(
            f"{rank}. {stock_data.get('symbol')} - {stock_data.get('name')}",
            level=3
        )

        # 종목 정보 표
        table = self.doc.add_table(rows=4, cols=2)
        table.style = 'Light Grid Accent 1'

        # 데이터 채우기
        data = [
            ('현재가', f"${stock_data.get('price', 0):.2f}"),
            ('등락률', f"{stock_data.get('change_percent', 0):+.2f}%"),
            ('거래량', f"{stock_data.get('volume', 0):,}"),
            ('뉴스 요약', stock_data.get('news_summary', 'N/A'))
        ]

        for i, (label, value) in enumerate(data):
            cells = table.rows[i].cells
            cells[0].text = label
            cells[1].text = value

            # 등락률 색상
            if label == '등락률':
                change = stock_data.get('change_percent', 0)
                for paragraph in cells[1].paragraphs:
                    for run in paragraph.runs:
                        if change >= 0:
                            run.font.color.rgb = RGBColor(0, 128, 0)
                        else:
                            run.font.color.rgb = RGBColor(255, 0, 0)

        # 차트 이미지 추가
        if 'chart_image' in stock_data and Path(stock_data['chart_image']).exists():
            self.doc.add_paragraph()
            self.doc.add_picture(stock_data['chart_image'], width=Inches(5))

        self.doc.add_paragraph()

    def add_footer_section(self):
        """푸터 섹션 추가"""
        from datetime import datetime
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.shared import Pt, RGBColor

        self.doc.add_paragraph('=' * 60)

        footer = self.doc.add_paragraph()
        footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
        footer_text = (
            f"생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"출처: Yahoo Finance, Exa News API\n"
            f"🤖 Generated with Claude Code - While You Were Sleeping"
        )
        footer_run = footer.add_run(footer_text)
        footer_run.font.size = Pt(9)
        footer_run.font.color.rgb = RGBColor(150, 150, 150)

    def save(self, output_path: str) -> str:
        """문서 저장"""
        self.doc.save(output_path)
        return output_path
```

### 2. 이미지 삽입

```python
def add_chart_to_document(doc, chart_path: str, width_inches: float = 5.0):
    """
    문서에 차트 이미지 추가

    Args:
        doc: Document 객체
        chart_path: 차트 이미지 경로
        width_inches: 이미지 너비 (인치)
    """
    from docx.shared import Inches
    from pathlib import Path

    if Path(chart_path).exists():
        doc.add_paragraph()
        doc.add_picture(chart_path, width=Inches(width_inches))
        # 이미지 캡션
        caption = doc.add_paragraph()
        caption.add_run(f"그림: {Path(chart_path).stem}").italic = True
        caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    else:
        print(f"Warning: Chart image not found: {chart_path}")
```

### 3. 하이퍼링크 추가

```python
def add_hyperlink(paragraph, url: str, text: str):
    """
    문단에 하이퍼링크 추가

    Args:
        paragraph: Paragraph 객체
        url: URL
        text: 표시할 텍스트
    """
    from docx.oxml.shared import OxmlElement
    from docx.oxml.ns import qn

    # 하이퍼링크 생성
    part = paragraph.part
    r_id = part.relate_to(url, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', is_external=True)

    # XML 요소 생성
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)

    # 텍스트 run 생성
    new_run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')

    # 하이퍼링크 스타일 (파란색, 밑줄)
    c = OxmlElement('w:color')
    c.set(qn('w:val'), '0000FF')
    rPr.append(c)

    u = OxmlElement('w:u')
    u.set(qn('w:val'), 'single')
    rPr.append(u)

    new_run.append(rPr)
    new_run.text = text
    hyperlink.append(new_run)

    paragraph._p.append(hyperlink)

    return hyperlink
```

## FastAPI 통합

### 리포트 생성 API

```python
# backend/api/reports.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from pathlib import Path

router = APIRouter(prefix="/v1/reports", tags=["reports"])

class StockData(BaseModel):
    symbol: str
    name: str
    price: float
    change_percent: float
    volume: int
    news_summary: Optional[str] = None
    chart_image_path: Optional[str] = None

class BriefingReportRequest(BaseModel):
    date: str
    title: str
    summary: str
    stocks: List[StockData]

@router.post("/briefing")
async def create_briefing_report(request: BriefingReportRequest):
    """브리핑 리포트 생성"""
    try:
        from docx_generator import create_briefing_report

        # 출력 디렉토리 확인
        output_dir = Path("backend/output/reports")
        output_dir.mkdir(parents=True, exist_ok=True)

        # 파일명 생성
        filename = f"briefing_{request.date}.docx"
        output_path = output_dir / filename

        # 리포트 생성
        briefing_data = {
            'date': request.date,
            'title': request.title,
            'summary': request.summary,
            'stocks': [stock.dict() for stock in request.stocks]
        }

        result_path = create_briefing_report(
            briefing_data=briefing_data,
            output_path=str(output_path)
        )

        return {
            "success": True,
            "message": "Briefing report created successfully",
            "file_path": str(result_path),
            "filename": filename
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create report: {str(e)}")

@router.get("/download/{filename}")
async def download_report(filename: str):
    """리포트 다운로드"""
    file_path = Path(f"backend/output/reports/{filename}")

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Report not found")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )

@router.get("/list")
async def list_reports():
    """생성된 리포트 목록 조회"""
    reports_dir = Path("backend/output/reports")

    if not reports_dir.exists():
        return {"reports": []}

    reports = []
    for file_path in reports_dir.glob("*.docx"):
        reports.append({
            "filename": file_path.name,
            "created_at": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
            "size_bytes": file_path.stat().st_size
        })

    # 최신순 정렬
    reports.sort(key=lambda x: x['created_at'], reverse=True)

    return {"reports": reports}
```

## 일괄 리포트 생성

### 여러 날짜의 브리핑을 한 번에 생성

```python
def create_multiple_briefing_reports(
    start_date: str,
    end_date: str,
    output_dir: str = "backend/output/reports"
) -> list:
    """
    여러 날짜의 브리핑 리포트를 일괄 생성

    Args:
        start_date: 시작 날짜 (YYYY-MM-DD)
        end_date: 종료 날짜 (YYYY-MM-DD)
        output_dir: 출력 디렉토리

    Returns:
        생성된 리포트 경로 리스트
    """
    from datetime import datetime, timedelta
    from get_trending_stocks import get_trending_stocks
    from exa_news import get_stock_news

    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    generated_reports = []
    current_date = start

    while current_date <= end:
        date_str = current_date.strftime('%Y-%m-%d')
        print(f"Generating report for {date_str}...")

        try:
            # 종목 데이터 조회
            stocks = get_trending_stocks(top_n=5)

            # 각 종목의 뉴스 조회
            for stock in stocks:
                news = get_stock_news(stock['symbol'], limit=3)
                stock['news_summary'] = ' '.join([n.get('title', '') for n in news[:2]])

            # 브리핑 데이터 구성
            briefing_data = {
                'date': date_str,
                'title': f'{date_str} 화제 종목 브리핑',
                'summary': '오늘의 화제 종목을 확인하세요.',
                'stocks': stocks
            }

            # 리포트 생성
            output_path = Path(output_dir) / f"briefing_{date_str}.docx"
            create_briefing_report(briefing_data, str(output_path))

            generated_reports.append(str(output_path))
            print(f"✓ Report created: {output_path}")

        except Exception as e:
            print(f"✗ Failed to create report for {date_str}: {e}")

        current_date += timedelta(days=1)

    return generated_reports
```

## 스타일 및 포맷팅

### 1. 색상 스키마

```python
# 문서 색상 팔레트
COLORS = {
    'primary': RGBColor(37, 99, 235),      # Blue-600
    'success': RGBColor(34, 197, 94),      # Green-500
    'danger': RGBColor(239, 68, 68),       # Red-500
    'warning': RGBColor(245, 158, 11),     # Amber-500
    'text_primary': RGBColor(17, 24, 39),  # Gray-900
    'text_secondary': RGBColor(107, 114, 128),  # Gray-500
}
```

### 2. 표 스타일

```python
# 사용 가능한 표 스타일
TABLE_STYLES = [
    'Light Grid Accent 1',
    'Medium Grid 1 Accent 1',
    'Light Shading Accent 1',
    'Medium Shading 1 Accent 1',
]
```

## 환경 변수

```bash
# backend/.env
REPORT_OUTPUT_DIR=backend/output/reports
REPORT_TEMPLATE_PATH=backend/templates/briefing_template.docx  # 선택
```

## 테스트

### 단위 테스트

```python
# backend/test_docx_generation.py
from docx_generator import create_briefing_report
from pathlib import Path

def test_briefing_report_generation():
    """브리핑 리포트 생성 테스트"""
    briefing_data = {
        'date': '2025-12-24',
        'title': '테스트 브리핑',
        'summary': '이것은 테스트 브리핑입니다.',
        'stocks': [
            {
                'symbol': 'TEST',
                'name': 'Test Stock',
                'price': 100.00,
                'change_percent': 5.0,
                'volume': 1000000,
                'news_summary': 'Test news summary'
            }
        ]
    }

    output_path = 'backend/output/reports/test_briefing.docx'
    result = create_briefing_report(briefing_data, output_path)

    assert result is not None
    assert Path(result).exists()
    print(f"✓ Test passed: {result}")

if __name__ == "__main__":
    test_briefing_report_generation()
```

### 실행

```bash
cd backend
python test_docx_generation.py
```

## 주의사항

### 1. 한글 폰트 지원

```python
# Windows에서 한글 폰트 사용
from docx.shared import Pt
from docx.oxml.ns import qn

def set_korean_font(run, font_name='Malgun Gothic'):
    """한글 폰트 설정"""
    run.font.name = font_name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
```

### 2. 이미지 파일 존재 확인

```python
from pathlib import Path

if Path(image_path).exists():
    doc.add_picture(image_path)
else:
    print(f"Warning: Image not found: {image_path}")
```

### 3. 파일 경로 처리

```python
# 플랫폼 독립적인 경로 처리
from pathlib import Path

output_path = Path("backend/output/reports") / "briefing.docx"
output_path.parent.mkdir(parents=True, exist_ok=True)
```

## 향후 개선 아이디어

- [ ] PDF 변환 기능 추가
- [ ] 다양한 템플릿 제공
- [ ] 차트 자동 생성 및 삽입
- [ ] 이메일 첨부 자동 전송
- [ ] 리포트 스케줄링 (일일/주간/월간)
- [ ] 커스텀 테마 적용
- [ ] 다국어 지원
- [ ] 리포트 버전 관리

## 관련 문서

- **python-docx 문서**: https://python-docx.readthedocs.io/
- **프로젝트 구조**: `프로젝트_구조.md`
- **Backend 가이드**: `backend/README.md`
- **이미지 생성**: `.claude/skills/image-editor/SKILL.md`

---

이 스킬은 브리핑 리포트를 Word 문서로 자동 생성하여 배포 및 보관을 용이하게 합니다.
