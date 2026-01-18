# main.py
import os
import time
from common import ArticleAggregator
from fetchers.newsapi_fetcher import NewsAPIHandler
from fetchers.web_scraper import WebScraper
from fetchers.csv_reader import CSVToJSON


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def setup_aggregator():
    """Setup the article aggregator with output directory"""
    OUTPUT_DIR = "/home/julian/Vsocde/python_/celltron-multi-source-ingestion/multi-source-ingestion/output"
    return ArticleAggregator(OUTPUT_DIR)


def fetch_newsapi(aggregator):
    clear_screen()
    print("Fetching NewsAPI...\n")

    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        print("✗ NEWS_API_KEY not set")
        return False

    handler = NewsAPIHandler(api_key=api_key, aggregator=aggregator)
    
    # Fetch both sources and articles
    sources_success = handler.fetch_newsapi_sources()
    articles_success = handler.fetch_newsapi_articles()
    
    return sources_success or articles_success


def read_csv(aggregator):
    clear_screen()
    print("Reading CSV...\n")

    CSV_FILE = "/home/julian/Vsocde/python_/celltron-multi-source-ingestion/multi-source-ingestion/Sample_Articles.csv"
    
    try:
        converter = CSVToJSON(
            csv_file=CSV_FILE,
            aggregator=aggregator,
            required_columns=["title", "content"]  # Adjust as needed
        )
        
        return converter.process()
        
    except Exception as e:
        print(f"✗ CSV processing failed: {e}")
        return False


def scrape_web(aggregator):
    clear_screen()
    print("Scraping Websites...\n")

    scraper = WebScraper(aggregator=aggregator, delay=0.5)
    return scraper.run_batch()


def run_all():
    clear_screen()
    print("Running All Ingestions...\n")
    
    # Setup aggregator
    aggregator = setup_aggregator()
    
    # Get initial count
    initial_count = len(aggregator.get_articles())
    print(f"Initial articles in database: {initial_count}\n")
    
    # Run all fetchers
    results = []
    
    print("=" * 50)
    results.append(("NewsAPI", fetch_newsapi(aggregator)))
    time.sleep(1)
    
    print("\n" + "=" * 50)
    results.append(("CSV", read_csv(aggregator)))
    time.sleep(1)
    
    print("\n" + "=" * 50)
    results.append(("Web Scraping", scrape_web(aggregator)))
    
    # Final summary
    print("\n" + "=" * 50)
    final_count = len(aggregator.get_articles())
    new_articles = final_count - initial_count
    
    print(f"\n✓ All tasks completed")
    print(f"✓ Total articles in database: {final_count}")
    print(f"✓ New articles added: {new_articles}")
    
    # Show results summary
    print("\nResults Summary:")
    for source, success in results:
        status = "✓ Success" if success else "✗ Failed"
        print(f"  {source}: {status}")
    
    return aggregator


def auto_loop(interval_minutes=1):
    interval = interval_minutes * 60
    count = 0
    
    # Setup aggregator once
    aggregator = setup_aggregator()
    
    try:
        while True:
            count += 1
            clear_screen()
            print(f"\n=== Auto Run #{count} ===\n")
            
            initial_count = len(aggregator.get_articles())
            
            # Run all fetchers
            fetch_newsapi(aggregator)
            time.sleep(1)
            
            read_csv(aggregator)
            time.sleep(1)
            
            scrape_web(aggregator)
            
            # Show summary
            final_count = len(aggregator.get_articles())
            new_articles = final_count - initial_count
            
            print(f"\n✓ Run #{count} completed")
            print(f"✓ Total articles: {final_count}")
            print(f"✓ New articles this run: {new_articles}")
            
            print(f"\nNext run in {interval_minutes} minute(s)...")
            
            for i in range(interval, 0, -1):
                print(f"\rWaiting: {i}s", end="", flush=True)
                time.sleep(1)
                
    except KeyboardInterrupt:
        print("\n\nAuto loop stopped")
        total_articles = len(aggregator.get_articles())
        print(f"Total articles collected: {total_articles}")


def menu():
    aggregator = None
    
    while True:
        clear_screen()
        print("=" * 50)
        print(" Multi-Source Article Aggregator ")
        print("=" * 50)
        
        if aggregator:
            article_count = len(aggregator.get_articles())
            print(f"Articles in database: {article_count}\n")
        
        print("1. Fetch NewsAPI")
        print("2. Read CSV")
        print("3. Scrape Websites")
        print("4. Run All")
        print("5. Show All Articles")
        print("6. Clear Database")
        print("7. Auto Loop (1 min)")
        print("8. Exit")
        
        choice = input("\nChoose (1-8): ").strip()
        
        if choice == "1":
            aggregator = setup_aggregator()
            fetch_newsapi(aggregator)
        elif choice == "2":
            aggregator = setup_aggregator()
            read_csv(aggregator)
        elif choice == "3":
            aggregator = setup_aggregator()
            scrape_web(aggregator)
        elif choice == "4":
            aggregator = run_all()
        elif choice == "5":
            aggregator = setup_aggregator()
            articles = aggregator.get_articles()
            clear_screen()
            print(f"\nTotal Articles: {len(articles)}\n")
            for i, article in enumerate(articles[:10], 1):  # Show first 10
                print(f"{i}. [{article.get('source_type', 'unknown')}] {article.get('title', 'No title')[:60]}...")
            if len(articles) > 10:
                print(f"... and {len(articles) - 10} more")
        elif choice == "6":
            aggregator = setup_aggregator()
            if aggregator.clear_articles():
                print("Database cleared")
            time.sleep(1)
        elif choice == "7":
            auto_loop(1)
        elif choice == "8":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice")
            time.sleep(1)
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    menu()