import os
import glob
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

folder_id = os.environ.get("FOLDER_ID", "1b9TR9AyctrxsQ2Fl4MaqjVosiIrHK3o6")

# 使用您個人的授權碼進行登入，完全避開服務帳號的 0 容量限制
creds = Credentials(
    token=None,
    refresh_token=os.environ["GDRIVE_REFRESH_TOKEN"],
    token_uri="https://oauth2.googleapis.com/token",
    client_id=os.environ["GDRIVE_CLIENT_ID"],
    client_secret=os.environ["GDRIVE_CLIENT_SECRET"]
)

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
else:
    print("No report files found to upload.")
