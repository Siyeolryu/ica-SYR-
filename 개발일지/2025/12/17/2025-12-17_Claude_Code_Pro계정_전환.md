# Claude Code Pro 계정 전환 개발일지

## 작성시각
2025년 12월 17일 오후 8:51

---

## 해결하고자 한 문제

Claude Code가 API 키를 사용하여 사용량만큼 과금되고 있었습니다. 사용자는 Claude Pro 정액 계정을 보유하고 있어서, 이를 활용하여 무제한으로 Claude Code를 사용하고자 했습니다.

### 초기 상황
- ❌ API 키로 인증 (`ANTHROPIC_API_KEY` 환경 변수)
- ❌ "Credit balance too low" 오류 발생
- ❌ 사용량당 과금

---

## 해결된 것

### 1. 문제 원인 파악 ✅
- `C:\Users\tlduf\.claude\settings.json`에 `apiKeyHelper` 설정이 있었음
- 환경 변수 `ANTHROPIC_API_KEY`가 설정되어 있었음
- Claude Code가 API 키 인증을 우선적으로 사용하고 있었음

### 2. 설정 파일 수정 ✅
**파일**: `C:\Users\tlduf\.claude\settings.json`

**변경 전**:
```json
{
  "apiKeyHelper": "powershell -NoProfile -Command \"Write-Output $env:ANTHROPIC_API_KEY\""
}
```

**변경 후**:
```json
{}
```

### 3. 환경 변수 제거 ✅
```powershell
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", $null, "User")
```

### 4. Claude Pro 계정 인증 확인 ✅
**파일**: `C:\Users\tlduf\.claude\.credentials.json`

```json
{
  "claudeAiOauth": {
    "subscriptionType": "pro",
    "rateLimitTier": "default_claude_ai",
    "expiresAt": 1766000762091  // 2025-12-18까지 유효
  }
}
```

**인증 상태**:
- ✅ OAuth 토큰 인증 완료
- ✅ 구독 타입: **Claude Pro**
- ✅ 토큰 만료일: 2025년 12월 18일
- ✅ 스코프: `user:inference`, `user:profile`, `user:sessions:claude_code`

### 5. 사용 통계 확인 ✅
**파일**: `C:\Users\tlduf\.claude\stats-cache.json`

```json
{
  "modelUsage": {
    "claude-sonnet-4-5-20250929": {
      "inputTokens": 5636,
      "outputTokens": 73204,
      "cacheReadInputTokens": 11074836,
      "cacheCreationInputTokens": 2146643,
      "costUSD": 0  // ✅ 비용 0달러!
    }
  }
}
```

**이미 사용한 내역도 비용이 0달러로 표시**됩니다! 🎉

---

## 해결되지 않은 것

### 1. `--print` 모드 오류 ❓
```bash
claude --print "테스트"
# 결과: Credit balance is too low
```

**가능한 원인**:
- `--print` 모드는 API 전용 기능일 수 있음
- 대화형 모드에서는 정상 작동할 가능성 있음

### 2. 대화형 모드 테스트 필요 🔜
PowerShell에서 대화형 명령어(`claude`, `claude setup-token`, `claude doctor`)가 "Raw mode not supported" 오류로 실행되지 않음.

**해결 방법**:
- ✅ **CMD** 또는 **Windows Terminal**에서 실행 필요
- ✅ 새 터미널 창에서 직접 실행

---

## 향후 개발을 위한 컨텍스트

### Claude Code 인증 구조

#### 1. 인증 우선순위
```
1순위: 환경 변수 (ANTHROPIC_API_KEY)
2순위: settings.json의 apiKeyHelper
3순위: .credentials.json의 OAuth 토큰
```

#### 2. 주요 설정 파일
| 파일 | 경로 | 용도 |
|------|------|------|
| `settings.json` | `C:\Users\tlduf\.claude\` | API 키 헬퍼 설정 |
| `.credentials.json` | `C:\Users\tlduf\.claude\` | OAuth 인증 토큰 |
| `stats-cache.json` | `C:\Users\tlduf\.claude\` | 사용 통계 |

#### 3. Claude Pro vs API 키

| 항목 | Claude Pro | API 키 |
|------|-----------|--------|
| **비용** | 월 $20 정액 | 사용량당 과금 |
| **인증 방식** | OAuth 토큰 | API 키 |
| **사용 제한** | 공정 사용 정책 | 크레딧 소진 시 중단 |
| **설정 파일** | `.credentials.json` | 환경 변수 |

### 테스트 방법

#### ✅ 작동하는 명령어
```bash
claude --version
```

#### ❌ PowerShell에서 작동하지 않는 명령어
```bash
claude              # Raw mode 오류
claude setup-token  # Raw mode 오류
claude doctor       # Raw mode 오류
claude --print      # Credit balance 오류
```

#### 🔜 테스트 필요
**CMD 또는 Windows Terminal에서 실행**:
```bash
# 대화형 모드 시작
claude

# 세션 내에서
/whoami  # 계정 정보 확인
```

### 주의사항

1. **환경 변수 우선순위**: 환경 변수가 설정되어 있으면 OAuth 토큰보다 우선 적용됨
2. **PowerShell 프로필**: 자동으로 별칭이 로드되지만 대화형 모드는 Raw mode 오류 발생
3. **토큰 만료**: OAuth 토큰은 주기적으로 갱신 필요 (현재는 12/18까지 유효)

### 다음 단계

1. ✅ **즉시 가능**: `claude --version`으로 설치 확인
2. 🔜 **CMD에서 테스트**: 대화형 모드로 실제 AI 기능 테스트
3. 🔜 **MCP 서버 연동**: Claude Code에서 프로젝트의 MCP 서버 사용 테스트

---

## 결과 요약

### ✅ 성공
- API 키 설정 완전 제거
- Claude Pro 계정 OAuth 인증 확인
- 사용 비용 0달러 확인
- 토큰 유효성 확인 (12/18까지)

### 🔜 추가 필요
- CMD에서 대화형 모드 테스트
- 실제 AI 응답 동작 확인
- MCP 서버 연동 테스트

---

**작성자**: AI Assistant  
**Claude Code 버전**: 2.0.71  
**인증 타입**: Claude Pro OAuth  
**프로젝트**: "당신이 잠든 사이" - 주식 브리핑 서비스

