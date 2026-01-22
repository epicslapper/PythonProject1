import streamlit as st
import pandas as pd
import os
import csv

CSV_FILE = "vdz_admin.csv"
URL_LOG = "url_log.txt"


# -------------------------------
# CSV Functions
# -------------------------------
def load_csv():
    if not os.path.exists(CSV_FILE):
        st.error(f"{CSV_FILE} niet gevonden.")
        return pd.DataFrame(columns=[
            "Relatiecode", "Volledige naam", "Geboortedatum", "E-mail",
            "paid", "ticket_ordered", "extra1", "extra2"
        ])

    try:
        # Read with default comma (since we save with comma)
        df = pd.read_csv(CSV_FILE, dtype=str, quoting=csv.QUOTE_MINIMAL, encoding='utf-8')

        # Clean Relatiecode column
        if "Relatiecode" in df.columns:
            df["Relatiecode"] = df["Relatiecode"].astype(str).str.strip()
        else:
            st.error("Kolom 'Relatiecode' ontbreekt!")
            return pd.DataFrame()

        # Remove any junk columns
        junk_cols = [col for col in df.columns if 'Unnamed' in col or ';' in col]
        if junk_cols:
            df = df.drop(columns=junk_cols)
            st.warning(f"Junk kolommen verwijderd: {junk_cols}")

        st.success(f"CSV geladen: {len(df)} rijen")
        return df
    except Exception as e:
        st.error(f"Fout bij laden: {e}")
        return pd.DataFrame()


def save_csv(df):
    df.to_csv(CSV_FILE, index=False, quoting=csv.QUOTE_MINIMAL, encoding='utf-8')
    st.info(f"Database opgeslagen: {CSV_FILE}")


# -------------------------------
# URL Processing
# -------------------------------
def process_url(df):
    params = st.query_params
    st.write("DEBUG: URL query params:", params)

    # Your original safe extraction (best version)
    member_param = params.get("member_id", [""])
    paid_param = params.get("paid", ["0"])

    member_id = member_param[0] if isinstance(member_param, list) else member_param
    paid = paid_param[0] if isinstance(paid_param, list) else paid_param

    member_id = str(member_id).strip()
    paid = str(paid).strip()

    st.write(f"DEBUG: Extracted member_id='{member_id}' (length {len(member_id)}), paid='{paid}'")

    if not member_id:
        st.info("Geen member_id in URL parameters.")
        return df

    # Log callback with timestamp
    with open(URL_LOG, "a", encoding='utf-8') as f:
        f.write(f"{pd.Timestamp.now()} | member_id={member_id} | paid={paid}\n")

    # Update if found
    if member_id in df["Relatiecode"].values:
        mask = df["Relatiecode"] == member_id
        df.loc[mask, "paid"] = paid
        df.loc[mask, "ticket_ordered"] = "yes"
        df.loc[mask, "extra1"] = f"Updated via callback - {pd.Timestamp.now()}"

        st.balloons()
        st.success(f"Bedankt! Ticket voor {member_id} succesvol bijgewerkt als betaald.")
    else:
        st.error(f"Member ID '{member_id}' NIET gevonden in database.")
        st.write("Debug: Eerste 10 Relatiecodes in CSV:")
        st.write(df["Relatiecode"].head(10).tolist())
        st.write("Controleer op spaties, hoofdletters of kolomnaam.")

    return df


# -------------------------------
# Main App
# -------------------------------
def main():
    st.title("URL Processor / Ticket Backoffice")

    df = load_csv()
    if not df.empty:
        # Process URL params
        df = process_url(df)

        st.subheader("Database Preview na update")
        st.dataframe(df)

        # Save after processing
        save_csv(df)


if __name__ == "__main__":
    main()