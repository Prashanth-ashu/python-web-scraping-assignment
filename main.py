import csv
import json
import logging
import time
from datetime import datetime
from pathlib import Path

from scrapers.books_scraper import scrape_books
from scrapers.quotes_scraper import scrape_quotes

from processing.cleaning import clean_record
from processing.validation import validate_records
from processing.deduplication import deduplicate_records


# ---------------------------------------------------------
# FOLDERS
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------
# LOGGING
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "scraping.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# SAVE CSV
# ---------------------------------------------------------

def save_csv(records, file_path):
    """Save final records to a CSV file."""

    if not records:
        logger.warning("No records available to save.")
        return

    fieldnames = [
        "source",
        "source_url",
        "name_or_title",
        "category",
        "price",
        "rating",
        "author",
        "tags",
        "description",
        "scraped_at"
    ]

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
            extrasaction="ignore"
        )

        writer.writeheader()
        writer.writerows(records)

    logger.info("CSV saved: %s", file_path)


# ---------------------------------------------------------
# SAVE SUMMARY JSON
# ---------------------------------------------------------

def save_summary(summary, file_path):
    """Save execution summary as JSON."""

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4)

    logger.info("Summary saved: %s", file_path)


# ---------------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------------

def main():

    start_time = time.time()

    logger.info("========================================")
    logger.info("Starting web scraping ETL pipeline")
    logger.info("========================================")

    # -----------------------------------------------------
    # 1. SCRAPE BOOKS
    # -----------------------------------------------------

    logger.info("Starting Books to Scrape...")

    try:
        books = scrape_books()
    except Exception as error:
        logger.error("Books scraper failed: %s", error)
        books = []

    logger.info("Books scraped: %d", len(books))


    # -----------------------------------------------------
    # 2. SCRAPE QUOTES
    # -----------------------------------------------------

    logger.info("Starting Quotes to Scrape...")

    try:
        quotes = scrape_quotes()
    except Exception as error:
        logger.error("Quotes scraper failed: %s", error)
        quotes = []

    logger.info("Quotes scraped: %d", len(quotes))


    # -----------------------------------------------------
    # 3. COMBINE RAW DATA
    # -----------------------------------------------------

    raw_records = books + quotes

    logger.info(
        "Total raw records: %d",
        len(raw_records)
    )


    # -----------------------------------------------------
    # 4. CLEAN DATA
    # -----------------------------------------------------

    logger.info("Cleaning records...")

    cleaned_records = []

    for record in raw_records:

        try:
            cleaned_record = clean_record(record)

            cleaned_records.append(cleaned_record)

        except Exception as error:
            logger.warning(
                "Record cleaning failed: %s",
                error
            )


    logger.info(
        "Records after cleaning: %d",
        len(cleaned_records)
    )


    # -----------------------------------------------------
    # 5. VALIDATE DATA
    # -----------------------------------------------------

    logger.info("Validating records...")

    valid_records, rejected_records = validate_records(
        cleaned_records
    )

    logger.info(
        "Valid records: %d",
        len(valid_records)
    )

    logger.info(
        "Rejected records: %d",
        len(rejected_records)
    )


    # -----------------------------------------------------
    # 6. REMOVE DUPLICATES
    # -----------------------------------------------------

    logger.info("Checking for duplicates...")

    unique_records, duplicate_records = deduplicate_records(
        valid_records
    )

    logger.info(
        "Duplicate records: %d",
        len(duplicate_records)
    )

    logger.info(
        "Final unique records: %d",
        len(unique_records)
    )


    # -----------------------------------------------------
    # 7. SAVE FINAL DATASET
    # -----------------------------------------------------

    csv_path = OUTPUT_DIR / "final_dataset.csv"

    save_csv(
        unique_records,
        csv_path
    )


    # -----------------------------------------------------
    # 8. CREATE SUMMARY
    # -----------------------------------------------------

    execution_time = time.time() - start_time

    summary = {
        "execution_timestamp": datetime.now().isoformat(),

        "records_scraped": {
            "books": len(books),
            "quotes": len(quotes),
            "total": len(raw_records)
        },

        "records_after_cleaning": len(cleaned_records),

        "rejected_records": len(rejected_records),

        "duplicate_records": len(duplicate_records),

        "final_unique_records": len(unique_records),

        "execution_time_seconds": round(
            execution_time,
            2
        )
    }


    # -----------------------------------------------------
    # 9. SAVE SUMMARY JSON
    # -----------------------------------------------------

    summary_path = OUTPUT_DIR / "summary_report.json"

    save_summary(
        summary,
        summary_path
    )


    # -----------------------------------------------------
    # 10. FINISHED
    # -----------------------------------------------------

    logger.info("========================================")
    logger.info("ETL pipeline completed successfully")
    logger.info(
        "Execution time: %.2f seconds",
        execution_time
    )
    logger.info("========================================")


if __name__ == "__main__":
    main()