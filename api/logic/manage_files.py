import shutil
from datetime import datetime
from pathlib import Path


from config import response_dir, PDF_FILENAME

def create_folder():
    try:
        path = response_dir / datetime.now().strftime("%d-%m-%Y-%H:%M:%S")
        Path.mkdir(path)
    except OSError:
        print ("Creation of the directory failed")
    else:
        return path


def delete_folder(dir_path):
    try:
        if Path.is_dir(dir_path):
            shutil.rmtree(dir_path)
    except OSError:
        print ("Deleting the directory %s failed" % dir_path)
    
def get_pdf_path(dir_path):
    return dir_path / PDF_FILENAME
