import streamlit as st
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

# -------------------------------
# Functions
# -------------------------------

def load_csv(file_path=None):
    """
    Load CSV from given path or via file uploader.
    """
    if file_path:
        df = pd.read_csv(file_path)
    else:
        uploaded_file = st.file_uploader("Upload club CSV (max 2000 rows)", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
        else:
            return None
    # Ensure Relatiecode is string
    df["Relatiecode"] = df["Relatiecode"].astype(str)
    # Add 4 extra columns if not exist
    extra_cols = ["ticket_ordered", "paid_date", "future_col1", "future_col2"]
    for col in extra_cols:
        if col not in df.columns:
            df[col] = ""
    return df

def save_csv(df, file_path="vdz_admin.csv"):
    """
    Save updated CSV to disk in project folder.
    """
    df.to_csv(file_path, index=False)
    st.success(f"CSV saved to {os.path.abspath(file_path)}")

def update_payment_status(df, member_id):
    """
    Update the 'ticket_ordered' and 'paid_date' columns when a payment is confirmed.
    """
    idx = df[df["Relatiecode"] == member_id].index
    if len(idx) > 0:
        df.at[idx[0], "ticket_ordered"] = "Yes"
        df.at[idx[0], "paid_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.success(f"Marked {member_id} as paid.")
    else:
        st.error(f"Member ID {member_id} not found.")

def display_member_table(df):
    """
    Show the full CSV table for admin.
    """
    st.subheader("Full Member Data")
    st.dataframe(df)

def plot_sales(df):
    """
    Show simple bar chart of tickets sold.
    """
    sales_count = df["ticket_ordered"].value_counts()
    fig, ax = plt.subplots()
    ax.bar(sales_count.index, sales_count.values, color=["orange", "green"])
    ax.set_ylabel("Number of Members")
    ax.set_title("Ticket Sales Overview")
    st.pyplot(fig)

def handle_query_params(df):
    """
    Check if URL has member_id & paid, and update CSV.
    Example: https://tickets-backoffice.streamlit.app/?member_id=QPNR392&paid=1
    """
    params = st.experimental_get_query_params()
    if "member_id" in params and "paid" in params:
        member_id = params["member_id"][0]
        paid_flag = params["paid"][0]
        if paid_flag == "1":
            update_payment_status(df, member_id)
            save_csv(df)

# -------------------------------
# Main App
# -------------------------------

def main():
    st.title("Ticket Sales Admin / Backoffice")

    # 1️⃣ Load CSV
    df = load_csv()
    if df is None:
        st.info("Please upload a CSV to begin.")
        return

    # 2️⃣ Handle URL callback from WooCommerce / JS
    handle_query_params(df)

    # 3️⃣ Display table and graph
    display_member_table(df)
    plot_sales(df)

    # 4️⃣ Manual Save button
    if st.button("Save CSV"):
        save_csv(df)

if __name__ == "__main__":
    main()

