import pandas as pd

def summarize_meeting(df):
    import pandas as pd
    from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration

    # 대체 KoBART 요약 모델과 토크나이저 로드
    tokenizer = PreTrainedTokenizerFast.from_pretrained('ainize/kobart-news')
    model = BartForConditionalGeneration.from_pretrained('ainize/kobart-news')

    # 텍스트 전처리 함수 (특수 문자 제거)
    def clean_text(text):
        return re.sub(r'[^가-힣a-zA-Z0-9\s.,!?]', '', text)

    # 전체 텍스트 합치기 및 전처리
    full_text = ' '.join(df['text'].apply(clean_text).tolist())

    # 전체 요약 생성
    inputs = tokenizer.encode(full_text, max_length=1024, truncation=True, return_tensors='pt')
    summary_ids = model.generate(inputs, num_beams=4, max_length=150, early_stopping=True)
    overall_summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    # 화자별 요약 생성
    speaker_summaries = {}
    for speaker in df['speaker'].unique():
        speaker_text = ' '.join(df[df['speaker'] == speaker]['text'].apply(clean_text).tolist())
        inputs = tokenizer.encode(speaker_text, max_length=1024, truncation=True, return_tensors='pt')
        summary_ids = model.generate(inputs, num_beams=4, max_length=150, early_stopping=True)
        speaker_summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        speaker_summaries[speaker] = speaker_summary

    return overall_summary, speaker_summaries



# 예시 데이터프레임 생성
data = {
    'speaker': ['A', 'B', 'A', 'C'],
    'text': [
        '안녕하세요, 오늘 회의 agenda를 말씀드리겠습니다.',
        '네, 감사합니다. 먼저 지난 회의 내용을 리뷰하죠.',
        '좋습니다. 지난 회의에서 결정된 사항은 다음과 같습니다.',
        '추가로 논의할 사항이 있습니다.'
    ]
}
df = pd.DataFrame(data)

# 함수 호출
overall_summary, speaker_summaries = summarize_meeting(df)

print("전체 요약:")
print(overall_summary)
print("\n화자별 요약:")
for speaker, summary in speaker_summaries.items():
    print(f"{speaker}: {summary}")

