"""
Gemini API 연결 테스트 스크립트
"""
from gemini_briefing import generate_briefing_text, initialize_client
import os

def test_gemini_connection():
    """Gemini API 연결을 테스트합니다."""
    print("=" * 60)
    print("Google Gemini API 연결 테스트")
    print("=" * 60)
    
    # API 키 확인
    api_key = os.getenv('GEMINI_API_KEY', '')
    
    if not api_key:
        print("\n❌ GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")
        print("다음 중 하나의 방법으로 설정하세요:")
        print("  1. backend/.env 파일에 GEMINI_API_KEY=your_key 추가")
        print("  2. 환경 변수로 설정: set GEMINI_API_KEY=your_key (Windows)")
        print("  3. 환경 변수로 설정: export GEMINI_API_KEY=your_key (Linux/Mac)")
        return False
    
    print(f"\n✅ API 키가 설정되었습니다. (길이: {len(api_key)} 문자)")
    
    try:
        # 클라이언트 초기화 테스트
        print("\n1. 클라이언트 초기화 중...")
        client = initialize_client(api_key)
        print("   ✅ 클라이언트 초기화 성공")
        
        # 간단한 API 호출 테스트
        print("\n2. API 호출 테스트 중...")
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents="한 문장으로 '안녕하세요'라고 인사해주세요.",
        )
        print(f"   ✅ API 호출 성공")
        print(f"   응답: {response.text}")
        
        # 브리핑 생성 테스트
        print("\n3. 브리핑 생성 테스트 중...")
        test_stocks = [
            {
                'symbol': 'AAPL',
                'name': 'Apple Inc.',
                'price': 185.50,
                'change_percent': 2.35,
                'volume': 45234567,
            },
        ]
        briefing = generate_briefing_text(test_stocks, language='ko', api_key=api_key)
        print(f"   ✅ 브리핑 생성 성공")
        print(f"   제목: {briefing['title']}")
        print(f"   요약: {briefing['summary']}")
        
        print("\n" + "=" * 60)
        print("✅ 모든 테스트 통과!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        print("\n문제 해결 방법:")
        print("  1. API 키가 올바른지 확인하세요")
        print("  2. 인터넷 연결을 확인하세요")
        print("  3. Gemini API 서비스 상태를 확인하세요")
        return False

if __name__ == "__main__":
    test_gemini_connection()




















