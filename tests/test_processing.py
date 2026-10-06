from processing.cleaning import clean_text, clean_price, clean_rating, clean_tags
from processing.validation import validate_record
from processing.deduplication import deduplicate_records


def test_clean_text():
    assert clean_text("  Hello    World  ") == "Hello World"


def test_clean_price():
    assert clean_price("£51.77") == 51.77


def test_clean_rating():
    assert clean_rating("Three") == 3


def test_clean_tags():
    assert clean_tags(["  change ", "deep-thoughts", " thinking "]) == [
        "change",
        "deep-thoughts",
        "thinking",
    ]


def test_validate_valid_record():
    record = {
        "source": "books",
        "source_url": "https://books.toscrape.com/book1",
        "name_or_title": "A Test Book",
        "price": 10.50,
        "rating": 4,
    }

    is_valid, errors = validate_record(record)

    assert is_valid is True
    assert errors == []


def test_validate_invalid_record():
    record = {
        "source": "unknown",
        "source_url": "wrong-url",
        "name_or_title": "",
        "price": -10,
        "rating": 8,
    }

    is_valid, errors = validate_record(record)

    assert is_valid is False
    assert len(errors) > 0


def test_deduplication():
    records = [
        {
            "source": "books",
            "name_or_title": "A Light in the Attic",
            "source_url": "https://books.toscrape.com/book1",
        },
        {
            "source": "books",
            "name_or_title": "A Light in the Attic",
            "source_url": "https://books.toscrape.com/book2",
        },
        {
            "source": "books",
            "name_or_title": "Tipping the Velvet",
            "source_url": "https://books.toscrape.com/book3",
        },
    ]

    unique, duplicates = deduplicate_records(records)

    assert len(unique) == 2
    assert len(duplicates) == 1