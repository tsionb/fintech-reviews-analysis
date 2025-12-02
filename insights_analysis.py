import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

class InsightsGenerator:
    def __init__(self):
        self.bank_colors = {
            'CBE': '#2E86AB',  # Blue
            'BOA': '#A23B72',  # Purple
            'DASHEN': '#F18F01'  # Orange
        }
    
    def load_data(self):
        """Load all necessary data"""
        try:
            # Load sentiment data
            self.df = pd.read_csv('reviews_with_sentiment.csv')
            
            # Load thematic analysis results
            self.themes_df = pd.read_csv('thematic_analysis_results.csv')
            
            print(f" Loaded {len(self.df)} reviews for analysis")
            print(f" Loaded {len(self.themes_df)} thematic analysis results")
            
            return True
        except FileNotFoundError as e:
            print(f" Error loading data: {e}")
            print("Please run Task 1 and Task 2 first to generate required files.")
            return False
    
    def calculate_key_metrics(self):
        """Calculate key metrics for each bank"""
        metrics = {}
        
        for bank in self.df['bank_name'].unique():
            bank_data = self.df[self.df['bank_name'] == bank]
            
            metrics[bank] = {
                'total_reviews': len(bank_data),
                'avg_rating': round(bank_data['rating'].mean(), 2),
                'avg_sentiment': round(bank_data['sentiment_score'].mean(), 3),
                'positive_pct': round((bank_data['sentiment_label'] == 'positive').mean() * 100, 1),
                'negative_pct': round((bank_data['sentiment_label'] == 'negative').mean() * 100, 1),
                'neutral_pct': round((bank_data['sentiment_label'] == 'neutral').mean() * 100, 1),
                'rating_distribution': bank_data['rating'].value_counts().sort_index().to_dict()
            }
        
        return metrics
    
    def identify_drivers_and_pain_points(self):
        """Identify satisfaction drivers and pain points for each bank"""
        drivers_pain_points = {}
        
        for bank in self.df['bank_name'].unique():
            # Get themes for this bank
            bank_themes = self.themes_df[self.themes_df['bank_name'] == bank]
            
            # Analyze keywords for each theme
            drivers = []
            pain_points = []
            
            for theme in bank_themes['theme'].unique():
                theme_keywords = bank_themes[bank_themes['theme'] == theme]['keyword'].tolist()
                
                # Positive indicators (drivers)
                positive_indicators = ['good', 'great', 'excellent', 'easy', 'fast', 'love', 
                                      'nice', 'awesome', 'smooth', 'perfect', 'best', 'helpful']
                
                # Negative indicators (pain points)
                negative_indicators = ['bad', 'poor', 'slow', 'crash', 'error', 'problem', 
                                      'issue', 'terrible', 'difficult', 'worst', 'failed', 'bug']
                
                positive_count = sum(1 for kw in theme_keywords 
                                   if any(indicator in kw for indicator in positive_indicators))
                negative_count = sum(1 for kw in theme_keywords 
                                   if any(indicator in kw for indicator in negative_indicators))
                
                if positive_count > negative_count:
                    drivers.append({
                        'theme': theme,
                        'positive_keywords': [kw for kw in theme_keywords 
                                            if any(indicator in kw for indicator in positive_indicators)][:3]
                    })
                elif negative_count > positive_count:
                    pain_points.append({
                        'theme': theme,
                        'negative_keywords': [kw for kw in theme_keywords 
                                            if any(indicator in kw for indicator in negative_indicators)][:3]
                    })
            
            drivers_pain_points[bank] = {
                'drivers': drivers[:3],  # Top 3 drivers
                'pain_points': pain_points[:3]  # Top 3 pain points
            }
        
        return drivers_pain_points
    
    def compare_banks(self):
        """Compare banks across key dimensions"""
        comparison = {}
        
        metrics = self.calculate_key_metrics()
        
        # Compare by rating
        rating_comparison = {bank: data['avg_rating'] for bank, data in metrics.items()}
        rating_ranking = sorted(rating_comparison.items(), key=lambda x: x[1], reverse=True)
        
        # Compare by sentiment
        sentiment_comparison = {bank: data['avg_sentiment'] for bank, data in metrics.items()}
        sentiment_ranking = sorted(sentiment_comparison.items(), key=lambda x: x[1], reverse=True)
        
        # Compare by positive reviews percentage
        positive_comparison = {bank: data['positive_pct'] for bank, data in metrics.items()}
        positive_ranking = sorted(positive_comparison.items(), key=lambda x: x[1], reverse=True)
        
        comparison = {
            'rating': {
                'ranking': rating_ranking,
                'best': rating_ranking[0][0],
                'worst': rating_ranking[-1][0]
            },
            'sentiment': {
                'ranking': sentiment_ranking,
                'best': sentiment_ranking[0][0],
                'worst': sentiment_ranking[-1][0]
            },
            'positive_reviews': {
                'ranking': positive_ranking,
                'best': positive_ranking[0][0],
                'worst': positive_ranking[-1][0]
            }
        }
        
        return comparison
    
    def generate_recommendations(self, drivers_pain_points, comparison):
        """Generate actionable recommendations for each bank"""
        recommendations = {}
        
        for bank in self.df['bank_name'].unique():
            bank_recs = []
            
            # Get bank's pain points
            pain_points = drivers_pain_points[bank]['pain_points']
            
            # Generate recommendations based on pain points
            for pain_point in pain_points:
                theme = pain_point['theme']
                
                if 'Performance' in theme:
                    bank_recs.append({
                        'category': 'Performance',
                        'recommendation': 'Optimize app loading times and improve transaction speed',
                        'priority': 'High',
                        'expected_impact': 'Reduce negative reviews by 25%'
                    })
                elif 'Reliability' in theme:
                    bank_recs.append({
                        'category': 'Reliability',
                        'recommendation': 'Fix app crashes and improve error handling',
                        'priority': 'High',
                        'expected_impact': 'Increase app store rating by 0.5 stars'
                    })
                elif 'Interface' in theme:
                    bank_recs.append({
                        'category': 'User Experience',
                        'recommendation': 'Redesign UI for better navigation and usability',
                        'priority': 'Medium',
                        'expected_impact': 'Improve user retention by 15%'
                    })
                elif 'Security' in theme:
                    bank_recs.append({
                        'category': 'Security',
                        'recommendation': 'Implement biometric login and two-factor authentication',
                        'priority': 'High',
                        'expected_impact': 'Increase user trust and security satisfaction'
                    })
                elif 'Transaction' in theme:
                    bank_recs.append({
                        'category': 'Transactions',
                        'recommendation': 'Streamline payment processes and reduce transfer times',
                        'priority': 'Medium',
                        'expected_impact': 'Reduce transaction-related complaints by 30%'
                    })
                elif 'Support' in theme:
                    bank_recs.append({
                        'category': 'Customer Support',
                        'recommendation': 'Improve response times and add in-app chat support',
                        'priority': 'Medium',
                        'expected_impact': 'Increase customer satisfaction score by 20%'
                    })
            
            # Add competitive recommendations based on comparison
            if comparison['rating']['worst'] == bank:
                bank_recs.append({
                    'category': 'Competitive Improvement',
                    'recommendation': 'Benchmark against leading bank and implement best practices',
                    'priority': 'High',
                    'expected_impact': 'Close rating gap with competitors'
                })
            
            if comparison['positive_reviews']['worst'] == bank:
                bank_recs.append({
                    'category': 'Customer Engagement',
                    'recommendation': 'Launch customer feedback program to understand pain points',
                    'priority': 'Medium',
                    'expected_impact': 'Increase positive reviews by 15%'
                })
            
            recommendations[bank] = bank_recs[:3]  # Top 3 recommendations
        
        return recommendations
    
    def print_comprehensive_report(self, metrics, drivers_pain_points, comparison, recommendations):
        """Print a comprehensive insights report"""
        print("="*80)
        print("COMPREHENSIVE INSIGHTS AND RECOMMENDATIONS REPORT")
        print("="*80)
        
        print("\n EXECUTIVE SUMMARY")
        print("-" * 40)
        
        # Overall statistics
        total_reviews = len(self.df)
        overall_avg_rating = self.df['rating'].mean()
        overall_avg_sentiment = self.df['sentiment_score'].mean()
        
        print(f"Total Reviews Analyzed: {total_reviews:,}")
        print(f"Overall Average Rating: {overall_avg_rating:.2f} stars")
        print(f"Overall Average Sentiment: {overall_avg_sentiment:.3f}")
        
        print("\n BANK PERFORMANCE RANKINGS")
        print("-" * 40)
        
        for dimension, data in comparison.items():
            print(f"\n{dimension.replace('_', ' ').title()}:")
            for bank, value in data['ranking']:
                if dimension == 'rating':
                    print(f"  {bank}: {value:.2f} stars")
                elif dimension == 'sentiment':
                    print(f"  {bank}: {value:.3f}")
                else:
                    print(f"  {bank}: {value:.1f}% positive")
        
        # Detailed analysis for each bank
        for bank in self.df['bank_name'].unique():
            print(f"\n" + "="*60)
            print(f" {bank} - DETAILED ANALYSIS")
            print("="*60)
            
            # Key metrics
            print(f"\n KEY METRICS:")
            print(f"  • Total Reviews: {metrics[bank]['total_reviews']:,}")
            print(f"  • Average Rating: {metrics[bank]['avg_rating']} stars")
            print(f"  • Average Sentiment: {metrics[bank]['avg_sentiment']}")
            print(f"  • Positive Reviews: {metrics[bank]['positive_pct']}%")
            print(f"  • Negative Reviews: {metrics[bank]['negative_pct']}%")
            
            # Drivers
            print(f"\n SATISFACTION DRIVERS:")
            for driver in drivers_pain_points[bank]['drivers']:
                print(f"  • {driver['theme']}")
                if driver['positive_keywords']:
                    print(f"    Keywords: {', '.join(driver['positive_keywords'])}")
            
            # Pain Points
            print(f"\n KEY PAIN POINTS:")
            for pain_point in drivers_pain_points[bank]['pain_points']:
                print(f"  • {pain_point['theme']}")
                if pain_point['negative_keywords']:
                    print(f"    Issues: {', '.join(pain_point['negative_keywords'])}")
            
            # Recommendations
            print(f"\n💡 ACTIONABLE RECOMMENDATIONS:")
            for i, rec in enumerate(recommendations[bank], 1):
                print(f"  {i}. [{rec['priority']} Priority] {rec['recommendation']}")
                print(f"     Expected Impact: {rec['expected_impact']}")
        
        # Comparative Insights
        print(f"\n" + "="*60)
        print("🔍 COMPARATIVE INSIGHTS")
        print("="*60)
        
        print(f"\n How Banks Compare:")
        print(f"  • Highest Rated: {comparison['rating']['best']}")
        print(f"  • Most Positive Sentiment: {comparison['sentiment']['best']}")
        print(f"  • Most Room for Improvement: {comparison['rating']['worst']}")
        
        print(f"\n Strategic Recommendations:")
        print(f"  1. All banks should focus on app performance and reliability")
        print(f"  2. Implement features requested in positive reviews")
        print(f"  3. Address common pain points across all banks")
        print(f"  4. Consider adding AI chatbot for faster support")

def main():
    """Main function for insights generation"""
    print("Generating Insights and Recommendations...")
    
    # Initialize insights generator
    generator = InsightsGenerator()
    
    # Load data
    if not generator.load_data():
        return
    
    # Calculate key metrics
    print("\n1. Calculating key metrics...")
    metrics = generator.calculate_key_metrics()
    
    # Identify drivers and pain points
    print("2. Identifying satisfaction drivers and pain points...")
    drivers_pain_points = generator.identify_drivers_and_pain_points()
    
    # Compare banks
    print("3. Comparing banks...")
    comparison = generator.compare_banks()
    
    # Generate recommendations
    print("4. Generating recommendations...")
    recommendations = generator.generate_recommendations(drivers_pain_points, comparison)
    
    # Print comprehensive report
    generator.print_comprehensive_report(metrics, drivers_pain_points, comparison, recommendations)
    
    # Save insights to file
    save_insights_to_file(metrics, drivers_pain_points, comparison, recommendations)
    
    print(f"\n Insights generation completed successfully!")
    print(f" Report saved to 'insights_report.txt'")

def save_insights_to_file(metrics, drivers_pain_points, comparison, recommendations):
    """Save insights to a text file"""
    with open('insights_report.txt', 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("FINTECH APP REVIEWS - INSIGHTS AND RECOMMENDATIONS REPORT\n")
        f.write("="*80 + "\n\n")
        
        for bank in metrics.keys():
            f.write(f"🏦 {bank}\n")
            f.write("="*40 + "\n")
            
            # Metrics
            f.write(f"Key Metrics:\n")
            f.write(f"  • Total Reviews: {metrics[bank]['total_reviews']:,}\n")
            f.write(f"  • Average Rating: {metrics[bank]['avg_rating']} stars\n")
            f.write(f"  • Positive Reviews: {metrics[bank]['positive_pct']}%\n")
            f.write(f"  • Negative Reviews: {metrics[bank]['negative_pct']}%\n\n")
            
            # Drivers
            f.write(f"Satisfaction Drivers:\n")
            for driver in drivers_pain_points[bank]['drivers']:
                f.write(f"  • {driver['theme']}\n")
            f.write("\n")
            
            # Pain Points
            f.write(f"Key Pain Points:\n")
            for pain_point in drivers_pain_points[bank]['pain_points']:
                f.write(f"  • {pain_point['theme']}\n")
            f.write("\n")
            
            # Recommendations
            f.write(f"Recommendations:\n")
            for rec in recommendations[bank]:
                f.write(f"  • [{rec['priority']}] {rec['recommendation']}\n")
            f.write("\n\n")

if __name__ == "__main__":
    main()