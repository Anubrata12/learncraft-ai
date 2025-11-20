import frontend as st
import requests

st.title("LearnCraft AI")

st.write("This is your Streamlit frontend.")

if st.button("Ping FastAPI"):
    response = requests.get("http://fastapi-backend:8000/")
    st.json(response.json())
