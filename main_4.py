import streamlit as st
import pandas as pd

# -------------------------------
# Functions
# -------------------------------
def load_data():
    """Load club members CSV and ensure member_id column is string."""
    df = pd.read_csv("vdz.csv")
    df["Relatiecode"] = df["Relatiecode"].astype(str)
    return df

def validate_member(df, member_id):
    """Check if the member_id exists in the CSV."""
    return not df[df["Relatiecode"] == member_id].empty

def display_user_info(df, member_id):
    """Display member info if valid."""
    row = df[df["Relatiecode"] == member_id].iloc[0]
    st.subheader("Matched Member")
    st.write(f"**Member ID:** {row['Relatiecode']}")
    st.write(f"**Name:** {row['Volledige naam']}")
    st.write(f"**Date of Birth:** {row['Geboortedatum']}")
    st.write(f"**Email:** {row['E-mail']}")

def show_pay_button(member_id):
    """Render Pay Now button linking to WooCommerce checkout with member_id."""
    st.markdown(
        f"""
        <a href="https://your-wordpress-site/checkout/?add-to-cart=13&member_id={member_id}" target="_blank">
            <button style="padding:10px 20px;font-size:16px;">Pay Now</button>
        </a>
        """,
        unsafe_allow_html=True
    )

# -------------------------------
# Main
# -------------------------------
def main():
    st.title("Club Ticket Validation")
    st.write("Enter your Member ID to check if you are eligible for a ticket.")

    df = load_data()
    member_id_input = st.text_input("Enter Member ID")

    if st.button("Validate"):
        if validate_member(df, member_id_input):
            st.success("Member ID is valid ✅")
            display_user_info(df, member_id_input)
            show_pay_button(member_id_input)
        else:
            st.error("Invalid Member ID ❌")

if __name__ == "__main__":
    main()
