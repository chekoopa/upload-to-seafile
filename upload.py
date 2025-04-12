import os
import requests
from glob import glob
import sys

def main():
    try:
        # Get environment variables
        server = os.environ['SEAFILE_SERVER']
        username = os.environ['SEAFILE_USER']
        password = os.environ['SEAFILE_PASS']
        repo_id = os.environ['SEAFILE_REPO_ID']
        remote_path = os.environ['REMOTE_PATH']
        local_path = os.environ['LOCAL_PATH']
        overwrite = os.environ['OVERWRITE'].lower() == 'true'

        # Get auth token
        auth_url = f'{server}/api2/auth-token/'
        resp = requests.post(auth_url, data={'username': username, 'password': password})
        resp.raise_for_status()
        token = resp.json()['token']
        headers = {'Authorization': f'Token {token}'}

        # Get upload link
        upload_url = f'{server}/api2/repos/{repo_id}/upload-link/'
        resp = requests.get(upload_url, headers=headers)
        resp.raise_for_status()
        upload_link = resp.json()

        # Upload each file
        for file_path in glob(local_path):
            file_name = os.path.basename(file_path)
            
            # Check if file exists if overwrite is false
            if not overwrite:
                check_url = f'{server}/api2/repos/{repo_id}/file/detail/?p={os.path.join(remote_path, file_name)}'
                check_resp = requests.get(check_url, headers=headers)
                if check_resp.status_code == 200:
                    print(f'File {file_name} already exists and overwrite is false. Skipping.')
                    continue

            with open(file_path, 'rb') as f:
                files = {'file': f, 'parent_dir': remote_path}
                resp = requests.post(upload_link, files=files, headers=headers)
                resp.raise_for_status()
                print(f'Successfully uploaded {file_name} to {remote_path}')

    except requests.exceptions.RequestException as e:
        print(f'Error uploading files: {str(e)}', file=sys.stderr)
        sys.exit(1)
    except KeyError as e:
        print(f'Missing required environment variable: {str(e)}', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
