from apify_client import ApifyClient
import json
from datetime import datetime

def run_twitter_scraper():
    # Initialize the ApifyClient with your API token
    client = ApifyClient("apify_api_8Pi5yQoJm8JoBHCLPTD5ivdQF6K22e3gmBBr")

    # Prepare the Actor input
    run_input = {
        "customMapFunction": "(object) => { return {...object} }",
        "end": "2024-09-28",  # Updated to current date
        "geotaggedNear": "india",
        "includeSearchTerms": False,
        "maxItems": 100,  # Increased for more results
        "onlyImage": False,
        "onlyQuote": False,
        "onlyTwitterBlue": False,
        "onlyVerifiedUsers": False,
        "onlyVideo": False,
        "searchTerms": [
            "crime",
            "kill"
        ],
        "sort": "Latest",
        "start": "2024-01-01",  # Updated to more recent date
        "tweetLanguage": "en",
        "withinRadius": "15km"
    }

    try:
        # Run the Actor and wait for it to finish
        run = client.actor("apidojo/tweet-scraper").call(run_input=run_input)

        print(f"Twitter Scraper Run ID: {run['id']}")
        print(f"Twitter Scraper Run Status: {run['status']}")

        if run['status'] == 'FAILED':
            error_message = client.run(run['id']).get().get('meta', {}).get('errorMessage', 'Unknown error')
            print(f"Error message: {error_message}")
            return

        # Prepare a list to store the tweet data
        tweets_data = []

        # Fetch Actor results from the run's dataset
        dataset_items = client.dataset(run["defaultDatasetId"]).list_items().items
        print(f"Number of items fetched: {len(dataset_items)}")

        for item in dataset_items:
            tweet = {
                "content": item.get('full_text', 'N/A'),
                "author": item.get('user', {}).get('screen_name', 'N/A'),
                "created_at": item.get('created_at', 'N/A'),
                "location": item.get('user', {}).get('location', 'Not specified'),
                "image_url": item.get('entities', {}).get('media', [{}])[0].get('media_url', None),
                "retweet_count": item.get('retweet_count', 'N/A'),
                "favorite_count": item.get('favorite_count', 'N/A'),
                "hashtags": [hashtag['text'] for hashtag in item.get('entities', {}).get('hashtags', [])],
                "mentions": [mention['screen_name'] for mention in item.get('entities', {}).get('user_mentions', [])],
                "tweet_url": f"https://twitter.com/{item.get('user', {}).get('screen_name', 'user')}/status/{item.get('id_str', 'id')}"
            }
            tweets_data.append(tweet)

        # Generate a filename with the current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"crime_tweets_{timestamp}.json"

        # Save the data to a JSON file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(tweets_data, f, ensure_ascii=False, indent=4)

        print(f"Twitter data has been saved to {filename}")

        # Print a sample of the data (first 5 tweets)
        print("\nSample of collected tweets:")
        for tweet in tweets_data[:5]:
            print(f"Content: {tweet['content']}")
            print(f"Author: {tweet['author']}")
            print(f"Created at: {tweet['created_at']}")
            print(f"Location: {tweet['location']}")
            print(f"Image URL: {tweet['image_url']}")
            print(f"Tweet URL: {tweet['tweet_url']}")
            print("---")

    except Exception as e:
        print(f"An error occurred in Twitter scraper: {str(e)}")

if __name__ == "__main__":
    run_twitter_scraper()