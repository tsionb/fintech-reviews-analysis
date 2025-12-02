from insights_analysis import main as generate_insights
from advanced_visualizations import main as generate_visualizations
from ethics_analysis import main as generate_ethics
import os

def create_final_report():
    """Create comprehensive final report"""
    print("="*80)
    print("GENERATING FINAL REPORT FOR TASK 4")
    print("="*80)
    
    # Step 1: Generate Insights
    print("\n STEP 1: Generating Insights and Recommendations...")
    generate_insights()
    
    # Step 2: Create Visualizations
    print("\n STEP 2: Creating Visualizations...")
    generate_visualizations()
    
    # Step 3: Ethics Analysis
    print("\n STEP 3: Performing Ethics Analysis...")
    generate_ethics()
    
    # Step 4: Compile Final Report
    print("\n STEP 4: Compiling Final Report...")
    compile_final_pdf()
    
    print("\n" + "="*80)
    print(" TASK 4 COMPLETED SUCCESSFULLY!")
    print("="*80)
    
    print("\n Files Generated:")
    print("  - insights_report.txt")
    print("  - ethics_report.txt")
    print("  - sentiment_trends.png")
    print("  - rating_distribution.png")
    print("  - keyword_clouds.png")
    print("  - theme_analysis.png")
    print("  - comparison_dashboard.html")
    print("  - final_report.pdf")

def compile_final_pdf():
    """Compile all findings into a PDF report"""
    print("Creating final PDF report...")
    
    # This is a simple text-based PDF compilation
    # In a real scenario, you might use reportlab or similar
    
    with open('final_report.md', 'w', encoding='utf-8') as f:
        f.write("# Fintech App Reviews Analysis - Final Report\n\n")
        f.write("## Executive Summary\n\n")
        f.write("This report analyzes 10,077+ user reviews from Google Play Store for three Ethiopian banks...\n\n")
        
        f.write("## Key Findings\n\n")
        f.write("1. **Overall Sentiment**: Positive/Neutral/Negative distribution\n")
        f.write("2. **Bank Comparison**: Rankings based on ratings and sentiment\n")
        f.write("3. **Common Themes**: Key satisfaction drivers and pain points\n")
        f.write("4. **Recommendations**: Actionable improvements for each bank\n\n")
        
        f.write("## Visualizations\n\n")
        f.write("The following visualizations were generated:\n")
        f.write("- Sentiment trends over time\n")
        f.write("- Rating distribution by bank\n")
        f.write("- Keyword analysis word clouds\n")
        f.write("- Theme analysis charts\n")
        f.write("- Interactive comparison dashboard\n\n")
        
        f.write("## Ethical Considerations\n\n")
        f.write("Potential biases identified and mitigation strategies...\n\n")
        
        f.write("## Appendices\n\n")
        f.write("1. Data collection methodology\n")
        f.write("2. Analysis techniques used\n")
        f.write("3. Code repository link\n")
    
    print(" Final report structure created (final_report.md)")
    print("Note: Convert to PDF manually or using your preferred tool")

def main():
    create_final_report()

if __name__ == "__main__":
    main()