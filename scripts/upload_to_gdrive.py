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

# ⚠️ 關鍵修改：強制只抓取 "report_" 開頭的檔案，過滤掉沒用的 "market_review_"
report_files = sorted(glob.glob("reports/report_*.md"), key=os.path.getmtime, reverse=True)

if report_files:
    target_file = report_files[0]
    filename = os.path.basename(target_file).replace('.md', '')
    
    media = MediaFileUpload(target_file, mimetype='text/plain', resumable=True)
    
    # 轉換為原生的 Google Docs
    file_metadata = {
        'name': filename,
        'parents': [folder_id],
        'mimeType': 'application/vnd.google-apps.document'
    }
    
    uploaded = service.files().create(body=file_metadata, media_body=media, fields='id, name').execute()
    print(f"Uploaded {uploaded.get('name')} (ID: {uploaded.get('id')}) to Drive as a native Google Doc.")
else:
    print("No valid stock report files found to upload.")
