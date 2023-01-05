import os
from constants import TEMPLATES_PATH
from google_drive_downloader import GoogleDriveDownloader as gdd

files = {
    'after.pdf': '1cQo-siTKvIbDLGKVcZLPX85GgiK5Yhqf',
    'before.pdf': '1eiNyOupXXf8HpTrJvpLBQJiD09dFTOZQ',
    'company_info.csv': '1GCNOj2LcazPU24l_3DUTmSlqfTYGQUuT'
}
dirs = ('temp', 'res', 'templates')

root_path = os.path.abspath(os.path.join('../'))
print(root_path)
for i_dir in dirs:
    if i_dir not in os.listdir(root_path):
        path = os.path.join(root_path, i_dir)
        os.mkdir(path)

for k, v in files.items():
    gdd.download_file_from_google_drive(file_id=v,
                                        dest_path=f'{TEMPLATES_PATH}/{k}',)
