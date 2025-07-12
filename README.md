
# Research Paper Fetcher

A Python tool to fetch research papers from PubMed with pharmaceutical/biotech affiliations.

## Features

- Search PubMed using their full query syntax
- Filter papers to only those with authors from pharmaceutical/biotech companies
- Output results as CSV with relevant information
- Command-line interface with options for output file and debugging

## Installation

1. Install Poetry if you don't have it already:
   ```bash
   pip install poetry

2.Clone this repository:
bash

git clone https://github.com/keerthireddy36/backendresearchpapers
cd backendresearchpapers

3.Install dependencies:
bash

    poetry install

Usage
Basic usage
bash

poetry run get-papers-list "your search query"

Save to file
bash

poetry run get-papers-list "cancer treatment" -f results.csv

With debug output
bash

poetry run get-papers-list "cancer treatment" -d

With PubMed API key
bash

poetry run get-papers-list "cancer treatment" --api-key your-api-key

Command Line Options

text

usage: get-papers-list [-h] [-f FILE] [-d] [--max-results MAX_RESULTS] [--email EMAIL] [--api-key API_KEY] query

Fetch research papers from PubMed with pharmaceutical/biotech affiliations.

positional arguments:
  query                 PubMed search query

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Output CSV file path (default: print to stdout)
  -d, --debug           Enable debug output
  --max-results MAX_RESULTS
                        Maximum number of results to fetch (default: 100)
  --email EMAIL         Email address for PubMed API (default: your-email@example.com)
  --api-key API_KEY     PubMed API key (optional)

Code Organization

The code is organized into several modules:

    api_client.py: Handles communication with the PubMed API

    processor.py: Processes and filters the paper data

    models.py: Contains data models for papers and authors

    utils.py: Utility functions (if any)

    get_papers_list.py: Command-line interface

Dependencies

    Python 3.8+

    Requests (for HTTP requests)

    Python-dateutil (for date handling)

Development

To run tests:
bash

poetry run pytest

To check types:
bash

poetry run mypy .

To format code:
bash

poetry run black .

External Tools Used

    PubMed API: https://www.ncbi.nlm.nih.gov/books/NBK25497/

    Poetry: https://python-poetry.org/

    Requests library: https://requests.readthedocs.io/

text


## How to Use

1. Install the package with Poetry:
   ```bash
   poetry install

2. Run the command-line tool:
    ```bash

    poetry run get-papers-list "cancer AND treatment" -f output.csv

3. For better results, consider:

        Using a PubMed API key (register at https://www.ncbi.nlm.nih.gov/account/)

        Providing your email address with the --email option

Key Features

    PubMed API Integration: Uses the official PubMed API to fetch papers

    Affiliation Filtering: Identifies pharmaceutical/biotech affiliations using keyword matching

    CSV Output: Generates clean CSV output with all required fields

    Error Handling: Robust error handling for API failures and missing data

    Type Annotations: Fully typed Python code for better maintainability

    Modular Design: Separated into logical components for easy testing and extension

