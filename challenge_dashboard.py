"""
Challenge Level 1: Interactive KPI Dashboard
Generates a dynamic HTML dashboard using Plotly Express.
"""

import os
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

def get_engine():
    """Create a SQLAlchemy engine connected to the amman_market database."""
    default_url = "postgresql+psycopg://postgres:postgres@localhost:5432/amman_market"
    database_url = os.getenv("DATABASE_URL", default_url)
    return create_engine(database_url)

def create_interactive_dashboard():
    engine = get_engine()
    print("--- Challenge Level 1: Generating Interactive Plotly Dashboard ---")
    
    try:
        # 1. Extraction
        orders = pd.read_sql("SELECT * FROM orders WHERE status != 'cancelled'", engine)
        order_items = pd.read_sql("SELECT * FROM order_items", engine)
        products = pd.read_sql("SELECT * FROM products", engine)
        
        # 2. Data Preparation
        orders['order_date'] = pd.to_datetime(orders['order_date'])
        df = order_items.merge(products, on='product_id').merge(orders, on='order_id')
        df['revenue'] = df['quantity'] * df['unit_price']

        # 3. Interactive Plot: Monthly Revenue Growth
        monthly_df = df.set_index('order_date').resample('ME')['revenue'].sum().reset_index()
        fig1 = px.line(monthly_df, x='order_date', y='revenue', 
                      title='Dynamic Monthly Revenue Growth (JOD)',
                      labels={'revenue': 'Total Revenue', 'order_date': 'Month'},
                      markers=True,
                      template='plotly_dark') # Professional dark theme

        # 4. Interactive Plot: Revenue by Category
        cat_df = df.groupby('category')['revenue'].sum().sort_values(ascending=False).reset_index()
        fig2 = px.bar(cat_df, x='category', y='revenue', 
                     color='revenue',
                     title='Revenue Performance by Category',
                     labels={'revenue': 'Revenue (JOD)', 'category': 'Product Category'},
                     color_continuous_scale='Viridis')

        # 5. Exporting to HTML (Unified Dashboard)
        os.makedirs("output", exist_ok=True)
        dashboard_file = 'output/interactive_dashboard.html'
        
        with open(dashboard_file, 'w', encoding='utf-8') as f:
            f.write("<html><head><title>Amman Market Interactive Dashboard</title></head><body>")
            f.write("<h1 style='text-align: center; font-family: Arial;'>Amman Digital Market: Interactive Analysis</h1>")
            f.write(fig1.to_html(full_html=False, include_plotlyjs='cdn'))
            f.write("<br><hr><br>")
            f.write(fig2.to_html(full_html=False, include_plotlyjs='cdn'))
            f.write("</body></html>")

        print(f"Success! Interactive dashboard saved to: {dashboard_file}")
        print("Tip: Open this file in your browser to interact with the charts.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_interactive_dashboard()