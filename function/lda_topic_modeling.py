import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import LatentDirichletAllocation
import streamlit as st

# LDA 토픽 모델링 함수
def lda_topic_modeling(tfidf_matrix, num_topics=3):
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    lda.fit(tfidf_matrix)
    return lda

# LDA 결과 시각화 함수
def plot_lda_topics(lda, vectorizer, n_top_words=10):
    words = vectorizer.get_feature_names_out()
    fig, axes = plt.subplots(1, lda.n_components, figsize=(15, 8), sharex=True)
    axes = axes.flatten()
    
    for topic_idx, topic in enumerate(lda.components_):
        top_features_idx = topic.argsort()[-n_top_words:]
        top_features = words[top_features_idx]
        weights = topic[top_features_idx]
        ax = axes[topic_idx]
        ax.barh(top_features, weights, height=0.7)
        ax.set_title(f'Topic {topic_idx + 1}', fontdict={'fontsize': 20})
        ax.invert_yaxis()
        ax.tick_params(axis='both', which='major', labelsize=12)
    plt.tight_layout()
    st.pyplot(plt.gcf())  # Streamlit에서 차트를 출력
