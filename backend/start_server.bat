@echo off
echo ====================================
echo FastAPI 서버 시작
echo ====================================
echo.

cd /d "%~dp0"

echo [1/2] 환경 변수 확인...
if not exist .env (
    echo 경고: .env 파일이 없습니다!
    echo backend\.env 파일을 생성하고 API 키를 설정해주세요.
    echo.
)

echo [2/2] FastAPI 서버 실행...
echo 서버 주소: http://localhost:8000
echo API 문서: http://localhost:8000/docs
echo.

python main.py

pause
