@echo off
echo ========================================
echo Claude Desktop MCP 설정 도우미
echo ========================================
echo.

echo [1] Claude Desktop 설정 파일 위치:
echo %APPDATA%\Claude\claude_desktop_config.json
echo.

echo [2] 설정 파일이 없으면 생성해주세요.
echo.

echo [3] 준비된 설정을 클립보드에 복사하시겠습니까?
echo    (예: 설정 내용이 클립보드에 복사됩니다)
echo.
pause

echo.
echo ========================================
echo 설정 내용을 claude_desktop_config.json 형식으로 출력합니다
echo ========================================
echo.

type "%~dp0claude_desktop_config.json"

echo.
echo.
echo ========================================
echo 다음 단계:
echo ========================================
echo 1. 위 내용을 복사하세요
echo 2. %APPDATA%\Claude\claude_desktop_config.json 파일을 여세요
echo 3. 파일 내용을 위 내용으로 교체하세요
echo 4. Claude Desktop을 재시작하세요
echo 5. test_mcp_connection.py를 실행하세요
echo.
pause
