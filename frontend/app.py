import streamlit as st
import requests
import os

FASTAPI_URL = "http://fastapi-backend:8000/generate"

st.set_page_config(page_title="Educative AI Video Generator")
st.title("Educative AI Video Generator")

topic = st.chat_input("Enter a topic...")

if topic:
    with st.chat_message("user"):
        st.write(topic)

    with st.chat_message("assistant"):
        with st.spinner("Processing..."):

            try:
                # Call FastAPI
                resp = requests.get(
                    FASTAPI_URL,
                    params={"topic": topic}
                )

                if resp.status_code != 200:
                    st.error("Video generation failed.")
                    st.stop()

                data = resp.json()

                #if "mp4" not in data:
                 #   st.error("Backend did not return an mp4 path.")
                 #   st.stop()

                # ⬇️ NEW — display exercises if present
                exercises = data.get("exercises", None)
                print("EXERCISE_TEXT:", exercises)
                if exercises:
                    st.subheader("📝 Practice Exercises")
                    st.write(exercises)
                    st.stop()

                backend_path = data["mp4"]  # e.g. /app/data/videos/algebra.mp4

                # Convert backend path → Streamlit container path
                local_path = backend_path.replace("/app/data", "/app/backend/data")

                if not os.path.exists(local_path):
                    #st.error(f"Video file not found at: {local_path}")
                    st.stop()

                # Load and play video
                with open(local_path, "rb") as f:
                    st.video(f.read())

            except Exception as e:
                st.error("Video generation failed.")
