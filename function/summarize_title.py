from transformers import BartForConditionalGeneration, PreTrainedTokenizerFast
from konlpy.tag import Okt

# KoBART 모델과 토크나이저 로드
tokenizer = PreTrainedTokenizerFast.from_pretrained('./kobart-finetuned')
model = BartForConditionalGeneration.from_pretrained('./kobart-finetuned')

# 한 줄 요약 (명사형으로 끝나게 처리)
def summarize_title(text, max_length=15):
    # 1. KoBART 모델을 사용하여 기본적인 요약 수행
    inputs = tokenizer([text], max_length=1024, return_tensors='pt', truncation=True)
    summary_ids = model.generate(
        inputs['input_ids'],
        num_beams=4,
        max_length=max_length,  # 최대 길이 (제목 길이)
        min_length=5,           # 최소 길이
        early_stopping=True
    )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    # 2. Okt 형태소 분석기를 사용하여 명사 추출
    okt = Okt()
    nouns = okt.nouns(summary)

    # 3. 명사로 끝나는 제목 생성 (명사가 있으면 마지막 명사 사용)
    if nouns:
        return ' '.join(nouns)  # 명사로만 구성된 문장 반환
    else:
        return summary  # 명사가 없을 경우 원래 요약 반환
