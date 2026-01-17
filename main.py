from fetchers.newsapi_fetcher import NewsAPIHandler
import os

def main():
    print("Starting news fetch...")

    handler = NewsAPIHandler(api_key=os.getenv("NEWS_API_KEY"))
    success = handler.fetch_newsapi_sources()

    if success:
        print("✓ News fetch completed successfully!")
    else:
        print("✗ News fetch failed")

if __name__ == "__main__":
    main()
