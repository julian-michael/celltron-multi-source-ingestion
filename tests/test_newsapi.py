from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException
import json
from datetime import datetime
import os
from dotenv import load_dotenv
import requests
import time
import sys
# Load env variables
load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")
TIMEOUT_SECONDS = 30
MAX_RETRIES = 3


OUTPUT_DIR = "/home/julian/Vsocde/python_/celltron-multi-source-ingestion/multi-source-ingestion/output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "news_sources.json")

class NewsAPIHandler:
    def __init__(self, api_key: str):
        if not api_key:
            print("❌ Missing NewsAPI key")
            self.newsapi = None
            return

        self.newsapi = NewsApiClient(api_key=api_key)

    def _make_api_call_with_retry(self, api_call, *args, **kwargs):
        for attempt in range(MAX_RETRIES):
            try:
                return api_call(*args, **kwargs)

            except requests.exceptions.Timeout:
                print(f"⚠️ Timeout (attempt {attempt + 1}/{MAX_RETRIES})")
                time.sleep(2 ** attempt)

            except requests.exceptions.ConnectionError as e:
                print(f"⚠️ Network error: {e}")
                time.sleep(2 ** attempt)

            except Exception as e:
                print(f"❌ Request error: {e}")
                break

        return None  # 👈 fail-soft

    def fetch_newsapi_sources(self):
        if not self.newsapi:
            return []

        os.makedirs(OUTPUT_DIR, exist_ok=True)

        try:
            response = self._make_api_call_with_retry(self.newsapi.get_sources)

            if not response or "sources" not in response:
                print("⚠️ No sources returned from NewsAPI")
                return []

            sources_list = []

            for source in response["sources"]:
                sources_list.append({
                    "id": source.get("id"),
                    "name": source.get("name"),
                    "description": source.get("description"),
                    "url": source.get("url"),
                    "category": source.get("category"),
                    "language": source.get("language"),
                    "country": source.get("country"),
                    "source": "newsapi",
                    "fetched_at": datetime.utcnow().isoformat() + "Z"
                })

            with open(OUTPUT_FILE, "w") as f:
                json.dump(sources_list, f, indent=2)

            print(f"✅ Saved {len(sources_list)} sources")
            return sources_list

        except NewsAPIException as e:
            print(f"❌ NewsAPI error: {e}")
            return []

        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return []

       




