import os
import time
import json
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

from fetchers.newsapi_fetcher import NewsAPIHandler
from fetchers.web_scraper import WebScraper
from fetchers.csv_reader import CSVToJSON

# =========================
# Configuration
# =========================
BASE_DIR = "/home/julian/Vsocde/python_/celltron-multi-source-ingestion/multi-source-ingestion"
OUTPUT_DIR = f"{BASE_DIR}/output"
LOG_DIR = BASE_DIR

CONFIG = {
    "urls": [
        "https://news.ycombinator.com",
        "https://themeisle.com/blog/rss-feeds-list/#gref"
    ],
    "save_path": f"{OUTPUT_DIR}/scraped_data.json",
    "csv_dir": f"{BASE_DIR}/csv_data",
    "log_path": f"{LOG_DIR}/ingestion_logs.log"
}

# =========================
# Logging
# =========================
def setup_logger():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    logger = logging.getLogger("ingestion")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )

    file_handler = RotatingFileHandler(
        CONFIG["log_path"], maxBytes=5 * 1024 * 1024, backupCount=5
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

logger = setup_logger()

def log(level, msg, src="system"):
    getattr(logger, level)(f"[{src}] {msg}")

# =========================
# Utilities
# =========================
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def load_json():
    if not os.path.exists(CONFIG["save_path"]):
        return []
    try:
        with open(CONFIG["save_path"]) as f:
            return json.load(f)
    except Exception as e:
        log("error", f"Failed loading JSON: {e}")
        return []

def save_json(data):
    with open(CONFIG["save_path"], "w") as f:
        json.dump(data, f, indent=2)

def append_data(new_data, source):
    if not new_data:
        log("warning", "No data to append", source)
        return False

    timestamp = datetime.utcnow().isoformat()
    for item in new_data:
        item.update({
            "_timestamp": timestamp,
            "_source": source,
            "_id": f"{source}_{int(time.time())}_{abs(hash(str(item)))}"
        })

    data = load_json()
    data.extend(new_data)
    save_json(data)

    log("info", f"Added {len(new_data)} items (total {len(data)})", source)
    print(f"✓ {source}: {len(new_data)} items added")
    return True

# =========================
# Ingestion Handlers
# =========================
def fetch_newsapi():
    clear()
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        print("✗ NEWS_API_KEY not set")
        return False

    handler = NewsAPIHandler(api_key)
    data = handler.fetch_newsapi_sources()
    return append_data(data or [], "newsapi")

def scrape_web():
    clear()
    if not CONFIG["urls"]:
        print("✗ No websites configured")
        return False

    scraper = WebScraper(delay=1)
    data = scraper.run_batch(CONFIG["urls"])
    return append_data(data if isinstance(data, list) else [data], "web")

def read_csv():
    clear()
    if not os.path.isdir(CONFIG["csv_dir"]):
        print("✗ CSV directory not found")
        return False

    all_rows = []
    for file in os.listdir(CONFIG["csv_dir"]):
        if file.endswith(".csv"):
            path = os.path.join(CONFIG["csv_dir"], file)
            rows = CSVToJSON(path).convert() or []
            for r in rows:
                r["csv_file"] = file
            all_rows.extend(rows)

    return append_data(all_rows, "csv")

# =========================
# Dynamic Website Input
# =========================
def add_websites():
    clear()
    print("Add websites to scrape")
    print("Enter one URL per line")
    print("Type 'done' when finished\n")

    new_urls = []

    while True:
        url = input("URL: ").strip()
        if url.lower() == "done":
            break
        if not url.startswith("http"):
            print("Invalid URL (must start with http)")
            continue
        new_urls.append(url)

    if not new_urls:
        print("No websites added")
        return

    CONFIG["urls"].extend(new_urls)
    log("info", f"Added {len(new_urls)} websites", "web")
    print(f"✓ Added {len(new_urls)} websites")

# =========================
# Views
# =========================
def view_data():
    clear()
    data = load_json()
    if not data:
        print("No data available")
        return

    print(f"Total items: {len(data)}\n")
    sources = {}
    for i in data:
        sources[i["_source"]] = sources.get(i["_source"], 0) + 1

    for s, c in sources.items():
        print(f"{s}: {c}")

def clear_data():
    clear()
    confirm = input("Clear ALL data? (y/n): ").lower()
    if confirm == "y":
        save_json([])
        print("✓ Data cleared")

def view_logs():
    clear()
    if not os.path.exists(CONFIG["log_path"]):
        print("No logs found")
        return

    with open(CONFIG["log_path"]) as f:
        lines = f.readlines()[-20:]
    print("".join(lines))

# =========================
# Runner
# =========================
def run_all():
    for fn in (fetch_newsapi, read_csv, scrape_web):
        fn()
        time.sleep(1)

# =========================
# Menu
# =========================
MENU = {
    "1": ("Fetch NewsAPI", fetch_newsapi),
    "2": ("Read CSV", read_csv),
    "3": ("Scrape Web", scrape_web),
    "4": ("Run All", run_all),
    "5": ("View Data", view_data),
    "6": ("Clear Data", clear_data),
    "7": ("View Logs", view_logs),
    "8": ("Add Websites to Scrape", add_websites),
    "9": ("Exit", None)
}

def menu():
    while True:
        clear()
        print("Multi-Source Ingestion Manager\n")
        for k, v in MENU.items():
            print(f"{k}. {v[0]}")

        choice = input("\nChoose: ").strip()
        if choice == "9":
            break
        action = MENU.get(choice)
        if action:
            action[1]()
        else:
            print("Invalid choice")
        input("\nPress Enter...")

# =========================
# Entry
# =========================
if __name__ == "__main__":
    log("info", "System started")
    menu()
