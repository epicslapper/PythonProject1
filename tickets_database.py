# tickets_database.py
"""
Tickets Database Manager
Manages loading, saving, and updating membership CSV.
Single source of truth for all ticket operations.
"""

import pandas as pd
import os
import streamlit as st

CSV_FILE = "vdz_admin.csv"

def load_membership_database():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE, dtype=str)
        st.success(f"Loaded database with {len(df)} members.")
        return df
    else:
        st.error("Database CSV not found.")
        return pd.DataFrame()

def save_membership_database(df):
    df.to_csv(CSV_FILE, index=False)
    st.success("Database saved.")

def update_member_ticket_status(df, member_id, paid_value="1"):
    if member_id in df["Relatiecode"].values:
        df.loc[df["Relatiecode"] == member_id, "paid"] = paid_value
        df.loc[df["Relatiecode"] == member_id, "ticket_ordered"] = "yes"
        st.success(f"Member {member_id} updated!")
    else:
        st.warning(f"Member {member_id} not found in database.")
    return df

def main():
    st.title("Tickets Database Manager")
    df = load_membership_database()
    if df.empty:
        return

    st.subheader("Database Preview")
    st.dataframe(df)

if __name__ == "__main__":
    main()
