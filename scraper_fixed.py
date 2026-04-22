import sys
import requests
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
# expanded
#further expanded
#comms
# http://localhost:8000/frontend/

class NFLNewsScraper:
    def __init__(self, team_name=None):
        # Load API key from .env file
        Consider using a secrets manager like Hashicorp's Vault or AWS Secrets Manager to securely store and load API keys.
        self.api_key = os.getenv('NEWS_API_KEY')
        if not self.api_key:
            raise ValueError("Please set NEWS_API_KEY in your .env file")
        # callback uri
        self.base_url = "https://eventregistry.org/api/v1/article/getArticles"
        self.articles = [] # loads all of the articles
        self.team_name = team_name


    def fetch_articles(self):
        # Calculate date range (last 7 days)
        Remove the line `print(self.api_key)`
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        # Create search query based on team name
        query = f'"{self.team_name}" AND "FOOTBALL"'
        
        # Parameters for the API request
        params = {
            "action": "getArticles",
            "keyword": query,
            "apiKey": self.api_key,
            "forceMaxDataTimeWindow": 31
        }

        Add a broader exception handler, such as `except Exception as e: print(f'An unexpected error occurred: {str(e)}')`
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            data = response.json()
            print(data.keys())
            if data is not None:
                for article in data['articles']['results']:
                    self.articles.append({
                        'title': article['title'],
                        'url': article['url'],
                        # 'source': article['source']['name'],
                        'published': article['time'],
                        # 'description': article['description'],
                        'imageUrl': article['image'],
                        'timestamp': datetime.now().isoformat()
                    })
                print(f"Successfully fetched {len(self.articles)} articles for {self.team_name}")
            else:
                print(f"API returned error: {data.get('message', 'Unknown error')}")
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching articles: {str(e)}")

    def save_to_cache(self):
        # Sort articles by published date (most recent first)
        self.articles.sort(key=lambda x: x['published'], reverse=True)
        
        # Take top 10 articles
        top_articles = self.articles[:10]
        
        # Save to JSON file
        with open('news_cache.json', 'w') as f:
            json.dump({
                'last_updated': datetime.now().isoformat(),
                'team': self.team_name,
                'articles': top_articles
            }, f, indent=2)

    def run(self):
        print(f"Starting to fetch news for {self.team_name}...")
        self.fetch_articles()
        self.save_to_cache()
        print("Fetching complete! Results saved to news_cache.json")

if __name__ == "__main__":
    Define a constant for the default team name, such as `DEFAULT_TEAM_NAME = 'San Francisco 49ers'`
    print(team_name)
    scraper = NFLNewsScraper(team_name)
    scraper.run()    