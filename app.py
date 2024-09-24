import mysql.connector
import streamlit as st
import io
import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import koreanize_matplotlib
#from IPython.display import display
from konlpy.tag import Okt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
from gensim.corpora.dictionary import Dictionary
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text
import platform
from word_cloud_utils import display_word_cloud  # 워드 클라우드 함수를 가져옴

#사이드바
st.set_page_config(
    page_title="T-Note",    # 타이틀바 명
    page_icon="📋",         # 타이틀바 아이콘
    layout="wide",          # 화면 꽉차게 확장해주는...
    initial_sidebar_state="auto"
)

font_path = r'/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf'

# Streamlit 앱 제목
st.title("T-Note : tsis AI 회의록작성111123455")

# Pandas display 옵션 설정
pd.set_option('display.max_columns', None)  # 모든 열 표시
pd.set_option('display.max_rows', None)     # 모든 행 표시
pd.set_option('display.width', 0)           # 터미널 너비에 맞춰 자동 조정
pd.set_option('display.max_colwidth', None) # 열 내용이 잘리지 않도록 설정

# MySQL 데이터베이스 연결 함수
def connect_to_db():
    return mysql.connector.connect(
        host='localhost',
        user='tnote',
        password='q1w2e3r4',
        database='db_tnote'
    )

# 파일 저장 함수
def save_file(uploaded_file, directory):
    file_name = uploaded_file.name
    file_size = uploaded_file.size
    save_path = os.path.join(directory, file_name)

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_name, file_size, save_path

# 데이터베이스에 파일 정보 삽입 함수
def insert_file_info_to_db(connection, file_name, file_size, save_path):
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO tn_rec_file (f_name, f_size, f_path) VALUES (%s, %s, %s)",
        (file_name, file_size, save_path)
    )
    connection.commit()

# 데이터베이스에서 파일 정보 조회 함수
def fetch_file_info_from_db(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT f_name, f_size, f_path, dt_insert FROM tn_rec_file")
    records = cursor.fetchall()
    return records


tabs = st.tabs(["회의녹취록 업로드", "회의녹취록  조회", "📄 회의 녹취록 전문", "🙋 화자별 녹취록 전문"])

# 첫번째 탭: 업로드
with tabs[0]:
    st.header("회의녹취록 업로드")
    uploaded_file = st.file_uploader("녹음된 회의파일을 올려주세요", type=["mp3", "wav", "ogg", "flac", "m4a"])

    # 저장할 경로 설정
    save_directory = "/home/tnote/backup_file/rec/"
    os.makedirs(save_directory, exist_ok=True)

    if uploaded_file is not None:
        # 파일 저장 및 정보 출력
        file_name, file_size, save_path = save_file(uploaded_file, save_directory)
        st.write(f"업로드된 파일명: {file_name}")
        st.write(f"파일 크기: {file_size / (1024 * 1024):.2f} MB")

        # "파일 저장" 버튼을 화면에 표시
        if st.button("파일 업로드"):
            st.success(f"파일 {file_name}이 '{save_path}'에 저장되었습니다. [{file_size / (1024 * 1024):.2f} MB]")

            # 데이터베이스에 정보 삽입
            connection = connect_to_db()
            insert_file_info_to_db(connection, file_name, file_size, save_path)
            st.write("데이터베이스에 데이터가 저장되었습니다.")
            connection.close()


# 두번째 탭: 조회
with tabs[1]:
    st.header("회의녹취록 조회")
    if st.button("조회"):
        connection = connect_to_db()
        records = fetch_file_info_from_db(connection)
        connection.close()

        # 조회된 데이터를 데이터프레임으로 변환하여 출력
        df = pd.DataFrame(records, columns=["파일명", "파일 크기(byte)", "파일 경로","업로드 일시"])
        st.write("업로드된 회의 녹취록 리스트:")
        st.dataframe(df)



with tabs[2]:
    st.header("회의록 STT 결과")
    st.write("""
<br>화자0) 우리가 인제 티맵을 같이 하게 됐는데, 주제를 이제 좀 정해야 될 것 같거든요.
<br>화자0) 주제를 어떤 거를 했으면 좋겠는지 좀 생각해 놓은 게 있으면 조금 얘기를 해주세요.
<br>화자1) 저는 클라우드가 좋은 것 같습니다.
<br>화자1) 요새는 클라우드에서 뭐든 데이터 처리하고 하는 게 많으니까 클라우드 주제가 좋은 것 같습니다. 클.
<br>화자0) 삼명 씨는 혹시 생각해 놓 법은 있어요.
<br>화자2) 요즘 또 트렌드가 빅데이터 쪽이 트렌드도 많고 저희 이제 자격증 같은 것들이 빅데이터 쪽 관련된 자격증이 많이 나오고 있거든요.
<br>화자2) 그래서 저희 그럼 자격증 취득하면서 그 연구 목적으로 빅데이터 쪽 하면은 괜찮을 것 같습니다.
<br>화자0) 빅데이터도 요새 많이 하니까 좋은 것 같긴 하네요.
<br>화자0) 근데 인제 제 생각은 우리가 아직 주니어 레벨이니까 그냥 언어 그러니까 씨라던지 자바라든지 이런 언어도 좀 공부해 보는 것도 나쁘지 않을 것 같아요.
<br>화자3) 저는 좀 AI가 해보고 싶은데요. 요즘 AI가 대세잖아요, 체치 비티라든지 AI 해보면 좀 재미있을 것 같습니다.
<br>화자0) 확실히 그 AI 관련해서 막 기사도 많이 올라오고 그런 것 같아요. AI 나쁘지 않은 것 같은데.
<br>화자1) AI 좋은 것 같습니다.
<br>화자0) 그쵸 AI 어때요? 편수도 AI. 어떻게 보나요?
<br>화자2) AI를 한다. 그러면은 지금 아까 얘기한 것처럼 채 DDPT도 있고 좀 분야가 많은 것 같은데.
<br>화자2) AI에서 어떤 분야가 좀 더 해야 될지 이것조 이거를 좀 정해야 될 것 같습니다.
<br>화자0) 그러면 아무래도 이게 우리가 회사에서 하는 거니까 업무에 좀 적용하기 좋은 주제를 잡꾸 하는 게 맞을 것 같은데요.
<br>화자0) 우리 팀에서 사용하기 좋은 업무 주제가 있을까요? AI를 만약에 한다고 하면.
<br>화자2) 제가 프로젝트 학교 다닐 때 썼던 게 이제 AI 쪽 체포 옷을 한번 쓴 적이 있었거든요. 그래서 근데 그거는?
<br>화자2) 이제 AI라기보다는 저희가 케이스 바이 케이스를 많이 만들어가지고.
<br>화자2) 이제 사용자가 입력한 그 핵심 단어만 딱 잡아가지고. 그거에 관련된 거를 보여주는 체포을 했던 적이 있거든요.
<br>화자2) 챗봇도 하면은 나쁘지 않을 것 같은데.
<br>화자2) 챗봇을 이제 채 지금 저희 사용자들이 뭐 물어봤을 때 이거를 답변을 해주는 거를 하는 것도 나쁘지 않을 것 같습니다.
<br>화자0) 그.
<br>화자0) 세포.
<br>화자1) 핫 꽃은 그럼 우리 팀에서만 쓸 수 있는 걸 말하는 건가?
<br>화자2) 그 연구 목적이면은 크게 문제없지 않을까 싶은데.
<br>화자2) 예, 이건 단순하게 의견이라서 그냥 이런 것도 해봤다라고.
<br>화자0) 얘기드린 거예요. 근데 또 얘기를 들어보니까 그러면은 좀 뭔가.
<br>화자0) 챗봇이라고 하면은 딱 다양한 업무에 좀 적용하기에는 좀 주제가 좀 어려울 수도 있다고 좀 생각이 들어가지고 이런 거 어때요?
<br>화자0) 그냥 이렇게 뭔가 실무에서 꼭 쓰지 않더라도 다양한 업무에서 그냥 모두가 쓸 수 있는 거를 한번 생각해보는 건 어떨지.
<br>화자1) 좋죠.
<br>화자0) 지금 우리 미디어 팀 말고도 다른 팀에서도 이제 다양하게 쓸 수 있는 주제를 한번 좀 생각해보는 것도 좋을 것 같아요.
<br>화자3) 회의는 다 하는데 회의 관련된 건 어떨까요?
<br>화자1) 오 괜찮다.
<br>화자2) 회의록 작성할 때 참고하는 괜찮네요.
<br>화자0) 그러네요. 회의할 때 이제 저희가 회의록은 쓰니까 회의는 누구나 하기도 하고.
<br>화자0) 괜찮네요.
<br>화자1) 그럼 회의를 요약해 주는 회의 요약 AI를 만들어 볼까요?
<br>화자0) 저는 나쁘지 않은 것 같아요. 그 주제 그.
<br>화자3) 네, 좋은 것 같아요. 회의로 요약.
""",unsafe_allow_html=True)

    
    df_tnote = pd.DataFrame(np.array([
    ['화자1', '우리가 이제 티앱을 같이 하게 됐는데 주제를 이제 좀 정해야 될 것 같거든요. 주제를 어떤 거를 했으면 좋겠는지 좀 한번 생각해 놓은 게 있으면 조금 얘기를 해 주세요. 찬명 씨는 혹시 생각해 놓은 거 있어>요? 빅데이터도 요새 많이 하니까 좋은 것 같긴 하네요.  근데 이제 제 생각은 우리가 아직 주니어 레벨이니까그냥 언어 그러니까 시라든지 자바라든지 이런 언어도 좀 공부해 보는 것도 나쁘지 않을 것 같아요. 확실히 AI 관>련해서 기사도 많이 올라오고 그런 것 같아요.  AI 나쁘지 않은 것 같은데. 그렇죠 AI 어때요? 찬민 씨도 AI 어떻게 생각하세요?그러면 아무래도 이게 우리가 회사에서 하는 거니까 업무에 좀 적용하기 좋은 주제를 자꾸 하는 게 맞을 것 같은데요. 우리 팀에서 사용하기 좋은 업무 주제가 뭐 있을까요? AI를 만약에 한다고 하면근데 또 얘기를 들어보니까 그러면은 좀 뭔가 챗봇이라고 하면은 일단 다양한 업무에 좀 적용하기에는 좀 주제가좀 어려울 수도 있다고 좀 생각이 들어가지고 이런 거 어때요? 그냥 이렇게 뭔가 실무에서 꼭 쓰지 않더라도 다양한 업무에서 그냥 모두가 쓸 수 있는 거를 한번 생각해 보는 건 어떨지. 지금 우리 미디어 팀 말고도 다른 팀에서도 이제 다양하게 쓸 수 있는 주제를 한번 좀 생각해 보는 것도 좋을 것 같아요. 그러네요.  회의할 때 이제 저희가 회의록은 쓰니까 회의는 누구나 하기도 하고 괜찮네요. 저는 나쁘지 않은 것 같아요  그 주제.']
    ,
    ['화자2', '저는 클라우드가 좋은 것 같습니다.  요새는 클라우드에서 모든 데이터 처리하고 하는 게 많으니까클라우드 주제가 좋은 것 같습니다. 네 좋은 것 같습니다. 챗봇은 그럼 우리 팀에서만 쓸 수 있는 걸 말하는 >건가? 괜찮다. 어 그럼 회의를 요약해 주는 회의 요약 AI를 만들어 볼까요?']
    ,
    ['화자3', '요즘 또 트렌드가 빅데이터 쪽이 트렌드도 많고 저희 이제 자격증 같은 것도 이제 빅데이터 쪽 관련된 자격증이 많이 나오고 있거든요.  그래서 저희 그런 자격증 취득하면서 연구 목적으로 빅데이터 쪽 하면은 괜찮을 것 같습니다. AI를 한다 그러면 지금 아까 얘기한 것처럼 DPT도 있고 좀 분야가 많은 것 같은데 AI에서 어떤 분야가 좀 더해야 될지. 이거 조금 이거를 좀 정해야 될 것 같습니다. 제가 프로젝트 학교 다닐 때 썼던 게 이제 AI 쪽 챗봇을 한번 쓴 적이 있었거든요.  그래서 근데 그거는 이제 AI라기보다는저희가 케이스 바이 케이스를 많이 만들어가지고 이제 사용자가 입력한 그 핵심 단어만 딱 잡아가지고 그거에 관련된 거를 보여주는 챗봇>을 했던 적이 있거든요.  챗봇도 하면은 나쁘지 않을 것 같은데챗봇을 이제 지금 저희 사용자들이 물어봤을 때 이거를 답변을 해 주는 거를 하는 것도 나쁘지 않을 것 같습니다. 어쨌든 연구 목적이면은 크게 문제없지 않을까 싶은데 이건 단순하게 의견이라서 그냥 이런 것도 해봤다라고 얘기드린 거예요. 회의록 작성할 때 참고하면 괜찮은데.']
     ,
    ['화자4', '저는 좀 AI가 해보고 싶은데요.  요즘 AI가 대세잖아요.  챗gpt라든지AI 해 보면 좀 재미있을 것 같습니다. 회의 회의는 다 하는데 회의 관련된 건 어떨까요? 네 좋은 것 같아요.  회의록 요약.']
    ]))

    df_tnote.columns =  ["name", "text"]

#st.write(df_tnote)



with tabs[3]:
    st.header("화자별 STT결과")
    st.dataframe(df_tnote, use_container_width=True)
    #st.write(df_tnote)


okt = Okt()


test_stopwords = ['하지만', '그리고', '그런데', '저는','제가',
             '그럼', '이런', '저런', '합니다',
             '많은', '많이', '정말', '너무', '수', '등', '것',
             '같습니다' , '좀' , '같아요' , '가' , '거', '이제']


def okt_clean(text):
    clean_text = []
    okt_pos = okt.pos(text, stem=True)
    for txt, pos in okt_pos:
        if pos not in ['Josa', 'Eomi', 'Punctuation', 'Adjective', 'Verb', 'Adverb'] and txt not in test_stopwords:
            clean_text.append(txt)
    return " ".join(clean_text)

for row in range(0, len(df_tnote)):
    df_tnote.iloc[row, 1] = okt_clean(df_tnote.iloc[row, 1])

#st.write(df_tnote)

result = ""
for idx in df_tnote.index:
    value = df_tnote.loc[idx,"text"]
    result += " " + value

#display_word_cloud(result)

#tab4.subheader("워트클라우드")
#tab4.write(display_word_cloud(result))
                               
