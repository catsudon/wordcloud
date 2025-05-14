import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from pythainlp.tokenize import word_tokenize
from collections import Counter
from components.wordcloud import generate_thai_wordcloud

# Optional: Thai font (download Sarabun or Noto Sans Thai if needed)
THAI_FONT_PATH = "fonts/FC Lamoon Regular ver 1.00.ttf"

st.set_page_config(page_title="Thai WordCloud", layout="centered")
st.title("☁️ Thai WordCloud Generator")

text_input = st.text_area("ใส่ข้อความภาษาไทยที่นี่", height=200)


if st.button("Generate WordCloud"):
    generate_thai_wordcloud(text_input)
    st.image("img/wordcloud.png", caption="Generated WordCloud", use_container_width =True)