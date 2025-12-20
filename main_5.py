import streamlit as st
import pandas as pd

# -------------------------------
# Functions
# -------------------------------
def load_data():
    df = pd.read_csv("vdz.csv")
    df["Relatiecode"] = df["Relatiecode"].astype(str)
    return df

def validate_member(df, member_id):
    return not df[df["Relatiecode"] == member_id].empty

def display_user_info(df, member_id):
    row = df[df["Relatiecode"] == member_id].iloc[0]
    st.subheader("Matched Member")
    st.write(f"**Relatiecode:** {row['Relatiecode']}")
    st.write(f"**Name:** {row['Volledige naam']}")
    st.write(f"**Date of Birth:** {row['Geboortedatum']}")
    st.write(f"**Email:** {row['E-mail']}")

def show_pay_button(member_id):
    # Primary: HTTPS link
    url_https = f"https://ticketsales.infinityfreeapp.com/checkout/?add-to-cart=13&member_id={member_id}"
    # Fallback: HTTP link (in case HTTPS shows strikethrough)
    url_http = f"http://ticketsales.infinityfreeapp.com/checkout/?add-to-cart=13&member_id={member_id}"

    st.markdown(
        f"""
        <p>Click to pay for your ticket:</p>
        <a href="{url_https}" target="_blank">
            <button style="padding:10px 20px;font-size:16px;">Pay Now (HTTPS)</button>
        </a>
        <br><br>
        <a href="{url_http}" target="_blank">
            <button style="padding:10px 20px;font-size:16px;">Pay Now (HTTP fallback)</button>
        </a>
        """,
        unsafe_allow_html=True
    )

def debug_dump(df):
    st.divider()
    st.subheader("DEBUG – Full CSV dump")
    st.dataframe(df)

# -------------------------------
# Main App
# -------------------------------
def main():
    st.title("Club Ticket Validation")
    df = load_data()

    user_id = st.text_input("Enter your Relatiecode / Club ID")

    if st.button("Validate"):
        if validate_member(df, user_id):
            st.success("ID is valid")
            display_user_info(df, user_id)
            show_pay_button(user_id)
        else:
            st.error("Invalid ID")

    # Admin/debug
    debug_dump(df)

if __name__ == "__main__":
    main()
