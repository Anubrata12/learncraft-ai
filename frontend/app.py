import streamlit as st
import base64
import os

st.set_page_config(page_title="AI Video", layout="centered")

VIDEO_PATH = "/app/backend/data/videos/music_video.mp4"

st.title("🎬 Educative AI Video Player")

# Chat-style input stays visible
query = st.chat_input("Enter a topic...")

if query:
    st.chat_message("user").write(query)
    st.chat_message("assistant").write("Generating video...")

    if not os.path.exists(VIDEO_PATH):
        st.error(f"Video file not found at: {VIDEO_PATH}")
    else:
        video_bytes = open(VIDEO_PATH, "rb").read()
        video_b64 = base64.b64encode(video_bytes).decode("utf-8")

        st.markdown(
            f"""
            <video width="100%" controls style="border-radius:12px;">
                <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
            </video>
            """,
            unsafe_allow_html=True
        )
