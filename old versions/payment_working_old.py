import streamlit as st
from mollie.api.client import Client
import pandas as pd

CSV_FILE = "vdz_admin.csv"

mollie = Client()
mollie.set_api_key("test_GQGaRypbVSE5PGQsThJCx68mTbR5gd")  # paste your Mollie test key

def load_csv():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE, dtype=str)
        return df
    return pd.DataFrame()

def save_csv(df):
    df.to_csv(CSV_FILE, index=False)

st.title("Ticket Betaling – €10")

lid = st.query_params.get("lid", [None])[0]
if lid:
    st.write("Voor lid:", lid)
else:
    st.warning("Geen lidnummer. Kom vanuit validatie.")

naam = st.text_input("Naam")
email = st.text_input("Email")

if st.button("Betaal €10"):
    if naam and email:
        try:
            payment = mollie.payments.create({
                "amount": {"value": "10.00", "currency": "EUR"},
                "description": f"Ticket {lid}",
                "redirectUrl": "http://localhost:8503?success=true&lid=" + lid,  # to dashboard
            })
            st.markdown(f"[Ga naar Mollie]({payment.checkout_url})")
        except Exception as e:
            st.error(f"Fout: {e}")
            st.info("Voor test: Simuleer success.")
            df = load_csv()
            if lid in df["Relatiecode"].values:
                df.loc[df["Relatiecode"] == lid, "paid"] = "1"
                df.loc[df["Relatiecode"] == lid, "ticket_ordered"] = "yes"
                save_csv(df)
                st.success("Test update gedaan!")

        # Button to dashboard
        dashboard_url = "http://localhost:8503"
        st.markdown(f'<a href="{dashboard_url}" target="_blank"><button>Toon Dashboard</button></a>', unsafe_allow_html=True)