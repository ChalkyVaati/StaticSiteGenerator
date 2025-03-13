import os
import shutil


def copy_files_recursive(source_dir_path, dest_dir_path):
    # Check if source exists
    if not os.path.exists(source_dir_path):
        print(f"Source directory {source_dir_path} doesn't exist")
        return
    
    # Create destination if it doesn't exist
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)
    
    # Copy files
    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)

            