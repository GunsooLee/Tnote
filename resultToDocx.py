from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime
import os

def create_meeting_minutes(title, meeting_room, date, writer, attendees, subject, contents, file_name='Tnote_'+datetime.now().strftime('%Y%m%d_%H%M%S')):
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

    # 문서 정보
    document.add_heading(title, 0)
    table = document.add_table(rows=1, cols=4)
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = '일시'
    hdr_cells[1].text = date
    hdr_cells[2].text = '장소'
    hdr_cells[3].text = meeting_room
    
    row_cells = table.add_row().cells
    row_cells[0].text = '참석자'
    row_cells[1].text = attendees
    row_cells[2].text = '작성자'
    row_cells[3].text = writer

    # 회의 주제
    document.add_heading('회의 주제', level=1)
    document.add_paragraph(subject)

    # 회의 주제
    document.add_heading('회의 내용', level=1)
    document.add_paragraph(contents)

    # 파일 저장 
    file_path = 'result_file/' + file_name + '.docx'
    document.save(file_path)
    
    #파일 사이즈
    file_size =  os.path.getsize(file_path)
    file_size = file_size / (1024)
    return file_size, file_path
