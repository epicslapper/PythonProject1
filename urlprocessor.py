import streamlit as st
import pandas as pd
import os

CSV_FILE = "vdz_admin.csv"
URL_LOG = "url_log.txt"


# -------------------------------
# CSV Functions
# -------------------------------
def load_csv():
    if not os.path.exists(CSV_FILE):
        st.error(f"{CSV_FILE} niet gevonden. Start met een lege database?")
        return pd.DataFrame(
            columns=["Relatiecode", "Volledige naam", "Geboortedatum", "E-mail", "paid", "ticket_ordered", "extra1",
                     "extra2"])

    try:
        df = pd.read_csv(CSV_FILE, dtype=str, encoding='utf-8')
        # Clean Relatiecode: strip spaces, make sure it's string
        if "Relatiecode" in df.columns:
            df["Relatiecode"] = df["Relatiecode"].astype(str).str.strip()
        else:
            st.error("Kolom 'Relatiecode' ontbreekt in CSV!")
            return pd.DataFrame()

        st.success(f"CSV geladen: {len(df)} rijen")
        return df
    except Exception as e:
        st.error(f"Fout bij laden CSV: {e}")
        return pd.DataFrame()


def save_csv(df):
    df.to_csv(CSV_FILE, index=False, encoding='utf-8')
    st.info(f"Database opgeslagen: {CSV_FILE}")


# -------------------------------
# URL Processing
# -------------------------------
def process_url(df):
    params = st.query_params
    st.write("DEBUG: URL query params:", params)

    # Extract safely (handles list or single value)
    member_param = params.get("member_id", [""])[0]
    paid_param = params.get("paid", ["0"])[0]

    member_id = str(member_param).strip()
    paid = str(paid_param).strip()

    st.write(f"DEBUG: Extracted member_id='{member_id}' (length {len(member_id)}), paid='{paid}'")

    if not member_id:
        st.info("Geen member_id in URL parameters — waarschijnlijk directe toegang.")
        return df

    # Log callback
    with open(URL_LOG, "a", encoding='utf-8') as f:
        f.write(f"{pd.Timestamp.now()} | member_id={member_id} | paid={paid}\n")

    # Check if member exists
    if member_id in df["Relatiecode"].values:
        mask = df["Relatiecode"] == member_id
        df.loc[mask, "paid"] = paid
        df.loc[mask, "ticket_ordered"] = "yes"
        # Optional: extra info
        df.loc[mask, "extra1"] = f"Paid via Mollie - {pd.Timestamp.now()}"

        st.balloons()
        st.success(f"Bedankt! Ticket voor {member_id} succesvol bijgewerkt als betaald.")
    else:
        st.error(f"Member ID '{member_id}' NIET gevonden in database.")
        st.write("Debug: Eerste 10 Relatiecodes in CSV:")
        st.write(df["Relatiecode"].head(10).tolist())
        st.write("Controleer of de code exact matcht (geen spaties, hoofdletters).")

    return df


# -------------------------------
# Main App
# -------------------------------
def main():
    st.title("URL Processor / Ticket Backoffice")

    df = load_csv()
    if not df.empty:
        # Process URL params (only once per load)
        df = process_url(df)

        st.subheader("Database Preview na update")
        st.dataframe(df)

        # Save after processing
        save_csv(df)

        # Optional: auto refresh after 10s if you want
        # st.rerun()  # uncomment if you want auto-update loop (careful with loops!)


if __name__ == "__main__":
    main()