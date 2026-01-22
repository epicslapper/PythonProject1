import pandas as pd
import os
import streamlit as st
import csv
import io

CSV_FILE = "vdz_admin.csv"  # your managed admin database
INPUT_EXAMPLE = "vdz.csv"  # Sportlink export example (for fallback)


def detect_delimiter(file_path_or_content):
    """Detect ; or , by looking at first line"""
    if isinstance(file_path_or_content, str) and os.path.exists(file_path_or_content):
        with open(file_path_or_content, 'r', encoding='utf-8') as f:
            first_line = f.readline()
    else:
        # if it's already content (from uploaded file)
        first_line = file_path_or_content.splitlines()[0] if '\n' in file_path_or_content else file_path_or_content

    if ';' in first_line and first_line.count(';') > first_line.count(','):
        return ';'
    return ','


def load_admin_csv():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=[
            "Relatiecode", "Volledige naam", "Geboortedatum", "E-mail",
            "paid", "ticket_ordered", "extra1", "extra2"
        ])
        st.info("Geen vdz_admin.csv gevonden → nieuwe lege database gestart.")
    else:
        delim = detect_delimiter(CSV_FILE)
        df = pd.read_csv(CSV_FILE, sep=delim, dtype=str, quoting=csv.QUOTE_MINIMAL, encoding='utf-8')
        st.success(f"Admin database geladen: {len(df)} rijen (delimiter: {delim})")

    # Zorg dat verplichte kolommen bestaan
    required = ["paid", "ticket_ordered", "extra1", "extra2"]
    for col in required:
        if col not in df.columns:
            df[col] = ""

    # Opruimen: verwijder lege kolommen die per ongeluk zijn toegevoegd
    df = df.loc[:, ~df.columns.str.contains('^Unnamed|^Relatiecode;')]  # kill junk like "Relatiecode;Volledige naam"

    return df


def save_admin_csv(df):
    # Altijd opslaan met komma en correcte quoting
    df.to_csv(CSV_FILE, sep=',', index=False, quoting=csv.QUOTE_MINIMAL, encoding='utf-8')
    st.success(f"Admin database opgeslagen: {CSV_FILE} ({len(df)} rijen)")


def load_and_merge_input(uploaded_file=None):
    df_admin = load_admin_csv()

    if uploaded_file:
        content = uploaded_file.getvalue().decode('utf-8')
        delim = detect_delimiter(content)
        new_df = pd.read_csv(io.StringIO(content), sep=delim, dtype=str, quoting=csv.QUOTE_MINIMAL)
        st.info(f"Geüpload bestand gelezen met delimiter '{delim}' – {len(new_df)} rijen gevonden.")
    else:
        if os.path.exists(INPUT_EXAMPLE):
            delim = detect_delimiter(INPUT_EXAMPLE)
            new_df = pd.read_csv(INPUT_EXAMPLE, sep=delim, dtype=str, quoting=csv.QUOTE_MINIMAL)
            st.info(f"Voorbeeld {INPUT_EXAMPLE} gebruikt (delimiter: {delim})")
        else:
            st.warning("Geen input bestand gevonden.")
            return df_admin

    # Hou alleen de kernkolommen van de import
    core_cols = ["Relatiecode", "Volledige naam", "Geboortedatum", "E-mail"]
    new_df = new_df[[c for c in core_cols if c in new_df.columns]]

    # Merge op Relatiecode (update bestaande, voeg nieuwe toe)
    df_merged = pd.merge(df_admin, new_df, on="Relatiecode", how="outer", suffixes=("", "_new"), indicator=True)

    # Neem nieuwe waarden als ze ontbreken
    for col in ["Volledige naam", "Geboortedatum", "E-mail"]:
        df_merged[col] = df_merged[col].combine_first(df_merged[f"{col}_new"])
        if f"{col}_new" in df_merged.columns:
            df_merged.drop(columns=f"{col}_new", inplace=True)

    # Behoud betaalstatus kolommen
    for col in ["paid", "ticket_ordered", "extra1", "extra2"]:
        if col not in df_merged.columns:
            df_merged[col] = ""

    # Opruimen
    df_merged = df_merged.drop(columns=['_merge'], errors='ignore')
    df_merged = df_merged.drop_duplicates(subset="Relatiecode", keep="last")

    return df_merged


def main():
    st.title("Database Manager - VDZ Tickets")

    uploaded_file = st.file_uploader("Upload nieuwe Sportlink export (CSV)", type=["csv"])

    df = load_and_merge_input(uploaded_file=uploaded_file)

    st.subheader("Database Preview")
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    if st.button("Opslaan"):
        save_admin_csv(edited_df)
        st.rerun()

    st.subheader("Stats")
    sold = len(df[df["ticket_ordered"].str.lower() == "yes"])
    st.write(f"Tickets verkocht: **{sold}**")


if __name__ == "__main__":
    main()