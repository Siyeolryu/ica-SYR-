# DOCX Report Skill

브리핑 리포트를 Word 문서(.docx)로 생성하는 Claude Code 스킬입니다.

## 스킬 활성화

```bash
# Claude Code에서 스킬 사용
/docx-report
```

또는 Word 문서 생성 작업 요청 시 자동으로 활성화됩니다.

## 주요 기능

### 1. 브리핑 리포트 자동 생성
- 종목 정보를 포함한 일일 브리핑 Word 문서 생성
- 표, 서식, 색상 자동 적용

### 2. 다양한 리포트 유형
- 표준 브리핑 리포트
- 종목 비교 리포트
- 뉴스 요약 리포트

### 3. 이미지 및 차트 삽입
- 주가 차트 이미지 자동 삽입
- 브리핑 이미지 통합

### 4. 커스텀 스타일링
- 다크/라이트 테마 지원
- 폰트, 색상 커스터마이징

## 설치

```bash
pip install python-docx
```

## 빠른 시작

### 1. 기본 브리핑 리포트 생성

```python
from docx_generator import create_briefing_report

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
        }
    ],
    'summary': '오늘 미국 증시는 기술주 중심으로 상승세를 보였습니다.'
}

output_path = create_briefing_report(
    briefing_data=briefing_data,
    output_path='backend/output/reports/briefing_2025-12-24.docx'
)

print(f"Report generated: {output_path}")
```

### 2. 예제 실행

```bash
cd backend
python ../.claude/skills/docx-report/example_generator.py
```

생성된 문서: `backend/output/reports/example_briefing.docx`

### 3. API를 통한 생성

```bash
# FastAPI 서버 실행
cd backend
python main.py

# 리포트 생성 요청
curl -X POST "http://localhost:8000/v1/reports/briefing" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-12-24",
    "title": "오늘의 화제 종목",
    "summary": "시장 요약...",
    "stocks": [...]
  }'

# 리포트 다운로드
curl "http://localhost:8000/v1/reports/download/briefing_2025-12-24.docx" \
  --output briefing.docx
```

## 파일 구조

```
.claude/skills/docx-report/
├── SKILL.md                # 스킬 가이드 (메인 문서)
├── README.md               # 이 파일
└── example_generator.py    # 예제 코드
```

## 문서 구조

생성되는 브리핑 리포트는 다음 구조를 따릅니다:

1. **헤더** - 제목, 날짜
2. **시장 요약** - 전체 시장 동향
3. **종목별 상세 정보**
   - 종목명, 티커
   - 가격 정보 (현재가, 등락률, 거래량)
   - 뉴스 요약
   - 차트 이미지
4. **푸터** - 생성 시간, 출처

## 스타일 커스터마이징

```python
from docx_generator import BriefingReportTemplate

# 커스텀 스타일로 생성
template = BriefingReportTemplate()
template.add_title_section("커스텀 브리핑", "2025-12-24")
template.add_summary_section("시장 요약...")
template.add_stock_section(stock_data, rank=1)
template.add_footer_section()
template.save("custom_report.docx")
```

## API 엔드포인트

### POST /v1/reports/briefing
브리핑 리포트 생성

### GET /v1/reports/download/{filename}
리포트 다운로드

### GET /v1/reports/list
생성된 리포트 목록 조회

## 환경 설정

```bash
# backend/.env
REPORT_OUTPUT_DIR=backend/output/reports
REPORT_TEMPLATE_PATH=backend/templates/briefing_template.docx  # 선택
```

## 테스트

```bash
cd backend
python test_docx_generation.py
```

## 주의사항

### 한글 폰트
- Windows: 맑은 고딕 (Malgun Gothic) 사용
- Linux: `sudo apt-get install fonts-nanum`

### 이미지 경로
- 차트 이미지는 절대 경로 또는 상대 경로로 제공
- 파일 존재 여부 확인 후 삽입

### 파일 크기
- 이미지가 많을 경우 파일 크기 주의
- 이미지 압축 권장

## 사용 예시

### Slack과 연동

```python
# 브리핑 리포트 생성 후 Slack으로 전송
from slack_sdk import WebClient

# 리포트 생성
report_path = create_briefing_report(briefing_data, output_path)

# Slack 업로드
client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
client.files_upload(
    channels="#stock-briefings",
    file=report_path,
    title="오늘의 브리핑 리포트"
)
```

### 이메일 첨부

```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# 리포트 생성
report_path = create_briefing_report(briefing_data, output_path)

# 이메일 전송
msg = MIMEMultipart()
msg['Subject'] = '일일 주식 브리핑'

# 첨부 파일
with open(report_path, 'rb') as f:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={Path(report_path).name}')
    msg.attach(part)

# 전송
# ... SMTP 전송 로직
```

## 스킬 문서

자세한 내용은 [SKILL.md](./SKILL.md)를 참고하세요:

- 문서 구조 패턴
- 고급 기능 (템플릿, 이미지, 하이퍼링크)
- FastAPI 통합
- 일괄 리포트 생성
- 스타일링 및 포맷팅
- 주의사항 및 베스트 프랙티스

## 관련 스킬

- **image-editor**: 브리핑 이미지 생성
- **frontend-design**: 프론트엔드 UI/UX 개발
- **positive-theme-design**: 긍정적 테마 디자인 시스템

## 문제 해결

### python-docx 설치 오류
```bash
pip install --upgrade pip
pip install python-docx
```

### 한글 깨짐 문제
- 한글 폰트(맑은 고딕, 나눔고딕) 설치 확인
- `set_korean_font()` 함수 사용

### 이미지 삽입 실패
- 이미지 파일 경로 확인
- 파일 존재 여부 확인
- 지원 형식: PNG, JPEG

## 향후 계획

- [ ] PDF 변환 기능
- [ ] 이메일 자동 전송
- [ ] 다양한 템플릿 제공
- [ ] 리포트 스케줄링
- [ ] 다국어 지원

## 참고 문서

- **python-docx**: https://python-docx.readthedocs.io/
- **프로젝트 구조**: `프로젝트_구조.md`
- **Backend 가이드**: `backend/README.md`

---

**문의 및 기여**: 개발일지에 기록하거나 프로젝트 문서 참고
