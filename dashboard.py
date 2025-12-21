# dashboard.py
"""
Ticket Sales Dashboard
Admin dashboard to view ticket sales, totals, and graphs.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from tickets_database import load_database_1_load_csv

def summarize_ticket_sales_1_total(df):
    """Return total tickets sold and percentage."""
    total_members = len(df)
    tickets_sold = df["ticket_ordered"].value_counts().get("yes", 0)
    return tickets_sold, total_members

def plot_ticket_sales_2_graph(df):
    """Generate a simple bar chart of sold vs not sold tickets."""
    sold = df["ticket_ordered"].value_counts().get("yes", 0)
    not_sold = df["ticket_ordered"].value_counts().get("no", len(df) - sold)
    fig, ax = plt.subplots()
    ax.bar(["Sold", "Not Sold"], [sold, not_sold], color=["green", "red"])
    ax.set_ylabel("Number of Tickets")
    ax.set_title("Ticket Sales Overview")
    st.pyplot(fig)

def main():
    st.title("Ticket Sales Admin Dashboard")
    df = load_database_1_load_csv()
    tickets_sold, total_members = summarize_ticket_sales_1_total(df)
    st.write(f"Tickets sold: {tickets_sold} / {total_members}")
    st.subheader("Detailed Ticket Database")
    st.dataframe(df)
    plot_ticket_sales_2_graph(df)

if __name__ == "__main__":
    main()
