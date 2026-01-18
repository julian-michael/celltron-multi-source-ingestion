from newsapi import NewsApiClient
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")
newsapi = NewsApiClient(api_key=API_KEY)

# Get top headlines about India
try:
    articles = newsapi.get_top_headlines(q="Ai", language="en", page_size=5)
    
    if articles['status'] == 'ok':
        print(f"Found {articles['totalResults']} articles\n")
        
        for i, article in enumerate(articles['articles'], 1):
            print(f"{i}. {article['title']}")
            
            # Handle None content gracefully
            content = article.get('content', 'No content available')
            if content:
                # Truncate content if it's too long
                content = content[:200] + "..." if len(content) > 200 else content
                print(f"   {content}")
            else:
                print("   (Content not available)")
            
            print(f"   Source: {article['source']['name']}")
            print(f"   URL: {article['url']}")
            print("-" * 80)
    else:
        print(f"Error: {articles.get('message', 'Unknown error')}")

except Exception as e:
    print(f"An error occurred: {e}")