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
