import streamlit as st
import pandas as pd
import os

CSV_FILE = "vdz_admin.csv"

# -------------------------------
# Load or initialize CSV
# -------------------------------
def load_csv():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE, dtype=str)
        st.success(f"Loaded CSV with {len(df)} rows.")
    else:
        df = pd.DataFrame(columns=["Relatiecode", "Volledige naam", "Geboortedatum", "E-mail",
                                   "paid", "ticket_ordered", "extra1", "extra2"])
        st.info("No CSV found. Start fresh.")
    # Ensure extra columns exist
    for col in ["paid", "ticket_ordered", "extra1", "extra2"]:
        if col not in df.columns:
            df[col] = ""
    return df

# -------------------------------
# Update from URL params
# -------------------------------
def update_from_url(df):
    params = st.query_params
    if "member_id" in params:
        member_id = params.get("member_id", [""])[0].strip()
        paid = params.get("paid", ["0"])[0].strip()

        if member_id in df["Relatiecode"].values:
            df.loc[df["Relatiecode"] == member_id, "paid"] = paid
            df.loc[df["Relatiecode"] == member_id, "ticket_ordered"] = "yes"
            st.success(f"Member {member_id} updated: paid={paid}")
        else:
            st.warning(f"Member ID {member_id} not found in database.")
    return df

# -------------------------------
# Upload new CSV (optional)
# -------------------------------
def upload_csv(df):
    uploaded_file = st.file_uploader("Upload new CSV (optional)", type=["csv"])
    if uploaded_file:
        new_df = pd.read_csv(uploaded_file, dtype=str)
        # Merge new rows, keep existing columns and added columns
        for col in ["paid", "ticket_ordered", "extra1", "extra2"]:
            if col not in new_df.columns:
                new_df[col] = ""
        df = pd.concat([df, new_df], ignore_index=True)
        df = df.drop_duplicates(subset="Relatiecode", keep="last")
        st.success(f"CSV uploaded. Total rows now: {len(df)}")
    return df

# -------------------------------
# Save CSV
# -------------------------------
def save_csv(df):
    df.to_csv(CSV_FILE, index=False)
    st.info(f"Database saved: {CSV_FILE}")

# -------------------------------
# Display basic stats / graph
# -------------------------------
def display_stats(df):
    st.subheader("Ticket Sales Summary")
    paid_count = df["ticket_ordered"].value_counts().get("yes", 0)
    st.write(f"Total tickets sold: {paid_count}")
    st.bar_chart(df["ticket_ordered"].map(lambda x: 1 if x=="yes" else 0))

# -------------------------------
# Main
# -------------------------------
def main():
    st.title("Ticket Admin Backoffice")

    df = load_csv()
    df = update_from_url(df)
    df = upload_csv(df)
    display_stats(df)
    st.dataframe(df)

    save_csv(df)

if __name__ == "__main__":
    main()
