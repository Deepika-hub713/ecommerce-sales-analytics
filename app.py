import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "ecommerce_sales.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE, parse_dates=["Order_Date"])
    df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)
    df["Month_Name"] = df["Order_Date"].dt.strftime("%b")
    df["Day"] = df["Order_Date"].dt.day_name()
    df["Year"] = df["Order_Date"].dt.year
    return df

df = load_data()

# ---------------- Sidebar filters ----------------
st.sidebar.title("🛒 E-Commerce Analytics")
st.sidebar.caption("Sales & Customer Behavior Dashboard")

min_date = df["Order_Date"].min().date()
max_date = df["Order_Date"].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered = df[
        (df["Order_Date"].dt.date >= start_date) &
        (df["Order_Date"].dt.date <= end_date)
    ].copy()
else:
    filtered = df.copy()

def multiselect_filter(label, column):
    options = sorted(df[column].dropna().unique().tolist())
    selected = st.sidebar.multiselect(label, options, default=options)
    return selected

categories = multiselect_filter("Category", "Category")
regions = multiselect_filter("Region", "Region")
segments = multiselect_filter("Customer Segment", "Customer_Segment")

filtered = filtered[
    filtered["Category"].isin(categories) &
    filtered["Region"].isin(regions) &
    filtered["Customer_Segment"].isin(segments)
].copy()

st.sidebar.divider()
st.sidebar.info(
    "Use the filters to explore sales, customers, products, and business insights."
)

# ---------------- Header ----------------
st.title("🛒 E-Commerce Sales Analytics & Customer Behavior Dashboard")
st.markdown(
    "Interactive analytics dashboard for understanding **sales performance, "
    "customer behavior, product performance, and business trends**."
)

if filtered.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

# ---------------- KPIs ----------------
total_sales = filtered["Sales"].sum()
total_profit = filtered["Profit"].sum()
total_orders = filtered["Order_ID"].nunique()
total_customers = filtered["Customer_ID"].nunique()
avg_order_value = total_sales / total_orders if total_orders else 0
total_units = filtered["Quantity"].sum()

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Total Sales", f"₹{total_sales:,.0f}")
c2.metric("Total Profit", f"₹{total_profit:,.0f}")
c3.metric("Orders", f"{total_orders:,}")
c4.metric("Customers", f"{total_customers:,}")
c5.metric("Avg. Order Value", f"₹{avg_order_value:,.0f}")
c6.metric("Units Sold", f"{total_units:,}")

st.divider()

# ---------------- Navigation ----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Overview",
    "📈 Sales Analysis",
    "👥 Customer Behavior",
    "📦 Product Analysis",
    "💡 Business Insights"
])

with tab1:
    st.subheader("Sales Overview")

    col1, col2 = st.columns(2)

    monthly = filtered.groupby("Month", as_index=False).agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    ).sort_values("Month")

    with col1:
        fig = px.line(
            monthly, x="Month", y="Sales",
            markers=True, title="Monthly Sales Trend"
        )
        fig.update_layout(xaxis_title="Month", yaxis_title="Sales (₹)")
        st.plotly_chart(fig, width="stretch")

    with col2:
        cat = filtered.groupby("Category", as_index=False)["Sales"].sum().sort_values(
            "Sales", ascending=False
        )
        fig = px.bar(
            cat, x="Category", y="Sales",
            title="Sales by Category", text_auto=".2s"
        )
        st.plotly_chart(fig, width="stretch")

    col1, col2 = st.columns(2)

    with col1:
        region_sales = filtered.groupby("Region", as_index=False)["Sales"].sum()
        fig = px.pie(
            region_sales, names="Region", values="Sales",
            title="Sales Distribution by Region", hole=0.4
        )
        st.plotly_chart(fig, width="stretch")

    with col2:
        payment = filtered.groupby("Payment_Method", as_index=False)["Sales"].sum()
        fig = px.bar(
            payment, x="Payment_Method", y="Sales",
            title="Sales by Payment Method"
        )
        st.plotly_chart(fig, width="stretch")

with tab2:
    st.subheader("📈 Sales Analysis")

    col1, col2 = st.columns(2)

    with col1:
        daily = filtered.groupby("Day", as_index=False)["Sales"].sum()
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday",
                     "Friday", "Saturday", "Sunday"]
        daily["Day"] = pd.Categorical(daily["Day"], categories=day_order, ordered=True)
        daily = daily.sort_values("Day")
        fig = px.bar(daily, x="Day", y="Sales", title="Sales by Day of Week")
        st.plotly_chart(fig, width="stretch")

    with col2:
        region_profit = filtered.groupby("Region", as_index=False)["Profit"].sum()
        fig = px.bar(
            region_profit, x="Region", y="Profit",
            title="Profit by Region", text_auto=".2s"
        )
        st.plotly_chart(fig, width="stretch")

    st.subheader("Monthly Sales & Profit")
    monthly_table = filtered.groupby("Month", as_index=False).agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order_ID", "nunique"),
        Units=("Quantity", "sum")
    )
    st.dataframe(
        monthly_table.style.format({
            "Sales": "₹{:,.2f}",
            "Profit": "₹{:,.2f}",
            "Orders": "{:,.0f}",
            "Units": "{:,.0f}"
        }),
        width="stretch"
    )

with tab3:
    st.subheader("👥 Customer Behavior")

    customer = filtered.groupby("Customer_ID", as_index=False).agg(
        Total_Spending=("Sales", "sum"),
        Orders=("Order_ID", "nunique"),
        Units=("Quantity", "sum"),
        Profit=("Profit", "sum")
    )
    customer["Avg_Order_Value"] = customer["Total_Spending"] / customer["Orders"]

    col1, col2 = st.columns(2)

    with col1:
        top_customers = customer.nlargest(10, "Total_Spending")
        fig = px.bar(
            top_customers.sort_values("Total_Spending"),
            x="Total_Spending", y="Customer_ID",
            orientation="h",
            title="Top 10 Customers by Spending"
        )
        st.plotly_chart(fig, width="stretch")

    with col2:
        segment_data = filtered.groupby("Customer_Segment", as_index=False).agg(
            Sales=("Sales", "sum"),
            Customers=("Customer_ID", "nunique")
        )
        fig = px.pie(
            segment_data, names="Customer_Segment", values="Customers",
            title="Customer Segment Distribution", hole=0.4
        )
        st.plotly_chart(fig, width="stretch")

    st.subheader("Customer Spending vs Orders")
    fig = px.scatter(
        customer,
        x="Orders",
        y="Total_Spending",
        size="Units",
        hover_name="Customer_ID",
        title="Customer Spending vs Number of Orders"
    )
    st.plotly_chart(fig, width="stretch")

    st.subheader("Top Customers")
    st.dataframe(
        customer.nlargest(20, "Total_Spending").style.format({
            "Total_Spending": "₹{:,.2f}",
            "Orders": "{:,.0f}",
            "Units": "{:,.0f}",
            "Profit": "₹{:,.2f}",
            "Avg_Order_Value": "₹{:,.2f}"
        }),
        width="stretch"
    )

with tab4:
    st.subheader("📦 Product Analysis")

    product = filtered.groupby(
        ["Product", "Category"], as_index=False
    ).agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Units=("Quantity", "sum"),
        Orders=("Order_ID", "nunique")
    )

    col1, col2 = st.columns(2)

    with col1:
        top_products = product.nlargest(10, "Sales")
        fig = px.bar(
            top_products.sort_values("Sales"),
            x="Sales", y="Product",
            color="Category",
            orientation="h",
            title="Top 10 Products by Sales"
        )
        st.plotly_chart(fig, width="stretch")

    with col2:
        top_profit = product.nlargest(10, "Profit")
        fig = px.bar(
            top_profit.sort_values("Profit"),
            x="Profit", y="Product",
            color="Category",
            orientation="h",
            title="Top 10 Products by Profit"
        )
        st.plotly_chart(fig, width="stretch")

    st.subheader("Product Performance")
    st.dataframe(
        product.sort_values("Sales", ascending=False).style.format({
            "Sales": "₹{:,.2f}",
            "Profit": "₹{:,.2f}",
            "Units": "{:,.0f}",
            "Orders": "{:,.0f}"
        }),
        width="stretch"
    )

with tab5:
    st.subheader("💡 Business Insights")

    best_category = (
        filtered.groupby("Category")["Sales"].sum().idxmax()
    )
    best_region = (
        filtered.groupby("Region")["Sales"].sum().idxmax()
    )
    best_product = (
        filtered.groupby("Product")["Sales"].sum().idxmax()
    )
    best_customer = (
        filtered.groupby("Customer_ID")["Sales"].sum().idxmax()
    )
    best_payment = (
        filtered.groupby("Payment_Method")["Sales"].sum().idxmax()
    )

    profit_margin = (total_profit / total_sales * 100) if total_sales else 0

    st.success(f"🏆 **Best Category:** {best_category}")
    st.info(f"🌍 **Best Region:** {best_region}")
    st.info(f"📦 **Best-Selling Product:** {best_product}")
    st.info(f"👤 **Highest-Spending Customer:** {best_customer}")
    st.info(f"💳 **Most Used/Highest Sales Payment Method:** {best_payment}")
    st.warning(f"💰 **Overall Profit Margin:** {profit_margin:.2f}%")

    st.subheader("Recommendations")
    recommendations = [
        f"Focus marketing campaigns on the **{best_category}** category.",
        f"Increase regional promotions in **{best_region}**, the highest-sales region.",
        f"Promote **{best_product}** using bundles and cross-selling offers.",
        "Create loyalty rewards for high-value and repeat customers.",
        "Use customer segmentation to personalize offers and campaigns.",
        "Monitor low-margin products and optimize discounts carefully."
    ]

    for recommendation in recommendations:
        st.markdown(f"- {recommendation}")

    st.subheader("Filtered Data")
    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Filtered CSV",
        data=csv,
        file_name="filtered_ecommerce_sales.csv",
        mime="text/csv"
    )

st.divider()
st.caption("E-Commerce Sales Analytics Dashboard | Built with Python + Streamlit + Pandas + Plotly")
