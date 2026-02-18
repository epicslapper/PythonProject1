import streamlit as st
import pandas as pd
import os

CSV_FILE = "vdz_admin.csv"

def load_csv():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE, dtype=str)
        df["Relatiecode"] = df["Relatiecode"].astype(str).str.strip()
        return df
    st.error("vdz_admin.csv niet gevonden.")
    return pd.DataFrame()

st.title("Ticket Admin Dashboard")

# Show success message if coming from payment
lid = st.query_params.get("lid", [None])[0]
if lid:
    st.success(f"Terug van betaling voor lid {lid} — controleer hieronder of het betaald is.")

df = load_csv()
if not df.empty:
    st.subheader("Database Preview")
    st.dataframe(df)

    sold_count = len(df[df["ticket_ordered"].str.lower() == "yes"])
    st.metric("Tickets verkocht", sold_count)
else:
    st.warning("Geen data beschikbaar.")