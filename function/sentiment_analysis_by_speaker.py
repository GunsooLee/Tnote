from transformers import pipeline
import pandas as pd
import matplotlib.pyplot as plt

# 감정 분석 모델 로드
sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment", max_length=512, truncation=True)

# 긍정 비율에 따른 감정 범주 분류 함수
def get_emotion_category(positive_ratio):
    if positive_ratio >= 80:
        return "매우긍정"
    elif positive_ratio >= 60:
        return "긍정"
    elif positive_ratio >= 40:
        return "중립"
    elif positive_ratio >= 20:
        return "부정"
    else:
        return "매우부정"

# 화자별 감정 분석 함수 (상세 정보 및 그래프 포함)
def analyze_emotion_by_speaker(df):
    speaker_groups = df.groupby('화자')['분석된 내용'].apply(list)  # 화자별로 내용을 리스트로 결합
    speaker_emotions = {}
    emotion_distributions = {}  # 각 화자의 감정 분포 저장
    
    for speaker, texts in speaker_groups.items():
        emotion_counts = {'매우 긍정': 0, '긍정': 0, '중립': 0, '부정': 0, '매우 부정': 0}
        all_emotions = []  # 화자의 모든 감정 레이블 저장

        for text in texts:
            emotions = sentiment_pipeline(text)[0]  # 개별 문장 감정 분석
            all_emotions.append(emotions)
            
            # 감정 레이블에 따라 카운트 증가
            if '1 star' in emotions['label']:
                emotion_counts['매우 부정'] += 1
            elif '2 star' in emotions['label']:
                emotion_counts['부정'] += 1
            elif '3 star' in emotions['label']:
                emotion_counts['중립'] += 1
            elif '4 star' in emotions['label']:
                emotion_counts['긍정'] += 1
            elif '5 star' in emotions['label']:
                emotion_counts['매우 긍정'] += 1
        
        # 총 분석된 텍스트 수 계산
        total_texts = len(texts)
        
        positive_ratio = (((emotion_counts['매우 긍정'] * 5) + (emotion_counts['긍정'] * 4) + (emotion_counts['중립'] * 3) + (emotion_counts['부정'] * 2) + (emotion_counts['매우 부정'] * 1)) / (total_texts*5)) * 100

        # 비율 계산
        emotion_distribution = {
            '긍정 비율': positive_ratio
        }

        # 긍정 비율을 감정 범주로 변환
        emotion_category = get_emotion_category(positive_ratio)
        
        # 화자별 감정 분석 결과 저장
        speaker_emotions[speaker] = {
            '총 텍스트 수': total_texts,
            '감정 분포': emotion_distribution,
            '상세 분석': emotion_counts,
            '감정 결과': emotion_category
        }

        emotion_distributions[speaker] = emotion_distribution['긍정 비율']
        
    return speaker_emotions, emotion_distributions

# 감정 분포 그래프 함수
def plot_emotion_distribution( emotion_distribution):
    speakers  = list(emotion_distribution.keys())
    values = list(emotion_distribution.values())
    
    plt.figure(figsize=(8, 3))
    bars = plt.barh(speakers, values, color='#FFD700', height=0.3)
    plt.xlim(0, 100)  # 비율이므로 100%까지 설정
    plt.xlabel('긍정 단어 비율 (%)')
    plt.title('화자별 긍정 단어 비율')

    # 막대 끝에 긍정 비율 값 표시
    for bar, value in zip(bars, values):
        plt.text(value + 1, bar.get_y() + bar.get_height()/2, f'{value:.2f}%', va='center')
        
    return plt
