import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"


#headers = {
#    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
#    "Accept-Language": "en-US,en;q=0.9"
#}


headers = {
 "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "lxml")

books = soup.find_all("article", class_="product_pod")

for book in books:

    title = book.find("h3").find("a").get("title").strip()

    price = book.find("p", class_="price_color").get_text().strip()

    print(title, price)

for page in range(1,6):

    url = f"https://books.toscrape.com/catalogue/page-{page}.html"

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text,"lxml")

    books = soup.find_all("article",class_="product_pod")

    for book in books:
        title = book.h3.a["title"]
        print(title)

