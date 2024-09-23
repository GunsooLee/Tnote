from docx import Document
from docx.shared import Inches, Pt
from datetime import datetime

def create_meeting_minutes(title, meeting_room, date, writer, time, location, attendees, contents):
    document = Document()

    # 제목 설정 (가운데 정렬)
    paragraph = document.add_paragraph()
    run = paragraph.add_run(title)
    run.font.size = Pt(16)
    run.bold = True
    paragraph.alignment = 1  # 1: center

    # 표 생성
    table = document.add_table(rows=4, cols=3)
    table.style = 'Table Grid'
    table.cell(0, 0).text = '회의실'
    table.cell(0, 1).text = '일자'
    table.cell(0, 2).text = '작성자'
    table.cell(1, 0).text = meeting_room
    table.cell(1, 1).text = date
    table.cell(1, 2).text = writer
    table.cell(2, 0).text = '일시'
    table.cell(2, 1).text = time
    table.cell(2, 2).text = '회의장소'
    table.cell(3, 0).text = location
    table.cell(3, 1).text = '참석자'
    table.cell(3, 2).text = attendees

    # 회의 내용
    document.add_paragraph()
    paragraph = document.add_paragraph()
    run = paragraph.add_run('회의록 내용')
    run.font.size = Pt(14)
    run.bold = True

    # 큰 네모칸 (여러 줄 추가 가능)
    for _ in range(10):  # 10줄 예시
        document.add_paragraph()

    # 회의 주제
    paragraph = document.add_paragraph()
    run = paragraph.add_run('회의 주제')
    run.font.size = Pt(12)
    run.bold = True

    # 파일 저장
    document.save('Tnote/result_file/meeting_minutes.docx')

# 예시 실행
title = 'TNOTE 회의록'
meeting_room = 'A 회의실'
date = datetime.now().strftime('%Y-%m-%d')
writer = '홍길동'
time = datetime.now().strftime('%H:%M')
location = '본사'
attendees = '홍길동, 이순신, 강감찬'
contents = '회의 내용을 여기에 작성하세요.'

create_meeting_minutes(title, meeting_room, date, writer, time, location, attendees, contents)