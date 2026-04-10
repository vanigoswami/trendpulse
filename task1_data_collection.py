import os
import json
import time
import requests
from datetime import datetime

CATEGORIES = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}

def main():
    headers = {"User-Agent": "TrendPulse/1.0"}
    session = requests.Session()
    session.headers.update(headers)
    
    print("Fetching top story IDs...")
    try:
        response = session.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=15)
        response.raise_for_status()
        top_ids = response.json()[:500]
    except Exception as e:
        print(f"Failed to fetch top stories: {e}")
        return

    stories_cache = {}
    used_sids = set()
    collected_stories = []
    
    collected_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for category, keywords in CATEGORIES.items():
        time.sleep(2)  
        
        print(f"Collecting stories for category: {category}")
        category_count = 0
        
        for sid in top_ids:
            if category_count >= 25:
                break
                
            if sid in used_sids:
                continue
                
            if sid not in stories_cache:
                try:
                    item_resp = session.get(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json", timeout=10)
                    item_resp.raise_for_status()
                    stories_cache[sid] = item_resp.json()
                except Exception as e:
                    print(f"Failed to fetch story {sid}: {e}")
                    stories_cache[sid] = None
                    continue
            
            story_data = stories_cache[sid]
            
            if not story_data or "title" not in story_data:
                continue
                
            title_lower = story_data["title"].lower()
            
            match_found = False
            for kw in keywords:
                if kw.lower() in title_lower:
                    match_found = True
                    break
                    
            if match_found:
                extracted = {
                    "post_id": story_data.get("id"),
                    "title": story_data.get("title"),
                    "category": category,
                    "score": story_data.get("score"),
                    "num_comments": story_data.get("descendants"),
                    "author": story_data.get("by"),
                    "collected_at": collected_at
                }
                
                collected_stories.append(extracted)
                used_sids.add(sid)
                category_count += 1
                
    if not os.path.exists("data"):
        os.makedirs("data")
        
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"data/trends_{date_str}.json"
    
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(collected_stories, f, indent=4)
        print(f"Collected {len(collected_stories)} stories. Saved to {filename}")
    except Exception as e:
        print(f"Failed to save data: {e}")

if __name__ == "__main__":
    main()
