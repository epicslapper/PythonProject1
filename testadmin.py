import streamlit as st

def main():
    st.title("Test Admin Callback")

    params = st.experimental_get_query_params()
    member_id = params.get("member_id", [None])[0]

    if member_id:
        st.success("Member ID received")
        st.code(member_id)
    else:
        st.warning("No member_id found in URL")

if __name__ == "__main__":
    main()
