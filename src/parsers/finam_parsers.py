from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import feedparser
from ..clients.redis_client import save_fundamental
from datetime import datetime

def parse_pe_pb(driver, ticker):
    try:
        driver.get(f"https://www.finam.ru/quote/moex/{ticker.lower()}/financial/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'P/E')]"))
        )

        rows = driver.find_elements(By.CSS_SELECTOR, "table.table-generic tbody tr")
        result = {"Ticker": ticker, "P/E": "N/A", "P/B": "N/A"}

        for row in rows:
            title_elem = row.find_elements(By.CSS_SELECTOR, ".finfin-local-plugin-company-item-part-financial-row-title div.p05x")
            if not title_elem:
                continue
            title = title_elem[0].text.strip()
            values = [td.text.strip() for td in row.find_elements(By.CSS_SELECTOR, "td[align='right']")]
            if "P/E" in title:
                result["P/E"] = values[-1] if values else "N/A"
            elif "P/B" in title:
                result["P/B"] = values[-1] if values else "N/A"

        return result

    except Exception as e:
        print(f"Ошибка (PE/PB {ticker}): {e}")
        return None

def parse_divs(driver, ticker):
    try:
        driver.get(f"https://www.finam.ru/quote/moex/{ticker.lower()}/dividends/")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.table-generic tbody tr"))
        )

        rows = driver.find_elements(By.CSS_SELECTOR, "table.table-generic tbody tr")
        all_dividends = []

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) < 3:
                continue
            dividend = {
                "Ticker": ticker,
                "Date": cells[1].text.strip(),
                "Amount": cells[2].text.strip().replace('\xa0', ''),
                "Income": cells[-1].text.strip().replace('\xa0', '')
            }
            all_dividends.append(dividend)

        return all_dividends

    except Exception as e:
        print(f"Ошибка (Divs {ticker}): {e}")
        return []


def parse_rss_news(ticker, rss_url):
    key = f"{ticker}:news"

    feed = feedparser.parse(rss_url)
    news_items = []
    for entry in feed.entries:
        date = datetime.strptime(entry.get("published", ""), "%a, %d %b %Y %H:%M:%S %z")
        formatted_date = date.strftime("%d.%m.%Y %H:%M")
        news_items.append({
            "title": entry.title,
            "link": entry.link,
            "pubDate": formatted_date,
            "source": rss_url
        })

    if news_items:
        save_fundamental(key, news_items)

    return news_items
