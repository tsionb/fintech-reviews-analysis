
## Task 1: Data Collection and Preprocessing

### Methodology
1. **Data Source**: Google Play Store reviews for three Ethiopian banks
2. **Tools Used**: google-play-scraper library, pandas for data cleaning
3. **Banks Analyzed**: 
   - Commercial Bank of Ethiopia (CBE)
   - Bank of Abyssinia (BOA) 
   - Dashen Bank

### Files Created
- `scraper.py` - Web scraping script
- `preprocessor.py` - Data cleaning script  
- `bank_reviews_clean.csv` - Final cleaned dataset
- `requirements.txt` - Project dependencies

### Data Collection
- Collected 10,077 total reviews
- Minimum 400 reviews per bank achieved: YES
- Data includes: review text, rating, date, bank name, source

### How to Reproduce
1. Install dependencies: `pip install -r requirements.txt`
2. Run scraper: `python scraper.py`
3. Clean data: `python preprocessor.py`


## Task 2: Sentiment and Thematic Analysis

### Files Created:
- `sentiment_analysis.py` - VADER sentiment analysis implementation
- `thematic_analysis.py` - TF-IDF keyword extraction and theme clustering
- `analysis_utils.py` - Helper functions for insights generation
- `run_analysis.py` - Complete analysis pipeline

### Methodology:
1. **Sentiment Analysis**: Used VADER sentiment analyzer optimized for social media text
2. **Thematic Analysis**: TF-IDF for keyword extraction + manual theme clustering
3. **Visualization**: Automated plot generation for sentiment distribution and keywords

### How to Run:
1. Ensure `bank_reviews_clean.csv` exists (from Task 1)
2. Install dependencies: `pip install -r requirements.txt`
3. Run analysis: `python run_analysis.py`

### Outputs Generated:
- `reviews_with_sentiment.csv` - Reviews with sentiment labels and scores
- `sentiment_analysis.png` - Sentiment distribution visualization
- `keyword_analysis.png` - Top keywords by bank visualization
# Fintech App Reviews Analysis


## Task 3: PostgreSQL Database Implementation

### Objective
Design and implement a relational database in PostgreSQL to store cleaned review data, simulating real-world data engineering workflows.

### Implementation
- **Database**: PostgreSQL with `bank_reviews` database
- **Tables**: 
  - `banks` - Bank information (bank_id, bank_name, app_name)
  - `reviews` - User reviews with sentiment analysis (review_id, bank_id, review_text, rating, sentiment_label, etc.)
- **Data Insertion**: Inserted 10,077+ reviews from Task 1 & 2
- **Verification**: SQL queries to verify data integrity and generate insights

### Key Files
- `database_schema.sql` - Database schema definition
- `create_schema.py` - Python script to create tables
- `insert_data.py` - Data insertion script
- `query_database.py` - Verification and analysis queries
- `task3_main.py` - Main execution script
- `DATABASE_README.md` - Database setup documentation

### Setup Instructions
1. Install PostgreSQL from [postgresql.org](https://www.postgresql.org/download/)
2. Create database: `CREATE DATABASE bank_reviews;`
3. Run: `python task3_main.py`

### Results
-  Database schema created successfully
-  10,077+ reviews inserted into PostgreSQL
-  Data integrity verified with SQL queries
-  All KPIs met: Working database with >1,000 review entries

## Task 4: Insights and Recommendations

### Objective
Derive actionable insights from sentiment and thematic analysis, create compelling visualizations, and provide recommendations for app improvement.

### Analysis Performed
1. **Insights Generation**:
   - Identified satisfaction drivers (strengths) for each bank
   - Identified pain points (weaknesses) for each bank
   - Bank comparison across multiple dimensions

2. **Visualizations Created**:
   - Sentiment trends over time
   - Rating distribution by bank
   - Keyword analysis word clouds
   - Theme analysis charts
   - Interactive comparison dashboard

3. **Ethics Analysis**:
   - Analyzed potential review biases
   - Provided mitigation recommendations
   - Addressed ethical considerations

### Key Files
- `insights_analysis.py` - Comprehensive insights generation
- `advanced_visualizations.py` - Professional visualization creation
- `ethics_analysis.py` - Bias and ethics analysis
- `generate_final_report.py` - Final report compilation

### Key Findings
- **CBE**: Strongest performance with highest average rating
- **BOA**: Most room for improvement in app performance
- **DASHEN**: Balanced performance with specific pain points

### Recommendations
1. **Performance Optimization**: All banks should focus on app loading times
2. **Reliability Improvements**: Address app crashes and error handling
3. **User Experience**: Enhance UI/UX design and navigation
4. **Security**: Implement biometric authentication
5. **Customer Support**: Improve response times and support channels

### Results
-  Generated comprehensive insights report
-  Created 3+ professional visualizations
-  Performed ethics analysis
-  Delivered actionable recommendations
-  All KPIs met: 2+ drivers/pain points per bank with evidence
