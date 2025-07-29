# pr_agent/connectors/gdrive_connector.py

from typing import List, Set
from pr_agent.drive_client import list_files_in_folder, fetch_file_bytes
from pr_agent.connectors.base_connector import SourceItem

def _gather_all_files_recursively(folder_id: str) -> List[dict]:
    """
    Returns a flat list of file‐metadata dicts for every non‐folder item under `folder_id`,
    descending into subfolders recursively.
    Each dict has keys: { 'id': fileId, 'name': fileName, 'modifiedTime': ... }.
    """
    all_files = []
    # 1) List everything directly in this folder
    results = list_files_in_folder(folder_id)
    #print(f"\nContents of folder {folder_id}:") # <- debug

    for meta in results:
        #print("  •", meta["name"], "→", meta["mimeType"])  # <— debug
        file_id   = meta["id"]
        name      = meta["name"]
        mime_type = meta.get("mimeType", "")

        if mime_type == "application/vnd.google-apps.folder":
            # Found a subfolder: recurse into it
            subfolder_id = file_id
            nested = _gather_all_files_recursively(subfolder_id)
            all_files.extend(nested)
        else:
            # It’s a normal file (PDF, DOCX, TXT, etc.)
            all_files.append(meta)

    return all_files


def list_new_items(existing_ids: Set[str], root_folder_id: str) -> List[SourceItem]:
    """
    Now uses a recursive gather to find every file under root_folder_id (any depth).
    """
    items: List[SourceItem] = []

    # 1) Recursively gather all file-metadata dicts under root_folder_id
    all_file_meta = _gather_all_files_recursively(root_folder_id)

    for meta in all_file_meta:
        file_id   = meta["id"]
        filename  = meta["name"]
        modified  = meta.get("modifiedTime", "")

        file_id   = meta["id"]
        if file_id in existing_ids:
             continue

        filename  = meta["name"]
        modified  = meta.get("modifiedTime", "")

        # 3) Download the file’s bytes
        buffer = fetch_file_bytes(file_id)  # BytesIO

        # 4) Wrap into a SourceItem
        item = SourceItem(
            id=file_id,
            name=filename,
            raw_bytes=buffer,
            last_modified=modified,
            source_system="GoogleDrive"
        )
        items.append(item)

    return items
