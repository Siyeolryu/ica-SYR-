"""
여러 종목의 브리핑 카드를 생성하는 스크립트
"""

from generate_briefing_card import BriefingCardGenerator
from pathlib import Path


def create_sample_briefings():
    """샘플 브리핑 카드 여러 개 생성"""
    generator = BriefingCardGenerator()

    # 브리핑 데이터 샘플
    briefings = [
        {
            'title': "오늘의 화제 종목",
            'summary': (
                "테슬라(TSLA)가 새로운 전기차 모델 출시 발표와 함께 주가가 상승세를 보이고 있습니다. "
                "자율주행 기술의 획기적인 발전과 배터리 효율성 개선으로 시장의 큰 관심을 받고 있으며, "
                "전 세계적으로 전기차 수요가 증가하면서 테슬라의 시장 지배력이 더욱 강화될 것으로 전망됩니다."
            ),
            'stock_symbol': 'TSLA',
            'stock_name': 'Tesla, Inc.',
            'current_price': 248.75,
            'change_percent': 5.42,
            'highlights': [
                "신형 Model 3 Performance 출시 발표",
                "완전자율주행(FSD) 기능 업데이트 예정",
                "중국 시장에서 판매량 급증"
            ]
        },
        {
            'title': "애플, 신제품 이벤트 앞두고 강세",
            'summary': (
                "애플(AAPL)이 다음 주 예정된 신제품 발표 이벤트를 앞두고 투자자들의 기대감이 높아지고 있습니다. "
                "새로운 아이폰과 맥북 라인업 공개가 예상되며, 특히 AI 기능이 대폭 강화된 제품들이 "
                "소비자들의 큰 관심을 받을 것으로 예상됩니다."
            ),
            'stock_symbol': 'AAPL',
            'stock_name': 'Apple Inc.',
            'current_price': 195.25,
            'change_percent': 2.18,
            'highlights': [
                "신형 iPhone 16 시리즈 발표 임박",
                "AI 칩 M4 탑재 맥북 프로 출시 예정",
                "서비스 부문 매출 사상 최고치 경신"
            ]
        },
        {
            'title': "마이크로소프트, 클라우드 성장 지속",
            'summary': (
                "마이크로소프트(MSFT)의 Azure 클라우드 서비스가 예상을 뛰어넘는 성장세를 보이며 "
                "기업 가치가 상승하고 있습니다. AI 서비스 통합과 엔터프라이즈 고객 확대로 "
                "클라우드 시장에서의 입지가 더욱 강화되고 있습니다."
            ),
            'stock_symbol': 'MSFT',
            'stock_name': 'Microsoft Corporation',
            'current_price': 415.30,
            'change_percent': 1.85,
            'highlights': [
                "Azure AI 서비스 고객 수 200% 증가",
                "GitHub Copilot 유료 구독자 100만 돌파",
                "게임 부문(Xbox) 실적 호조"
            ]
        }
    ]

    created_files = []

    for briefing in briefings:
        output_path = generator.create_briefing_card(
            title=briefing['title'],
            summary=briefing['summary'],
            stock_symbol=briefing['stock_symbol'],
            stock_name=briefing['stock_name'],
            current_price=briefing['current_price'],
            change_percent=briefing['change_percent'],
            highlights=briefing['highlights']
        )
        created_files.append(output_path)

    return created_files


if __name__ == "__main__":
    print("Creating multiple briefing cards...")
    print("-" * 60)

    files = create_sample_briefings()

    print("\n" + "=" * 60)
    print("All briefing cards created successfully!")
    print("=" * 60)

    for i, file in enumerate(files, 1):
        print(f"{i}. {Path(file).name}")

    print(f"\nTotal: {len(files)} briefing cards")
    print(f"Location: {Path(files[0]).parent.absolute()}")
