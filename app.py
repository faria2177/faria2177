import streamlit as st
import google.generativeai as genai
import time
import os

# --- কনফিগারেশন ---
API_KEY = "AIzaSyAtrQELPcIDk_uUs5NgdkcmhmJEoA8X7y8" 
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Video to AI Prompt", page_icon="🎬")

# এখানে unsafe_allow_html=True ব্যবহার করা হয়েছে (সংশোধিত)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 AI Video Prompt Generator")
st.info("ভিডিও আপলোড করুন এবং এআই আপনার ভিডিওর জন্য একটি টেক্সট প্রম্পট লিখে দেবে।")

uploaded_file = st.file_uploader("ভিডিও ফাইল নির্বাচন করুন (MP4, MOV, AVI)...", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.video("temp_video.mp4")

    if st.button("Generate Prompt ✨"):
        try:
            with st.spinner('AI ভিডিওটি দেখছে... ধৈর্য ধরুন।'):
                video_file = genai.upload_file(path="temp_video.mp4")
                
                while video_file.state.name == "PROCESSING":
                    time.sleep(2)
                    video_file = genai.get_file(video_file.name)

                model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                prompt = (
                    "Analyze this video and provide a high-quality descriptive prompt. "
                    "Describe the visual elements, camera movement, lighting, and style."
                )
                
                response = model.generate_content([video_file, prompt])

                st.success("কাজ সম্পন্ন হয়েছে!")
                st.subheader("Generated Prompt:")
                st.code(response.text, language='text')
                
                genai.delete_file(video_file.name)
                os.remove("temp_video.mp4")

        except Exception as e:
            st.error(f"দুঃখিত, একটি সমস্যা হয়েছে: {e}")
