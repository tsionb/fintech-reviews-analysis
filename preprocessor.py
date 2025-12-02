import pandas as pd
import numpy as np
from datetime import datetime

def load_and_clean_data(input_file='bank_reviews_raw.csv', output_file='bank_reviews_clean.csv'):
    """Load, clean, and preprocess the scraped review data"""
    
    # Load the raw data
    print("Loading raw data...")
    df = pd.read_csv(input_file)
    print(f"Original data shape: {df.shape}")
    
    # Step 1: Remove duplicates
    print("1. Removing duplicate reviews...")
    initial_count = len(df)
    df = df.drop_duplicates(subset=['review_text'])
    duplicates_removed = initial_count - len(df)
    print(f"   Removed {duplicates_removed} duplicate reviews")
    
    # Step 2: Handle missing data
    print("2. Handling missing data...")
    missing_before = df.isnull().sum()
    
    # Remove rows where review text is missing
    df = df.dropna(subset=['review_text'])
    
    # Fill missing ratings with 0 (or you could use median)
    df['rating'] = df['rating'].fillna(0)
    
    # Fill missing dates with today's date
    df['date'] = df['date'].fillna(datetime.now().strftime('%Y-%m-%d'))
    
    missing_after = df.isnull().sum()
    print(f"   Missing values handled")
    
    # Step 3: Data validation and cleaning
    print("3. Validating and cleaning data...")
    
    # Ensure ratings are between 1-5
    invalid_ratings = df[~df['rating'].between(1, 5)]
    if not invalid_ratings.empty:
        print(f"   Found {len(invalid_ratings)} invalid ratings, setting to 0")
        df.loc[~df['rating'].between(1, 5), 'rating'] = 0
    
    # Clean review text - remove extra whitespace
    df['review_text'] = df['review_text'].str.strip()
    
    # Remove very short reviews (less than 3 characters)
    short_reviews = df[df['review_text'].str.len() < 3]
    if not short_reviews.empty:
        print(f"   Removing {len(short_reviews)} very short reviews")
        df = df[df['review_text'].str.len() >= 3]
    
    # Step 4: Final data quality check
    print("4. Final data quality check...")
    print(f"   Final data shape: {df.shape}")
    print(f"   Reviews per bank:")
    print(f"   {df['bank_name'].value_counts()}")
    
    # Calculate data quality metrics
    total_reviews = len(df)
    completeness = (1 - (df.isnull().sum().sum() / (len(df) * len(df.columns)))) * 100
    print(f"   Data completeness: {completeness:.2f}%")
    
    # Step 5: Save cleaned data
    print("5. Saving cleaned data...")
    df.to_csv(output_file, index=False)
    print(f"✓ Cleaned data saved to {output_file}")
    
    return df

def create_data_summary(df):
    """Create a summary of the cleaned dataset"""
    print("\n=== FINAL DATASET SUMMARY ===")
    print(f"Total reviews: {len(df)}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    
    print("\nReviews by bank:")
    bank_summary = df['bank_name'].value_counts()
    for bank, count in bank_summary.items():
        percentage = (count / len(df)) * 100
        print(f"  {bank}: {count} reviews ({percentage:.1f}%)")
    
    print("\nRating distribution:")
    rating_dist = df['rating'].value_counts().sort_index()
    for rating, count in rating_dist.items():
        percentage = (count / len(df)) * 100
        print(f"  {rating} stars: {count} reviews ({percentage:.1f}%)")
    
    # Check if we met the 400 reviews per bank requirement
    print("\n=== REQUIREMENT CHECK ===")
    for bank in df['bank_name'].unique():
        bank_count = len(df[df['bank_name'] == bank])
        status = "✓ PASS" if bank_count >= 400 else "✗ FAIL"
        print(f"  {bank}: {bank_count}/400 reviews {status}")

# Main execution
if __name__ == "__main__":
    print("Starting data preprocessing...")
    
    # Load and clean the data
    cleaned_df = load_and_clean_data()
    
    # Create summary report
    create_data_summary(cleaned_df)
    
    print("\n✅ Preprocessing completed successfully!")