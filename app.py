"""
Challenge Level 3: Multi-Page Analytic Report with Plotly Dash
Creates a local web server to host the Amman Market Dashboard.
"""
from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os

# Initialize the Dash app
app = Dash(__name__)

# Data Connection
engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5432/amman_market")

def load_data():
    # Fetch data for dashboarding
    df_items = pd.read_sql("SELECT * FROM order_items", engine)
    df_products = pd.read_sql("SELECT * FROM products", engine)
    df_orders = pd.read_sql("SELECT * FROM orders WHERE status != 'cancelled'", engine)
    
    # Merge and Clean
    df = df_items.merge(df_products, on='product_id').merge(df_orders, on='order_id')
    df['revenue'] = df['quantity'] * df['unit_price']
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

# Create Visuals
# Page 1: Revenue Trends
monthly_rev = df.set_index('order_date').resample('ME')['revenue'].sum().reset_index()
fig_rev = px.area(monthly_rev, x='order_date', y='revenue', title='Revenue Growth Over Time')

# Page 2: Category Analysis
fig_cat = px.sunburst(df, path=['category', 'product_name'], values='revenue',
                      title='Revenue Distribution by Category and Product')

# Dashboard Layout
app.layout = html.Div(style={'fontFamily': 'Arial', 'padding': '20px'}, children=[
    html.H1("Amman Digital Market - Advanced Analytics Portal", style={'textAlign': 'center', 'color': '#2c3e50'}),
    html.Hr(),
    
    html.Div([
        html.H3("Overview: Financial Performance"),
        dcc.Graph(figure=fig_rev)
    ], style={'marginBottom': '50px'}),
    
    html.Div([
        html.H3("Deep Dive: Product & Category Breakdown"),
        dcc.Graph(figure=fig_cat)
    ])
])

if __name__ == '__main__':
    print("Starting the Dash server... Access it at http://127.0.0.1:8050")
    app.run(debug=True)