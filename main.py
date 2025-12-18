import streamlit as st
import pandas as pd
import os
import webbrowser

# -----------------------------
# Load database
# -----------------------------
db_file_csv = "football_ids.csv"

st.title("Football Ticket Checker 🎟️")

if not os.path.exists(db_file_csv):
    st.warning("Database not found. Please create it first.")
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

            # -----------------------------
            # Create HTML file
            # -----------------------------
            html_file = "ticket_info.html"
            html_content = f"""
            <html>
              <body>
                <h1>Ticket Info</h1>
                <p>Football ID: {football_id}</p>
                <p>Ticket String: {ticket_code}</p>
                <p><a href="#">Simulated checkout link</a></p>
              </body>
            </html>
            """

            with open(html_file, "w") as f:
                f.write(html_content)

            st.info(f"HTML file created: `{html_file}`")

            # -----------------------------
            # Link to open HTML file
            # -----------------------------
            if st.button("Open Ticket HTML"):
                path = os.path.abspath(html_file)
                webbrowser.open(f"file://{path}")

        else:
            st.error("❌ Invalid Football ID. Please check and try again.")

import streamlit as st
import pandas as pd

# Load CSV
csv_file = "vdz.csv"  # make sure it's in the same directory as your app
df = pd.read_csv(csv_file)

# Display CSV at the bottom
st.subheader("Full CSV Data Check")
st.dataframe(df)  # nice scrollable table in Streamlit
