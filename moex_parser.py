import urllib.request
import json
from datetime import datetime
from typing import List
from datetime import timedelta
from redis_client import save_candles
from redis_client import load_candles
from redis_client import redis_has_candles
from models import Candle

# доступные инттервалы для свечей
def convert_interval(tf: str) -> int:
    return {
        "M1": 1,
        "M10": 10,
        "H1": 60,
        "D1": 24,
        "W1": 7,
        "MN": 31,
        "QN": 4
    }[tf.upper()]

# сколько дней доступно для просмотра для каждого интервала свечей
def get_days_back(tf: str) -> int | None:
    return {
        "M1": 3,
        "M10": 30,
        "H1": 100,
        "D1": None,
        "W1": None,
        "MN": None,
        "QN": None
    }[tf.upper()]


def get_stock_candles(ticker: str, tf: str) -> List[Candle]:
    headers = {"User-Agent": "Mozilla/5.0"}
    candles = []

    interval = convert_interval(tf)
    days = get_days_back(tf)

    from_param = (
        f"&from={(datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')}"
        if days is not None else ""
    )

    start = 0
    limit = 500

    while True:
        url = (
            f"https://iss.moex.com/iss/engines/stock/markets/shares/"
            f"boards/tqbr/securities/{ticker}/candles.json"
            f"?interval={interval}{from_param}&start={start}"
        )

        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode())["candles"]["data"]

        if not data:
            break

        for c in data:
            candles.append(Candle(
                time=datetime.strptime(c[7], "%Y-%m-%d %H:%M:%S"),
                open_price=float(c[0]),
                close=float(c[1]),
                high=float(c[2]),
                low=float(c[3]),
                volume=int(c[5])
            ))

        start += limit

    return sorted(candles, key=lambda x: x.time)


def parse_and_save(ticker: str, timeframe: str):
    print(f"Запрос {ticker} [{timeframe}]...")

    if redis_has_candles(ticker, timeframe):
        print("Данные найдены в Redis")
        candles = load_candles(ticker, timeframe)
    else:
        print("Парсим и сохраняем в Redis")
        candles = get_stock_candles(ticker, timeframe)

        if not candles:
            print("Нет данных от МосБиржи")
            return

        save_candles(candles, ticker, timeframe)

    print(f"Свечей: {len(candles)}")
    print(f"Период: {candles[0].time} - {candles[-1].time}")
    for c in candles:
        print(c.to_txt_format())
    return candles

if __name__ == "__main__":
    candles = parse_and_save("YDEX", "M10")

