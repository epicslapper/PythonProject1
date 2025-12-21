import pandas as pd
import os
import streamlit as st

CSV_FILE = "vdz_admin.csv"


def load_csv():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE, dtype=str)
        st.success(f"Loaded CSV with {len(df)} rows.")
    else:
        df = pd.DataFrame(columns=[
            "Relatiecode", "Volledige naam", "Geboortedatum", "E-mail",
            "paid", "ticket_ordered", "extra1", "extra2"
        ])
        st.info("No CSV found. Starting fresh.")

    for col in ["paid", "ticket_ordered", "extra1", "extra2"]:
        if col not in df.columns:
            df[col] = ""
    return df


def save_csv(df):
    df.to_csv(CSV_FILE, index=False)
    st.info(f"Database saved: {CSV_FILE}")


def main():
    st.title("Database Manager")
    df = load_csv()
    uploaded_file = st.file_uploader("Upload new CSV (optional)", type=["csv"])
    if uploaded_file:
        new_df = pd.read_csv(uploaded_file, dtype=str)
        for col in ["paid", "ticket_ordered", "extra1", "extra2"]:
            if col not in new_df.columns:
                new_df[col] = ""
        df = pd.concat([df, new_df], ignore_index=True)
        df = df.drop_duplicates(subset="Relatiecode", keep="last")
        st.success(f"CSV uploaded. Total rows now: {len(df)}")

    st.subheader("Database Preview")
    st.dataframe(df)
    save_csv(df)


if __name__ == "__main__":
    main()
