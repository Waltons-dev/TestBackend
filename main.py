from selenium_driver import init_driver
from parsers import parse_pe_pb, parse_divs, parse_rss_news
from redis_client import save, load

tickers = ["sber", "gazp"]
rss_feeds = {
    "sber": "https://www.finam.ru/analysis/conews/rsspoint/",
    "gazp": "https://www.finam.ru/analysis/conews/rsspoint/"
}
driver = init_driver()

for t in tickers:
    pe_pb = load(f"{t}:pe_pb")
    divs = load(f"{t}:divs")

    if not pe_pb:
        pe_pb = parse_pe_pb(driver, t)
        if pe_pb:
            save(f"{t}:pe_pb", pe_pb)

    if not divs:
        divs = parse_divs(driver, t)
        if divs:
            save(f"{t}:divs", divs)

driver.quit()


for t in tickers:
    print(f"\nPE/PB {t}:", load(f"{t}:pe_pb"))
    print(f"Dividends {t}:", load(f"{t}:divs"))

    AllNews = parse_rss_news(t, rss_feeds[t])
    print(f"\nНовости {t}:")
    for news in AllNews[:5]:
        print(f"{news['title']} ({news['pubDate']})")

