# Database Setup Guide

## PostgreSQL Database: `bank_reviews`

### Tables:
1. `banks` - Stores bank information
   - bank_id (PK), bank_name, app_name, created_at

2. `reviews` - Stores user reviews
   - review_id (PK), bank_id (FK), review_text, rating, 
     review_date, sentiment_label, sentiment_score, source, created_at

### Setup Instructions:

1. **Install PostgreSQL** from https://www.postgresql.org/download/

2. **Create database**:
   ```sql
   CREATE DATABASE bank_reviews;