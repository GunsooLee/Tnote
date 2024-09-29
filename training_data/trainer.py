import os
import json
import pandas as pd
from transformers import BartForConditionalGeneration, PreTrainedTokenizerFast, Trainer, TrainingArguments
from datasets import Dataset

# KoBART 모델과 토크나이저 불러오기
model = BartForConditionalGeneration.from_pretrained('gogamza/kobart-summarization')
tokenizer = PreTrainedTokenizerFast.from_pretrained('gogamza/kobart-summarization')

# JSON 데이터가 들어 있는 폴더 경로
data_dir = './training_data/data'

# JSON 파일에서 텍스트와 요약문 추출 함수
def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
        # 'passage'와 'summary1' 필드 추출
        text = data['Meta(Refine)']['passage']
        summary = data['Annotation']['summary1']
        
        # summary1이 없으면 summary2 사용 (예시를 따라 추가 처리)
        if not summary:
            summary = data['Annotation']['summary2']
        
        return {'text': text, 'summary': summary}

# 모든 파일 불러오기
def load_all_data(data_dir):
    dataset = []
    
    for file_name in os.listdir(data_dir):
        file_path = os.path.join(data_dir, file_name)
        
        # 파일 확장자가 .json인 파일만 처리
        if file_name.endswith('.json'):
            data = load_json_data(file_path)
            if data['summary']:  # 요약이 있는 데이터만 사용
                dataset.append(data)
    
    if not dataset:
        print("데이터셋이 비어 있습니다.")
        print(file_name)
    else:
        print(f"{len(dataset)}개의 데이터를 로드했습니다.")
    
    return dataset

# 데이터 로드
data = load_all_data(data_dir)

# 데이터셋을 Hugging Face Dataset으로 변환
if data:
    dataset = Dataset.from_pandas(pd.DataFrame(data))
else:
    raise ValueError("데이터를 불러오는 데 실패했습니다. 데이터를 확인하세요.")


# 데이터셋 확인
if len(dataset) == 0:
    print("데이터셋이 비어 있습니다. 데이터를 확인하세요.")
else:
    print("데이터셋이 제대로 로드되었습니다.")
    print(dataset[0])

# 데이터 전처리 함수 정의
def preprocess_data(examples):
    # 입력 텍스트를 토큰화하고 최대 길이 1024로 제한
    inputs = tokenizer(examples['text'], max_length=1024, truncation=True, padding='max_length')

    # 타겟 요약문도 토큰화하고 최대 길이 128로 제한
    targets = tokenizer(examples['summary'], max_length=128, truncation=True, padding='max_length')
    
    # 입력의 input_ids와 요약문의 input_ids를 합침
    inputs['labels'] = targets['input_ids']
    
    return inputs

# 데이터 전처리 적용
dataset = dataset.map(preprocess_data, batched=True)

# 훈련과 검증 데이터셋 나누기
train_test_split = dataset.train_test_split(test_size=0.1)
train_dataset = train_test_split['train']
val_dataset = train_test_split['test']

# 훈련 파라미터 설정
training_args = TrainingArguments(
    output_dir='./results',              # 체크포인트 저장 경로
    evaluation_strategy='epoch',         # 매 에포크마다 평가
    learning_rate=2e-5,                  # 학습률
    per_device_train_batch_size=4,       # 훈련 배치 크기
    per_device_eval_batch_size=4,        # 평가 배치 크기
    num_train_epochs=3,                  # 학습 에포크 수
    weight_decay=0.01,                   # 가중치 감쇠
    logging_dir='./logs',                # 로깅 디렉토리
    logging_steps=10,
    save_total_limit=2,                  # 저장할 체크포인트 개수
)

# Trainer 객체 생성
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

# 모델 훈련 시작
trainer.train()

# 모델과 토크나이저 저장
model.save_pretrained('./kobart-finetuned')
tokenizer.save_pretrained('./kobart-finetuned')

# 요약 함수 정의
def generate_summary(text):
    inputs = tokenizer([text], max_length=1024, return_tensors='pt', truncation=True)
    summary_ids = model.generate(inputs['input_ids'], num_beams=4, max_length=128, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# 예시 텍스트 요약 실행
text = "오늘 날씨가 좋네요. 오후에 산책을 해야겠어요."
summary = generate_summary(text)
print("요약된 텍스트:", summary)
