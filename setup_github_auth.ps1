# GitHub 인증 설정 스크립트
# Personal Access Token을 사용하여 GitHub 인증 설정

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "GitHub 인증 설정 도우미" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 현재 Git 설정 확인
Write-Host "[1/4] 현재 Git 설정 확인 중..." -ForegroundColor Yellow
$currentUser = git config --global user.name
$currentEmail = git config --global user.email
$remoteUrl = (git remote get-url origin 2>$null)

Write-Host "사용자 이름: $currentUser" -ForegroundColor White
Write-Host "이메일: $currentEmail" -ForegroundColor White
Write-Host "원격 저장소: $remoteUrl" -ForegroundColor White
Write-Host ""

# Personal Access Token 안내
Write-Host "[2/4] Personal Access Token 생성 안내" -ForegroundColor Yellow
Write-Host ""
Write-Host "다음 단계를 따라 Personal Access Token을 생성하세요:" -ForegroundColor White
Write-Host ""
Write-Host "1. 브라우저에서 다음 주소 열기:" -ForegroundColor Green
Write-Host "   https://github.com/settings/tokens/new" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. 토큰 설정:" -ForegroundColor White
Write-Host "   - Note: ica-project-access" -ForegroundColor Gray
Write-Host "   - Expiration: 90 days (또는 원하는 기간)" -ForegroundColor Gray
Write-Host "   - Scopes: repo, workflow 체크" -ForegroundColor Gray
Write-Host ""
Write-Host "3. 'Generate token' 클릭 후 토큰 복사" -ForegroundColor White
Write-Host "   (토큰은 한 번만 표시되므로 반드시 복사하세요!)" -ForegroundColor Red
Write-Host ""

# 토큰 입력 받기
$token = Read-Host "생성한 Personal Access Token을 입력하세요"

if ([string]::IsNullOrWhiteSpace($token)) {
    Write-Host "토큰이 입력되지 않았습니다. 스크립트를 종료합니다." -ForegroundColor Red
    exit 1
}

# 원격 저장소 URL 업데이트
Write-Host ""
Write-Host "[3/4] 원격 저장소 URL 업데이트 중..." -ForegroundColor Yellow

# 현재 원격 URL에서 사용자명과 저장소명 추출
if ($remoteUrl -match "github\.com/([^/]+)/([^/]+)\.git") {
    $username = $matches[1]
    $repoName = $matches[2]
    
    # 토큰을 포함한 새 URL 생성
    $newUrl = "https://$token@github.com/$username/$repoName.git"
    
    Write-Host "새 URL 설정: https://$username@github.com/$username/$repoName.git" -ForegroundColor Green
    git remote set-url origin $newUrl
    
    Write-Host "원격 저장소 URL이 업데이트되었습니다!" -ForegroundColor Green
} else {
    Write-Host "원격 저장소 URL을 파싱할 수 없습니다." -ForegroundColor Red
    Write-Host "수동으로 설정하세요:" -ForegroundColor Yellow
    Write-Host "  git remote set-url origin https://YOUR_TOKEN@github.com/USERNAME/REPO.git" -ForegroundColor Cyan
}

# 테스트
Write-Host ""
Write-Host "[4/4] 연결 테스트 중..." -ForegroundColor Yellow
Write-Host ""

$testResult = git ls-remote origin 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "인증 성공!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "이제 다음 명령어로 푸시할 수 있습니다:" -ForegroundColor White
    Write-Host "  git push origin main" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "인증 실패" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "오류 메시지:" -ForegroundColor Yellow
    Write-Host $testResult -ForegroundColor Red
    Write-Host ""
    Write-Host "다음을 확인하세요:" -ForegroundColor Yellow
    Write-Host "1. 토큰이 올바르게 입력되었는지" -ForegroundColor White
    Write-Host "2. 토큰에 'repo' 권한이 있는지" -ForegroundColor White
    Write-Host "3. 토큰이 만료되지 않았는지" -ForegroundColor White
    Write-Host ""
}

Write-Host "스크립트 완료!" -ForegroundColor Cyan


