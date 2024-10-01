from docx import Document
from datetime import datetime
import os

def create_meeting_minutes(title, meeting_room, date, writer, attendees, contents, file_name='Tnote_'+datetime.now().strftime('%Y%m%d_%H%M%S')):
    """_summary_
    Args:
        title (string): 회의록 문서 제목
        meeting_room (string): 회의실 
        date (string): 회의 날짜
        writer (string): 작성자
        attendees (string): 참석 인원
        contents (string): 회의 내용
        file_name (string): 다운로드 파일 이름
    """

    document = Document()

    # 제목 설정 (가운데 정렬)
    paragraph = document.add_paragraph()
    run = paragraph.add_run(title)
    run.bold = True
    paragraph.alignment = 1  # 1: center

    # 표 생성
    table = document.add_table(rows=3, cols=4)
    table.style = 'Table Grid'
    table.cell(0, 0).text = '회의실'
    table.cell(0, 1).text = meeting_room
    table.cell(0, 2).text = '일자'
    table.cell(0, 3).text = date

    table.cell(1, 0).text = '작성자'
    table.cell(1, 1).text = writer
    table.cell(1, 2).text = '참석인원'
    table.cell(1, 3).text = "\n".join(attendees)

    # 회의 내용
    document.add_paragraph()
    paragraph = document.add_paragraph()
    run = paragraph.add_run('회의 내용')
    run.bold = True

    # 회의 주제
    paragraph = document.add_paragraph(contents)

    # 파일 저장 
    file_path = 'result_file/' + file_name + '.docx'
    document.save(file_path)
    
    #파일 사이즈
    file_size =  os.path.getsize(file_path)
    file_size = file_size / (1024 * 1024)
    return file_size, file_path
