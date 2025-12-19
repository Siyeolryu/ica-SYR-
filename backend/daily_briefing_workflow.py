"""
매일 아침 자동 실행되는 브리핑 생성 워크플로우
"""
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List
import json

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 모듈 임포트
from get_trending_stocks import get_top_trending_stock, format_stock_data
from exa_news import search_stock_news, get_news_summary
from gemini_briefing import (
    generate_briefing_text,
    generate_briefing_image,
    analyze_why_trending,
    generate_stock_analysis
)
from send_briefing import send_briefing_to_channels

# 출력 디렉토리 설정
OUTPUT_DIR = Path(__file__).parent / 'output'
OUTPUT_DIR.mkdir(exist_ok=True)


def step1_collect_trending_stocks() -> Optional[Dict]:
    """
    Step 1: 화제 종목 수집 및 TOP 1 선정
    
    Returns:
        TOP 1 종목 정보 또는 None
    """
    logger.info("=" * 60)
    logger.info("Step 1: 화제 종목 수집 시작")
    logger.info("=" * 60)
    
    try:
        # Yahoo Finance Screener를 사용하여 TOP 1 종목 선정
        top_stock = get_top_trending_stock(
            screener_types=['most_actives', 'day_gainers'],
            count=5
        )
        
        if not top_stock:
            logger.error("화제 종목을 찾을 수 없습니다.")
            return None
        
        # 데이터 포맷팅
        formatted_stock = format_stock_data(top_stock)
        
        logger.info(f"TOP 1 종목 선정 완료: {formatted_stock['symbol']} ({formatted_stock['name']})")
        logger.info(f"  현재가: ${formatted_stock['price']:.2f}")
        logger.info(f"  변동률: {formatted_stock['change_percent']:+.2f}%")
        logger.info(f"  거래량: {formatted_stock['volume']:,}")
        
        return formatted_stock
    
    except Exception as e:
        logger.error(f"화제 종목 수집 실패: {str(e)}")
        return None


def step2_collect_stock_info(stock_data: Dict) -> Dict:
    """
    Step 2: 종목 정보 수집
    
    Args:
        stock_data: Step 1에서 수집한 종목 데이터
    
    Returns:
        종목 정보가 추가된 딕셔너리
    """
    logger.info("=" * 60)
    logger.info("Step 2: 종목 정보 수집 시작")
    logger.info("=" * 60)
    
    try:
        symbol = stock_data['symbol']
        name = stock_data.get('name', '')
        
        # 관련 뉴스 수집
        logger.info(f"{symbol} 관련 뉴스 수집 중...")
        news_articles = search_stock_news(
            symbol,
            stock_name=name,
            limit=5,
            days_back=7
        )
        
        stock_data['news_articles'] = news_articles
        logger.info(f"뉴스 {len(news_articles)}개 수집 완료")
        
        # 뉴스 요약 생성
        if news_articles:
            logger.info("뉴스 요약 생성 중...")
            news_summary = get_news_summary(news_articles, language='ko')
            stock_data['news_summary'] = news_summary
            logger.info("뉴스 요약 완료")
        
        # 종목 분석 생성
        logger.info("종목 분석 생성 중...")
        stock_analysis = generate_stock_analysis(
            symbol,
            stock_data,
            language='ko'
        )
        stock_data['analysis'] = stock_analysis
        logger.info("종목 분석 완료")
        
        # 왜 화제인지 분석
        logger.info("화제 원인 분석 중...")
        why_trending = analyze_why_trending(
            symbol,
            stock_data,
            news_articles,
            language='ko'
        )
        stock_data['why_trending'] = why_trending
        logger.info("화제 원인 분석 완료")
        
        return stock_data
    
    except Exception as e:
        logger.error(f"종목 정보 수집 실패: {str(e)}")
        return stock_data


def step3_generate_briefing(stock_data: Dict) -> Dict:
    """
    Step 3: 브리핑 콘텐츠 생성 (텍스트 + 이미지)
    
    Args:
        stock_data: 종목 데이터
    
    Returns:
        브리핑 데이터 딕셔너리
    """
    logger.info("=" * 60)
    logger.info("Step 3: 브리핑 콘텐츠 생성 시작")
    logger.info("=" * 60)
    
    try:
        # 브리핑 텍스트 생성
        logger.info("브리핑 텍스트 생성 중...")
        briefing_text = generate_briefing_text(
            [stock_data],
            language='ko'
        )
        logger.info("브리핑 텍스트 생성 완료")
        
        # 화제 원인 분석을 섹션에 추가
        if 'why_trending' in stock_data:
            briefing_text['sections'].append({
                'stock_symbol': stock_data['symbol'],
                'title': f"{stock_data['symbol']}이 화제가 된 이유",
                'content': stock_data['why_trending']
            })
        
        # 브리핑 이미지 생성
        logger.info("브리핑 이미지 생성 중...")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        image_filename = f"briefing_{stock_data['symbol']}_{timestamp}.png"
        image_path = OUTPUT_DIR / image_filename
        
        image_result = generate_briefing_image(
            briefing_text,
            stock_data,
            language='ko',
            output_path=str(image_path)
        )
        
        if image_result:
            logger.info(f"브리핑 이미지 생성 완료: {image_path}")
            briefing_text['image_path'] = str(image_path)
        else:
            logger.warning("브리핑 이미지 생성 실패")
            briefing_text['image_path'] = None
        
        # 메타데이터 추가
        briefing_text['generated_at'] = datetime.now().isoformat()
        briefing_text['stock_symbol'] = stock_data['symbol']
        briefing_text['stock_name'] = stock_data.get('name', '')
        
        return briefing_text
    
    except Exception as e:
        logger.error(f"브리핑 콘텐츠 생성 실패: {str(e)}")
        return {}


def step4_send_briefing(briefing_data: Dict, config: Optional[Dict] = None) -> Dict:
    """
    Step 4: 브리핑 자동 발송 (샘플)
    
    Args:
        briefing_data: 브리핑 데이터
        config: 발송 설정 (선택)
    
    Returns:
        발송 결과 딕셔너리
    """
    logger.info("=" * 60)
    logger.info("Step 4: 브리핑 자동 발송 시작")
    logger.info("=" * 60)
    
    # 기본 설정
    if config is None:
        config = {
            'email_recipients': [],  # 실제 사용 시 이메일 주소 리스트
            'slack_channels': []  # 실제 사용 시 슬랙 채널 리스트
        }
    
    try:
        # 발송 실행 (샘플)
        send_results = send_briefing_to_channels(
            briefing_data,
            image_path=briefing_data.get('image_path'),
            email_recipients=config.get('email_recipients', []),
            slack_channels=config.get('slack_channels', [])
        )
        
        logger.info(f"발송 완료: 성공 {send_results['total_sent']}개, 실패 {send_results['total_failed']}개")
        return send_results
    
    except Exception as e:
        logger.error(f"브리핑 발송 실패: {str(e)}")
        return {'total_sent': 0, 'total_failed': 1}


def save_briefing_data(briefing_data: Dict, stock_data: Dict) -> str:
    """
    브리핑 데이터를 JSON 파일로 저장
    
    Args:
        briefing_data: 브리핑 데이터
        stock_data: 종목 데이터
    
    Returns:
        저장된 파일 경로
    """
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"briefing_{stock_data['symbol']}_{timestamp}.json"
        filepath = OUTPUT_DIR / filename
        
        data_to_save = {
            'briefing': briefing_data,
            'stock_data': stock_data,
            'created_at': datetime.now().isoformat()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=2)
        
        logger.info(f"브리핑 데이터 저장 완료: {filepath}")
        return str(filepath)
    
    except Exception as e:
        logger.error(f"브리핑 데이터 저장 실패: {str(e)}")
        return ''


def run_daily_briefing_workflow(config: Optional[Dict] = None) -> Dict:
    """
    전체 워크플로우 실행
    
    Args:
        config: 설정 딕셔너리 (선택)
    
    Returns:
        실행 결과 딕셔너리
    """
    logger.info("=" * 80)
    logger.info("매일 아침 브리핑 워크플로우 시작")
    logger.info(f"실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 80)
    
    result = {
        'success': False,
        'steps_completed': [],
        'steps_failed': [],
        'stock_data': None,
        'briefing_data': None,
        'send_results': None,
        'error': None
    }
    
    try:
        # Step 1: 화제 종목 수집
        stock_data = step1_collect_trending_stocks()
        if not stock_data:
            result['error'] = '화제 종목을 찾을 수 없습니다.'
            return result
        result['steps_completed'].append('step1_collect_trending_stocks')
        result['stock_data'] = stock_data
        
        # Step 2: 종목 정보 수집
        stock_data = step2_collect_stock_info(stock_data)
        result['steps_completed'].append('step2_collect_stock_info')
        
        # Step 3: 브리핑 콘텐츠 생성
        briefing_data = step3_generate_briefing(stock_data)
        if not briefing_data:
            result['error'] = '브리핑 콘텐츠 생성 실패'
            return result
        result['steps_completed'].append('step3_generate_briefing')
        result['briefing_data'] = briefing_data
        
        # 브리핑 데이터 저장
        save_briefing_data(briefing_data, stock_data)
        
        # Step 4: 브리핑 발송 (샘플)
        send_results = step4_send_briefing(briefing_data, config)
        result['steps_completed'].append('step4_send_briefing')
        result['send_results'] = send_results
        
        result['success'] = True
        logger.info("=" * 80)
        logger.info("워크플로우 완료!")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"워크플로우 실행 중 오류 발생: {str(e)}")
        result['error'] = str(e)
        result['steps_failed'].append('workflow_execution')
    
    return result


if __name__ == "__main__":
    # 직접 실행 시 테스트
    print("=" * 80)
    print("매일 아침 브리핑 워크플로우 테스트")
    print("=" * 80)
    
    # 설정 (실제 사용 시 환경 변수나 설정 파일에서 로드)
    test_config = {
        'email_recipients': [],  # 실제 이메일 주소 리스트
        'slack_channels': []  # 실제 슬랙 채널 리스트
    }
    
    # 워크플로우 실행
    result = run_daily_briefing_workflow(test_config)
    
    # 결과 출력
    print("\n" + "=" * 80)
    print("실행 결과")
    print("=" * 80)
    print(f"성공: {result['success']}")
    print(f"완료된 단계: {', '.join(result['steps_completed'])}")
    if result['steps_failed']:
        print(f"실패한 단계: {', '.join(result['steps_failed'])}")
    if result['error']:
        print(f"오류: {result['error']}")
    
    if result['stock_data']:
        print(f"\n선정된 종목: {result['stock_data']['symbol']} ({result['stock_data'].get('name', '')})")
    
    if result['briefing_data']:
        print(f"\n브리핑 제목: {result['briefing_data'].get('title', '')}")
        if result['briefing_data'].get('image_path'):
            print(f"이미지 경로: {result['briefing_data']['image_path']}")

