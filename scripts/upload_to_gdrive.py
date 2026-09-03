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

# ⚠️ 改為抓取最新的繁體中文 docx 檔案
report_files = sorted(glob.glob("reports/report_*.docx"), key=os.path.getmtime, reverse=True)

if report_files:
    target_file = report_files[0]
    filename = os.path.basename(target_file).replace('.docx', '')
    
    # 指定上傳格式為 Word，讓 Google 自動轉為可編輯的 Google Docs
    media = MediaFileUpload(target_file, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document', resumable=True)
    
    file_metadata = {
        'name': filename,
        'parents': [folder_id],
        'mimeType': 'application/vnd.google-apps.document'
    }
    
    uploaded = service.files().create(body=file_metadata, media_body=media, fields='id, name').execute()
    print(f"Uploaded {uploaded.get('name')} (ID: {uploaded.get('id')}) to Drive as a native Google Doc.")
else:
    print("No docx report files found to upload.")
