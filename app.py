import streamlit as st
import google.generativeai as genai
import time
import os

# --- এপিআই কী সেটআপ ---
API_KEY = "AIzaSyAtrQELPcIDk_uUs5NgdkcmhmJEoA8X7y8" 
genai.configure(api_key=API_KEY)

# পেজ কনফিগারেশন
st.set_page_config(page_title="AI Video Analyzer", page_icon="🎥")

st.title("🎬 Video to AI Prompt Generator")
st.write("সহজেই ভিডিও থেকে প্রম্পট তৈরি করুন।")

# ১. ভিডিও ফাইল আপলোড করার অপশন
uploaded_file = st.file_uploader("আপনার ভিডিও ফাইলটি এখানে ড্রপ করুন", type=["mp4", "mov", "avi", "mkv"])

# ফাইল আপলোড হলে পরবর্তী ধাপগুলো শুরু হবে
if uploaded_file is not None:
    # ভিডিওর প্রিভিউ দেখানো
    st.video(uploaded_file)
    
    st.write("---") # একটি ডিভাইডার বা দাগ
    
    # ২. প্রম্পট জেনারেট করার বাটন (এটি ভিডিও আপলোডের নিচেই থাকবে)
    if st.button("Generate Prompt ✨"):
        try:
            with st.spinner('ভিডিওটি বিশ্লেষণ করা হচ্ছে... অনুগ্রহ করে অপেক্ষা করুন।'):
                # ভিডিওটি টেম্পোরারি সেভ করা
                with open("temp_video.mp4", "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Gemini-তে ভিডিও আপলোড
                video_file = genai.upload_file(path="temp_video.mp4")
                
                # ভিডিওটি পুরোপুরি প্রসেস হওয়া পর্যন্ত অপেক্ষা করা
                while video_file.state.name == "PROCESSING":
                    time.sleep(2)
                    video_file = genai.get_file(video_file.name)

                if video_file.state.name == "FAILED":
                    st.error("দুঃখিত, গুগল ভিডিওটি প্রসেস করতে ব্যর্থ হয়েছে।")
                else:
                    # AI মডেল কল করা
                    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                    prompt_query = (
                        "Describe this video in detail for an AI video generator prompt. "
                        "Include mood, lighting, style, and camera movement."
                    )
                    
                    response = model.generate_content([video_file, prompt_query])

                    # ফলাফল দেখানো
                    st.success("প্রম্পট তৈরি সম্পন্ন হয়েছে!")
                    st.subheader("আপনার প্রম্পট:")
                    st.code(response.text, language='text')

                # কাজ শেষে ফাইল ডিলিট করা (নিরাপত্তার জন্য)
                genai.delete_file(video_file.name)
                if os.path.exists("temp_video.mp4"):
                    os.remove("temp_video.mp4")

        except Exception as e:
            st.error(f"একটি সমস্যা হয়েছে: {e}")
else:
    st.info("শুরু করতে প্রথমে একটি ভিডিও ফাইল আপলোড করুন।")
