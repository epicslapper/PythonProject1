import streamlit as st
import pandas as pd

def load_data():
    df = pd.read_csv("vdz.csv")
    df["Relatiecode"] = df["Relatiecode"].astype(str)
    return df

def debug_dump(df):
    st.subheader("Admin – Full Member List")
    st.dataframe(df)

def main():
    st.title("Club Admin Panel")
    st.write("Debug / full member data view. Only for admin use!")

    df = load_data()
    debug_dump(df)

if __name__ == "__main__":
    main()
