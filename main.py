import click
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


def file_upload():
    try:
        file1 = drive.CreateFile({'title': 'Hello.txt'})
        file1.Upload()
        print("File uploaded successfully. File ID:", file1['id'])
    except Exception as e:
        print("Error uploading file:", str(e))


@click.command()
@click.option('--list', is_flag=True, help='List files on Google Drive.')
@click.option('--tree', is_flag=True, help='Show filesystem tree on Google Drive.')
@click.option('--upload', is_flag=True, help='Upload a file to Google Drive.')
def main(list, tree, upload):
    try:
        if list:
            list_files()
        elif tree:
            root_folder_tree = get_filesystem_tree(drive)
            for node in root_folder_tree:
                print_tree(node)
        elif upload:
            file_upload()
    except Exception as e:
        print("Error in main function:", str(e))


if __name__ == '__main__':
    main()
