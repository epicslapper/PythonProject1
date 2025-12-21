import streamlit as st
import pandas as pd
import os

CSV_FILE = "vdz_admin.csv"

def load_csv():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE, dtype=str)
    else:
        st.error("Database CSV not found.")
        return pd.DataFrame()

def display_stats(df):
    st.subheader("Ticket Sales Summary")
    sold_count = df["ticket_ordered"].value_counts().get("yes", 0)
    st.write(f"Total tickets sold: {sold_count}")
    st.bar_chart(df["ticket_ordered"].map(lambda x: 1 if x=="yes" else 0))

def main():
    st.title("Ticket Admin Dashboard")
    df = load_csv()
    if not df.empty:
        st.subheader("Database Preview")
        st.dataframe(df)
        display_stats(df)

if __name__ == "__main__":
    main()
