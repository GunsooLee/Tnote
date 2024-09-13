import pandas as pd
from transformers import pipeline

# 요약 파이프라인 불러오기
# KoGPT2 tokenizer, model 불러오기
from transformers import PreTrainedTokenizerFast
from transformers import GPT2LMHeadModel

model_ckpt = "skt/kogpt2-base-v2"
tokenizer = PreTrainedTokenizerFast.from_pretrained(
    model_ckpt,
    bos_token='<s>',
    eos_token='</s>',
    unk_token='<unk>',
    pad_token='<pad>',
    mask_token='<mask>')


model = GPT2LMHeadModel.from_pretrained(model_ckpt)
model