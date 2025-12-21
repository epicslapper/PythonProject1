# tickets_sales.py
"""
Tickets Sales App
Validates member ID and directs to WooCommerce checkout.
"""

import streamlit as st
import pandas as pd
from tickets-database import load_membership_database

def validate_member_id(df, member_id):
    if member_id in df["Relatiecode"].values:
        st.success("Member validated successfully!")
        return True
    else:
        st.error("Invalid member ID.")
        return False

def show_member_info(df, member_id):
    member_row = df[df["Relatiecode"] == member_id]
    st.write(member_row)

def redirect_to_checkout(member_id):
    # WooCommerce ticket product ID 13
    checkout_url = f"https://YOUR_WP_SITE/checkout/?add-to-cart=13&member_id={member_id}"
    st.markdown(f"[Click to Pay]({checkout_url})", unsafe_allow_html=True)

def main():
    st.title("Ticket Sales")
    df = load_membership_database()
    if df.empty:
        return

    member_id = st.text_input("Enter your member ID:")
    if member_id:
        if validate_member_id(df, member_id):
            show_member_info(df, member_id)
            redirect_to_checkout(member_id)

if __name__ == "__main__":
    main()
