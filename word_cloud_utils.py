import matplotlib.pyplot as plt
from wordcloud import WordCloud
import streamlit as st

font_path = r'/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf'


def display_word_cloud(data, width=1200, height=500):
    word_cloud = WordCloud(font_path=font_path,
                          width=width,
                          height=height,
                          background_color="white",
                          random_state=42
                         ).generate(data)
    plt.figure()
    plt.imshow(word_cloud, interpolation="bilinear")
    plt.axis("off")

    st.pyplot(plt)
