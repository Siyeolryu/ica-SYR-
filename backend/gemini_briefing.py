"""
Google Gemini API를 사용하여 브리핑 텍스트와 뉴스 요약을 생성하는 모듈
"""
from google import genai
from typing import List, Dict, Optional
import logging
import os
from datetime import datetime
from pathlib import Path
import base64
from io import BytesIO

# 로깅 설정 (모듈 최상단에서 초기화)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logger.warning("Pillow가 설치되지 않았습니다. 이미지 생성 기능이 제한될 수 있습니다.")

# .env 파일에서 API 키 로드 (python-dotenv 사용)
try:
    from dotenv import load_dotenv
    # backend 폴더의 .env 파일 로드
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        logger.info(".env 파일에서 API 키를 로드했습니다.")
except ImportError:
    logger.warning("python-dotenv가 설치되지 않았습니다. 환경 변수에서만 API 키를 가져옵니다.")

# 환경 변수에서 API 키 가져오기
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')


def initialize_client(api_key: Optional[str] = None) -> genai.Client:
    """
    Gemini API 클라이언트를 초기화합니다.
    
    Args:
        api_key: Gemini API 키 (없으면 환경 변수에서 가져옴)
    
    Returns:
        Gemini API 클라이언트
    """
    api_key = api_key or GEMINI_API_KEY
    
    if not api_key:
        raise ValueError(
            "Gemini API 키가 필요합니다. "
            "환경 변수 GEMINI_API_KEY를 설정하거나 api_key 파라미터를 제공하세요."
        )
    
    return genai.Client(api_key=api_key)


def translate_news_to_korean(news_articles: List[Dict], api_key: Optional[str] = None) -> List[Dict]:
    """
    뉴스 제목과 요약을 한국어로 번역합니다.
    
    Args:
        news_articles: 뉴스 기사 리스트 (title, summary 포함)
        api_key: Gemini API 키
    
    Returns:
        번역된 뉴스 기사 리스트
    """
    try:
        client = initialize_client(api_key)
        translated_articles = []
        
        for article in news_articles:
            # 번역할 텍스트 준비
            title = article.get('title', '')
            summary = article.get('summary', '')
            
            if not title:
                translated_articles.append(article)
                continue
            
            # 프롬프트 구성
            prompt = f"""다음 영문 뉴스 제목을 자연스러운 한국어로 번역해주세요.
뉴스의 맥락과 의미를 유지하면서 한국 독자가 이해하기 쉽게 번역해주세요.

제목: {title}

번역된 제목만 출력하고, 다른 설명은 생략하세요."""

            # Gemini API 호출
            response = client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            translated_title = response.text.strip()
            
            # 요약이 있으면 번역 (너무 짧거나 없으면 건너뛰기)
            translated_summary = summary
            if summary and len(summary) > 20:
                summary_prompt = f"""다음 영문 뉴스 요약을 자연스러운 한국어로 번역해주세요.

요약: {summary}

번역된 요약만 출력하고, 다른 설명은 생략하세요."""
                
                try:
                    summary_response = client.models.generate_content(
                        model='gemini-2.0-flash-exp',
                        contents=summary_prompt
                    )
                    translated_summary = summary_response.text.strip()
                except Exception as e:
                    logger.warning(f"요약 번역 실패: {str(e)}")
            
            # 번역된 내용으로 업데이트
            translated_article = article.copy()
            translated_article['title'] = translated_title
            translated_article['summary'] = translated_summary
            translated_article['title_en'] = title  # 원본 제목 보존
            
            translated_articles.append(translated_article)
            
            logger.info(f"번역 완료: {title[:50]}... -> {translated_title[:50]}...")
        
        return translated_articles
        
    except Exception as e:
        logger.error(f"뉴스 번역 중 오류 발생: {str(e)}")
        # 오류 발생 시 원본 반환
        return news_articles


def generate_briefing_text(
    stocks: List[Dict],
    language: str = 'ko',
    api_key: Optional[str] = None
) -> Dict[str, str]:
    """
    주식 데이터를 기반으로 브리핑 텍스트를 생성합니다.
    
    Args:
        stocks: 종목 정보 리스트
        language: 언어 ('ko' 또는 'en')
        api_key: Gemini API 키 (선택)
    
    Returns:
        브리핑 텍스트 딕셔너리 (title, summary, sections)
    """
    try:
        client = initialize_client(api_key)
        
        # 종목 정보를 텍스트로 변환
        stocks_text = "\n\n".join([
            f"종목: {stock.get('symbol', 'N/A')} ({stock.get('name', 'N/A')})\n"
            f"현재가: ${stock.get('price', 0):.2f}\n"
            f"변동률: {stock.get('change_percent', 0):+.2f}%\n"
            f"거래량: {stock.get('volume', 0):,}"
            for stock in stocks
        ])
        
        # 프롬프트 생성
        lang_instruction = "한국어로" if language == 'ko' else "in English"
        
        prompt = f"""다음은 오늘 미국 증시에서 가장 활발했던 주식 종목들입니다:

{stocks_text}

이 정보를 바탕으로 {lang_instruction} 다음 형식으로 브리핑을 작성해주세요:

1. 제목: 간결하고 매력적인 제목 (예: "오늘의 화제 종목 브리핑")
2. 요약: 전체적인 시장 동향을 2-3문장으로 요약
3. 각 종목별 섹션:
   - 종목명 (심볼)
   - 핵심 내용: 가격 변동과 거래량을 바탕으로 한 간단한 분석 (2-3문장)

JSON 형식으로 반환해주세요:
{{
  "title": "제목",
  "summary": "요약",
  "sections": [
    {{
      "stock_symbol": "AAPL",
      "title": "Apple Inc. (AAPL)",
      "content": "핵심 내용"
    }}
  ]
}}
"""
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt,
        )
        
        # 응답 파싱 (실제로는 JSON 파싱이 필요할 수 있음)
        result_text = response.text
        
        # 간단한 파싱 (실제로는 더 정교한 JSON 파싱 필요)
        # 여기서는 기본 구조만 반환
        sections = []
        for stock in stocks:
            sections.append({
                'stock_symbol': stock.get('symbol', ''),
                'title': f"{stock.get('name', '')} ({stock.get('symbol', '')})",
                'content': f"{stock.get('name', '')}는 전일 대비 {stock.get('change_percent', 0):+.2f}% 변동하며 거래량 {stock.get('volume', 0):,}주를 기록했습니다."
            })
        
        return {
            'title': f"오늘의 화제 종목 브리핑 ({datetime.now().strftime('%Y년 %m월 %d일')})" if language == 'ko' else f"Today's Trending Stocks ({datetime.now().strftime('%B %d, %Y')})",
            'summary': f"{len(stocks)}개 종목이 오늘 시장에서 주목받았습니다." if language == 'ko' else f"{len(stocks)} stocks gained attention in today's market.",
            'sections': sections,
            'raw_response': result_text,  # 디버깅용
        }
    
    except Exception as e:
        logger.error(f"브리핑 텍스트 생성 실패: {str(e)}")
        # 에러 발생 시 기본 템플릿 반환
        sections = []
        for stock in stocks:
            sections.append({
                'stock_symbol': stock.get('symbol', ''),
                'title': f"{stock.get('name', '')} ({stock.get('symbol', '')})",
                'content': f"{stock.get('name', '')}는 전일 대비 {stock.get('change_percent', 0):+.2f}% 변동했습니다."
            })
        
        return {
            'title': "오늘의 화제 종목 브리핑",
            'summary': f"{len(stocks)}개 종목이 오늘 시장에서 주목받았습니다.",
            'sections': sections,
        }


def summarize_news(
    news_articles: List[Dict],
    language: str = 'ko',
    api_key: Optional[str] = None
) -> str:
    """
    뉴스 기사들을 요약합니다.
    
    Args:
        news_articles: 뉴스 기사 리스트 (각 기사는 title, content 등을 포함)
        language: 언어 ('ko' 또는 'en')
        api_key: Gemini API 키 (선택)
    
    Returns:
        요약된 텍스트
    """
    try:
        client = initialize_client(api_key)
        
        # 뉴스 기사를 텍스트로 변환
        news_text = "\n\n---\n\n".join([
            f"제목: {article.get('title', 'N/A')}\n"
            f"내용: {article.get('content', article.get('summary', 'N/A'))[:500]}"
            for article in news_articles
        ])
        
        lang_instruction = "한국어로" if language == 'ko' else "in English"
        
        prompt = f"""다음 뉴스 기사들을 {lang_instruction} 3-5문장으로 요약해주세요:

{news_text}

요약:
"""
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt,
        )
        
        return response.text
    
    except Exception as e:
        logger.error(f"뉴스 요약 실패: {str(e)}")
        return "뉴스 요약을 생성할 수 없습니다."


def generate_stock_analysis(
    stock_symbol: str,
    stock_data: Dict,
    language: str = 'ko',
    api_key: Optional[str] = None
) -> str:
    """
    특정 종목에 대한 분석을 생성합니다.
    
    Args:
        stock_symbol: 종목 심볼
        stock_data: 종목 데이터
        language: 언어 ('ko' 또는 'en')
        api_key: Gemini API 키 (선택)
    
    Returns:
        분석 텍스트
    """
    try:
        client = initialize_client(api_key)
        
        lang_instruction = "한국어로" if language == 'ko' else "in English"
        
        prompt = f"""다음 {stock_symbol} 종목 정보를 바탕으로 {lang_instruction} 간단한 분석을 작성해주세요:

종목명: {stock_data.get('name', 'N/A')}
현재가: ${stock_data.get('price', 0):.2f}
변동률: {stock_data.get('change_percent', 0):+.2f}%
거래량: {stock_data.get('volume', 0):,}
시가총액: {stock_data.get('market_cap', 0):,}
섹터: {stock_data.get('sector', 'N/A')}

2-3문장으로 핵심 내용을 요약해주세요:
"""
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt,
        )
        
        return response.text
    
    except Exception as e:
        logger.error(f"종목 분석 생성 실패: {str(e)}")
        return f"{stock_symbol}에 대한 분석을 생성할 수 없습니다."


def generate_briefing_image(
    briefing_text: Dict[str, str],
    stock_data: Dict,
    language: str = 'ko',
    api_key: Optional[str] = None,
    output_path: Optional[str] = None
) -> Optional[str]:
    """
    브리핑 텍스트를 기반으로 이미지를 생성합니다.
    
    Args:
        briefing_text: generate_briefing_text()의 반환값
        stock_data: 종목 데이터
        language: 언어 ('ko' 또는 'en')
        api_key: Gemini API 키 (선택)
        output_path: 이미지 저장 경로 (선택, 없으면 BytesIO 반환)
    
    Returns:
        이미지 파일 경로 또는 base64 인코딩된 이미지 데이터
    """
    try:
        client = initialize_client(api_key)
        
        # 이미지 생성을 위한 프롬프트 생성
        lang_instruction = "한국어로" if language == 'ko' else "in English"
        
        image_prompt = f"""다음 주식 브리핑 정보를 시각적으로 아름다운 이미지로 만들어주세요:

제목: {briefing_text.get('title', '')}
요약: {briefing_text.get('summary', '')}

종목 정보:
- 심볼: {stock_data.get('symbol', 'N/A')}
- 종목명: {stock_data.get('name', 'N/A')}
- 현재가: ${stock_data.get('price', 0):.2f}
- 변동률: {stock_data.get('change_percent', 0):+.2f}%

{lang_instruction} 전문적이고 깔끔한 디자인의 브리핑 이미지를 생성해주세요.
주식 차트, 그래프, 아이콘 등을 포함하여 시각적으로 매력적인 이미지로 만들어주세요.
"""
        
        # Gemini API로 이미지 생성 시도
        # 참고: Gemini API의 이미지 생성 기능은 제한적일 수 있음
        # 실제로는 텍스트를 이미지로 렌더링하는 방식 사용
        try:
            # Gemini 2.0 Flash는 이미지 생성보다는 텍스트 기반 작업에 특화되어 있음
            # 따라서 Pillow를 사용하여 텍스트를 이미지로 렌더링
            return generate_briefing_image_with_pillow(
                briefing_text, stock_data, language, output_path
            )
        except Exception as e:
            logger.warning(f"Gemini 이미지 생성 실패, Pillow로 대체: {str(e)}")
            return generate_briefing_image_with_pillow(
                briefing_text, stock_data, language, output_path
            )
    
    except Exception as e:
        logger.error(f"브리핑 이미지 생성 실패: {str(e)}")
        return None


def generate_briefing_image_with_pillow(
    briefing_text: Dict[str, str],
    stock_data: Dict,
    language: str = 'ko',
    output_path: Optional[str] = None
) -> Optional[str]:
    """
    Pillow를 사용하여 브리핑 텍스트를 이미지로 렌더링합니다.
    
    Args:
        briefing_text: generate_briefing_text()의 반환값
        stock_data: 종목 데이터
        language: 언어 ('ko' 또는 'en')
        output_path: 이미지 저장 경로 (선택)
    
    Returns:
        이미지 파일 경로 또는 base64 인코딩된 이미지 데이터
    """
    if not PIL_AVAILABLE:
        logger.error("Pillow가 설치되지 않아 이미지를 생성할 수 없습니다.")
        return None
    
    try:
        # 이미지 크기 설정
        width, height = 1200, 1600
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        
        # 폰트 설정 (시스템 기본 폰트 사용)
        try:
            title_font = ImageFont.truetype("arial.ttf", 48)
            subtitle_font = ImageFont.truetype("arial.ttf", 32)
            body_font = ImageFont.truetype("arial.ttf", 24)
        except:
            # 폰트를 찾을 수 없으면 기본 폰트 사용
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            body_font = ImageFont.load_default()
        
        y_position = 50
        
        # 제목 그리기
        title = briefing_text.get('title', '주식 브리핑')
        draw.text((50, y_position), title, fill='black', font=title_font)
        y_position += 80
        
        # 요약 그리기
        summary = briefing_text.get('summary', '')
        draw.text((50, y_position), summary, fill='gray', font=body_font)
        y_position += 100
        
        # 종목 정보 그리기
        symbol = stock_data.get('symbol', 'N/A')
        name = stock_data.get('name', 'N/A')
        price = stock_data.get('price', 0)
        change_percent = stock_data.get('change_percent', 0)
        
        stock_info = f"{symbol} - {name}"
        draw.text((50, y_position), stock_info, fill='blue', font=subtitle_font)
        y_position += 60
        
        price_text = f"현재가: ${price:.2f}"
        draw.text((50, y_position), price_text, fill='black', font=body_font)
        y_position += 40
        
        change_color = 'green' if change_percent >= 0 else 'red'
        change_text = f"변동률: {change_percent:+.2f}%"
        draw.text((50, y_position), change_text, fill=change_color, font=body_font)
        y_position += 60
        
        # 섹션 그리기
        sections = briefing_text.get('sections', [])
        for section in sections[:3]:  # 최대 3개 섹션만
            section_title = section.get('title', '')
            section_content = section.get('content', '')
            
            draw.text((50, y_position), section_title, fill='darkblue', font=subtitle_font)
            y_position += 50
            
            # 긴 텍스트는 줄바꿈 처리
            words = section_content.split()
            line = ""
            for word in words:
                test_line = line + word + " "
                bbox = draw.textbbox((0, 0), test_line, font=body_font)
                if bbox[2] - bbox[0] < width - 100:
                    line = test_line
                else:
                    draw.text((50, y_position), line, fill='black', font=body_font)
                    y_position += 35
                    line = word + " "
            if line:
                draw.text((50, y_position), line, fill='black', font=body_font)
                y_position += 50
            
            y_position += 20
        
        # 이미지 저장 또는 반환
        if output_path:
            image.save(output_path, 'PNG')
            logger.info(f"이미지 저장 완료: {output_path}")
            return output_path
        else:
            # BytesIO로 변환하여 base64 인코딩
            buffer = BytesIO()
            image.save(buffer, format='PNG')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            return image_base64
    
    except Exception as e:
        logger.error(f"Pillow 이미지 생성 실패: {str(e)}")
        return None


def analyze_why_trending(
    stock_symbol: str,
    stock_data: Dict,
    news_articles: List[Dict],
    language: str = 'ko',
    api_key: Optional[str] = None
) -> str:
    """
    종목이 왜 화제인지 분석합니다.
    
    Args:
        stock_symbol: 종목 심볼
        stock_data: 종목 데이터
        news_articles: 관련 뉴스 기사 리스트
        language: 언어 ('ko' 또는 'en')
        api_key: Gemini API 키 (선택)
    
    Returns:
        화제 원인 분석 텍스트
    """
    try:
        client = initialize_client(api_key)
        
        # 뉴스 제목과 요약 수집
        news_summary = "\n".join([
            f"- {article.get('title', '')}: {article.get('summary', '')[:200]}"
            for article in news_articles[:5]
        ])
        
        lang_instruction = "한국어로" if language == 'ko' else "in English"
        
        prompt = f"""다음 종목이 왜 화제가 되었는지 분석해주세요:

종목: {stock_symbol} ({stock_data.get('name', 'N/A')})
현재가: ${stock_data.get('price', 0):.2f}
변동률: {stock_data.get('change_percent', 0):+.2f}%
거래량: {stock_data.get('volume', 0):,}

관련 뉴스:
{news_summary}

{lang_instruction} 3-5문장으로 이 종목이 화제가 된 주요 원인을 분석해주세요.
뉴스 내용, 가격 변동, 거래량 등을 종합하여 설명해주세요.
"""
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt,
        )
        
        return response.text
    
    except Exception as e:
        logger.error(f"화제 원인 분석 실패: {str(e)}")
        return f"{stock_symbol}이 화제가 된 원인을 분석할 수 없습니다."


if __name__ == "__main__":
    # 테스트용 목업 데이터
    test_stocks = [
        {
            'symbol': 'AAPL',
            'name': 'Apple Inc.',
            'price': 185.50,
            'change_percent': 2.35,
            'volume': 45234567,
            'market_cap': 2850000000000,
        },
        {
            'symbol': 'TSLA',
            'name': 'Tesla, Inc.',
            'price': 245.30,
            'change_percent': 5.12,
            'volume': 38923456,
            'market_cap': 780000000000,
        },
    ]
    
    print("=" * 60)
    print("Google Gemini API 테스트")
    print("=" * 60)
    
    # API 키 확인
    if not GEMINI_API_KEY:
        print("\n⚠️  GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")
        print("다음 명령어로 설정하세요:")
        print("  Windows: set GEMINI_API_KEY=your_api_key")
        print("  Linux/Mac: export GEMINI_API_KEY=your_api_key")
        print("\n또는 코드에서 직접 api_key 파라미터를 제공하세요.")
    else:
        try:
            # 브리핑 텍스트 생성 테스트
            print("\n1. 브리핑 텍스트 생성:")
            briefing = generate_briefing_text(test_stocks, language='ko')
            print(f"   제목: {briefing['title']}")
            print(f"   요약: {briefing['summary']}")
            print(f"   섹션 수: {len(briefing['sections'])}")
            
            # 종목 분석 생성 테스트
            print("\n2. 종목 분석 생성:")
            analysis = generate_stock_analysis('AAPL', test_stocks[0], language='ko')
            print(f"   {analysis[:200]}...")
            
        except Exception as e:
            print(f"\n❌ 오류 발생: {str(e)}")
            print("API 키를 확인하고 다시 시도하세요.")

