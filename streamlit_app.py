import os
import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="SecureAPI Streamlit", layout="centered")
st.title("SecureAPI Prototype (Streamlit)")

st.markdown("Enter your prompt and the app will call the SecureAPI backend (Flask / SOP).")

prompt = st.text_area("Prompt", height=150)

if st.button("Submit"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        try:
            endpoint = os.getenv("SECUREAPI_BACKEND", "http://localhost:5000/api/secureapi")
            resp = requests.post(endpoint, json={"prompt": prompt}, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                st.subheader("Response")
                st.text_area("Output", value=data.get("output", ""), height=200)
            else:
                st.error(f"Backend error: {resp.status_code} - {resp.text}")
        except Exception as e:
            st.error(f"Request failed: {e}")
