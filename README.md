# MIVA Open University - Department of Data Science
## Course: MIVA-DTS 305 - Data Quality and Data Wrangling
### Tutor-Marked Assessment (TMA) Lab Solution

**Student Information:**
- **Full Name:** Richard John
- **Matriculation / Reg Number:** 2024/C/DSC/0548
- **Department:** Data Science
- **Email:** richard.john@miva.edu.ng
- **Institution:** Miva Open University

---

## Project Overview

This repository contains the practical solutions and deliverables for the MIVA-DTS 305 assessment:

1. **Question 1: Cleaning and Analysing Tabular Data**
   - Dataset: Customer orders (100 records).
   - Tasks: Deterministic formulaic imputation of missing `Total Amount` values (`Quantity * Price`), verification of row uniqueness (0 duplicates), categorical standardisation of inconsistent `Country` formatting (`usa`, `U.S.A.`, `United States` -> `United States`), category revenue aggregations, and comparative visual analysis of the "top 3 countries" pitfall versus standardized reality.
   - Deliverables: `data/customer_orders_cleaned.csv`, `notebooks/Question_1_Tabular_Data_Cleaning.ipynb`, and revenue charts in `figures/`.

2. **Question 2: Web Scraping and Feature Engineering**
   - Source: [Books to Scrape](http://books.toscrape.com/)
   - Tasks: Automated extraction of homepage book pod details (`Title`, `Price`, `Rating`, `Availability`), currency symbol sanitisation, text star-rating to ordinal integer mapping, and engineering an affordability metric (`Affordable` < £20 vs `Expensive` >= £20) with statistical and graphical analysis.
   - Deliverables: `data/books_scraped_cleaned.csv`, `notebooks/Question_2_Web_Scraping_Feature_Engineering.ipynb`, and distribution charts in `figures/`.

3. **Final Report:**
   - Compiled PDF report formatted in Miva Open University's template: `MIVA_DTS305_TMA_Richard_John_2024_C_DSC_0548.pdf`.

---

## Repository Structure

```
.
├── MIVA_DTS305_TMA_Richard_John_2024_C_DSC_0548.pdf  # Submitted assessment report
├── README.md                                         # Project documentation
├── customer_orders_pipeline.py                       # Question 1 data cleaning script
├── books_scraper_pipeline.py                         # Question 2 web scraping script
├── generate_report.py                                # Script to compile the PDF report
├── miva_exact_top_banner.png                         # Report template header asset
├── data/
│   ├── customer_orders_raw.csv                       # Raw orders dataset (100 records)
│   ├── customer_orders_cleaned.csv                   # Cleaned orders dataset
│   ├── books_scraped_raw.csv                         # Raw scraped books data
│   └── books_scraped_cleaned.csv                     # Cleaned and feature-engineered books data
├── figures/
│   ├── q1_revenue_by_category.png                    # Category revenue bar chart
│   ├── q1_top_countries_revenue.png                  # Country revenue comparison chart
│   ├── q2_affordability_pie_chart.png                # Book affordability pie chart
│   └── q2_ratings_bar_chart.png                      # Average customer ratings bar chart
└── notebooks/
    ├── Question_1_Tabular_Data_Cleaning.ipynb        # Question 1 notebook
    ├── Question_2_Web_Scraping_Feature_Engineering.ipynb # Question 2 notebook
    └── MIVA_DTS305_TMA_Richard_John.ipynb            # Unified master notebook
```

---

## How to Run

### Requirements
Install the required Python packages:
```bash
pip install pandas numpy matplotlib requests beautifulsoup4 reportlab
```

### Run Question 1 Pipeline
```bash
python3 customer_orders_pipeline.py
```

### Run Question 2 Web Scraper
```bash
python3 books_scraper_pipeline.py
```

### Recompile the PDF Report
```bash
python3 generate_report.py
```
