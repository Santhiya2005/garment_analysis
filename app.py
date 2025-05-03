from flask import Flask, render_template_string
import pandas as pd
import plotly.express as px
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Load your dataset
    df = pd.read_csv("order_report (6).csv")

    # Clean and preprocess
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    df["Total Amount"] = df["Total Amount"].replace('[₹,]', '', regex=True).astype(float)

    # Group by product
    product_summary = df.groupby("Product").size().reset_index(name="Count")
    product_summary = product_summary.sort_values("Count", ascending=False)

    # Create pie chart using Plotly
    fig = px.pie(product_summary, names="Product", values="Count", title="Product Distribution")
    pie_chart_html = fig.to_html(full_html=False)

    # Show table and pie chart
    return render_template_string('''
        <html>
            <head><title>Product Analysis</title></head>
            <body>
                <h2>Product Analysis Table</h2>
                {{ table|safe }}
                <h2>Product Distribution (Pie Chart)</h2>
                {{ pie_chart|safe }}
            </body>
        </html>
    ''', table=product_summary.to_html(index=False), pie_chart=pie_chart_html)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
