import os
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

target_file = "reports/Daily_Stock_Analysis_Report.docx"

if os.path.exists(target_file):
    # 您可以在這裡自訂存入 Google Drive 後的檔名
    filename = "今日台股決策儀表板分析_繁體版" 
    
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
