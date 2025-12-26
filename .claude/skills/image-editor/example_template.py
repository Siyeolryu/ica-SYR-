"""
브리핑 이미지 생성 예제 템플릿

이 파일은 image-editor 스킬의 실제 사용 예제를 제공합니다.
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from datetime import datetime


class BriefingImageTemplate:
    """브리핑 이미지 템플릿 클래스"""

    # 색상 테마
    DARK_THEME = {
        'background': (17, 24, 39),      # gray-900
        'card': (31, 41, 55),            # gray-800
        'text_primary': (255, 255, 255), # white
        'text_secondary': (209, 213, 219), # gray-300
        'accent': (59, 130, 246),        # blue-500
        'success': (34, 197, 94),        # green-500
        'danger': (239, 68, 68),         # red-500
    }

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

    def __init__(self, width=1200, height=630, theme='dark'):
        """
        템플릿 초기화

        Args:
            width: 이미지 너비
            height: 이미지 높이
            theme: 테마 ('dark' 또는 'positive')
        """
        self.width = width
        self.height = height
        self.theme = self.DARK_THEME if theme == 'dark' else self.POSITIVE_THEME

    def create_briefing_image(
        self,
        title: str,
        content: str,
        stock_info: dict,
        output_path: str = None
    ) -> str:
        """
        완전한 브리핑 이미지 생성

        Args:
            title: 브리핑 제목
            content: 브리핑 내용
            stock_info: 종목 정보 (symbol, name, price, change_percent)
            output_path: 저장 경로 (없으면 자동 생성)

        Returns:
            생성된 이미지 경로
        """
        # 출력 경로 설정
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f"backend/output/briefing_{timestamp}.png"

        # 이미지 생성
        img = Image.new('RGB', (self.width, self.height), self.theme['background'])

        # 각 섹션 추가
        img = self._add_header(img, title)
        img = self._add_content(img, content)
        img = self._add_stock_info(img, stock_info)
        img = self._add_footer(img)

        # 저장
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        img.save(output_path)

        return output_path

    def _add_header(self, img: Image, title: str) -> Image:
        """헤더 영역 추가"""
        draw = ImageDraw.Draw(img)

        # 헤더 배경
        draw.rectangle([0, 0, self.width, 120], fill=self.theme['accent'])

        # 제목
        font = self._get_font(size=48, bold=True)
        draw.text((50, 35), title, fill=(255, 255, 255), font=font)

        # 로고/아이콘 영역 (선택적)
        logo_text = "💼 당신이 잠든 사이"
        logo_font = self._get_font(size=24)
        draw.text((self.width - 300, 45), logo_text, fill=(255, 255, 255), font=logo_font)

        return img

    def _add_content(self, img: Image, content: str) -> Image:
        """본문 영역 추가"""
        draw = ImageDraw.Draw(img)
        font = self._get_font(size=24)

        # 텍스트 줄바꿈
        lines = self._wrap_text(content, font, self.width - 100)

        y_position = 160
        for line in lines[:8]:  # 최대 8줄
            draw.text((50, y_position), line, fill=self.theme['text_secondary'], font=font)
            y_position += 40

        return img

    def _add_stock_info(self, img: Image, stock_info: dict) -> Image:
        """종목 정보 영역 추가"""
        draw = ImageDraw.Draw(img)

        # 카드 배경
        card_y = self.height - 180
        card_height = 120
        draw.rectangle(
            [40, card_y, self.width - 40, card_y + card_height],
            fill=self.theme['card'],
            outline=self.theme['accent'],
            width=2
        )

        # 종목 심볼
        symbol = stock_info.get('symbol', 'N/A')
        name = stock_info.get('name', 'Unknown')
        symbol_font = self._get_font(size=36, bold=True)
        draw.text((60, card_y + 20), symbol, fill=self.theme['text_primary'], font=symbol_font)

        # 종목명
        name_font = self._get_font(size=20)
        draw.text((60, card_y + 70), name, fill=self.theme['text_secondary'], font=name_font)

        # 가격
        price = stock_info.get('price', 0)
        price_text = f"${price:.2f}"
        price_font = self._get_font(size=40, bold=True)
        price_x = self.width - 400
        draw.text((price_x, card_y + 20), price_text, fill=self.theme['text_primary'], font=price_font)

        # 변동률
        change = stock_info.get('change_percent', 0)
        change_color = self.theme['success'] if change >= 0 else self.theme['danger']
        change_text = f"{change:+.2f}%"
        change_font = self._get_font(size=32, bold=True)
        draw.text((price_x, card_y + 70), change_text, fill=change_color, font=change_font)

        return img

    def _add_footer(self, img: Image) -> Image:
        """푸터 영역 추가"""
        draw = ImageDraw.Draw(img)

        # 푸터 라인
        footer_y = self.height - 50
        draw.line([50, footer_y, self.width - 50, footer_y], fill=self.theme['accent'], width=2)

        # 생성 시간
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M KST')
        footer_font = self._get_font(size=16)
        draw.text((50, footer_y + 10), timestamp, fill=self.theme['text_secondary'], font=footer_font)

        # 브랜딩
        branding = "AI Generated Briefing"
        draw.text(
            (self.width - 250, footer_y + 10),
            branding,
            fill=self.theme['text_secondary'],
            font=footer_font
        )

        return img

    def _get_font(self, size: int, bold: bool = False) -> ImageFont:
        """폰트 로드 (폴백 포함)"""
        font_paths = [
            "C:/Windows/Fonts/malgun.ttf",      # Windows 맑은 고딕
            "C:/Windows/Fonts/arial.ttf",       # Windows Arial
            "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",  # Linux 나눔고딕
            "/System/Library/Fonts/AppleSDGothicNeo.ttc",       # macOS
        ]

        for font_path in font_paths:
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue

        # 폴백
        return ImageFont.load_default()

    def _wrap_text(self, text: str, font: ImageFont, max_width: int) -> list:
        """텍스트 줄바꿈 처리"""
        lines = []
        words = text.split()
        current_line = ""

        for word in words:
            test_line = current_line + word + " "

            try:
                bbox = font.getbbox(test_line)
                width = bbox[2] - bbox[0]
            except:
                width = len(test_line) * 10

            if width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.strip())

        return lines


# 사용 예제
if __name__ == "__main__":
    # 템플릿 생성
    template = BriefingImageTemplate(theme='dark')

    # 샘플 데이터
    sample_briefing = {
        'title': "애플(AAPL) 급등 - 신제품 발표 앞두고",
        'content': "애플이 새로운 아이폰 발표를 앞두고 주가가 급등했습니다. "
                  "시장 전문가들은 신제품 라인업에 대한 기대감이 반영된 것으로 분석하고 있습니다. "
                  "특히 AI 기능 강화와 프리미엄 모델의 성능 개선이 주목받고 있습니다."
    }

    sample_stock = {
        'symbol': 'AAPL',
        'name': 'Apple Inc.',
        'price': 185.50,
        'change_percent': 3.25
    }

    # 이미지 생성
    output_path = template.create_briefing_image(
        title=sample_briefing['title'],
        content=sample_briefing['content'],
        stock_info=sample_stock,
        output_path='backend/output/example_briefing.png'
    )

    print(f"이미지 생성 완료: {output_path}")

    # Positive 테마 버전
    positive_template = BriefingImageTemplate(theme='positive')
    positive_output = positive_template.create_briefing_image(
        title=sample_briefing['title'],
        content=sample_briefing['content'],
        stock_info=sample_stock,
        output_path='backend/output/example_briefing_positive.png'
    )

    print(f"Positive 테마 이미지 생성 완료: {positive_output}")
