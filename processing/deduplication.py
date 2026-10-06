import hashlib
import re


def normalize_for_duplicate(value):
    """
    Normalize text before generating a duplicate fingerprint.
    """
    if value is None:
        return ""

    value = str(value).lower().strip()

    # Remove punctuation
    value = re.sub(r"[^\w\s]", "", value)

    # Collapse multiple spaces
    value = re.sub(r"\s+", " ", value)

    return value


def create_fingerprint(record):
    """
    Create a unique fingerprint for a record.

    Books:
        source + title

    Quotes:
        source + author + first 50 characters of quote
    """

    source = normalize_for_duplicate(record.get("source"))

    name_or_title = normalize_for_duplicate(
        record.get("name_or_title")
    )

    author = normalize_for_duplicate(
        record.get("author")
    )

    if source == "books":
        raw_key = f"{source}|{name_or_title}"

    elif source == "quotes":
        quote_text = name_or_title[:50]
        raw_key = f"{source}|{author}|{quote_text}"

    else:
        raw_key = f"{source}|{name_or_title}|{author}"

    return hashlib.sha256(
        raw_key.encode("utf-8")
    ).hexdigest()


def deduplicate_records(records):
    """
    Remove duplicate records.

    Returns:
        unique_records
        duplicate_records
    """

    seen = set()
    unique_records = []
    duplicate_records = []

    for record in records:

        fingerprint = create_fingerprint(record)

        if fingerprint in seen:
            duplicate_records.append(record)
        else:
            seen.add(fingerprint)
            unique_records.append(record)

    return unique_records, duplicate_records