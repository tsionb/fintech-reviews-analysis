from sentiment_analysis import main as run_sentiment_analysis
from thematic_analysis import main as run_thematic_analysis
import pandas as pd
from analysis_utils import generate_insights_report, print_final_insights

def main():
    """Run complete analysis pipeline"""

    print("="*50)
    
    # Step 1: Sentiment Analysis
    print("\n1. RUNNING SENTIMENT ANALYSIS...")
    run_sentiment_analysis()
    
    # Step 2: Thematic Analysis  
    print("\n2. RUNNING THEMATIC ANALYSIS...")
    run_thematic_analysis()
    
    # Step 3: Generate Insights
    print("\n3. GENERATING FINAL INSIGHTS...")
    
    # Load all data
    df = pd.read_csv('reviews_with_sentiment.csv')
    thematic_df = pd.read_csv('thematic_analysis_results.csv')
    
    # Generate insights
    insights = generate_insights_report(df, thematic_df)
    print_final_insights(insights)
    
    print("📊 Output files created:")
    print("   - reviews_with_sentiment.csv")
    print("   - thematic_analysis_results.csv") 
    print("   - sentiment_analysis.png")
    print("   - sentiment_vs_rating.png")
    print("   - keyword_analysis.png")
    print("   - wordclouds.png")

if __name__ == "__main__":
    main()