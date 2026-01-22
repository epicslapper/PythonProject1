import streamlit as st
import pandas as pd
import os
import csv

CSV_FILE = "vdz_admin.csv"

def detect_delimiter(file_path):
    """Quick check: ; or , based on first line"""
    if not os.path.exists(file_path):
        return ','
    with open(file_path, 'r', encoding='utf-8') as f:
        first_line = f.readline()
    if ';' in first_line and first_line.count(';') > first_line.count(','):
        return ';'
    return ','

def load_admin_csv():
    if not os.path.exists(CSV_FILE):
        st.error("vdz_admin.csv niet gevonden.")
        return pd.DataFrame()

    delim = detect_delimiter(CSV_FILE)
    try:
        df = pd.read_csv(CSV_FILE, sep=delim, dtype=str, quoting=csv.QUOTE_MINIMAL, encoding='utf-8')
        st.info(f"Admin bestand geladen: {len(df)} rijen (delimiter: {delim})")
    except Exception as e:
        st.error(f"Fout bij laden: {e}")
        return pd.DataFrame()

    # Verwijder junk kolommen als die er zijn gekomen (bijv. van foute append)
    junk_cols = [col for col in df.columns if 'Unnamed' in col or ';' in col or 'Relatiecode;' in col]
    if junk_cols:
        df = df.drop(columns=junk_cols)
        st.warning(f"Junk kolommen verwijderd: {junk_cols}")

    # Zorg dat we de juiste kolom hebben
    if "Relatiecode" not in df.columns:
        st.error("Kolom 'Relatiecode' niet gevonden. Beschikbare kolommen: " + ", ".join(df.columns))
        return pd.DataFrame()

    # Strip whitespace in Relatiecode (vaak oorzaak van "not found")
    df["Relatiecode"] = df["Relatiecode"].astype(str).str.strip()

    return df

def display_stats(df):
    if df.empty:
        return

    st.subheader("Ticket Verkoop Overzicht")
    # Maak kolom robuust tegen lege/ongeldige waarden
    ticket_col = df["ticket_ordered"].fillna("").astype(str).str.lower()
    sold_count = (ticket_col == "yes").sum()
    total = len(df)

    st.metric("Tickets verkocht", f"{sold_count} van {total}")

    if sold_count > 0:
        st.bar_chart(ticket_col.map(lambda x: 1 if x == "yes" else 0).value_counts())

def main():
    st.title("Ticket Admin Dashboard")
    df = load_admin_csv()

    if not df.empty:
        st.subheader("Database Preview")
        st.dataframe(df)

        # Extra debug: toon of BMVY28V aanwezig is
        if "BMVY28V" in df["Relatiecode"].values:
            st.success("BMVY28V gevonden in database!")
        else:
            st.warning("BMVY28V NIET gevonden — controleer Relatiecode kolom handmatig.")

        display_stats(df)
    else:
        st.warning("Geen data beschikbaar.")

if __name__ == "__main__":
    main()