import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
import numpy as np
from datetime import datetime

class DatabaseManager:
    def __init__(self, host='localhost', database='bank_reviews', 
                 user='postgres', password='031628'):
        """Initialize database connection"""
        self.connection_params = {
            'host': host,
            'database': database,
            'user': user,
            'password': password
        }
        self.conn = None
        self.cur = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(**self.connection_params)
            self.cur = self.conn.cursor()
            print(" Connected to database successfully!")
            return True
        except Exception as e:
            print(f" Connection failed: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        print("Database connection closed.")
    
    def insert_banks(self, banks_data):
        """Insert banks into database"""
        try:
            insert_query = """
                INSERT INTO banks (bank_name, app_name)
                VALUES (%s, %s)
                ON CONFLICT (bank_name) DO NOTHING
                RETURNING bank_id;
            """
            
            bank_ids = {}
            for bank_name, app_name in banks_data.items():
                self.cur.execute(insert_query, (bank_name, app_name))
                result = self.cur.fetchone()
                if result:
                    bank_ids[bank_name] = result[0]
                else:
                    # Bank already exists, get existing ID
                    self.cur.execute(
                        "SELECT bank_id FROM banks WHERE bank_name = %s",
                        (bank_name,)
                    )
                    bank_ids[bank_name] = self.cur.fetchone()[0]
            
            self.conn.commit()
            print(f" Inserted {len(bank_ids)} banks")
            return bank_ids
            
        except Exception as e:
            self.conn.rollback()
            print(f" Error inserting banks: {e}")
            return {}
    
    def prepare_review_data(self, df, bank_ids):
        """Prepare review data for insertion"""
        reviews_data = []
        
        for _, row in df.iterrows():
            # Get bank_id
            bank_id = bank_ids.get(row['bank_name'])
            
            if not bank_id:
                print(f"Warning: Bank '{row['bank_name']}' not found in database")
                continue
            
            # Handle missing values
            review_text = str(row['review_text']) if pd.notna(row['review_text']) else ''
            rating = int(row['rating']) if pd.notna(row['rating']) else 0
            sentiment_label = str(row['sentiment_label']) if 'sentiment_label' in df.columns else 'neutral'
            sentiment_score = float(row['sentiment_score']) if 'sentiment_score' in df.columns else 0.0
            
            # Handle date
            try:
                if pd.notna(row.get('date')):
                    review_date = pd.to_datetime(row['date']).date()
                else:
                    review_date = None
            except:
                review_date = None
            
            reviews_data.append((
                bank_id,
                review_text[:5000],  # Limit text length
                rating,
                review_date,
                sentiment_label,
                sentiment_score
            ))
        
        return reviews_data
    
    def insert_reviews(self, reviews_data, batch_size=1000):
        """Insert reviews in batches"""
        try:
            insert_query = """
                INSERT INTO reviews 
                (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score)
                VALUES (%s, %s, %s, %s, %s, %s);
            """
            
            total_reviews = len(reviews_data)
            inserted_count = 0
            
            # Insert in batches
            for i in range(0, total_reviews, batch_size):
                batch = reviews_data[i:i + batch_size]
                execute_batch(self.cur, insert_query, batch)
                inserted_count += len(batch)
                print(f"  Inserted batch: {inserted_count}/{total_reviews} reviews")
            
            self.conn.commit()
            print(f" Successfully inserted {inserted_count} reviews")
            
        except Exception as e:
            self.conn.rollback()
            print(f" Error inserting reviews: {e}")
    
    def verify_data(self):
        """Verify data was inserted correctly"""
        try:
            # Check counts
            self.cur.execute("SELECT COUNT(*) FROM banks;")
            bank_count = self.cur.fetchone()[0]
            
            self.cur.execute("SELECT COUNT(*) FROM reviews;")
            review_count = self.cur.fetchone()[0]
            
            # Check reviews per bank
            self.cur.execute("""
                SELECT b.bank_name, COUNT(r.review_id) as review_count
                FROM banks b
                LEFT JOIN reviews r ON b.bank_id = r.bank_id
                GROUP BY b.bank_name
                ORDER BY review_count DESC;
            """)
            
            bank_review_counts = self.cur.fetchall()
            
            print("\n" + "="*50)
            print("DATA VERIFICATION")
            print("="*50)
            print(f"Total banks: {bank_count}")
            print(f"Total reviews: {review_count}")
            print("\nReviews per bank:")
            for bank, count in bank_review_counts:
                print(f"  {bank}: {count} reviews")
            
            return bank_count, review_count
            
        except Exception as e:
            print(f" Error verifying data: {e}")
            return 0, 0

def main():
    """Main function to insert data into database"""
    print("Starting data insertion into PostgreSQL...")
    
    # Load cleaned data
    try:
        # Try to load data with sentiment first
        df = pd.read_csv('reviews_with_sentiment.csv')
        print(f" Loaded {len(df)} reviews with sentiment analysis")
    except FileNotFoundError:
        # Fall back to clean data if sentiment file doesn't exist
        try:
            df = pd.read_csv('bank_reviews_clean.csv')
            print(f" Loaded {len(df)} cleaned reviews")
        except FileNotFoundError:
            print(" No data files found. Run Task 1 and Task 2 first.")
            return
    
    # Define bank information
    banks_info = {
        'CBE': 'Commercial Bank of Ethiopia Mobile',
        'BOA': 'Bank of Abyssinia Mobile Banking',
        'DASHEN': 'Dashen Bank Mobile Banking'
    }
    
    # Initialize database manager
    db_manager = DatabaseManager()
    
    if not db_manager.connect():
        return
    
    try:
        # Step 1: Insert banks
        print("\n1. Inserting banks...")
        bank_ids = db_manager.insert_banks(banks_info)
        
        # Step 2: Prepare review data
        print("\n2. Preparing review data...")
        reviews_data = db_manager.prepare_review_data(df, bank_ids)
        
        # Step 3: Insert reviews
        print(f"\n3. Inserting {len(reviews_data)} reviews...")
        db_manager.insert_reviews(reviews_data)
        
        # Step 4: Verify data
        print("\n4. Verifying data...")
        db_manager.verify_data()
        
        print("\n Data insertion completed successfully!")
        
    except Exception as e:
        print(f" Error during data insertion: {e}")
    
    finally:
        db_manager.disconnect()

if __name__ == "__main__":
    main()