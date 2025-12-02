import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_insights_report(df, thematic_results):
    """Generate actionable insights from the analysis"""
    
    insights = []
    
    # Analyze each bank
    for bank in df['bank_name'].unique():
        bank_data = df[df['bank_name'] == bank]
        bank_themes = thematic_results[thematic_results['bank_name'] == bank]
        
        # Key metrics
        avg_rating = bank_data['rating'].mean()
        avg_sentiment = bank_data['sentiment_score'].mean()
        positive_pct = (bank_data['sentiment_label'] == 'positive').mean() * 100
        
        # Top themes
        top_themes = bank_themes['theme'].value_counts().head(3)
        
        # Key insights
        insight = {
            'bank': bank,
            'avg_rating': avg_rating,
            'avg_sentiment': avg_sentiment,
            'positive_reviews_pct': positive_pct,
            'top_themes': list(top_themes.index),
            'strengths': [],
            'weaknesses': [],
            'recommendations': []
        }
        
        # Determine strengths and weaknesses based on themes and sentiment
        theme_sentiment = {}
        for theme in top_themes.index:
            theme_keywords = bank_themes[bank_themes['theme'] == theme]['keyword'].tolist()
            # Simple analysis - in real scenario, you'd analyze reviews mentioning these themes
            theme_sentiment[theme] = 'positive' if any('good' in kw or 'easy' in kw for kw in theme_keywords) else 'negative'
        
        for theme, sentiment in theme_sentiment.items():
            if sentiment == 'positive':
                insight['strengths'].append(theme)
            else:
                insight['weaknesses'].append(theme)
        
        insights.append(insight)
    
    return insights

def print_final_insights(insights):
    """Print formatted insights"""
    print("\n" + "="*70)
    print("FINAL INSIGHTS & RECOMMENDATIONS")
    print("="*70)
    
    for insight in insights:
        print(f"\n🏦 {insight['bank']}")
        print(f"   Average Rating: {insight['avg_rating']:.1f} stars")
        print(f"   Sentiment Score: {insight['avg_sentiment']:.3f}")
        print(f"   Positive Reviews: {insight['positive_reviews_pct']:.1f}%")
        
        print(f"\n   💪 STRENGTHS:")
        for strength in insight['strengths'][:2]:  # Top 2 strengths
            print(f"     • {strength}")
            
        print(f"\n   📉 WEAKNESSES:")
        for weakness in insight['weaknesses'][:2]:  # Top 2 weaknesses
            print(f"     • {weakness}")
            
        print(f"\n   💡 RECOMMENDATIONS:")
        # Generate simple recommendations based on weaknesses
        for weakness in insight['weaknesses'][:2]:
            if 'Performance' in weakness:
                print(f"     • Optimize app performance and reduce loading times")
            elif 'Reliability' in weakness:
                print(f"     • Focus on bug fixes and app stability")
            elif 'Interface' in weakness:
                print(f"     • Improve UI/UX design and navigation")
            elif 'Security' in weakness:
                print(f"     • Enhance login security and authentication process")
            elif 'Transaction' in weakness:
                print(f"     • Streamline payment and transfer processes")
        
        print("-" * 50)