import streamlit as st
import pandas as pd
import os

CSV_FILE = "vdz_admin.csv"

st.title("Ticket Betaling – Demo")

# Get lid from URL (passed from main.py)
lid = st.query_params.get("lid", [None])[0]
if lid:
    st.write("Voor lid:", lid)
else:
    st.warning("Geen lidnummer meegegeven. Kom terug vanuit validatie pagina.")

naam = st.text_input("Naam")
email = st.text_input("Email")

Mollie test key :
test_GQGaRypbVSE5PGQsThJCx68mTbR5gd



if st.button("Start Test Betaling"):
    if naam and email:
        st.balloons()
        st.success(f"Test betaling gesimuleerd voor {naam}!")

        # Fake update CSV for demo
        if os.path.exists(CSV_FILE):
            df = pd.read_csv(CSV_FILE, dtype=str)
            if lid in df["Relatiecode"].values:
                df.loc[df["Relatiecode"] == lid, "paid"] = "1"
                df.loc[df["Relatiecode"] == lid, "ticket_ordered"] = "yes"
                df.to_csv(CSV_FILE, index=False)
                st.success("Database bijgewerkt (demo update)!")

        st.markdown(
            '<a href="http://localhost:8503" target="_blank">'
            '<button style="background:#006600;color:white;padding:12px 24px;font-size:18px;border:none;border-radius:6px;">'
            'Toon bijgewerkte database (dashboard)'
            '</button></a>',
            unsafe_allow_html=True
        )
    else:
        st.error("Vul naam en email in")