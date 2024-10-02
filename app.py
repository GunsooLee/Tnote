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
import uuid
from ClovaSpeechClient import ClovaSpeechClient
from hanspell import spell_checker

# 회의록 파일 다운로드 추가
from resultToDocx import create_meeting_minutes
from datetime import datetime

# 그리드 클릭 이벤트
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

# 프로그레스바
import time

# 회의록 요약 관련 함수
from function.summarize_overall import summarize_overall
from function.summarize_by_speaker import summarize_by_speaker
from function.summarize_title import summarize_title
from function.sentiment_analysis_by_speaker import analyze_emotion_by_speaker
from function.tfidf_vectorization import tfidf_vectorize, plot_tfidf_matrix
from function.lda_topic_modeling import lda_topic_modeling, plot_lda_topics
from function.kmeans_clustering import kmeans_clustering, plot_kmeans_clusters
from function.okt_clean import okt_clean

# 세션 상태 초기화
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def login():
    """로그인 함수"""
    st.title("T-Note : tsis AI (login ver.)")
    username = st.text_input("Login ID : tsis")
    password = st.text_input("Password : 1 ", type="password")

    if st.button("로그인"):
        # 예시로 간단한 인증 로직 (실제 환경에서는 안전한 인증 방법 사용)
        if username == "tsis" and password == "1":
            st.session_state['logged_in'] = True
            st.success("로그인 성공!")
            st.rerun()  # 로그인 성공 시 페이지 새로고침
        else:
            st.error("로그인 실패. 사용자 이름 또는 비밀번호가 잘못되었습니다.")

def main_app():
    #사이드바
    st.set_page_config(
        page_title="T-Note",    # 타이틀바 명
        page_icon="📋",         # 타이틀바 아이콘
        layout="wide",          # 화면 꽉차게 확장해주는...
        initial_sidebar_state="auto"
    )

    # 세션 데이터
    if 'data' not in st.session_state:
        st.session_state.data = {
            'name_topic': '',
            'mt_date': '',
            'num_spk': '',
            'mt_term': '',
        }

    font_path = r'/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf'

    # Streamlit 앱 제목
    st.title("T-Note : tsis AI 회의록작성(로그인버전)")

    with st.sidebar:
        st.write("안녕하세요 tsis 님.")

    # Pandas display 옵션 설정
    pd.set_option('display.max_columns', None)  # 모든 열 표시
    pd.set_option('display.max_rows', None)     # 모든 행 표시
    pd.set_option('display.width', 0)           # 터미널 너비에 맞춰 자동 조정
    pd.set_option('display.max_colwidth', None) # 열 내용이 잘리지 않도록 설정

    # 로딩바 : 단계별 정보를 반환하는 함수
    def progress_steps(step):
        if step == 1:
            return "        1/4 단계: STT 적용중.......", "/home/tnote/app/Tnote/res/image/progressbar_1_stt.png"
        elif step == 2:
            return "        2/4 단계: 자연어처리중.......", "/home/tnote/app/Tnote/res/image/progressbar_2_nlp.png"
        elif step == 3:
            return "        3/4 단계: 주제선정중.......", "/home/tnote/app/Tnote/res/image/progressbar_3_topic.png"
        elif step == 4:
            return "        4/4 단계: 회의요약중.......", "/home/tnote/app/Tnote/res/image/progressbar_4_summary.png"

    # 단계별 프로그레스바와 텍스트, 이미지를 표시하는 함수
    def show_progress_with_image(total_steps):

        progress_bar = st.progress(0)

        # 텍스트와 이미지를 업데이트할 공간 확보
        text_placeholder = st.empty()
        image_placeholder = st.empty()

        for step in range(1, total_steps + 1):

            # 각 단계별 텍스트와 이미지 가져오기
            step_text, image_path = progress_steps(step)

            # 텍스트와 이미지를 업데이트
            text_placeholder.write(f"### {step_text}")  # 텍스트를 업데이트
            image_placeholder.image(image_path, width=200)  # 이미지를 업데이트

            # 프로그레스바 업데이트 (총 단계 중 몇 번째 단계인지 계산하여 반영)
            progress_bar.progress(step / total_steps)

            # 각 단계에서 작업이 진행되는 시간 (예시로 2초)
            time.sleep(2)

    # MySQL 데이터베이스 연결 함수
    def connect_to_db():
        return mysql.connector.connect(
            host='localhost',
            # host='211.188.48.50',
            user='tnote',
            password='q1w2e3r4',
            database='db_tnote'
        )

    # 파일 저장 함수
    def save_file(uploaded_file, directory):

        # UUID 생성
        unique_id = uuid.uuid4()

        st.success("uuid 호출 시도") # 디버깅 로그

        # 새로운 파일명 생성
        new_filename = f"{unique_id}-{uploaded_file.name}"

        #file_name = uploaded_file.name
        file_name = new_filename
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
        #connection.commit()

        cursor.execute("SELECT LAST_INSERT_ID()")
        rec_seq = cursor.fetchone()[0]
        return rec_seq

    # tn_note_mst 테이블에 회의 정보 삽입 함수
    def insert_meeting_info_to_db(connection, rec_seq, name_topic, num_spk, mt_date, mt_term, res_file_seq):
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO tn_note_mst (rec_file_seq, name_topic, num_spk, mt_date, mt_term, res_file_seq) VALUES (%s, %s, %s, %s, %s, %s)",
            (rec_seq, name_topic, num_spk, mt_date.strftime('%Y-%m-%d'), mt_term, res_file_seq)
        )
        #connection.commit()

    # 데이터베이스에 회의록 파일 정보 삽입 함수
    def insert_result_file_info_to_db(connection, file_name, file_size, save_path, document_title, meeting_room, meeting_date, attendees):
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO tn_result_file (file_name, file_size, file_path,document_title, meeting_room, meeting_date, attendees ) VALUES (%s, %s, %s,%s, %s, %s, %s)",
            (file_name, file_size, save_path, document_title, meeting_room, meeting_date, attendees)
        )
        #connection.commit()

        cursor.execute("SELECT LAST_INSERT_ID()")
        res_file_seq = cursor.fetchone()[0]
        return res_file_seq

    # 데이터베이스에서 파일 정보 조회 함수
    def fetch_file_info_from_db(connection):
        cursor = connection.cursor()
        cursor.execute("SELECT f_name, f_size, f_path, dt_insert FROM tn_rec_file")
        records = cursor.fetchall()
        return records

    # 회의록 정보 select
    def result_file_info_from_db(connection):
        cursor = connection.cursor()
        cursor.execute("SELECT document_title, meeting_room, meeting_date, attendees, file_name, file_size, file_path,insert_date  FROM tn_result_file")
        records = cursor.fetchall()
        return records

    tabs = st.tabs(["📄 회의녹취록 업로드", "회의녹취록 조회", "회의록 다운로드"])

    # 첫번째 탭: 업로드
    with tabs[0]:
        st.header("회의녹취록 업로드")
        uploaded_file = st.file_uploader("녹음된 회의파일을 올려주세요", type=["mp3", "wav", "ogg", "flac", "m4a"])

        # 2열 레이아웃 생성
        col1, col2 = st.columns(2)

        with col1:
            name_topic = st.text_input("회의 제목을 입력하세요")
            mt_date = st.date_input("회의날짜를 선택하세요.")
            num_spk_opt = ["2","3","4","5","6","7","8","9","10"]
            num_spk = st.selectbox("회의 참여인원을 선택하세요.", options=num_spk_opt)

        with col2:
            meeting_room = st.text_input("회의실을 입력하세요")
            # 회의 종료 시간을 30분 단위로 선택할 수 있도록 설정
            mt_term_opt = ["30분", "1시간", "1시간30분", "2시간","2시간30분","3시간","3시간30분","4시간","4시간30분","5시간","5시간30분","6시간"]
            mt_term = st.selectbox("회의 진행시간을 선택하세요", options=mt_term_opt)
            speakers_text = st.text_area("참석자 이름을 엔터로 구분하여 입력하세요")
            speakers = speakers_text

        #회의록 저장을 위한 데이터 저장 - 회의록 생성로직 이동으로 주석
        # st.session_state.data['name_topic'] = name_topic
        # st.session_state.data['mt_date'] = mt_date.strftime("%Y-%m-%d")
        # st.session_state.data['num_spk'] = num_spk
        # st.session_state.data['mt_term'] = mt_term

        # 저장할 경로 설정
        save_directory = "/home/tnote/backup_file/rec/"
        os.makedirs(save_directory, exist_ok=True)

        # 마스터 테이블에 저장할때 시퀀스 가져오는거 중복 내용 처리
        rec_seq=''

        if uploaded_file is not None:

            # "파일 저장" 버튼을 화면에 표시
            if st.button("파일 업로드"):

                if not name_topic :
                # 회의제목이 입력되지 않았을 경우 경고 메시지 표시
                    st.warning("회의 제목을 입력해야 합니다.")
                else :

                    show_progress_with_image(4)

                    # 파일 저장 및 정보 출력
                    file_name, file_size, save_path = save_file(uploaded_file, save_directory)
                    st.write(f"업로드 파일명: {file_name}")
                    st.write(f"파일 크기: {file_size / (1024 * 1024):.2f} MB")
                    st.success(f"파일 {file_name}이 '{save_path}'에 저장되었습니다. [{file_size / (1024 * 1024):.2f} MB]")

                    # 데이터베이스에 정보 삽입
                    connection = connect_to_db()
                    rec_seq = insert_file_info_to_db(connection, file_name, file_size, save_path)
                    st.success("데이터베이스에 데이터가 저장시도. :: tn_rec_file") # 디버깅 로그


                    connection.commit()
                    connection.close()

                    st.success("데이터베이스에 commit 완료") # 디버깅 로그

                    #회의록 생성 로직 
                    if 'file_generated' not in st.session_state:  # 파일 생성 여부 확인
                        date = datetime.now().strftime('%Y%m%d_%H%M%S')
                        file_name = f"회의록_{date}"
                        retrun_filesize, return_filepath = create_meeting_minutes(
                            name_topic,
                            meeting_room,  
                            mt_date.strftime("%Y-%m-%d"),
                            '작성자', # 임시로 고정, 실제 내용으로 대체
                            speakers.splitlines(),
                            "회의 주제"   # 임시로 고정, 실제 내용으로 대체
                            "회의 내용",  # 임시로 고정, 실제 내용으로 대체
                            file_name
                        )
                        st.session_state.file_generated = True  # 파일 생성 완료 표시

                    # 회의록 내용 db 저장
                    connection = connect_to_db()
                    res_file_seq = insert_result_file_info_to_db(connection,file_name,retrun_filesize,return_filepath,name_topic,meeting_room,mt_date.strftime("%Y-%m-%d"),speakers)
                    insert_meeting_info_to_db(connection, rec_seq, name_topic, num_spk, mt_date, mt_term, res_file_seq)

                    connection.commit()
                    connection.close()


                    st.success("데이터베이스에 데이터가 저장시도. :: tn_note_mst") # 디버깅 로그
                    # 확장 가능한 컨테이너에 결과 표시
                    with st.expander("회의 녹취록 업로드 결과 보기▼"):
                        st.divider() 
                        st.write(f"◆ 파일명: {file_name}")
                        st.write(f"◆ 파일 크기: {file_size / (1024 * 1024):.2f} MB")
                        st.write(f"◆ 저장 경로: {save_path}")
                        st.divider() 
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"◆ 회의제목: {name_topic}")
                            st.write(f"◆ 회의참여인원: {num_spk}")
                            st.write(f"◆ 회의날짜: {mt_date}")
                            st.write(f"◆ 회의진행시간: {mt_term}")
                            st.write(f"◆ 회의주제: T-LAB 주제정하기")
                            st.write(f"◆ 회의요약: T-LAB 주제를 정해야해서 회의를 함.")
                        with col2:
                            # 이미지
                            #display_word_cloud(result)
                            st.image("https://static.streamlit.io/examples/dice.jpg", caption="Dice Image")

                    # 회의록 다운로드 추가
                    with st.expander("회의록 다운로드 보기▼"):
                        # 파일 다운로드 버튼 생성
                        if 'file_generated' in st.session_state:
                            if os.path.exists(return_filepath):
                                # 파일 다운로드 버튼 생성
                                st.text(return_filepath)
                                try:
                                    with open(return_filepath, 'rb') as file:
                                        st.download_button(
                                            label="회의록 파일 다운로드",
                                            data=file,
                                            file_name=return_filepath.split('\\')[-1],
                                            mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                                        )
                                except FileNotFoundError as e:
                                    print(f"파일을 열 수 없습니다: {e}")
                                except PermissionError as e:
                                    print(f"파일 접근 권한이 없습니다: {e}")
                                except Exception as e:
                                    print(f"알 수 없는 오류 발생: {e}")    

                    # 데이터프레임 입력 예시
                    df_origin = pd.DataFrame(np.array([
                    ['화자0', '우리가 인제 티맵을 같이 하게 됐는데, 주제를 이제 좀 정해야 될 것 같거든요.']
                    ,['화자0', '주제를 어떤 거를 했으면 좋겠는지 좀 생각해 놓은 게 있으면 조금 얘기를 해주세요.']
                    ,['화자1', '저는 클라우드가 좋은 것 같습니다.']
                    ,['화자1', '요새는 클라우드에서 뭐든 데이터 처리하고 하는 게 많으니까 클라우드 주제가 좋은 것 같습니다. 클.']
                    ,['화자0', '삼명 씨는 혹시 생각해 놓 법은 있어요.']
                    ,['화자2', '요즘 또 트렌드가 빅데이터 쪽이 트렌드도 많고 저희 이제 자격증 같은 것들이 빅데이터 쪽 관련된 자격증이 많이 나오고 있거든요.']
                    ,['화자2', '그래서 저희 그럼 자격증 취득하면서 그 연구 목적으로 빅데이터 쪽 하면은 괜찮을 것 같습니다.']
                    ,['화자0', '빅데이터도 요새 많이 하니까 좋은 것 같긴 하네요.']
                    ,['화자0', '근데 인제 제 생각은 우리가 아직 주니어 레벨이니까 그냥 언어 그러니까 씨라던지 자바라든지 이런 언어도 좀 공부해 보는 것도 나쁘지 않을 것 같아요.']
                    ,['화자3', '저는 좀 AI가 해보고 싶은데요. 요즘 AI가 대세잖아요, 체치 비티라든지 AI 해보면 좀 재미있을 것 같습니다.']
                    ,['화자0', '확실히 그 AI 관련해서 막 기사도 많이 올라오고 그런 것 같아요. AI 나쁘지 않은 것 같은데.']
                    ,['화자1', 'AI 좋은 것 같습니다.']
                    ,['화자0', '그쵸 AI 어때요? 편수도 AI. 어떻게 보나요?']
                    ,['화자2', 'AI를 한다. 그러면은 지금 아까 얘기한 것처럼 채 DDPT도 있고 좀 분야가 많은 것 같은데.']
                    ,['화자2', 'AI에서 어떤 분야가 좀 더 해야 될지 이것조 이거를 좀 정해야 될 것 같습니다.']
                    ,['화자0', '그러면 아무래도 이게 우리가 회사에서 하는 거니까 업무에 좀 적용하기 좋은 주제를 잡꾸 하는 게 맞을 것 같은데요.']
                    ,['화자0', '우리 팀에서 사용하기 좋은 업무 주제가 있을까요? AI를 만약에 한다고 하면.']
                    ,['화자2', '제가 프로젝트 학교 다닐 때 썼던 게 이제 AI 쪽 체포 옷을 한번 쓴 적이 있었거든요. 그래서 근데 그거는?']
                    ,['화자2', '이제 AI라기보다는 저희가 케이스 바이 케이스를 많이 만들어가지고.']
                    ,['화자2', '이제 사용자가 입력한 그 핵심 단어만 딱 잡아가지고. 그거에 관련된 거를 보여주는 체포을 했던 적이 있거든요.']
                    ,['화자2', '챗봇도 하면은 나쁘지 않을 것 같은데.']
                    ,['화자2', '챗봇을 이제 채 지금 저희 사용자들이 뭐 물어봤을 때 이거를 답변을 해주는 거를 하는 것도 나쁘지 않을 것 같습니다.']
                    ,['화자0', '그.']
                    ,['화자0', '세포.']
                    ,['화자1', '핫 꽃은 그럼 우리 팀에서만 쓸 수 있는 걸 말하는 건가?']
                    ,['화자2', '그 연구 목적이면은 크게 문제없지 않을까 싶은데.']
                    ,['화자2', '예, 이건 단순하게 의견이라서 그냥 이런 것도 해봤다라고.']
                    ,['화자0', '얘기드린 거예요. 근데 또 얘기를 들어보니까 그러면은 좀 뭔가.']
                    ,['화자0', '챗봇이라고 하면은 딱 다양한 업무에 좀 적용하기에는 좀 주제가 좀 어려울 수도 있다고 좀 생각이 들어가지고 이런 거 어때요?']
                    ,['화자0', '그냥 이렇게 뭔가 실무에서 꼭 쓰지 않더라도 다양한 업무에서 그냥 모두가 쓸 수 있는 거를 한번 생각해보는 건 어떨지.']
                    ,['화자1', '좋죠.']
                    ,['화자0', '지금 우리 미디어 팀 말고도 다른 팀에서도 이제 다양하게 쓸 수 있는 주제를 한번 좀 생각해보는 것도 좋을 것 같아요.']
                    ,['화자3', '회의는 다 하는데 회의 관련된 건 어떨까요?']
                    ,['화자1', '오 괜찮다.']
                    ,['화자2', '회의록 작성할 때 참고하는 괜찮네요.']
                    ,['화자0', '그러네요. 회의할 때 이제 저희가 회의록은 쓰니까 회의는 누구나 하기도 하고.']
                    ,['화자0', '괜찮네요.']
                    ,['화자1', '그럼 회의를 요약해 주는 회의 요약 AI를 만들어 볼까요?']
                    ,['화자0', '저는 나쁘지 않은 것 같아요. 그 주제 그.']
                    ,['화자3', '네, 좋은 것 같아요. 회의로 요약.']
                    ]))

                    df_origin.columns =  ["화자", "원문"]

                    # 맞춤법 교정 함수
                    def correct_spelling(text):
                        try:
                            result = spell_checker.check(text)
                            return result.checked  # 맞춤법이 교정된 텍스트 반환
                        except KeyError as e:
                            # 'result' 키가 없을 경우 원본 텍스트 반환
                            print(f"맞춤법 교정 중 오류 발생: {e}. 원본 텍스트 반환.")
                            return text
                        except Exception as e:
                            # 그 외 다른 오류가 발생한 경우에도 원본 텍스트 반환
                            print(f"맞춤법 교정 중 알 수 없는 오류 발생: {e}. 원본 텍스트 반환.")
                            return text

                    # 맞춤법 교정 적용
                    df_origin['내용'] = df_origin['원문'].apply(correct_spelling)
                                            
                    with st.expander("전체 STT 결과"):
                        st.write(df_origin)
                    with st.expander("한국어 형태소 분석"):
                        df_origin['분석된 내용'] = df_origin['내용'].apply(okt_clean)
                        st.write(df_origin)
                    with st.expander("단어 벡터화"):
                        tfidf_matrix, vectorizer = tfidf_vectorize(df_origin[['화자', '분석된 내용']])
                        plot_tfidf_matrix(tfidf_matrix, vectorizer)
                    with st.expander("토픽 모델링"):
                        lda_model = lda_topic_modeling(tfidf_matrix, num_topics=3)
                        plot_lda_topics(lda_model, vectorizer)
                    with st.expander("군집화"):
                        kmeans_model = kmeans_clustering(tfidf_matrix, num_clusters=3)
                        plot_kmeans_clusters(kmeans_model, tfidf_matrix)
                    with st.expander("전체 회의 제목"):
                        combined_text = df_origin['내용'].str.cat(sep=' ')
                        title = summarize_title(combined_text)
                        st.write(title)
                    with st.expander("전체 회의 요약"):
                        overall_summary = summarize_overall(combined_text)
                        st.write(overall_summary)
                    with st.expander("화자별 요약"):
                        speaker_summaries = summarize_by_speaker(df_origin)
                        for speaker, summary in speaker_summaries.items():
                            st.write(f"{speaker}: {summary}")
                    with st.expander("화자별 감정 분석"):
                        speaker_emotions = analyze_emotion_by_speaker(df_origin)
                        for speaker, emotions in speaker_emotions.items():
                            st.write(f"{speaker}: {emotions}")


    # 두번째 탭: 조회
    with tabs[1]:
        st.header("회의녹취록 조회")

        # session_state에서 grid_data를 초기화
        if 'grid_data' not in st.session_state:
            st.session_state.grid_data = None

        if st.button("조회"):
            connection = connect_to_db()
            records = result_file_info_from_db(connection)
            connection.close()            

            # 조회된 데이터를 데이터프레임으로 변환하여 출력
            df = pd.DataFrame(records, columns=["회의록 제목","회의실","회의날짜","참석자","파일명", "파일 크기(byte)", "파일 경로","업로드 일시"])
            st.session_state.grid_data = df  # session_state에 저장

            #st.dataframe(df)

        # session_state에 저장된 데이터가 있을 경우에만 그리드를 표시
        if st.session_state.grid_data is not None:
            st.write("업로드된 회의 녹취록 리스트:")
            df = st.session_state.grid_data

            # AgGrid로 그리드 표시
            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_selection('single')  # 행을 클릭할 수 있도록 설정
            grid_options = gb.build()

            grid_response = AgGrid(
                df,
                gridOptions=grid_options,
                height=250,
                update_mode=GridUpdateMode.SELECTION_CHANGED,
                fit_columns_on_grid_load=True
            )

            # 사용자가 선택한 행에 대한 정보 처리
            selected_row = grid_response['selected_rows']

            # 선택된 행의 데이터 구조 확인
            st.write("선택된 행의 데이터 구조: ", selected_row)

            # 자료형 확인
            #st.write("선택된 데이터의 자료형: ", type(selected_row))

            # DataFrame으로 반환된 경우, 선택된 행을 DataFrame 형식으로 처리
            if isinstance(selected_row, pd.DataFrame) and not selected_row.empty:
                # 선택된 첫 번째 행 데이터 추출
                selected_row_data = selected_row.iloc[0]  # DataFrame에서 첫 번째 행 가져오기

                # 파일 경로 추출
                file_path = selected_row_data['파일 경로']  # '파일 경로' 컬럼에서 값 추출

                # 파일 경로가 존재하는지 확인하고 다운로드 버튼 제공
                if os.path.exists(file_path):
                    # 파일을 읽어서 다운로드 버튼으로 제공
                    with open(file_path, 'rb') as file:
                        st.download_button(
                            label="회의록 다운로드",
                            data=file,
                            file_name=os.path.basename(file_path)
                        )
                else:
                    st.write("회의록 파일 경로가 존재하지 않습니다.")
            else:
                st.write("선택된 회의록이이 없습니다.")
    with tabs[2]:
        st.header("회의록 다운로드")
        # Session State에서 데이터 가져오기
        data = st.session_state.data
        return_filepath =''
        if data:        
            attendees = st.text_area("회의 참석자 (한 줄에 한 명씩 입력)", height=100)
            attendees_list = attendees.splitlines()
            if st.button("회의록 생성"):
                if 'file_generated' not in st.session_state:  # 파일 생성 여부 확인
                    # 회의록 생성 로직
                    date = datetime.now().strftime('%Y%m%d_%H%M%S')
                    file_name = f"회의록_{date}"
                    return_filepath = create_meeting_minutes(
                        data['name_topic'],
                        "회의실 A",  # 임시로 고정, 필요에 따라 수정
                        data['mt_date'],
                        attendees_list,  # 임시로 고정, 필요에 따라 수정
                        data['num_spk'],
                        "회의 내용",  # 임시로 고정, 실제 내용으로 대체
                        file_name
                    )
                    st.session_state.file_generated = True  # 파일 생성 완료 표시

            # 파일 다운로드 버튼 생성
            if 'file_generated' in st.session_state:
                if os.path.exists(return_filepath):
                    # 파일 다운로드 버튼 생성
                    st.text(return_filepath)
                    try:
                        with open(return_filepath, 'rb') as file:
                            st.download_button(
                                label="회의록 파일 다운로드",
                                data=file,
                                file_name=return_filepath.split('\\')[-1],
                                mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                            )
                    except FileNotFoundError as e:
                        print(f"파일을 열 수 없습니다: {e}")
                    except PermissionError as e:
                        print(f"파일 접근 권한이 없습니다: {e}")
                    except Exception as e:
                        print(f"알 수 없는 오류 발생: {e}")    
        else:
            st.warning("아직 데이터가 없습니다.")

if not st.session_state['logged_in']:
    login()
else:
    main_app()                 