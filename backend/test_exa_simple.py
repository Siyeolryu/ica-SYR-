"""
간단한 EXA API 테스트 스크립트
"""
import requests
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

api_key = os.getenv('EXA_API_KEY', '')

print("=" * 60)
print("EXA API 간단 테스트")
print("=" * 60)

if not api_key:
    print("[오류] EXA_API_KEY가 설정되지 않았습니다.")
    exit(1)

print(f"[정보] API 키 길이: {len(api_key)} 문자")
print(f"[정보] API 키 시작: {api_key[:8]}...")

# 간단한 검색 테스트
url = "https://api.exa.ai/search"
headers = {
    'x-api-key': api_key,
    'Content-Type': 'application/json',
}
payload = {
    'query': 'Apple stock news',
    'num_results': 2,
}

print(f"\n[요청] POST {url}")
print(f"[헤더] x-api-key: {api_key[:8]}...")
print(f"[본문] {payload}")

try:
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    
    print(f"\n[응답] 상태 코드: {response.status_code}")
    print(f"[응답] 헤더: {dict(response.headers)}")
    print(f"[응답] 본문: {response.text[:500]}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n[성공] 검색 결과: {len(data.get('results', []))}개")
    elif response.status_code == 401:
        print("\n[오류] 401 Unauthorized - API 키가 유효하지 않습니다.")
        print("       https://exa.ai/ 에서 API 키를 확인하거나 새로 발급받으세요.")
    else:
        print(f"\n[오류] {response.status_code} - {response.text}")
        
except requests.exceptions.Timeout:
    print("\n[오류] 요청 시간 초과 (10초)")
except Exception as e:
    print(f"\n[오류] {type(e).__name__}: {str(e)}")

print("\n" + "=" * 60)

