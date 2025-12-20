import streamlit as st
import pandas as pd
import os

CSV_FILE = "vdz_admin.csv"
URL_LOG = "url_log.txt"

def load_csv():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE, dtype=str)
    else:
        st.error("Database CSV not found.")
        return None

def save_csv(df):
    df.to_csv(CSV_FILE, index=False)
    st.info(f"Database saved: {CSV_FILE}")

def process_url(df):
    params = st.query_params
    st.write("DEBUG: URL query params:", params)

    if "member_id" in params:
        member_id = params.get("member_id", [""])[0].strip()
        paid = params.get("paid", ["0"])[0].strip()
        st.write(f"DEBUG: Extracted member_id={member_id}, paid={paid}")

        # Log callback
        with open(URL_LOG, "a") as f:
            f.write(f"{member_id},{paid}\n")

        if member_id in df["Relatiecode"].values:
            df.loc[df["Relatiecode"] == member_id, "paid"] = paid
            df.loc[df["Relatiecode"] == member_id, "ticket_ordered"] = "yes"
            st.success(f"Member {member_id} updated in database!")
        else:
            st.warning(f"Member ID {member_id} NOT found in database.")
    else:
        st.info("No member_id in URL params.")
    return df

def main():
    st.title("URL Processor")
    df = load_csv()
    if df is not None:
        df = process_url(df)
        st.subheader("Database Preview")
        st.dataframe(df)
        save_csv(df)

if __name__ == "__main__":
    main()
