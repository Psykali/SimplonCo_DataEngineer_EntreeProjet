import sqlite3
import requests
import pandas as pd
from datetime import datetime

# Database setup
def setup_database():
    conn = sqlite3.connect('data/sales.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price REAL,
        category TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stores (
        id INTEGER PRIMARY KEY,
        city TEXT,
        region TEXT,
        address TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY,
        product_id INTEGER,
        store_id INTEGER,
        sale_date TEXT,
        quantity INTEGER,
        amount REAL,
        FOREIGN KEY (product_id) REFERENCES products(id),
        FOREIGN KEY (store_id) REFERENCES stores(id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS analysis_results (
        id INTEGER PRIMARY KEY,
        analysis_type TEXT,
        result_value REAL,
        result_details TEXT,
        created_at TEXT
    )
    ''')
    
    conn.commit()
    return conn

# Data import functions
def import_products(conn, url):
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    
    # Check for existing records
    existing = pd.read_sql('SELECT id FROM products', conn)
    new_records = df[~df['id'].isin(existing['id'])]
    
    if not new_records.empty:
        new_records.to_sql('products', conn, if_exists='append', index=False)
        print(f"Imported {len(new_records)} new product records")
    else:
        print("No new product records to import")

def import_sales(conn, url):
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    
    # Convert date format if needed
    df['sale_date'] = pd.to_datetime(df['sale_date']).dt.strftime('%Y-%m-%d')
    
    # Check for existing records
    existing = pd.read_sql('SELECT id FROM sales', conn)
    new_records = df[~df['id'].isin(existing['id'])]
    
    if not new_records.empty:
        new_records.to_sql('sales', conn, if_exists='append', index=False)
        print(f"Imported {len(new_records)} new sales records")
    else:
        print("No new sales records to import")

# Analysis functions
def run_sales_analysis(conn):
    cursor = conn.cursor()
    
    # Total revenue
    cursor.execute('SELECT SUM(amount) FROM sales')
    total_revenue = cursor.fetchone()[0]
    
    # Sales by product
    product_sales = pd.read_sql('''
    SELECT p.name, SUM(s.amount) as total_sales
    FROM sales s
    JOIN products p ON s.product_id = p.id
    GROUP BY p.name
    ORDER BY total_sales DESC
    ''', conn)
    
    # Sales by region
    region_sales = pd.read_sql('''
    SELECT st.region, SUM(s.amount) as total_sales
    FROM sales s
    JOIN stores st ON s.store_id = st.id
    GROUP BY st.region
    ORDER BY total_sales DESC
    ''', conn)
    
    # Store results
    now = datetime.now().isoformat()
    cursor.execute('''
    INSERT INTO analysis_results 
    (analysis_type, result_value, result_details, created_at)
    VALUES (?, ?, ?, ?)
    ''', ('total_revenue', total_revenue, 'Overall revenue', now))
    
    conn.commit()
    
    return {
        'total_revenue': total_revenue,
        'product_sales': product_sales.to_dict('records'),
        'region_sales': region_sales.to_dict('records')
    }

if __name__ == '__main__':
    # Initialize database
    conn = setup_database()
    
    # Import data (replace with actual URLs)
    import_products(conn, 'http://example.com/products.csv')
    import_sales(conn, 'http://example.com/sales.csv')
    
    # Run analysis
    results = run_sales_analysis(conn)
    print("Analysis Results:")
    print(results)
    
    conn.close()