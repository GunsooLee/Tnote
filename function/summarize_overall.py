from transformers import BartForConditionalGeneration, PreTrainedTokenizerFast

# KoBART 모델과 토크나이저 로드
tokenizer = PreTrainedTokenizerFast.from_pretrained('./kobart-finetuned')
model = BartForConditionalGeneration.from_pretrained('./kobart-finetuned')

# 전체 요약 함수
def summarize_overall(text):
    inputs = tokenizer([text], max_length=1024, return_tensors='pt', truncation=True)
    summary_ids = model.generate(inputs['input_ids'], num_beams=4, max_length=256, min_length=20, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary
