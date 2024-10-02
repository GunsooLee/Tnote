from konlpy.tag import Okt
import streamlit as st

okt = Okt()
# 형태소 분석기(Okt) 불러오기
# ['Josa', 'Eomi', 'Punctuation'] 조사, 어미, 구두점 제거
# test_stopwords 불용어 제거

test_stopwords = ['하지만', '그리고', '그런데', '저는','제가',
             '그럼', '이런', '저런', '합니다',
             '많은', '많이', '정말', '너무', '수', '등', '것',
             '같습니다' , '좀' , '같아요' , '가' , '거', '이제', 
             '를', '하다', '되다', '가다', '않다', '싶다', '대다',
             '주다', '라든지', '해보다', '보다', '저희', '요즘',
             '그냥', '요새']


def okt_clean(text):
    clean_text = []
    okt_pos = okt.pos(text, stem=True)
    for txt, pos in okt_pos:
        if pos not in ['Josa', 'Eomi', 'Punctuation', 'Adjective'] and txt not in test_stopwords:
            clean_text.append(txt)
    return " ".join(clean_text)
