"""
TODO:represent tree and help in cli
TODO:use ccourse outcome topics (cover almost everything) 
"""
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



# def list_files():
#     file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
#     for file1 in file_list:
#         print('title: %s, id: %s' % (file1['title'], file1['id']))
#     print("Listeddd")
#     for file_list in drive.ListFile({'q': 'trashed=true', 'maxResults': 10}):
#         print('Received %s files from Files.list()' % len(file_list))  # <= 10
#     for file1 in file_list:
#         print('title: %s, id: %s' % (file1['title'], file1['id']))


def get_filesystem_tree(drive, folder_id='root', depth=0):
   
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


root_folder_tree = get_filesystem_tree(drive)
print(root_folder_tree)




def file_upload():

    file1 = drive.CreateFile({'title': 'Hello.txt'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
    file1.SetContentString('Hello World!') # Set content of the file from given string.
    file1.Upload()
    print("done")
