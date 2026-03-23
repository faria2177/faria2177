import streamlit as st
import google.generativeai as genai
import time
import os

# --- এপিআই কী সেটআপ (নিরাপদ রাখার চেষ্টা করবেন) ---
# আপনার দেওয়া কী-টি এখানে আছে। এটি কাজ না করলে নতুন কী তৈরি করে নেবেন।
API_KEY = "AIzaSyAtrQELPcIDk_uUs5NgdkcmhmJEoA8X7y8" 
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Video Prompt AI", page_icon="🎬", layout="centered")

# ইন্টারফেস সুন্দর করার জন্য কিছু CSS
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #007BFF;
        color: white;
        height: 3em;
        font-size: 20px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 Video to AI Prompt Generator")
st.write("নিচের বক্সে ভিডিও আপলোড করুন এবং প্রম্পট জেনারেট করুন।")

# ১. ভিডিও আপলোড সেকশন
uploaded_file = st.file_uploader("ভিডিও ফাইল নির্বাচন করুন (MP4, MOV, AVI)", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    # ভিডিওর প্রিভিউ দেখানো
    st.info("ভিডিওটি আপলোড হয়েছে। নিচে বাটনে ক্লিক করুন।")
    st.video(uploaded_file)
    
    st.write("---") # একটি ডিভাইডার বা রেখা

    # ২. জেনারেট বাটন (ভিডিওর ঠিক নিচে)
    if st.button("Generate Prompt ✨"):
        try:
            with st.spinner('এআই ভিডিওটি বিশ্লেষণ করছে... এটি ১-২ মিনিট সময় নিতে পারে।'):
                # ভিডিওটি সাময়িকভাবে সেভ করা
                with open("temp_video.mp4", "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # জেমিনিতে ভিডিও আপলোড
                video_file = genai.upload_file(path="temp_video.mp4")
                
                # প্রসেসিং স্ট্যাটাস চেক করা
                while video_file.state.name == "PROCESSING":
                    time.sleep(3)
                    video_file = genai.get_file(video_file.name)

                if video_file.state.name == "FAILED":
                    st.error("ভিডিওটি প্রসেস করতে ব্যর্থ হয়েছে। আবার চেষ্টা করুন।")
                else:
                    # এআই মডেল থেকে উত্তর নেওয়া
                    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                    response = model.generate_content([
                        video_file, 
                        "Analyze this video and write a detailed prompt for an AI video generator. Describe objects, colors, camera movements, and the overall mood."
                    ])

                    # আউটপুট দেখানো
                    st.success("প্রম্পট তৈরি সম্পন্ন হয়েছে!")
                    st.subheader("আপনার প্রম্পট:")
                    st.code(response.text, language='text')

                # ফাইল মুছে ফেলা
                genai.delete_file(video_file.name)
                os.remove("temp_video.mp4")

        except Exception as e:
            st.error(f"দুঃখিত, একটি সমস্যা হয়েছে। এরর মেসেজ: {e}")
            st.warning("টিপস: আপনার API Key ব্লক হয়ে থাকতে পারে। নতুন কী ব্যবহার করে দেখুন।")

else:
    st.warning("প্রথমে একটি ভিডিও আপলোড করুন।")
