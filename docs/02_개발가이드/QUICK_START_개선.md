# 빠른 시작 가이드 (개선판)

## 1. 사전 준비

### 필수 설치 항목
- **Node.js** 18.x 이상
- **Python** 3.9 이상
- **Git**

### API 키 발급
1. **Google Gemini API 키**
   - https://makersuite.google.com/app/apikey
   - 무료 티어 사용 가능

2. **Exa API 키**
   - https://exa.ai
   - 회원가입 후 API 키 발급

3. **Slack Webhook** (선택사항)
   - Slack 워크스페이스 생성
   - Incoming Webhook 앱 설치
   - Webhook URL 복사

## 2. 프로젝트 설정

### 2.1 저장소 클론
```bash
git clone <repository-url>
cd ica-project
```

### 2.2 백엔드 설정
```bash
cd backend

# 환경 변수 파일 생성
copy .env.example .env  # Windows
# cp .env.example .env  # Mac/Linux

# .env 파일을 열어서 API 키 입력
# GEMINI_API_KEY=실제_발급받은_키
# EXA_API_KEY=실제_발급받은_키
# SLACK_WEBHOOK_URL=실제_웹훅_URL

# Python 가상환경 생성 (권장)
python -m venv venv

# 가상환경 활성화
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# 의존성 설치
pip install -r requirements.txt
```

### 2.3 프론트엔드 설정
```bash
# 프로젝트 루트로 이동
cd ..

# 의존성 설치
npm install
```

## 3. 실행

### 3.1 백엔드 테스트 실행
```bash
cd backend

# 개별 모듈 테스트
python test_stocks.py      # 화제 종목 수집 테스트
python test_exa.py          # 뉴스 수집 테스트
python test_gemini.py       # Gemini API 테스트

# 전체 워크플로우 즉시 실행 (테스트)
python scheduler.py --run-once
```

### 3.2 스케줄러 실행 (자동화)
```bash
cd backend

# 매일 아침 7시에 자동 실행
python scheduler.py

# 다른 시간으로 설정 (예: 오전 9시)
python scheduler.py --hour 9
```

### 3.3 프론트엔드 실행
```bash
# 개발 서버 실행
npm run dev

# 브라우저에서 http://localhost:3000 열기
```

## 4. 확인 사항

### 백엔드 정상 작동 확인
- [ ] `test_stocks.py` 실행 시 화제 종목 5개 출력
- [ ] `test_exa.py` 실행 시 뉴스 기사 출력
- [ ] `test_gemini.py` 실행 시 브리핑 텍스트 생성
- [ ] `scheduler.py --run-once` 실행 시 브리핑 이미지 생성

### 프론트엔드 정상 작동 확인
- [ ] 대시보드 페이지 로드
- [ ] 화제 종목 카드 표시
- [ ] 다크/라이트 모드 전환
- [ ] 브리핑 카드 표시

## 5. 문제 해결

### API 키 오류
```
ValueError: Gemini API 키가 필요합니다.
```
**해결**: `backend/.env` 파일에 API 키가 올바르게 입력되었는지 확인

### 모듈 없음 오류
```
ModuleNotFoundError: No module named 'yahooquery'
```
**해결**: `pip install -r requirements.txt` 재실행

### 포트 충돌
```
Error: Port 3000 is already in use
```
**해결**: 
```bash
npm run dev -- -p 3001  # 다른 포트 사용
```

### Yahoo Finance API 오류
```
화제 종목을 찾을 수 없습니다.
```
**해결**: 
- 인터넷 연결 확인
- 미국 증시 개장 시간 확인 (한국 시간 23:30 ~ 06:00)
- 잠시 후 다시 시도

## 6. 다음 단계

### 개발 환경
- [ ] 코드 에디터 설정 (VS Code 권장)
- [ ] Python 린터 설정 (pylint, black)
- [ ] TypeScript 린터 설정 (ESLint)

### 배포 준비
- [ ] 프로덕션 환경 변수 설정
- [ ] Docker 컨테이너화
- [ ] CI/CD 파이프라인 구축

### 기능 확장
- [ ] 데이터베이스 연동 (브리핑 히스토리 저장)
- [ ] 사용자 인증 시스템
- [ ] 이메일 발송 기능
- [ ] 모바일 앱 개발

## 7. 유용한 명령어

### 백엔드
```bash
# 가상환경 비활성화
deactivate

# 패키지 업데이트
pip install --upgrade -r requirements.txt

# 로그 확인
tail -f backend/output/*.log  # Mac/Linux
```

### 프론트엔드
```bash
# 프로덕션 빌드
npm run build

# 프로덕션 서버 실행
npm start

# 린트 검사
npm run lint

# 타입 체크
npx tsc --noEmit
```

## 8. 참고 자료

- [Next.js 문서](https://nextjs.org/docs)
- [Google Gemini API 문서](https://ai.google.dev/docs)
- [Yahoo Finance API (yahooquery)](https://yahooquery.dpguthrie.com/)
- [Exa API 문서](https://docs.exa.ai/)
- [TailwindCSS 문서](https://tailwindcss.com/docs)

---

문제가 발생하면 `프로젝트_점검_보고서.md`를 참고하거나 이슈를 등록해주세요.


