import os
import time

from fetchers.newsapi_fetcher import NewsAPIHandler
from fetchers.web_scraper import WebScraper
from fetchers.csv_reader import csv_to_json


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def fetch_newsapi():
    clear_screen()
    print("Fetching NewsAPI...\n")

    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        print("✗ NEWS_API_KEY not set")
        return

    handler = NewsAPIHandler(api_key=api_key)
    print("✓ Success" if handler.fetch_newsapi_sources() else "✗ Failed")


def read_csv():
    clear_screen()
    print("Reading CSV...\n")

    try:
        csv_to_json()
        print("✓ CSV converted to JSON")
    except Exception as e:
        print(f"✗ CSV failed: {e}")


def scrape_web():
    clear_screen()
    print("Scraping Websites...\n")

    scraper = WebScraper(delay=0.5)
    urls = scraper.default_urls if hasattr(scraper, "default_urls") else []

    data = scraper.run_batch(urls)
    print("✓ Scraping complete" if scraper.save() else "✗ Save failed")


def run_all():
    clear_screen()
    print("Running All Ingestions...\n")

    fetch_newsapi()
    time.sleep(1)

    read_csv()
    time.sleep(1)

    scrape_web()

    print("\n✓ All tasks completed")


def auto_loop(interval_minutes=1):
    interval = interval_minutes * 60
    count = 0

    try:
        while True:
            count += 1
            print(f"\n=== Auto Run #{count} ===\n")
            run_all()
            print(f"\nNext run in {interval_minutes} minute(s)...")

            for i in range(interval, 0, -1):
                print(f"\rWaiting: {i}s", end="", flush=True)
                time.sleep(1)

            clear_screen()

    except KeyboardInterrupt:
        print("\nAuto loop stopped")


def menu():
    while True:
        clear_screen()
        print("=" * 40)
        print(" Multi-Source Ingestion ")
        print("=" * 40)
        print("1. Fetch NewsAPI")
        print("2. Read CSV")
        print("3. Scrape Websites")
        print("4. Run All")
        print("5. Auto Loop (1 min)")
        print("6. Exit")

        choice = input("\nChoose (1-6): ").strip()

        if choice == "1":
            fetch_newsapi()
        elif choice == "2":
            read_csv()
        elif choice == "3":
            scrape_web()
        elif choice == "4":
            run_all()
        elif choice == "5":
            auto_loop(1)
        elif choice == "6":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice")
            time.sleep(1)

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    menu()
