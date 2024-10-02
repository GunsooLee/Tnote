from transformers import pipeline

# 감정 분석 모델 로드
emotion_model = pipeline('sentiment-analysis')

# 화자별 감정 분석 함수
def analyze_emotion_by_speaker(df):
    speaker_groups = df.groupby('화자')['분석된 내용'].apply(' '.join)  # 화자별로 내용 결합
    speaker_emotions = {}

    for speaker, combined_text in speaker_groups.items():
        emotions = emotion_model(combined_text)  # 감정 분석
        speaker_emotions[speaker] = emotions

    return speaker_emotions
