import requests
import time
import os
import json
from datetime import datetime

# Base URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Header (important as per instructions)
HEADERS = {"User-Agent": "TrendPulse/1.0"}

# Categories with keywords
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# Max stories per category
MAX_PER_CATEGORY = 25


def fetch_top_story_ids():
    """Fetch top story IDs from HackerNews"""
    try:
        response = requests.get(TOP_STORIES_URL, headers=HEADERS)
        response.raise_for_status()
        return response.json()[:500]  # First 500 IDs
    except Exception as e:
        print(f"Error fetching top stories: {e}")
        return []


def fetch_story(story_id):
    """Fetch a single story's details"""
    try:
        response = requests.get(ITEM_URL.format(story_id), headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching story {story_id}: {e}")
        return None


def categorize_title(title):
    """Assign category based on keywords"""
    title_lower = title.lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category

    return None  # Ignore if no category matches


def main():
    # Step 1: Get story IDs
    story_ids = fetch_top_story_ids()

    # Dictionary to track counts per category
    category_counts = {cat: 0 for cat in CATEGORIES}

    collected_stories = []

    # Current timestamp
    collected_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Loop category-wise (IMPORTANT for sleep condition)
    for category in CATEGORIES:
        print(f"Collecting {category} stories...")

        for story_id in story_ids:
            # Stop if category limit reached
            if category_counts[category] >= MAX_PER_CATEGORY:
                break

            story = fetch_story(story_id)

            if not story or "title" not in story:
                continue

            # Check if story belongs to this category
            detected_category = categorize_title(story["title"])

            if detected_category == category:
                data = {
                    "post_id": story.get("id"),
                    "title": story.get("title"),
                    "category": category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by"),
                    "collected_at": collected_time
                }

                collected_stories.append(data)
                category_counts[category] += 1

        # Sleep AFTER finishing one category
        time.sleep(2)

    # Step 3: Save JSON
    os.makedirs("data", exist_ok=True)

    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected_stories, f, indent=4)

    print(f"Collected {len(collected_stories)} stories. Saved to {filename}")


if __name__ == "__main__":
    main() 
    