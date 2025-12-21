# tickets-dashboard.py
"""
Tickets Dashboard
Displays ticket sales summary and statistics.
Graphs ticket sales by member, status, etc.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from tickets-database import load_membership_database

def summarize_ticket_sales(df):
    total_members = len(df)
    tickets_sold = df["ticket_ordered"].value_counts().get("yes", 0)
    return total_members, tickets_sold

def plot_ticket_sales(df):
    summary = df["ticket_ordered"].value_counts()
    plt.figure(figsize=(5,4))
    summary.plot(kind="bar", color=["green","red"])
    plt.title("Tickets Sold vs Not Sold")
    plt.ylabel("Number of Members")
    st.pyplot(plt)

def main():
    st.title("Tickets Dashboard")
    df = load_membership_database()
    if df.empty:
        return

    total_members, tickets_sold = summarize_ticket_sales(df)
    st.subheader(f"Total Members: {total_members}")
    st.subheader(f"Tickets Sold: {tickets_sold}")
    st.subheader("Sales Distribution")
    plot_ticket_sales(df)
    st.subheader("Database Preview")
    st.dataframe(df)

if __name__ == "__main__":
    main()
