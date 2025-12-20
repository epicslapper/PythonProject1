import streamlit as st
import pandas as pd
import os

# -------------------------------
# Constants
# -------------------------------
CSV_FILE = "vdz_admin.csv"
LOG_FILE = "url_callbacks.log"
DEFAULT_COLUMNS = ["ticket_ordered", "paid_flag", "last_callback_url", "future_col"]

# -------------------------------
# Functions
# -------------------------------
def load_csv(file_path):
    """Load CSV if exists, else return empty dataframe"""
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, dtype=str)
        # Ensure extra columns exist
        for col in DEFAULT_COLUMNS:
            if col not in df.columns:
                df[col] = ""
        return df
    else:
        return pd.DataFrame(columns=["Relatiecode", "Volledige naam", "Geboortedatum", "E-mail"] + DEFAULT_COLUMNS)

def upload_csv():
    """Allow user to upload a CSV file and store it locally"""
    uploaded_file = st.file_uploader("Upload new club member CSV (optional)", type=["csv"])
    if uploaded_file is not None:
        df_new = pd.read_csv(uploaded_file, dtype=str)
        for col in DEFAULT_COLUMNS:
            if col not in df_new.columns:
                df_new[col] = ""
        df_new.to_csv(CSV_FILE, index=False)
        st.success("CSV uploaded and saved!")
        return df_new
    return None

def update_from_url(df):
    """Check Streamlit URL params and update dataframe"""
    params = st.query_params  # Only use st.query_params
    raw_url = f"?{'&'.join([f'{k}={v[0]}' for k,v in params.items()])}" if params else ""
    if raw_url:
        with open(LOG_FILE, "a") as f:
            f.write(raw_url + "\n")

    if "member_id" in params:
        member_id = params["member_id"][0]
        paid_flag = params.get("paid", ["0"])[0]

        if member_id in df["Relatiecode"].values:
            df.loc[df["Relatiecode"] == member_id, "ticket_ordered"] = "yes"
            df.loc[df["Relatiecode"] == member_id, "paid_flag"] = paid_flag
            df.loc[df["Relatiecode"] == member_id, "last_callback_url"] = raw_url
            st.success(f"Callback received: member {member_id}, paid={paid_flag}")
        else:
            st.warning(f"Member ID {member_id} not found in database")
    return df

def show_dataframe(df):
    """Show full dataframe"""
    st.subheader("Club Members Database")
    st.dataframe(df)

def show_sales_graph(df):
    """Show simple graph of ticket sales"""
    st.subheader("Ticket Sales Overview")
    sales_df = df["ticket_ordered"].value_counts().reindex(["yes", "no"], fill_value=0)
    st.bar_chart(sales_df)

def save_df(df):
    """Persist dataframe to CSV"""
    df.to_csv(CSV_FILE, index=False)
    st.info("Database saved!")

# -------------------------------
# Main
# -------------------------------
def main():
    st.title("Club Ticket Admin Backoffice")

    # Step 1: Load existing CSV
    df = load_csv(CSV_FILE)

    # Step 2: Optional CSV upload
    df_new = upload_csv()
    if df_new is not None:
        df = df_new  # replace with uploaded CSV but keep extra columns

    # Step 3: Update from URL if callback
    df = update_from_url(df)

    # Step 4: Show dataframe
    show_dataframe(df)

    # Step 5: Show sales graph
    show_sales_graph(df)

    # Step 6: Save button
    if st.button("Save Database"):
        save_df(df)

if __name__ == "__main__":
    main()
