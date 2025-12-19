import streamlit as st
import pandas as pd

# -------------------------------
# Load CSV
# -------------------------------
df = pd.read_csv("vdz.csv")
df["Relatiecode"] = df["Relatiecode"].astype(str)

# -------------------------------
# UI
# -------------------------------
st.title("Club Ticket Validation")

user_id = st.text_input("Enter your Relatiecode / Club ID")

if st.button("Validate"):
    match = df[df["Relatiecode"] == user_id]

    if not match.empty:
        st.success("ID is valid")
        row = match.iloc[0]

        st.subheader("Matched user")
        st.write(f"**Relatiecode:** {row['Relatiecode']}")
        st.write(f"**Name:** {row['Volledige naam']}")
        st.write(f"**Date of birth:** {row['Geboortedatum']}")
        st.write(f"**Email:** {row['E-mail']}")

        # -------------------------------
        # Pay Now Button
        # -------------------------------
        product_id = 13  # Your ticket product ID
        checkout_url = f"https://ticketsales.infinityfree.me/checkout/?add-to-cart={product_id}&billing_address_2={user_id}"

        st.markdown(
            f"""
            <a href="{checkout_url}" target="_blank">
                <button style="padding:10px 20px;font-size:16px;">
                    Pay Now
                </button>
            </a>
            """,
            unsafe_allow_html=True
        )
    else:
        st.error("Invalid ID")

# -------------------------------
# FULL CSV DUMP (debug / admin)
# -------------------------------
st.divider()
st.subheader("DEBUG – Full CSV dump")
st.dataframe(df)
