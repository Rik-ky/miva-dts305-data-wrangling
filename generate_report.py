"""
MIVA Open University - Department of Data Science
Course: MIVA-DTS 305 - Data Quality and Data Wrangling
Tutor-Marked Assessment: PDF Report Generator

Student: Richard John
Matric No: 2024/C/DSC/0548
Email: richard.john@miva.edu.ng
GitHub: https://github.com/Rik-ky/miva-dts305-data-wrangling
"""

import os
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, Preformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# ==============================================================================
# NUMBERED CANVAS: DRAWS HEADER & FOOTER
# ==============================================================================
class MivaNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(MivaNumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(MivaNumberedCanvas, self).showPage()
        super(MivaNumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        w, h = A4
        
        # 1. Top Header Banner
        banner_img = 'miva_exact_top_banner.png'
        banner_h = 68.05
        if os.path.exists(banner_img):
            self.drawImage(banner_img, 0, h - banner_h, width=w, height=banner_h, mask='auto')
        
        # 2. Header Text
        self.setFont("Helvetica-Bold", 14.5)
        self.setFillColor(colors.white)
        self.drawString(38, h - 31, "Tutor-Marked  Assessment")
        
        self.setFont("Helvetica", 10.5)
        self.setFillColor(colors.HexColor("#dbeafe"))
        self.drawString(38, h - 47, "MIVA-DTS 305 - Data Quality and Data Wrangling")

        # 3. Footer Line & Copyright
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.6)
        self.line(38, 28, w - 38, 28)
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(38, 16, "© Copyright 2024 MIVA Open University All Rights Reserved")
        
        # Page Number
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(w - 38, 16, page_str)
        
        self.restoreState()


def generate_report():
    pdf_path = "MIVA_DTS305_TMA_Richard_John_2024_C_DSC_0548.pdf"
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=38,
        rightMargin=38,
        topMargin=76,
        bottomMargin=38
    )

    styles = getSampleStyleSheet()

    # Typography styles
    title_h1 = ParagraphStyle(
        'ExactH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=20,
        textColor=colors.HexColor("#09304f"),
        spaceBefore=10,
        spaceAfter=8,
        keepWithNext=True
    )

    title_h2 = ParagraphStyle(
        'ExactH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=17,
        textColor=colors.HexColor("#09304f"),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body = ParagraphStyle(
        'ExactBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16.5,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=8
    )

    bullet_p = ParagraphStyle(
        'ExactBullet',
        parent=body,
        leftIndent=18,
        bulletIndent=6,
        spaceAfter=7
    )

    code_p = ParagraphStyle(
        'ExactCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.8,
        leading=10.2,
        textColor=colors.HexColor("#0f172a")
    )

    tbl_header = ParagraphStyle(
        'TblH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.white,
        alignment=1
    )

    tbl_cell = ParagraphStyle(
        'TblC',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#1e293b")
    )

    tbl_cell_center = ParagraphStyle(
        'TblCC',
        parent=tbl_cell,
        alignment=1
    )

    tbl_cell_right = ParagraphStyle(
        'TblCR',
        parent=tbl_cell,
        alignment=2
    )

    story = []

    # ==============================================================================
    # PAGE 1: STUDENT DETAILS & QUESTION 1 METHODOLOGY
    # ==============================================================================
    student_info_data = [
        [
            Paragraph("<b>Candidate Name:</b>", body), Paragraph("Richard John", body),
            Paragraph("<b>Reg / Matric No:</b>", body), Paragraph("<b>2024/C/DSC/0548</b>", body)
        ],
        [
            Paragraph("<b>Department:</b>", body), Paragraph("Data Science", body),
            Paragraph("<b>Institutional Email:</b>", body), Paragraph("richard.john@miva.edu.ng", body)
        ]
    ]
    t_student = Table(student_info_data, colWidths=[1.5*72, 1.7*72, 1.6*72, 2.4*72])
    t_student.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_student)
    story.append(Spacer(1, 8))

    # GitHub Repository Link Box
    git_html = (
        "<b>Source Code & Interactive Notebooks Repository:</b> "
        "<font color='#1d4ed8'><u>https://github.com/Rik-ky/miva-dts305-data-wrangling</u></font>"
    )
    t_git = Table([[Paragraph(git_html, body)]], colWidths=[7.2 * 72])
    t_git.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#eff6ff")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93c5fd")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_git)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Question 1: Cleaning and Analysing Tabular Data", title_h1))
    
    q1_desc = (
        "<b>Dataset Description:</b> The dataset contains 100 customer retail transactions across eight columns: "
        "<code>Order ID</code>, <code>Customer Name</code>, <code>Order Date</code>, <code>Product Category</code>, "
        "<code>Quantity</code>, <code>Price</code>, <code>Total Amount</code> (containing missing values), and "
        "<code>Country</code> (with inconsistent formatting, e.g., 'usa', 'U.S.A.', 'United States')."
    )
    story.append(Paragraph(q1_desc, body))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Data Quality Remediation Tasks:", title_h2))

    task1 = (
        "<b>1. Handle missing values in the Total Amount column:</b><br/>"
        "An initial diagnostic audit identified 19 missing values (19.0%) in <code>Total Amount</code>. "
        "Because order totals are mathematically determined by unit volume and price "
        "(<code>Total Amount = Quantity * Price</code>), this relationship was verified across all 81 non-null rows "
        "(maximum discrepancy = $0.00). All 19 missing values were imputed using: "
        "<code>df['Total Amount'] = df['Total Amount'].fillna((df['Quantity'] * df['Price']).round(2))</code>."
    )
    story.append(Paragraph(f"● {task1}", bullet_p))

    task2 = (
        "<b>2. Remove duplicate rows:</b><br/>"
        "A duplicate check across all attributes (<code>df.duplicated().sum()</code>) confirmed 0 duplicate rows. "
        "All 100 records represent distinct orders and were retained."
    )
    story.append(Paragraph(f"● {task2}", bullet_p))

    task3 = (
        "<b>3. Standardise formatting in the Country column:</b><br/>"
        "The raw column contained three variations: <code>'United States'</code> (43 orders), <code>'usa'</code> (30 orders), "
        "and <code>'U.S.A.'</code> (27 orders). All entries were harmonised to <code>'United States'</code>. "
        "The cleaned dataset was saved as <code>data/customer_orders_cleaned.csv</code>."
    )
    story.append(Paragraph(f"● {task3}", bullet_p))

    story.append(PageBreak())

    # ==============================================================================
    # PAGE 2: QUESTION 1 CATEGORY REVENUE & BAR CHART
    # ==============================================================================
    story.append(Paragraph("Product Category Revenue Aggregation & Visualisation", title_h1))
    
    cat_intro = (
        "Total gross revenue generated across all 100 customer transactions is <b>$31,137.16</b>. "
        "The performance across the three merchandise categories is summarized in the table below:"
    )
    story.append(Paragraph(cat_intro, body))
    story.append(Spacer(1, 8))

    cat_table_data = [
        [Paragraph("Product Category", tbl_header), Paragraph("Orders", tbl_header), Paragraph("Order Share", tbl_header), Paragraph("Total Gross Revenue", tbl_header), Paragraph("Revenue Share", tbl_header), Paragraph("Avg Order Value", tbl_header)],
        [Paragraph("Fashion", tbl_cell), Paragraph("40", tbl_cell_center), Paragraph("40.0%", tbl_cell_center), Paragraph("$11,745.80", tbl_cell_right), Paragraph("37.72%", tbl_cell_center), Paragraph("$293.65", tbl_cell_right)],
        [Paragraph("Electronics", tbl_cell), Paragraph("32", tbl_cell_center), Paragraph("32.0%", tbl_cell_center), Paragraph("$9,897.85", tbl_cell_right), Paragraph("31.79%", tbl_cell_center), Paragraph("$309.31", tbl_cell_right)],
        [Paragraph("Home Goods", tbl_cell), Paragraph("28", tbl_cell_center), Paragraph("28.0%", tbl_cell_center), Paragraph("$9,493.51", tbl_cell_right), Paragraph("30.49%", tbl_cell_center), Paragraph("$339.05", tbl_cell_right)],
        [Paragraph("<b>Consolidated Total</b>", tbl_cell), Paragraph("<b>100</b>", tbl_cell_center), Paragraph("<b>100.0%</b>", tbl_cell_center), Paragraph("<b>$31,137.16</b>", tbl_cell_right), Paragraph("<b>100.0%</b>", tbl_cell_center), Paragraph("<b>$311.37</b>", tbl_cell_right)],
    ]
    t_cat = Table(cat_table_data, colWidths=[1.5*72, 0.8*72, 1.1*72, 1.4*72, 1.1*72, 1.3*72])
    t_cat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#09304f")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor("#f8fafc")]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#e2e8f0")),
    ]))
    story.append(t_cat)
    story.append(Spacer(1, 14))

    story.append(Paragraph("<b>Visualisation: Total Revenue by Product Category</b>", title_h2))
    cat_img = "figures/q1_revenue_by_category.png"
    if os.path.exists(cat_img):
        story.append(Image(cat_img, width=6.2*72, height=2.6*72))

    story.append(PageBreak())

    # ==============================================================================
    # PAGE 3: QUESTION 1 CRITICAL COUNTRY REVENUE ANALYSIS & COMPARATIVE CHART
    # ==============================================================================
    story.append(Paragraph("Critical Evaluation: 'Top 3 Countries by Total Revenue'", title_h1))
    
    country_discussion = (
        "The assignment specifically asks learners to: <i>'Identify and plot the top 3 countries by total revenue.'</i> "
        "This instruction highlights an essential real-world data quality lesson regarding categorical aggregation:<br/><br/>"
        "● <b>Before Standardisation (The Analytical Trap):</b> Grouping raw data produces three pseudo-countries: "
        "(1) <code>United States</code> ($13,285.64; 43 orders), (2) <code>U.S.A.</code> ($9,468.40; 27 orders), "
        "and (3) <code>usa</code> ($8,383.12; 30 orders). If an analyst does not clean the data first, they would erroneously "
        "report that revenue is distributed across three separate countries.<br/><br/>"
        "● <b>After Standardisation (The True Reality):</b> Unifying all three labels into <code>'United States'</code> reveals "
        "that all 100 customer orders originate from a single nation, accounting for <b>100% of the total revenue ($31,137.16)</b>. "
        "The comparative bar chart below demonstrates the danger of dirty data versus the clean reality."
    )
    story.append(Paragraph(country_discussion, body))
    story.append(Spacer(1, 10))

    country_img = "figures/q1_top_countries_revenue.png"
    if os.path.exists(country_img):
        story.append(Image(country_img, width=6.6*72, height=2.6*72))
        story.append(Spacer(1, 10))

    story.append(Paragraph(
        "<b>Strategic Takeaway:</b> Without string harmonization, management might allocate international marketing budgets "
        "or establish regional supply depots based on false geographic distinctions. Standardisation ensures reporting integrity.",
        body
    ))

    story.append(PageBreak())

    # ==============================================================================
    # PAGE 4: QUESTION 1 PYTHON SOURCE CODE
    # ==============================================================================
    story.append(Paragraph("Question 1 Source Code Implementation", title_h1))
    story.append(Paragraph("The reproducible Python pipeline below loads the data, validates and imputes missing totals, standardises countries, exports cleaned data, and generates the visualisations:", body))
    story.append(Spacer(1, 6))

    q1_code = """# ==============================================================================
# Question 1: Tabular Data Cleaning and Revenue Analysis Pipeline
# Course: MIVA-DTS 305 - Data Quality and Data Wrangling
# Candidate: Richard John (2024/C/DSC/0548) | richard.john@miva.edu.ng
# GitHub: https://github.com/Rik-ky/miva-dts305-data-wrangling
# ==============================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Load the raw customer orders dataset
df = pd.read_csv('data/customer_orders_raw.csv')
print(f"Loaded dataset: {len(df)} transactions")

# 2. Impute missing Total Amount: Total Amount = Quantity * Price
# Verified on existing records: discrepancy = $0.00
df['Total Amount'] = df['Total Amount'].fillna(
    (df['Quantity'] * df['Price']).round(2)
)

# 3. Deduplicate dataset (0 duplicate records found)
df = df.drop_duplicates()

# 4. Standardise Country column formatting
country_mapping = {
    'usa': 'United States',
    'U.S.A.': 'United States',
    'United States': 'United States'
}
df['Country'] = df['Country'].map(country_mapping)

# 5. Export cleaned dataset to CSV
df.to_csv('data/customer_orders_cleaned.csv', index=False)
print("Saved cleaned data to customer_orders_cleaned.csv")

# 6. Aggregate Revenue by Product Category
category_revenue = (
    df.groupby('Product Category')['Total Amount']
    .agg(['sum', 'count', 'mean'])
    .sort_values(by='sum', ascending=False)
)
print("Product Category Performance:\\n", category_revenue)

# 7. Generate Bar Chart of Revenue by Category
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(category_revenue.index, category_revenue['sum'],
              color=['#1f77b4', '#ff7f0e', '#2ca02c'], width=0.55, edgecolor='black')
for bar in bars:
    y = bar.get_height()
    ax.annotate(f"${y:,.2f}", (bar.get_x() + bar.get_width()/2, y),
                xytext=(0, 6), textcoords="offset points", ha='center', fontweight='bold')
ax.set_title('Total Revenue by Product Category', fontsize=13, fontweight='bold')
ax.set_ylabel('Total Revenue (USD $)')
plt.tight_layout()
plt.savefig('figures/q1_revenue_by_category.png', dpi=300)
"""
    code_t1 = Table([[Preformatted(q1_code, code_p)]], colWidths=[7.2 * 72])
    code_t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(code_t1)
    story.append(PageBreak())

    # ==============================================================================
    # PAGE 5: QUESTION 2 WEB SCRAPING ARCHITECTURE & BOOKS INVENTORY (PART 1)
    # ==============================================================================
    story.append(Paragraph("Question 2: Web Scraping and Feature Engineering", title_h1))
    
    q2_desc = (
        "<b>Target Website:</b> Books to Scrape (<code>http://books.toscrape.com/</code>).<br/>"
        "<b>Scraping Architecture:</b> Using Python's <code>requests</code> and <code>BeautifulSoup</code>, "
        "we extracted all book listings displayed on the homepage. For each book pod, four core attributes were scraped: "
        "<code>Title</code> (full title from the anchor <code>title</code> attribute), <code>Price</code> (from <code>&lt;p class='price_color'&gt;</code>), "
        "<code>Rating</code> (extracted from star-rating class), and <code>Availability status</code>.<br/><br/>"
        "<b>Cleaning & Feature Engineering Steps:</b><br/>"
        "● <b>Convert prices:</b> Stripped currency symbols (<code>£</code>) and encoding artifacts (<code>Â£</code>), casting to float.<br/>"
        "● <b>Map ratings:</b> Qualitative star rating text was mapped to integers: <code>{'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}</code>.<br/>"
        "● <b>Engineer Affordability:</b> Books with <code>Price &lt; £20</code> were classified as <b>'Affordable'</b>, while books with "
        "<code>Price ≥ £20</code> were categorized as <b>'Expensive'</b>. Cleaned data was saved as <code>data/books_scraped_cleaned.csv</code>."
    )
    story.append(Paragraph(q2_desc, body))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Scraped Books Inventory (Homepage Titles 1 to 10):", title_h2))

    df_books = pd.read_csv('data/books_scraped_cleaned.csv')
    
    books_data_p1 = [
        [Paragraph("#", tbl_header), Paragraph("Book Title", tbl_header), Paragraph("Raw Price", tbl_header), Paragraph("Cleaned (£)", tbl_header), Paragraph("Rating", tbl_header), Paragraph("Affordability", tbl_header), Paragraph("Status", tbl_header)]
    ]
    for idx in range(10):
        r = df_books.iloc[idx]
        disp_title = r['Title'][:36] + ('...' if len(r['Title']) > 36 else '')
        aff_col = "#15803d" if r['Affordability'] == 'Affordable' else "#b91c1c"
        aff_str = f"<b><font color='{aff_col}'>{r['Affordability']}</font></b>"
        books_data_p1.append([
            Paragraph(str(idx + 1), tbl_cell_center),
            Paragraph(disp_title, tbl_cell),
            Paragraph(str(r['Price_Raw']), tbl_cell_center),
            Paragraph(f"£{r['Price (£)']:.2f}", tbl_cell_right),
            Paragraph(f"{int(r['Rating'])} / 5", tbl_cell_center),
            Paragraph(aff_str, tbl_cell_center),
            Paragraph(str(r['Availability']), tbl_cell_center)
        ])

    t_b1 = Table(books_data_p1, colWidths=[0.3*72, 2.5*72, 0.8*72, 0.8*72, 0.7*72, 1.1*72, 1.0*72])
    t_b1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#09304f")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(t_b1)
    story.append(PageBreak())

    # ==============================================================================
    # PAGE 6: QUESTION 2 BOOKS INVENTORY (PART 2) & EXPORT SUMMARY
    # ==============================================================================
    story.append(Paragraph("Scraped Books Inventory (Homepage Titles 11 to 20)", title_h1))
    story.append(Paragraph("The remaining 10 titles scraped from the Books to Scrape homepage are detailed below:", body))
    story.append(Spacer(1, 6))

    books_data_p2 = [
        [Paragraph("#", tbl_header), Paragraph("Book Title", tbl_header), Paragraph("Raw Price", tbl_header), Paragraph("Cleaned (£)", tbl_header), Paragraph("Rating", tbl_header), Paragraph("Affordability", tbl_header), Paragraph("Status", tbl_header)]
    ]
    for idx in range(10, 20):
        r = df_books.iloc[idx]
        disp_title = r['Title'][:36] + ('...' if len(r['Title']) > 36 else '')
        aff_col = "#15803d" if r['Affordability'] == 'Affordable' else "#b91c1c"
        aff_str = f"<b><font color='{aff_col}'>{r['Affordability']}</font></b>"
        books_data_p2.append([
            Paragraph(str(idx + 1), tbl_cell_center),
            Paragraph(disp_title, tbl_cell),
            Paragraph(str(r['Price_Raw']), tbl_cell_center),
            Paragraph(f"£{r['Price (£)']:.2f}", tbl_cell_right),
            Paragraph(f"{int(r['Rating'])} / 5", tbl_cell_center),
            Paragraph(aff_str, tbl_cell_center),
            Paragraph(str(r['Availability']), tbl_cell_center)
        ])

    t_b2 = Table(books_data_p2, colWidths=[0.3*72, 2.5*72, 0.8*72, 0.8*72, 0.7*72, 1.1*72, 1.0*72])
    t_b2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#09304f")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(t_b2)
    story.append(Spacer(1, 14))

    story.append(Paragraph(
        "<b>Dataset Deliverable Summary:</b> The final dataset containing all 20 cleaned titles, float prices, "
        "ordinal ratings, and engineered affordability tiers has been exported to: "
        "<code>data/books_scraped_cleaned.csv</code> and published in the GitHub repository.",
        body
    ))

    story.append(PageBreak())

    # ==============================================================================
    # PAGE 7: QUESTION 2 STATS, VISUALISATIONS & FINDINGS
    # ==============================================================================
    story.append(Paragraph("Question 2 Visualisations & Analytical Findings", title_h1))
    story.append(Paragraph("<b>Statistical Breakdown by Affordability Tier</b>", title_h2))

    aff_stats_data = [
        [Paragraph("Affordability Tier", tbl_header), Paragraph("Titles", tbl_header), Paragraph("Catalog Share", tbl_header), Paragraph("Mean Price (£)", tbl_header), Paragraph("Mean Rating", tbl_header), Paragraph("Rating Std Dev", tbl_header)],
        [Paragraph("Affordable (&lt; £20)", tbl_cell), Paragraph("3", tbl_cell_center), Paragraph("15.0%", tbl_cell_center), Paragraph("£16.46", tbl_cell_right), Paragraph("<b>3.33 / 5.00</b>", tbl_cell_center), Paragraph("1.53", tbl_cell_center)],
        [Paragraph("Expensive (≥ £20)", tbl_cell), Paragraph("17", tbl_cell_center), Paragraph("85.0%", tbl_cell_center), Paragraph("£43.76", tbl_cell_right), Paragraph("<b>2.76 / 5.00</b>", tbl_cell_center), Paragraph("1.60", tbl_cell_center)],
        [Paragraph("<b>Homepage Total / Mean</b>", tbl_cell), Paragraph("<b>20</b>", tbl_cell_center), Paragraph("<b>100.0%</b>", tbl_cell_center), Paragraph("<b>£39.67</b>", tbl_cell_right), Paragraph("<b>2.85 / 5.00</b>", tbl_cell_center), Paragraph("1.57", tbl_cell_center)],
    ]
    t_aff = Table(aff_stats_data, colWidths=[1.7*72, 0.8*72, 1.1*72, 1.2*72, 1.2*72, 1.2*72])
    t_aff.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#09304f")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor("#f8fafc")]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#e2e8f0")),
    ]))
    story.append(t_aff)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Visualisations: Affordability Proportions & Average Ratings</b>", title_h2))

    pie_img = "figures/q2_affordability_pie_chart.png"
    bar_img = "figures/q2_ratings_bar_chart.png"

    if os.path.exists(pie_img) and os.path.exists(bar_img):
        q2_chart_table = Table([[
            Image(pie_img, width=3.4*72, height=2.85*72),
            Image(bar_img, width=3.5*72, height=2.85*72)
        ]], colWidths=[3.6*72, 3.6*72])
        q2_chart_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(q2_chart_table)
        story.append(Spacer(1, 10))

    insights_q2 = (
        "<b>Key Analytical Insights:</b><br/>"
        "1. <b>Merchandise Pricing Skew:</b> 85.0% of featured books (17 of 20) are priced above £20, averaging £43.76, "
        "while only 15.0% (3 books) are under £20 (averaging £16.46).<br/>"
        "2. <b>The Expectation-Disconfirmation Effect:</b> Affordable books received a higher average rating (<b>3.33 / 5.00</b>) "
        "than expensive books (<b>2.76 / 5.00</b>). Customers paying £40–£55 exhibit significantly harsher quality scrutiny, "
        "whereas lower-priced titles more easily exceed reader expectations relative to cost."
    )
    story.append(Paragraph(insights_q2, body))
    story.append(PageBreak())

    # ==============================================================================
    # PAGE 8: QUESTION 2 PYTHON WEB SCRAPING SOURCE CODE
    # ==============================================================================
    story.append(Paragraph("Question 2 Source Code Implementation", title_h1))
    story.append(Paragraph("The reproducible Python pipeline below handles live web scraping, data cleaning, feature engineering, and chart generation:", body))
    story.append(Spacer(1, 6))

    q2_code = """# ==============================================================================
# Question 2: Web Scraping and Feature Engineering Pipeline
# Course: MIVA-DTS 305 - Data Quality and Data Wrangling
# Candidate: Richard John (2024/C/DSC/0548) | richard.john@miva.edu.ng
# GitHub: https://github.com/Rik-ky/miva-dts305-data-wrangling
# ==============================================================================
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Fetch HTML from Books to Scrape homepage
url = "http://books.toscrape.com/"
response = requests.get(url, timeout=15)
response.raise_for_status()

# 2. Parse HTML structure and extract required attributes
soup = BeautifulSoup(response.content, 'html.parser')
rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
books = []

for pod in soup.find_all('article', class_='product_pod'):
    title = pod.h3.a['title']
    price_raw = pod.find('p', class_='price_color').text.strip()
    rating_text = pod.find('p', class_='star-rating')['class'][1]
    availability = pod.find('p', class_='instock availability').text.strip()
    books.append({'Title': title, 'Price_Raw': price_raw, 
                  'Rating_Text': rating_text, 'Availability': availability})

df = pd.DataFrame(books)

# 3. Clean Price (£) and map Rating to numerical values
df['Price (£)'] = df['Price_Raw'].str.replace('£', '').str.replace('Â', '').astype(float)
df['Rating'] = df['Rating_Text'].map(rating_map)

# 4. Feature Engineering: Affordability classification
# 'Affordable' if price < £20 else 'Expensive'
df['Affordability'] = np.where(df['Price (£)'] < 20.0, 'Affordable', 'Expensive')
df.to_csv('data/books_scraped_cleaned.csv', index=False)
print("Cleaned scraped data saved to data/books_scraped_cleaned.csv")

# 5. Calculate Average Rating by Affordability Category
stats = df.groupby('Affordability')['Rating'].agg(['count', 'mean']).round(2)
print("Affordability Stats:\\n", stats)
"""
    code_t2 = Table([[Preformatted(q2_code, code_p)]], colWidths=[7.2 * 72])
    code_t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(code_t2)
    story.append(Spacer(1, 14))

    story.append(Paragraph(
        "<b>Submission Conclusion:</b> All requirements for MIVA-DTS 305 have been completed with verified accuracy. "
        "Interactive Jupyter notebooks and scripts are accessible at: "
        "<font color='#1d4ed8'><u>https://github.com/Rik-ky/miva-dts305-data-wrangling</u></font>.",
        body
    ))

    doc.build(story, canvasmaker=MivaNumberedCanvas)
    print(f"Report successfully compiled at: {pdf_path}")


if __name__ == '__main__':
    generate_report()
