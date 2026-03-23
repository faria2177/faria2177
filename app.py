import streamlit as st
import google.generativeai as genai
import time
import os

# --- API Key Setup ---
# সরাসরি কোডে না লিখে Streamlit Secrets ব্যবহার করা ভালো
# আপাতত আপনার কি-টি দিয়ে ট্রাই করুন, কাজ না করলে নতুন কি তৈরি করবেন।
API_KEY = "AIzaSyAtrQELPcIDk_uUs5NgdkcmhmJEoA8X7y8" 
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Video to AI Prompt", page_icon="🎬")

st.title("🎬 AI Video Prompt Generator")

uploaded_file = st.file_uploader("ভিডিও ফাইল নির্বাচন করুন...", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    # ভিডিও প্রিভিউ দেখানো
    st.video(uploaded_file)
    
    if st.button("Generate Prompt ✨"):
        try:
            with st.spinner('ভিডিও প্রসেস করা হচ্ছে...'):
                # ভিডিও ফাইল সেভ করা
                with open("temp_video.mp4", "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Gemini-তে আপলোড
                video_file = genai.upload_file(path="temp_video.mp4")
                
                # প্রসেস হওয়া পর্যন্ত অপেক্ষা (ম্যাক্সিমাম ২ মিনিট)
                wait_time = 0
                while video_file.state.name == "PROCESSING" and wait_time < 60:
                    time.sleep(2)
                    video_file = genai.get_file(video_file.name)
                    wait_time += 2

                if video_file.state.name == "FAILED":
                    st.error("গুগল ভিডিওটি প্রসেস করতে পারেনি।")
                else:
                    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                    response = model.generate_content([video_file, "Describe this video for an AI prompt."])
                    
                    st.success("সফলভাবে প্রম্পট তৈরি হয়েছে!")
                    st.code(response.text)

                # ক্লিনআপ
                genai.delete_file(video_file.name)
                if os.path.exists("temp_video.mp4"):
                    os.remove("temp_video.mp4")

        except Exception as e:
            st.error(f"Error Details: {e}") # এখানে এরর মেসেজ দেখাবে
