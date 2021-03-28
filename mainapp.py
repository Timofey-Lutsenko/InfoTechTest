import requests as req
import json
import sys
import os
import webbrowser
import logging
import time

import loggercnf
import launcher


logger = logging.getLogger('mainapp')


# Сonstants.
APP_KEY = 'mlfjqpykeprpqso'
APP_SECRET = '3q9y9dk1oav1tvj'
AUTH_URL = f'https://www.dropbox.com/oauth2/authorize?' \
           f'client_id={APP_KEY}&response_type=code'


# Function for obtaining an access token.
def authorization():
    webbrowser.open_new(AUTH_URL)
    print('Click "Continue" on the site that opens, '
          'than click "Allow" '
          'and copy your access token to the next request.')
    auth_code = input('Enter the authorization code: ')
    token_url = "https://api.dropboxapi.com/oauth2/token"
    params = {
        "code": auth_code,
        "grant_type": "authorization_code",
        "client_id": APP_KEY,
        "client_secret": APP_SECRET
    }
    try:
        r = req.post(token_url, data=params)
        response_data = json.loads(r.text)
        logger.info('Access token received successfully.')
        return response_data.get('access_token')
    except ValueError:
        logger.critical('Error getting access token')


# The function that downloads the specified file.
def uploader(src_path_file, dropbox_folder, access_token):
    upload_url = 'https://content.dropboxapi.com/2/files/upload'
    try:
        with open(f'{src_path_file}', 'rb') as f:
            data = f.read()
    except:
        logger.error(f'Impossible to read next file {src_path_file}')
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Dropbox-API-Arg': f'{{"path":{dropbox_folder},'
                           f'"mode": "add",'
                           f'"autorename": true,'
                           f'"mute": false,'
                           f'"strict_conflict": false}}',
        'Content-Type': 'application/octet-stream'
    }
    try:
        r = req.post(upload_url, headers=headers, data=data)
        if r:
            print('File sent successfully.')
            logger.info('File sent successfully.')
        else:
            print('Bad request. Check dst_path.')
            logger.critical(r)
    except:
        print('ER')
    return


# The function that loads the specified file.
def downloader(src_path, dst_path, access_token):
    download_url = 'https://content.dropboxapi.com/2/files/download'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Dropbox-API-Arg': f'{{"path":{src_path}}}'
    }
    r = req.post(download_url, headers=headers)
    try:
        with open(f'{dst_path}', 'wb') as f:
            f.write(r.content)
        if r:
            print('File received successfully.')
            logger.info('File received successfully.')
        else:
            logger.critical(r.text)
    except PermissionError:
        logger.error(f'Permission denied: {dst_path}')
    return


# put/get src_path dst_path
if len(sys.argv) < 3:
    print(f'Invalid number of arguments {len(sys.argv)}.'
          f'\nMust be 3: put or get, '
          f'source path and destination path.')
    logger.error(f'Invalid number of arguments {len(sys.argv)}.')
else:
    # DropBox file size limit for download function.
    dp_size_limiter = 150000000
    key_list = [
        'util',
        'action',
        'src_path',
        'dst_path'
    ]
    argv_list = [i for i in sys.argv]
    user_args_dict = dict(zip(key_list, argv_list))
    if user_args_dict.get('action') == 'get':
        logger.info('Started "downloader" fun.')
        downloader(
            f'"{user_args_dict.get("src_path")}"',
            user_args_dict.get("dst_path"),
            authorization()
        )
    elif user_args_dict.get('action') == 'put':
        if os.path.exists(user_args_dict.get('src_path')):
            if os.path.getsize(user_args_dict.get('src_path')) <= dp_size_limiter:
                logger.info('Started "uploader" fun.')
                uploader(
                    user_args_dict.get("src_path"),
                    f'"{user_args_dict.get("dst_path")}"',
                    authorization()
                )
            else:
                print('Exceeded the file size for the specified function. '
                      'The file should be no more than 150Mb')
                logger.error(f'File size more than 150Mb: '
                             f'{os.path.getsize(user_args_dict.get("src_path"))}')
        else:
            print('The file at the specified path is missing '
                  'or the path is incorrect.')
            logger.error(f'No file or wrong path: '
                         f'{user_args_dict.get("src_path")}')
    else:
        print('File operation not possible. Please, use "get" or "put".')
        logger.error(f'Unknown action "{user_args_dict.get("action")}"')

print('This window will close in 10 seconds.')
time.sleep(10)

