# Query API

This is an example API that exposes a sample dataset through a single generic HTTP API endpoint, capable of filtering, grouping, and sorting. The dataset represents performance metrics (impressions, clicks, installs, spend, revenue) for a given date, advertising channel, country, and operating system. The dataset is expected to be stored and processed in a relational database.

## Getting Started

### Prerequisites

- Python 3.x
- SQLite database

### Installation

Clone the repository:

   ```shell
    cd QueryApi
    pip install -r requirements.txt
   ```

### Usage

1. Start the API server:
````
uvicorn src.main:app --reload
````

2. API Endpoints:

- GET /get_metrics/: Retrieves performance metrics from the dataset based on specified filters, groupings, and sortings.

  - Query Parameters:
      - date_from (optional): Start date to filter the metrics (format: YYYY-MM-DD)
      - date_to (optional): End date to filter the metrics (format: YYYY-MM-DD).
      - channels (optional): Comma-separated list of advertising channels to filter.
      - countries (optional): Comma-separated list of countries to filter.
      - operating_systems (optional): Comma-separated list of operating systems to filter.
      - group_by (optional): Comma-separated list of columns which will use in group by clause
      - sort_by (optional): Comma-separated list of columns which will use in ordering
      - select_columns: Comma-separated list of columns to be shown. (Default *)
