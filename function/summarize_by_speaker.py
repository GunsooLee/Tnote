from transformers import BartForConditionalGeneration, PreTrainedTokenizerFast

# KoBART 모델과 토크나이저 로드
tokenizer = PreTrainedTokenizerFast.from_pretrained('./kobart-finetuned')
model = BartForConditionalGeneration.from_pretrained('./kobart-finetuned')

# 화자별 요약 함수
def summarize_by_speaker(df):
    speaker_groups = df.groupby('화자')['내용'].apply(' '.join)  # 화자별로 내용 결합
    speaker_summaries = {}

    for speaker, combined_text in speaker_groups.items():
        inputs = tokenizer([combined_text], max_length=1024, return_tensors='pt', truncation=True)
        summary_ids = model.generate(inputs['input_ids'], num_beams=4, max_length=256, no_repeat_ngram_size=3, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        speaker_summaries[speaker] = summary

    return speaker_summaries
