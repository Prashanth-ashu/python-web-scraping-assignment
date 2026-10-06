# AI Usage

## AI Tool Used

ChatGPT

## Purpose

AI was used as an assistance tool during development of the web scraping
ETL pipeline.

## Areas Where AI Assisted

- Project structure planning
- Python scraping logic
- Requests and BeautifulSoup usage
- Pagination handling
- Data cleaning functions
- Validation logic
- Duplicate detection approach
- Unit test creation
- README documentation

## Human Review and Corrections

All AI-generated suggestions were reviewed, tested, and modified where
necessary. The final implementation was executed locally and verified
using the generated CSV, JSON summary, logs, and automated tests.

## Testing

The project was tested by running:

python main.py

and:

python -m pytest -v

The automated test suite currently contains 7 tests, all of which pass.

## Incorrect or Modified AI Suggestions

Some AI-generated suggestions required modification during implementation.
The generated code was not used blindly. The implementation was reviewed against
the actual website HTML structure and assignment requirements.

Changes were made where necessary to ensure correct pagination, CSV output,
validation, duplicate detection, error handling, and compatibility with the
actual project structure.

## Verification

The final implementation was verified by:

- Running the complete ETL pipeline successfully
- Checking the generated CSV file
- Checking the generated JSON summary
- Reviewing the scraping logs
- Running all automated unit tests

All 7 automated tests passed successfully.