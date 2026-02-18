import streamlit as st
import pandas as pd
import os
import csv

def load_data():
    if os.path.exists("vdz.csv"):
        df = pd.read_csv("vdz.csv", sep=";", dtype=str, quoting=csv.QUOTE_MINIMAL, encoding='utf-8')
        df["Relatiecode"] = df["Relatiecode"].astype(str).str.strip()
        st.info(f"Leden geladen: {len(df)}")
        return df
    st.error("vdz.csv niet gevonden")
    return pd.DataFrame()

def validate_member(df, member_id):
    return member_id.strip() in df["Relatiecode"].values

def display_user_info(df, member_id):
    row = df[df["Relatiecode"] == member_id.strip()].iloc[0]
    st.subheader("Gevonden lid")
    st.write(f"**Relatiecode:** {row['Relatiecode']}")
    st.write(f"**Naam:** {row['Volledige naam']}")
    st.write(f"**Geboortedatum:** {row['Geboortedatum']}")
    st.write(f"**E-mail:** {row['E-mail']}")

st.title("Club Ticket Validatie")

df = load_data()
user_id = st.text_input("Relatiecode")

if st.button("Valideer"):
    if validate_member(df, user_id):
        st.success("Relatiecode geldig!")
        display_user_info(df, user_id)

        # Automatic open payment in new tab with lid param
        payment_url = f"http://localhost:8502/?lid={user_id.strip()}"
        st.markdown(
            f"""
            <script>
                window.open("{payment_url}", "_blank");
            </script>
            <a href="{payment_url}" target="_blank">
                <button style="background:#cc0000;color:white;padding:12px 24px;font-size:18px;border:none;border-radius:6px;cursor:pointer;">
                    Betaal €10 – Koop Ticket
                </button>
            </a>
            """,
            unsafe_allow_html=True
        )
    else:
        st.error("Relatiecode niet gevonden – controleer aub.")