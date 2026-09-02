import os
import glob
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

folder_id = os.environ.get("FOLDER_ID", "1b9TR9AyctrxsQ2Fl4MaqjVosiIrHK3o6")

# OAuth 驗證
creds = Credentials(
    token=None,
    refresh_token=os.environ["GDRIVE_REFRESH_TOKEN"],
    token_uri="https://oauth2.googleapis.com/token",
    client_id=os.environ["GDRIVE_CLIENT_ID"],
    client_secret=os.environ["GDRIVE_CLIENT_SECRET"]
)

service = build('drive', 'v3', credentials=creds)

# 抓取剛才由背景產生的 .docx 檔案
report_files = sorted(glob.glob("reports/*.docx"), key=os.path.getmtime, reverse=True)

if report_files:
    target_file = report_files[0]
    
    # 讓檔名更乾淨，去掉副檔名 (例如把 market_review_20260902.docx 變成 market_review_20260902)
    filename = os.path.basename(target_file).replace('.docx', '')
    
    # 原始檔案是 Word 格式
    media = MediaFileUpload(target_file, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document', resumable=True)
    
    # 關鍵魔法：在 mimeType 明確指定 'application/vnd.google-apps.document'，Google 就會自動把它無縫轉換成 Google 文件！
    file_metadata = {
        'name': filename,
        'parents': [folder_id],
        'mimeType': 'application/vnd.google-apps.document'
    }
    
    uploaded = service.files().create(body=file_metadata, media_body=media, fields='id, name').execute()
    print(f"Uploaded {uploaded.get('name')} (ID: {uploaded.get('id')}) to Drive as Google Doc.")
else:
    print("No report files found to upload.")
