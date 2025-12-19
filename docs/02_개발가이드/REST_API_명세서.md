# 🌙 "당신이 잠든 사이" REST API 명세서

> 미국 증시 화제 종목 브리핑 서비스 API 문서

<br>

## 📑 목차

1. [기본 정보](#기본-정보)
2. [인증](#인증)
3. [Rate Limiting](#rate-limiting)
4. [API 엔드포인트](#api-엔드포인트)
   - [화제 종목 조회](#1-화제-종목-조회-api)
   - [종목 상세 정보](#2-종목-상세-정보-api)
   - [브리핑 생성](#3-브리핑-생성-api)
   - [브리핑 발송](#4-발송-api-이메일슬랙)
   - [브리핑 히스토리](#5-브리핑-히스토리-조회-api)
5. [에러 처리](#공통-에러-응답-형식)

<br>

---

<br>

## 🔧 기본 정보

| 항목 | 내용 |
|------|------|
| **Base URL** | `https://api.whileyouweresleeping.com/v1` |
| **인증 방식** | Bearer Token (JWT) |
| **Content-Type** | `application/json` |
| **날짜 형식** | ISO 8601 (예: `2024-01-15T06:00:00Z`) |
| **API 버전** | v1 |
| **프로토콜** | HTTPS Only |

<br>

---

<br>

## 📊 API 엔드포인트

<br>

### 1. 화제 종목 조회 API

> Yahoo Finance Screener를 활용하여 화제 종목 목록을 조회합니다.

<br>

#### 📋 기본 정보

| 항목 | 내용 |
|------|------|
| **HTTP Method** | `GET` |
| **Endpoint** | `/trending-stocks` |
| **인증 필요** | ❌ 선택적 |
| **Rate Limit** | 분당 60회 |

<br>

#### 🔍 Query Parameters

| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|----------|------|------|--------|------|
| `screener_types` | `string[]` | ❌ | `["most_actives", "day_gainers"]` | 스크리너 타입<br>• `most_actives`: 거래량 상위<br>• `day_gainers`: 상승률 상위<br>• `day_losers`: 하락률 상위 |
| `count` | `integer` | ❌ | `10` | 각 스크리너당 종목 수<br>• 범위: 1-50 |
| `limit` | `integer` | ❌ | `10` | 최종 반환 종목 수<br>• 범위: 1-100 |
| `min_volume` | `integer` | ❌ | - | 최소 거래량 필터 |
| `min_change_percent` | `float` | ❌ | - | 최소 변동률 필터 (%) |
| `sort_by` | `string` | ❌ | `score` | 정렬 기준<br>• `score`: 종합 점수<br>• `volume`: 거래량<br>• `change_percent`: 변동률 |
| `order` | `string` | ❌ | `desc` | 정렬 순서<br>• `asc`: 오름차순<br>• `desc`: 내림차순 |

<br>

#### 📤 Request Example

```http
GET /v1/trending-stocks?screener_types=most_actives,day_gainers&count=10&limit=5
Authorization: Bearer {your_jwt_token}
```

**curl 예제:**

```bash
curl -X GET "https://api.whileyouweresleeping.com/v1/trending-stocks?screener_types=most_actives,day_gainers&count=10&limit=5" \
  -H "Authorization: Bearer {your_jwt_token}"
```

<br>

#### ✅ Response Example (200 OK)

```json
{
  "success": true,
  "data": {
    "stocks": [
      {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "price": 185.50,
        "change_percent": 2.35,
        "volume": 45234567,
        "market_cap": 2850000000000,
        "score": 0.875,
        "screener_types": ["most_actives", "day_gainers"],
        "timestamp": "2024-01-15T06:00:00Z"
      },
      {
        "symbol": "TSLA",
        "name": "Tesla, Inc.",
        "price": 245.30,
        "change_percent": 5.12,
        "volume": 38923456,
        "market_cap": 780000000000,
        "score": 0.823,
        "screener_types": ["day_gainers"],
        "timestamp": "2024-01-15T06:00:00Z"
      }
    ],
    "total": 2,
    "generated_at": "2024-01-15T06:00:00Z"
  }
}
```

**Response 필드 설명:**

| 필드 | 타입 | 설명 |
|------|------|------|
| `success` | `boolean` | 요청 성공 여부 |
| `data.stocks` | `array` | 화제 종목 목록 |
| `data.stocks[].symbol` | `string` | 종목 심볼 (티커) |
| `data.stocks[].name` | `string` | 회사명 |
| `data.stocks[].price` | `number` | 현재 주가 (USD) |
| `data.stocks[].change_percent` | `number` | 전일 대비 변동률 (%) |
| `data.stocks[].volume` | `number` | 거래량 |
| `data.stocks[].market_cap` | `number` | 시가총액 (USD) |
| `data.stocks[].score` | `number` | 화제성 점수 (0-1) |
| `data.stocks[].screener_types` | `string[]` | 해당 종목이 속한 스크리너 타입 |
| `data.stocks[].timestamp` | `string` | 데이터 수집 시간 (ISO 8601) |
| `data.total` | `number` | 반환된 종목 수 |
| `data.generated_at` | `string` | 응답 생성 시간 (ISO 8601) |

<br>

#### ❌ Error Cases

| HTTP Status | Error Code | 설명 |
|-------------|------------|------|
| `400` | `INVALID_PARAMETER` | 잘못된 파라미터 값 |
| `429` | `RATE_LIMIT_EXCEEDED` | API 호출 제한 초과 |
| `500` | `DATA_FETCH_ERROR` | 외부 데이터 수집 실패 |
| `503` | `SERVICE_UNAVAILABLE` | 외부 서비스 일시 장애 |

**에러 응답 예시:**

```json
{
  "success": false,
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "count must be between 1 and 50",
    "details": {
      "parameter": "count",
      "provided": 100,
      "valid_range": "1-50"
    },
    "request_id": "req_abc123",
    "timestamp": "2024-01-15T06:00:00Z"
  }
}
```

<br>

---

<br>

### 2. 종목 상세 정보 API

> 특정 종목의 상세 정보와 관련 뉴스를 조회합니다.

<br>

#### 📋 기본 정보

| 항목 | 내용 |
|------|------|
| **HTTP Method** | `GET` |
| **Endpoint** | `/stocks/{symbol}` |
| **인증 필요** | ❌ 선택적 |
| **Rate Limit** | 분당 100회 |

<br>

#### 🔗 Path Parameters

| 파라미터 | 타입 | 필수 | 설명 |
|----------|------|------|------|
| `symbol` | `string` | ✅ | 종목 심볼 (티커)<br>예: `AAPL`, `TSLA`, `MSFT` |

<br>

#### 🔍 Query Parameters

| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|----------|------|------|--------|------|
| `include_news` | `boolean` | ❌ | `true` | 관련 뉴스 포함 여부 |
| `news_limit` | `integer` | ❌ | `5` | 뉴스 개수<br>• 범위: 1-20 |
| `include_financials` | `boolean` | ❌ | `false` | 재무 정보 포함 여부 |

<br>

#### 📤 Request Example

```http
GET /v1/stocks/AAPL?include_news=true&news_limit=5
Authorization: Bearer {your_jwt_token}
```

**curl 예제:**

```bash
curl -X GET "https://api.whileyouweresleeping.com/v1/stocks/AAPL?include_news=true&news_limit=5" \
  -H "Authorization: Bearer {your_jwt_token}"
```

<br>

#### ✅ Response Example (200 OK)

```json
{
  "success": true,
  "data": {
    "symbol": "AAPL",
    "name": "Apple Inc.",
    "description": "Apple Inc. designs, manufactures, and markets smartphones...",
    "current_price": 185.50,
    "previous_close": 181.25,
    "change": 4.25,
    "change_percent": 2.35,
    "volume": 45234567,
    "average_volume": 52345678,
    "market_cap": 2850000000000,
    "pe_ratio": 28.5,
    "dividend_yield": 0.52,
    "52_week_high": 198.23,
    "52_week_low": 124.17,
    "sector": "Technology",
    "industry": "Consumer Electronics",
    "news": [
      {
        "title": "Apple announces new product line",
        "source": "Reuters",
        "published_at": "2024-01-15T03:30:00Z",
        "url": "https://example.com/news/1",
        "summary": "Apple Inc. announced..."
      }
    ],
    "updated_at": "2024-01-15T06:00:00Z"
  }
}
```

**Response 필드 설명:**

| 필드 | 타입 | 설명 |
|------|------|------|
| `symbol` | `string` | 종목 심볼 |
| `name` | `string` | 회사명 |
| `description` | `string` | 회사 설명 |
| `current_price` | `number` | 현재 주가 (USD) |
| `previous_close` | `number` | 전일 종가 (USD) |
| `change` | `number` | 전일 대비 변동 금액 (USD) |
| `change_percent` | `number` | 전일 대비 변동률 (%) |
| `volume` | `number` | 당일 거래량 |
| `average_volume` | `number` | 평균 거래량 (3개월) |
| `market_cap` | `number` | 시가총액 (USD) |
| `pe_ratio` | `number` | 주가수익비율 (PER) |
| `dividend_yield` | `number` | 배당수익률 (%) |
| `52_week_high` | `number` | 52주 최고가 |
| `52_week_low` | `number` | 52주 최저가 |
| `sector` | `string` | 섹터 |
| `industry` | `string` | 업종 |
| `news` | `array` | 관련 뉴스 목록 |
| `updated_at` | `string` | 업데이트 시간 |

<br>

#### ❌ Error Cases

| HTTP Status | Error Code | 설명 |
|-------------|------------|------|
| `400` | `INVALID_SYMBOL` | 잘못된 종목 심볼 형식 |
| `404` | `STOCK_NOT_FOUND` | 종목을 찾을 수 없음 |
| `500` | `DATA_FETCH_ERROR` | 데이터 수집 실패 |

<br>

---

<br>

### 3. 브리핑 생성 API

> 화제 종목 정보를 기반으로 AI 브리핑(이미지 + 텍스트)을 생성합니다.

<br>

#### 📋 기본 정보

| 항목 | 내용 |
|------|------|
| **HTTP Method** | `POST` |
| **Endpoint** | `/briefings` |
| **인증 필요** | ✅ 필수 |
| **Rate Limit** | 분당 10회 |
| **처리 방식** | 동기 또는 비동기 (생성 시간에 따라) |

<br>

#### 📝 Request Body

| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|--------|------|
| `stock_symbols` | `string[]` | ❌ | - | 특정 종목 지정<br>• 미지정 시 자동 선정 |
| `screener_types` | `string[]` | ❌ | `["most_actives", "day_gainers"]` | 자동 선정 시 사용할 스크리너 |
| `count` | `integer` | ❌ | `5` | 포함할 종목 수<br>• 범위: 1-10 |
| `format` | `string` | ❌ | `both` | 브리핑 형식<br>• `image`: 이미지만<br>• `text`: 텍스트만<br>• `both`: 이미지 + 텍스트 |
| `language` | `string` | ❌ | `ko` | 언어<br>• `ko`: 한국어<br>• `en`: 영어 |
| `template_id` | `string` | ❌ | - | 템플릿 ID<br>• 미지정 시 기본 템플릿 사용 |

<br>

#### 📤 Request Example

```http
POST /v1/briefings
Authorization: Bearer {your_jwt_token}
Content-Type: application/json

{
  "stock_symbols": ["AAPL", "TSLA", "MSFT"],
  "format": "both",
  "language": "ko",
  "count": 5
}
```

**curl 예제:**

```bash
curl -X POST "https://api.whileyouweresleeping.com/v1/briefings" \
  -H "Authorization: Bearer {your_jwt_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "stock_symbols": ["AAPL", "TSLA", "MSFT"],
    "format": "both",
    "language": "ko",
    "count": 5
  }'
```

<br>

#### ✅ Response Example (200 OK - 동기 처리)

```json
{
  "success": true,
  "data": {
    "briefing_id": "brf_20240115_060000_abc123",
    "generated_at": "2024-01-15T06:00:00Z",
    "status": "completed",
    "stocks_included": [
      {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "price": 185.50,
        "change_percent": 2.35,
        "volume": 45234567
      }
    ],
    "content": {
      "text": {
        "title": "오늘의 화제 종목 브리핑",
        "summary": "2024년 1월 15일 미국 증시에서 가장 활발했던 종목들을 정리했습니다...",
        "sections": [
          {
            "stock_symbol": "AAPL",
            "title": "Apple Inc. (AAPL)",
            "content": "애플은 전일 대비 2.35% 상승하며 거래량 4,523만 주를 기록했습니다..."
          }
        ]
      },
      "image": {
        "url": "https://cdn.whileyouweresleeping.com/briefings/brf_20240115_060000_abc123.png",
        "thumbnail_url": "https://cdn.whileyouweresleeping.com/briefings/thumbnails/brf_20240115_060000_abc123.png",
        "width": 1200,
        "height": 1600,
        "format": "png"
      }
    },
    "metadata": {
      "template_used": "default_v1",
      "generation_time_ms": 3450,
      "ai_model": "gemini-pro"
    }
  }
}
```

<br>

#### ⏳ Response Example (202 Accepted - 비동기 처리)

```json
{
  "success": true,
  "data": {
    "briefing_id": "brf_20240115_060000_abc123",
    "status": "processing",
    "estimated_completion_time": "2024-01-15T06:00:30Z",
    "check_status_url": "/v1/briefings/brf_20240115_060000_abc123/status"
  }
}
```

> 💡 비동기 처리 시 `check_status_url`을 통해 생성 상태를 확인할 수 있습니다.

<br>

#### ❌ Error Cases

| HTTP Status | Error Code | 설명 |
|-------------|------------|------|
| `400` | `INVALID_REQUEST` | 잘못된 요청 데이터 |
| `401` | `UNAUTHORIZED` | 인증 실패 또는 토큰 만료 |
| `422` | `INSUFFICIENT_STOCKS` | 충분한 종목 데이터 없음 |
| `429` | `RATE_LIMIT_EXCEEDED` | 브리핑 생성 제한 초과 |
| `500` | `GENERATION_ERROR` | 브리핑 생성 실패 |
| `503` | `SERVICE_UNAVAILABLE` | AI 서비스 일시 장애 |

<br>

---

<br>

### 4. 발송 API (이메일/슬랙)

> 생성된 브리핑을 이메일 또는 Slack으로 발송합니다.

<br>

#### 📋 기본 정보

| 항목 | 내용 |
|------|------|
| **HTTP Method** | `POST` |
| **Endpoint** | `/briefings/{briefing_id}/send` |
| **인증 필요** | ✅ 필수 |
| **Rate Limit** | 분당 30회 |
| **지원 채널** | 이메일, Slack |

<br>

#### 🔗 Path Parameters

| 파라미터 | 타입 | 필수 | 설명 |
|----------|------|------|------|
| `briefing_id` | `string` | ✅ | 발송할 브리핑 ID<br>예: `brf_20240115_060000_abc123` |

<br>

#### 📝 Request Body

| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|--------|------|
| `channels` | `object[]` | ✅ | - | 발송 채널 목록 |
| `channels[].type` | `string` | ✅ | - | 채널 타입<br>• `email`: 이메일<br>• `slack`: Slack |
| `channels[].email` | `string` | 조건부 | - | 이메일 주소<br>• `type=email`일 때 필수 |
| `channels[].slack_webhook_url` | `string` | 조건부 | - | Slack Webhook URL<br>• `type=slack`일 때 필수 |
| `channels[].slack_channel` | `string` | ❌ | `#general` | Slack 채널명 |
| `send_immediately` | `boolean` | ❌ | `true` | 즉시 발송 여부 |
| `scheduled_at` | `string` | 조건부 | - | 예약 발송 시간 (ISO 8601)<br>• `send_immediately=false`일 때 필수 |

<br>

#### 📤 Request Example

```http
POST /v1/briefings/brf_20240115_060000_abc123/send
Authorization: Bearer {your_jwt_token}
Content-Type: application/json

{
  "channels": [
    {
      "type": "email",
      "email": "user@example.com"
    },
    {
      "type": "slack",
      "slack_webhook_url": "https://hooks.slack.com/services/XXX/YYY/ZZZ",
      "slack_channel": "#stock-briefing"
    }
  ],
  "send_immediately": true
}
```

**curl 예제:**

```bash
curl -X POST "https://api.whileyouweresleeping.com/v1/briefings/brf_20240115_060000_abc123/send" \
  -H "Authorization: Bearer {your_jwt_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "channels": [
      {
        "type": "email",
        "email": "user@example.com"
      },
      {
        "type": "slack",
        "slack_webhook_url": "https://hooks.slack.com/services/XXX/YYY/ZZZ",
        "slack_channel": "#stock-briefing"
      }
    ],
    "send_immediately": true
  }'
```

<br>

#### ✅ Response Example (200 OK - 즉시 발송)

```json
{
  "success": true,
  "data": {
    "briefing_id": "brf_20240115_060000_abc123",
    "send_job_id": "job_20240115_060100_def456",
    "status": "sent",
    "channels": [
      {
        "type": "email",
        "email": "user@example.com",
        "status": "sent",
        "sent_at": "2024-01-15T06:01:00Z",
        "message_id": "msg_email_789"
      },
      {
        "type": "slack",
        "slack_channel": "#stock-briefing",
        "status": "sent",
        "sent_at": "2024-01-15T06:01:01Z",
        "message_ts": "1705292461.123456"
      }
    ],
    "total_sent": 2,
    "total_failed": 0
  }
}
```

<br>

#### ⏳ Response Example (202 Accepted - 예약 발송)

```json
{
  "success": true,
  "data": {
    "briefing_id": "brf_20240115_060000_abc123",
    "send_job_id": "job_20240115_060100_def456",
    "status": "scheduled",
    "scheduled_at": "2024-01-15T07:00:00Z",
    "channels": [
      {
        "type": "email",
        "email": "user@example.com",
        "status": "scheduled"
      }
    ]
  }
}
```

<br>

#### ❌ Error Cases

| HTTP Status | Error Code | 설명 |
|-------------|------------|------|
| `400` | `INVALID_REQUEST` | 잘못된 요청 데이터 |
| `401` | `UNAUTHORIZED` | 인증 실패 또는 토큰 만료 |
| `404` | `BRIEFING_NOT_FOUND` | 브리핑을 찾을 수 없음 |
| `422` | `INVALID_EMAIL` | 잘못된 이메일 형식 |
| `422` | `INVALID_SLACK_WEBHOOK` | 잘못된 Slack Webhook URL |
| `429` | `RATE_LIMIT_EXCEEDED` | 발송 제한 초과 |
| `500` | `SEND_ERROR` | 발송 실패 |
| `503` | `EMAIL_SERVICE_UNAVAILABLE` | 이메일 서비스 일시 장애 |
| `503` | `SLACK_SERVICE_UNAVAILABLE` | Slack 서비스 일시 장애 |

<br>

---

<br>

### 5. 브리핑 히스토리 조회 API

> 생성된 브리핑 목록과 상세 정보를 조회합니다.

<br>

#### 📋 기본 정보 (목록 조회)

| 항목 | 내용 |
|------|------|
| **HTTP Method** | `GET` |
| **Endpoint** | `/briefings` |
| **인증 필요** | ✅ 필수 |
| **Rate Limit** | 분당 100회 |

<br>

#### 🔍 Query Parameters

| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|----------|------|------|--------|------|
| `page` | `integer` | ❌ | `1` | 페이지 번호<br>• 1부터 시작 |
| `limit` | `integer` | ❌ | `20` | 페이지당 항목 수<br>• 범위: 1-100 |
| `start_date` | `string` | ❌ | - | 시작 날짜 (ISO 8601) |
| `end_date` | `string` | ❌ | - | 종료 날짜 (ISO 8601) |
| `stock_symbol` | `string` | ❌ | - | 특정 종목 필터<br>예: `AAPL` |
| `status` | `string` | ❌ | - | 브리핑 상태 필터<br>• `completed`: 완료<br>• `processing`: 처리 중<br>• `failed`: 실패 |

<br>

#### 📤 Request Example

```http
GET /v1/briefings?page=1&limit=10&start_date=2024-01-01T00:00:00Z&end_date=2024-01-15T23:59:59Z
Authorization: Bearer {your_jwt_token}
```

**curl 예제:**

```bash
curl -X GET "https://api.whileyouweresleeping.com/v1/briefings?page=1&limit=10&start_date=2024-01-01T00:00:00Z&end_date=2024-01-15T23:59:59Z" \
  -H "Authorization: Bearer {your_jwt_token}"
```

<br>

#### ✅ Response Example (200 OK)

```json
{
  "success": true,
  "data": {
    "briefings": [
      {
        "briefing_id": "brf_20240115_060000_abc123",
        "generated_at": "2024-01-15T06:00:00Z",
        "status": "completed",
        "stocks_count": 5,
        "stocks": [
          {
            "symbol": "AAPL",
            "name": "Apple Inc."
          },
          {
            "symbol": "TSLA",
            "name": "Tesla, Inc."
          }
        ],
        "content": {
          "text_available": true,
          "image_available": true,
          "image_url": "https://cdn.whileyouweresleeping.com/briefings/brf_20240115_060000_abc123.png",
          "thumbnail_url": "https://cdn.whileyouweresleeping.com/briefings/thumbnails/brf_20240115_060000_abc123.png"
        },
        "sent_channels": ["email", "slack"],
        "view_count": 12
      },
      {
        "briefing_id": "brf_20240114_060000_xyz789",
        "generated_at": "2024-01-14T06:00:00Z",
        "status": "completed",
        "stocks_count": 5,
        "stocks": [
          {
            "symbol": "MSFT",
            "name": "Microsoft Corporation"
          }
        ],
        "content": {
          "text_available": true,
          "image_available": true,
          "image_url": "https://cdn.whileyouweresleeping.com/briefings/brf_20240114_060000_xyz789.png",
          "thumbnail_url": "https://cdn.whileyouweresleeping.com/briefings/thumbnails/brf_20240114_060000_xyz789.png"
        },
        "sent_channels": ["email"],
        "view_count": 8
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 45,
      "total_pages": 5,
      "has_next": true,
      "has_prev": false
    }
  }
}
```

<br>

---

<br>

### 📄 특정 브리핑 상세 조회

> 특정 브리핑의 전체 내용과 발송 히스토리를 조회합니다.

<br>

#### 📋 기본 정보

| 항목 | 내용 |
|------|------|
| **HTTP Method** | `GET` |
| **Endpoint** | `/briefings/{briefing_id}` |
| **인증 필요** | ✅ 필수 |
| **Rate Limit** | 분당 100회 |

<br>

#### 🔗 Path Parameters

| 파라미터 | 타입 | 필수 | 설명 |
|----------|------|------|------|
| `briefing_id` | `string` | ✅ | 조회할 브리핑 ID |

<br>

#### 📤 Request Example

```http
GET /v1/briefings/brf_20240115_060000_abc123
Authorization: Bearer {your_jwt_token}
```

**curl 예제:**

```bash
curl -X GET "https://api.whileyouweresleeping.com/v1/briefings/brf_20240115_060000_abc123" \
  -H "Authorization: Bearer {your_jwt_token}"
```

<br>

#### ✅ Response Example (200 OK)

```json
{
  "success": true,
  "data": {
    "briefing_id": "brf_20240115_060000_abc123",
    "generated_at": "2024-01-15T06:00:00Z",
    "status": "completed",
    "stocks": [
      {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "price": 185.50,
        "change_percent": 2.35,
        "volume": 45234567,
        "news_count": 3
      }
    ],
    "content": {
      "text": {
        "title": "오늘의 화제 종목 브리핑",
        "summary": "2024년 1월 15일 미국 증시에서 가장 활발했던 종목들을 정리했습니다...",
        "full_content": "..."
      },
      "image": {
        "url": "https://cdn.whileyouweresleeping.com/briefings/brf_20240115_060000_abc123.png",
        "thumbnail_url": "https://cdn.whileyouweresleeping.com/briefings/thumbnails/brf_20240115_060000_abc123.png",
        "width": 1200,
        "height": 1600,
        "format": "png",
        "file_size_bytes": 245678
      }
    },
    "metadata": {
      "template_used": "default_v1",
      "generation_time_ms": 3450,
      "ai_model": "gemini-pro",
      "language": "ko"
    },
    "send_history": [
      {
        "channel": "email",
        "email": "user@example.com",
        "sent_at": "2024-01-15T06:01:00Z",
        "status": "sent"
      },
      {
        "channel": "slack",
        "slack_channel": "#stock-briefing",
        "sent_at": "2024-01-15T06:01:01Z",
        "status": "sent"
      }
    ],
    "view_count": 12,
    "last_viewed_at": "2024-01-15T08:30:00Z"
  }
}
```

<br>

#### ❌ Error Cases

| HTTP Status | Error Code | 설명 |
|-------------|------------|------|
| `400` | `INVALID_PARAMETER` | 잘못된 파라미터 |
| `401` | `UNAUTHORIZED` | 인증 실패 또는 토큰 만료 |
| `403` | `FORBIDDEN` | 접근 권한 없음 |
| `404` | `BRIEFING_NOT_FOUND` | 브리핑을 찾을 수 없음 |
| `500` | `INTERNAL_ERROR` | 내부 서버 오류 |

<br>

---

<br>

## 🚨 공통 에러 응답 형식

모든 API는 통일된 형식의 에러 응답을 반환합니다.

<br>

### 에러 응답 구조

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "사용자 친화적인 에러 메시지",
    "details": {
      "field": "추가 에러 상세 정보 (선택사항)"
    },
    "request_id": "req_1234567890abcdef",
    "timestamp": "2024-01-15T06:00:00Z"
  }
}
```

<br>

### 주요 에러 코드

| Error Code | HTTP Status | 설명 |
|------------|-------------|------|
| `INVALID_REQUEST` | 400 | 잘못된 요청 형식 |
| `INVALID_PARAMETER` | 400 | 잘못된 파라미터 값 |
| `UNAUTHORIZED` | 401 | 인증 실패 |
| `FORBIDDEN` | 403 | 접근 권한 없음 |
| `NOT_FOUND` | 404 | 리소스를 찾을 수 없음 |
| `RATE_LIMIT_EXCEEDED` | 429 | API 호출 제한 초과 |
| `INTERNAL_ERROR` | 500 | 내부 서버 오류 |
| `SERVICE_UNAVAILABLE` | 503 | 서비스 일시 장애 |

<br>

---

<br>

## ⚡ Rate Limiting

API 호출 횟수는 사용자 플랜에 따라 제한됩니다.

<br>

### 사용자별 제한

| 사용자 타입 | 분당 제한 | 시간당 제한 | 일일 제한 |
|------------|----------|------------|----------|
| **무료 사용자** | 10회 | 100회 | 1,000회 |
| **프리미엄 사용자** | 60회 | 1,000회 | 10,000회 |
| **엔터프라이즈** | 협의 | 협의 | 협의 |

<br>

### Rate Limit 헤더

Rate limit 관련 정보는 모든 응답의 헤더에 포함됩니다:

```http
X-RateLimit-Limit: 100        # 시간당 최대 호출 횟수
X-RateLimit-Remaining: 45     # 남은 호출 횟수
X-RateLimit-Reset: 1705296000 # 제한 초기화 시간 (Unix timestamp)
```

<br>

### Rate Limit 초과 시

```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "API 호출 제한을 초과했습니다. 잠시 후 다시 시도해주세요.",
    "details": {
      "retry_after": 30,
      "limit": 100,
      "window": "1 hour"
    },
    "request_id": "req_abc123",
    "timestamp": "2024-01-15T06:00:00Z"
  }
}
```

<br>

---

<br>

## 🔐 인증

API 인증은 JWT (JSON Web Token)을 사용합니다.

<br>

### 1️⃣ 토큰 발급

#### Request

```http
POST /v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "your_secure_password"
}
```

**curl 예제:**

```bash
curl -X POST "https://api.whileyouweresleeping.com/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "your_secure_password"
  }'
```

<br>

#### Response

```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "expires_at": "2024-01-16T06:00:00Z",
    "expires_in": 86400,
    "user": {
      "id": "user_123",
      "email": "user@example.com",
      "name": "홍길동",
      "plan": "premium"
    }
  }
}
```

<br>

### 2️⃣ API 호출 시 인증

모든 인증이 필요한 API 호출 시 `Authorization` 헤더에 토큰을 포함합니다:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

<br>

### 3️⃣ 토큰 갱신

만료된 토큰을 갱신하려면 refresh token을 사용합니다:

```http
POST /v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "your_refresh_token"
}
```

<br>

### 인증 실패 시

```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "유효하지 않거나 만료된 토큰입니다.",
    "details": {
      "reason": "token_expired"
    },
    "request_id": "req_xyz789",
    "timestamp": "2024-01-15T06:00:00Z"
  }
}
```

<br>

---

<br>

## 📚 추가 정보

### 지원 및 문의

- 📧 **이메일**: support@whileyouweresleeping.com
- 📖 **개발자 문서**: https://docs.whileyouweresleeping.com
- 💬 **Discord 커뮤니티**: https://discord.gg/whileyouweresleeping

<br>

### 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| **v1.0** | 2024-01-15 | 초기 버전 릴리스 |

<br>

---

<div align="center">

**"당신이 잠든 사이" REST API v1.0**

Made with ❤️ by WYWS Team

</div>



