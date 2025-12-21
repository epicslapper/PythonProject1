# tickets_callback.py
"""
Ticket URL Callback Processor
Receives member_id and payment confirmation from WordPress.
Updates CSV database accordingly.
"""

import streamlit as st
from tickets-database import load_membership_database, save_membership_database, update_member_ticket_status

def process_callback_from_url(df):
    params = st.query_params
    st.write("Callback Processor Active")

    member_id = params.get("member_id", [""])[0].strip() if "member_id" in params else ""
    paid = params.get("paid", ["0"])[0].strip() if "paid" in params else "0"

    if member_id and paid == "1":
        df = update_member_ticket_status(df, member_id, paid)
    else:
        st.info("No valid member_id or payment detected in URL.")
    return df

def main():
    st.title("Tickets Callback Processor")
    df = load_membership_database()
    if df.empty:
        return
    df = process_callback_from_url(df)
    st.subheader("Database Preview")
    st.dataframe(df)
    save_membership_database(df)

if __name__ == "__main__":
    main()
