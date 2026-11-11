"""
MIVA Open University - Department of Data Science
Course: MIVA-DTS 305 - Data Quality and Data Wrangling
Tutor-Marked Assessment: Question 1 Solution

Student: Richard John
Matric No: 2024/C/DSC/0548
Email: rihard.john@miva.edu.ng
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run_pipeline():
    print("=== Loading Raw Customer Orders Dataset ===")
    df = pd.read_csv('data/customer_orders_raw.csv')
    print(f"Total records loaded: {len(df)}")
    
    # 1. Inspect missing values in Total Amount
    missing_count = df['Total Amount'].isna().sum()
    print(f"Missing Total Amount values: {missing_count}")
    
    # Verify the formula Total Amount = Quantity * Price on valid rows
    valid_mask = df['Total Amount'].notna()
    expected = (df.loc[valid_mask, 'Quantity'] * df.loc[valid_mask, 'Price']).round(2)
    max_diff = (df.loc[valid_mask, 'Total Amount'] - expected).abs().max()
    print(f"Discrepancy test on non-null rows: ${max_diff:.4f}")
    
    # Impute missing values deterministically
    df['Total Amount'] = df['Total Amount'].fillna(
        (df['Quantity'] * df['Price']).round(2)
    )
    print("Missing values successfully imputed.")
    
    # 2. Check and remove duplicates
    dups = df.duplicated().sum()
    print(f"Duplicate rows detected: {dups}")
    df = df.drop_duplicates()
    
    # 3. Standardise Country column
    print("Country entries before standardisation:")
    print(df['Country'].value_counts())
    
    country_mapping = {
        'usa': 'United States',
        'U.S.A.': 'United States',
        'United States': 'United States'
    }
    df['Country'] = df['Country'].map(country_mapping)
    print("\nCountry entries after standardisation:")
    print(df['Country'].value_counts())
    
    # Save cleaned dataset
    df.to_csv('data/customer_orders_cleaned.csv', index=False)
    print("\nCleaned dataset exported to data/customer_orders_cleaned.csv")
    
    # 4. Aggregations & Visualisations
    cat_summary = (
        df.groupby('Product Category')['Total Amount']
        .agg(Revenue='sum', Orders='count', Average_Value='mean')
        .sort_values(by='Revenue', ascending=False)
        .reset_index()
    )
    print("\nRevenue by Product Category:")
    print(cat_summary)
    
    # Plot Revenue by Category
    plt.figure(figsize=(8, 5))
    bars = plt.bar(cat_summary['Product Category'], cat_summary['Revenue'], 
                   color=['#1f77b4', '#ff7f0e', '#2ca02c'], width=0.55, edgecolor='black', linewidth=0.8)
    for bar in bars:
        h = bar.get_height()
        plt.annotate(f"${h:,.2f}", (bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 6), textcoords="offset points", ha='center', va='bottom',
                     fontweight='bold', fontsize=11)
    plt.title('Total Revenue by Product Category', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Product Category', fontsize=12, labelpad=10)
    plt.ylabel('Total Revenue (USD $)', fontsize=12, labelpad=10)
    plt.ylim(0, cat_summary['Revenue'].max() * 1.18)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('figures/q1_revenue_by_category.png', dpi=300)
    plt.close()
    print("Chart saved to figures/q1_revenue_by_category.png")

if __name__ == '__main__':
    run_pipeline()
