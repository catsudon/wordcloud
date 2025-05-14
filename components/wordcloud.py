from wordcloud import WordCloud, STOPWORDS
from pythainlp.tokenize import word_tokenize
from collections import Counter
from config import custom_vocab
from pythainlp.corpus.common import thai_stopwords
import re


# Optional: Thai font (download Sarabun or Noto Sans Thai if needed)
THAI_FONT_PATH = "fonts/FC Lamoon Regular ver 1.00.ttf"
stopwords = set(thai_stopwords())

def merge_numbers_with_context(tokens):
    merged = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        next_token = tokens[i+1] if i+1 < len(tokens) else ""

        # กรณีปี เช่น "ปี 2550"
        if token == "ปี" and re.fullmatch(r"\d{4}", next_token):
            merged.append(token + " " + next_token)
            i += 2

        # กรณีเงิน เช่น "2550 บาท"
        elif re.fullmatch(r"\d+(\.\d+)?", token) and next_token in ["บาท", "ล้าน", "แสน", "หมื่น", "พัน", "ร้อย", "วินาที", "นาที", "ชั่วโมง", "วัน", "เดือน", "ปี"]:
            merged.append(token + " " + next_token)
            i += 2

        # กรณีเวลา เช่น "19.15 น."
        elif re.fullmatch(r"\d{1,2}\.\d{1,2}", token) and next_token in ["น.", "นาฬิกา"]:
            merged.append(token + " " + next_token)
            i += 2

        # ลบตัวเลขโดดๆที่ไม่เข้ากลุ่มข้างบน
        elif re.fullmatch(r"\d+", token):
            i += 1  # skip

        else:
            merged.append(token)
            i += 1

    return merged

def generate_thai_wordcloud(text_input, output_file="img/wordcloud.png"):
    tokens = word_tokenize(
        text_input.replace("\n", " "),
        engine="deepcut",
        custom_dict=custom_vocab,
        keep_whitespace=False,
    )
    tokens = merge_numbers_with_context(tokens)
    filtered_tokens = [
        t
        for t in tokens
        if t.strip() != ""
        and t not in stopwords
    ]
    filtered_freqs = Counter(filtered_tokens)

    wc = WordCloud(
        font_path=THAI_FONT_PATH, width=800, height=600, background_color="black"
    ).generate_from_frequencies(filtered_freqs)

    wc.to_file(output_file)
    print(f"Wordcloud saved to {output_file}")