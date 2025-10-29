import streamlit as st
import requests

st.title("AI Code Review Dashboard")

uploaded_files = st.file_uploader("Upload Source Files", accept_multiple_files=True)
if uploaded_files and st.button("Run Review"):
    st.info("Reviewing code, please wait...")
    files = [("files", (f.name, f.getvalue())) for f in uploaded_files]
    res = requests.post("http://localhost:8000/review/", files=files)
    if res.ok:
        data = res.json()
        for item in data["reviews"]:
            st.subheader(item["filename"])
            st.markdown(item["review"])
    else:
        st.error("Error during analysis.")
