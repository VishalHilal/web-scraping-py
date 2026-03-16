import requests
from bs4 import BeautifulSoup
import csv
import time

base_url = "https://books.toscrape.com/catalogue/page-{}.html"

headers = {
    "User-Agent": "Mozilla/5.0"
}

all_books = []

for page in range(1, 6):

    url = base_url.format(page)

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Request failed")
        continue

    soup = BeautifulSoup(response.text, "lxml")

    books = soup.select(".product_pod")

    for book in books:

        title = book.select_one("h3 a")["title"].strip()

        price = book.select_one(".price_color").text.strip()

        all_books.append({
            "title": title,
            "price": price
        })

    time.sleep(1)

print("Total Books Scraped:", len(all_books))

with open("books.csv","w",newline="",encoding="utf-8") as f:

    writer = csv.DictWriter(f, fieldnames=["title","price"])

    writer.writeheader()

    writer.writerows(all_books)
