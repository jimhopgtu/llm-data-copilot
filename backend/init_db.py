"""
Initialize sample SQLite database with e-commerce data
Run this once to set up your database: python init_db.py
"""

import sqlite3
from datetime import datetime, timedelta
import random

DB_PATH = "sample.db"

def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_date DATE NOT NULL,
            customer_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            total DECIMAL(10,2) NOT NULL,
            channel TEXT NOT NULL
        )
    """)
    
    # Create customers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            signup_date DATE NOT NULL,
            total_orders INTEGER DEFAULT 0
        )
    """)
    
    print("✅ Tables created")
    
    # Insert sample customers
    customers = [
        ("Alice Johnson", "alice@example.com", "2023-01-15"),
        ("Bob Smith", "bob@example.com", "2023-02-20"),
        ("Carol White", "carol@example.com", "2023-03-10"),
        ("David Brown", "david@example.com", "2023-04-05"),
        ("Eve Davis", "eve@example.com", "2023-05-12"),
    ]
    
    cursor.executemany(
        "INSERT INTO customers (name, email, signup_date) VALUES (?, ?, ?)",
        customers
    )
    print(f"✅ Inserted {len(customers)} customers")
    
    # Insert sample orders
    products = [
        ("Laptop", "Electronics", 999.99),
        ("Wireless Mouse", "Electronics", 29.99),
        ("Office Chair", "Furniture", 299.99),
        ("Standing Desk", "Furniture", 599.99),
        ("Notebook Set", "Office Supplies", 15.99),
        ("Coffee Maker", "Appliances", 89.99),
        ("Headphones", "Electronics", 149.99),
    ]
    
    channels = ["Website", "Mobile App", "In-Store", "Phone"]
    
    orders = []
    base_date = datetime(2024, 1, 1)
    
    for i in range(200):  # Generate 200 orders
        order_date = base_date + timedelta(days=random.randint(0, 364))
        customer_id = random.randint(1, 5)
        product_name, category, price = random.choice(products)
        quantity = random.randint(1, 5)
        total = round(price * quantity, 2)
        channel = random.choice(channels)
        
        orders.append((
            order_date.strftime("%Y-%m-%d"),
            customer_id,
            product_name,
            category,
            quantity,
            price,
            total,
            channel
        ))
    
    cursor.executemany("""
        INSERT INTO orders 
        (order_date, customer_id, product_name, category, quantity, price, total, channel)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, orders)
    
    print(f"✅ Inserted {len(orders)} orders")
    
    # Update customer order counts
    cursor.execute("""
        UPDATE customers 
        SET total_orders = (
            SELECT COUNT(*) FROM orders WHERE orders.customer_id = customers.id
        )
    """)
    
    conn.commit()
    conn.close()
    
    print("\n🎉 Database initialized successfully!")
    print(f"📁 Location: {DB_PATH}")
    print("\nSample queries to try:")
    print("  - SELECT * FROM orders LIMIT 5")
    print("  - SELECT category, SUM(total) as revenue FROM orders GROUP BY category")
    print("  - SELECT channel, COUNT(*) as order_count FROM orders GROUP BY channel")

if __name__ == "__main__":
    create_database()