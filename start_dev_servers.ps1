# 당신이 잠든 사이 - 개발 서버 시작 스크립트 (PowerShell)

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "당신이 잠든 사이 - 개발 서버 시작" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# 프로젝트 루트로 이동
Set-Location $PSScriptRoot

# 프론트엔드 서버 시작
Write-Host "[1/3] 프론트엔드 서버 시작 중..." -ForegroundColor Yellow
Write-Host "주소: http://localhost:3000" -ForegroundColor Green
Write-Host ""

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; npm run dev" -WindowStyle Normal

Start-Sleep -Seconds 3

# 백엔드 서버 시작
Write-Host "[2/3] 백엔드 서버 시작 중..." -ForegroundColor Yellow
Write-Host "주소: http://localhost:8000" -ForegroundColor Green
Write-Host "API 문서: http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""

$backendPath = Join-Path $PSScriptRoot "backend"
if (-not (Test-Path (Join-Path $backendPath ".env"))) {
    Write-Host "⚠️  경고: backend\.env 파일이 없습니다!" -ForegroundColor Red
    Write-Host "   API 키를 설정해주세요." -ForegroundColor Red
    Write-Host ""
}

Set-Location $backendPath
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; python main.py" -WindowStyle Normal
Set-Location $PSScriptRoot

Write-Host "[3/3] 서버 시작 완료!" -ForegroundColor Green
Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "서버 정보" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "프론트엔드: http://localhost:3000" -ForegroundColor White
Write-Host "백엔드:     http://localhost:8000" -ForegroundColor White
Write-Host "API 문서:   http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "서버를 중지하려면 각 창에서 Ctrl+C를 누르세요." -ForegroundColor Yellow
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

Start-Sleep -Seconds 5

$response = Read-Host "브라우저를 자동으로 열까요? (Y/N)"
if ($response -eq "Y" -or $response -eq "y") {
    Write-Host ""
    Write-Host "브라우저를 엽니다..." -ForegroundColor Green
    Start-Process "http://localhost:3000"
}

Write-Host ""
Write-Host "서버가 실행 중입니다. 이 창을 닫지 마세요." -ForegroundColor Yellow
Write-Host ""




