import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

class AdvancedVisualizer:
    def __init__(self):
        self.bank_colors = {
            'CBE': '#2E86AB',
            'BOA': '#A23B72', 
            'DASHEN': '#F18F01'
        }
        
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
    
    def load_data(self):
        """Load data for visualization"""
        try:
            self.df = pd.read_csv('reviews_with_sentiment.csv')
            self.themes_df = pd.read_csv('thematic_analysis_results.csv')
            print(f" Loaded data for visualization")
            return True
        except FileNotFoundError:
            print(" Data files not found")
            return False
    
    def create_sentiment_trends_plot(self):
        """Create sentiment trends over time"""
        print("Creating sentiment trends plot...")
        
        # Convert date to datetime
        self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
        
        # Filter for recent data
        recent_df = self.df[self.df['date'] >= '2024-01-01'].copy()
        
        # Create monthly aggregates
        recent_df['month'] = recent_df['date'].dt.to_period('M')
        monthly_avg = recent_df.groupby(['bank_name', 'month'])['sentiment_score'].mean().reset_index()
        monthly_avg['month'] = monthly_avg['month'].astype(str)
        
        # Create plot
        fig, ax = plt.subplots(figsize=(12, 6))
        
        for bank in monthly_avg['bank_name'].unique():
            bank_data = monthly_avg[monthly_avg['bank_name'] == bank]
            ax.plot(bank_data['month'], bank_data['sentiment_score'], 
                   marker='o', linewidth=2, label=bank, color=self.bank_colors.get(bank))
        
        ax.set_title('Sentiment Trends Over Time (2024)', fontsize=16, fontweight='bold')
        ax.set_xlabel('Month', fontsize=12)
        ax.set_ylabel('Average Sentiment Score', fontsize=12)
        ax.legend(title='Bank')
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('sentiment_trends.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_rating_distribution_plot(self):
        """Create rating distribution plot"""
        print("Creating rating distribution plot...")
        
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        for idx, bank in enumerate(self.df['bank_name'].unique()):
            bank_data = self.df[self.df['bank_name'] == bank]
            
            # Count ratings
            rating_counts = bank_data['rating'].value_counts().sort_index()
            
            axes[idx].bar(rating_counts.index, rating_counts.values, 
                         color=self.bank_colors.get(bank), alpha=0.7)
            axes[idx].set_title(f'{bank} - Rating Distribution', fontweight='bold')
            axes[idx].set_xlabel('Rating (Stars)')
            axes[idx].set_ylabel('Count')
            axes[idx].set_xticks(range(1, 6))
            axes[idx].grid(True, alpha=0.3)
            
            # Add value labels
            for i, v in enumerate(rating_counts.values):
                axes[idx].text(i+1, v, str(v), ha='center', va='bottom')
        
        plt.suptitle('Rating Distribution by Bank', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig('rating_distribution.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_keyword_clouds(self):
        """Create keyword word clouds for each bank"""
        print("Creating keyword clouds...")
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        
        for idx, bank in enumerate(self.df['bank_name'].unique()):
            # Get keywords for this bank
            bank_themes = self.themes_df[self.themes_df['bank_name'] == bank]
            
            if len(bank_themes) > 0:
                # Create word frequency dictionary
                word_freq = {}
                for _, row in bank_themes.iterrows():
                    word_freq[row['keyword']] = word_freq.get(row['keyword'], 0) + 1
                
                # Generate word cloud
                wordcloud = WordCloud(
                    width=400,
                    height=300,
                    background_color='white',
                    colormap='viridis',
                    max_words=50
                ).generate_from_frequencies(word_freq)
                
                axes[idx].imshow(wordcloud, interpolation='bilinear')
                axes[idx].set_title(f'{bank} - Common Keywords', fontweight='bold')
                axes[idx].axis('off')
            else:
                axes[idx].text(0.5, 0.5, 'No data available', 
                              ha='center', va='center', fontsize=12)
                axes[idx].axis('off')
        
        plt.suptitle('Keyword Analysis by Bank', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig('keyword_clouds.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_comparison_dashboard(self):
        """Create comparison dashboard"""
        print("Creating comparison dashboard...")
        
        # Calculate metrics
        metrics = []
        for bank in self.df['bank_name'].unique():
            bank_data = self.df[self.df['bank_name'] == bank]
            
            metrics.append({
                'Bank': bank,
                'Avg Rating': round(bank_data['rating'].mean(), 2),
                'Avg Sentiment': round(bank_data['sentiment_score'].mean(), 3),
                'Positive %': round((bank_data['sentiment_label'] == 'positive').mean() * 100, 1),
                'Total Reviews': len(bank_data)
            })
        
        metrics_df = pd.DataFrame(metrics)
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Average Rating by Bank', 'Average Sentiment by Bank',
                           'Positive Reviews Percentage', 'Total Reviews Count'),
            specs=[[{'type': 'bar'}, {'type': 'bar'}],
                   [{'type': 'bar'}, {'type': 'bar'}]]
        )
        
        # Plot 1: Average Rating
        fig.add_trace(
            go.Bar(x=metrics_df['Bank'], y=metrics_df['Avg Rating'],
                  marker_color=[self.bank_colors.get(b) for b in metrics_df['Bank']]),
            row=1, col=1
        )
        
        # Plot 2: Average Sentiment
        fig.add_trace(
            go.Bar(x=metrics_df['Bank'], y=metrics_df['Avg Sentiment'],
                  marker_color=[self.bank_colors.get(b) for b in metrics_df['Bank']]),
            row=1, col=2
        )
        
        # Plot 3: Positive Percentage
        fig.add_trace(
            go.Bar(x=metrics_df['Bank'], y=metrics_df['Positive %'],
                  marker_color=[self.bank_colors.get(b) for b in metrics_df['Bank']]),
            row=2, col=1
        )
        
        # Plot 4: Total Reviews
        fig.add_trace(
            go.Bar(x=metrics_df['Bank'], y=metrics_df['Total Reviews'],
                  marker_color=[self.bank_colors.get(b) for b in metrics_df['Bank']]),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title_text='Bank Performance Comparison Dashboard',
            showlegend=False,
            height=800
        )
        
        # Save as HTML for interactive view
        fig.write_html('comparison_dashboard.html')
        print(" Comparison dashboard saved as 'comparison_dashboard.html'")
    
    def create_theme_analysis_plot(self):
        """Create theme analysis plot"""
        print("Creating theme analysis plot...")
        
        if len(self.themes_df) == 0:
            print("No thematic analysis data available")
            return
        
        # Count themes per bank
        theme_counts = self.themes_df.groupby(['bank_name', 'theme']).size().reset_index(name='count')
        
        # Get top 5 themes overall
        top_themes = self.themes_df['theme'].value_counts().head(5).index.tolist()
        theme_counts_filtered = theme_counts[theme_counts['theme'].isin(top_themes)]
        
        # Create plot
        plt.figure(figsize=(12, 6))
        
        # Pivot for grouped bar chart
        pivot_df = theme_counts_filtered.pivot(index='bank_name', columns='theme', values='count')
        pivot_df.plot(kind='bar', figsize=(12, 6), color=['#2E86AB', '#A23B72', '#F18F01', '#73B761', '#E15554'])
        
        plt.title('Top 5 Themes by Bank', fontsize=16, fontweight='bold')
        plt.xlabel('Bank')
        plt.ylabel('Number of Keywords')
        plt.xticks(rotation=0)
        plt.legend(title='Theme')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('theme_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_all_visualizations(self):
        """Create all visualizations"""
        if not self.load_data():
            return
        
        print("Creating Task 4 visualizations...")
        
        # Create each visualization
        self.create_sentiment_trends_plot()
        self.create_rating_distribution_plot()
        self.create_keyword_clouds()
        self.create_theme_analysis_plot()
        self.create_comparison_dashboard()
        
        print(" All visualizations created successfully!")

def main():
    """Main function for visualization generation"""
    print("Generating Advanced Visualizations for Task 4...")
    
    visualizer = AdvancedVisualizer()
    visualizer.create_all_visualizations()
    
    print("\n Visualizations created:")
    print("  - sentiment_trends.png")
    print("  - rating_distribution.png")
    print("  - keyword_clouds.png")
    print("  - theme_analysis.png")
    print("  - comparison_dashboard.html (interactive)")

if __name__ == "__main__":
    main()