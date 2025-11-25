import streamlit as st
import requests
import os

FASTAPI_URL = "http://fastapi-backend:8000/generate"

st.set_page_config(page_title="Educative AI Video Generator")
st.title("🎬 Educative AI Video Generator")

topic = st.chat_input("Enter a topic...")

if topic:
    with st.chat_message("user"):
        st.write(topic)

    with st.chat_message("assistant"):

        # -----------------------
        # RUN BACKEND inside spinner
        # -----------------------
        with st.spinner("Processing..."):
            try:
                resp = requests.get(
                    FASTAPI_URL,
                    params={"topic": topic},
                    timeout=120
                )

                if resp.status_code != 200:
                    st.error("Generation failed.")
                    st.stop()

                data = resp.json()

            except Exception:
                st.error("Generation failed.")
                st.stop()  # important!

        # -----------------------
        # SPINNER HAS STOPPED HERE
        # -----------------------

        # Now show exercises WITHOUT spinner
        exercises = data.get("exercises")
        if exercises:
            st.subheader("📝 Practice Exercises")
            st.write(exercises)
            st.stop()

        # -----------------------
        # Otherwise show video
        # -----------------------
        mp4_path = data.get("mp4")

        if not mp4_path:
            st.info("No video generated.")
            st.stop()

        backend_path = mp4_path
        local_path = backend_path.replace("/app/data", "/app/backend/data")

        if os.path.exists(local_path):
            with open(local_path, "rb") as f:
                st.video(f.read())
        else:
            st.error("Video file not found.")
