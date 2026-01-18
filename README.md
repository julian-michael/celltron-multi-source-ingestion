# celltron-multi-source-ingestion
# Multi-Source Data Ingestion System

**Celltron Intelligence – Take Home Assignment (Option A)**

---

## 1. Project Overview

This project is a **Python-based backend ingestion system** that collects article-style data from **multiple heterogeneous sources**, normalizes the data into a single format, and stores it in a JSON file.

The system is designed to demonstrate:

* Backend thinking
* Error handling
* Code modularity
* Testability
* AI-assisted development workflow

The application runs as a **terminal-based interactive program** (CLI).

---

## 2. Data Sources Implemented

The system ingests data from **three different sources**:

### 1. NewsAPI (REST API)

* Fetches news articles using an API key
* Handles API failures gracefully (timeouts, invalid keys, empty responses)

### 2. CSV Files (Local Data)

* Reads `.csv` files from a local directory
* Converts rows into normalized article objects
* Handles missing files and malformed rows

### 3. Websites (Web Scraping)

* Scrapes multiple websites for article-like data
* Supports dynamically adding new websites at runtime
* Handles request failures and HTML parsing issues

---

## 3. Key Features

* ✅ Unified JSON output format
* ✅ Modular fetchers (easy to add new sources)
* ✅ Graceful error handling (system never crashes)
* ✅ Logging with file rotation
* ✅ Terminal-based interactive menu
* ✅ Designed for AI-assisted development

---

## 4. Project Structure

```
multi-source-ingestion/
├── main.py
├── fetchers/
│   ├── newsapi_fetcher.py
│   ├── csv_reader.py
│   ├── web_scraper.py
│   └── common.py
├── csv_data/
│   └── sample.csv
├── output/
│   └── scraped_data.json
├── tests/
│   ├── test_newsapi.py
│   ├── test_csv.py
│   ├── test_scraper.py
│   └── test_main.py
├── requirements.txt
├── .env
├── .gitignore
└── DEVELOPMENT_PROCESS.md
```

---

## 5. Normalized Output Format

All data from every source is converted into the **same JSON structure**:

```json
{
  "title": "Article title",
  "content": "Article content or summary",
  "url": "https://example.com",
  "_source": "newsapi | csv | web",
  "_timestamp": "2025-01-17T12:30:45",
  "_id": "unique_identifier"
}
```

This ensures consistency regardless of where the data comes from.

---

## 6. How to Run the Project

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd multi-source-ingestion
```

---

### Step 2: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

---

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 4: Setup Environment Variables

Create a `.env` file:

```env
NEWS_API_KEY=your_newsapi_key_here
```

⚠️ **Important:**
`.env` is added to `.gitignore` to protect API keys.

---

### Step 5: Run the Application

```bash
python main.py
```

You will see an interactive terminal menu.

---

## 7. Terminal Menu Options

```
1. Fetch NewsAPI
2. Read CSV
3. Scrape Web
4. Run All
5. View Data
6. Clear Data
7. View Logs
8. Add Websites to Scrape
9. Exit
```

### Add Multiple Websites

Option **8** allows adding multiple websites dynamically without changing code.

---

## 8. Error Handling Strategy

The system is designed to **never crash entirely**.

Examples:

* If NewsAPI fails → logs error → continues
* If CSV directory is missing → skipped safely
* If a website is unreachable → scraper logs and moves on

All errors are logged to:

```
ingestion_logs.log
```

with automatic file rotation.

---

## 9. Logging

* Logs stored in a rotating log file
* Console shows warnings/errors only
* Each data source logs independently

This mirrors real-world backend logging practices.

---

## 10. Testing

Basic tests are provided using **pytest**.

To run tests:

```bash
pytest
```

Tests cover:

* Fetcher outputs
* Error handling scenarios
* Data normalization
* Main aggregation logic

Tests are intentionally simple but meaningful.

---

## 11. Extensibility (Reusability)

Adding a **new data source** requires:

1. Creating a new fetcher module
2. Returning normalized data
3. Registering it in `main.py`

No core logic changes required.

---

## 12. AI-Assisted Development

AI tools (ChatGPT) were used to:

* Generate initial code drafts
* Suggest error handling patterns
* Improve code readability

All AI output was **reviewed, modified, and validated manually**.
Design decisions and corrections are documented in `DEVELOPMENT_PROCESS.md`.

---

## 13. Conclusion

This project demonstrates:

* Backend system design
* Robust ingestion pipelines
* Error resilience
* Clean architecture
* Responsible AI-assisted development

The solution favors **clarity, reliability, and extensibility** over unnecessary complexity.

---

**End of Document**
