import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


# Load service account credentials from the environment variable
credentials_json = json.loads(os.getenv('SERVICE_ACCOUNT_CREDENTIALS'))
credentials = service_account.Credentials.from_service_account_info(
    credentials_json, scopes=['https://www.googleapis.com/auth/drive'])

# Create the Drive service
drive_service = build('drive', 'v3', credentials=credentials)


def get_file_parent_path(file_id):
    try:
        file_metadata = drive_service.files().get(
            fileId=file_id, fields='id, name, parents').execute()

        # Get the list of parent folders' IDs associated with the file
        parent_ids = file_metadata.get('parents', [])
        path = []
        for parent_id in parent_ids:
            parent_folder = drive_service.files().get(
                fileId=parent_id, fields='name').execute()
            path.append(parent_folder.get('name', 'Unknown'))

        path.append(file_metadata.get('name', 'Unknown'))

        return "/".join(path) if len(path) > 0 else ""

    except Exception as e:
        print(f"Error getting file parent path")
        return ""


def main():

    file_ids = [
        '1cxSRFE1MZ_FdM7bgCBcNVe02xqxziiLs',  # on twik
        '1fUNwDB8S_OLW83bjO_KB9G7rDQXTUSjJ',  # on pfe
        # '15Sip8RlcZdBGRfwt1Sv_83HLYgngKm3y'  # on nc
    ]

    file_path = 'main.pdf'

    file_metadata = {
        'name': os.path.basename(file_path)
    }

    media = MediaFileUpload(file_path, mimetype='application/pdf')

    # Upload the new versions of the files
    for file_id in file_ids:
        path = get_file_parent_path(file_id)
        print(f'Uploading new version to {path}')
        updated_file = drive_service.files().update(
            fileId=file_id, body=file_metadata, media_body=media).execute()

        # Print the updated file information
        print(
            f"Updated File [name: {updated_file['name']}, type: {updated_file['mimeType']}]")


if __name__ == "__main__":
    main()
