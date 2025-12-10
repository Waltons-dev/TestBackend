from typing import List, Dict, Any
import asyncio
from datetime import datetime
from litestar import Litestar, get
from ..clients.redis_client import save_fundamental, load_fundamental
from ..parsers.moex_parser import load_candles, parse_and_save
from ..drivers.selenium_driver import init_driver
from ..parsers.finam_parsers import parse_pe_pb, parse_divs, parse_rss_news

async def get_candles_cached(ticker: str, tf: str) -> List[Dict[str, Any]]:
    candles = load_candles(ticker, tf)
    if candles:
        return [
            {
                "time": c.time.isoformat(),
                "open": c.open,
                "high": c.high,
                "low": c.low,
                "close": c.close,
                "volume": c.volume
            }
            for c in candles
        ]

    # если нет в Redis, то парсим и сохраняем
    def run():
        return parse_and_save(ticker, tf)

    candles = await asyncio.to_thread(run)
    return [
        {
            "time": c.time.isoformat(),
            "open": c.open,
            "high": c.high,
            "low": c.low,
            "close": c.close,
            "volume": c.volume
        }
        for c in candles
    ]




async def get_pe_pb_cached(ticker: str) -> Dict[str, Any]:
    key = f"{ticker}:pe_pb"
    data = load_fundamental(key)
    if data:
        return data

    def run():
        driver = init_driver()
        res = parse_pe_pb(driver, ticker)
        driver.quit()
        if res:
            save_fundamental(key, res)
        return res or {"Ticker": ticker, "P/E": "N/A", "P/B": "N/A"}

    return await asyncio.to_thread(run)




async def get_divs_cached(ticker: str) -> List[Dict[str, Any]]:
    key = f"{ticker}:divs"
    data = load_fundamental(key)
    if data:
        return data

    def run():
        driver = init_driver()
        res = parse_divs(driver, ticker)
        driver.quit()
        if res:
            save_fundamental(key, res)
        return res or []

    return await asyncio.to_thread(run)




async def get_news_cached(ticker: str, rss_url: str) -> List[Dict[str, Any]]:
    key = f"{ticker}:news"
    data = load_fundamental(key)
    if data:
        return data

    news_items = parse_rss_news(ticker, rss_url)
    if news_items:
        save_fundamental(key, news_items)
    return news_items