# pr_agent/drive_client.py

import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
#from pr_agent.settings import GDRIVE_CREDFILE, GDRIVE_SCOPES

from pr_agent.settings import settings  

credfile = settings.GDRIVE_CRED_FILE
gdrive_scope = settings.GDRIVE_SCOPES

def get_drive_service():
    """
    Returns an authenticated Drive API client (service account).
    """
    creds = service_account.Credentials.from_service_account_file(
        credfile, scopes=gdrive_scope
    )
    return build("drive", "v3", credentials=creds)

def list_files_in_folder(folder_id: str):
    """
    List all non‐folder files in the given Drive folder ID.
    Returns: a list of dicts, each { "id": fileId, "name": fileName, "modifiedTime": RFC3339 }.
    """
    service = get_drive_service()
    results = []
    page_token = None
    query = f"'{folder_id}' in parents and trashed = false"
    while True:
        resp = service.files().list(
            q=query,
            spaces="drive",
            fields="nextPageToken, files(id, name, mimeType, modifiedTime)",
            pageToken=page_token
        ).execute()
        results.extend(resp.get("files", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return results

def fetch_file_bytes(file_id: str):
    """
    Download a file’s raw bytes from Drive into an in‐memory BytesIO buffer.
    Returns: io.BytesIO positioned at start.
    """
    service = get_drive_service()
    request = service.files().get_media(fileId=file_id)
    buffer = io.BytesIO()
    downloader = MediaIoBaseDownload(buffer, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    buffer.seek(0)
    return buffer
