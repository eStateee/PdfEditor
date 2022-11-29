import os

from google_drive_downloader import GoogleDriveDownloader as gdd

files = {
    'after.pdf': '1cQo-siTKvIbDLGKVcZLPX85GgiK5Yhqf',
    'before.pdf': '1eiNyOupXXf8HpTrJvpLBQJiD09dFTOZQ',
    'before_1.pdf': '15Y3DP-IoKtfxSllF4mbM4Tfmipw0-_g4',
    'company_info.csv': '1GCNOj2LcazPU24l_3DUTmSlqfTYGQUuT'
}
dirs = ('temp', 'res', 'templates')

cur = os.curdir
for i_dir in dirs:
    if i_dir not in os.listdir(cur):
        path = os.path.join(cur, i_dir)
        os.mkdir(path)
template_path = os.path.join(os.curdir, 'templates')
for k, v in files.items():
    gdd.download_file_from_google_drive(file_id=v,
                                        dest_path=f'{template_path}/{k}',

                                        )
