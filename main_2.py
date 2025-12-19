import streamlit as st
import pandas as pd

# -------------------------------
# Load CSV
# -------------------------------
df = pd.read_csv("vdz.csv")
df["Relatiecode"] = df["Relatiecode"].astype(str)

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(
    page_title="Football Club Ticket Validation",
    page_icon="🏟️",
    layout="centered",
)

# -------------------------------
# Header / Banner
# -------------------------------
st.title("🏟️ Club Ticket Validation")
st.markdown(
    "Enter your **Club ID** below to check eligibility and purchase a ticket."
)

st.divider()

# -------------------------------
# Input & Validation
# -------------------------------
user_id = st.text_input("Club ID", placeholder="e.g., TKRL41D")

if st.button("Validate"):
    match = df[df["Relatiecode"] == user_id]

    if not match.empty:
        st.success("✅ ID is valid!")

        row = match.iloc[0]

        st.subheader("Matched User Info")
        st.write(f"**Relatiecode:** {row['Relatiecode']}")
        st.write(f"**Name:** {row['Volledige naam']}")
        st.write(f"**Date of Birth:** {row['Geboortedatum']}")
        st.write(f"**Email:** {row['E-mail']}")

        st.markdown("---")

        # Pay Now button (native widget)
        st.write("Click below to proceed to checkout:")
        checkout_url = f"https://ticketsales.infinityfree.me/checkout/?add-to-cart=13&billing_address_2={user_id}"
        if st.button("💳 Pay Now"):
            st.markdown(f"[Proceed to Checkout]({checkout_url})", unsafe_allow_html=True)

    else:
        st.error("❌ Invalid ID. Please check your Club ID.")

# -------------------------------
# Debug CSV dump (admin only)
# -------------------------------
st.divider()
st.subheader("DEBUG – Full CSV Dump")
st.dataframe(df)
