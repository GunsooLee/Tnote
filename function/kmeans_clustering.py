import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import streamlit as st

# KMeans 군집화 함수
def kmeans_clustering(tfidf_matrix, num_clusters=3):
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(tfidf_matrix)
    return kmeans

# KMeans 결과 시각화 함수
def plot_kmeans_clusters(kmeans, tfidf_matrix):
    pca = PCA(n_components=2)
    reduced_data = pca.fit_transform(tfidf_matrix.toarray())
    clusters = kmeans.predict(tfidf_matrix)
    
    plt.figure(figsize=(10, 7))
    sns.scatterplot(x=reduced_data[:, 0], y=reduced_data[:, 1], hue=clusters, palette="Set1", s=100)
    plt.title("KMeans Clustering of Documents")
    
    # st.pyplot(plt.gcf())  # Streamlit에서 차트를 출력
    return plt.gcf()
