from ..services.parsers_service import get_candles_cached, get_pe_pb_cached, get_divs_cached, get_news_cached
from litestar import get
from typing import List,Dict,Any

@get("/candles")
async def get_candles(ticker: str, tf: str) -> List[Dict[str, Any]]:
    return await get_candles_cached(ticker, tf)

@get("/fundamentals/pe_pb")
async def get_pe_pb(ticker: str) -> Dict[str, Any]:
    return await get_pe_pb_cached(ticker)

@get("/fundamentals/dividends")
async def get_dividends(ticker: str) -> List[Dict[str, Any]]:
    return await get_divs_cached(ticker)

@get("/news")
async def get_news(ticker: str, rss_url: str) -> List[Dict[str, Any]]:
    return await get_news_cached(ticker, rss_url)
