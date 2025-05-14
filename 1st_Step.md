### Step 1: **Understanding the Brief**
The goal of this project is to:
- **Design and implement an architecture with two services**: 
  - One service for executing scripts (importing data).
  - Another service for storing data using **SQLite**.
- **Analyze provided datasets** (sales, products, stores).
- **Create a relational database** structure.
- **Import and process data** while ensuring duplicate sales entries are avoided.
- **Perform SQL queries** for business analysis (total revenue, product sales, regional sales).
- **Store results** in the database.

Now, let’s go step by step to implement the solution.

---

### Step 2: **Designing the Architecture**
#### Architecture Diagram:
You need to design a system with two services:
1. **Script Execution Service** (e.g., using Python) 
   - Handles data import & processing.
   - Connects to SQLite database.
2. **Database Service** (SQLite)
   - Stores data and executes SQL queries.

Key components:
- **Docker** will be used to containerize both services.
- **Docker Compose** to orchestrate service startup.

#### Communication Flow:
- **Script Execution Service → SQLite Database**:
  - The script reads CSV files from the URLs.
  - Imports data into SQLite database.
  - Runs SQL queries for analysis.

---

### Step 3: **Building the Architecture**
#### Docker Setup:
1. **Create the Dockerfile for script execution:**
   ```Dockerfile
   # Use Python as the base image
   FROM python:3.10

   # Set working directory
   WORKDIR /app

   # Copy scripts into the container
   COPY . /app

   # Install dependencies
   RUN pip install pandas sqlite3 requests

   # Run the script
   CMD ["python", "main.py"]
   ```

2. **Create the Docker Compose file (`docker-compose.yml`):**
   ```yaml
   version: '3'
   services:
     database:
       image: nouchka/sqlite3
       container_name: sqlite_db
     script:
       build: .
       container_name: data_script
       depends_on:
         - database
   ```

---

### Step 4: **Defining the Database Schema**
You need a **relational database schema** in SQLite:
#### Tables:
1. **Products Table**
   ```sql
   CREATE TABLE products (
       product_id INTEGER PRIMARY KEY,
       name TEXT,
       category TEXT,
       price REAL
   );
   ```
2. **Stores Table**
   ```sql
   CREATE TABLE stores (
       store_id INTEGER PRIMARY KEY,
       name TEXT,
       city TEXT,
       region TEXT
   );
   ```
3. **Sales Table** (Avoid duplicate imports)
   ```sql
   CREATE TABLE sales (
       sale_id INTEGER PRIMARY KEY,
       date TEXT,
       store_id INTEGER,
       product_id INTEGER,
       quantity INTEGER,
       revenue REAL,
       UNIQUE(date, store_id, product_id) -- Ensures no duplicate entries
   );
   ```

---

### Step 5: **Importing Data into SQLite**
Write a Python script (`main.py`) to:
1. Download CSV files using **requests**.
2. Read data using **pandas**.
3. Insert data into SQLite while checking for duplicates.

Example:
```python
import pandas as pd
import sqlite3
import requests

# Connect to database
conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

# Load CSV from URL
url = "https://example.com/sales.csv"
response = requests.get(url)
with open("sales.csv", "w") as file:
    file.write(response.text)

# Read CSV
df = pd.read_csv("sales.csv")

# Insert data (avoiding duplicates)
for _, row in df.iterrows():
    cursor.execute("""
        INSERT OR IGNORE INTO sales (date, store_id, product_id, quantity, revenue)
        VALUES (?, ?, ?, ?, ?)""",
        (row["date"], row["store_id"], row["product_id"], row["quantity"], row["revenue"])
    )

conn.commit()
conn.close()
```

---

### Step 6: **Performing Data Analysis with SQL**
Run queries to analyze sales:
1. **Total Revenue**
   ```sql
   SELECT SUM(revenue) AS total_revenue FROM sales;
   ```
2. **Sales per Product**
   ```sql
   SELECT product_id, SUM(quantity) AS total_sold FROM sales GROUP BY product_id;
   ```
3. **Sales by Region**
   ```sql
   SELECT stores.region, SUM(sales.revenue) AS total_revenue 
   FROM sales 
   JOIN stores ON sales.store_id = stores.store_id 
   GROUP BY stores.region;
   ```

---

### Step 7: **Deliverables & Submission**
You need to prepare:
✅ **Architecture Diagram**
✅ **Database Schema**
✅ **Dockerfile**
✅ **Docker Compose YAML**
✅ **Python Data Processing Scripts**
✅ **SQL Queries**
✅ **Summary of Analysis Results**

💾 **How to Submit?**
- Git repository (**recommended**).
- Cloud storage link.
- USB drive or personal laptop.
