import twitter
import meta

def main():
    print("Starting Twitter scraper...")
    twitter.run_twitter_scraper()
    
    print("\nStarting Meta scraper...")
    meta.run_meta_scraper()

if __name__ == "__main__":
    main()