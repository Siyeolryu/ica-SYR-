"""
JSON 파일에서 브리핑 데이터를 읽어 Word 문서를 생성하는 스크립트
"""
import json
import sys
from pathlib import Path
from datetime import datetime
import logging

from docx_generator import create_briefing_report

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def convert_json_to_docx_format(json_path: str) -> dict:
    """
    JSON 파일을 읽어 python-docx 형식으로 변환

    Args:
        json_path: JSON 파일 경로

    Returns:
        python-docx용 데이터 딕셔너리
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    briefing = data.get('briefing', {})
    stock_data = data.get('stock_data', {})

    # 날짜 포맷팅
    generated_at = briefing.get('generated_at', datetime.now().isoformat())
    try:
        date_obj = datetime.fromisoformat(generated_at)
        date_str = date_obj.strftime('%Y년 %m월 %d일')
    except:
        date_str = datetime.now().strftime('%Y년 %m월 %d일')

    # 뉴스 요약 생성 (실제 뉴스 제목들로부터)
    news_articles = stock_data.get('news_articles', [])
    news_summary_parts = []

    if news_articles:
        news_summary_parts.append("주요 뉴스:")
        for i, article in enumerate(news_articles[:5], 1):
            title = article.get('title', '제목 없음')
            if title and title.strip():
                news_summary_parts.append(f"{i}. {title}")

    news_summary = '\n'.join(news_summary_parts) if news_summary_parts else '뉴스 정보를 확인할 수 없습니다.'

    # 종목 데이터 구성
    stocks = [{
        'symbol': stock_data.get('symbol', ''),
        'name': stock_data.get('name', ''),
        'price': stock_data.get('price', 0.0),
        'change_percent': stock_data.get('change_percent', 0.0),
        'volume': stock_data.get('volume', 0),
        'news_summary': news_summary,
    }]

    # 시장 요약 생성
    symbol = stock_data.get('symbol', '')
    name = stock_data.get('name', '')
    price = stock_data.get('price', 0.0)
    change_pct = stock_data.get('change_percent', 0.0)
    volume = stock_data.get('volume', 0)
    market_cap = stock_data.get('market_cap', 0)

    change_direction = "상승" if change_pct > 0 else "하락" if change_pct < 0 else "보합"

    summary = f"""
{name} ({symbol})이 오늘 화제의 중심에 있습니다.

현재 주가는 ${price:.2f}로 전일 대비 {abs(change_pct):.2f}% {change_direction}했습니다.
거래량은 {volume:,}주를 기록하며 시장의 높은 관심을 받고 있습니다.
시가총액은 ${market_cap/1e12:.2f}조 달러입니다.

최근 주요 뉴스와 애널리스트 의견을 통해 {symbol}의 동향을 확인해보세요.
    """.strip()

    return {
        'date': date_str,
        'title': '당신이 잠든 사이 - 미국 주식 브리핑',
        'summary': summary,
        'stocks': stocks
    }


def main():
    if len(sys.argv) < 2:
        print("사용법: python generate_briefing_from_json.py <json_path> [output_path]")
        sys.exit(1)

    json_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    if not Path(json_path).exists():
        logger.error(f"JSON 파일을 찾을 수 없습니다: {json_path}")
        sys.exit(1)

    # 데이터 변환
    logger.info(f"JSON 파일 읽기: {json_path}")
    docx_data = convert_json_to_docx_format(json_path)

    # 출력 경로 결정
    if not output_path:
        json_file = Path(json_path)
        output_filename = json_file.stem.replace('briefing', 'briefing_report') + '.docx'
        output_path = json_file.parent / 'reports' / output_filename

    output_path = Path(output_path)

    # Word 문서 생성
    logger.info(f"Word 문서 생성 중: {output_path}")
    result_path = create_briefing_report(
        docx_data,
        str(output_path),
        include_charts=False
    )

    print("\n" + "=" * 80)
    print("✓ 브리핑 Word 문서 생성 완료!")
    print("=" * 80)
    print(f"파일 위치: {result_path}")
    print(f"파일 크기: {Path(result_path).stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
