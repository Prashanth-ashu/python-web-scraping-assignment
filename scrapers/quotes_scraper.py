import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE_URL = "https://quotes.toscrape.com/"


def create_session():
    session = requests.Session()

    session.headers.update({
        "User-Agent": "Mozilla/5.0 (compatible; ScrapingAssignment/1.0)"
    })

    return session


def scrape_quotes():
    session = create_session()

    current_url = BASE_URL
    quotes = []

    while current_url:
        print(f"Scraping: {current_url}")

        try:
            response = session.get(current_url, timeout=10)
            response.raise_for_status()

        except requests.RequestException as error:
            print(f"Request failed for {current_url}: {error}")
            break

        soup = BeautifulSoup(response.text, "lxml")

        quote_cards = soup.select("div.quote")

        for quote in quote_cards:

            # Quote text
            quote_element = quote.select_one("span.text")

            if not quote_element:
                continue

            quote_text = quote_element.get_text(strip=True)

            # Author
            author_element = quote.select_one("small.author")
            author = (
                author_element.get_text(strip=True)
                if author_element
                else None
            )

            # Author URL
            author_link = quote.select_one("a[href^='/author/']")

            author_url = None

            if author_link:
                author_url = urljoin(
                    current_url,
                    author_link.get("href", "")
                )

            # Tags
            tag_elements = quote.select("div.tags a.tag")

            tags = [
                tag.get_text(strip=True)
                for tag in tag_elements
            ]

            # Store the quote
            quote_record = {
                "source": "quotes",
                "source_url": current_url,
                "name_or_title": quote_text,
                "category": None,
                "price": None,
                "rating": None,
                "author": author,
                "tags": tags,
                "description": None,
                "author_url": author_url
            }

            quotes.append(quote_record)

        # Find next page
        next_link = soup.select_one("li.next a")

        if next_link:
            next_url = next_link.get("href")
            current_url = urljoin(current_url, next_url)
        else:
            current_url = None

    return quotes


if __name__ == "__main__":
    quotes = scrape_quotes()

    print(f"\nTotal quotes scraped: {len(quotes)}")

    if quotes:
        print("\nFirst quote:")
        print(quotes[0])