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
    st.title("T-Note : tsis AI 회의록작성")
    username = st.text_input("Login ID")
    password = st.text_input("Password", type="password")

    if st.button("로그인"):
        # 예시로 간단한 인증 로직 (실제 환경에서는 안전한 인증 방법 사용)
        if username == "tsis" and password == "1":
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success("로그인 성공!")
            st.rerun()  # 로그인 성공 시 페이지 새로고침
        else:
            st.error("로그인 실패. 사용자 이름 또는 비밀번호가 잘못되었습니다.")

def main_app():
    # 페이지 레이아웃 변경
    st.set_page_config(layout="wide")
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
    st.title("T-Note : tsis AI 회의록작성")

    #with st.sidebar:
    #    st.write("안녕하세요 tsis 님.")

    # Pandas display 옵션 설정
    pd.set_option('display.max_columns', None)  # 모든 열 표시
    pd.set_option('display.max_rows', None)     # 모든 행 표시
    pd.set_option('display.width', 0)           # 터미널 너비에 맞춰 자동 조정
    pd.set_option('display.max_colwidth', None) # 열 내용이 잘리지 않도록 설정


    # 로딩바 : 단계별 정보를 반환하는 함수
    def progress_steps(step):
        if step == 1:
            return "        1/8 단계: STT 적용 중......."
        elif step == 2:
            return "        2/8 단계: 형태소 분석 중......."
        elif step == 3:
            return "        3/8 단계: 단어 벡터화......."
        elif step == 4:
            return "        4/8 단계: 토픽 모델링/군집화......."
        elif step == 5:
            return "        5/8 단계: 주제 선정 중......."
        elif step == 6:
            return "        6/8 단계: 전체 회의 요약......."
        elif step == 7:
            return "        7/8 단계: 화자별 요약......."
        elif step == 8:
            return "        8/8 단계: 화자별 감정분석......."
        elif step == 9:
            return "        회의록 작성 완료"

    # 단계별 프로그레스바와 텍스트, 이미지를 표시하는 함수
    def show_progress(step):

        step_text = progress_steps(step)
    
        text_placeholder.write(f"### {step_text}")  # 텍스트를 업데이트

        progress_bar.progress(step / total_steps)

        time.sleep(1)
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
        cursor.execute("SELECT document_title, meeting_room, meeting_date, attendees,file_path, insert_date  FROM tn_result_file ORDER BY insert_date desc")
        records = cursor.fetchall()
        return records

    def make_docx(topic, room, date_ymd, username, speakers, title, summary):
        #회의록 생성 로직 
        date = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = f"회의록_{date}"
        retrun_filesize, return_filepath = create_meeting_minutes(
            name_topic,
            meeting_room,  
            mt_date.strftime("%Y-%m-%d"),
            st.session_state['username'], # 임시로 고정, 실제 내용으로 대체
            speakers.splitlines(),
            to_title,   # 임시로 고정, 실제 내용으로 대체
            to_overall_summary,  # 임시로 고정, 실제 내용으로 대체
            file_name
        )
        st.session_state.file_generated = True  # 파일 생성 완료 표시

        # 회의록 내용 db 저장
        connection = connect_to_db()
        res_file_seq = insert_result_file_info_to_db(connection,file_name,retrun_filesize,return_filepath,name_topic,meeting_room,mt_date.strftime("%Y-%m-%d"),speakers)
        insert_meeting_info_to_db(connection, rec_seq, name_topic, num_spk, mt_date, mt_term, res_file_seq)

        connection.commit()
        connection.close()
        return return_filepath

    # 세션데이터
    
    st.session_state.info = {}
    if 'file_info' not in st.session_state:
        st.session_state.file_info = {}
    if 'process_check' not in st.session_state:
        st.session_state.process_check = None
    if 'df_origin' not in st.session_state:
        st.session_state.df_origin = None
    if 'df_origin_analyze' not in st.session_state:
        st.session_state.df_origin_analyze = None
    if 'plot_tfidf_matrix' not in st.session_state:
        st.session_state.plot_tfidf_matrix = None
    if 'plot_lda_topics' not in st.session_state:
        st.session_state.plot_lda_topics = None
    if 'plot_kmeans_clusters' not in st.session_state:
        st.session_state.plot_kmeans_clusters = None
    if 'summarize_title' not in st.session_state:
        st.session_state.summarize_title = None
    if 'summarize_overall' not in st.session_state:
        st.session_state.summarize_overall = None
    if 'summarize_by_speaker' not in st.session_state:
        st.session_state.summarize_by_speaker = None
    if 'analyze_emotion_by_speaker' not in st.session_state:
        st.session_state.analyze_emotion_by_speaker = None

    tabs = st.tabs(["📄 회의녹취록 업로드", "회의녹취록 조회"])

    # 첫번째 탭: 업로드
    with tabs[0]:
        st.header("회의녹취록 업로드")
        uploaded_file = st.file_uploader("녹음된 회의파일을 올려주세요", type=["mp3", "wav", "ogg", "flac", "m4a"])
        st.session_state.file_generated = False
        # 2열 레이아웃 생성
        col1, col2 = st.columns(2)

        if not st.session_state.info:            
            with col1:            
                name_topic = st.text_input("회의 제목을 입력하세요")
                mt_date = st.date_input("회의날짜를 선택하세요.")
                num_spk_opt = ["2","3","4","5","6","7","8","9","10"]
                num_spk = st.selectbox("회의 참여인원을 선택하세요.", options=num_spk_opt)
                st.session_state.info['name_topic'] = name_topic
                st.session_state.info['mt_date'] = mt_date
                st.session_state.info['num_spk'] = num_spk
            with col2:            
                meeting_room = st.text_input("회의실을 입력하세요")
                # 회의 종료 시간을 30분 단위로 선택할 수 있도록 설정
                mt_term_opt = ["30분", "1시간", "1시간30분", "2시간","2시간30분","3시간","3시간30분","4시간","4시간30분","5시간","5시간30분","6시간"]
                mt_term = st.selectbox("회의 진행시간을 선택하세요", options=mt_term_opt)
                speakers_text = st.text_area("참석자 이름을 엔터로 구분하여 입력하세요")
                speakers = speakers_text
                st.session_state.info['meeting_room'] = meeting_room
                st.session_state.info['mt_term'] = mt_term
                st.session_state.info['speakers'] = speakers
        else:
            with col1:            
                name_topic = st.text_input("회의 제목을 입력하세요",value=st.session_state.info.get('name_topic'))
                mt_date = st.date_input("회의날짜를 선택하세요.",value=st.session_state.info.get('mt_date'))
                num_spk_opt = ["2","3","4","5","6","7","8","9","10"]
                num_spk = st.selectbox("회의 참여인원을 선택하세요.", options=num_spk_opt,index=st.session_state.info.get('num_spk'))

            with col2:
                meeting_room = st.text_input("회의실을 입력하세요",value=st.session_state.info.get('meeting_room'))
                # 회의 종료 시간을 30분 단위로 선택할 수 있도록 설정
                mt_term_opt = ["30분", "1시간", "1시간30분", "2시간","2시간30분","3시간","3시간30분","4시간","4시간30분","5시간","5시간30분","6시간"]
                mt_term = st.selectbox("회의 진행시간을 선택하세요", options=mt_term_opt,index=st.session_state.info.get('mt_term'))
                speakers = st.text_area("참석자 이름을 엔터로 구분하여 입력하세요",value=st.session_state.info.get('speakers'))
                
            
        total_steps = 8
        
        progress_bar = st.progress(0)

        # 텍스트와 이미지를 업데이트할 공간 확보
        text_placeholder = st.empty()
        image_placeholder = st.empty()

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
        st.write(f"{st.session_state.process_check}")
        # 한번이라도 프로세스가 실행되었는지 확인
        if not st.session_state.process_check:
            if uploaded_file is not None:

                # "파일 저장" 버튼을 화면에 표시
                if st.button("파일 업로드"):

                    if not name_topic :
                    # 회의제목이 입력되지 않았을 경우 경고 메시지 표시
                        st.warning("회의 제목을 입력해야 합니다.")
                    else :                    
                        #show_progress_with_image(4)
                        st.session_state.process_check = True
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

                        st.success("데이터베이스에 commit 완료") # 디*-버깅 로그                  


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

                        st.session_state.file_info['file_name']=file_name
                        st.session_state.file_info['file_size']=file_size
                        st.session_state.file_info['save_path']=save_path

                        # 데이터프레임 입력 예시
                        show_progress(1)
                        client = ClovaSpeechClient()
                        try:    
                            df_origin = pd.DataFrame(np.array(client.getSttAllResultDf(save_path)))
                            df_origin.columns =  ["화자", "내용"]                            
                        except ValueError as e:
                            print(f"ClovaSpeechClient 오류 발생: {e}")

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
                        # try:
                        #     df_origin['내용'] = df_origin['원문'].apply(correct_spelling)
                        #     st.session_state.df_origin = df_origin
                        # except KeyError as e:
                        #     print(f"ClovaSpeechClient 데이터 없음: {e}")
                            
                        
                        
                        # 전체 회의 제목과 요약을 회의록생성시 가져오기위한 변수
                        to_title =''
                        to_overall_summary=''    
                        
                        # placeholder 생성
                        placeholder = st.empty()
                        
                                                                
                        with st.expander("전체 STT 결과"):
                            #show_progress(1)
                            st.dataframe(data=df_origin,width=None)
                        with st.expander("한국어 형태소 분석"):                    
                            show_progress(2)
                            df_origin['분석된 내용'] = df_origin['내용'].apply(okt_clean)
                            st.write(df_origin)
                            st.session_state.df_origin_analyze = df_origin
                        with st.expander("단어 벡터화"):
                            if st.session_state.plot_tfidf_matrix is None:
                                show_progress(3)
                                tfidf_matrix, vectorizer = tfidf_vectorize(df_origin[['화자', '분석된 내용']])
                                print_date = plot_tfidf_matrix(tfidf_matrix, vectorizer)
                                st.pyplot(print_date)
                                st.session_state.plot_tfidf_matrix = print_date
                        with st.expander("토픽 모델링"):
                            if st.session_state.plot_lda_topics is None:
                                show_progress(4)
                                lda_model = lda_topic_modeling(tfidf_matrix, num_topics=3)
                                print_date=plot_lda_topics(lda_model, vectorizer)
                                st.pyplot(print_date)
                                st.session_state.plot_lda_topics = print_date
                                
                        with st.expander("군집화"):
                            if st.session_state.plot_kmeans_clusters is None:
                                show_progress(4)
                                kmeans_model = kmeans_clustering(tfidf_matrix, num_clusters=3)
                                print_date = plot_kmeans_clusters(kmeans_model, tfidf_matrix)
                                st.pyplot(print_date)
                                st.session_state.plot_kmeans_clusters = print_date
                        with st.expander("전체 회의 제목"):
                            if st.session_state.summarize_title is None:
                                show_progress(5)
                                combined_text = df_origin.apply(lambda row: f"{row['화자']}] {row['내용']}", axis=1).str.cat(sep='\n')
                                title = summarize_title(combined_text)
                                to_title=title
                                st.write(title)
                                st.session_state.summarize_title = title
                        with st.expander("전체 회의 요약"):
                            if st.session_state.summarize_overall is None:
                                show_progress(6)
                                overall_summary = summarize_overall(combined_text)
                                to_overall_summary = overall_summary
                                st.write(overall_summary)
                                st.session_state.summarize_overall = overall_summary
                        with st.expander("화자별 요약"):
                            if st.session_state.summarize_by_speaker is None:
                                show_progress(7)
                                speaker_summaries = summarize_by_speaker(df_origin)
                                for speaker, summary in speaker_summaries.items():
                                    st.write(f"{speaker}: {summary}")
                                st.session_state.summarize_by_speaker=speaker_summaries
                        with st.expander("화자별 감정 분석"):
                            if st.session_state.analyze_emotion_by_speaker is None:
                                show_progress(8)
                                speaker_emotions = analyze_emotion_by_speaker(df_origin)
                                for speaker, emotions in speaker_emotions.items():
                                    st.write(f"{speaker}: {emotions}")
                                st.session_state.analyze_emotion_by_speaker = speaker_emotions
                                # 프로세스 종료시 파일다운로드 추가
                                down_file_path = make_docx(name_topic,meeting_room,mt_date.strftime("%Y-%m-%d"),st.session_state['username'],speakers, to_title, to_overall_summary)
                            
                        # 회의록 다운로드 추가
                        with placeholder.expander("회의록 다운로드 보기▼"):
                            # 파일 다운로드 버튼 생성
                            if st.session_state.file_generated:
                                if os.path.exists(down_file_path):
                                    # 파일 다운로드 버튼 생성
                                    st.text(down_file_path)
                                    try:
                                        with open(down_file_path, 'rb') as file:
                                            st.download_button(
                                                label="회의록 파일 다운로드",
                                                data=file,
                                                file_name=down_file_path.split('\\')[-1],
                                                mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                                            )
                                    except FileNotFoundError as e:
                                        print(f"파일을 열 수 없습니다: {e}")
                                    except PermissionError as e:
                                        print(f"파일 접근 권한이 없습니다: {e}")
                                    except Exception as e:
                                        print(f"알 수 없는 오류 발생: {e}")    
        else:
            st.write(f"{st.session_state.file_info}")
            # 세션 데이터 있는경우
            with st.expander("회의 녹취록 업로드 결과 보기▼"):
                st.divider() 
                st.write(f"◆ 파일명: {st.session_state.file_info.get('file_name')}")
                st.write(f"◆ 파일 크기: {st.session_state.file_info.get('file_size') / (1024 * 1024):.2f} MB")
                st.write(f"◆ 저장 경로: {st.session_state.file_info.get('save_path')}")
                st.divider() 
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"◆ 회의제목: {st.session_state.info.get('name_topic')}")
                    st.write(f"◆ 회의참여인원: {st.session_state.info.get('num_spk')}")
                    st.write(f"◆ 회의날짜: {st.session_state.info.get('mt_date')}")
                    st.write(f"◆ 회의진행시간: {st.session_state.info.get('mt_term')}")
                    st.write(f"◆ 회의주제: T-LAB 주제정하기")
                    st.write(f"◆ 회의요약: T-LAB 주제를 정해야해서 회의를 함.")
                with col2:
                    # 이미지
                    #display_word_cloud(result)
                    st.image("https://static.streamlit.io/examples/dice.jpg", caption="Dice Image")           
            
            # 전체 회의 제목과 요약을 회의록생성시 가져오기위한 변수
                to_title =''
                to_overall_summary=''    
                
                # placeholder 생성
                placeholder = st.empty()
                
                                                        
                with st.expander("전체 STT 결과"):                        
                    st.write(st.session_state.df_origin)
                with st.expander("한국어 형태소 분석"):
                    st.write(st.session_state.df_origin_analyze)
                with st.expander("단어 벡터화"):
                    st.pyplot(st.session_state.plot_tfidf_matrix)
                with st.expander("토픽 모델링"):
                    st.pyplot(st.session_state.plot_lda_topic)                            
                with st.expander("군집화"):
                    st.pyplot(st.session_state.plot_kmeans_clusters)
                with st.expander("전체 회의 제목"):
                    st.write(st.session_state.summarize_title)
                with st.expander("전체 회의 요약"):
                    st.write(st.session_state.summarize_overall)
                with st.expander("화자별 요약"):
                    for speaker, summary in st.session_state.summarize_by_speaker.items():
                        st.write(f"{speaker}: {summary}")
                with st.expander("화자별 감정 분석"):
                    for speaker, emotions in st.session_state.analyze_emotion_by_speaker.items():
                        st.write(f"{speaker}: {emotions}")
                            
                    
                # 회의록 다운로드 추가
                with placeholder.expander("회의록 다운로드 보기▼"):
                    # 파일 다운로드 버튼 생성
                    if st.session_state.file_generated:
                        if os.path.exists(down_file_path):
                            # 파일 다운로드 버튼 생성
                            st.text(down_file_path)
                            try:
                                with open(down_file_path, 'rb') as file:
                                    st.download_button(
                                        label="회의록 파일 다운로드",
                                        data=file,
                                        file_name=down_file_path.split('\\')[-1],
                                        mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                                    )
                            except FileNotFoundError as e:
                                print(f"파일을 열 수 없습니다: {e}")
                            except PermissionError as e:
                                print(f"파일 접근 권한이 없습니다: {e}")
                            except Exception as e:
                                print(f"알 수 없는 오류 발생: {e}") 

    st.write(f"{st.session_state.process_check}")
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
            df = pd.DataFrame(records, columns=["회의록 제목","회의실","회의날짜","참석자","파일 경로","업로드 일시"])
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
            st.write("선택된 회의 녹취록 : ", selected_row)

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

if not st.session_state['logged_in']:
    login()
else:
    main_app()                 
