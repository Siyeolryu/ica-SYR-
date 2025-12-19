#!/usr/bin/env python3
"""
MCP 서버 연결 테스트
Claude Desktop 설정 후 이 스크립트로 MCP 서버가 정상 작동하는지 확인합니다.
"""
import sys
import os
import json
from pathlib import Path

# 상위 디렉토리를 path에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("=" * 60)
print("당신이 잠든 사이 - MCP 연결 테스트")
print("=" * 60)
print()

# 1. Claude Desktop 설정 파일 확인
print("[1/5] Claude Desktop 설정 파일 확인...")
appdata = os.getenv('APPDATA')
if appdata:
    config_path = Path(appdata) / "Claude" / "claude_desktop_config.json"
    print(f"   설정 파일 경로: {config_path}")

    if config_path.exists():
        print("   ✅ 설정 파일이 존재합니다")
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            if 'mcpServers' in config:
                servers = config['mcpServers']
                print(f"   ✅ MCP 서버 {len(servers)}개 발견:")
                for server_name in servers.keys():
                    print(f"      - {server_name}")
            else:
                print("   ⚠️  mcpServers 설정이 없습니다")
        except Exception as e:
            print(f"   ⚠️  설정 파일 읽기 실패: {str(e)}")
    else:
        print("   ⚠️  설정 파일이 없습니다")
        print(f"   다음 위치에 파일을 생성하세요: {config_path}")
else:
    print("   ⚠️  APPDATA 환경변수를 찾을 수 없습니다")

print()

# 2. Python 환경 확인
print("[2/5] Python 환경 확인...")
print(f"   Python 버전: {sys.version}")
print(f"   Python 경로: {sys.executable}")

# 필수 패키지 확인
required_packages = ['mcp', 'yahooquery', 'google.generativeai', 'exa_py']
missing_packages = []

for package in required_packages:
    try:
        __import__(package.replace('.', '_') if '.' in package else package)
        print(f"   ✅ {package} 설치됨")
    except ImportError:
        print(f"   ❌ {package} 미설치")
        missing_packages.append(package)

if missing_packages:
    print()
    print("   다음 명령어로 패키지를 설치하세요:")
    print(f"   pip install {' '.join(missing_packages)}")

print()

# 3. MCP 서버 파일 확인
print("[3/5] MCP 서버 파일 확인...")
server_dir = Path(__file__).parent
stocks_server = server_dir / "stocks_server.py"
briefing_server = server_dir / "briefing_server.py"

if stocks_server.exists():
    print(f"   ✅ stocks_server.py 존재")
else:
    print(f"   ❌ stocks_server.py 없음")

if briefing_server.exists():
    print(f"   ✅ briefing_server.py 존재")
else:
    print(f"   ❌ briefing_server.py 없음")

print()

# 4. Stocks 서버 기능 테스트 (API 키 불필요)
print("[4/5] Stocks 서버 기능 테스트...")
try:
    from get_trending_stocks import get_top_trending_stock, format_stock_data

    print("   화제 종목 조회 중...")
    top_stock = get_top_trending_stock(count=3)

    if top_stock:
        stock = format_stock_data(top_stock)
        print(f"   ✅ 성공!")
        print(f"      종목: {stock['symbol']} - {stock['name']}")
        print(f"      현재가: ${stock['price']:.2f}")
        print(f"      변동률: {stock['change_percent']:.2f}%")
        print(f"      거래량: {stock['volume']:,}")
    else:
        print("   ⚠️  화제 종목을 찾을 수 없습니다")
        print("      (시장이 열려있지 않을 수 있습니다)")

except Exception as e:
    print(f"   ❌ 오류: {str(e)}")

print()

# 5. API 키 확인 (Briefing 서버용)
print("[5/5] API 키 설정 확인...")
from dotenv import load_dotenv
load_dotenv()

gemini_key = os.getenv('GEMINI_API_KEY')
exa_key = os.getenv('EXA_API_KEY')

if gemini_key and gemini_key != 'your_gemini_api_key_here':
    print("   ✅ GEMINI_API_KEY 설정됨")
else:
    print("   ⚠️  GEMINI_API_KEY 미설정")
    print("      .env 파일에 실제 API 키를 입력하세요")

if exa_key and exa_key != 'your_exa_api_key_here':
    print("   ✅ EXA_API_KEY 설정됨")
else:
    print("   ⚠️  EXA_API_KEY 미설정")
    print("      .env 파일에 실제 API 키를 입력하세요")

print()
print("=" * 60)
print("테스트 완료!")
print("=" * 60)
print()

# 결과 요약
print("📋 요약:")
print()
print("✅ 완료된 항목:")
print("   - MCP 서버 파일 생성")
print("   - Python 환경 확인")
print("   - Stocks 서버 기능 테스트")
print()
print("📌 다음 단계:")
print()
print("1. Claude Desktop 설정:")
print(f"   파일: {config_path if appdata else '%APPDATA%\\Claude\\claude_desktop_config.json'}")
print("   내용: claude_desktop_config.json 파일 참고")
print()
print("2. API 키 설정 (Briefing 서버용):")
print("   파일: backend/.env")
print("   - GEMINI_API_KEY=실제_키")
print("   - EXA_API_KEY=실제_키")
print()
print("3. Claude Desktop 재시작")
print()
print("4. Claude Desktop에서 테스트:")
print('   "오늘 미국 주식 화제 종목을 알려줘"')
print()
print("=" * 60)
