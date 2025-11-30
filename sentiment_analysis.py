import pandas as pd
import numpy as np
from textblob import TextBlob
from vadersentiment import SentimentIntensityAnalyzer
import spacy
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

class SentimentAnalyzer:
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
    
    def analyze_with_textblob(self, text):
        """Analyze sentiment using TextBlob (rule-based)"""
        analysis = TextBlob(str(text))
        polarity = analysis.sentiment.polarity
        
        if polarity > 0.1:
            return 'positive', polarity
        elif polarity < -0.1:
            return 'negative', polarity
        else:
            return 'neutral', polarity
    
    def analyze_with_vader(self, text):
        """Analyze sentiment using VADER (specifically for social media text)"""
        scores = self.vader_analyzer.polarity_scores(str(text))
        
        if scores['compound'] >= 0.05:
            return 'positive', scores['compound']
        elif scores['compound'] <= -0.05:
            return 'negative', scores['compound']
        else:
            return 'neutral', scores['compound']
    
    def analyze_reviews(self, df, method='vader'):
        """Analyze sentiment for all reviews"""
        print(f"Analyzing sentiment using {method}...")
        
        sentiments = []
        scores = []
        
        for review in df['review_text']:
            if method == 'vader':
                sentiment, score = self.analyze_with_vader(review)
            else:
                sentiment, score = self.analyze_with_textblob(review)
            
            sentiments.append(sentiment)
            scores.append(score)
        
        df['sentiment_label'] = sentiments
        df['sentiment_score'] = scores
        
        return df
    
    def compare_methods(self, df, sample_size=100):
        """Compare TextBlob vs VADER on a sample"""
        sample_reviews = df['review_text'].sample(sample_size, random_state=42)
        
        comparison = []
        for review in sample_reviews:
            vader_sentiment, vader_score = self.analyze_with_vader(review)
            textblob_sentiment, textblob_score = self.analyze_with_textblob(review)
            
            comparison.append({
                'review': review[:100] + '...' if len(review) > 100 else review,
                'vader_sentiment': vader_sentiment,
                'vader_score': vader_score,
                'textblob_sentiment': textblob_sentiment,
                'textblob_score': textblob_score,
                'agreement': vader_sentiment == textblob_sentiment
            })
        
        agreement_rate = sum([1 for comp in comparison if comp['agreement']]) / len(comparison)
        print(f"Sentiment method agreement: {agreement_rate:.1%}")
        
        return pd.DataFrame(comparison)

def load_data():
    """Load the cleaned review data"""
    try:
        df = pd.read_csv('bank_reviews_clean.csv')
        print(f"Loaded {len(df)} reviews")
        return df
    except FileNotFoundError:
        print("Error: bank_reviews_clean.csv not found. Run Task 1 first.")
        return None

def analyze_sentiment_by_bank(df):
    """Analyze sentiment distribution by bank"""
    print("\n=== SENTIMENT ANALYSIS BY BANK ===")
    
    # Overall sentiment distribution
    overall_sentiment = df['sentiment_label'].value_counts()
    print("Overall sentiment distribution:")
    for sentiment, count in overall_sentiment.items():
        percentage = (count / len(df)) * 100
        print(f"  {sentiment}: {count} ({percentage:.1f}%)")
    
    # Sentiment by bank
    sentiment_by_bank = pd.crosstab(df['bank_name'], df['sentiment_label'], normalize='index') * 100
    print("\nSentiment distribution by bank (%):")
    print(sentiment_by_bank.round(1))
    
    # Average sentiment score by bank
    avg_sentiment_by_bank = df.groupby('bank_name')['sentiment_score'].mean()
    print("\nAverage sentiment score by bank:")
    for bank, score in avg_sentiment_by_bank.items():
        print(f"  {bank}: {score:.3f}")
    
    return sentiment_by_bank

def analyze_sentiment_by_rating(df):
    """Analyze how sentiment correlates with star ratings"""
    print("\n=== SENTIMENT BY RATING ===")
    
    # Create a cross-tab of rating vs sentiment
    rating_sentiment = pd.crosstab(df['rating'], df['sentiment_label'])
    print("Rating vs Sentiment distribution:")
    print(rating_sentiment)
    
    # Calculate average sentiment score by rating
    avg_sentiment_by_rating = df.groupby('rating')['sentiment_score'].mean()
    print("\nAverage sentiment score by rating:")
    for rating, score in avg_sentiment_by_rating.items():
        print(f"  {rating} stars: {score:.3f}")
    
    return rating_sentiment

def create_sentiment_visualizations(df, sentiment_by_bank):
    """Create visualizations for sentiment analysis"""
    print("Creating sentiment visualizations...")
    
    # Set up the plotting style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Plot 1: Sentiment distribution by bank
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    sentiment_counts = pd.crosstab(df['bank_name'], df['sentiment_label'])
    sentiment_counts.plot(kind='bar', stacked=True, ax=plt.gca())
    plt.title('Sentiment Distribution by Bank')
    plt.xlabel('Bank')
    plt.ylabel('Number of Reviews')
    plt.legend(title='Sentiment')
    plt.xticks(rotation=45)
    
    # Plot 2: Average sentiment score by bank
    plt.subplot(1, 2, 2)
    avg_scores = df.groupby('bank_name')['sentiment_score'].mean().sort_values()
    colors = ['red' if score < 0 else 'green' if score > 0.1 else 'gray' for score in avg_scores]
    plt.bar(avg_scores.index, avg_scores.values, color=colors, alpha=0.7)
    plt.title('Average Sentiment Score by Bank')
    plt.xlabel('Bank')
    plt.ylabel('Average Sentiment Score')
    plt.xticks(rotation=45)
    
    # Add value labels on bars
    for i, v in enumerate(avg_scores.values):
        plt.text(i, v, f'{v:.3f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('sentiment_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Plot 3: Sentiment vs Rating
    plt.figure(figsize=(10, 6))
    sentiment_by_rating = df.groupby(['rating', 'sentiment_label']).size().unstack()
    sentiment_by_rating.plot(kind='bar', stacked=True)
    plt.title('Sentiment Distribution by Star Rating')
    plt.xlabel('Star Rating')
    plt.ylabel('Number of Reviews')
    plt.legend(title='Sentiment')
    plt.tight_layout()
    plt.savefig('sentiment_vs_rating.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """Main execution function"""
    print("Starting Sentiment Analysis...")
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Initialize analyzer
    analyzer = SentimentAnalyzer()
    
    # Compare methods on a sample
    print("Comparing sentiment analysis methods...")
    comparison_df = analyzer.compare_methods(df, sample_size=200)
    
    # Use VADER for full analysis (better for social media/text)
    df = analyzer.analyze_reviews(df, method='vader')
    
    # Analyze by bank and rating
    sentiment_by_bank = analyze_sentiment_by_bank(df)
    rating_sentiment = analyze_sentiment_by_rating(df)
    
    # Create visualizations
    create_sentiment_visualizations(df, sentiment_by_bank)
    
    # Save results
    df.to_csv('reviews_with_sentiment.csv', index=False)
    print(f"\n✅ Sentiment analysis completed! Saved to 'reviews_with_sentiment.csv'")
    
    # Print key insights
    print("\n=== KEY INSIGHTS ===")
    most_positive_bank = df.groupby('bank_name')['sentiment_score'].mean().idxmax()
    most_negative_bank = df.groupby('bank_name')['sentiment_score'].mean().idxmin()
    
    print(f"Most positive bank: {most_positive_bank}")
    print(f"Most negative bank: {most_negative_bank}")
    
    # Sentiment accuracy check (compare with ratings)
    positive_reviews_low_rating = len(df[(df['sentiment_label'] == 'positive') & (df['rating'] <= 2)])
    negative_reviews_high_rating = len(df[(df['sentiment_label'] == 'negative') & (df['rating'] >= 4)])
    
    print(f"Potential mismatches: {positive_reviews_low_rating} positive reviews with low ratings")
    print(f"Potential mismatches: {negative_reviews_high_rating} negative reviews with high ratings")

if __name__ == "__main__":
    main()