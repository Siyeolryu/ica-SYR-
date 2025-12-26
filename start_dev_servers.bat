@echo off
chcp 65001 >nul
echo ====================================
echo 당신이 잠든 사이 - 개발 서버 시작
echo ====================================
echo.

cd /d "%~dp0"

echo [1/3] 프론트엔드 서버 시작 중...
echo 주소: http://localhost:3000
echo.

start "Next.js Dev Server" cmd /k "npm run dev"

timeout /t 3 /nobreak >nul

echo [2/3] 백엔드 서버 시작 중...
echo 주소: http://localhost:8000
echo API 문서: http://localhost:8000/docs
echo.

cd backend
if not exist .env (
    echo ⚠️  경고: backend\.env 파일이 없습니다!
    echo    API 키를 설정해주세요.
    echo.
)

start "FastAPI Server" cmd /k "python main.py"

cd ..

echo [3/3] 서버 시작 완료!
echo.
echo ====================================
echo 서버 정보
echo ====================================
echo 프론트엔드: http://localhost:3000
echo 백엔드:     http://localhost:8000
echo API 문서:   http://localhost:8000/docs
echo.
echo 서버를 중지하려면 각 창에서 Ctrl+C를 누르세요.
echo ====================================
echo.

timeout /t 5 /nobreak >nul

echo 브라우저를 자동으로 열까요? (Y/N)
set /p openBrowser="> "

if /i "%openBrowser%"=="Y" (
    echo.
    echo 브라우저를 엽니다...
    start http://localhost:3000
)

echo.
echo 서버가 실행 중입니다. 이 창을 닫지 마세요.
pause




