import os
import glob
from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn
from opencc import OpenCC
import markdown
from bs4 import BeautifulSoup

def process_and_format():
    # 尋找最新生成的 Markdown 報告
    files = sorted(glob.glob("reports/report_*.md"), key=os.path.getmtime, reverse=True)
    if not files:
        print("未找到報告檔案")
        return
        
    md_file = files[0]
    with open(md_file, 'r', encoding='utf-8') as f:
        content_sc = f.read()

    # 1. 簡體轉繁體 (s2tw.json: 簡體到台灣正體)
    cc = OpenCC('s2twp')
    content_tc = cc.convert(content_sc)

    # 將 Markdown 轉為 HTML 以利解析
    html = markdown.markdown(content_tc, extensions=['tables'])
    soup = BeautifulSoup(html, 'html.parser')

    # 2. 建立 Word 文件並設定「微軟正黑體」與字型大小
    doc = Document()
    style = doc.styles['Normal']
    style.font.name = 'Microsoft JhengHei'
    style.font.size = Pt(11)
    style.element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft JhengHei')

    for element in soup:
        if element.name in ['h1', 'h2', 'h3', 'h4']:
            level = int(element.name[1]) - 1
            heading = doc.add_heading(element.text, level=level)
            # 設定標題也是微軟正黑體
            heading.style.font.name = 'Microsoft JhengHei'
            heading.style.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
            heading.style.element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft JhengHei')
            
        elif element.name == 'p':
            doc.add_paragraph(element.text)
            
        elif element.name == 'ul':
            for li in element.find_all('li'):
                doc.add_paragraph(li.text, style='List Bullet')
                
        elif element.name == 'table':
            rows = element.find_all('tr')
            if rows:
                cols = len(rows[0].find_all(['th', 'td']))
                table = doc.add_table(rows=0, cols=cols)
                table.style = 'Light Shading Accent 1'
                for row in rows:
                    cells = row.find_all(['th', 'td'])
                    row_obj = table.add_row()
                    for i, cell in enumerate(cells):
                        row_obj.cells[i].text = cell.text

    # 儲存為 docx
    out_file = md_file.replace('.md', '.docx')
    doc.save(out_file)
    print(f"已成功轉換並排版為繁體 Word 檔: {out_file}")

if __name__ == "__main__":
    process_and_format()
