import streamlit as st
import requests

FASTAPI_URL = "http://fastapi-backend:8000/generate"
VIDEO_PATH = "/app/backend/data/videos/Summertime.mp4"

st.title("🎬 Educative AI Video Generator")

topic = st.chat_input("Enter a topic...")

if topic:
    with st.chat_message("user"):
        st.write(topic)

    with st.chat_message("assistant"):
        with st.spinner("Processing..."):

            try:
                # Call FastAPI
                resp = requests.get(FASTAPI_URL, params={"topic": topic}, timeout=90)

                if resp.status_code == 200:
                    # Success → always show the hard-coded video
                    try:
                        with open(VIDEO_PATH, "rb") as f:
                            st.video(f.read())
                    except:
                        st.error(f"Video file not found at: {VIDEO_PATH}")
                else:
                    st.error("Video generation failed.")

            except Exception:
                st.error("Video generation failed.")
