# app.py
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
        with st.spinner("Processing..."):
            try:
                resp = requests.get(
                    FASTAPI_URL,
                    params={"topic": topic}
                )

                if resp.status_code != 200:
                    st.error("Please try again.")
                else:
                    data = resp.json()
                    exercises = data.get("exercises", None)
                    answers = data.get("answers", None)

                    if exercises and not answers:
                        st.subheader("📝 Practice Exercises")
                        st.write(exercises)

                    elif exercises and answers:
                        st.subheader("📝 Practice Exercises")
                        st.write(exercises)

                        st.subheader("✅ Answers")
                        st.write(answers)

                    else:
                        backend_path = data["mp4"]
                        local_path = backend_path.replace("/app/data", "/app/backend/data")
                        if os.path.exists(local_path):
                            with open(local_path, "rb") as f:
                                st.video(f.read())

            except Exception:
                st.error("Please try again.")

