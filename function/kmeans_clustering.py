import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import pandas as pd
from adjustText import adjust_text

# KMeans 군집화 함수
def kmeans_clustering(df_tfidf, num_clusters=5):
    df_tfidf_trans = df_tfidf.transpose()

    kmeans = KMeans(n_clusters=num_clusters, n_init="auto", random_state=42)
    kmeans.fit(df_tfidf_trans).predict(df_tfidf_trans)

    df_kmeans = pd.DataFrame()
    df_kmeans["corpus"] = df_tfidf_trans.index
    df_kmeans["label"] = kmeans.labels_

    return df_tfidf_trans, df_kmeans

# KMeans 결과 시각화 함수
def plot_kmeans_clusters(df_tfidf_trans, df_kmeans):

    tsne = TSNE(n_components=2, perplexity=10, random_state=42)
    tsne_result = tsne.fit_transform(df_tfidf_trans)
    
    df_tsne = pd.DataFrame(tsne_result, columns=["x", "y"])
    df_tsne["corpus"] = df_kmeans["corpus"]
    df_tsne["label"] = df_kmeans["label"]

    # 기존 코드
    plt.figure(figsize=(15, 8))
    sns.scatterplot(data=df_tsne, x="x", y="y", hue="label", palette="Set1")

    # 텍스트 추가 및 위치 조정
    texts = []
    for i in df_tsne.index:
        texts.append(plt.text(x=df_tsne.loc[i, "x"], y=df_tsne.loc[i, "y"], s=df_tsne.loc[i, "corpus"]))

    # adjust_text로 텍스트 위치 조정
    adjust_text(texts, arrowprops=dict(arrowstyle='->', color='red'))


    plt.title("KMeans Clustering of Documents")
    
    # st.pyplot(plt.gcf())  # Streamlit에서 차트를 출력
    return plt.gcf()
