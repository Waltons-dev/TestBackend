### Run app  
```
uv run granian src.app:app --interface asgi --port 8000
```


### Вывод sber pe pb:
```
{
   "Ticker":"sber",
   "P/E":"3,94",
   "P/B":"0,87"
}
```

### Вывод sber divs:  
```
[
   {
      "Ticker":"SBER",
      "Date":"18.07.2025",
      "Amount":"34,84 ₽",
      "Income":"10,65%"
   },
   {
      "Ticker":"SBER",
      "Date":"11.07.2024",
      "Amount":"33,3 ₽",
      "Income":"10,52%"
   },
   {
    "Ticker": "SBER",
    "Date": "11.05.2023",
    "Amount": "25,0 ₽",
    "Income": "10,49%"
  },
]
```

### Вывод news:  
```
[
   {
    "title": "«Сбер» сохраняет план выплатить дивиденды в 2026 году в размере 50% от прибыли за 2025 год",
    "link": "https://www.finam.ru/publications/item/sber-sokhranyaet-plan-vyplatit-dividendy-v-2026-godu-v-razmere-50-ot-pribyli-za-2025-god-20251210-1120/?utm_source=rss&utm_medium=new_compaigns&news_to_finamb=new_compaigns",
    "pubDate": "10.12.2025 11:15",
    "source": "https://www.finam.ru/analysis/conews/rsspoint/"
  },
  {
    "title": "Рынок растет на фоне небольшого ослабления рубля",
    "link": "https://www.finam.ru/publications/item/rynok-rastet-na-fone-nebolshogo-oslableniya-rublya-20251210-1006/?utm_source=rss&utm_medium=new_compaigns&news_to_finamb=new_compaigns",
    "pubDate": "10.12.2025 10:06",
    "source": "https://www.finam.ru/analysis/conews/rsspoint/"
  },
  {
    "title": "“Сбер” проведет День инвестора - основные события 10 декабря",
    "link": "https://www.finam.ru/publications/item/sber-provedet-den-investora-osnovnye-sobytiya-10-dekabrya-20251210-0900/?utm_source=rss&utm_medium=new_compaigns&news_to_finamb=new_compaigns",
    "pubDate": "09.12.2025 20:08",
    "source": "https://www.finam.ru/analysis/conews/rsspoint/"
  },
]
```

### Вывод SBER свечей с интервалом M1(1 минута):  
```
[
  {
    "time": "2025-12-08T06:59:59",
    "open": 307.53,
    "high": 307.53,
    "low": 307.53,
    "close": 307.53,
    "volume": 30832
  },
  {
    "time": "2025-12-08T07:00:59",
    "open": 307.55,
    "high": 307.79,
    "low": 307.3,
    "close": 307.44,
    "volume": 51236
  },
  {
    "time": "2025-12-08T07:01:59",
    "open": 307.3,
    "high": 307.44,
    "low": 306.88,
    "close": 307.16,
    "volume": 85558
  },
]
```