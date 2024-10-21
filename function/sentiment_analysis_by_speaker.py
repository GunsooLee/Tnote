from transformers import pipeline

# 감정 분석 모델 로드
sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment", max_length=512, truncation=True))

# 화자별 감정 분석 함수
def analyze_emotion_by_speaker(df):
    speaker_groups = df.groupby('화자')['분석된 내용'].apply(' '.join)  # 화자별로 내용 결합
    speaker_emotions = {}
    labels = []
    scores = []

    for speaker, combined_text in speaker_groups.items():
        emotions = sentiment_pipeline(combined_text)[0]  # 감정 분석
        labels.append(f"화자 {speaker}: {emotions['label']}")
        scores.append(emotions['score'])
        #speaker_emotions[speaker] = emotions

    return labels, scores
