from datetime import datetime
import redis.asyncio
import json
import os
from typing import List
from models.candle import Candle

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

r = redis.Redis(
    host=REDIS_HOST, 
    port=REDIS_PORT, 
    db=REDIS_DB, 
    decode_responses=True
)

def save_fundamental(key, data):
    r.set(key, json.dumps(data, ensure_ascii=False))

def load_fundamental(key):
    value = r.get(key)
    return json.loads(value) if value else None

def save_candles(candles: List[Candle], ticker: str, timeframe: str):
    key_prefix = f"moex:{ticker}:{timeframe}"

    pipe = r.pipeline()

    for candle in candles:
        ts = int(candle.time.timestamp())

        data = {
            "open": candle.open,
            "high": candle.high,
            "low": candle.low,
            "close": candle.close,
            "volume": candle.volume
        }
        pipe.hset(f"{key_prefix}:{ts}", mapping=data)

    pipe.execute()

def load_candles(ticker: str, timeframe: str) -> List[Candle]:
    pattern = f"moex:{ticker}:{timeframe}:*"
    candles = []

    for key in r.scan_iter(match=pattern, count=1000):
        ts = int(key.split(":")[-1])
        data = r.hgetall(key)

        candles.append(Candle(
            time=datetime.fromtimestamp(ts),
            open_price=float(data["open"]),
            close=float(data["close"]),
            high=float(data["high"]),
            low=float(data["low"]),
            volume=int(data["volume"])
        ))

    return sorted(candles, key=lambda x: x.time)

def redis_has_candles(ticker: str, timeframe: str) -> bool:
    pattern = f"moex:{ticker}:{timeframe}:*"
    for i in r.scan_iter(match=pattern, count=1):
        return True
    return False
