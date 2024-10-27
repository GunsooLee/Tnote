import numpy as np
from transformers import BartForConditionalGeneration, PreTrainedTokenizerFast

# KoBART 모델과 토크나이저 로드
tokenizer = PreTrainedTokenizerFast.from_pretrained('./kobart-finetuned')
model = BartForConditionalGeneration.from_pretrained('./kobart-finetuned')

# 전체 요약 함수
def summarize_overall(df_origin):
    # 데이터프레임을 5등분
    split_dfs = np.array_split(df_origin, 3)
    
    summaries = []
    for split_df in split_dfs:
        
        text = split_df.apply(lambda row: f"{row['화자']}] \"{row['내용']}.\"", axis=1).str.cat(sep='\n')

        # 요약 생성
        inputs = tokenizer([text], max_length=1024, return_tensors='pt', truncation=True)
        summary_ids = model.generate(
            inputs['input_ids'], 
            num_beams=4, 
            max_length=256, 
            min_length=100, 
            early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        summaries.append(summary)
    
    # 분할된 요약들을 하나로 합치기
    overall_summary = '\n'.join(summaries)
    return overall_summary
