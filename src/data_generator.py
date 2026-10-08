from pathlib import Path
import random
import numpy as np
import pandas as pd

def generate_data(n=1500, output_path="data/ecommerce_sales.csv", seed=42):
    random.seed(seed)
    np.random.seed(seed)

    dates = pd.date_range("2025-01-01", "2025-12-31", freq="D")
    products = [
        ("Laptop Pro 14", "Electronics", 850, 0.18),
        ("Wireless Headphones", "Electronics", 120, 0.25),
        ("Smartphone X", "Electronics", 650, 0.15),
        ("Smart Watch", "Electronics", 180, 0.22),
        ("Bluetooth Speaker", "Electronics", 75, 0.28),
        ("Running Shoes", "Fashion", 90, 0.35),
        ("Denim Jacket", "Fashion", 65, 0.32),
        ("Cotton T-Shirt", "Fashion", 25, 0.40),
        ("Backpack", "Fashion", 45, 0.30),
        ("Coffee Maker", "Home & Kitchen", 110, 0.24),
        ("Air Fryer", "Home & Kitchen", 140, 0.20),
        ("Water Bottle", "Home & Kitchen", 22, 0.42),
        ("Desk Lamp", "Home & Kitchen", 35, 0.38),
        ("Notebook Set", "Stationery", 15, 0.45),
        ("Office Chair", "Furniture", 210, 0.20),
    ]
    regions = ["North", "South", "East", "West", "Central"]
    cities = {
        "North": ["Delhi", "Chandigarh", "Jaipur"],
        "South": ["Hyderabad", "Bengaluru", "Chennai"],
        "East": ["Kolkata", "Bhubaneswar", "Patna"],
        "West": ["Mumbai", "Pune", "Ahmedabad"],
        "Central": ["Bhopal", "Nagpur", "Indore"],
    }
    payment_methods = ["Credit Card", "UPI", "Debit Card", "Net Banking", "Cash on Delivery"]
    segments = ["New", "Regular", "Loyal"]
    genders = ["Male", "Female", "Other"]

    rows = []
    for i in range(n):
        date = random.choice(dates)
        product, category, base_price, margin = random.choice(products)
        region = random.choice(regions)
        city = random.choice(cities[region])
        segment = random.choices(segments, weights=[35, 45, 20])[0]
        gender = random.choice(genders)
        quantity = random.choices([1, 2, 3, 4, 5], weights=[42, 30, 17, 8, 3])[0]
        discount = random.choice([0, .05, .10, .15, .20])
        unit_price = round(base_price * np.random.uniform(.92, 1.08), 2)
        sales = round(unit_price * quantity * (1 - discount), 2)
        profit = round(sales * margin * np.random.uniform(.85, 1.15), 2)
        rows.append([
            f"ORD{100001+i}", date, f"C{random.randint(1001,1250)}",
            random.randint(18,65), gender, segment, product, category,
            region, city, quantity, unit_price, discount, sales, profit,
            random.choice(payment_methods)
        ])

    columns = [
        "Order_ID", "Order_Date", "Customer_ID", "Age", "Gender",
        "Customer_Segment", "Product", "Category", "Region", "City",
        "Quantity", "Unit_Price", "Discount", "Sales", "Profit",
        "Payment_Method"
    ]
    df = pd.DataFrame(rows, columns=columns)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=False)
    print(f"Generated {len(df)} records: {output}")

if __name__ == "__main__":
    generate_data()
