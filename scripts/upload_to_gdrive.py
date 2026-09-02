import os
import glob
import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

folder_id = os.environ.get("FOLDER_ID", "1b9TR9AyctrxsQ2Fl4MaqjVosiIrHK3o6")

# 免金鑰驗證：自動抓取 GitHub Actions 注入的憑證
creds, project = google.auth.default()
service = build('drive', 'v3', credentials=creds)

# 取得 reports/ 最新生成的檔案
report_files = sorted(glob.glob("reports/*.*"), key=os.path.getmtime, reverse=True)
if report_files:
    target_file = report_files[0]
    filename = os.path.basename(target_file)
    media = MediaFileUpload(target_file, resumable=True)
    file_metadata = {'name': filename, 'parents': [folder_id]}
    uploaded = service.files().create(body=file_metadata, media_body=media, fields='id, name').execute()
    print(f"Uploaded {uploaded.get('name')} (ID: {uploaded.get('id')}) to Drive.")
