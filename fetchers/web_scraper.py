import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class WebScraper:
    def __init__(self, delay=1.0, timeout=10):
        """
        Initialize the scraper with technical settings only.
        URLs are provided during the run phase.
        """
        self.delay = delay
        self.timeout = timeout
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/91.0.4472.124 Safari/537.36"
            )
        }

    @staticmethod
    def _timestamp():
        return datetime.utcnow().isoformat() + "Z"

    def scrape_single_url(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)

            if response.status_code in (403, 404):
                return {
                    "url": url,
                    "error": f"{response.status_code} Error",
                    "status": response.status_code,
                }

            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Remove noise
            for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
                tag.decompose()

            # Find a Title
            title_tag = (
                soup.find("h1")
                or soup.find("title")
                or soup.find("h2")
            )
            title = title_tag.get_text(strip=True) if title_tag else "No Title Found"

            # Clean content
            content = " ".join(
                soup.get_text(separator=" ", strip=True).split()
            )[:1000]

            return {
                "title": title,
                "content": content or "No readable content found",
                "source": "web scraping",
                "url": url,
                "fetched_at": self._timestamp(),
                "status": response.status_code,
            }

        except requests.exceptions.Timeout:
            return {"url": url, "error": "Timeout", "status": "timeout"}
        except requests.exceptions.ConnectionError:
            return {"url": url, "error": "Connection Error", "status": "conn_error"}
        except Exception as e:
            return {"url": url, "error": str(e), "status": "unknown_error"}

    def run_batch(self, urls):
        """Accepts a list of URLs, processes them, and returns the data."""
        if not urls:
            print("No URLs provided to run_batch")
            return []

        results = []
        print(f"Scraping {len(urls)} URLs...\n")

        for i, url in enumerate(urls, 1):
            print(f"[{i}/{len(urls)}] {url}")
            result = self.scrape_single_url(url)
            results.append(result)

            if "error" in result:
                print(f"  ✗ {result['error']}")
            else:
                print(f"  ✓ {result['title'][:50]}")

            if i < len(urls):
                time.sleep(self.delay)

        success = sum(1 for r in results if "error" not in r)
        print(f"\nCompleted: {success} success, {len(results) - success} failed\n")
        return results