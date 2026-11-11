"""
MIVA Open University - Department of Data Science
Course: MIVA-DTS 305 - Data Quality and Data Wrangling
Tutor-Marked Assessment: Question 2 Solution

Student: Richard John
Matric No: 2024/C/DSC/0548
Email: rihard.john@miva.edu.ng
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run_scraper_pipeline():
    url = "http://books.toscrape.com/"
    print(f"Connecting to {url}...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
    }
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    book_pods = soup.find_all('article', class_='product_pod')
    print(f"Scraped {len(book_pods)} book items from the homepage.")
    
    rating_map = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }
    
    scraped_data = []
    for pod in book_pods:
        title = pod.h3.a['title']
        raw_price = pod.find('p', class_='price_color').text.strip()
        star_tag = pod.find('p', class_='star-rating')
        rating_text = star_tag['class'][1] if star_tag else 'None'
        availability = pod.find('p', class_='instock availability').text.strip()
        
        scraped_data.append({
            'Title': title,
            'Price_Raw': raw_price,
            'Rating_Text': rating_text,
            'Availability': availability
        })
        
    df = pd.DataFrame(scraped_data)
    df.to_csv('data/books_scraped_raw.csv', index=False)
    
    # Clean data
    # Convert prices to numeric floats (removing currency sign £)
    df['Price (£)'] = (
        df['Price_Raw']
        .str.replace('£', '', regex=False)
        .str.replace('Â', '', regex=False)
        .str.strip()
        .astype(float)
    )
    
    # Map rating strings to integer numbers
    df['Rating'] = df['Rating_Text'].map(rating_map)
    
    # Feature engineering: Categorise books as Affordable (< £20) vs Expensive (>= £20)
    df['Affordability'] = np.where(df['Price (£)'] < 20.0, 'Affordable', 'Expensive')
    
    df.to_csv('data/books_scraped_cleaned.csv', index=False)
    print("Cleaned scraped data saved to data/books_scraped_cleaned.csv")
    
    # Calculate average rating by affordability
    stats = df.groupby('Affordability')['Rating'].agg(['count', 'mean', 'std']).round(2)
    print("\nAffordability Statistics:")
    print(stats)
    
    # Chart 1: Pie Chart of Affordability Proportions
    counts = df['Affordability'].value_counts()
    plt.figure(figsize=(7, 7))
    plt.pie(
        counts,
        labels=counts.index,
        autopct='%1.1f%%',
        startangle=140,
        colors=['#dc2626', '#16a34a'],
        explode=(0.05, 0.05),
        shadow=True,
        textprops={'fontsize': 12, 'fontweight': 'bold'},
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5}
    )
    plt.title('Proportion of Books by Affordability\n(Affordable: < £20 | Expensive: ≥ £20)',
              fontsize=13, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig('figures/q2_affordability_pie_chart.png', dpi=300)
    plt.close()
    
    # Chart 2: Bar Chart of Average Ratings
    plt.figure(figsize=(7, 5))
    bars = plt.bar(stats.index, stats['mean'], color=['#16a34a', '#dc2626'], width=0.45, edgecolor='black', linewidth=0.8)
    for bar in bars:
        h = bar.get_height()
        plt.annotate(f"{h:.2f} / 5.0", (bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 6), textcoords="offset points", ha='center', va='bottom',
                     fontweight='bold', fontsize=12)
    plt.title('Average Customer Rating by Affordability Category', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Affordability Category', fontsize=12, labelpad=10)
    plt.ylabel('Mean Rating (Stars: 1 to 5)', fontsize=12, labelpad=10)
    plt.ylim(0, 5.5)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('figures/q2_ratings_bar_chart.png', dpi=300)
    plt.close()
    print("Question 2 charts generated successfully.")

if __name__ == '__main__':
    run_scraper_pipeline()
