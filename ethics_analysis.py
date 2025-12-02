import pandas as pd
import matplotlib.pyplot as plt

class EthicsAnalyzer:
    def __init__(self):
        pass
    
    def analyze_biases(self, df):
        """Analyze potential biases in the review data"""
        print("\n" + "="*60)
        print("ETHICS ANALYSIS - POTENTIAL BIASES")
        print("="*60)
        
        biases = []
        
        # 1. Check for review volume bias
        bank_counts = df['bank_name'].value_counts()
        print("\n1. Review Volume Distribution:")
        for bank, count in bank_counts.items():
            percentage = (count / len(df)) * 100
            print(f"   {bank}: {count} reviews ({percentage:.1f}%)")
            
            if percentage > 40:  # If one bank has >40% of reviews
                biases.append({
                    'type': 'Volume Bias',
                    'description': f'{bank} has {percentage:.1f}% of all reviews',
                    'impact': 'May over-represent this bank\'s user experience'
                })
        
        # 2. Check for rating bias
        print("\n2. Rating Distribution Analysis:")
        for bank in df['bank_name'].unique():
            bank_data = df[df['bank_name'] == bank]
            avg_rating = bank_data['rating'].mean()
            
            print(f"   {bank}: Average rating = {avg_rating:.2f} stars")
            
            if avg_rating < 2.5:
                biases.append({
                    'type': 'Negative Bias',
                    'description': f'{bank} has very low average rating ({avg_rating:.2f} stars)',
                    'impact': 'May reflect specific issues rather than overall user experience'
                })
        
        # 3. Check for sentiment bias
        print("\n3. Sentiment Distribution:")
        for bank in df['bank_name'].unique():
            bank_data = df[df['bank_name'] == bank]
            negative_pct = (bank_data['sentiment_label'] == 'negative').mean() * 100
            
            print(f"   {bank}: {negative_pct:.1f}% negative reviews")
            
            if negative_pct > 50:
                biases.append({
                    'type': 'Negative Sentiment Bias',
                    'description': f'{bank} has {negative_pct:.1f}% negative reviews',
                    'impact': 'Users more likely to review when experiencing problems'
                })
        
        # 4. Check for recency bias
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            recent_reviews = df[df['date'] >= '2025-01-01']
            recent_pct = (len(recent_reviews) / len(df)) * 100
            
            print(f"\n4. Recency Analysis:")
            print(f"   Reviews from 2025: {len(recent_reviews)} ({recent_pct:.1f}%)")
            
            if recent_pct > 70:
                biases.append({
                    'type': 'Recency Bias',
                    'description': f'{recent_pct:.1f}% of reviews are from recent months',
                    'impact': 'May not represent long-term app performance'
                })
        
        # Print summary
        print("\n" + "="*60)
        print("BIAS SUMMARY")
        print("="*60)
        
        if biases:
            for i, bias in enumerate(biases, 1):
                print(f"\n{i}. {bias['type']}:")
                print(f"   Description: {bias['description']}")
                print(f"   Potential Impact: {bias['impact']}")
        else:
            print("No significant biases detected in the data.")
        
        # Recommendations for mitigating biases
        print("\n" + "="*60)
        print("MITIGATION RECOMMENDATIONS")
        print("="*60)
        print("""
1. Acknowledge Limitations:
   - Mention that reviews may be skewed toward negative experiences
   - Note that vocal minority may be over-represented

2. Contextualize Findings:
   - Compare findings with other data sources if available
   - Consider seasonality and recent updates

3. Future Improvements:
   - Supplement with survey data for balanced perspective
   - Track changes over longer time periods
   - Consider implementing sentiment weighting

4. Ethical Considerations:
   - Avoid making definitive claims based solely on review data
   - Present findings as indicators rather than absolute truths
   - Consider cultural and regional differences in review behavior
        """)
        
        return biases

def main():
    """Main function for ethics analysis"""
    print("Performing Ethics Analysis...")
    
    try:
        # Load data
        df = pd.read_csv('reviews_with_sentiment.csv')
        print(f" Loaded {len(df)} reviews for ethics analysis")
        
        # Analyze biases
        analyzer = EthicsAnalyzer()
        biases = analyzer.analyze_biases(df)
        
        # Save ethics report
        with open('ethics_report.txt', 'w') as f:
            f.write("Ethics Analysis Report\n")
            f.write("="*40 + "\n\n")
            
            if biases:
                f.write("Potential Biases Identified:\n")
                for bias in biases:
                    f.write(f"- {bias['type']}: {bias['description']}\n")
            else:
                f.write("No significant biases detected.\n")
        
        print(f"\n Ethics analysis completed!")
        print(f" Report saved to 'ethics_report.txt'")
        
    except FileNotFoundError:
        print(" Data file not found. Run previous tasks first.")

if __name__ == "__main__":
    main()