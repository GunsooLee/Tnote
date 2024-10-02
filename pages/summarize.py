import streamlit as st

from transformers import BartForConditionalGeneration, PreTrainedTokenizerFast

# KoBART 모델과 토크나이저 불러오기
model = BartForConditionalGeneration.from_pretrained('./kobart-finetuned')
tokenizer = PreTrainedTokenizerFast.from_pretrained('./kobart-finetuned')

# 대화 데이터를 화자별로 분리
def split_speakers(conversation_text):
    speakers = {}
    lines = conversation_text.split("\n")

    for line in lines:
        if ']' in line:
            speaker, text = line.split(']', 1)
            speaker = speaker.strip()
            text = text.strip()

            if speaker not in speakers:
                speakers[speaker] = []

            speakers[speaker].append(text)
    
    return speakers

# 텍스트 요약 함수
def generate_summary(text):
    inputs = tokenizer([text], max_length=1024, return_tensors='pt', truncation=True)
    summary_ids = model.generate(inputs['input_ids'], num_beams=4, max_length=128, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# 화자별로 대화를 요약
def summarize_by_speaker(speakers):
    speaker_summaries = {}
    for speaker, texts in speakers.items():
        combined_text = ' '.join(texts)
        summary = generate_summary(combined_text)
        speaker_summaries[speaker] = summary
    return speaker_summaries

# 예시 대화
conversation_text = """
화자0] 우리가 인제 티맵을 같이 하게 됐는데, 주제를 이제 좀 정해야 될 것 같거든요.
화자0] 주제를 어떤 거를 했으면 좋겠는지 좀 생각해 놓은 게 있으면 조금 얘기를 해주세요.
화자1] 저는 클라우드가 좋은 것 같습니다.
화자1] 요새는 클라우드에서 뭐든 데이터 처리하고 하는 게 많으니까 클라우드 주제가 좋은 것 같습니다.
화자0] 삼명 씨는 혹시 생각해 놓은 게 있나요?
화자2] 요즘 또 트렌드가 빅데이터 쪽이 트렌드도 많고 저희 이제 자격증 같은 것들이 빅데이터 쪽 관련된 자격증이 많이 나오고 있거든요.
화자2] 그래서 저희 그럼 자격증 취득하면서 그 연구 목적으로 빅데이터 쪽 하면은 괜찮을 것 같습니다.
화자0] 빅데이터도 요새 많이 하니까 좋은 것 같긴 하네요.
"""

# 화자별 요약
speakers = split_speakers(conversation_text)
speaker_summaries = summarize_by_speaker(speakers)

# 출력
st.write("화자별 요약:")
for speaker, summary in speaker_summaries.items():
    st.write(f"{speaker}: {summary}")
