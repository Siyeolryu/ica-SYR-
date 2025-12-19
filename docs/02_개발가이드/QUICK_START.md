# 🚀 빠른 시작 가이드

## Node.js 설치 확인 후 실행하기

### ⚡ 빠른 실행 (3단계)

#### 1️⃣ 터미널 재시작
**중요:** Node.js 설치 후 반드시 PowerShell을 완전히 닫고 새로 열어주세요!

#### 2️⃣ 의존성 설치
```powershell
cd C:\Users\tlduf\Downloads\ica-project
npm install
```

#### 3️⃣ 개발 서버 실행
```powershell
npm run dev
```

브라우저에서 **http://localhost:3000** 열기

---

## 📝 상세 단계

### Step 1: 터미널 재시작 및 확인

1. **현재 PowerShell 창 완전히 닫기**
2. **새 PowerShell 창 열기**
3. **프로젝트 폴더로 이동:**
   ```powershell
   cd C:\Users\tlduf\Downloads\ica-project
   ```
4. **Node.js 확인:**
   ```powershell
   node --version
   ```
   ✅ 성공하면: `v20.x.x` 같은 버전 번호가 나옵니다
   ❌ 실패하면: 터미널을 다시 재시작하거나 Node.js 재설치

### Step 2: 라이브러리 설치

```powershell
npm install
```

**예상 시간:** 1-3분
**성공 표시:** `added XXX packages` 메시지

### Step 3: 개발 서버 실행

```powershell
npm run dev
```

**성공 표시:**
```
  ▲ Next.js 14.0.4
  - Local:        http://localhost:3000
  - Ready in 2.3s
```

### Step 4: 브라우저에서 확인

브라우저 주소창에 입력:
```
http://localhost:3000
```

---

## 🎯 확인할 수 있는 화면

### 메인 대시보드
- 📊 오늘의 화제 종목 (큰 카드)
- 📈 주가 차트 (라인 + 바 차트)
- 📋 최근 브리핑 목록
- ➕ 브리핑 생성 버튼

### 브리핑 상세 페이지
- 🖼️ 브리핑 이미지
- 📝 리포트 텍스트
- 📧 이메일/슬랙 발송 버튼

---

## 🛑 서버 중지하기

터미널에서:
```
Ctrl + C
```

---

## ❓ 문제 해결

### "node를 찾을 수 없습니다"
→ 터미널 재시작 또는 Node.js 재설치

### "포트 3000이 사용 중입니다"
→ `npm run dev -- -p 3001` (다른 포트 사용)

### 설치가 너무 느립니다
→ 인터넷 연결 확인 또는 npm 캐시 삭제

---

**준비되셨으면 터미널을 재시작하고 위 단계를 따라주세요!** 🎉










