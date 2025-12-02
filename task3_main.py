from create_schema import create_schema
from insert_data import main as insert_data_main
from query_database import main as query_database_main

def main():
    """Main function to run Task 3 complete pipeline"""
    print("="*60)
    print("TASK 3: POSTGRESQL DATABASE IMPLEMENTATION")
    print("="*60)
    
    # Step 1: Create schema
    print("\n STEP 1: Creating database schema...")
    create_schema()
    
    # Step 2: Insert data
    print("\n STEP 2: Inserting data into database...")
    insert_data_main()
    
    # Step 3: Run verification queries
    print("\n STEP 3: Running verification queries...")
    query_database_main()
    
    print("\n" + "="*60)
    print("COMPLETED SUCCESSFULLY!")
    print("="*60)

    

if __name__ == "__main__":
    main()