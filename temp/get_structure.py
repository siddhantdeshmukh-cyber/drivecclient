import listt
def print_folder_structure(folder, indentation=""):
    print(f"{indentation}{folder['title']} (ID: {folder['id']})")

    if 'children' in folder:
        for child in folder['children']:
            print_folder_structure(child, indentation + "├── ")

# Your provided data
data = listt.list

# Print the folder structure
print_folder_structure(data[0])
