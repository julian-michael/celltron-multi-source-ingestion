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

# Remove the OUTPUT_DIR and OUTPUT_FILE constants - let the main script handle saving

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
        return None

    def fetch_newsapi_sources(self):
        """
        Fetch news sources from NewsAPI and return as a list.
        Does NOT save to file directly - returns data for main script to handle.
        """
        if not self.newsapi:
            print("❌ NewsAPI client not initialized")
            return []

        try:
            # Make API call with retry logic
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
                    "_source": "newsapi",  # Changed from "source" to "_source" to match main script
                    "_timestamp": datetime.utcnow().isoformat() + "Z",
                    "_id": f"newsapi_{source.get('id', 'unknown')}_{int(time.time())}"
                })

            print(f"✅ Retrieved {len(sources_list)} sources from NewsAPI")
            return sources_list

        except NewsAPIException as e:
            print(f"❌ NewsAPI error: {e}")
            return []
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return []

    # OPTIONAL: Keep a method for direct file saving if needed elsewhere
    def fetch_and_save_sources(self, output_file: str):
       
        sources = self.fetch_newsapi_sources()
        
        if not sources:
            return False
        
        try:
            # Create directory if it doesn't exist
            output_dir = os.path.dirname(output_file)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            
            with open(output_file, "w") as f:
                json.dump(sources, f, indent=2)
            
            print(f"✅ Saved {len(sources)} sources to {output_file}")
            return True
        except Exception as e:
            print(f"❌ Error saving to file: {e}")
            return False