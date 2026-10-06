import re
from urllib.parse import urljoin


def clean_text(value):
    """
    Clean text by removing extra whitespace.
    Return None for missing values.
    """
    if value is None:
        return None

    value = str(value).strip()

    if not value:
        return None

    value = re.sub(r"\s+", " ", value)

    return value


def clean_price(value):
    """
    Convert price values such as '£51.77' into 51.77.
    """
    if value is None:
        return None

    value = str(value).strip()

    match = re.search(r"\d+(?:\.\d+)?", value)

    if not match:
        return None

    try:
        return float(match.group())
    except ValueError:
        return None


def clean_rating(value):
    """
    Convert rating values into integers from 1 to 5.
    """
    if value is None:
        return None

    if isinstance(value, int):
        return value if 1 <= value <= 5 else None

    value = str(value).strip()

    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    if value in rating_map:
        return rating_map[value]

    try:
        rating = int(value)

        if 1 <= rating <= 5:
            return rating

    except ValueError:
        pass

    return None


def clean_tags(tags):
    """
    Clean a list of tags.
    """
    if not tags:
        return []

    cleaned = []

    for tag in tags:
        tag = clean_text(tag)

        if tag:
            cleaned.append(tag)

    return cleaned


def normalize_url(url, base_url=None):
    """
    Convert relative URLs into absolute URLs.
    """
    if not url:
        return None

    url = str(url).strip()

    if not url:
        return None

    if base_url:
        return urljoin(base_url, url)

    return url


def clean_record(record):
    """
    Clean one scraped record.
    """
    cleaned = record.copy()

    cleaned["source"] = clean_text(cleaned.get("source"))

    cleaned["source_url"] = normalize_url(
        cleaned.get("source_url")
    )

    cleaned["name_or_title"] = clean_text(
        cleaned.get("name_or_title")
    )

    cleaned["category"] = clean_text(
        cleaned.get("category")
    )

    cleaned["price"] = clean_price(
        cleaned.get("price")
    )

    cleaned["rating"] = clean_rating(
        cleaned.get("rating")
    )

    cleaned["author"] = clean_text(
        cleaned.get("author")
    )

    cleaned["tags"] = clean_tags(
        cleaned.get("tags")
    )

    cleaned["description"] = clean_text(
        cleaned.get("description")
    )

    return cleaned