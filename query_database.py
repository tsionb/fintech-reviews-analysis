import psycopg2
import pandas as pd

class DatabaseQuerier:
    def __init__(self, host='localhost', database='bank_reviews', 
                 user='postgres', password='031628'):
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
    
    def execute_query(self, query, params=None):
        """Execute a query and return results as DataFrame"""
        try:
            df = pd.read_sql_query(query, self.conn, params=params)
            return df
        except Exception as e:
            print(f"Query error: {e}")
            return pd.DataFrame()
    
    def get_basic_stats(self):
        """Get basic statistics about the data"""
        print("="*60)
        print("BASIC DATABASE STATISTICS")
        print("="*60)
        
        # Count total reviews
        query1 = "SELECT COUNT(*) as total_reviews FROM reviews;"
        total_reviews = self.execute_query(query1)
        print(f"Total reviews in database: {total_reviews['total_reviews'][0]}")
        
        # Reviews per bank
        query2 = """
            SELECT b.bank_name, COUNT(r.review_id) as review_count
            FROM banks b
            JOIN reviews r ON b.bank_id = r.bank_id
            GROUP BY b.bank_name
            ORDER BY review_count DESC;
        """
        reviews_per_bank = self.execute_query(query2)
        print("\nReviews per bank:")
        print(reviews_per_bank.to_string(index=False))
        
        # Average rating per bank
        query3 = """
            SELECT b.bank_name, 
                   ROUND(AVG(r.rating), 2) as avg_rating,
                   COUNT(r.review_id) as review_count
            FROM banks b
            JOIN reviews r ON b.bank_id = r.bank_id
            GROUP BY b.bank_name
            ORDER BY avg_rating DESC;
        """
        avg_ratings = self.execute_query(query3)
        print("\nAverage rating per bank:")
        print(avg_ratings.to_string(index=False))
        
        # Sentiment distribution
        query4 = """
            SELECT sentiment_label, COUNT(*) as count,
                   ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM reviews), 2) as percentage
            FROM reviews
            GROUP BY sentiment_label
            ORDER BY count DESC;
        """
        sentiment_dist = self.execute_query(query4)
        print("\nSentiment distribution:")
        print(sentiment_dist.to_string(index=False))
        
        # Rating distribution
        query5 = """
            SELECT rating, COUNT(*) as count,
                   ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM reviews), 2) as percentage
            FROM reviews
            GROUP BY rating
            ORDER BY rating;
        """
        rating_dist = self.execute_query(query5)
        print("\nRating distribution:")
        print(rating_dist.to_string(index=False))
    
    def get_advanced_queries(self):
        """Execute advanced queries for insights"""
        print("\n" + "="*60)
        print("ADVANCED QUERIES FOR INSIGHTS")
        print("="*60)
        
        # Query 1: Most common issues per bank
        query1 = """
            SELECT b.bank_name, r.sentiment_label, COUNT(*) as count
            FROM banks b
            JOIN reviews r ON b.bank_id = r.bank_id
            WHERE r.sentiment_label = 'negative'
            GROUP BY b.bank_name, r.sentiment_label
            ORDER BY count DESC;
        """
        common_issues = self.execute_query(query1)
        print("\n1. Negative reviews per bank:")
        print(common_issues.to_string(index=False))
        
        # Query 2: Monthly trend of reviews
        query2 = """
            SELECT DATE_TRUNC('month', review_date) as month,
                   COUNT(*) as review_count,
                   ROUND(AVG(rating), 2) as avg_rating
            FROM reviews
            WHERE review_date IS NOT NULL
            GROUP BY DATE_TRUNC('month', review_date)
            ORDER BY month DESC
            LIMIT 6;
        """
        monthly_trend = self.execute_query(query2)
        print("\n2. Monthly review trend (last 6 months):")
        print(monthly_trend.to_string(index=False))
        
        # Query 3: Reviews with highest and lowest sentiment scores
        query3_highest = """
            SELECT b.bank_name, r.review_text, r.sentiment_score, r.rating
            FROM reviews r
            JOIN banks b ON r.bank_id = b.bank_id
            ORDER BY r.sentiment_score DESC
            LIMIT 3;
        """
        query3_lowest = """
            SELECT b.bank_name, r.review_text, r.sentiment_score, r.rating
            FROM reviews r
            JOIN banks b ON r.bank_id = b.bank_id
            ORDER BY r.sentiment_score ASC
            LIMIT 3;
        """
        
        highest_sentiment = self.execute_query(query3_highest)
        lowest_sentiment = self.execute_query(query3_lowest)
        
        print("\n3. Reviews with highest sentiment scores:")
        print(highest_sentiment.to_string(index=False))
        
        print("\n4. Reviews with lowest sentiment scores:")
        print(lowest_sentiment.to_string(index=False))
    
    def close(self):
        """Close database connection"""
        self.conn.close()

def main():
    """Main function to run queries"""
    print("Running database queries for verification...")
    
    querier = DatabaseQuerier()
    
    try:
        # Run basic statistics
        querier.get_basic_stats()
        
        # Run advanced queries
        querier.get_advanced_queries()
        
        print("\n" + "="*60)
        print(" All queries executed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f" Error: {e}")
    
    finally:
        querier.close()

if __name__ == "__main__":
    main()