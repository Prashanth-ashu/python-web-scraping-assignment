import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE_URL = "https://books.toscrape.com/"


def create_session():
    session = requests.Session()

    session.headers.update({
        "User-Agent": "Mozilla/5.0 (compatible; ScrapingAssignment/1.0)"
    })

    return session


def scrape_books():
    session = create_session()

    current_url = BASE_URL
    books = []

    while current_url:
        print(f"Scraping: {current_url}")

        try:
            response = session.get(current_url, timeout=10)
            response.raise_for_status()

        except requests.RequestException as error:
            print(f"Request failed for {current_url}: {error}")
            break

        soup = BeautifulSoup(response.text, "lxml")

        book_cards = soup.select("article.product_pod")

        for book in book_cards:

            # Title and book URL
            title_element = book.select_one("h3 a")

            if not title_element:
                continue

            title = title_element.get("title", "").strip()

            relative_url = title_element.get("href", "")
            book_url = urljoin(current_url, relative_url)

            # Price
            price_element = book.select_one("p.price_color")
            price = price_element.get_text(strip=True) if price_element else None

            # Rating
            rating_element = book.select_one("p.star-rating")

            rating = None

            if rating_element:
                rating_classes = rating_element.get("class", [])

                rating_names = {
                    "One": 1,
                    "Two": 2,
                    "Three": 3,
                    "Four": 4,
                    "Five": 5
                }

                for class_name in rating_classes:
                    if class_name in rating_names:
                        rating = rating_names[class_name]
                        break

            # Store the book
            book_record = {
                "source": "books",
                "source_url": book_url,
                "name_or_title": title,
                "category": None,
                "price": price,
                "rating": rating,
                "author": None,
                "tags": [],
                "description": None
            }

            books.append(book_record)

        # Find next page
        next_link = soup.select_one("li.next a")

        if next_link:
            next_url = next_link.get("href")
            current_url = urljoin(current_url, next_url)
        else:
            current_url = None

    return books


if __name__ == "__main__":
    books = scrape_books()

    print(f"\nTotal books scraped: {len(books)}")

    if books:
        print("\nFirst book:")
        print(books[0])