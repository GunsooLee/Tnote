import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer


# 모델을 받아 변환을 하고 문서 용어 행렬을 반환하는 함수를 만들어 재사용합니다.
def display_transform_dtm(cvect, corpus):
    X = cvect.fit_transform(corpus)
    print(cvect.get_feature_names_out())
    df_dtm = pd.DataFrame(X.toarray(), columns=cvect.get_feature_names_out())
    return df_dtm

# TF-IDF 벡터화 함수
def tfidf_vectorize(df):
    # 형태소 분석 후 단순화된 텍스트로 변환
    #df['명사 추출'] = df['분석된 내용'].apply(morphs_analysis)
    
    # TF-IDF 벡터화
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df['분석된 내용'])

    df_tfidf = display_transform_dtm(vectorizer, df['분석된 내용'])
    return df_tfidf, tfidf_matrix, vectorizer



# TF-IDF 시각화 함수 (막대그래프)
def plot_tfidf_matrix(tfidf_matrix, vectorizer, top_n=20):
    # TF-IDF 결과를 DataFrame으로 변환
    #df_graph = pd.DataFrame(tfidf_matrix.toarray(), index=vectorizer.get_feature_names_out())
    
    df_graph = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())
  
    # 전체 단어별 TF-IDF 합계 계산
    tfidf_scores = df_graph.sum(axis=0).sort_values(ascending=False)
    
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
    
    return plt.gcf()
