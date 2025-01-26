import os
import shutil
import git

# Path to your local repository
repo_path: str = 'https://github.com/ckfnr/Projekt-Debbie'

# Path to the target folder within the repository
target_folder: str = os.path.join(repo_path, 'Software')

blacklisted_items: list[str] = []

# List of files/folders to upload
files_to_upload: list[str] = []

# Function to copy files to the target folder
def copy_files_to_target(files, target_folder):
    os.makedirs(target_folder, exist_ok=True)

    for file in files:
        if os.path.isdir(file):
            shutil.copytree(file, os.path.join(target_folder, os.path.basename(file)))
        else:
            shutil.copy2(file, target_folder)

# Function to add and commit files
def add_and_commit_files(repo_path, target_folder):
    repo = git.Repo(repo_path)
    repo.index.add([target_folder])
    repo.index.commit("Add files and folders to Software folder")

# Function to push changes
def push_changes(repo_path):
    repo = git.Repo(repo_path)
    origin = repo.remote(name='origin')
    origin.push()

if __name__ == "__main__":
    copy_files_to_target(files_to_upload, target_folder)
    add_and_commit_files(repo_path, target_folder)
    push_changes(repo_path)
