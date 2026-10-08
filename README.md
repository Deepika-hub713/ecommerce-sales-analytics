# E-Commerce Sales Analytics and Customer Behavior Dashboard

## Project Overview
This is a complete Data Analytics project built using Python, Pandas, Plotly, and Streamlit.

The dashboard analyzes:
- Sales performance
- Profitability
- Orders and units sold
- Customer behavior
- Customer segmentation
- Product performance
- Regional performance
- Payment methods
- Business recommendations

## Project Structure

```text
ecommerce_sales_analytics/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── ecommerce_sales.csv
└── src/
    ├── __init__.py
    ├── analysis.py
    └── data_generator.py
```

## Requirements
- Python 3.10 or newer
- VS Code or another Python IDE

## Installation

Open a terminal inside the project folder:

```bash
python -m venv venv
```

### Windows
```bash
venv\Scripts\activate
```

### macOS/Linux
```bash
source venv/bin/activate
```

Install packages:

```bash
pip install -r requirements.txt
```

## Run the Dashboard

```bash
streamlit run app.py
```

Open the URL displayed by Streamlit, usually:

```text
http://localhost:8501
```

## Generate a New Dataset

If you want to create a fresh dataset:

```bash
python src/data_generator.py
```

Then run:

```bash
streamlit run app.py
```

## Technologies Used

- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- CSV

## Main Dashboard Sections

1. Overview
2. Sales Analysis
3. Customer Behavior
4. Product Analysis
5. Business Insights

## Academic Project Flow

Data Collection → Data Cleaning → Exploratory Data Analysis → KPI Calculation → Visualization → Customer Analysis → Business Insights → Streamlit Dashboard

## Example Viva Questions

### Why did you use Streamlit?
Streamlit makes it easy to convert Python data-analysis code into an interactive web dashboard without requiring frontend development.

### Why Pandas?
Pandas provides efficient tools for data cleaning, grouping, aggregation, and analysis.

### What is AOV?
AOV means Average Order Value.

AOV = Total Sales / Number of Orders

### What business insights can be obtained?
The dashboard identifies top products, profitable categories, high-value customers, strong regions, payment preferences, and sales trends.
