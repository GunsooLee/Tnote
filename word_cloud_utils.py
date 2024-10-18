import matplotlib.pyplot as plt
from wordcloud import WordCloud
import streamlit as st
from pecab import PeCab

font_path = r'/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf'

stopwords = ['하지만', '그리고', '그런데', '저는','제가',
             '그럼', '이런', '저런', '합니다',
             '많은', '많이', '정말', '너무', '수', '등', '것',
             '같습니다' , '좀' , '같아요' , '가' , '거']


def display_word_cloud(data, width=1200, height=500):
    pecab = PeCab()
    nouns = " ".join(pecab.nouns(data)) #명사만 가져오기
    
    word_cloud = WordCloud(font_path=font_path,
                          width=width,
                          height=height,
                          stopwords=stopwords,
                          background_color="white",
                          random_state=42
                         ).generate(nouns)
    plt.figure()
    plt.imshow(word_cloud, interpolation="bilinear")
    plt.axis("off")

    # st.pyplot(plt)
    return plt