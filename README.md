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