import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import LatentDirichletAllocation

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

    # 전체 가중치 합계를 구함
    total_weights = np.sum(lda.components_)
    
    for topic_idx, topic in enumerate(lda.components_):
        # 퍼센트 계산 
        topic_total_weight = np.sum(topic)
        percentage = (topic_total_weight / total_weights) * 100
    
        top_features_idx = topic.argsort()[-n_top_words:]
        top_features = words[top_features_idx]
        weights = topic[top_features_idx]
        ax = axes[topic_idx]
        ax.barh(top_features, weights, height=0.7)
        ax.set_title(f'주제 {topic_idx + 1} ({percentage:.2f}%)', fontdict={'fontsize': 20})
        #ax.invert_yaxis()

        # 테두리 제거
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
                                        
        ax.tick_params(axis='both', which='major', labelsize=12)

    plt.suptitle("LDA model 주제 선정", fontsize=24)

    plt.tight_layout(rect=[0, 0, 1, 0.95])

    
    #st.pyplot(plt.gcf())  # Streamlit에서 차트를 출력
    return plt.gcf()
