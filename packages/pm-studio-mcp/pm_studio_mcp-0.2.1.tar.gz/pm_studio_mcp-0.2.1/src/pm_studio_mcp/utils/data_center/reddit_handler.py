from base_handler import BaseHandler
from datetime import datetime
from typing import List, Dict, Any

try:
    import praw
    import csv
    import os
    import datetime
    import requests
    from typing import List, Dict, Any, Optional
except ImportError:
    print("Please install required packages: pip install praw requests")

class RedditHandler(BaseHandler):
    """
    Handler for Reddit operations.
    This class is responsible for managing Reddit-related functionalities.
    """
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(RedditHandler, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, client_id: str, client_secret: str, subreddit_name: str):
        """
        Initialize the RedditHandler with the provided API key.
        
        :param api_key: The API key for Reddit.
        """
        if self._initialized:
            return
        
        # Create a user agent string
        user_agent = f"python:reddit-post-scraper:v1.0 (by u/{subreddit_name})"
        
        # Initialize Reddit API connection
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        self.subreddit_name = subreddit_name
        self._initialized = True

    def fetch_data(self, keywords: List[str], working_dir: str = "", post_limit: int = 100, time_filter: str = "month") -> Dict[str, Any]:
        """
        Fetch data from Reddit based on the provided query and date range."""
        try:
            subreddit = self.reddit.subreddit(self.subreddit_name)
                
            # Get posts from subreddit based on time filter
            if time_filter == "all":
                posts = subreddit.top(limit=post_limit)
            elif time_filter == "year":
                posts = subreddit.top("year", limit=post_limit)
            elif time_filter == "month":
                posts = subreddit.top("month", limit=post_limit)
            elif time_filter == "week":
                posts = subreddit.top("week", limit=post_limit)
            elif time_filter == "day":
                posts = subreddit.top("day", limit=post_limit)
            else:
                posts = subreddit.new(limit=post_limit)
                
            filtered_posts = []
            
            # Process each post
            for post in posts:
                # Check if any keyword is in title or selftext (case-insensitive)
                post_text = (post.title + " " + (post.selftext if post.selftext else "")).lower()
                
                # Check if any keyword matches
                if any(keyword.lower() in post_text for keyword in keywords):
                    post_data = {
                        "title": post.title,
                        "url": f"https://www.reddit.com{post.permalink}",
                        "author": str(post.author),
                        "score": post.score,
                        "num_comments": post.num_comments,
                        "created_utc": datetime.datetime.fromtimestamp(post.created_utc).strftime('%Y-%m-%d'),
                        "selftext": post.selftext[:500] + "..." if len(post.selftext) > 500 else post.selftext
                    }
                    filtered_posts.append(post_data)
            
            # Save the results to CSV
            output_file = f"reddit_{self.subreddit_name}_posts.csv"
            if working_dir:
                output_file = os.path.join(working_dir, output_file)
                
            if filtered_posts:
                with open(output_file, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=filtered_posts[0].keys())
                    writer.writeheader()
                    writer.writerows(filtered_posts)
                
                return {
                    "status": "success",
                    "posts_found": len(filtered_posts),
                    "output_file": os.path.abspath(output_file)
                }
            else:
                return {
                    "status": "success",
                    "posts_found": 0,
                    "message": "No posts found matching the criteria."
                }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error scraping Reddit: {str(e)}"
            }
        

if __name__ == "__main__":
    # Example usage
    reddit_handler = RedditHandler(
        client_id=os.environ.get('REDDIT_CLIENT_ID'),
        client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
        subreddit_name="chatgpt"
    )
    
    result = reddit_handler.fetch_data(
        keywords=["chatgpt"],
        working_dir=os.environ.get('WORKING_DIR'),
        post_limit=50,
        time_filter="all"
    )
    
    print(result)