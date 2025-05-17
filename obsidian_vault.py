import os
import sys
import re
from datetime import datetime
from pydantic import BaseModel, model_validator 

class FileName(BaseModel):
    file: str
    timestamp: str = ""
    renamed_file: str =  ""

    @model_validator(mode='before')
    @classmethod
    def process_file_name(cls, data: dict) -> dict:
        file_path = data.get('file')
        if file_path:
            try:
                # Get timestamp
                timestamp = os.stat(file_path, follow_symlinks=False)
                timestamp_str = datetime.fromtimestamp(timestamp.st_birthtime).strftime("%Y%m%d")
                data['timestamp'] = timestamp_str

                # Replace whitespace for renamed_file
                file_base_name = os.path.basename(file_path)
                data['renamed_file'] = file_base_name.replace(" ", "-")

            except FileNotFoundError:
                print(f"Warning: File not found: {file_path}. Timestamp and renamed_file will be empty.")
                data['timestamp'] = ""
                data['renamed_file'] = ""
            except Exception as e:
                print(f"Warning: Error processing {file_path}: {e}. Timestamp and renamed_file might be incomplete.")
                data['timestamp'] = ""
                data['renamed_file'] = ""
        return data
   
    def has_timestamp_name(self) -> bool:
        match = re.search(r'(\d{4})(\d{2})(\d{2})', self.file)
        if match:
            return False
        return True 

    def rename_file(self) -> None:
        file_path= os.path.dirname(self.file)
        new_name = f"{self.timestamp}-{self.renamed_file}"
        new_full_path = os.path.join(file_path, new_name)
        try:
            print(f"Renaming {self.file} to {new_name}")
            os.rename(self.file, os.path.join(file_path, new_name))
            self.file = new_full_path
        except Exception as e:
            print(f"Error renaming file {self.file}: {e}")



def walk_directory(path: str) -> list:
    """
    Walks through the directory and returns a list of all files.
    """
    file_list = []
    for root, _, files in os.walk(path):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

def main(path: str):
    print(f"Running script on {path}")
    file_list = walk_directory(path)
    count = 0
    for file in file_list:
        f = FileName(file=file)
        if f.has_timestamp_name():
            f.rename_file()
            count += 1
    print(f"Modified {count} files")
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python obsidian_vault.py <path>")
        sys.exit(1)
    path = sys.argv[1]
    main(path)


