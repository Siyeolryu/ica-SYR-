#!/usr/bin/env python3
"""
브리핑 생성 MCP 서버
Claude Desktop에서 "당신이 잠든 사이" 브리핑을 생성할 수 있습니다.
"""
import sys
import os

# 상위 디렉토리를 path에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
import logging
from datetime import datetime
import base64

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MCP 서버 생성
app = Server("briefing-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """사용 가능한 도구 목록 반환"""
    return [
        Tool(
            name="generate_daily_briefing",
            description="화제 종목을 자동으로 선정하고 AI 브리핑을 생성합니다. 뉴스 수집, 분석, 이미지 생성을 모두 포함한 완전 자동화 워크플로우입니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "include_image": {
                        "type": "boolean",
                        "description": "브리핑 이미지 생성 여부",
                        "default": True
                    }
                }
            }
        ),
        Tool(
            name="analyze_stock_trending_reason",
            description="특정 종목이 화제가 된 이유를 분석합니다. 뉴스와 시장 데이터를 종합하여 AI가 분석합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "종목 심볼 (예: AAPL, TSLA, MSFT)"
                    },
                    "include_news": {
                        "type": "boolean",
                        "description": "관련 뉴스 포함 여부",
                        "default": True
                    }
                },
                "required": ["symbol"]
            }
        ),
        Tool(
            name="get_stock_news": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "종목 심볼 (예: AAPL)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "뉴스 개수 (기본: 5)",
                        "default": 5
                    }
                },
                "required": ["symbol"]
            },
            description="Exa API를 사용하여 특정 종목의 최신 뉴스를 수집하고 요약합니다."
        }
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent | ImageContent]:
    """도구 실행"""
    try:
        if name == "generate_daily_briefing":
            from daily_briefing_workflow import run_daily_briefing_workflow

            include_image = arguments.get("include_image", True)

            logger.info(f"브리핑 생성 시작: include_image={include_image}")

            result = run_daily_briefing_workflow()

            if not result or not result.get('briefing_data'):
                return [TextContent(type="text", text="브리핑 생성에 실패했습니다.")]

            briefing_data = result['briefing_data']
            top_stock = result.get('top_stock', {})

            # 텍스트 브리핑
            text_content = f"# 🌙 당신이 잠든 사이 - 오늘의 브리핑\n\n"
            text_content += f"**생성 시간**: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M:%S')}\n\n"

            if top_stock:
                text_content += f"## 📈 오늘의 화제 종목\n\n"
                text_content += f"### {top_stock.get('symbol')} - {top_stock.get('name')}\n"
                text_content += f"- **현재가**: ${top_stock.get('price', 0):.2f}\n"
                text_content += f"- **변동률**: {top_stock.get('change_percent', 0):.2f}%\n"
                text_content += f"- **거래량**: {top_stock.get('volume', 0):,}\n\n"

            # 브리핑 내용
            if briefing_data.get('text_content'):
                text_content += f"## 📝 브리핑 내용\n\n"
                text_content += briefing_data['text_content']

            # 분석 결과
            if briefing_data.get('analysis'):
                text_content += f"\n\n## 🔍 화제 원인 분석\n\n"
                text_content += briefing_data['analysis']

            contents = [TextContent(type="text", text=text_content)]

            # 이미지 포함
            if include_image and briefing_data.get('image_path'):
                try:
                    image_path = briefing_data['image_path']
                    if os.path.exists(image_path):
                        with open(image_path, 'rb') as f:
                            image_data = base64.b64encode(f.read()).decode('utf-8')
                        contents.append(ImageContent(
                            type="image",
                            data=image_data,
                            mimeType="image/png"
                        ))
                        logger.info(f"브리핑 이미지 포함됨: {image_path}")
                except Exception as e:
                    logger.error(f"이미지 로드 실패: {str(e)}")

            return contents

        elif name == "analyze_stock_trending_reason":
            from gemini_briefing import analyze_why_trending
            from yahooquery import Ticker
            from exa_news import search_and_summarize_news

            symbol = arguments["symbol"].upper()
            include_news = arguments.get("include_news", True)

            logger.info(f"종목 분석 시작: {symbol}")

            # 종목 정보 가져오기
            ticker = Ticker(symbol)
            quotes = ticker.quotes

            if symbol not in quotes:
                return [TextContent(type="text", text=f"종목 {symbol}을(를) 찾을 수 없습니다.")]

            stock_data = quotes[symbol]

            # 뉴스 수집
            news_summary = ""
            if include_news:
                try:
                    news_result = search_and_summarize_news(
                        company_name=stock_data.get('shortName', symbol),
                        num_results=5
                    )
                    if news_result and news_result.get('summary'):
                        news_summary = news_result['summary']
                except Exception as e:
                    logger.error(f"뉴스 수집 실패: {str(e)}")
                    news_summary = "뉴스를 가져올 수 없습니다."

            # AI 분석
            try:
                analysis = analyze_why_trending(stock_data, news_summary)
            except Exception as e:
                logger.error(f"AI 분석 실패: {str(e)}")
                analysis = "분석을 수행할 수 없습니다."

            # 결과 포맷팅
            result_text = f"# {symbol} - 화제 원인 분석\n\n"
            result_text += f"## 📊 종목 정보\n"
            result_text += f"- **회사명**: {stock_data.get('shortName', '')}\n"
            result_text += f"- **현재가**: ${stock_data.get('regularMarketPrice', 0):.2f}\n"
            result_text += f"- **변동률**: {stock_data.get('regularMarketChangePercent', 0):.2f}%\n"
            result_text += f"- **거래량**: {stock_data.get('regularMarketVolume', 0):,}\n\n"

            if news_summary:
                result_text += f"## 📰 관련 뉴스 요약\n\n{news_summary}\n\n"

            result_text += f"## 🔍 AI 분석 결과\n\n{analysis}\n"

            return [TextContent(type="text", text=result_text)]

        elif name == "get_stock_news":
            from exa_news import search_and_summarize_news
            from yahooquery import Ticker

            symbol = arguments["symbol"].upper()
            limit = arguments.get("limit", 5)

            logger.info(f"뉴스 수집: {symbol}, limit={limit}")

            # 회사명 가져오기
            ticker = Ticker(symbol)
            quotes = ticker.quotes

            if symbol not in quotes:
                return [TextContent(type="text", text=f"종목 {symbol}을(를) 찾을 수 없습니다.")]

            company_name = quotes[symbol].get('shortName', symbol)

            # 뉴스 검색
            try:
                news_result = search_and_summarize_news(
                    company_name=company_name,
                    num_results=limit
                )

                if not news_result:
                    return [TextContent(type="text", text=f"{symbol}에 대한 뉴스를 찾을 수 없습니다.")]

                result_text = f"# {symbol} - 최신 뉴스\n\n"
                result_text += f"**검색어**: {company_name}\n"
                result_text += f"**수집 뉴스 수**: {limit}개\n\n"

                if news_result.get('summary'):
                    result_text += f"## 📝 뉴스 요약\n\n{news_result['summary']}\n\n"

                if news_result.get('articles'):
                    result_text += f"## 📰 뉴스 목록\n\n"
                    for idx, article in enumerate(news_result['articles'], 1):
                        result_text += f"### {idx}. {article.get('title', '제목 없음')}\n"
                        result_text += f"- **출처**: {article.get('url', '')}\n"
                        if article.get('published_date'):
                            result_text += f"- **날짜**: {article.get('published_date')}\n"
                        if article.get('snippet'):
                            result_text += f"- **내용**: {article.get('snippet')[:200]}...\n"
                        result_text += "\n"

                return [TextContent(type="text", text=result_text)]

            except Exception as e:
                logger.error(f"뉴스 수집 실패: {str(e)}")
                return [TextContent(type="text", text=f"뉴스 수집 중 오류 발생: {str(e)}")]

        else:
            return [TextContent(type="text", text=f"알 수 없는 도구: {name}")]

    except Exception as e:
        logger.error(f"도구 실행 오류: {str(e)}")
        return [TextContent(type="text", text=f"오류 발생: {str(e)}")]


async def main():
    """MCP 서버 실행"""
    logger.info("브리핑 생성 MCP 서버 시작...")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
