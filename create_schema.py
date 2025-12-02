import psycopg2
from psycopg2 import sql

def create_schema():
    """Create database tables and schema"""
    try:
        # Connect to database
        conn = psycopg2.connect(
            host="localhost",
            database="bank_reviews",
            user="postgres",
            password="031628"  
        )
        
        cur = conn.cursor()
        
        print("Creating database schema...")
        
        # Read and execute schema SQL
        with open('database_schema.sql', 'r') as f:
            schema_sql = f.read()
        
        cur.execute(schema_sql)
        conn.commit()
        
        print(" Database schema created successfully!")
        
        # Verify tables were created
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        tables = cur.fetchall()
        print(f"\nTables created: {[table[0] for table in tables]}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f" Error creating schema: {e}")

if __name__ == "__main__":
    create_schema()