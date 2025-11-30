from google_play_scraper import reviews_all, Sort
import pandas as pd
import time

def scrape_bank_reviews():
    # Bank apps with their actual Google Play Store IDs
    bank_apps = {
        'CBE': 'com.combanketh.mobilebanking',
        'BOA': 'com.boa.boaMobileBanking', 
        'DASHEN': 'com.dashen.dashensuperapp'
    }
    
    all_reviews = []
    
    for bank_name, app_id in bank_apps.items():
        print(f"Scraping reviews for {bank_name}...")
        
        try:
            # Scrape reviews with error handling
            reviews = reviews_all(
                app_id,
                lang='en',        # Language: English
                country='et',     # Country: Ethiopia
                sort=Sort.NEWEST, # Sort by newest first
                sleep_milliseconds=1000, # Be polite - wait 1 second between requests
            )
            
            # Process each review
            for review in reviews:
                all_reviews.append({
                    'review_text': review['content'],
                    'rating': review['score'],
                    'date': review['at'].strftime('%Y-%m-%d'), # Format as YYYY-MM-DD
                    'bank_name': bank_name,
                    'source': 'Google Play'
                })
                
            print(f"✓ Collected {len(reviews)} reviews for {bank_name}")
            
        except Exception as e:
            print(f"✗ Error scraping {bank_name}: {e}")
            continue
        
        # Small delay between banks to be respectful
        time.sleep(2)
    
    return all_reviews

def save_reviews_to_csv(reviews_list, filename='bank_reviews_raw.csv'):
    """Save reviews to CSV file"""
    df = pd.DataFrame(reviews_list)
    df.to_csv(filename, index=False)
    print(f"✓ Saved {len(df)} reviews to {filename}")
    return df

# Main execution
if __name__ == "__main__":
    print("Starting Google Play Store review scraping...")
    
    # Scrape reviews
    reviews_data = scrape_bank_reviews()
    
    # Save to CSV
    if reviews_data:
        df = save_reviews_to_csv(reviews_data)
        
        # Show summary
        print("\n=== SCRAPING SUMMARY ===")
        print(f"Total reviews collected: {len(df)}")
        print("\nReviews per bank:")
        print(df['bank_name'].value_counts())
        print("\nSample of data:")
        print(df.head())
    else:
        print("No reviews were collected. Please check the app IDs and try again.")