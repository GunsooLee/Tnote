from transformers import BartForConditionalGeneration, PreTrainedTokenizerFast
from konlpy.tag import Okt

# KoBART 모델과 토크나이저 로드
tokenizer = PreTrainedTokenizerFast.from_pretrained('./kobart-finetuned')
model = BartForConditionalGeneration.from_pretrained('./kobart-finetuned')

# 한 줄 요약 (명사형으로 끝나게 처리)
def summarize_title(text, max_length=100):
    inputs = tokenizer([text], max_length=1024, return_tensors='pt', truncation=True)
    summary_ids = model.generate(
        inputs['input_ids'],
        num_beams=4,
        max_length=max_length,  # 최대 길이 (제목 길이)
        min_length=16,           # 최소 길이
        early_stopping=True
    )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary
