"""Integration 4 — KPI Dashboard: Amman Digital Market Analytics

Extract data from PostgreSQL, compute KPIs, run statistical tests,
and create visualizations for the executive summary.
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sqlalchemy import create_engine

def connect_db():
    """Create a SQLAlchemy engine connected to the amman_market database."""
    default_url = "postgresql+psycopg://postgres:postgres@localhost:5432/amman_market"
    database_url = os.getenv("DATABASE_URL", default_url)
    return create_engine(database_url)

def extract_data(engine):
    """Task 1: Extract and Clean Data."""
    print("--- Task 1: Extracting and Cleaning Data ---")
    customers = pd.read_sql("SELECT * FROM customers", engine)
    products = pd.read_sql("SELECT * FROM products", engine)
    orders = pd.read_sql("SELECT * FROM orders", engine)
    order_items = pd.read_sql("SELECT * FROM order_items", engine)

    # Data Quality filters
    orders_clean = orders[orders['status'] != 'cancelled'].copy()
    order_items_clean = order_items[order_items['quantity'] <= 100].copy()
    
    return {
        "customers": customers,
        "products": products,
        "orders": orders_clean,
        "order_items": order_items_clean
    }

def compute_kpis(data_dict):
    """Task 2: Compute the 5 KPIs defined in kpi_framework.md."""
    print("--- Task 2: Computing 5 KPIs ---")
    orders = data_dict['orders']
    order_items = data_dict['order_items']
    products = data_dict['products']
    
    # Convert dates
    orders['order_date'] = pd.to_datetime(orders['order_date'])

    # Merging for calculations
    df_items_prod = order_items.merge(products, on='product_id')
    df_items_prod['revenue'] = df_items_prod['quantity'] * df_items_prod['unit_price']
    full_df = df_items_prod.merge(orders, on='order_id')

    # KPI 1: Monthly Revenue Growth
    monthly_revenue = full_df.set_index('order_date').resample('ME')['revenue'].sum()

    # KPI 2: Weekly Order Volume
    weekly_orders = orders.set_index('order_date').resample('W')['order_id'].nunique()

    # KPI 3: Revenue by Product Category
    category_revenue = full_df.groupby('category')['revenue'].sum().sort_values(ascending=False)

    # KPI 4: Average Order Value (AOV)
    total_rev = full_df['revenue'].sum()
    aov = total_rev / orders['order_id'].nunique()

    # KPI 5: Top 5 Best-Selling Products
    top_products = full_df.groupby('product_name')['quantity'].sum().nlargest(5)

    return {
        "total_revenue": total_rev,
        "aov": aov,
        "monthly_revenue": monthly_revenue,
        "weekly_orders": weekly_orders,
        "category_revenue": category_revenue,
        "top_products": top_products
    }

def run_statistical_tests(data_dict):
    """
    Task 3: Run ANOVA test to validate if Average Order Value (AOV) 
    differs significantly across product categories.
    """
    print("--- Task 3: Running Statistical Validation (ANOVA) ---")
    order_items = data_dict['order_items']
    products = data_dict['products']

    # Prepare data: join items with products to get revenue and category
    df = order_items.merge(products, on='product_id')
    df['line_total'] = df['quantity'] * df['unit_price']
    
    # Group by order and category to get AOV components
    group_data = df.groupby(['order_id', 'category'])['line_total'].sum().reset_index()

    # Create groups for ANOVA
    categories = group_data['category'].unique()
    category_groups = [group_data[group_data['category'] == cat]['line_total'] for cat in categories]

    # Perform One-way ANOVA
    f_stat, p_value = stats.f_oneway(*category_groups)

    # Interpretation
    alpha = 0.05
    is_significant = p_value < alpha
    interpretation = "Reject Null Hypothesis: Significant difference across categories." if is_significant \
                     else "Fail to Reject Null Hypothesis: No significant difference found."

    results = {
        "test_name": "One-way ANOVA",
        "f_stat": f_stat,
        "p_value": p_value,
        "interpretation": interpretation
    }
    
    print(f"Test Complete. P-Value: {p_value:.4f}")
    return results

def create_visualizations(kpi_results, stat_results):
    """
    Task 4: Create professional multi-panel visualizations for the Amman Market KPIs.
    Saves the full dashboard and individual plots as PNG files in the output/ directory.
    """
    print("--- Task 4: Generating Professional Visualizations ---")
    
    # Set high-quality styling and colorblind-friendly palette
    sns.set_palette('colorblind')
    plt.style.use('ggplot') 

    # Create a 2x2 Multi-panel Figure
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Amman Digital Market Executive Dashboard', fontsize=22, fontweight='bold', color='#2c3e50')

    # 1. Line Chart: Monthly Revenue Trend (Time-based KPI)
    sns.lineplot(ax=axes[0, 0], x=kpi_results['monthly_revenue'].index.astype(str), 
                 y=kpi_results['monthly_revenue'].values, marker='o', linewidth=3, color='#3498db')
    axes[0, 0].set_title('Monthly Revenue Growth Trend', fontsize=15, pad=10)
    axes[0, 0].set_ylabel('Revenue (JOD)')
    axes[0, 0].set_xlabel('Month End Date')
    axes[0, 0].tick_params(axis='x', rotation=30)

    # 2. Bar Chart: Revenue by Category (Cohort-based KPI)
    sns.barplot(ax=axes[0, 1], x=kpi_results['category_revenue'].index, 
                y=kpi_results['category_revenue'].values, palette='viridis')
    axes[0, 1].set_title('Total Revenue by Product Category', fontsize=15, pad=10)
    axes[0, 1].set_ylabel('Revenue (JOD)')
    axes[0, 1].set_xlabel('Category')

    # 3. Bar Chart: Top 5 Best-Selling Products
    sns.barplot(ax=axes[1, 0], x=kpi_results['top_products'].values, 
                y=kpi_results['top_products'].index, palette='magma')
    axes[1, 0].set_title('Top 5 Best-Selling Products (Quantity)', fontsize=15, pad=10)
    axes[1, 0].set_xlabel('Units Sold')
    axes[1, 0].set_ylabel('Product Name')

    # 4. Area Chart: Weekly Order Volume (Time-based KPI)
    kpi_results['weekly_orders'].plot(kind='area', ax=axes[1, 1], alpha=0.4, color='#e67e22')
    axes[1, 1].set_title('Weekly Order Volume Activity', fontsize=15, pad=10)
    axes[1, 1].set_ylabel('Number of Unique Orders')
    axes[1, 1].set_xlabel('Week')

    # Adjust layout to prevent overlapping
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Save the consolidated dashboard
    dashboard_output = 'output/executive_dashboard.png'
    plt.savefig(dashboard_output, dpi=300)
    
    print(f"Dashboard generated successfully at: {dashboard_output}")

def main():
    os.makedirs("output", exist_ok=True)
    engine = connect_db()

    try:
        # 1. Extraction (Task 1)
        data_dict = extract_data(engine)
        
        # 2. KPIs (Task 2)
        kpi_results = compute_kpis(data_dict)
        
        # 3. Statistical Test (Task 3)
        stat_results = run_statistical_tests(data_dict)
        
        # 4. Final Summary Print
        print("\n" + "="*40)
        print("      FINAL ANALYSIS SUMMARY")
        print("="*40)
        print(f"Total Revenue:         {kpi_results['total_revenue']:,.2f} JOD")
        print(f"P-Value (ANOVA):       {stat_results['p_value']:.4f}")
        print(f"Stat Finding:          {stat_results['interpretation']}")
        print("="*40)

        # 5. Visualizations (Task 4) - تم تفعيل السطر هنا
        create_visualizations(kpi_results, stat_results)
        
        print("\nPipeline executed successfully. Check the 'output/' folder for results.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()