# Multi-Source Web Scraping & Data Consolidation

## 1. Project Overview

This project implements a Python ETL pipeline that collects data from two public practice websites:

- Books to Scrape
- Quotes to Scrape

The pipeline performs:

1. Web scraping
2. Pagination handling
3. Data cleaning and normalization
4. Data validation
5. Duplicate detection
6. Data consolidation
7. CSV and JSON output generation
8. Logging and error handling
9. Automated unit testing

The final dataset combines records from both sources into a common schema.

---

## 2. Data Sources

### Books to Scrape

URL:

https://books.toscrape.com/

The scraper extracts:

- Book title
- Price
- Rating
- Product URL
- Source
- Scraped timestamp

The scraper follows the website's pagination dynamically until there are no more pages.

### Quotes to Scrape

URL:

https://quotes.toscrape.com/

The scraper extracts:

- Quote text
- Author
- Tags
- Quote URL
- Source
- Scraped timestamp

The scraper also follows pagination dynamically.

Both websites are public practice websites and do not require authentication.

---

## 3. Technologies Used

- Python 3.10+
- Requests
- BeautifulSoup4
- lxml
- Pytest

Python standard libraries used include:

- csv
- json
- logging
- re
- hashlib
- datetime
- pathlib
- urllib.parse
- time

---

## 4. Project Structure

```text
scraping_assignment/
│
├── scrapers/
│   ├── __init__.py
│   ├── books_scraper.py
│   └── quotes_scraper.py
│
├── processing/
│   ├── __init__.py
│   ├── cleaning.py
│   ├── validation.py
│   └── deduplication.py
│
├── output/
│   ├── final_dataset.csv
│   └── summary_report.json
│
├── logs/
│   └── scraping.log
│
├── tests/
│   └── test_processing.py
│
├── main.py
├── requirements.txt
├── README.md
└── AI_USAGE.md

---

## 5. Installation and Setup

### Prerequisites

- Python 3.10 or higher
- Internet connection
- pip

### Create Virtual Environment

Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1

## 6. Install Dependencies

With the virtual environment activated, install the required packages:

```powershell
pip install -r requirements.txt