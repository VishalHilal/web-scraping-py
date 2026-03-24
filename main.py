import requests
from bs4 import BeautifulSoup
import csv
import json
import time
import pandas as pd

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

session = requests.Session()
all_books = []


def get_page(url, retries=3):
    for attempt in range(retries):
        try:
            response = session.get(url, headers=HEADERS, timeout=10)
            if response.status_code == 200:
                return response
        except Exception as e:
            print(f"Retry {attempt+1} failed:", e)
            time.sleep(2)
    return None


def scrape_books():
    page = 1

    while True:
        print(f"Scraping page {page}...")

        url = BASE_URL.format(page)
        response = get_page(url)

        if not response:
            print("Stopping: Page not reachable")
            break

        soup = BeautifulSoup(response.text, "lxml")
        books = soup.select(".product_pod")

        if not books:
            print("No more books found.")
            break

        for book in books:
            try:
                title = book.select_one("h3 a")["title"].strip()

                price_text = book.select_one(".price_color").text.strip()
                price = float(price_text.replace("£", ""))

                rating = book.select_one("p.star-rating")["class"][1]

                availability = book.select_one(".availability").text.strip()

                relative_url = book.select_one("h3 a")["href"]
                product_url = "https://books.toscrape.com/catalogue/" + relative_url

                image_url = book.select_one("img")["src"]
                image_url = "https://books.toscrape.com/" + image_url.replace("../", "")

                all_books.append({
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "availability": availability,
                    "product_url": product_url,
                    "image_url": image_url
                })

            except Exception as e:
                print("Error parsing book:", e)

        page += 1
        time.sleep(1)


def save_csv():
    with open("books.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_books[0].keys())
        writer.writeheader()
        writer.writerows(all_books)


def save_json():
    with open("books.json", "w", encoding="utf-8") as f:
        json.dump(all_books, f, indent=4)


def save_excel():
    df = pd.DataFrame(all_books)
    df.to_excel("books.xlsx", index=False)


if __name__ == "__main__":
    scrape_books()

    print(f"\nTotal Books Scraped: {len(all_books)}")

    if all_books:
        save_csv()
        save_json()
        save_excel()
        print("Data saved to CSV, JSON, and Excel.")
    else:
        print("No data to save.")
