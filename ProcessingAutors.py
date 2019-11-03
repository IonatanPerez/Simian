import os
import shutil
from Settings import tempAutorFolder, localfolder

src_files = os.listdir(localfolder)
for file_name in src_files:
    full_file_name = os.path.join(localfolder, file_name)
    if os.path.isfile(full_file_name):
        shutil.copy(full_file_name, tempAutorFolder)