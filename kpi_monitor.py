import pandas as pd
import json
import os
from sqlalchemy import create_engine

def get_status(actual, target):
    """Returns a status indicator based on performance vs target."""
    if actual >= target:
        return "🟢 EXCEEDED"
    elif actual >= target * 0.8:
        return "🟡 ON TRACK"
    else:
        return "🔴 UNDERPERFORMING"

def monitor_performance():
    print("--- Challenge Level 2: KPI Automated Monitoring ---")
    
    engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5432/amman_market")
    
    with open('config.json', 'r') as f:
        targets = json.load(f)

    # Updated logic to match your working analysis.py
    # Join order_items with products to get the correct price column
    df_items = pd.read_sql("SELECT * FROM order_items", engine)
    df_products = pd.read_sql("SELECT * FROM products", engine)
    df_orders = pd.read_sql("SELECT * FROM orders WHERE status != 'cancelled'", engine)
    
    # Calculate Revenue correctly
    df_combined = df_items.merge(df_products, on='product_id')
    # Check if column is 'unit_price' or 'price' based on your schema
    price_col = 'unit_price' if 'unit_price' in df_combined.columns else 'price'
    df_combined['revenue'] = df_combined['quantity'] * df_combined[price_col]
    
    actual_revenue = df_combined['revenue'].sum()
    actual_orders = df_orders['order_id'].nunique()
    actual_aov = actual_revenue / actual_orders if actual_orders > 0 else 0

    # Print Report
    print("\n" + "="*55)
    print(f"{'KPI NAME':<20} | {'ACTUAL':<12} | {'TARGET':<10} | {'STATUS'}")
    print("-" * 55)
    print(f"{'Total Revenue':<20} | {actual_revenue:<12,.2f} | {targets['revenue_target']:<10} | {get_status(actual_revenue, targets['revenue_target'])}")
    print(f"{'Avg Order Value':<20} | {actual_aov:<12,.2f} | {targets['aov_target']:<10} | {get_status(actual_aov, targets['aov_target'])}")
    print("="*55)

if __name__ == "__main__":
    monitor_performance()