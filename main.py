import click
import os
from pydrive2.drive import GoogleDrive
from pydrive2.auth import GoogleAuth

gauth = GoogleAuth()

gauth.LoadCredentialsFile("mycreds.txt")

# Check if credentials are not found or expired
if gauth.credentials is None or gauth.access_token_expired:
    # Authenticate if credentials are not found or expired
    gauth.LocalWebserverAuth()
else:
    # Initialize the saved credentials
    gauth.Authorize()

# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth)


def list_files():
    try:
        file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file1 in file_list:
            print(f"title: {file1['title']}, id: {file1['id']}")
    except Exception as e:
        print("Error listing files:", str(e))


def print_tree(node, depth=0):
    indent = '  ' * depth
    print(f"{indent}- {node['title']} ({node['mimeType']})")

    for child in node['children']:
        print_tree(child, depth + 1)


def get_filesystem_tree(drive, folder_id='root', depth=0):
    try:
        files = drive.ListFile({'q': f"'{folder_id}' in parents"}).GetList()

        tree = []
        for file1 in files:
            node = {
                'title': file1['title'],
                'id': file1['id'],
                'mimeType': file1['mimeType'],
                'children': []
            }

            if file1['mimeType'] == 'application/vnd.google-apps.folder':
                node['children'] = get_filesystem_tree(drive, file1['id'], depth + 1)

            tree.append(node)

        return tree

    except Exception as e:
        print("Error getting filesystem tree:", str(e))
        return []


def file_upload(file_path):
    try:
        file_name = os.path.basename(file_path)
        file1 = drive.CreateFile({'title': file_name})
        file1.SetContentFile(file_path)
        file1.Upload()
        print("File uploaded successfully. File ID:", file1['id'])
    except Exception as e:
        print("Error uploading file:", str(e))


def file_details(file_id):
    try:
        file1 = drive.CreateFile({'id': file_id})
        print(f"Details for File ID {file_id}:")
        print(f"Title: {file1['title']}")
        print(f"Description: {file1['description']}")
        print(f"MIME Type: {file1['mimeType']}")
        print(f"File Size: {file1['fileSize']} bytes")
        print(f"Created Date: {file1['createdDate']}")
        print(f"Modified Date: {file1['modifiedDate']}")
    except Exception as e:
        print("Error getting file details:", str(e))


def file_delete(file_id):
    try:
        file1 = drive.CreateFile({'id': file_id})
        file1.Delete()
        print("File deleted successfully.")
    except Exception as e:
        print("Error deleting file:", str(e))


@click.command()
@click.option('--list', is_flag=True, help='List files on Google Drive.')
@click.option('--tree', is_flag=True, help='Show filesystem tree on Google Drive.')
@click.option('--upload', 'upload_file_path', type=click.Path(exists=True), help='Upload a file to Google Drive by providing the file path.')
@click.option('--details', 'file_details_id', help='Get details of a file by providing the file ID.')
@click.option('--delete', 'delete_file_id', help='Delete a file from Google Drive by providing the file ID.')
def main(list, tree, upload_file_path, file_details_id, delete_file_id):
    try:
        if list:
            list_files()
        elif tree:
            root_folder_tree = get_filesystem_tree(drive)
            for node in root_folder_tree:
                print_tree(node)
        elif upload_file_path:
            file_upload(upload_file_path)
        elif file_details_id:
            file_details(file_details_id)
        elif delete_file_id:
            file_delete(delete_file_id)
    except Exception as e:
        print("Error in main function:", str(e))


if __name__ == '__main__':
    main()
