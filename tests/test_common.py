# common.py
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional


class CommonUtils:
    @staticmethod
    def get_timestamp() -> str:
        """Get current UTC timestamp in ISO format"""
        return datetime.utcnow().isoformat() + "Z"
    
    @staticmethod
    def normalize_article(article: Dict[str, Any], source_type: str) -> Dict[str, Any]:
        """
        Normalize article structure to a common format
        Ensures all articles have the same basic structure
        """
        normalized = {
            "id": article.get("id", ""),
            "title": article.get("title", ""),
            "content": article.get("content", ""),
            "author": article.get("author", ""),
            "url": article.get("url", ""),
            "source": source_type,
            "published_at": article.get("published_at", ""),
            "fetched_at": CommonUtils.get_timestamp(),
            "metadata": {}
        }
        
        # Copy additional fields to metadata
        for key, value in article.items():
            if key not in normalized:
                normalized["metadata"][key] = value
        
        return normalized
    
    @staticmethod
    def save_to_json(data: List[Dict], output_path: str) -> bool:
        """Save data to JSON file with error handling"""
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Saved {len(data)} records to {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving JSON: {e}")
            return False
    
    @staticmethod
    def load_from_json(input_path: str) -> List[Dict]:
        """Load data from JSON file"""
        try:
            if not os.path.exists(input_path):
                return []
            
            with open(input_path, "r", encoding="utf-8") as f:
                return json.load(f)
                
        except Exception as e:
            print(f"❌ Error loading JSON: {e}")
            return []
    
    @staticmethod
    def merge_json_files(files: List[str], output_path: str) -> List[Dict]:
        """Merge multiple JSON files into one"""
        all_data = []
        
        for file_path in files:
            if os.path.exists(file_path):
                data = CommonUtils.load_from_json(file_path)
                all_data.extend(data)
                print(f"✓ Merged {len(data)} records from {os.path.basename(file_path)}")
        
        CommonUtils.save_to_json(all_data, output_path)
        return all_data


class ArticleAggregator:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.articles_file = os.path.join(output_dir, "articles.json")
        self.common = CommonUtils()
    
    def add_articles(self, articles: List[Dict], source_type: str) -> bool:
        """Add new articles to the main articles.json file"""
        # Normalize articles
        normalized_articles = [
            self.common.normalize_article(article, source_type)
            for article in articles
        ]
        
        # Load existing articles
        existing_articles = self.common.load_from_json(self.articles_file)
        
        # Merge and remove duplicates based on URL
        url_set = {article["url"] for article in existing_articles if article.get("url")}
        
        unique_new_articles = [
            article for article in normalized_articles 
            if article.get("url") not in url_set
        ]
        
        # Combine old and new articles
        all_articles = existing_articles + unique_new_articles
        
        # Save back to file
        return self.common.save_to_json(all_articles, self.articles_file)
    
    def get_articles(self) -> List[Dict]:
        """Get all articles from the main file"""
        return self.common.load_from_json(self.articles_file)
    
    def clear_articles(self) -> bool:
        """Clear all articles"""
        return self.common.save_to_json([], self.articles_file)