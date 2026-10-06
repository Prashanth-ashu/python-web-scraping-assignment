from urllib.parse import urlparse


VALID_SOURCES = {"books", "quotes"}


def validate_url(url):
    """Check whether a URL looks valid."""
    if not url:
        return False

    try:
        parsed = urlparse(url)

        return (
            parsed.scheme in {"http", "https"}
            and bool(parsed.netloc)
        )

    except Exception:
        return False


def validate_record(record):
    """
    Validate one cleaned record.

    Returns:
        (True, []) if valid
        (False, [reasons]) if invalid
    """

    errors = []

    # Source validation
    source = record.get("source")

    if source not in VALID_SOURCES:
        errors.append("invalid_source")

    # Title / quote validation
    name_or_title = record.get("name_or_title")

    if not name_or_title:
        errors.append("missing_name_or_title")

    # Source URL validation
    source_url = record.get("source_url")

    if not validate_url(source_url):
        errors.append("invalid_source_url")

    # Price validation
    price = record.get("price")

    if price is not None:
        if not isinstance(price, (int, float)):
            errors.append("invalid_price")

        elif price < 0:
            errors.append("negative_price")

    # Rating validation
    rating = record.get("rating")

    if rating is not None:
        if not isinstance(rating, int):
            errors.append("invalid_rating")

        elif not 1 <= rating <= 5:
            errors.append("rating_out_of_range")

    return len(errors) == 0, errors


def validate_records(records):
    """
    Validate multiple records.

    Returns:
        valid_records
        rejected_records
    """

    valid_records = []
    rejected_records = []

    for record in records:

        is_valid, errors = validate_record(record)

        if is_valid:
            valid_records.append(record)

        else:
            rejected_records.append({
                "record": record,
                "errors": errors
            })

    return valid_records, rejected_records