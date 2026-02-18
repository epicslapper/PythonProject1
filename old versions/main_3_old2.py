import streamlit as st
import pandas as pd
import csv
import io
import os

def detect_delimiter(file_path_or_content):
    if isinstance(file_path_or_content, str) and os.path.exists(file_path_or_content):
        with open(file_path_or_content, 'r', encoding='utf-8') as f:
            first_line = f.readline()
    else:
        first_line = file_path_or_content.splitlines()[0] if '\n' in file_path_or_content else file_path_or_content
    return ';' if ';' in first_line and first_line.count(';') > first_line.count(',') else ','

@st.cache_data
def load_members():
    if os.path.exists("vdz.csv"):
        delim = detect_delimiter("vdz.csv")
        df = pd.read_csv("vdz.csv", sep=delim, dtype=str, quoting=csv.QUOTE_MINIMAL, encoding='utf-8')
        df["Relatiecode"] = df["Relatiecode"].astype(str).str.strip()
        st.info(f"Ledenbestand geladen: {len(df)} leden (delimiter: {delim})")
        return df
    else:
        st.error("vdz.csv niet gevonden.")
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

# ────────────────────────────────────────────────
# TEMP TEST BUTTON for local/demo today (comment out after test)
# ────────────────────────────────────────────────

if st.button("TEST: Ga direct naar ticket betaling (lokaal demo)"):

    # Option A: Switch to payment page (if multi-page setup)
    # Uncomment if you have pages/01_Ticket_Betaling.py
    # st.switch_page("pages/01_Ticket_Betaling.py")

    # Option B: Show simple payment form right here (single-file version, easiest for today)
    st.markdown("---")
    st.subheader("Ticket Betaling Demo – €10 (test mode)")

    with st.form("test_ticket_form"):
        test_naam = st.text_input("Naam", value="Test Lid")
        test_email = st.text_input("Email", value="test@club.nl")
        test_lidnummer = st.text_input("Relatiecode (voor check)", value=user_id)
        test_submit = st.form_submit_button("Test Betaling Starten")

    if test_submit:
        if test_lidnummer == user_id:
            st.success(f"Test betaling gestart voor {test_naam} ({test_lidnummer})")
            st.info("In echte versie: hier komt Mollie redirect. Voor nu alleen simulatie.")
            # Fake success update (for demo only)
            st.balloons()
            st.markdown("**Demo resultaat:** Ticket zou nu betaald zijn in database!")
        else:
            st.error("Relatiecode komt niet overeen met gevalideerd lid.")

# End of temp test button block
# Comment out or delete this whole block after today's club test








def show_pay_button(member_id):
    # Voor nu nog je oude WordPress link – later vervangen door directe Mollie
    checkout_url = (
        f"https://ticketsales.infinityfree.me/checkout/"
        f"?add-to-cart=13&member_id={member_id}"
    )
    st.markdown(
        f"""
        <a href="{checkout_url}" target="_blank">
            <button style="background:#cc0000;color:white;padding:12px 24px;font-size:18px;border:none;border-radius:6px;cursor:pointer;">
                Betaal €10 – Koop Ticket
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

def main():
    st.title("Club Ticket Validatie")

    df = load_members()
    if df.empty:
        return

    user_id = st.text_input("Voer je Relatiecode in", help="Zoals in Sportlink export (bijv. TFFL49I)")

    if st.button("Valideer"):
        if validate_member(df, user_id):
            st.success("Relatiecode geldig!")
            display_user_info(df, user_id)
            show_pay_button(user_id)
        else:
            st.error("Relatiecode niet gevonden — controleer aub.")

if __name__ == "__main__":
    main()