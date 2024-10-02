import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from konlpy.tag import Okt
import streamlit as st



# TF-IDF 벡터화 함수
def tfidf_vectorize(df):
    # 형태소 분석 후 단순화된 텍스트로 변환
    #df['명사 추출'] = df['분석된 내용'].apply(morphs_analysis)
    
    # TF-IDF 벡터화
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    tfidf_matrix = vectorizer.fit_transform(df['분석된 내용'])
    return tfidf_matrix, vectorizer

# TF-IDF 시각화 함수 (막대그래프)
def plot_tfidf_matrix(tfidf_matrix, vectorizer, top_n=20):
    # TF-IDF 결과를 DataFrame으로 변환
    df_tfidf = pd.DataFrame(tfidf_matrix.T.toarray(), index=vectorizer.get_feature_names_out())
    
    # 전체 단어별 TF-IDF 합계 계산
    tfidf_scores = df_tfidf.sum(axis=1).sort_values(ascending=False)
    
    # 상위 top_n개의 단어 선택
    top_tfidf = tfidf_scores.head(top_n)
    
    # 막대그래프 생성
    plt.figure(figsize=(10, 4))
    sns.barplot(x=top_tfidf.index, y=top_tfidf.values, palette="viridis")
    plt.title(f"TF-IDF 키워드 분석 Top {top_n}")
    plt.xlabel("TF-IDF 점수")
    plt.ylabel("단어")

    # x축 레이블을 잘 보이게 회전
    plt.xticks(rotation=45)
    
    # Streamlit에 그래프 표시
    st.pyplot(plt.gcf())
