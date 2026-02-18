import streamlit as st
from mollie.api.client import Client
import pandas as pd
import os
import json
from datetime import datetime

CSV_FILE = "vdz_admin.csv"

mollie = Client()
mollie.set_api_key("test_GQGaRypbVSE5PGQsThJCx68mTbR5gd")  # your key

st.title("Ticket Betaling – €10 (FIXED LID EXTRACTION)")

# LID EXTRACTION – NO MORE FUCKING SLICING MISTAKES
st.subheader("RAW QUERY PARAMS FROM MOLLIE")
st.json(dict(st.query_params))

lid_list = st.query_params.get("lid")
st.write("lid_list (raw from params):", lid_list)
st.write("lid_list type:", type(lid_list))

lid = ""
if lid_list:
    if isinstance(lid_list, list):
        lid = lid_list[0] if lid_list else ""
    else:
        lid = lid_list

lid = str(lid).strip()
st.write(f"FINAL LID AFTER CLEANUP: '{lid}' (length {len(lid)})")

if not lid:
    st.error("Geen lidnummer in de URL (geen ?lid=...). Kom vanuit main.py met de parameter.")
    st.stop()

st.subheader(f"Betaling voor lid: {lid}")

naam = st.text_input("Naam", value="Test Naam")
email = st.text_input("Email", value="test@example.com")

if st.button("Start Betaling"):
    st.write("Start Betaling knop ingedrukt")
    if not naam or not email:
        st.error("Naam en email verplicht")
    else:
        st.info("Aanmaken betaling bij Mollie...")
        try:
            payment = mollie.payments.create({
                "amount": {"value": "10.00", "currency": "EUR"},
                "description": f"Ticket {lid} - {naam}",
                "redirectUrl": f"http://localhost:8502/?lid={lid}",
                "metadata": {"naam": naam, "email": email, "lidnummer": lid},
            })
            st.session_state.payment_id = payment['id']
            st.success("Betaling AANGEMAAKT")
            st.write("Payment ID:", payment['id'])
            st.markdown(f"[Ga naar Mollie checkout]({payment.checkout_url})")
            st.info("Betaal in test mode. Kom terug naar deze pagina en klik 'Check Status'.")
        except Exception as e:
            st.error(f"Aanmaken betaling mislukt: {e}")

# CHECK STATUS & UPDATE
payment_id = st.session_state.get("payment_id", None)
if payment_id:
    st.markdown("---")
    st.subheader("Betaling controleren")

    if st.button("Check Status & Update Database"):
        st.write("Polling Mollie voor ID:", payment_id)
        try:
            p = mollie.payments.get(payment_id)
            st.info("VOLLEDIGE MOLLIE RESPONSE (RAW):")
            st.json(p)

            status = p.get('status', 'unknown')
            st.write("Status:", status)
            st.write("Amount:", p.get('amount', 'n/a'))
            st.write("Paid at:", p.get('paidAt', 'nog niet'))

            if status == 'paid':
                st.balloons()
                st.success("BETALING BETAALD!")
                df = pd.read_csv(CSV_FILE, dtype=str) if os.path.exists(CSV_FILE) else pd.DataFrame()
                st.write("CSV voor update:", df.to_dict('records'))
                if lid in df["Relatiecode"].values:
                    mask = df["Relatiecode"] == lid
                    df.loc[mask, "paid"] = "1"
                    df.loc[mask, "ticket_ordered"] = "yes"
                    df.loc[mask, "extra1"] = f"Paid {p.get('paidAt', datetime.now())}"
                    df.to_csv(CSV_FILE, index=False)
                    st.success("DATABASE BIJGEWERKT!")
                    st.write("CSV na update:", df.to_dict('records'))
                else:
                    st.error(f"Lid '{lid}' NIET gevonden in CSV.")
            else:
                st.warning(f"Status: {status} – nog niet betaald.")
        except Exception as e:
            st.error(f"Poll fout: {e}")

# Manual dashboard link
st.markdown("---")
st.markdown(
    '<a href="http://localhost:8503" target="_blank">'
    '<button style="background:#006600;color:white;padding:12px 24px;font-size:18px;border:none;border-radius:6px;">'
    'Toon Dashboard'
    '</button></a>',
    unsafe_allow_html=True
)