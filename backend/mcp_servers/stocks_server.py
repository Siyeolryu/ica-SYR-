#!/usr/bin/env python3
"""
화제 종목 조회 MCP 서버
Claude Desktop이나 다른 MCP 클라이언트에서 미국 주식 화제 종목을 조회할 수 있습니다.
"""
import sys
import os

# 상위 디렉토리를 path에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import logging
from get_trending_stocks import get_trending_stocks, get_top_trending_stock, format_stock_data

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MCP 서버 생성
app = Server("stocks-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """사용 가능한 도구 목록 반환"""
    return [
        Tool(
            name="get_trending_stocks",
            description="Yahoo Finance에서 화제 종목 목록을 조회합니다. 거래량 상위(most_actives)와 상승률 상위(day_gainers) 종목을 가져올 수 있습니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "screener_types": {
                        "type": "array",
                        "items": {"type": "string", "enum": ["most_actives", "day_gainers", "day_losers"]},
                        "description": "스크리너 타입 목록. most_actives(거래량 상위), day_gainers(상승률 상위), day_losers(하락률 상위)",
                        "default": ["most_actives", "day_gainers"]
                    },
                    "count": {
                        "type": "integer",
                        "description": "각 스크리너에서 가져올 종목 수 (1-50)",
                        "minimum": 1,
                        "maximum": 50,
                        "default": 10
                    }
                }
            }
        ),
        Tool(
            name="get_top_trending_stock",
            description="오늘의 화제 종목 TOP 1을 가져옵니다. 거래량이 가장 많거나 상승률이 가장 높은 종목을 반환합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "screener_types": {
                        "type": "array",
                        "items": {"type": "string", "enum": ["most_actives", "day_gainers"]},
                        "description": "우선순위 스크리너 타입",
                        "default": ["most_actives", "day_gainers"]
                    },
                    "count": {
                        "type": "integer",
                        "description": "조회할 종목 수",
                        "default": 5
                    }
                }
            }
        ),
        Tool(
            name="get_stock_info",
            description="특정 종목의 상세 정보를 조회합니다. Yahoo Finance에서 실시간 데이터를 가져옵니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "종목 심볼 (예: AAPL, TSLA, MSFT)",
                    }
                },
                "required": ["symbol"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """도구 실행"""
    try:
        if name == "get_trending_stocks":
            screener_types = arguments.get("screener_types", ["most_actives", "day_gainers"])
            count = arguments.get("count", 10)

            logger.info(f"화제 종목 조회: screener_types={screener_types}, count={count}")

            stocks_data = get_trending_stocks(screener_types=screener_types, count=count)

            # 결과 포맷팅
            result_text = "# 화제 종목 목록\n\n"
            total_count = 0

            for screener_type, quotes in stocks_data.items():
                if quotes:
                    result_text += f"## {screener_type}\n\n"
                    for quote in quotes:
                        stock = format_stock_data(quote)
                        result_text += f"### {stock['symbol']} - {stock['name']}\n"
                        result_text += f"- 현재가: ${stock['price']:.2f}\n"
                        result_text += f"- 변동률: {stock['change_percent']:.2f}%\n"
                        result_text += f"- 거래량: {stock['volume']:,}\n"
                        result_text += f"- 시가총액: ${stock['market_cap']:,}\n\n"
                        total_count += 1

            result_text += f"\n**총 {total_count}개 종목 조회 완료**"

            return [TextContent(type="text", text=result_text)]

        elif name == "get_top_trending_stock":
            screener_types = arguments.get("screener_types", ["most_actives", "day_gainers"])
            count = arguments.get("count", 5)

            logger.info(f"TOP 1 종목 조회: screener_types={screener_types}, count={count}")

            top_stock = get_top_trending_stock(screener_types=screener_types, count=count)

            if top_stock:
                stock = format_stock_data(top_stock)
                result_text = f"# 🔥 오늘의 화제 종목 TOP 1\n\n"
                result_text += f"## {stock['symbol']} - {stock['name']}\n\n"
                result_text += f"- **현재가**: ${stock['price']:.2f}\n"
                result_text += f"- **변동**: ${stock['change']:.2f} ({stock['change_percent']:.2f}%)\n"
                result_text += f"- **거래량**: {stock['volume']:,}\n"
                result_text += f"- **시가총액**: ${stock['market_cap']:,}\n"
                result_text += f"- **데이터 수집 시간**: {stock['timestamp']}\n"
            else:
                result_text = "화제 종목을 찾을 수 없습니다."

            return [TextContent(type="text", text=result_text)]

        elif name == "get_stock_info":
            from yahooquery import Ticker
            symbol = arguments["symbol"].upper()

            logger.info(f"종목 상세 정보 조회: {symbol}")

            ticker = Ticker(symbol)
            quotes = ticker.quotes

            if symbol not in quotes or not quotes[symbol]:
                return [TextContent(type="text", text=f"종목 {symbol}을(를) 찾을 수 없습니다.")]

            quote = quotes[symbol]
            summary = ticker.summary_detail.get(symbol, {})
            profile = ticker.summary_profile.get(symbol, {})

            result_text = f"# {symbol} - {quote.get('shortName', '')}\n\n"
            result_text += f"## 기본 정보\n"
            result_text += f"- **회사명**: {quote.get('longName', quote.get('shortName', ''))}\n"
            result_text += f"- **섹터**: {profile.get('sector', 'N/A')}\n"
            result_text += f"- **산업**: {profile.get('industry', 'N/A')}\n\n"

            result_text += f"## 가격 정보\n"
            result_text += f"- **현재가**: ${quote.get('regularMarketPrice', 0):.2f}\n"
            result_text += f"- **전일종가**: ${quote.get('regularMarketPreviousClose', 0):.2f}\n"
            result_text += f"- **변동**: ${quote.get('regularMarketChange', 0):.2f} ({quote.get('regularMarketChangePercent', 0):.2f}%)\n"
            result_text += f"- **시가**: ${quote.get('regularMarketOpen', 0):.2f}\n"
            result_text += f"- **고가**: ${quote.get('regularMarketDayHigh', 0):.2f}\n"
            result_text += f"- **저가**: ${quote.get('regularMarketDayLow', 0):.2f}\n\n"

            result_text += f"## 거래 정보\n"
            result_text += f"- **거래량**: {quote.get('regularMarketVolume', 0):,}\n"
            result_text += f"- **평균거래량**: {summary.get('averageVolume', 0):,}\n"
            result_text += f"- **시가총액**: ${quote.get('marketCap', 0):,}\n\n"

            if summary.get('fiftyTwoWeekHigh') and summary.get('fiftyTwoWeekLow'):
                result_text += f"## 52주 범위\n"
                result_text += f"- **52주 최고**: ${summary.get('fiftyTwoWeekHigh', 0):.2f}\n"
                result_text += f"- **52주 최저**: ${summary.get('fiftyTwoWeekLow', 0):.2f}\n\n"

            if profile.get('longBusinessSummary'):
                result_text += f"## 회사 설명\n"
                result_text += f"{profile.get('longBusinessSummary')[:500]}...\n"

            return [TextContent(type="text", text=result_text)]

        else:
            return [TextContent(type="text", text=f"알 수 없는 도구: {name}")]

    except Exception as e:
        logger.error(f"도구 실행 오류: {str(e)}")
        return [TextContent(type="text", text=f"오류 발생: {str(e)}")]


async def main():
    """MCP 서버 실행"""
    logger.info("화제 종목 MCP 서버 시작...")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
