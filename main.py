import streamlit as st
import pandas as pd
import subprocess
import os

st.title("Football Ticket Checker 🎟️")

# -----------------------------
# Sidebar: Create Database
# -----------------------------
if st.sidebar.button("Create / Reset Database"):
    subprocess.run(["python", "create_db.py"])
    st.sidebar.success("Database created!")

# -----------------------------
# Load database
# -----------------------------
db_file_csv = "football_ids.csv"

if not os.path.exists(db_file_csv):
    st.warning("Database not found. Please click 'Create / Reset Database' in the sidebar.")
else:
    df = pd.read_csv(db_file_csv)

    st.subheader("Current database")
    st.dataframe(df)

    # -----------------------------
    # Input field
    # -----------------------------
    football_id = st.text_input("Enter your Football ID")

    if st.button("Check Ticket"):
        if football_id.strip() == "":
            st.warning("Please enter your Football ID.")
        elif football_id.isdigit() and int(football_id) in df['FootballID'].values:
            st.success("✅ Football ID is valid!")

            ticket_code = f"TICKET-{football_id}-2025"
            st.write(f"Your ticket string: **{ticket_code}**")

            wp_checkout_url = "https://www.google.nl"
            st.markdown(f"[Go to Google]({wp_checkout_url})")
        else:
            st.error("❌ Invalid Football ID. Please check and try again.")
