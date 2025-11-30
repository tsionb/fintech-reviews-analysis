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