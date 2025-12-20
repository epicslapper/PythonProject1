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
    checkout_url = (
            "https://ticketsales.infinityfree.me/checkout/"
            "?add-to-cart=13&member_id=" + member_id
    )

    st.markdown(
        f"""
        <a href="{checkout_url}" target="_blank">
            <button style="padding:12px 24px;font-size:16px;">
                Pay €10 – Buy Ticket
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

def debug_dump(df):
    # intentionally empty in main app
    pass

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

if __name__ == "__main__":
    main()







    # checkout_url = (
    # f"https://ticketsales.infinityfree.me/checkout/"
    # f"?add-to-cart=13&football_id={member_id}"-------------------------------
    #   )
