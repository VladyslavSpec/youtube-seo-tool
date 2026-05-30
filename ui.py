import streamlit as st
import requests

st.set_page_config(page_title="YouTube SEO Generator", page_icon="🎬")

st.title("YouTube SEO Generator")
st.write("Enter your video topic and get an optimized title, description, and tags.")

topic = st.text_input("Video topic", placeholder="e.g. how to make money on YouTube")
language = st.selectbox("Language", ["English", "Spanish", "French", "German"])

if st.button("Generate SEO", type="primary"):
    if not topic:
        st.error("Please enter a topic first.")
    else:
        with st.spinner("Generating..."):
            response = requests.post(
                "http://127.0.0.1:8000/generate-seo",
                json={"topic": topic, "language": language},
            )
            data = response.json()

        st.success("Done!")

        st.subheader("Title")
        st.code(data["title"], language=None)

        st.subheader("Description")
        st.text_area("", value=data["description"], height=250)

        st.subheader("Tags")
        st.write(", ".join(data["tags"]))
