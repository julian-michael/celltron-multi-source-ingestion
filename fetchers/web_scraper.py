import requests
from bs4 import BeautifulSoup

def quick_scrape(url):
    try:
        # 1. Fetch the page
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # 2. Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 3. Clean up (Remove "noise" tags)
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        # 4. Extract Title and Text
        title = soup.find('h1').get_text(strip=True) if soup.find('h1') else soup.title.string
        
        # Get all text, separated by newlines, then clean up extra spacing
        lines = [line.strip() for line in soup.get_text(separator='\n').splitlines() if line.strip()]
        content = '\n'.join(lines)

        return {
            "title": title.strip() if title else "No Title",
            "content": content[:2000], # Return first 2000 chars
            "status": "Success"
        }

    except Exception as e:
        return {"status": "Error", "message": str(e)}

# --- Example Usage ---
if __name__ == "__main__":
    target_url = "https://example.com"
    data = quick_scrape(target_url)
    
    print(f"TITLE: {data.get('title')}")
    print(f"CONTENT:\n{data.get('content')}")