from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time

pages = [
    {"name": "retail_interest_rates", "url": "https://bankofmaharashtra.bank.in/retail-interest-rates"},
    {"name": "maha_super_flexi", "url": "https://bankofmaharashtra.bank.in/maha-super-flexi-housing-loan-scheme"},
    {"name": "car_festive_blog", "url": "https://bankofmaharashtra.bank.in/blogs/why-you-should-buy-your-dream-car-during-festive-season"}
]

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
service = Service("/usr/bin/chromedriver")  
driver = webdriver.Chrome(service=service, options=chrome_options)

def scrape_page(name, url, selector):
    driver.get(url)
    time.sleep(2) 

    element = driver.find_element(By.CSS_SELECTOR, selector)
    html = element.get_attribute('innerHTML')
    soup = BeautifulSoup(html, "html.parser")

    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)]

    tables = []
    for table in soup.find_all("table"):
        headers = [th.get_text(strip=True) for th in table.find_all("th")]
        rows = []
        for tr in table.find_all("tr"):
            cells = [td.get_text(strip=True) for td in tr.find_all("td")]
            if cells:
                if headers and len(headers) == len(cells):
                    rows.append(dict(zip(headers, cells)))
                else:
                    rows.append(cells)
        if rows:
            tables.append({"title": table.get("summary", ""), "columns": headers, "rows": rows})

    return {"paragraphs": paragraphs, "tables": tables}

def main():
    selectors = {
        "retail_interest_rates": "body > div.outerWrap > div.dvMainBodyCLS > div.container-fluid.contentarea.cmpad > div > div > div",
        "maha_super_flexi": "body > div.outerWrap > div.dvMainBodyCLS > div.container-fluid.contentarea.cmpad > div > div > div > div",
        "car_festive_blog": "body > div.outerWrap > div.dvMainBodyCLS > div.container-fluid.contentarea.cmpad > div > div.detarea > div:nth-child(2) > div"
    }

    data = {}
    for page in pages:
        print(f"[Scraping] {page['name']} ...")
        data[page['name']] = scrape_page(page['name'], page['url'], selectors[page['name']])
    
    with open("scraped_pages.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Scraping completed!")

if __name__ == "__main__":
    main()
    driver.quit()
