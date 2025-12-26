# Image Editor Skill

브리핑 이미지 생성 및 편집을 위한 Claude Code 스킬입니다.

## 스킬 활성화

```bash
# Claude Code에서 스킬 사용
/image-editor
```

또는 이미지 생성/편집 작업 요청 시 자동으로 활성화됩니다.

## 주요 기능

### 1. AI 기반 이미지 생성
- Google Gemini API를 사용한 브리핑 이미지 자동 생성
- 종목 정보와 뉴스를 시각화

### 2. Pillow 기반 템플릿 시스템
- 커스텀 이미지 템플릿 생성
- 다크/라이트/Positive 테마 지원
- 반응형 텍스트 레이아웃

### 3. 최적화 및 배포
- 소셜 미디어 플랫폼별 크기 최적화
- 파일 크기 압축
- Slack 자동 전송

## 파일 구조

```
.claude/skills/image-editor/
├── SKILL.md              # 스킬 가이드 (메인 문서)
├── README.md             # 이 파일
└── example_template.py   # 템플릿 예제 코드
```

## 빠른 시작

### 1. 예제 템플릿 실행

```bash
cd backend
python ../.claude/skills/image-editor/example_template.py
```

생성된 이미지:
- `backend/output/example_briefing.png` (다크 테마)
- `backend/output/example_briefing_positive.png` (Positive 테마)

### 2. 프로젝트에 통합

```python
# backend/your_module.py
from gemini_briefing import generate_briefing_image

# 이미지 생성
image_path = generate_briefing_image(
    briefing_text={'title': '...', 'summary': '...'},
    stock_data={'symbol': 'AAPL', 'price': 150.0, 'change_percent': 2.5},
    output_path='backend/output/briefing.png'
)
```

### 3. 커스텀 템플릿 사용

```python
from example_template import BriefingImageTemplate

template = BriefingImageTemplate(theme='positive')
output = template.create_briefing_image(
    title="브리핑 제목",
    content="브리핑 내용...",
    stock_info={'symbol': 'TSLA', 'price': 250.0, 'change_percent': 5.0}
)
```

## 스킬 문서

자세한 내용은 [SKILL.md](./SKILL.md)를 참고하세요:

- 이미지 생성 패턴
- 템플릿 시스템
- 색상 팔레트
- 최적화 기법
- FastAPI 통합
- 주의사항 및 베스트 프랙티스

## 테마 예시

### Dark Theme (기본)
- 배경: Gray-900 (#111827)
- 텍스트: White/Gray-300
- 강조: Blue-500

### Positive Theme
- 배경: Amber-50 (#FFFBEB)
- 텍스트: Amber-900/800
- 강조: Amber-500
- 하이라이트: Yellow-300

## 환경 설정

```bash
# backend/.env
GEMINI_API_KEY=your_gemini_api_key

# 이미지 설정 (선택)
IMAGE_OUTPUT_DIR=backend/output
IMAGE_DEFAULT_WIDTH=1200
IMAGE_DEFAULT_HEIGHT=630
```

## 관련 스킬

- **frontend-design**: 프론트엔드 UI/UX 개발
- **positive-theme-design**: 긍정적 테마 디자인 시스템

## 문제 해결

### 한글 폰트 깨짐
- Windows: `C:\Windows\Fonts\malgun.ttf` (맑은 고딕) 확인
- Linux: `sudo apt-get install fonts-nanum` 설치

### Pillow 설치 오류
```bash
pip install Pillow
```

### Gemini API 오류
- `.env` 파일의 `GEMINI_API_KEY` 확인
- API 할당량 확인

## 향후 계획

- [ ] 차트/그래프 자동 생성
- [ ] 애니메이션 GIF 지원
- [ ] 워터마크 자동 추가
- [ ] 배치 이미지 생성
- [ ] 이미지 캐싱 시스템

---

**문의 및 기여**: 개발일지에 기록하거나 프로젝트 문서 참고
