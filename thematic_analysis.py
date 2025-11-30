import pandas as pd
import numpy as np
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import re

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

class ThematicAnalyzer:
    def __init__(self):
        self.common_fintech_terms = {
            'transfer', 'login', 'password', 'app', 'mobile', 'bank', 'account',
            'money', 'payment', 'transaction', 'error', 'problem', 'issue',
            'slow', 'fast', 'easy', 'good', 'bad', 'work', 'update', 'crash'
        }
    
    def preprocess_text(self, text):
        """Clean and preprocess text for analysis"""
        if not isinstance(text, str):
            return ""
        
        # Basic cleaning
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove punctuation/numbers
        text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
        
        # spaCy processing
        doc = nlp(text)
        
        # Extract relevant tokens (nouns, adjectives, verbs)
        tokens = []
        for token in doc:
            if (not token.is_stop and 
                not token.is_punct and 
                len(token.lemma_) > 2 and
                token.pos_ in ['NOUN', 'ADJ', 'VERB'] and
                token.lemma_ not in self.common_fintech_terms):
                tokens.append(token.lemma_)
        
        return ' '.join(tokens)
    
    def extract_keywords_tfidf(self, texts, max_features=50):
        """Extract keywords using TF-IDF"""
        vectorizer = TfidfVectorizer(
            max_features=max_features,
            stop_words='english',
            ngram_range=(1, 2)  # Single words and bigrams
        )
        
        tfidf_matrix = vectorizer.fit_transform(texts)
        feature_names = vectorizer.get_feature_names_out()
        
        # Get average TF-IDF scores
        avg_tfidf_scores = tfidf_matrix.mean(axis=0).A1
        keyword_scores = list(zip(feature_names, avg_tfidf_scores))
        keyword_scores.sort(key=lambda x: x[1], reverse=True)
        
        return keyword_scores[:20]  # Return top 20
    
    def manual_theme_clustering(self, keywords, bank_name):
        """Manually cluster keywords into themes based on banking context"""
        # Define theme categories
        theme_categories = {
            'User Interface & Experience': {'interface', 'design', 'layout', 'navigation', 'button', 'screen', 'view'},
            'Performance & Speed': {'slow', 'fast', 'speed', 'loading', 'response', 'lag', 'delay'},
            'Reliability & Bugs': {'crash', 'bug', 'error', 'freeze', 'stop', 'work', 'fix'},
            'Account Access & Security': {'login', 'password', 'pin', 'security', 'access', 'verification', 'authenticate'},
            'Transactions & Payments': {'transfer', 'payment', 'transaction', 'send', 'receive', 'money', 'bill'},
            'Customer Support': {'support', 'help', 'service', 'contact', 'response', 'assistance'},
            'Features & Functionality': {'feature', 'function', 'option', 'tool', 'capability', 'missing'}
        }
        
        # Map keywords to themes
        keyword_themes = {}
        for keyword, score in keywords:
            assigned = False
            for theme, theme_keywords in theme_categories.items():
                # Check if keyword relates to theme
                if any(theme_word in keyword for theme_word in theme_keywords):
                    keyword_themes[keyword] = theme
                    assigned = True
                    break
            
            # If no theme matched, assign based on common patterns
            if not assigned:
                if any(word in keyword for word in ['slow', 'fast', 'speed', 'lag']):
                    keyword_themes[keyword] = 'Performance & Speed'
                elif any(word in keyword for word in ['crash', 'error', 'bug', 'fix']):
                    keyword_themes[keyword] = 'Reliability & Bugs'
                elif any(word in keyword for word in ['login', 'password', 'security']):
                    keyword_themes[keyword] = 'Account Access & Security'
                elif any(word in keyword for word in ['transfer', 'payment', 'money']):
                    keyword_themes[keyword] = 'Transactions & Payments'
                else:
                    keyword_themes[keyword] = 'General Feedback'
        
        return keyword_themes
    
    def analyze_bank_themes(self, df, bank_name):
        """Analyze themes for a specific bank"""
        print(f"\nAnalyzing themes for {bank_name}...")
        
        # Filter reviews for this bank
        bank_reviews = df[df['bank_name'] == bank_name]
        
        # Separate positive and negative reviews for deeper insight
        positive_reviews = bank_reviews[bank_reviews['sentiment_label'] == 'positive']
        negative_reviews = bank_reviews[bank_reviews['sentiment_label'] == 'negative']
        
        print(f"  Positive reviews: {len(positive_reviews)}")
        print(f"  Negative reviews: {len(negative_reviews)}")
        
        # Preprocess all reviews
        all_processed = [self.preprocess_text(text) for text in bank_reviews['review_text']]
        positive_processed = [self.preprocess_text(text) for text in positive_reviews['review_text']]
        negative_processed = [self.preprocess_text(text) for text in negative_reviews['review_text']]
        
        # Extract keywords
        all_keywords = self.extract_keywords_tfidf(all_processed)
        positive_keywords = self.extract_keywords_tfidf(positive_processed) if len(positive_processed) > 0 else []
        negative_keywords = self.extract_keywords_tfidf(negative_processed) if len(negative_processed) > 0 else []
        
        # Cluster into themes
        themes = self.manual_theme_clustering(all_keywords, bank_name)
        
        return {
            'all_keywords': all_keywords,
            'positive_keywords': positive_keywords,
            'negative_keywords': negative_keywords,
            'themes': themes
        }

def create_keyword_visualizations(bank_results):
    """Create visualizations for keyword analysis"""
    print("Creating thematic analysis visualizations...")
    
    # Plot 1: Top keywords for each bank
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    axes = axes.flatten()
    
    for idx, (bank_name, results) in enumerate(bank_results.items()):
        if idx >= 4:  # Limit to 4 plots
            break
            
        keywords = results['all_keywords'][:10]  # Top 10 keywords
        words = [kw[0] for kw in keywords]
        scores = [kw[1] for kw in keywords]
        
        axes[idx].barh(words, scores, color='skyblue')
        axes[idx].set_title(f'Top Keywords - {bank_name}')
        axes[idx].set_xlabel('TF-IDF Score')
    
    plt.tight_layout()
    plt.savefig('keyword_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Plot 2: Word clouds for each bank
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    for idx, (bank_name, results) in enumerate(list(bank_results.items())[:3]):
        # Create word frequency dictionary
        word_freq = {kw[0]: kw[1] for kw in results['all_keywords'][:30]}
        
        wordcloud = WordCloud(
            width=400, 
            height=300, 
            background_color='white',
            colormap='viridis'
        ).generate_from_frequencies(word_freq)
        
        axes[idx].imshow(wordcloud, interpolation='bilinear')
        axes[idx].set_title(f'Word Cloud - {bank_name}')
        axes[idx].axis('off')
    
    plt.tight_layout()
    plt.savefig('wordclouds.png', dpi=300, bbox_inches='tight')
    plt.show()

def generate_theme_report(bank_results):
    """Generate a comprehensive theme report"""
    print("\n" + "="*60)
    print("THEMATIC ANALYSIS REPORT")
    print("="*60)
    
    for bank_name, results in bank_results.items():
        print(f"\n📊 {bank_name.upper()} - THEME ANALYSIS")
        print("-" * 40)
        
        # Count themes
        theme_counts = {}
        for keyword, theme in results['themes'].items():
            theme_counts[theme] = theme_counts.get(theme, 0) + 1
        
        # Print top themes
        print("Top Themes:")
        for theme, count in sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  • {theme}: {count} keywords")
        
        # Print top positive keywords
        if results['positive_keywords']:
            print("\nPositive Feedback Keywords:")
            for keyword, score in results['positive_keywords'][:5]:
                print(f"  ✓ {keyword} (score: {score:.3f})")
        
        # Print top negative keywords
        if results['negative_keywords']:
            print("\nNegative Feedback Keywords:")
            for keyword, score in results['negative_keywords'][:5]:
                print(f"  ✗ {keyword} (score: {score:.3f})")
        
        # Print example keywords for each major theme
        print("\nKey Themes with Examples:")
        major_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        for theme, count in major_themes:
            theme_keywords = [kw for kw, t in results['themes'].items() if t == theme][:3]
            print(f"  🎯 {theme}: {', '.join(theme_keywords)}")

def main():
    """Main execution function for thematic analysis"""
    print("Starting Thematic Analysis...")
    
    # Load data with sentiment
    try:
        df = pd.read_csv('reviews_with_sentiment.csv')
        print(f"Loaded {len(df)} reviews with sentiment analysis")
    except FileNotFoundError:
        print("Error: Run sentiment analysis first!")
        return
    
    # Initialize analyzer
    analyzer = ThematicAnalyzer()
    
    # Analyze themes for each bank
    banks = df['bank_name'].unique()
    bank_results = {}
    
    for bank in banks:
        bank_results[bank] = analyzer.analyze_bank_themes(df, bank)
    
    # Create visualizations
    create_keyword_visualizations(bank_results)
    
    # Generate comprehensive report
    generate_theme_report(bank_results)
    
    # Save thematic analysis results
    thematic_results = []
    for bank_name, results in bank_results.items():
        for keyword, theme in results['themes'].items():
            thematic_results.append({
                'bank_name': bank_name,
                'keyword': keyword,
                'theme': theme
            })
    
    thematic_df = pd.DataFrame(thematic_results)
    thematic_df.to_csv('thematic_analysis_results.csv', index=False)
    
    print(f"\n✅ Thematic analysis completed!")
    print(f"📁 Results saved to 'thematic_analysis_results.csv'")

if __name__ == "__main__":
    main()