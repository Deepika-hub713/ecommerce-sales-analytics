import pandas as pd

def load_data(path):
    """Load the e-commerce CSV and create useful date fields."""
    df = pd.read_csv(path, parse_dates=["Order_Date"])
    df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)
    df["Day"] = df["Order_Date"].dt.day_name()
    return df

def calculate_kpis(df):
    """Return the main business KPIs."""
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    orders = df["Order_ID"].nunique()
    customers = df["Customer_ID"].nunique()

    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "orders": orders,
        "customers": customers,
        "average_order_value": total_sales / orders if orders else 0,
        "units_sold": df["Quantity"].sum()
    }

def sales_by_category(df):
    return df.groupby("Category", as_index=False)["Sales"].sum().sort_values(
        "Sales", ascending=False
    )

def sales_by_region(df):
    return df.groupby("Region", as_index=False)["Sales"].sum().sort_values(
        "Sales", ascending=False
    )

def top_products(df, n=10):
    return df.groupby("Product", as_index=False).agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Units=("Quantity", "sum")
    ).nlargest(n, "Sales")

def customer_summary(df):
    return df.groupby("Customer_ID", as_index=False).agg(
        Spending=("Sales", "sum"),
        Orders=("Order_ID", "nunique"),
        Units=("Quantity", "sum"),
        Profit=("Profit", "sum")
    ).sort_values("Spending", ascending=False)
