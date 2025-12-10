from datetime import datetime

class Candle:
    def __init__(self, time: datetime, open_price: float, close: float,
                 high: float, low: float, volume: int):
        self.time = time
        self.open = open_price
        self.close = close
        self.high = high
        self.low = low
        self.volume = volume

    def to_txt_format(self) -> str:
        date_str = self.time.strftime("%Y%m%d")
        time_str = self.time.strftime("%H%M")

        return (
            f"{date_str} {time_str} "
            f"{self.open:.2f} {self.high:.2f} "
            f"{self.low:.2f} {self.close:.2f} "
            f"{self.volume}"
        )
