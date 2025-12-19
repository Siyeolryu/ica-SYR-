#!/usr/bin/env python3
"""
MCP 서버 연결 테스트 (간단 버전)
"""
import sys
import os
import json
from pathlib import Path

# 상위 디렉토리를 path에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("=" * 60)
print("MCP Connection Test")
print("=" * 60)
print()

# 1. Claude Desktop 설정 파일 확인
print("[1/5] Claude Desktop config check...")
appdata = os.getenv('APPDATA')
config_exists = False
mcp_configured = False

if appdata:
    config_path = Path(appdata) / "Claude" / "claude_desktop_config.json"
    print(f"Config path: {config_path}")

    if config_path.exists():
        print("   [OK] Config file exists")
        config_exists = True
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            if 'mcpServers' in config:
                servers = config['mcpServers']
                print(f"   [OK] Found {len(servers)} MCP servers:")
                for server_name in servers.keys():
                    print(f"      - {server_name}")
                mcp_configured = True
            else:
                print("   [WARNING] No mcpServers in config")
        except Exception as e:
            print(f"   [ERROR] Cannot read config: {str(e)}")
    else:
        print("   [WARNING] Config file does not exist")
        print(f"   Create file at: {config_path}")
else:
    print("   [ERROR] APPDATA not found")

print()

# 2. Python 환경 확인
print("[2/5] Python environment check...")
print(f"Python version: {sys.version.split()[0]}")
print(f"Python path: {sys.executable}")

required_packages = {
    'mcp': 'mcp',
    'yahooquery': 'yahooquery',
    'google.generativeai': 'google-generativeai',
    'exa_py': 'exa-py'
}

all_installed = True
for package, pip_name in required_packages.items():
    try:
        __import__(package)
        print(f"   [OK] {pip_name}")
    except ImportError:
        print(f"   [MISSING] {pip_name}")
        all_installed = False

print()

# 3. MCP 서버 파일 확인
print("[3/5] MCP server files check...")
server_dir = Path(__file__).parent
stocks_server = server_dir / "stocks_server.py"
briefing_server = server_dir / "briefing_server.py"

stocks_exists = stocks_server.exists()
briefing_exists = briefing_server.exists()

print(f"   stocks_server.py: {'[OK]' if stocks_exists else '[MISSING]'}")
print(f"   briefing_server.py: {'[OK]' if briefing_exists else '[MISSING]'}")

print()

# 4. Stocks 서버 기능 테스트
print("[4/5] Stocks server functionality test...")
stocks_working = False
try:
    from get_trending_stocks import get_top_trending_stock, format_stock_data

    print("   Fetching trending stocks...")
    top_stock = get_top_trending_stock(count=3)

    if top_stock:
        stock = format_stock_data(top_stock)
        print(f"   [OK] Success!")
        print(f"      Symbol: {stock['symbol']}")
        print(f"      Name: {stock['name']}")
        print(f"      Price: ${stock['price']:.2f}")
        print(f"      Change: {stock['change_percent']:.2f}%")
        print(f"      Volume: {stock['volume']:,}")
        stocks_working = True
    else:
        print("   [WARNING] No trending stocks found")
        print("      (Market may be closed)")

except Exception as e:
    print(f"   [ERROR] {str(e)}")

print()

# 5. API 키 확인
print("[5/5] API keys check...")
from dotenv import load_dotenv
load_dotenv()

gemini_key = os.getenv('GEMINI_API_KEY')
exa_key = os.getenv('EXA_API_KEY')

gemini_set = gemini_key and gemini_key != 'your_gemini_api_key_here'
exa_set = exa_key and exa_key != 'your_exa_api_key_here'

print(f"   GEMINI_API_KEY: {'[OK]' if gemini_set else '[NOT SET]'}")
print(f"   EXA_API_KEY: {'[OK]' if exa_set else '[NOT SET]'}")

print()
print("=" * 60)
print("Test Summary")
print("=" * 60)
print()

# 결과 요약
results = {
    "Claude Desktop config file": config_exists,
    "MCP servers configured": mcp_configured,
    "Python packages installed": all_installed,
    "MCP server files": stocks_exists and briefing_exists,
    "Stocks server working": stocks_working,
    "API keys configured": gemini_set and exa_set
}

for item, status in results.items():
    status_text = "[OK]" if status else "[NEEDS SETUP]"
    print(f"{status_text} {item}")

print()
print("=" * 60)
print("Next Steps")
print("=" * 60)
print()

if not config_exists or not mcp_configured:
    print("1. Configure Claude Desktop:")
    print(f"   File: {config_path if appdata else '%APPDATA%/Claude/claude_desktop_config.json'}")
    print("   Copy contents from: claude_desktop_config.json")
    print()

if not (gemini_set and exa_set):
    print("2. Set API keys:")
    print("   File: backend/.env")
    print("   - GEMINI_API_KEY=your_actual_key")
    print("   - EXA_API_KEY=your_actual_key")
    print()

if config_exists and mcp_configured:
    print("3. Restart Claude Desktop")
    print()
    print("4. Test in Claude Desktop:")
    print('   Say: "Get me today\'s trending US stocks"')
    print()

print("=" * 60)

# Exit code
if stocks_working and config_exists:
    print("\nSTATUS: MCP servers are ready!")
    sys.exit(0)
else:
    print("\nSTATUS: Setup incomplete - see above steps")
    sys.exit(1)
