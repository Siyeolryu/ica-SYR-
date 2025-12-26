"""
브리핑 카드 이미지 생성 스크립트

실제 브리핑 데이터를 사용하여 시각적인 브리핑 카드를 생성합니다.
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from datetime import datetime


class BriefingCardGenerator:
    """브리핑 카드 이미지 생성기"""

    def __init__(self, width=1200, height=630):
        self.width = width
        self.height = height

        # 다크 테마 색상
        self.colors = {
            'background': (17, 24, 39),      # gray-900
            'card': (31, 41, 55),            # gray-800
            'accent': (59, 130, 246),        # blue-500
            'text_primary': (255, 255, 255), # white
            'text_secondary': (209, 213, 219), # gray-300
            'success': (34, 197, 94),        # green-500
            'danger': (239, 68, 68),         # red-500
        }

    def create_briefing_card(
        self,
        title: str,
        summary: str,
        stock_symbol: str,
        stock_name: str,
        current_price: float,
        change_percent: float,
        highlights: list = None,
        output_path: str = None
    ):
        """
        브리핑 카드 이미지 생성

        Args:
            title: 브리핑 제목
            summary: 브리핑 요약
            stock_symbol: 종목 심볼
            stock_name: 종목명
            current_price: 현재가
            change_percent: 변동률
            highlights: 주요 포인트 리스트
            output_path: 저장 경로
        """
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f"output/briefing_card_{stock_symbol}_{timestamp}.png"

        # 출력 디렉토리 생성
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # 이미지 생성
        img = Image.new('RGB', (self.width, self.height), self.colors['background'])
        draw = ImageDraw.Draw(img)

        # 각 섹션 그리기
        self._draw_header(draw, title)
        self._draw_stock_info_card(draw, stock_symbol, stock_name, current_price, change_percent)
        self._draw_summary(draw, summary)

        if highlights:
            self._draw_highlights(draw, highlights)

        self._draw_footer(draw)

        # 저장
        img.save(output_path, quality=95)
        print(f"Briefing card created: {output_path}")

        return output_path

    def _draw_header(self, draw: ImageDraw, title: str):
        """헤더 그리기"""
        # 헤더 배경
        draw.rectangle([0, 0, self.width, 100], fill=self.colors['accent'])

        # 로고/브랜드
        logo_font = self._get_font(24)
        draw.text(
            (40, 25),
            "💼 당신이 잠든 사이",
            fill=self.colors['text_primary'],
            font=logo_font
        )

        # 날짜
        date_text = datetime.now().strftime('%Y년 %m월 %d일')
        draw.text(
            (self.width - 250, 25),
            date_text,
            fill=self.colors['text_primary'],
            font=logo_font
        )

        # 타이틀
        title_font = self._get_font(28, bold=True)
        draw.text(
            (40, 60),
            title,
            fill=self.colors['text_primary'],
            font=title_font
        )

    def _draw_stock_info_card(
        self,
        draw: ImageDraw,
        symbol: str,
        name: str,
        price: float,
        change: float
    ):
        """종목 정보 카드 그리기"""
        card_y = 120
        card_height = 140

        # 카드 배경
        draw.rectangle(
            [30, card_y, self.width - 30, card_y + card_height],
            fill=self.colors['card'],
            outline=self.colors['accent'],
            width=3
        )

        # 종목 심볼 (큰 글씨)
        symbol_font = self._get_font(48, bold=True)
        draw.text(
            (50, card_y + 20),
            symbol,
            fill=self.colors['text_primary'],
            font=symbol_font
        )

        # 종목명
        name_font = self._get_font(20)
        draw.text(
            (50, card_y + 85),
            name,
            fill=self.colors['text_secondary'],
            font=name_font
        )

        # 현재가
        price_font = self._get_font(42, bold=True)
        price_text = f"${price:,.2f}"
        draw.text(
            (self.width - 450, card_y + 20),
            price_text,
            fill=self.colors['text_primary'],
            font=price_font
        )

        # 변동률
        change_color = self.colors['success'] if change >= 0 else self.colors['danger']
        change_font = self._get_font(36, bold=True)
        change_text = f"{change:+.2f}%"

        # 변동률 배경
        change_bg_width = 180
        change_bg_height = 50
        change_bg_x = self.width - 200
        change_bg_y = card_y + 80

        draw.rectangle(
            [change_bg_x, change_bg_y, change_bg_x + change_bg_width, change_bg_y + change_bg_height],
            fill=change_color,
            outline=None
        )

        draw.text(
            (change_bg_x + 25, change_bg_y + 7),
            change_text,
            fill=(255, 255, 255),
            font=change_font
        )

    def _draw_summary(self, draw: ImageDraw, summary: str):
        """요약 그리기"""
        summary_y = 290

        # 섹션 타이틀
        section_font = self._get_font(24, bold=True)
        draw.text(
            (50, summary_y),
            "📊 브리핑 요약",
            fill=self.colors['accent'],
            font=section_font
        )

        # 요약 텍스트
        summary_font = self._get_font(20)
        lines = self._wrap_text(summary, summary_font, self.width - 100)

        y_position = summary_y + 45
        for line in lines[:5]:  # 최대 5줄
            draw.text(
                (50, y_position),
                line,
                fill=self.colors['text_secondary'],
                font=summary_font
            )
            y_position += 35

    def _draw_highlights(self, draw: ImageDraw, highlights: list):
        """주요 포인트 그리기"""
        highlights_y = 480

        # 섹션 타이틀
        section_font = self._get_font(22, bold=True)
        draw.text(
            (50, highlights_y),
            "✨ 주요 포인트",
            fill=self.colors['accent'],
            font=section_font
        )

        # 하이라이트 리스트
        bullet_font = self._get_font(18)
        y_position = highlights_y + 40

        for i, highlight in enumerate(highlights[:3]):  # 최대 3개
            # 불릿 포인트
            draw.ellipse(
                [60, y_position + 5, 70, y_position + 15],
                fill=self.colors['accent']
            )

            # 텍스트
            draw.text(
                (85, y_position),
                highlight,
                fill=self.colors['text_secondary'],
                font=bullet_font
            )
            y_position += 30

    def _draw_footer(self, draw: ImageDraw):
        """푸터 그리기"""
        footer_y = self.height - 40

        # 구분선
        draw.line(
            [40, footer_y - 10, self.width - 40, footer_y - 10],
            fill=self.colors['accent'],
            width=2
        )

        # 생성 정보
        footer_font = self._get_font(14)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M KST')

        draw.text(
            (40, footer_y),
            f"🤖 AI Generated | {timestamp}",
            fill=self.colors['text_secondary'],
            font=footer_font
        )

        # 브랜딩
        draw.text(
            (self.width - 300, footer_y),
            "Powered by Claude & Gemini",
            fill=self.colors['text_secondary'],
            font=footer_font
        )

    def _get_font(self, size: int, bold: bool = False):
        """폰트 로드"""
        font_paths = [
            "C:/Windows/Fonts/malgun.ttf",
            "C:/Windows/Fonts/arial.ttf",
            "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        ]

        for font_path in font_paths:
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue

        return ImageFont.load_default()

    def _wrap_text(self, text: str, font: ImageFont, max_width: int) -> list:
        """텍스트 줄바꿈"""
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


# 실행 예제
if __name__ == "__main__":
    generator = BriefingCardGenerator()

    # 샘플 브리핑 데이터
    briefing_data = {
        'title': "오늘의 화제 종목",
        'summary': (
            "엔비디아(NVDA)가 AI 반도체 시장에서의 강력한 입지를 바탕으로 "
            "주가가 급등했습니다. 최신 GPU 제품 발표와 함께 데이터센터 수요 "
            "증가로 실적 전망이 크게 개선되었습니다. 시장 전문가들은 "
            "AI 붐이 지속되면서 엔비디아의 성장세가 당분간 계속될 것으로 전망하고 있습니다."
        ),
        'stock_symbol': 'NVDA',
        'stock_name': 'NVIDIA Corporation',
        'current_price': 495.50,
        'change_percent': 7.25,
        'highlights': [
            "신형 GPU H200 발표로 시장 점유율 확대 기대",
            "데이터센터 부문 매출 전년 대비 217% 급증",
            "주요 투자은행들 목표가 상향 조정"
        ]
    }

    # 브리핑 카드 생성
    output_path = generator.create_briefing_card(
        title=briefing_data['title'],
        summary=briefing_data['summary'],
        stock_symbol=briefing_data['stock_symbol'],
        stock_name=briefing_data['stock_name'],
        current_price=briefing_data['current_price'],
        change_percent=briefing_data['change_percent'],
        highlights=briefing_data['highlights']
    )

    print(f"\nSaved to: {Path(output_path).absolute()}")
    print("Briefing card generated successfully!")
