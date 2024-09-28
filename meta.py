import requests
import json
import time

def run_meta_scraper():
    # Your Apify API token
    API_TOKEN = "apify_api_8Pi5yQoJm8JoBHCLPTD5ivdQF6K22e3gmBBr"

    # Base URL for Apify API
    BASE_URL = "https://api.apify.com/v2"

    # Headers for the API request
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }

    def fetch_data(url, method="GET", payload=None):
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code in [200, 201]:
            return response.json()
        else:
            print(f"Error fetching data from {url}. Status code: {response.status_code}")
            print(response.text)
            return None

    # Start a new run of the actor with crime-related hashtags
    print("Starting a new run of the Meta scraper...")
    start_url = f"{BASE_URL}/acts/apify~social-media-hashtag-research/runs"
    run_input = {
         "hashtags": [
            "Crime"
        ],
        "maxPerSocial": 50,  # Increased for more results
        "socials": [
            "facebook",
            "instagram"
        ]
    }

    new_run = fetch_data(start_url, method="POST", payload=run_input)

    if not new_run:
        print("Failed to start a new run.")
        return

    run_id = new_run['data']['id']
    print(f"New run started with ID: {run_id}")

    # Wait for the run to finish
    while True:
        status_url = f"{BASE_URL}/acts/apify~social-media-hashtag-research/runs/{run_id}"
        run_status = fetch_data(status_url)
        
        if run_status['data']['status'] == "SUCCEEDED":
            print("Run completed successfully.")
            break
        elif run_status['data']['status'] in ["FAILED", "ABORTED", "TIMED-OUT"]:
            print(f"Run failed with status: {run_status['data']['status']}")
            return
        else:
            print("Run still in progress. Waiting...")
            time.sleep(10)

    # Fetch the dataset items
    dataset_id = run_status['data']['defaultDatasetId']
    dataset_url = f"{BASE_URL}/datasets/{dataset_id}/items"

    print("Fetching dataset items...")
    dataset_items = fetch_data(dataset_url)

    if dataset_items:
        print(f"Fetched {len(dataset_items)} items from the dataset.")
        
        # Save output data to a file
        filename = "crime_hashtag_results.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(dataset_items, f, ensure_ascii=False, indent=2)
        print(f"\nOutput data saved to {filename}")

        # Print a sample of the results
        print("\nSample results:")
        for item in dataset_items[:5]:  # Print first 5 items
            print(f"Platform: {item.get('platform', 'N/A')}")
            print(f"Post URL: {item.get('postUrl', 'N/A')}")
            print(f"Text: {item.get('text', 'N/A')}")  # Full text content
            print(f"Hashtags: {', '.join(item.get('hashtags', []))}")
            print(f"Author: {item.get('authorUsername', 'N/A')}")
            print(f"Posted At: {item.get('postedAt', 'N/A')}")  # This is the creation date
            print(f"Likes: {item.get('likes', 'N/A')}")
            print(f"Comments: {item.get('comments', 'N/A')}")
            print(f"Shares: {item.get('shares', 'N/A')}")
            
            # Attempt to get geolocation data
            location = item.get('location', {})
            if location:
                print(f"Location: {location.get('name', 'N/A')}")
                print(f"Latitude: {location.get('latitude', 'N/A')}")
                print(f"Longitude: {location.get('longitude', 'N/A')}")
            else:
                print("Location: Not available")
            
            # Additional media information
            if item.get('videoUrl'):
                print(f"Video URL: {item['videoUrl']}")
            if item.get('imageUrl'):
                print(f"Image URL: {item['imageUrl']}")
            
            print("---")
    else:
        print("Failed to fetch dataset items.")

if __name__ == "__main__":
    run_meta_scraper()