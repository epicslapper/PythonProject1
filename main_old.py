import streamlit as st
st.write("Hello, World! 🎈")


import streamlit as st
from pathlib import Path

def tree(path: Path, prefix=""):
    result = ""
    for p in sorted(path.iterdir()):
        if p.name.startswith(".") and p.name not in [".gitignore"]:
            continue
        result += prefix + p.name + "\n"
        if p.is_dir():
            result += tree(p, prefix + "  ")
    return result

st.title("Hello Streamlit!")
st.subheader("Repository Structure")
st.text(tree(Path(".")))



