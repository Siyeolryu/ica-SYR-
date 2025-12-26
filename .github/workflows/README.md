# GitHub Actions Workflows

## Scheduled Briefing Generation

매주 월/수/금 19:00 (한국 시간)에 브리핑을 자동으로 생성하는 워크플로우입니다.

### 실행 스케줄

- **요일**: 월요일, 수요일, 금요일
- **시간**: 19:00 (한국 시간, KST)
- **기간**: 4주간 (총 12회 실행)

### 설정 방법

1. **GitHub Secrets 설정**:
   - `GEMINI_API_KEY`: Google Gemini API 키
   - `EXA_API_KEY`: Exa API 키
   - `SLACK_WEBHOOK_URL`: Slack Webhook URL (선택사항)

2. **워크플로우 활성화**:
   - GitHub 저장소 → Settings → Actions → General
   - "Allow all actions and reusable workflows" 선택

3. **첫 실행 테스트**:
   - Actions 탭 → "Scheduled Briefing Generation" → "Run workflow"

### 실행 시간 변경

`.github/workflows/scheduled-briefing.yml` 파일에서 cron 표현식을 수정:

```yaml
# 20:00에 실행하려면
- cron: '0 11 * * 1,3,5'  # 20:00 KST = 11:00 UTC

# 21:00에 실행하려면
- cron: '0 12 * * 1,3,5'  # 21:00 KST = 12:00 UTC

# 22:00에 실행하려면
- cron: '0 13 * * 1,3,5'  # 22:00 KST = 13:00 UTC
```

### 4주 후 자동 중지

워크플로우 파일에서 다음 줄의 주석을 해제하면 12회 실행 후 자동으로 중지됩니다:

```yaml
if: ${{ github.event.schedule != '' && github.run_number <= 12 }}
```

---

자세한 내용은 `GitHub_Actions_스케줄_설정_가이드.md`를 참고하세요.


